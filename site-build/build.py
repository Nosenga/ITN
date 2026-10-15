#!/usr/bin/env python3
"""
Build the ITN Chapters 5–7 study website from the source PDFs.

- Extracts EVERY line of text from every page (slides), reconstructs
  titles / kickers / bullets / headings / code blocks.
- Extracts every figure image and embeds it (base64 WebP) so pages are
  fully self-contained (work in sandboxed preview + offline).
- Builds a passage corpus for the client-side "mini AI" ask box.
- Verifies at the end that no extracted line was left out of the HTML.
"""
import base64
import hashlib
import html as H
import importlib.util
import io
import json
import os
import re
import sys

import pymupdf
from PIL import Image

ROOT = "/home/user"
UPLOADS = os.path.join(ROOT, "uploads")
OUT = os.path.join(ROOT, "itn-site")
BUILD = os.path.join(ROOT, "site-build")

CSS = open(os.path.join(BUILD, "style.css"), encoding="utf-8").read()
BOTJS = open(os.path.join(BUILD, "bot.js"), encoding="utf-8").read()
IPV4JS = open(os.path.join(BUILD, "ipv4.js"), encoding="utf-8").read()
LABJS = open(os.path.join(BUILD, "lab.js"), encoding="utf-8").read()
PTJS = open(os.path.join(BUILD, "pt.js"), encoding="utf-8").read()
IOSJS = open(os.path.join(BUILD, "ios.js"), encoding="utf-8").read()
EXAMJS = open(os.path.join(BUILD, "exam.js"), encoding="utf-8").read()


# ---------------- chapter revision kit (site-build/revision/chNN.py) ----------------
def load_revision():
    """Load per-chapter revision data. Each chNN.py defines DATA with the keys
    overview/objectives/concepts/definitions/explanations/comparisons/facts/
    questions/misunderstandings/quick (see revision/README)."""
    data = {}
    rev_dir = os.path.join(BUILD, "revision")
    if not os.path.isdir(rev_dir):
        return data
    for fn in sorted(os.listdir(rev_dir)):
        m = re.fullmatch(r"ch(\d{2})\.py", fn)
        if not m:
            continue
        path = os.path.join(rev_dir, fn)
        spec = importlib.util.spec_from_file_location("rev_ch" + m.group(1), path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            data[int(m.group(1))] = mod.DATA
        except Exception as e:                       # pragma: no cover
            print(f"  ! revision/ch{m.group(1)}.py failed to load: {e}")
    return data


REVISION = load_revision()


# ---------------- Packet Tracer prep kit (site-build/ptlabs.py) ----------------
def load_ptlabs():
    """Load the PT preparation content module (LABS + render_pt_body)."""
    path = os.path.join(BUILD, "ptlabs.py")
    if not os.path.isfile(path):
        return None
    spec = importlib.util.spec_from_file_location("ptlabs", path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        return mod
    except Exception as e:                       # pragma: no cover
        print(f"  ! ptlabs.py failed to load: {e}")
        return None


PTLABS = load_ptlabs()


# ---------------- exam practice bank (site-build/exam.py) ----------------
def load_exam():
    """Load the exam question bank builder (build_bank + render_exam_body)."""
    path = os.path.join(BUILD, "exam.py")
    if not os.path.isfile(path):
        return None
    spec = importlib.util.spec_from_file_location("exambank", path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        mod.BANK = mod.build_bank()
        return mod
    except Exception as e:                       # pragma: no cover
        print(f"  ! exam.py failed to load: {e}")
        return None


EXAMMOD = load_exam()

BUL = set("▪•●‣∙⁃")
def is_pua(ch):
    o = ord(ch)
    return 0xE000 <= o <= 0xF8FF

def strip_glyphs(s):
    s = s.replace("\u200b", "").replace("\u200d", "").replace("\xa0", " ")
    while s and (s[0] in BUL or is_pua(s[0])):
        s = s[1:].lstrip(" ")
    return s

def norm(s):
    s = strip_glyphs(str(s))
    return re.sub(r"\s+", " ", s).strip()

CHAPTERS = [
    dict(
        n=1, file="chapter1.html",
        pdf=os.path.join(UPLOADS, "Chapter 1_ITN_Exploring the Network.pdf"),
        title="Exploring the Network",
        blurb="How networks connect our world: networks of many sizes, network components, "
              "media and topologies, LANs, WANs and the Internet, converged and reliable "
              "networks with QoS and security, and the changing network environment.",
        topics=["Networks of all sizes, clients & servers", "Components, media & topologies",
                "LANs, WANs & the Internet", "Converged, reliable networks & QoS",
                "Security threats & solutions"],
        sections=[
            dict(id="s11", title="1.1 Globally Connected", pages=(3, 7)),
            dict(id="s12", title="1.2 LANs, WANs, and the Internet", pages=(8, 22)),
            dict(id="s13", title="1.3 The Network as a Platform", pages=(23, 33)),
            dict(id="s14", title="1.4 The Changing Network Environment", pages=(34, 40)),
            dict(id="s15", title="Chapter 1 Summary", pages=(41, 42)),
        ],
        dividers={3, 8, 23, 34},
    ),
    dict(
        n=2, file="chapter2.html",
        pdf=os.path.join(UPLOADS, "Chapter 2_ITN_Configuring a Network OS.pdf"),
        title="Configuring a Network OS",
        blurb="Network operating systems and the Cisco IOS CLI — console and remote access "
              "methods, IOS modes and command structure, basic device configuration and "
              "security, addressing schemes and verifying connectivity.",
        topics=["The IOS and its functions", "Console, Telnet & SSH access",
                "IOS modes & command structure", "Hostnames, passwords & banners",
                "SVI addressing & verification"],
        sections=[
            dict(id="s21", title="2.1 IOS Bootcamp", pages=(3, 22)),
            dict(id="s22", title="2.2 Getting Basic", pages=(23, 31)),
            dict(id="s23", title="2.3 Addressing Schemes", pages=(32, 39)),
            dict(id="s24", title="Chapter 2 Summary", pages=(40, 42)),
            dict(id="s25", title="Homework", pages=(43, 43)),
        ],
        dividers={3, 23, 32},
    ),
    dict(
        n=3, file="chapter3.html",
        pdf=os.path.join(UPLOADS, "Chapter 3_ITN_Network Protocols and Communication.pdf"),
        title="Network Protocols and Communication",
        blurb="The rules of communication, network protocols and standards, the OSI and TCP/IP "
              "reference models, and how data moves — encapsulation, PDUs, and accessing "
              "local and remote resources.",
        topics=["Rules of communication", "Protocols & standards organizations",
                "OSI & TCP/IP reference models", "Encapsulation & PDUs",
                "Local vs remote communication"],
        sections=[
            dict(id="s31", title="3.1 Rules of Communication", pages=(3, 10)),
            dict(id="s32", title="3.2 Network Protocols and Standards", pages=(11, 23)),
            dict(id="s33", title="3.3 Moving Data in the Network", pages=(24, 32)),
            dict(id="s34", title="Chapter 3 Summary", pages=(33, 34)),
            dict(id="s35", title="Homework", pages=(35, 35)),
        ],
        dividers={3, 11, 24},
    ),
    dict(
        n=4, file="chapter4.html",
        pdf=os.path.join(UPLOADS, "Chapter 4_ITN_Network Access.pdf"),
        title="Network Access",
        blurb="Physical layer protocols and principles — bandwidth, throughput and standards — "
              "network media (copper, UTP/STP, coaxial, fiber, wireless), data link sublayers, "
              "topologies and frame structures.",
        topics=["Physical layer standards", "Copper, fiber & wireless media",
                "UTP cabling & connectors", "WAN & LAN topologies",
                "Data link frames & addressing"],
        sections=[
            dict(id="s41", title="4.1 Physical Layer Protocols", pages=(3, 9)),
            dict(id="s42", title="4.2 Network Media", pages=(10, 26)),
            dict(id="s43", title="4.3 Data Link Layer Protocols", pages=(27, 45)),
            dict(id="s44", title="Chapter 4 Summary", pages=(46, 46)),
        ],
        dividers={3, 10, 27},
    ),
    dict(
        n=5, file="chapter5.html",
        pdf=os.path.join(UPLOADS, "Chapter 5_ITN_Ethernet - Tagged (1).pdf"),
        title="Ethernet",
        blurb="Ethernet standards, frames and MAC addressing, the Address Resolution Protocol, "
              "LAN switching and Layer 3 switching.",
        topics=["LLC & MAC sublayers", "MAC addresses & Ethernet frames", "ARP",
                "LAN switch operations", "Layer 3 switching"],
        sections=[
            dict(id="s51", title="5.1 Ethernet Operation", pages=(2, 15)),
            dict(id="s52", title="5.2 Address Resolution Protocol", pages=(16, 22)),
            dict(id="s53", title="5.3 LAN Switches", pages=(23, 31)),
            dict(id="s54", title="Layer 3 Switching", pages=(32, 34)),
            dict(id="s55", title="Chapter 5 Summary", pages=(35, 35)),
        ],
        dividers={16, 23},
    ),
    dict(
        n=6, file="chapter6.html",
        pdf=os.path.join(UPLOADS, "Chapter 6_ITN_Network Layer.pdf"),
        title="Network Layer",
        blurb="The OSI Layer 3 role, IPv4 and IPv6, routing decisions and routing tables, "
              "router anatomy and boot-up, and configuring a Cisco router.",
        topics=["IPv4 & IPv6", "Host & router routing tables", "Router memory and boot",
                "Initial router configuration", "Default gateways"],
        sections=[
            dict(id="s61", title="6.1 Network Layer in Communication", pages=(2, 9)),
            dict(id="s62", title="6.2 Routing", pages=(10, 16)),
            dict(id="s63", title="6.3 Routers", pages=(17, 26)),
            dict(id="s64", title="6.4 Configuring a Cisco Router", pages=(27, 32)),
            dict(id="s65", title="Chapter 6 Summary", pages=(33, 33)),
        ],
        dividers={10, 17, 27},
    ),
    dict(
        n=7, file="chapter7.html",
        pdf=os.path.join(UPLOADS, "Chapter 7_ITN_Transport Layer.pdf"),
        title="Transport Layer",
        blurb="The transport layer’s role, conversation multiplexing, TCP vs UDP, port "
              "numbers, the three-way handshake, reliability and flow control.",
        topics=["Transport layer responsibilities", "TCP vs UDP", "Port numbers",
                "TCP three-way handshake", "Reliability & flow control"],
        sections=[
            dict(id="s71", title="7.1 Transportation of Data", pages=(2, 15)),
            dict(id="s72", title="7.2 TCP and UDP", pages=(16, 25)),
            dict(id="s73", title="Chapter 7 Summary", pages=(26, 26)),
        ],
        dividers={16},
    ),
    dict(
        n=9, file="chapter9.html",
        pdf=os.path.join(UPLOADS, "Chapter 9_ITN_Subnetting IP Networks (1).pdf"),
        title="Subnetting IP Networks",
        blurb="Network segmentation and the reasons for subnetting, subnetting by host and "
              "network requirements, VLSM, structured addressing schemes, and design "
              "considerations for IPv6.",
        topics=["Reasons for subnetting", "Subnet mask calculations", "VLSM benefits & practice",
                "Structured addressing design", "IPv6 design considerations"],
        sections=[
            dict(id="s91", title="9.1 Subnetting an IPv4 Network", pages=(3, 10)),
            dict(id="s92", title="9.2 Addressing Schemes", pages=(11, 12)),
            dict(id="s93", title="9.3 Design Considerations for IPv6", pages=(13, 13)),
            dict(id="s94", title="Chapter 9 Summary", pages=(14, 15)),
        ],
        dividers={3, 11, 13},
    ),
    dict(
        n=10, file="chapter10.html",
        pdf=os.path.join(UPLOADS, "Chapter 10_ITN_Application Layer (1).pdf"),
        title="Application Layer",
        blurb="The application, presentation and session layers, peer-to-peer and client-server "
              "models, well-known protocols (HTTP/S, SMTP, POP, IMAP, DNS, DHCP, FTP) and "
              "getting data through the internetwork.",
        topics=["Application, presentation & session layers", "Peer-to-peer & client-server",
                "HTTP, SMTP, POP & IMAP", "DNS & DHCP services",
                "FTP & moving data"],
        sections=[
            dict(id="s101", title="10.1 Application, Session and Presentation", pages=(2, 9)),
            dict(id="s102", title="10.2 Well-Known Application Layer Protocols and Services",
                 pages=(10, 25)),
            dict(id="s103", title="Chapter 10 Summary", pages=(26, 26)),
        ],
        dividers={10},
    ),
    dict(
        n=16, file="chapter16.html",
        pdf=os.path.join(UPLOADS, "ITN_Network Security_Chapter 16.pdf"),
        title="Network Security Fundamentals",
        blurb="Threats and vulnerabilities, malware/reconnaissance/access/DoS attacks, "
              "defense-in-depth mitigations (AAA, firewalls, endpoint security), and device "
              "hardening with strong passwords and SSH.",
        topics=["Threats & vulnerabilities", "Types of network attacks",
                "Defense-in-depth mitigations", "Firewalls & endpoint security",
                "Device security & SSH"],
        sections=[
            dict(id="s161", title="16.1 Security Threats and Vulnerabilities", pages=(6, 9)),
            dict(id="s162", title="16.2 Network Attacks", pages=(10, 15)),
            dict(id="s163", title="16.3 Network Attack Mitigations", pages=(16, 23)),
            dict(id="s164", title="16.4 Device Security", pages=(24, 31)),
            dict(id="s165", title="16.5 Module Practice and Quiz", pages=(32, 38)),
        ],
        dividers={6, 10, 16, 24, 32},
    ),
]

# ------------------------------------------------------------------ parsing

def page_lines(page):
    """Return structured lines from a page, in reading order."""
    d = page.get_text("dict")
    lines, images = [], []
    for bi, b in enumerate(d["blocks"]):
        if b["type"] == 1:
            w, h = b.get("width", 0), b.get("height", 0)
            if w >= 40 and h >= 40:
                images.append(b)
            continue
        for li, line in enumerate(b["lines"]):
            spans = line.get("spans", [])
            if not spans:
                continue
            text = "".join(s["text"] for s in spans)
            if not text.strip():
                continue
            dom = max(spans, key=lambda s: s["size"])
            bold = ("Bold" in dom["font"]) or any(
                "Bold" in s["font"] and s["size"] >= dom["size"] - 0.4 for s in spans)
            mono = any("Courier" in s["font"] for s in spans)
            first_font = spans[0]["font"]
            t0 = text.lstrip()
            bullet = ("Wingdings" in first_font) or (t0[:1] in BUL) or (t0[:1] and is_pua(t0[0]))
            # strip a leading glyph char for bullet detection consistency
            lines.append(dict(
                text=text, x0=line["bbox"][0], y=line["bbox"][1], size=dom["size"],
                bold=bold, mono=mono, bullet=bullet, font=first_font,
                bi=bi, li=li,
            ))
    return lines, images


FOOT_RE = re.compile(r"All rights reserved|Cisco Confidential")
PRES_RE = re.compile(r"^Presentation_ID$")


def classify_lines(lines):
    footer, body = [], []
    for l in lines:
        t = l["text"].strip()
        if FOOT_RE.search(t) or PRES_RE.match(t):
            l["footer"] = True
            footer.append(l)
        elif l["size"] < 12 and re.fullmatch(r"\d+", t):
            l["footer"] = True
            footer.append(l)
        else:
            body.append(l)
    return footer, body


def find_title(body):
    cands = [(i, l) for i, l in enumerate(body)
             if not l["bullet"] and not l["mono"] and l["size"] >= 14]
    if not cands:
        cands = [(i, l) for i, l in enumerate(body) if not l["bullet"]]
    if not cands:
        return None, None, list(range(len(body))), []
    maxs = max(l["size"] for _, l in cands)
    ti = None
    for pos, (i, l) in enumerate(cands):
        if l["size"] >= maxs - 1.5:
            ti = pos
            break
    start = cands[ti][0]
    tsize = body[start]["size"]
    tidx = []
    j = start
    while j < len(body):
        l = body[j]
        if (not l["bullet"] and not l["mono"]
                and tsize - 1.5 <= l["size"] <= tsize + 1.5):
            tidx.append(j)
            j += 1
        else:
            break
    title_txt = " ".join(norm(body[k]["text"]) for k in tidx)
    # kicker = last bold line before the title
    kicker, kidx = None, []
    for i in range(start - 1, -1, -1):
        l = body[i]
        if l["bold"] and not l["bullet"] and not l["mono"] and l["size"] >= 13:
            kicker = norm(l["text"])
            kidx = [i]
            # include additional consecutive bold kicker lines above
            break
    # lead lines: before title, not kicker, not footer
    lead_idx = [i for i in range(0, start) if i not in kidx]
    after_idx = [i for i in range(start + len(tidx), len(body))]
    return title_txt, kicker, lead_idx + after_idx, kidx


def build_blocks(body, order_idx):
    """Classify remaining lines into display blocks (order preserved)."""
    blocks = []
    cur_bullet = None   # dict(lv, x, size)
    cur_pre = None
    base_x0 = None
    open_h_size = None

    def flush_pre():
        nonlocal cur_pre
        if cur_pre is not None:
            blocks.append(dict(t="pre", x="\n".join(cur_pre)))
            cur_pre = None

    def flush_bullet():
        nonlocal cur_bullet
        if cur_bullet is not None:
            blocks.append(dict(t="li", lv=cur_bullet["lv"], x=cur_bullet["x"]))
            cur_bullet = None

    def flush_all():
        nonlocal open_h_size
        flush_pre()
        flush_bullet()
        open_h_size = None

    for idx in order_idx:
        l = body[idx]
        raw = l["text"].replace("\xa0", " ")
        stripped = raw.strip()

        if l["mono"]:
            flush_bullet()
            open_h_size = None
            if cur_pre is None:
                cur_pre = []
            cur_pre.append(raw.rstrip())
            continue
        flush_pre()

        if l["bullet"]:
            cleaned = strip_glyphs(raw)
            cleaned = re.sub(r"\s+", " ", cleaned).strip()
            if not cleaned:
                continue
            if base_x0 is None:
                base_x0 = l["x0"]
            lv = 1 if l["x0"] >= base_x0 + 6 else 0
            flush_bullet()
            open_h_size = None
            cur_bullet = dict(lv=lv, x=cleaned, size=l["size"], x0=l["x0"])
            continue

        cleaned = re.sub(r"\s+", " ", strip_glyphs(raw)).strip()
        if not cleaned:
            continue

        # sub-heading (bold, not tiny)
        if l["bold"] and l["size"] >= 14.5:
            flush_bullet()
            # join consecutive same-size headings
            if (blocks and blocks[-1]["t"] == "h"
                    and abs(blocks[-1].get("size", 0) - l["size"]) <= 1.5
                    and open_h_size is not None):
                blocks[-1]["x"] = blocks[-1]["x"] + " " + cleaned
            else:
                blocks.append(dict(t="h", x=cleaned, size=l["size"]))
            open_h_size = l["size"]
            continue

        # plain text: continuation of the open bullet when sizes line up
        if (cur_bullet is not None
                and abs(l["size"] - cur_bullet["size"]) <= 1.3
                and l["x0"] >= cur_bullet["x0"] - 6):
            cur_bullet["x"] = cur_bullet["x"] + " " + cleaned
            open_h_size = None
            continue

        flush_bullet()
        open_h_size = None
        blocks.append(dict(t="p", x=cleaned, small=l["size"] < 15))

    flush_pre()
    flush_bullet()

    # Table cells whose glyphs are letter-spaced extract as separate lines
    # ("V"+"O"+"I"+"P", "H"+"T"+"T"+"P"+"S"). Join them so the page shows —
    # and the search index can match — the real words (VOIP, HTTPS, IPTV).
    joined = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        toks = b.get("x", "").split()
        if b["t"] in ("h", "p") and len(toks) >= 2 and all(
                re.fullmatch(r"[A-Z]", t or "") for t in toks):
            b = dict(b, x="".join(toks))
        if b["t"] == "p" and re.fullmatch(r"[A-Z]", b.get("x", "")):
            run = [b["x"]]
            j = i + 1
            while (j < len(blocks) and blocks[j]["t"] == "p"
                   and re.fullmatch(r"[A-Z]", blocks[j].get("x", ""))):
                run.append(blocks[j]["x"])
                j += 1
            if len(run) >= 2:
                joined.append(dict(t="p", x="".join(run),
                                   small=b.get("small", True)))
                i = j
                continue
        joined.append(b)
        i += 1
    return joined


def extract_images(page, cache):
    out = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 1:
            continue
        w, h = b.get("width", 0), b.get("height", 0)
        if w < 40 or h < 40:
            continue
        raw = b.get("image") or b""
        mask = b.get("mask") or None
        key = hashlib.sha1(raw[:2048] + str(w).encode() + str(h).encode()
                           + (mask[:64] if mask else b"")).hexdigest()
        if key not in cache:
            cache[key] = _encode_img(raw, mask, w, h)
        uri = cache[key]
        if uri:
            out.append(uri)
    return out


def _encode_img(raw, mask, w, h):
    try:
        im = Image.open(io.BytesIO(raw))
        im.load()
        if mask:
            try:
                a = Image.open(io.BytesIO(mask))
                a.load()
                if a.size != im.size:
                    a = a.resize(im.size)
                if a.mode != "L":
                    a = a.convert("L")
                im = im.convert("RGBA")
                im.putalpha(a)
            except Exception:
                pass
        if im.width > 1100:
            ratio = 1100 / im.width
            im = im.resize((1100, max(1, int(im.height * ratio))), Image.LANCZOS)
        buf = io.BytesIO()
        has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
        if has_alpha:
            im = im.convert("RGBA")
            im.save(buf, "WEBP", lossless=True, method=5)
        else:
            if im.mode != "RGB":
                im = im.convert("RGB")
            im.save(buf, "WEBP", quality=84, method=5)
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        ext = "webp"
        return f"data:image/{ext};base64,{b64}"
    except Exception as e:
        print("  ! image encode failed:", e)
        return None


# ------------------------------------------------------------------ passages

def words_of(s):
    return re.findall(r"[a-z0-9]+", s.lower())


def build_passages(ch, sec_title, sec_id, slide):
    """Split a slide's blocks into search passages (grouped, size-capped).

    Each passage records where it lives (chapter/section/slide anchors) so the
    search UI can build honest, clickable source references, plus a figure flag
    (slide has diagrams) and a code flag (CLI/config excerpt).
    """
    groups = []
    cur = dict(h="", parts=[])

    def wcount():
        return sum(len(words_of(p)) for p in cur["parts"])

    def flush():
        nonlocal cur
        if cur["parts"]:
            groups.append(cur)
        elif cur["h"]:
            # heading-only group: keep it — the heading is real course text
            # and must remain searchable (it was previously discarded here).
            groups.append(dict(h=cur["h"], parts=[cur["h"]]))
        cur = dict(h="", parts=[])

    for b in slide["blocks"]:
        if b["t"] == "h":
            flush()
            cur = dict(h=b["x"], parts=[])
        elif b["t"] == "pre":
            flush()
            groups.append(dict(h=b["x"].splitlines()[0][:80], parts=[b["x"]], k="code"))
        else:
            cur["parts"].append(b["x"])
            if wcount() > 105:
                flush()
    flush()

    # merge tiny groups so passages have enough context (never merge code groups)
    merged = []
    for g in groups:
        wc = sum(len(words_of(p)) for p in g["parts"])
        if (wc < 7 and merged and merged[-1].get("k") != "code"
                and g.get("k") != "code"):
            # fold the small group's heading into the text before merging so
            # heading content (e.g. "Password attacks …") is never dropped.
            carry = g["parts"]
            if g.get("h") and (not g["parts"] or g["h"] != g["parts"][0]):
                carry = [g["h"]] + g["parts"]
            merged[-1]["parts"].extend(carry)
        else:
            merged.append(g)

    ctx = " ".join(x for x in [sec_title, slide.get("kicker"), slide["title"]] if x)
    out = []
    leftovers = []
    for g in merged:
        text = " ".join(g["parts"])
        if len(words_of(text)) < 3:
            # too short for a passage, but it is still course text — keep it
            # on the slide (see leftovers handling below) instead of dropping.
            if text.strip():
                leftovers.append(text.strip())
            continue
        p = dict(
            c=ch["n"], s=sec_title, t=slide["title"], a=f"p{slide['page']}",
            f=ch["file"], h=g["h"], x=text, sid=sec_id,
        )
        if slide.get("kicker"):
            p["bk"] = slide["kicker"]   # section banner — must stay searchable
        if g.get("k") == "code":
            p["k"] = "code"
        if slide.get("images"):
            p["g"] = 1
        out.append(p)
    if leftovers:
        extra = " ".join(leftovers)
        if out:
            out[-1]["x"] = out[-1]["x"] + " " + extra
        else:
            ctx = ctx + " " + extra

    # also ensure the slide title context itself is searchable when blocks are empty
    if not out and slide.get("title"):
        p = dict(c=ch["n"], s=sec_title, t=slide["title"], a=f"p{slide['page']}",
                 f=ch["file"], h="", x=ctx, sid=sec_id)
        if slide.get("kicker"):
            p["bk"] = slide["kicker"]
        if slide.get("images"):
            p["g"] = 1
        out.append(p)
    return out, ctx


# ------------------------------------------------------------------ rendering

def esc(s):
    return H.escape(str(s), quote=False)


def esc_a(s):
    return H.escape(str(s), quote=True)


def slide_html(slide, ch, sec_id, divider=False):
    pid = f"p{slide['page']}"
    kicker = slide.get("kicker") or ""
    title = slide.get("title") or f"Slide {slide['page']}"
    parts = []
    parts.append(f'<article class="slide{" divider" if divider else ""}" id="{pid}" '
                 f'data-sec="{esc_a(sec_id)}" data-page="{slide["page"]}">')
    parts.append(f'<span class="slide-n">Slide {slide["page"]}</span>')
    parts.append('<div class="slide-h">')
    if kicker:
        parts.append(f'<div class="slide-k">{esc(kicker)}</div>')
    parts.append(f'<h3 class="slide-t">{esc(title)}</h3>')
    parts.append("</div>")

    body = []
    for lead in slide.get("lead_blocks", []):
        # (unused hook — leads are merged into blocks by the builder)
        pass
    for b in slide["blocks"]:
        if b["t"] == "h":
            body.append(f"<h4>{esc(b['x'])}</h4>")
        elif b["t"] == "li":
            cls = ' class="lv1"' if b.get("lv") else ""
            body.append(f"<li{cls}>{esc(b['x'])}</li>")
        elif b["t"] == "pre":
            body.append(f"<pre><code>{esc(b['x'])}</code></pre>")
        else:
            cls = ' class="small"' if b.get("small") else ""
            body.append(f"<p{cls}>{esc(b['x'])}</p>")
    if body:
        # wrap loose <p>/<h4> fine as-is; group consecutive <li> into <ul>
        parts.append('<div class="slide-b">' + wrap_lists("".join(body)) + "</div>")

    if slide["images"]:
        figs = "".join(
            f'<figure><img src="{u}" alt="Figure from Chapter {ch["n"]}, '
            f'slide {slide["page"]}" loading="lazy"></figure>'
            for u in slide["images"])
        parts.append(f'<div class="figures">{figs}</div>')

    # verbatim raw text of the page (guarantees nothing is left out)
    raw = slide.get("raw") or ""
    parts.append("<details class=\"raw\"><summary>Verbatim slide text (exactly as extracted)</summary>"
                 f"<pre>{esc(raw)}</pre></details>")

    def _fkey(t):
        if "All rights" in t:
            return 0
        if "Confidential" in t:
            return 1
        if "Presentation_ID" in t:
            return 2
        if re.fullmatch(r"\d+", t.strip()):
            return 3
        return 4
    fbits = [norm(fl) for fl in slide["footer_lines"]]
    seen, foot = set(), []
    for b_ in sorted(fbits, key=_fkey):
        if b_ and b_ not in seen:
            seen.add(b_)
            foot.append(b_)
    parts.append('<div class="slide-f"><span>' + esc(" · ".join(foot)) + "</span></div>")
    parts.append("</article>")
    return "".join(parts)


def wrap_lists(html_str):
    """Wrap runs of consecutive <li>...</li> with <ul>."""
    out, i, n = [], 0, len(html_str)
    li_re = re.compile(r"<li[^>]*>.*?</li>")
    while i < n:
        m = li_re.match(html_str, i)
        if m:
            run = []
            while m:
                run.append(m.group(0))
                i = m.end()
                m = li_re.match(html_str, i)
            out.append("<ul>" + "".join(run) + "</ul>")
        else:
            j = html_str.find("<li", i)
            if j == -1:
                out.append(html_str[i:])
                break
            out.append(html_str[i:j])
            i = j
    return "".join(out)


def page_shell(title, active, body, corpus_json, description, lab_scripts=False,
               pt_scripts=False, exam_scripts=False):
    def nav(id_, href, label, extra=""):
        cur = ' aria-current="page"' if active == id_ else ""
        return f'<a href="{href}"{cur}{extra}>{label}</a>'
    # chapters dropdown (pure HTML/CSS, scales to any number of chapters)
    dd_links = []
    for c in CHAPTERS:
        cur = ' aria-current="page"' if active == f"c{c['n']}" else ""
        dd_links.append(
            f'<a href="{c["file"]}"{cur}>Ch {c["n"]} <span class="dnn">· {esc(c["title"])}</span></a>')
    dd_cur = " has-cur" if active.startswith("c") else ""
    dropdown = (
        f'<details class="navdrop{dd_cur}"><summary>Chapters<span class="caret">▾</span></summary>'
        f'<div class="dd">{"".join(dd_links)}</div></details>')
    lab_block = (
        "\n<script>\n" + IPV4JS + "\n</script>\n"
        "<script>\n" + LABJS + "\n</script>"
    ) if lab_scripts else ""
    pt_nav = nav("pt", "ptlab.html", "PT Prep") if PTLABS is not None else ""
    pt_block = (
        "\n<script>\n" + PTJS + "\n</script>\n"
        "<script>\n" + IOSJS + "\n</script>"
    ) if (pt_scripts and PTLABS is not None) else ""
    exam_nav = nav("exam", "exam.html", "Exam") if EXAMMOD is not None else ""
    exam_block = ""
    if exam_scripts and EXAMMOD is not None:
        bank_json = json.dumps(EXAMMOD.BANK, ensure_ascii=False,
                               separators=(",", ":"))
        bank_json = bank_json.replace("<", "\\u003c")
        exam_block = (
            "\n<script>window.__ITN_EXAM__=" + bank_json + ";</script>\n"
            "<script>\n" + EXAMJS + "\n</script>")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc_a(description)}">
<style>
{CSS}
</style>
</head>
<body>
<header class="site-header"><div class="wrap hdr">
  <a class="brand" href="index.html"><span class="logo">ITN</span>
    <span>Networking Study Hub<small>Introduction to Networks · 10 chapters</small></span></a>
  <nav class="main">
    {nav("home", "index.html", "Home")}
    {dropdown}
    {nav("lab", "lab.html", "IPv4 Lab")}
    {pt_nav}
    {exam_nav}
    <a href="#" class="ask-nav" data-open-ask="">Ask a question</a>
  </nav>
</div></header>
{body}
<footer class="site-footer"><div class="wrap">
  <span><b>Networking Study Hub</b> — complete content of Cisco <b>Introduction to Networks</b>:
  Chapters 1, 2, 3, 4, 5, 6, 7, 9, 10 &amp; 16 (Network Security).</span>
  <span>© 2008 Cisco Systems, Inc. · Every slide, figure &amp; summary included</span>
</div></footer>
<button class="back-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑ Top</button>
<script>window.__ITN__={corpus_json};</script>
<script>
{BOTJS}
</script>{lab_block}{pt_block}{exam_block}
</body>
</html>
"""


def render_index(corpus_json, meta):
    cards = []
    for ch in CHAPTERS:
        m = meta[ch["n"]]
        lis = "".join(f"<li>{esc(t)}</li>" for t in ch["topics"])
        cards.append(f"""
<div class="card">
  <span class="num">Ch {ch['n']}</span>
  <h3>{esc(ch['title'])}</h3>
  <p>{esc(ch['blurb'])}</p>
  <ul>{lis}</ul>
  <a class="go" href="{ch['file']}">Open Chapter {ch['n']} → ({m['slides']} slides)</a>
</div>""")
    features = [
        ("📄", "All the content, nothing left out",
         "Every slide’s full text, headings, bullets, CLI examples, figures and the chapter "
         "summaries — plus the verbatim source text of each slide."),
        ("🧭", "Chapter-based navigation",
         "Each of the ten chapters is its own page with a sticky table of contents covering "
         "every section (1.1 … 16.5) and every slide — jump anywhere in one click."),
        ("🔍", "Local question search (no AI, no APIs)",
         "Type any question in plain language — the built-in search runs entirely in your "
         "browser over every passage of the material and returns the most relevant excerpts "
         "with their sources. No paid services, nothing leaves your device."),
        ("🧮", "IPv4 addressing & subnetting lab",
         "Calculator with step-by-step solutions, plus randomly generated practice questions "
         "and quizzes at three levels — masks, networks, broadcasts, ranges, host counts and "
         "VLSM — with automatic checking and full worked answers."),
    ]
    feat_html = "".join(
        f'<div class="card feature"><span class="ic">{ic}</span><div><h3>{t}</h3><p>{d}</p></div></div>'
        for ic, t, d in features)
    body = f"""
<section class="hero"><div class="wrap">
  <span class="eyebrow">Cisco ITN · Introduction to Networks</span>
  <h1>Study <span class="grad">networking fundamentals — from exploring
  networks to network security</span> — every slide at your fingertips</h1>
  <p class="lead">A complete, navigable version of <b>ten chapters</b> of Introduction to
  Networks (1, 2, 3, 4, 5, 6, 7, 9, 10 &amp; 16). Read the material section by section,
  jump between slides, and ask any question in the box below — answers come straight from
  the course content.</p>
  <div class="ask-box">
    <form id="heroAskForm" class="ask-row" autocomplete="off">
      <span class="ask-field">
        <input type="text" id="heroAskInput"
               placeholder="Ask any question, e.g. What is the purpose of ARP?"
               aria-label="Your question">
        <button type="button" class="ask-clear" id="heroClear" hidden
                aria-label="Clear question">✕</button>
      </span>
      <button type="submit">Search</button>
    </form>
    <div class="ask-hint">The built-in search (running locally in your browser, no external
    services) scans every passage across the ten chapters and shows the information that
    matches your question — most relevant first.</div>
    <div class="chips" id="heroChips"></div>
  </div>
  <div class="hero-ask-results" id="heroAskResults"></div>
</div></section>

<div class="wrap">
  <h2 class="section-title">Chapters</h2>
  <p class="section-sub">Navigation is organised by chapter — each opens its own page with a
  section-level table of contents.</p>
  <div class="grid">{"".join(cards)}</div>

  <div class="card" style="margin:18px 0 0;border-color:var(--brand);border-width:1.5px">
    <h3>🧮 IPv4 addressing &amp; subnetting practice lab</h3>
    <p>Work through address/subnet/broadcast/range calculations with full step-by-step working,
    then drill yourself with randomly generated, answer-verified questions and quizzes at easy,
    medium and hard levels — instant checking, complete solutions, accuracy tracking and retries.
    Everything runs locally in your browser.</p>
    <a class="go" href="lab.html">Open the IPv4 Lab →</a>
  </div>
  <div class="card" style="margin:14px 0 0;border-color:var(--accent);border-width:1.5px">
    <h3>🧪 Packet Tracer practical preparation</h3>
    <p>Four guided labs — basic network setup, connecting networks, subnetting &amp;
    address planning, and troubleshooting — with topologies, addressing tables, IOS
    commands, verification steps, a completion checklist and a self-assessment quiz
    per lab. Prepare here, then perform every configuration in the official Cisco
    Packet Tracer application.</p>
    <a class="go" href="ptlab.html">Open the PT Prep labs →</a>
  </div>
  <div class="card" style="margin:14px 0 0;border-color:var(--brand2);border-width:1.5px">
    <h3>📝 Exam practice mode</h3>
    <p>Self-checked sessions built only from the course material — pick chapters,
    pick 10/20/30 questions, optional countdown timer, one question at a time with
    answers revealed only on submit, final score with weak-topic analysis, review
    of every wrong answer and a retry pass. Results persist in your browser.</p>
    <a class="go" href="exam.html">Start practising →</a>
  </div>

  <h2 class="section-title">What’s inside the site</h2>
  <p class="section-sub">Everything you need to review these five chapters.</p>
  <div class="grid">{feat_html}</div>

  <div class="card" style="margin:26px 0 40px">
    <h3>How to use the ask box</h3>
    <p>Press <b>Ask a question</b> in the menu or the floating 💬 button (bottom-right), or use the
    box above. Ask in plain language — “what is a runt frame?”, “difference between TCP and UDP”,
    “difference between a LAN and a WAN?”, “what is encapsulation?” — and the site returns the
    passages that answer you, with the matching words highlighted and a link that opens the
    exact slide in context.</p>
  </div>
</div>"""
    return page_shell(
        "Networking Study Hub — ITN · 10 Chapters", "home", body, corpus_json,
        "Complete study site for Cisco Introduction to Networks — Chapters 1, 2, 3, 4, 5, "
        "6, 7, 9, 10 and 16 (Network Security), with a built-in question search.")


def render_lab(corpus_json):
    """IPv4 addressing & subnetting practice laboratory (lab.html)."""
    body = f"""
<div class="wrap" id="lab-root">
  <h1 class="section-title" style="margin-top:30px">IPv4 Addressing &amp; Subnetting Lab</h1>
  <p class="section-sub">Interactive calculator, step-by-step solutions, and unlimited generated
  practice — three difficulty levels, instant feedback, full worked answers.</p>
  <span id="lab-selftest" class="lab-badge badge-ok">Running in-page self-test…</span>

  <section class="lab-sec">
    <h2>1 · Calculator</h2>
    <p class="lede">Enter an IPv4 address and either a dotted mask (255.255.255.0) or a CIDR
    prefix (/24). You can also type them together as <code>192.168.1.10/24</code> in the address
    box and leave the mask empty. Special prefixes (/31, /32) are handled correctly.</p>
    <form id="cal-form" class="panel" autocomplete="off">
      <div class="cal-row">
        <div class="cal-field">
          <label for="cal-addr">IPv4 address</label>
          <input type="text" id="cal-addr" placeholder="192.168.1.10" spellcheck="false">
        </div>
        <div class="cal-field">
          <label for="cal-mask">Subnet mask or prefix</label>
          <input type="text" id="cal-mask" placeholder="255.255.255.0  or  /24" spellcheck="false">
        </div>
        <button class="btn" type="submit">Calculate</button>
      </div>
      <div id="cal-err" class="cal-err" hidden></div>
      <div id="cal-out"></div>
    </form>
  </section>

  <section class="lab-sec">
    <h2>2 · Step-by-step solutions</h2>
    <p class="lede">After every calculation you get the full working: prefix → mask, block-size
    arithmetic, network and broadcast identification, host range and usable count — shown for
    both dotted-decimal and CIDR input.</p>
    <div id="cal-steps" class="panel"><p class="note" style="margin:0">The worked solution appears
    here after each calculation.</p></div>
  </section>

  <section class="lab-sec">
    <h2>3–5 · Practice &amp; quiz</h2>
    <p class="lede">Questions are <b>generated randomly</b> each time (so answers can’t be
    memorised) from verified templates: subnet masks, network and broadcast addresses, usable
    ranges, host counts, choosing a subnet size, dividing a network, and VLSM. Pick a level and
    question types, then answer one question at a time — you get automatic checking, an
    explanation of a wrong answer, the complete correct solution, running accuracy, and the
    chance to retry anything you missed. Pick <b>Mixed</b> as the difficulty for a revision
    set that draws questions at random from all three levels.</p>

    <div class="panel">
      <div class="qs-setup-grid">
        <label>Difficulty
          <select id="qs-level">
            <option value="easy">Easy</option>
            <option value="medium" selected>Medium</option>
            <option value="hard">Hard</option>
            <option value="mixed">Mixed — revision set (easy → hard)</option>
          </select>
        </label>
        <label>Questions per set
          <select id="qs-count">
            <option value="5" selected>5</option>
            <option value="10">10</option>
            <option value="15">15</option>
            <option value="20">20</option>
          </select>
        </label>
      </div>
      <div class="qs-types" id="qs-types">
        <label><input type="checkbox" value="maskValue" checked> Subnet masks</label>
        <label><input type="checkbox" value="network" checked> Network addresses</label>
        <label><input type="checkbox" value="broadcast" checked> Broadcast addresses</label>
        <label><input type="checkbox" value="hostRange" checked> Usable host ranges</label>
        <label><input type="checkbox" value="hostCount" checked> Host counts</label>
        <label><input type="checkbox" value="subnetForHosts" checked> Subnet size for hosts</label>
        <label><input type="checkbox" value="subnetPrefix" checked> Dividing a network</label>
        <label><input type="checkbox" value="subnetCount" checked> Number of subnets</label>
        <label><input type="checkbox" value="subnetOf" checked> Subnet of a host</label>
        <label><input type="checkbox" value="vlsm" checked> VLSM (hard)</label>
      </div>
      <div id="qs-setup-msg" class="qs-msg" hidden></div>
      <div class="qs-actions">
        <button class="btn" id="qs-start" type="button">Start a fresh random set</button>
        <span class="note" style="margin:0">Every set is newly generated and answer-checked
        before it is shown.</span>
      </div>
    </div>

    <div class="panel qs-stage" id="qs-stage" hidden>
      <div class="qs-stage-top">
        <span class="qs-pill" id="q-type"></span>
        <span class="qs-pill" id="q-level"></span>
        <span class="qs-progress" id="q-progress"></span>
      </div>
      <div class="q-prompt" id="q-prompt"></div>
      <div class="q-answer-row" id="q-input">
        <input type="text" id="q-answer" autocomplete="off" spellcheck="false"
               aria-label="Your answer">
        <button class="btn" id="q-check" type="button">Check answer</button>
      </div>
      <div id="q-feedback"></div>
      <div id="q-solution"></div>
      <div class="q-next-wrap">
        <button class="btn ghost" id="q-next" type="button" hidden>Next question →</button>
        <button class="btn ghost" id="q-retry" type="button" hidden>Retry the ones you missed</button>
      </div>
      <div class="q-stats" id="q-stats"></div>
    </div>
  </section>

  <p class="lab-foot-note">The calculator’s arithmetic (including /0, /8, /16, /24, /30, /31 and
  /32) is covered by automated tests in <code>site-build/test-ipv4.js</code>, and the badge above
  re-runs the calculator’s self-test in your browser every time this page loads. The question
    generator only admits questions whose answers it can re-derive independently. Lifetime
    accuracy counters are stored <b>only in this browser</b> (localStorage key
    <code>itn-lab-stats-v1</code>) — no accounts, no servers, nothing syncs between
    devices, and clearing site data resets them; individual questions and answers are not
    saved. Everything runs locally — no paid services or external APIs, and your answers
    never leave the page.</p>
</div>"""
    return page_shell(
        "IPv4 Addressing & Subnetting Lab — Networking Study Hub", "lab", body, corpus_json,
        "Interactive IPv4 subnetting calculator with step-by-step solutions plus randomly "
        "generated, verified practice questions and quizzes (easy/medium/hard).",
        lab_scripts=True)


def rev_ref(page):
    """Link back to the source slide from revision content."""
    return f'<a class="rev-link" href="#p{page}">slide {page}</a>'


def render_revision(ch):
    """Build the structured revision kit for one chapter from site-build/revision/chNN.py.
    Additive only — never alters or removes slide content."""
    rev = REVISION.get(ch["n"])
    if not rev:
        return ""
    n = ch["n"]
    out = []
    TAG_NAME = {"src": "From the course PDFs", "sup": "Study note", "prac": "Practice"}

    def sec(num, title, tag, body):
        out.append(
            f'<div class="rev-sec"><h3><span class="n">{num}</span>{esc(title)}'
            f'<span class="rev-tag {tag}">{TAG_NAME[tag]}</span></h3>{body}</div>')

    out.append(f"""<section class="rev" id="revision">
  <div class="rev-h">
    <h2>★ Revision kit — Chapter {n}: {esc(ch['title'])}</h2>
    <p class="rev-lede">Eight structured sections for revision: overview, definitions, concept
    explanations, comparisons, important facts, a knowledge check, common misunderstandings and a
    quick revision read. Everything here is additive — the complete original slides follow below,
    unchanged, and every fact links back to its source slide.</p>
    <div class="rev-legend">
      <span class="lg"><span class="rev-tag src">From the course PDFs</span>grounded in the source slides (linked)</span>
      <span class="lg"><span class="rev-tag sup">Study note</span>supplementary wording written for this site</span>
      <span class="lg"><span class="rev-tag prac">Practice</span>revision questions — not lecturer or exam questions</span>
    </div>
  </div>""")

    # 1 — chapter overview ------------------------------------------------
    obj = "".join(f"<li>{o}</li>" for o in rev.get("objectives", []))
    con = "".join(f"<li>{c}</li>" for c in rev.get("concepts", []))
    body = f"<p>{rev.get('overview', '')}</p>"
    if obj:
        body += f"<h4>Learning objectives</h4><ul>{obj}</ul>"
    if con:
        body += f"<h4>Most important concepts</h4><ul>{con}</ul>"
    sec(1, "Chapter overview", "src", body)

    # 2 — key definitions -------------------------------------------------
    items = []
    for d in rev.get("definitions", []):
        abbr = f'<span class="abbr">{esc(d["abbr"])}</span>' if d.get("abbr") else ""
        ref = f" {rev_ref(d['r'])}" if d.get("r") else ""
        items.append(f'<div class="def-item"><span class="term">{esc(d["t"])}</span>{abbr}'
                     f'<p>{d["d"]}{ref}</p></div>')
    sec(2, "Key definitions", "src", f'<div class="def-list">{"".join(items)}</div>')

    # 3 — concept explanations -------------------------------------------
    cards = []
    for e in rev.get("explanations", []):
        ref = f" {rev_ref(e['r'])}" if e.get("r") else ""
        ex = f'<p><b>Example:</b> {e["e"]}</p>' if e.get("e") else ""
        cards.append(f'<div class="rev-card"><h4>{esc(e["t"])}{ref}</h4><p>{e["d"]}</p>{ex}</div>')
    sec(3, "Concept explanations", "sup",
        f'<div class="rev-cards">{"".join(cards)}</div>'
        f'<p class="rev-note">Technical terms are kept exactly as the course uses them; the plain-language '
        f'wording and examples are supplementary study notes.</p>')

    # 4 — comparisons -----------------------------------------------------
    body4 = []
    comps = rev.get("comparisons", [])
    if not comps:
        body4.append('<div class="rev-gap">No comparison in the requested list is supported by '
                     'this chapter’s source material.</div>')
    for c in comps:
        if c.get("gap"):
            body4.append(f'<div class="rev-gap"><b>{esc(c["t"])}:</b> {c["gap"]}</div>')
            continue
        refs = " ".join(rev_ref(r) for r in c.get("refs", []))
        head = "".join(f"<th>{h}</th>" for h in c["cols"])
        rows = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
                       for row in c["rows"])
        note = f'<p class="rev-note">{c.get("note", "")}{" " + refs if refs else ""}</p>'
        body4.append(f'<h4>{esc(c["t"])}</h4><div class="cmp-wrap"><table class="cmp">'
                     f'<thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>{note}')
    sec(4, "Comparisons", "src", "".join(body4))

    # 5 — important facts -------------------------------------------------
    facts = "".join(
        f'<li>{f["d"]}{" " + rev_ref(f["r"]) if f.get("r") else ""}</li>'
        for f in rev.get("facts", []))
    sec(5, "Important facts", "src", f"<ul>{facts}</ul>")

    # 6 — knowledge check -------------------------------------------------
    TYPE_LABEL = {"mc": "Multiple choice", "tf": "True or false",
                  "short": "Short answer", "explain": "Explanation"}
    qs = rev.get("questions", [])
    kc = []
    for i, q in enumerate(qs, 1):
        opts = ""
        if q.get("opts"):
            letters = "ABCDEFGH"
            opts = ('<ul class="kc-opts">' +
                    "".join(f"<li><b>{letters[j]}.</b> {o}</li>"
                            for j, o in enumerate(q["opts"])) + "</ul>")
        kc.append(
            f'<div class="kc-item"><p class="kc-q"><span class="kc-type">'
            f'{TYPE_LABEL.get(q.get("type"), "Practice")}</span>Q{i}. {q["q"]}</p>{opts}'
            f'<details class="kc-ans"><summary>Show answer &amp; explanation</summary>'
            f'<p class="kc-a"><b>Answer:</b> {q["a"]}</p>'
            f'<p class="kc-why"><b>Why:</b> {q["why"]}</p></details></div>')
    intro = (f'<div class="kc-intro">{len(qs)} practice questions — a mix of multiple-choice, '
             'true/false, short-answer and explanation tasks. Answers stay hidden until you '
             'reveal them, and each one explains why it is correct. These are revision '
             'questions written for this site from the course content — they are <b>not</b> '
             'lecturer instructions or examination questions.</div>')
    sec(6, "Knowledge check", "prac", intro + "".join(kc))

    # 7 — common misunderstandings ----------------------------------------
    mm = "".join(f'<div class="rev-card"><h4>{esc(m["t"])}</h4><p>{m["d"]}</p></div>'
                 for m in rev.get("misunderstandings", []))
    sec(7, "Common misunderstandings", "sup", f'<div class="rev-cards">{mm}</div>')

    # 8 — quick revision --------------------------------------------------
    sec(8, "Quick revision (2–5 minutes)", "sup",
        f'<div>{rev.get("quick", "")}</div>')

    gaps = rev.get("gaps", [])
    if gaps:
        out.append('<div class="rev-sec"><h4>Identified source-material gaps</h4>'
                   + "".join(f'<div class="rev-gap">{g}</div>' for g in gaps) + "</div>")

    out.append("""  <div class="rev-sec"><p class="rev-note">This kit sits above the original
    material — nothing below has been shortened or removed. Slide links (e.g.
    <a class="rev-link" href="#p5">slide 5</a>) open the exact source slide on this page.</p></div>
</section>""")
    return "\n".join(out)


def render_chapter(ch, sections_data, all_slides, corpus_json):
    n = ch["n"]
    total_slides = len(all_slides)
    nsec = len(ch["sections"])

    # slides not inside any section (title / objectives pages)
    section_pages = set()
    for sec in ch["sections"]:
        section_pages.update(range(sec["pages"][0], sec["pages"][1] + 1))
    loose = [s for s in all_slides if s["page"] not in section_pages]

    def toc_label(s):
        t = s.get("title") or ""
        if re.fullmatch(r"Slide \d+", t):
            # untitled slide — use its first content line for the TOC
            for b in s.get("blocks", []):
                if b.get("x"):
                    t = b["x"]
                    break
        t = t or f"Slide {s['page']}"
        return t[:40] + ("…" if len(t) > 40 else "")

    # TOC — revision kit first, then loose (overview) slides, then every section with its slides
    toc_items = []
    toc_items.append('<a class="rev-toc-flag" href="#revision">★ Revision kit '
                     '(overview → quick revision)</a>')
    for s in loose:
        if s["page"] == 1:
            label = "Overview (title slide)"
        else:
            label = toc_label(s)
        toc_items.append(f'<a href="#p{s["page"]}">{esc(label)}</a>')
    for sec in ch["sections"]:
        toc_items.append(f'<a href="#{sec["id"]}">{esc(sec["title"])}</a>')
        sub = [s for s in sections_data[sec["id"]]]
        if sub:
            toc_items.append('<div class="toc-slides">')
            for s in sub:
                toc_items.append(f'<a href="#p{s["page"]}">{s["page"]}. {esc(toc_label(s))}</a>')
            toc_items.append("</div>")
    toc = "".join(toc_items)

    # sections HTML — overview/loose slides rendered right after the hero
    secs_html = [slide_html(s, ch, f"p{s['page']}", divider=False) for s in loose]

    for sec in ch["sections"]:
        slides = [s for s in all_slides if sec["pages"][0] <= s["page"] <= sec["pages"][1]]
        cards = "".join(
            slide_html(s, ch, sec["id"], divider=(s["page"] in ch["dividers"]))
            for s in slides)
        secs_html.append(
            f'<section class="sec" id="{sec["id"]}">'
            f'<div class="sec-h"><h2>{esc(sec["title"])}</h2>'
            f'<span class="cnt">{len(slides)} slide{"s" if len(slides) != 1 else ""}</span></div>'
            f"{cards}</section>")

    topics = "".join(f"<span>{esc(t)}</span>" for t in ch["topics"])
    rev_html = render_revision(ch)
    body = f"""
<div class="chapter-layout">
  <aside class="toc">
    <div class="toc-h">On this page</div>
    {toc}
    <div class="toc-ask"><button type="button" data-open-ask="">💬 Ask about Chapter {n}</button></div>
  </aside>
  <div class="toc-content">
    <details class="toc-mobile"><summary>☰ Contents — Chapter {n}: {esc(ch['title'])}</summary>
      <div class="toc"><div class="toc-h">Sections</div>{toc}</div>
    </details>
    <div class="chapter-hero">
      <div class="k">Introduction to Networks</div>
      <h1>Chapter {n}: {esc(ch['title'])}</h1>
      <p>{esc(ch['blurb'])}</p>
      <div class="meta"><span>{total_slides} slides</span><span>{nsec} sections</span>
      <span>Full text + figures</span></div>
      <div class="meta" style="margin-top:8px">{topics}</div>
    </div>
    {rev_html}
    {"".join(secs_html)}
  </div>
</div>"""
    return page_shell(
        f"Chapter {n}: {ch['title']} — Networking Study Hub", f"c{n}", body, corpus_json,
        f"Complete content of Cisco ITN Chapter {n}: {ch['title']} — every slide, figure and summary.")


# ------------------------------------------------------------------ main build

def main():
    os.makedirs(OUT, exist_ok=True)
    img_cache = {}
    corpus = []
    meta = {}
    parsed = []          # (ch, all_slides, sections_data, docs) — render AFTER full parse
    verify_errors = []

    # ---------------- pass 1: parse everything ----------------
    for ch in CHAPTERS:
        print(f"Parsing Chapter {ch['n']} …")
        doc = pymupdf.open(ch["pdf"])
        all_slides, sections_data = [], {s["id"]: [] for s in ch["sections"]}
        annot_count = 0

        for pno in range(len(doc)):
            page = doc[pno]
            pageno = pno + 1
            annot_count += len(list(page.annots() or []))
            raw_text = page.get_text("text")
            lines, img_blocks = page_lines(page)
            footer, body = classify_lines(lines)
            title, kicker, order_idx, kidx = find_title(body)
            blocks = build_blocks(body, order_idx)

            # which section?
            sec = None
            for s in ch["sections"]:
                if s["pages"][0] <= pageno <= s["pages"][1]:
                    sec = s
                    break
            sec_title = sec["title"] if sec else f"Chapter {ch['n']}"
            sec_id = sec["id"] if sec else f"p{pageno}"

            slide = dict(
                page=pageno,
                title=title or f"Slide {pageno}",
                kicker=kicker,
                blocks=blocks,
                footer_lines=[f["text"] for f in footer],
                raw=raw_text,
                images=extract_images(page, img_cache),
            )
            all_slides.append(slide)
            if sec:
                sections_data[sec["id"]].append(slide)

            passages, _ = build_passages(ch, sec_title, sec_id, slide)
            corpus.extend(passages)

            expected_figs = len(img_blocks)
            if len(slide["images"]) != expected_figs:
                print(f"  ! ch{ch['n']} p{pageno}: figures {len(slide['images'])} vs expected {expected_figs}")

        if annot_count:
            print(f"  note: {annot_count} annotations found (page text already extracted)")
        meta[ch["n"]] = dict(slides=len(all_slides))
        parsed.append((ch, all_slides, sections_data, doc))

    # ---------------- pass 2: render every page with the FULL corpus ----------------
    corpus_json = json.dumps(dict(passages=corpus), ensure_ascii=False, separators=(",", ":"))
    corpus_json = (corpus_json.replace("<", "\\u003c")
                   .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))

    for ch, all_slides, sections_data, doc in parsed:
        print(f"Rendering Chapter {ch['n']} …")
        sec_map = {s["id"]: sections_data[s["id"]] for s in ch["sections"]}
        html_page = render_chapter(ch, sec_map, all_slides, corpus_json)
        out_path = os.path.join(OUT, ch["file"])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_page)
        print(f"  wrote {ch['file']} ({len(html_page)/1e6:.2f} MB)")

        # ---- verification: every extracted line must exist in the page ----
        html_text = re.sub(r"<[^>]*>", " ", html_page)
        html_text = H.unescape(html_text)
        html_norm = norm(html_text)
        for pno in range(len(doc)):
            page = doc[pno]
            lines, _ = page_lines(page)
            for l in lines:
                nl = norm(l["text"])
                if not nl:
                    continue
                if nl not in html_norm:
                    verify_errors.append((ch["file"], pno + 1, nl[:120]))
            # raw text too (line-based)
            for ln in page.get_text("text").splitlines():
                nl = norm(ln)
                if nl and nl not in html_norm:
                    verify_errors.append((ch["file"], pno + 1, "RAW: " + nl[:120]))
        doc.close()

    idx = render_index(corpus_json, meta)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(idx)
    print(f"  wrote index.html ({len(idx)/1e6:.2f} MB)")

    lab_page = render_lab(corpus_json)
    with open(os.path.join(OUT, "lab.html"), "w", encoding="utf-8") as f:
        f.write(lab_page)
    print(f"  wrote lab.html ({len(lab_page)/1e6:.2f} MB)")

    if PTLABS is not None:
        pt_page = page_shell(
            "Packet Tracer Practical Preparation — ITN", "pt",
            PTLABS.render_pt_body(), corpus_json,
            "Four guided Packet Tracer preparation labs for Cisco Introduction to "
            "Networks — basic setup, connecting networks, subnetting and address "
            "planning, and troubleshooting — with checklists and self-assessment "
            "quizzes.", pt_scripts=True)
        with open(os.path.join(OUT, "ptlab.html"), "w", encoding="utf-8") as f:
            f.write(pt_page)
        print(f"  wrote ptlab.html ({len(pt_page)/1e6:.2f} MB)")
    else:
        print("  ! ptlabs.py missing — ptlab.html NOT generated")

    if EXAMMOD is not None:
        ex_page = page_shell(
            "Exam Practice Mode — ITN", "exam",
            EXAMMOD.render_exam_body(), corpus_json,
            "Independent exam practice for Cisco Introduction to Networks — "
            "chapter-selectable timed or untimed sessions, scoring, weak-topic "
            "analysis and review, built from the course material.",
            exam_scripts=True)
        with open(os.path.join(OUT, "exam.html"), "w", encoding="utf-8") as f:
            f.write(ex_page)
        print(f"  wrote exam.html ({len(ex_page)/1e6:.2f} MB) "
              f"[{len(EXAMMOD.BANK)} questions]")
    else:
        print("  ! exam.py missing — exam.html NOT generated")

    # corpus sidecar for debugging / reuse
    with open(os.path.join(OUT, "corpus.json"), "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=1)

    n_pass = len(corpus)
    print(f"\nPassages: {n_pass}")
    if verify_errors:
        print(f"\nVERIFY FAILURES: {len(verify_errors)}")
        seen = set()
        for v in verify_errors:
            k = (v[0], v[2])
            if k in seen:
                continue
            seen.add(k)
            print("  ", v)
        sys.exit(2)
    else:
        print("VERIFY OK — every extracted line is present in the generated HTML.")


if __name__ == "__main__":
    main()
