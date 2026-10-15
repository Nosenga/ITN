"""Packet Tracer practical preparation content for ptlab.html.

Grounding (primary source = the course PDFs, slide = PDF page):
  Ch 1  p.10 end devices · p.14 topology diagrams · p.19 ARP
  Ch 2  p.25 hostnames · p.36 automatic IP config · p.37 IP address conflicts ·
        p.38 testing the interface assignment
  Ch 4  UTP / RJ-45 copper media (pp.12–17)
  Ch 5  p.24 switch port fundamentals (MAC address table) · p.27 Auto-MDIX
  Ch 6  p.28 router configuration steps (enable → conf t) · p.29 configure LAN
        interfaces (full transcript) · p.30 show ip interface brief + ping output ·
        p.31 default gateway on a host · p.33 summary
  Ch 9  p.4 reasons for subnetting · p.6 formula 2^n − 2 · p.7 design ·
        p.8 traditional waste · p.9 VLSM · p.10 LAN /27 — WAN /30 example
Everything the course does NOT specify (Packet Tracer GUI paths, device names,
cable choices, exact lab address plans) is labelled as an assumption in the page.
"""

# --------------------------------------------------------------------------
# topology diagram helpers (inline SVG — no external resources)
# --------------------------------------------------------------------------
_SVG_FONT = 'font-family="-apple-system,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif"'
_MONO = "SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace"


def _txt(x, y, s, size=13, weight=None, fill="var(--ink)", anchor="middle",
         mono=False, muted=False):
    w = f' font-weight="{weight}"' if weight else ""
    f = f' fill="{fill}"'
    fam = f' font-family="{_MONO}"' if mono else ""
    a = f' text-anchor="{anchor}"' if anchor != "middle" else ""
    st = ' style="font-size:%spx"' % size
    return f'<text x="{x}" y="{y}"{st}{w}{f}{fam}{a}>{s}</text>'


def _box(x, y, w, h, title, l1=None, l2=None):
    """Device box: bold title + up to two muted sub-lines."""
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="var(--panel)" '
         f'stroke="var(--brand)" stroke-width="2"/>')
    cx = x + w / 2
    s += _txt(cx, y + 24, title, size=14.5, weight="800")
    if l1:
        s += _txt(cx, y + 44, l1, size=11.5, mono=True, fill="var(--muted)")
    if l2:
        s += _txt(cx, y + 61, l2, size=11.5, mono=True, fill="var(--muted)")
    return s


def _rbox(x, y, w, h, title, l1, l2):
    """Router box (taller, three lines)."""
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="var(--panel)" '
         f'stroke="var(--brand2)" stroke-width="2.5"/>')
    cx = x + w / 2
    s += _txt(cx, y + 30, title, size=16, weight="800")
    s += _txt(cx, y + 56, l1, size=12, mono=True, fill="var(--ink2)")
    s += _txt(cx, y + 76, l2, size=12, mono=True, fill="var(--ink2)")
    return s


def _ln(x1, y1, x2, y2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="var(--muted)" stroke-width="2.5"/>')


def _lbl(x, y, s, anchor="middle"):
    """Link label with a light halo so it stays readable over lines."""
    return (f'<text x="{x}" y="{y}" style="font-size:11px;font-weight:700" '
            f'fill="var(--muted)" text-anchor="{anchor}" paint-order="stroke" '
            f'stroke="var(--panel2)" stroke-width="5">{s}</text>')


def _banner(x, y, s, anchor="start"):
    a = ' text-anchor="end"' if anchor == "end" else ""
    return (f'<text x="{x}" y="{y}" style="font-size:13.5px;font-weight:800" '
            f'fill="var(--brand2)"{a}>{s}</text>')


def _svg(vb_w, vb_h, body):
    return (f'<svg viewBox="0 0 {vb_w} {vb_h}" role="img" {_SVG_FONT} '
            f'aria-label="Lab topology diagram">{body}</svg>')


def topo_lab1():
    """One LAN: PC0 — SW0 — PC1."""
    b = _banner(24, 34, "Single LAN · 192.168.10.0/24 — no router needed")
    b += _box(24, 114, 158, 66, "PC0", "192.168.10.10 / 24", "gw: (not needed)")
    b += _box(300, 120, 132, 54, "SW0", "Layer 2 switch")
    b += _box(578, 114, 158, 66, "PC1", "192.168.10.11 / 24", "gw: (not needed)")
    b += _ln(182, 147, 300, 147)
    b += _ln(432, 147, 578, 147)
    b += _lbl(241, 137, "straight-through")
    b += _lbl(505, 137, "straight-through")
    b += _ln(24, 246, 70, 246)
    b += _txt(78, 250, "copper straight-through UTP (PC ↔ switch) — Ch 4 media, "
             "Auto-MDIX Ch 5 p.27", size=11.5, anchor="start", fill="var(--muted)")
    return _svg(760, 272, b)


def topo_lab2():
    """Two LANs + R1 (the course's own slide 28–31 addresses)."""
    b = _banner(20, 30, "LAN-A · 192.168.10.0/24")
    b += _banner(820, 30, "LAN-B · 192.168.11.0/24", anchor="end")
    b += _box(20, 120, 150, 66, "PC0", "192.168.10.10 / 24", "gw 192.168.10.1")
    b += _box(195, 126, 105, 54, "SW0", "L2 switch")
    b += _rbox(345, 106, 140, 94, "R1", "G0/0  192.168.10.1", "G0/1  192.168.11.1")
    b += _box(530, 126, 105, 54, "SW1", "L2 switch")
    b += _box(670, 120, 150, 66, "PC1", "192.168.11.10 / 24", "gw 192.168.11.1")
    b += _ln(170, 153, 195, 153)
    b += _ln(300, 153, 345, 153)
    b += _ln(485, 153, 530, 153)
    b += _ln(635, 153, 670, 153)
    b += _lbl(322, 141, "G0/0")
    b += _lbl(507, 141, "G0/1")
    b += _txt(420, 250, "Each router interface is the default gateway of its LAN "
             "(Ch 6 slide 31)", size=12, fill="var(--muted)")
    return _svg(840, 272, b)


def topo_lab3():
    """VLSM plan over the same shape + optional /30 WAN extension."""
    b = _banner(20, 52, "LAN-A · 192.168.10.0/27  (30 usable)")
    b += _banner(820, 52, "LAN-B · 192.168.10.32/28  (14 usable)", anchor="end")
    b += _box(345, 14, 140, 62, "R2 (optional)", "G0/0 192.168.10.50/30")
    b += _ln(415, 76, 415, 146)
    b += _lbl(425, 100, "G0/2 ↔ R2", anchor="start")
    b += _lbl(425, 117, "192.168.10.48/30 · .49–.50", anchor="start")
    b += _box(20, 160, 150, 66, "PC0", "192.168.10.10/27", "gw .1")
    b += _box(195, 166, 105, 54, "SW0", "L2 switch")
    b += _rbox(345, 146, 140, 94, "R1", "G0/0  192.168.10.1/27", "G0/1  192.168.10.33/28")
    b += _box(530, 166, 105, 54, "SW1", "L2 switch")
    b += _box(670, 160, 150, 66, "PC1", "192.168.10.34/28", "gw .33")
    b += _ln(170, 193, 195, 193)
    b += _ln(300, 193, 345, 193)
    b += _ln(485, 193, 530, 193)
    b += _ln(635, 193, 670, 193)
    b += _lbl(322, 181, "G0/0")
    b += _lbl(507, 181, "G0/1")
    b += _txt(420, 272, "Subnets carved from 192.168.10.0/24 with 2^n − 2 (Ch 9) — "
             "sizes follow the course's /27-LAN, /30-WAN example (slide 10)",
             size=12, fill="var(--muted)")
    return _svg(840, 294, b)


def topo_lab4():
    """Two LANs, four PCs — five hidden configuration faults."""
    b = _banner(20, 30, "LAN-A · 192.168.10.0/24")
    b += _banner(820, 30, "LAN-B · 192.168.11.0/24", anchor="end")
    b += _box(15, 110, 140, 66, "PC0", "192.168.10.10 / 24", "gw 192.168.10.1")
    b += _box(15, 250, 140, 66, "PC1", "192.168.10.11 / 24", "gw 192.168.10.1")
    b += _box(205, 194, 105, 54, "SW0", "L2 switch")
    b += _rbox(355, 174, 140, 94, "R1", "G0/0  192.168.10.1", "G0/1  192.168.11.1")
    b += _box(540, 194, 105, 54, "SW1", "L2 switch")
    b += _box(680, 110, 145, 66, "PC2", "192.168.11.10 / 24", "gw 192.168.11.1")
    b += _box(680, 250, 145, 66, "PC3", "192.168.11.11 / 24", "gw 192.168.11.1")
    b += _ln(155, 143, 205, 221)
    b += _ln(155, 283, 205, 221)
    b += _ln(310, 221, 355, 221)
    b += _ln(495, 221, 540, 221)
    b += _ln(645, 221, 680, 143)
    b += _ln(645, 221, 680, 283)
    b += _lbl(332, 210, "G0/0")
    b += _lbl(517, 210, "G0/1")
    b += _txt(420, 412, "Diagram shows the INTENDED (correct) addressing — the running "
             "configuration contains five faults to find", size=12, fill="var(--muted)")
    return _svg(840, 434, b)


# --------------------------------------------------------------------------
# shared fragments
# --------------------------------------------------------------------------
def ref(ch, page):
    return (f'<a class="rev-link" href="chapter{ch}.html#p{page}">'
            f'course · Ch {ch} slide {page}</a>')


def _cmd_table(rows):
    """rows: (command, where, purpose)"""
    tr = []
    for c, w, p in rows:
        tr.append(f"<tr><td><code>{c}</code></td><td>{w}</td><td>{p}</td></tr>")
    return ('<div class="pt-tbl"><table class="cmp">'
            "<thead><tr><th>Command</th><th>Where it is typed</th>"
            "<th>What it does</th></tr></thead>"
            f"<tbody>{''.join(tr)}</tbody></table></div>")


def _addr_table(cols, rows):
    head = "".join(f"<th>{c}</th>" for c in cols)
    body = ""
    for r in rows:
        body += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    return (f'<div class="pt-tbl"><table class="cmp"><thead><tr>{head}</tr></thead>'
            f"<tbody>{body}</tbody></table></div>")


def _sec(n, title, body):
    return f'<div class="pt-sec"><h3><span class="n">{n}</span>{title}</h3>{body}</div>'


def _quiz(lab_id, items):
    letters = "ABCDEFGH"
    out = [f'<form class="ptq" data-ptq="{lab_id}">']
    for i, q in enumerate(items):
        opts = q["opts"]
        correct = q["a"]
        qtype = "Multiple choice" if len(opts) > 2 else "True / false"
        out.append(
            f'<div class="ptq-item"><p class="ptq-q"><span class="ptq-type">{qtype}</span>'
            f'{q["q"]}</p><div>')
        for j, o in enumerate(opts):
            dc = f' data-correct="{j}"' if j == correct else ""
            out.append(f'<label class="ptq-opt"><input type="radio" '
                       f'name="{lab_id}-q{i}" value="{j}"{dc}> '
                       f"<b>{letters[j]}.</b> {o}</label>")
        out.append("</div>")
        out.append(f'<div class="ptq-why"><b>Answer: {letters[correct]} — '
                   f'{opts[correct]}.</b> {q["why"]}</div></div>')
    out.append(
        '<div class="pt-tools">'
        '<button type="button" class="pt-btn" data-ptq-grade>Check answers</button> '
        '<button type="button" class="pt-btn ghost" data-ptq-retry hidden>Try again</button>'
        '<p class="ptq-score" hidden></p></div></form>')
    return "".join(out)


def _tsq(items):
    out = []
    for i, t in enumerate(items, 1):
        out.append(
            f'<div class="kc-item"><p><b>Q{i}.</b> {t["q"]}</p>'
            f'<details class="kc-ans"><summary>Show answer</summary>'
            f'<p>{t["a"]}</p></details></div>')
    return "".join(out)


def _checklist(lab):
    items = "".join(
        f'<li><label><input type="checkbox" data-ck="{lab["id"]}-{i}"> '
        f"<span>{t}</span></label></li>"
        for i, t in enumerate(lab["checklist"], 1))
    n = len(lab["checklist"])
    return f"""
<div class="pt-ck-head">
  <b>Lab checklist — mark each task as completed</b>
  <div class="pt-bar" data-ptbar="{lab['id']}"><i></i></div>
  <span data-ptcount="{lab['id']}">0 / {n} tasks</span>
  <button type="button" class="pt-reset" data-ptreset="{lab['id']}">Reset</button>
</div>
<ul class="pt-check">{items}</ul>"""


TOPOS = {"lab1": topo_lab1, "lab2": topo_lab2, "lab3": topo_lab3,
         "lab4": topo_lab4}


def _lab_html(lab):
    hd = f"""
<div class="pt-lab-hd">
  <h2><span class="pt-n">LAB {lab['n']}</span>{lab['title']}</h2>
  <div class="pt-lab-progress"><div class="pt-bar" data-ptbar="{lab['id']}"><i></i></div>
    <span data-ptcount="{lab['id']}">0 / {len(lab['checklist'])} tasks</span></div>
</div>"""
    assume = "".join(f"<li>{a}</li>" for a in lab["assumptions"])
    s1 = _sec(1, "Objective", f"<p>{lab['objective']}</p>"
              f'<div class="pt-assume"><b>Assumptions for this lab</b>'
              f'<ul class="pt-assump-list">{assume}</ul></div>')
    devices = "".join(f"<li>{d}</li>" for d in lab["devices"])
    s2 = _sec(2, "Required devices", f"<ul>{devices}</ul>")
    s3 = _sec(3, "Network topology description",
              f'<p>{lab["topo_desc"]}</p>'
              f'<div class="pt-topo">{TOPOS[lab["id"]]()}'
              f'<p class="cap">{lab["topo_cap"]}</p></div>')
    s4 = _sec(4, "IP addressing table",
              f'<p>{lab["addr_note"]}</p>'
              + _addr_table(lab["addr_cols"], lab["addr_rows"]))
    steps = "".join(
        f"<li><b>{t}.</b> {html}</li>" for t, html in lab["steps"])
    s5 = _sec(5, "Step-by-step configuration instructions",
              f'<ol class="pt-steps">{steps}</ol>')
    s6 = _sec(6, "Relevant Cisco IOS commands",
              f'<p>{lab["cmds_note"]}</p>' + _cmd_table(lab["cmds"]))
    ver = "".join(f"<li><code>{c}</code> — {d}</li>" for c, d in lab["verify"])
    s7 = _sec(7, "Verification commands", f"<ul>{ver}</ul>")
    exp = "".join(f"<li>{e}</li>" for e in lab["expected"])
    s8 = _sec(8, "Expected results", f"<ul>{exp}</ul>")
    mist = "".join(f"<li>{m}</li>" for m in lab["mistakes"])
    s9 = _sec(9, "Common mistakes", f"<ul>{mist}</ul>")
    s10 = _sec(10, "Troubleshooting questions", _tsq(lab["tsq"]))
    s11 = _sec(11, "Self-assessment quiz",
               f'<p>{lab["quiz_note"]}</p>' + _quiz(lab["id"], lab["quiz"]))
    ck = _checklist(lab)
    return (f'<section class="pt-lab" id="{lab["id"]}">{hd}'
            f"{s1}{s2}{s3}{s4}{s5}{s6}{s7}{s8}{s9}{s10}{s11}"
            f'<div class="pt-sec">{ck}</div></section>')


# --------------------------------------------------------------------------
# LAB CONTENT
# --------------------------------------------------------------------------
LABS = [
    # ================= LAB 1 =================
    {
        "id": "lab1", "n": 1, "title": "Basic Network Setup",
        "objective": (
            "Build your first network in the official <b>Cisco Packet Tracer</b> "
            "application: place two PCs and a switch, connect them with the right "
            "copper cabling, give the PCs IPv4 addresses and subnet masks, and prove "
            "connectivity with <b>ping</b>. This practises the course's addressing "
            "rules — every end device needs an address + mask "
            + ref(2, 33) + " — on a single network where no default gateway is "
            "required " + ref(6, 31) + "."),
        "assumptions": [
            "<b>Assumption</b> — the course does not name Packet Tracer objects: "
            "devices use Packet Tracer defaults (<code>PC0</code>, <code>PC1</code>, "
            "<code>Switch0</code>).",
            "<b>Assumption</b> — cabling: use <b>Copper Straight-Through</b> between "
            "PC and switch (course covers UTP/RJ-45 copper media in Ch 4 "
            + ref(4, 13) + " and Auto-MDIX crossover handling in Ch 5 "
            + ref(5, 27) + "; the PC↔switch cable name itself is Packet Tracer "
            "convention).",
            "<b>Assumption</b> — addresses below are chosen for practice; the course "
            "uses 192.168.10.0/24 style LAN addresses in its examples "
            + ref(6, 29) + " but does not prescribe addresses for this exercise.",
            "<b>Packet Tracer workflow</b> — IPs are entered in "
            "<i>Desktop → IP Configuration</i> and ping in "
            "<i>Desktop → Command Prompt</i>; the course states devices "
            "must be configured " + ref(2, 33) + " but not through which GUI.",
        ],
        "devices": [
            "<b>2 × end devices (PCs)</b> — the course's end-device class: computers "
            "that are source or destination of messages " + ref(1, 10) + ".",
            "<b>1 × intermediary device (switch)</b> — connects end devices, "
            "switches on MAC addresses and builds a MAC address table "
            + ref(5, 24) + ".",
            "<b>2 × Copper Straight-Through Ethernet cables</b> (UTP, RJ-45) "
            + ref(4, 13) + ".",
        ],
        "topo_desc": (
            "One LAN, one broadcast domain: <b>PC0 — Switch0 — PC1</b>, all inside "
            "<b>192.168.10.0/24</b>. There is no router, so nothing leaves the "
            "network — and per the course's own gateway figures, a default gateway "
            "<i>is not needed</i> when hosts communicate on the same network "
            + ref(6, 31) + ". The course also stresses that a topology diagram "
            "documents devices, ports and the addressing scheme " + ref(1, 14) + " — "
            "the table below is that scheme for this lab."),
        "topo": None,          # filled below
        "topo_cap": "Lab 1 topology — a single /24 LAN. Diagram drawn for this exercise.",
        "addr_note": (
            "Plan (assumption — chosen for this practice): one /24 network, two host "
            "addresses, <b>no gateway</b>. Mask 255.255.255.0 = /24 "
            + ref(2, 33) + "."),
        "addr_cols": ["Device", "Interface", "IPv4 address", "Subnet mask",
                      "Default gateway"],
        "addr_rows": [
            ["PC0", "FastEthernet0", "192.168.10.10", "255.255.255.0",
             "(leave empty — same network)"],
            ["PC1", "FastEthernet0", "192.168.10.11", "255.255.255.0",
             "(leave empty — same network)"],
            ["Switch0", "—", "(none required)", "—", "—"],
        ],
        "steps": [
            ("Open the official Packet Tracer application", 
             "Create a new empty topology. <b>This website cannot run Packet "
             "Tracer</b> — everything below happens in the Packet Tracer app on your "
             "computer."),
            ("Place the devices",
             "From the device-type bar choose <i>End Devices → PC-PT</i> twice, then "
             "<i>Network Devices → Switches → 2960</i> once (any switch that "
             "offers Ethernet ports works). <b>Assumption:</b> the course does not "
             "specify a switch model. " + ref(5, 24)),
            ("Connect with the correct cable",
             "Use the lightning/connections menu → <b>Copper Straight-Through</b>: "
             "PC0 <code>FastEthernet0</code> → any switch Ethernet port, and PC1 "
             "→ another switch port. Links show green triangles when the link is up. "
             + ref(4, 13)),
            ("Address PC0",
             "<i>PC0 → Desktop → IP Configuration</i>: IPv4 address "
             "<code>192.168.10.10</code>, Subnet Mask <code>255.255.255.0</code>, "
             "Default Gateway <b>blank</b>. Every end device needs address + mask "
             + ref(2, 33) + "."),
            ("Address PC1",
             "<i>PC1 → Desktop → IP Configuration</i>: <code>192.168.10.11</code>, "
             "<code>255.255.255.0</code>, gateway blank. Both PCs must be in the same "
             "network — that is what makes the ping local."),
            ("Test with ping",
             "<i>PC0 → Desktop → Command Prompt</i>: <code>ping "
             "192.168.10.11</code>. Watch for replies; then repeat from PC1 to PC0 "
             "(<code>ping 192.168.10.10</code>). Ping output follows the course's "
             "format " + ref(6, 30) + "."),
            ("Explain the result in your own words",
             "Write one sentence for your notes: why did these two PCs communicate "
             "with no router and no default gateway? (Answer lives in "
             "troubleshooting Q3 and the course's 'Default Gateway not needed' "
             "figure " + ref(6, 31) + ".)"),
        ],
        "cmds_note": (
            "Switches need <b>no IOS configuration</b> for this lab — they forward "
            "using the MAC address table they build themselves " + ref(5, 24) + ". "
            "The ping below runs on the PC's command prompt (Packet Tracer "
            "Desktop), not in IOS; the same <code>ping</code> command exists on "
            "router IOS " + ref(6, 30) + "."),
        "cmds": [
            ("ping 192.168.10.11",
             "PC0 — <i>Desktop → Command Prompt</i> (Packet Tracer, not IOS)",
             "Five ICMP echo requests to PC1 — the course's connectivity test "
             + ref(6, 30) + "."),
            ("ping 192.168.10.10", "PC1 — Command Prompt",
             "Return path test — connectivity must work in both directions."),
            ("(no IOS commands)", "Switch0",
             "Nothing to type: switches switch at Layer 2 from their MAC address "
             "table " + ref(5, 24) + ". <b>Assumption:</b> no switch management "
             "IP is required for this lab (course covers switch default gateways "
             "separately " + ref(6, 32) + ")."),
        ],
        "verify": [
            ("ping 192.168.10.11", "from PC0 — echo replies from PC1"),
            ("ping 192.168.10.10", "from PC1 — echo replies from PC0"),
            ("(check) IP Configuration screen", "both PCs show mask "
             "255.255.255.0 and an address in 192.168.10.0/24"),
            ("(check) link lights", "green up-flags on every connection you made"),
        ],
        "expected": [
            "Ping output in the course's format: <code>Sending 5, 100-byte ICMP "
            "Echos … !!!!! Success rate is 100 percent (5/5)</code> "
            + ref(6, 30) + " — five exclamation marks, no timeouts.",
            "Ping works in <b>both</b> directions (PC0 → PC1 and PC1 → PC0).",
            "Both PCs answer with each other's addresses because they share one "
            "network — no router traffic appears in the topology.",
            "<b>PT note (assumption):</b> the very first ping may lose one packet "
            "while ARP resolves the neighbour's MAC address " + ref(5, 19) + " — "
            "a second ping is then 5/5. The course's own example shows 5/5 "
            + ref(6, 30) + ".",
        ],
        "mistakes": [
            "Swapping address and mask fields, or typing a mask that does not match "
            "the address plan (both PCs must be 255.255.255.0).",
            "Putting a <b>default gateway</b> on these PCs — this lab needs none; a "
            "gateway only matters when leaving the network " + ref(6, 31) + ".",
            "Using different networks (e.g. 192.168.10.10 with 192.168.11.10) — that "
            "silently turns a local ping into a routed one that must fail here.",
            "Connecting PC→PC directly instead of through the switch (works only by "
            "accident with Auto-MDIX " + ref(5, 27) + " — build it the way the "
            "topology shows).",
            "Forgetting to press the apply/save in the IP Configuration window, then "
            "pinging the old (empty) settings.",
            "Reading one successful ping as 'the whole network is done' — the lab "
            "requires the return ping too (course: testing the interface assignment "
            + ref(2, 38) + ").",
        ],
        "tsq": [
            {"q": "PC0's ping to PC1 shows <code>Request timed out</code> the whole "
                  "time. Give the first three things you would check, in order.",
             "a": "1) Physical/link: are the cables Copper Straight-Through on working "
                  "switch ports (green indicators) " + ref(5, 24) + "? 2) Addressing: "
                  "do both PCs share one network and the same mask (192.168.10.x with "
                  "255.255.255.0)? 3) Conflicts/typos: is any address duplicated "
                  "(course: IP address conflicts " + ref(2, 37) + ") or mistyped? "
                  "Only after those does ARP/resolution matter " + ref(5, 19) + "."},
            {"q": "Your first ping loses one reply but the next ping is 5/5. Why is "
                  "this not a failure?",
             "a": "The first echo may time out while the PC resolves the destination's "
                  "MAC address into its ARP table " + ref(5, 19) + ". Once cached, "
                  "every echo answers — the course's reference output is 5/5 "
                  + ref(6, 30) + ". <b>Assumption:</b> Packet Tracer exhibits this "
                  "ARP warm-up behaviour; the course does not describe it."},
            {"q": "Why do PC0 and PC1 need no router and no default gateway, even "
                  "though they are different devices?",
             "a": "They are on the <b>same</b> network (192.168.10.0/24): the switch "
                  "forwards frames between their ports using MAC addresses "
                  + ref(5, 24) + ", and a gateway is only needed to leave the network "
                  "— the course labels this exact case 'Default Gateway not needed' "
                  + ref(6, 31) + "."},
        ],
        "quiz_note": "Five questions — pick an answer, then press <b>Check "
                     "answers</b>. The correct option and the course-based "
                     "explanation appear immediately.",
        "quiz": [
            {"q": "PC0 is 192.168.10.10 and PC1 is 192.168.10.11, both mask 255.255.255.0, no gateway configured. Which statement is correct?", "opts": ["Both are in 192.168.10.0/24, so they exchange frames directly "
                      "through the switch",
                      "They must be given a default gateway before any ping works",
                      "A router must forward the ping between two PCs on one LAN",
                      "They need different subnet masks to talk to each other"],
             "a": 0,
             "why": "Same network + switch forwarding " + ref(5, 24) +
                    "; gateways are for leaving the network " + ref(6, 31) + "."},
            {"q": "In this lab a default gateway must be configured on both PCs because the ping travels across network devices.", "opts": ["True", "False"], "a": 1,
             "why": "False — the course's own figure marks same-network hosts "
                    "'Default Gateway not needed' " + ref(6, 31) + "."},
            {"q": "Which connection type should you use between each PC and the switch?", "opts": ["Copper Straight-Through (UTP) — PC to switch",
                      "A serial WAN cable",
                      "A console cable for every data connection",
                      "Fiber must be used whenever PCs are involved"],
             "a": 0,
             "why": "Copper straight-through is the Packet Tracer convention for "
                    "PC↔switch (assumption, built on the course's UTP/RJ-45 media "
                    + ref(4, 13) + "); Auto-MDIX would also forgive a crossover "
                    + ref(5, 27) + "."},
            {"q": "Your ping output ends with: !!!!! Success rate is 100 percent (5/5). What does this tell you?", "opts": ["All five echo requests were answered — 100% success",
                      "Five percent of packets were lost",
                      "The ping travelled five hops",
                      "The connection failed five times"],
             "a": 0,
             "why": "The course's ping output: '!!!!! Success rate is 100 percent "
                    "(5/5)' " + ref(6, 30) + " — each ! is one reply."},
            {"q": "Which address and mask pair matches this lab's plan for PC0?", "opts": ["192.168.10.10 with 255.255.255.0",
                      "192.168.10.10 with 255.255.0.0",
                      "192.168.11.10 with 255.255.255.0",
                      "192.168.10.1 with 255.255.255.0 (as a PC address)"],
             "a": 0,
             "why": "The plan: .10/24 inside 192.168.10.0/24. /16 is the wrong mask, "
                    "192.168.11.10 is a different network, and .1 is reserved here "
                    "for the router interface of Lab 2 " + ref(6, 29) + "."},
        ],
        "checklist": [
            "Opened the official Packet Tracer app (this website does not run it)",
            "Placed PC0, PC1 and Switch0",
            "Connected both PCs to the switch with copper straight-through cables "
            "(link lights green)",
            "Set PC0 to 192.168.10.10 / 255.255.255.0, no gateway",
            "Set PC1 to 192.168.10.11 / 255.255.255.0, no gateway",
            "Pinged PC1 from PC0 and saw replies (5/5 format)",
            "Pinged PC0 from PC1 (both directions verified)",
            "Wrote down why no default gateway was needed",
        ],
    },
    # ================= LAB 2 =================
    {
        "id": "lab2", "n": 2, "title": "Connecting Different Networks",
        "objective": (
            "Join two separate networks with a router: configure both router "
            "interfaces with IPv4 addresses, <b>enable</b> them, set the PCs' default "
            "gateways, and prove <b>end-to-end connectivity</b> across network "
            "boundaries. This is the course's own scenario — LAN "
            "<b>192.168.10.0/24</b> on G0/0 and LAN <b>192.168.11.0/24</b> on G0/1, "
            "each interface acting as its LAN's default gateway " + ref(6, 29) +
            " " + ref(6, 31) + "."),
        "assumptions": [
            "<b>Assumption</b> — device names: the router is renamed <code>R1</code> "
            "with <code>hostname R1</code>, exactly as in the course steps "
            + ref(6, 28) + "; Packet Tracer defaults to <code>Router0</code>, "
            "<code>Switch0</code>/<code>Switch1</code>, <code>PC0</code>/<code>PC1</code>.",
            "<b>Course basis</b> — all addresses (10.0/11.0 LANs, .1 interfaces, .10 "
            "hosts) come from the course's own figures " + ref(6, 28) +
            " " + ref(6, 31) + ".",
            "<b>Assumption</b> — scope: the course figure also shows a serial link to "
            "R2 " + ref(6, 30) + "; this lab stops at the two LANs, as required.",
            "<b>Assumption</b> — no passwords/secret are set (the course's step slide "
            "includes <code>enable secret</code> " + ref(6, 28) + "; skipping it "
            "keeps this lab focused on addressing).",
        ],
        "devices": [
            "<b>1 × router</b> (Packet Tracer 4221/1941 or similar with Gigabit "
            "Ethernet interfaces) — routers pass data between IP subnetworks "
            + ref(5, 24) + ".",
            "<b>2 × switches</b> — one per LAN " + ref(5, 24) + ".",
            "<b>2 × PCs</b> (one per LAN) " + ref(1, 10) + ".",
            "<b>4 × Copper Straight-Through cables</b> (PC↔switch, switch↔router) "
            + ref(4, 13) + ".",
        ],
        "topo_desc": (
            "Two LANs joined by one router: <b>PC0 — SW0 — R1 — SW1 — PC1</b>. "
            "R1's <b>G0/0</b> (192.168.10.1) is LAN-A's default gateway; "
            "<b>G0/1</b> (192.168.11.1) is LAN-B's. Each PC uses its own LAN's "
            "interface as gateway " + ref(6, 31) + ". Devices, ports and addresses "
            "are documented in the table — the diagram's purpose per the course "
            + ref(1, 14) + "."),
        "topo": None,
        "topo_cap": "Lab 2 topology — the course's two-LAN router scenario "
                    "(Ch 6 slides 28–31), LAN-only scope.",
        "addr_note": (
            "<b>Course figures</b> — identical to Ch 6 slides 28–31: both interfaces "
            ".1, hosts .10 " + ref(6, 29) + "."),
        "addr_cols": ["Device", "Interface", "IPv4 address", "Subnet mask",
                      "Default gateway"],
        "addr_rows": [
            ["PC0 (LAN-A)", "FastEthernet0", "192.168.10.10", "255.255.255.0",
             "192.168.10.1"],
            ["R1", "GigabitEthernet0/0", "192.168.10.1", "255.255.255.0", "—"],
            ["R1", "GigabitEthernet0/1", "192.168.11.1", "255.255.255.0", "—"],
            ["PC1 (LAN-B)", "FastEthernet0", "192.168.11.10", "255.255.255.0",
             "192.168.11.1"],
        ],
        "steps": [
            ("Place and cable the devices",
             "2 PCs, 2 switches, 1 router. Copper straight-through: PC0→SW0, "
             "SW0→R1 <code>G0/0</code>, SW1→R1 <code>G0/1</code>, PC1→SW1 "
             + ref(4, 13) + ". Use the router's <b>GigabitEthernet</b> ports "
             "— the course configures G0/0 and G0/1 " + ref(6, 29) + "."),
            ("Configure PC0 (LAN-A)",
             "IP <code>192.168.10.10</code>, mask <code>255.255.255.0</code>, "
             "<b>gateway 192.168.10.1</b> — the gateway is R1's G0/0 address "
             + ref(6, 31) + "."),
            ("Configure PC1 (LAN-B)",
             "IP <code>192.168.11.10</code>, mask <code>255.255.255.0</code>, "
             "<b>gateway 192.168.11.1</b> (R1's G0/1)."),
            ("Enter the router configuration mode",
             "Click R1 → CLI (or console " + ref(2, 38) + "). Follow the course "
             "steps: <code>enable</code> → <code>configure terminal</code> "
             "(abbreviated <code>conf t</code>) → <code>hostname R1</code> "
             + ref(6, 28) + "."),
            ("Configure and enable G0/0 (LAN-A)",
             "<code>interface gigabitethernet 0/0</code> → <code>ip address "
             "192.168.10.1 255.255.255.0</code> → <code>description Link to "
             "LAN-10</code> → <code>no shutdown</code> — watch for "
             "<code>%LINK-5-CHANGED: … changed state to up</code> "
             + ref(6, 29) + "."),
            ("Configure and enable G0/1 (LAN-B)",
             "<code>int g0/1</code> → <code>ip add 192.168.11.1 255.255.255.0</code> "
             "→ <code>des Link to LAN-11</code> → <code>no shut</code> → "
             "<code>exit</code> → <code>end</code> — same transcript pattern as "
             "the course " + ref(6, 29) + "."),
            ("Verify interfaces and routing table",
             "Run <code>show ip interface brief</code> and <code>show ip route</code> "
             "— both interfaces must read <code>up up</code> and the table must "
             "list both LANs as <code>C</code> (connected) entries "
             + ref(6, 30) + " " + ref(6, 14) + "."),
            ("Test end-to-end and save",
             "From PC0: <code>ping 192.168.11.10</code> (and back from PC1 to "
             "<code>192.168.10.10</code>). Then on R1: <code>copy running-config "
             "startup-config</code> to keep the work " + ref(6, 30) + "."),
        ],
        "cmds_note": (
            "The router rows below follow the course's transcript exactly "
            + ref(6, 28) + " " + ref(6, 29) + " (including the abbreviations "
            "<code>conf t</code>, <code>int g0/1</code>, <code>ip add</code>, "
            "<code>des</code>, <code>no shut</code>)."),
        "cmds": [
            ("enable", "R1 user EXEC (Router>)", "Enter privileged EXEC mode "
             + ref(6, 28) + "."),
            ("configure terminal", "R1 privileged EXEC (R1#)",
             "Enter global configuration mode — 'conf t' " + ref(6, 28) + "."),
            ("hostname R1", "R1(config)", "Name the device R1 " + ref(6, 28) + "."),
            ("interface gigabitethernet 0/0", "R1(config)",
             "Select the LAN-A interface " + ref(6, 29) + "."),
            ("ip address 192.168.10.1 255.255.255.0", "R1(config-if)",
             "Address G0/0 — becomes LAN-A's default gateway " + ref(6, 29) + "."),
            ("description Link to LAN-10", "R1(config-if)",
             "Label the interface " + ref(6, 29) + "."),
            ("no shutdown", "R1(config-if)",
             "<b>Enable</b> the interface (administratively up) " + ref(6, 29) + "."),
            ("int g0/1 / ip add 192.168.11.1 255.255.255.0 / des Link to LAN-11 / "
             "no shut", "R1(config)",
             "Same sequence for LAN-B " + ref(6, 29) + "."),
            ("end", "R1(config-if)", "Return to privileged EXEC (R1#) " + ref(6, 29) + "."),
            ("show ip interface brief", "R1 privileged EXEC",
             "Verify addresses/status/protocol of every interface " + ref(6, 30) + "."),
            ("show ip route", "R1 privileged EXEC",
             "Verify connected routes — C entries " + ref(6, 14) + "."),
            ("ping <address>", "R1 or a PC",
             "End-to-end reachability test " + ref(6, 30) + "."),
            ("copy running-config startup-config", "R1 privileged EXEC",
             "Save the configuration " + ref(6, 30) + "."),
        ],
        "verify": [
            ("show ip interface brief", "G0/0 = 192.168.10.1 up/up, G0/1 = "
             "192.168.11.1 up/up " + ref(6, 30)),
            ("show ip route", "C 192.168.10.0/24 … GigabitEthernet0/0 and "
             "C 192.168.11.0/24 … GigabitEthernet0/1 " + ref(6, 14)),
            ("ping 192.168.10.1  (from PC0)", "PC0 reaches its gateway"),
            ("ping 192.168.11.1  (from PC1)", "PC1 reaches its gateway"),
            ("ping 192.168.11.10  (from PC0)", "end-to-end across networks"),
            ("ping 192.168.10.10  (from PC1)", "end-to-end return direction"),
        ],
        "expected": [
            "<code>show ip interface brief</code> matches the course's output: "
            "<code>GigabitEthernet0/0 192.168.10.1 YES manual up up</code> and "
            "<code>GigabitEthernet0/1 192.168.11.1 YES manual up up</code> "
            + ref(6, 30) + ".",
            "During configuration: <code>%LINK-5-CHANGED: Interface "
            "GigabitEthernet0/0, changed state to up</code> after each "
            "<code>no shutdown</code> " + ref(6, 29) + ".",
            "<code>show ip route</code> lists <code>C 192.168.10.0/24 is directly "
            "connected, GigabitEthernet0/0</code> and the 192.168.11.0/24 equivalent "
            + ref(6, 14) + ".",
            "Cross-network ping: <code>!!!!! Success rate is 100 percent (5/5)</code> "
            "PC0 ↔ PC1 " + ref(6, 30) + ".",
            "Saving asks <code>Destination filename [startup-config]?</code> — "
            "accept it " + ref(6, 30) + ".",
        ],
        "mistakes": [
            "Forgetting <code>no shutdown</code> — the interface stays "
            "<i>administratively down</i> (the course shows exactly this state in "
            "its brief output " + ref(6, 30) + ").",
            "Configuring the right address on the <b>wrong interface</b> (G0/0 and "
            "G0/1 swapped) — each address must belong to the network the interface "
            "connects " + ref(6, 29) + ".",
            "Wrong PC gateway: LAN-B PCs must use 192.168.11.1, not .10.1 "
            + ref(6, 31) + ".",
            "Mask typos on the router (255.255.0.0) — the interface and its LAN fall "
            "into different networks.",
            "Testing only one direction, or only gateway pings — end-to-end means "
            "host-to-host both ways " + ref(2, 38) + ".",
            "Leaving the configuration unsaved — <code>copy running-config "
            "startup-config</code> " + ref(6, 30) + ".",
        ],
        "tsq": [
            {"q": "PC0 cannot reach PC1. PC0's local ping to its own switch-neighbours "
                  "works. What ordered checks isolate the fault fastest?",
             "a": "1) <code>ping 192.168.10.1</code> from PC0 (gateway reachable? if "
                  "not: R1 G0/0 address/enable state — <code>show ip interface "
                  "brief</code> " + ref(6, 30) + "). 2) Same for PC1 with 192.168.11.1. "
                  "3) On R1: are both LANs in <code>show ip route</code> as C entries "
                  + ref(6, 14) + "? 4) Re-check PC gateway fields against the table "
                  + ref(6, 31) + ". This 'local → gateway → remote' order is the "
                  "course's testing-the-interface pattern " + ref(2, 38) + "."},
            {"q": "<code>show ip interface brief</code> shows an interface "
                  "<code>administratively down</code>. What caused it and what is the "
                  "fix?",
             "a": "The interface was never enabled — a freshly configured interface "
                  "stays administratively down until <code>no shutdown</code> is "
                  "issued " + ref(6, 29) + "; the course's brief output shows the "
                  "state " + ref(6, 30) + "."},
            {"q": "Why must PC0's gateway be 192.168.10.1 and not 192.168.11.1?",
             "a": "A host's default gateway is the router interface <b>on its own "
                  "network</b> " + ref(6, 31) + " — for PC0 that is R1's G0/0 "
                  "(192.168.10.1) " + ref(6, 29) + ". The gateway must be reachable "
                  "in-layer before it can forward anywhere else."},
            {"q": "Both router interfaces are up/up and both C routes exist, yet PC0 "
                  "pings 192.168.11.10 with 0% success. What is left to check?",
             "a": "PC-side settings: PC0's mask (must be 255.255.255.0) and its "
                  "gateway value; PC1's address/mask/gateway against the table; then "
                  "link/ARP — addresses and conflicts " + ref(2, 37) +
                  ". Router output alone never proves end-device configuration "
                  + ref(2, 33) + "."},
        ],
        "quiz_note": "Five questions on the configuration flow — instant marking "
                     "with course-based explanations.",
        "quiz": [
            {"q": "What is the correct command sequence to reach interface configuration mode on R1?", "opts": ["enable → configure terminal → interface gigabitethernet 0/0",
                      "configure terminal → enable → ip address",
                      "interface g0/0 → enable → hostname",
                      "enable → ip address → configure terminal"],
             "a": 0,
             "why": "The course's Router Configuration Steps: <code>enable</code> → "
                    "<code>configure terminal</code>, then interface selection "
                    + ref(6, 28) + " " + ref(6, 29) + "."},
            {"q": "After assigning an interface's IP address you must still run no shutdown before the interface will pass traffic.", "opts": ["True", "False"], "a": 0,
             "why": "True — each LAN interface needs <code>no shutdown</code>; the "
                    "course transcript shows 'changed state to up' immediately after "
                    + ref(6, 29) + ", and a missed one reads 'administratively down' "
                    + ref(6, 30) + "."},
            {"q": "PC1 sits on 192.168.11.0/24. What must its default gateway be?", "opts": ["192.168.11.1 — R1's G0/1 address on LAN-B",
                      "192.168.11.10 — the other PC's address",
                      "192.168.10.1 — R1's G0/0 address",
                      "255.255.255.0 — the subnet mask"],
             "a": 0,
             "why": "The gateway is the router interface on the host's own network "
                    + ref(6, 31) + " — G0/1 = 192.168.11.1 " + ref(6, 29) + "."},
            {"q": "show ip interface brief shows: GigabitEthernet0/0 192.168.10.1 YES manual up up. What does this line confirm?", "opts": ["G0/0 is addressed 192.168.10.1 and its link/protocol are both "
                      "up",
                      "G0/0 is connected to LAN-B",
                      "G0/0 has been saved to startup-config",
                      "G0/0 is passing PC0's pings automatically"],
             "a": 0,
             "why": "The brief shows IP-Address + Status + Protocol per interface "
                    + ref(6, 30) + "; routing/saving are separate checks "
                    + ref(6, 14) + "."},
            {"q": "Which pair of lines in show ip route proves both LANs are directly connected to R1?", "opts": ["C 192.168.10.0/24 is directly connected, GigabitEthernet0/0 "
                      "and C 192.168.11.0/24 … GigabitEthernet0/1",
                      "S 192.168.10.0/24 via 10.0.0.1",
                      "R 192.168.10.0/24 [120/1] via 192.168.11.1",
                      "G 0.0.0.0/0 via 209.165.200.1"],
             "a": 0,
             "why": "Connected LANs appear as <code>C</code> (local, directly "
                    "connected) entries pointing at the interface — exactly the "
                    "course's route output " + ref(6, 14) + "."},
        ],
        "checklist": [
            "Built the 5-device topology and cabled all four links",
            "PC0: 192.168.10.10/24 with gateway 192.168.10.1",
            "PC1: 192.168.11.10/24 with gateway 192.168.11.1",
            "Router renamed R1 (enable → conf t → hostname)",
            "G0/0 configured 192.168.10.1/24 + description + no shutdown",
            "G0/1 configured 192.168.11.1/24 + description + no shutdown",
            "show ip interface brief: both interfaces up up",
            "show ip route: C entries for both LANs",
            "End-to-end ping works both directions (5/5)",
            "Configuration saved with copy running-config startup-config",
        ],
    },
    # ================= LAB 3 =================
    {
        "id": "lab3", "n": 3, "title": "Subnetting and IP Address Planning",
        "objective": (
            "Take one network address and a list of host requirements, calculate "
            "suitable subnets with the course's <b>2<sup>n</sup> − 2</b> formula "
            + ref(9, 6) + ", assign addresses to PCs and router interfaces, "
            "<b>verify every address sits inside the right subnet</b>, and catch "
            "addressing mistakes before they reach a real device. This is Chapter 9 "
            "practised hands-on — including VLSM sizing in the style of the "
            "course's /27-LAN, /30-WAN example " + ref(9, 10) + "."),
        "assumptions": [
            "<b>Assumption</b> — the requirement numbers (25 / 10 / 2 hosts) are "
            "practice values; the course gives the method (plan first: subnets "
            "required + host addresses required " + ref(9, 6) + ") but not this "
            "specific brief.",
            "<b>Course basis</b> — subnet sizes /27 for LANs and /30 for WAN links "
            "mirror the course's VLSM example " + ref(9, 10) + "; all math uses "
            "2<sup>n</sup> − 2 " + ref(9, 6) + ".",
            "<b>Assumption</b> — the optional second router (R2) extends the course's "
            "WAN idea (its own figure shows router-to-router links "
            + ref(6, 30) + "); it is not required to pass this lab.",
            "<b>Assumption</b> — same Packet Tracer GUI conventions as Labs 1–2 for "
            "entering addresses (the course does not specify GUI steps).",
        ],
        "devices": [
            "<b>1 × router (R1)</b> with ≥ 2 Gigabit Ethernet interfaces "
            + ref(6, 29) + ".",
            "<b>2 × switches</b> (SW0 for LAN-A, SW1 for LAN-B) " + ref(5, 24) + ".",
            "<b>2 × PCs</b> (one per LAN) " + ref(1, 10) + ".",
            "<b>4 × copper straight-through cables</b> " + ref(4, 13) + ".",
            "<b>(Optional) 1 × router (R2) + 2 × serial/copper links</b> for the "
            "/30 WAN extension — assumption, see objectives.",
        ],
        "topo_desc": (
            "The same two-LAN shape as Lab 2, but the address space "
            "<b>192.168.10.0/24</b> is carved into <b>unequal</b> subnets: LAN-A "
            "<b>/27</b> (25 hosts), LAN-B <b>/28</b> (10 hosts), and a <b>/30</b> "
            "WAN subnet (2 hosts) for the optional R1↔R2 link. Subnetting this way "
            "contains broadcasts and prepares for growth " + ref(9, 4) + "; VLSM "
            "sizing avoids the waste of equal blocks " + ref(9, 8) + " "
            + ref(9, 9) + "."),
        "topo": None,
        "topo_cap": "Lab 3 topology — one /24 planned into /27 + /28 (+ optional /30 "
                    "WAN). Diagram drawn for this exercise.",
        "addr_note": (
            "Working (course method): <b>LAN-A</b> 25 hosts → n=5 remaining host "
            "bits → 2<sup>5</sup> = 32 − 2 = <b>30 usable</b> → /27, network "
            "<b>192.168.10.0</b>, usable .1–.30, broadcast .31. <b>LAN-B</b> 10 "
            "hosts → n=4 → 2<sup>4</sup> = 16 − 2 = <b>14 usable</b> → /28, "
            "network <b>192.168.10.32</b>, usable .33–.46, broadcast .47. "
            "<b>WAN</b> 2 hosts → n=2 → 4 − 2 = <b>2 usable</b> → /30, network "
            "<b>192.168.10.48</b>, usable .49–.50, broadcast .51 "
            + ref(9, 6) + " " + ref(9, 8) + ". Design for the largest subnet and "
            "allow growth " + ref(9, 7) + "."),
        "addr_cols": ["Device", "Interface", "IPv4 address", "Prefix / mask",
                      "Subnet (network)", "Gateway"],
        "addr_rows": [
            ["PC0", "FastEthernet0", "192.168.10.10", "/27 · 255.255.255.224",
             "192.168.10.0 (usable .1–.30)", "192.168.10.1"],
            ["R1", "GigabitEthernet0/0", "192.168.10.1", "/27 · 255.255.255.224",
             "192.168.10.0", "—"],
            ["PC1", "FastEthernet0", "192.168.10.34", "/28 · 255.255.255.240",
             "192.168.10.32 (usable .33–.46)", "192.168.10.33"],
            ["R1", "GigabitEthernet0/1", "192.168.10.33", "/28 · 255.255.255.240",
             "192.168.10.32", "—"],
            ["R1 (optional)", "GigabitEthernet0/2", "192.168.10.49",
             "/30 · 255.255.255.252", "192.168.10.48 (usable .49–.50)", "—"],
            ["R2 (optional)", "GigabitEthernet0/0", "192.168.10.50",
             "/30 · 255.255.255.252", "192.168.10.48", "—"],
        ],
        "steps": [
            ("Write down the plan inputs",
             "The course's two questions first: <b>number of subnets required</b> "
             "and <b>number of host addresses required</b> " + ref(9, 6) + " → here: "
             "LAN-A 25, LAN-B 10, WAN 2."),
            ("Calculate with 2<sup>n</sup> − 2",
             "For each: pick n so 2<sup>n</sup> − 2 ≥ hosts, minus the two "
             "reserved addresses (subnetwork ID + broadcast) " + ref(9, 6) + ". "
             "Record network, usable range and broadcast for every block (see the "
             "addressing-table note)."),
            ("Lay out the VLSM blocks",
             "Take the blocks in order from 192.168.10.0: /27 → .0–.31, /28 → "
             ".32–.47, /30 → .48–.51 — subnet then resubnet with unequal sizes "
             "instead of one equal cut " + ref(9, 9) + " " + ref(9, 10) + "."),
            ("Build the topology",
             "Same physical build as Lab 2 (R1, 2 switches, 2 PCs + cables); "
             "add R2 and its link only for the WAN extension "
             + ref(4, 13) + "."),
            ("Assign addresses to PCs and router interfaces",
             "Configure exactly the table above: PC0 192.168.10.<b>10</b> /27 gw "
             ".1; R1 G0/0 .1/27; PC1 192.168.10.<b>34</b> /28 gw .33; R1 G0/1 "
             ".33/28 (+ optional .49/.50 on the /30). PC input via Desktop → IP "
             "Configuration; router via <code>enable → conf t → interface … → ip "
             "address … → no shut</code> " + ref(6, 29) + "."),
            ("Verify each address belongs to the correct subnet",
             "Check membership by range: .10 ∈ .0–.30 ✓ · .1 ∈ .0–.30 ✓ · "
             ".34 ∈ .33–.46 ✓ · .33 ∈ .33–.46 ✓ · .49/.50 ∈ .49–.50 ✓. "
             "Then cross-check on-device with <code>show ip interface brief</code> "
             + ref(6, 30) + " — or double-check ranges in the site's "
             "<a href=\"lab.html\">IPv4 Lab</a> calculator."),
            ("Identify the addressing mistakes (deliberate errors)",
             "The four rows below are wrong on purpose — find the fault in each, "
             "state the correct value from the plan, then fix them if you typed any "
             "into Packet Tracer."),
            ("Test and save",
             "PC0 → <code>ping 192.168.10.34</code> (cross-subnet via R1) and back "
             "→ <code>show ip route</code> shows three C entries (two LANs + WAN) "
             + ref(6, 14) + " → <code>copy running-config startup-config</code>."),
        ],
        "cmds_note": (
            "Same IOS commands as Lab 2, applied to the new addressing "
            + ref(6, 29) + "; on PCs, verification is done from the Desktop tools "
            "(assumption — Packet Tracer workflow)."),
        "cmds": [
            ("interface gigabitethernet 0/0 + ip address 192.168.10.1 "
             "255.255.255.224", "R1(config)",
             "Address the LAN-A gateway in the /27 " + ref(6, 29) + "."),
            ("interface gigabitethernet 0/1 + ip address 192.168.10.33 "
             "255.255.255.240", "R1(config)",
             "Address the LAN-B gateway in the /28 " + ref(6, 29) + "."),
            ("no shutdown", "R1(config-if)", "Enable each interface " + ref(6, 29) + "."),
            ("show ip interface brief", "R1 privileged EXEC",
             "Confirm all three addresses landed correctly " + ref(6, 30) + "."),
            ("show ip route", "R1 privileged EXEC",
             "Connected C entries for every planned subnet " + ref(6, 14) + "."),
            ("ping <address>", "PC command prompt / R1",
             "Reachability across the new subnets " + ref(6, 30) + "."),
        ],
        "verify": [
            ("show ip interface brief", "G0/0 192.168.10.1/27, G0/1 "
             "192.168.10.33/28, both up up " + ref(6, 30)),
            ("show ip route", "C entries: 192.168.10.0/27, 192.168.10.32/28, "
             "(optional) 192.168.10.48/30 " + ref(6, 14)),
            ("ping 192.168.10.34 (from PC0)", "cross-subnet traffic via R1"),
            ("ping 192.168.10.10 (from PC1)", "return direction"),
            ("(range check)", "every assigned host address falls inside its "
             "subnet's usable range — formula 2^n − 2 " + ref(9, 6)),
        ],
        "expected": [
            "Plan maths: /27 → 30 usable, /28 → 14 usable, /30 → 2 usable — all "
            "from 2<sup>n</sup> − 2 " + ref(9, 6) + ".",
            "Every address in the table passes the range test (usable .1–.30 / "
            ".33–.46 / .49–.50).",
            "Cross-subnet ping succeeds: <code>!!!!! Success rate is 100 percent "
            "(5/5)</code> " + ref(6, 30) + " — proving R1 routes between the "
            "subnets " + ref(5, 24) + ".",
            "No broadcast (.31/.47/.51) or network ID (.0/.32/.48) is used on any "
            "device " + ref(9, 6) + ".",
            "(Optional WAN) R1↔R2 ping over .49 → .50 works with only two usable "
            "addresses — minimal waste " + ref(9, 8) + ".",
        ],
        "mistakes": [
            "Counting 2<sup>n</sup> instead of 2<sup>n</sup> − 2 — .31/.47/.51 are "
            "broadcasts, never assignable " + ref(9, 6) + ".",
            "Misaligned block sizes: a /27 starts at .0, the next block at .32 "
            "(not .31) — blocks must not overlap " + ref(9, 9) + ".",
            "Gateway chosen outside the host's subnet (e.g. .1 on the LAN-B PC) "
            + ref(6, 31) + ".",
            "Applying /24 masks by habit from Labs 1–2 — masks must match each "
            "prefix (.224 / .240 / .252).",
            "Handing every subnet the same size — that is traditional subnetting "
            "and it wastes addresses (WAN needs only two) " + ref(9, 8) + ".",
            "Skipping the growth check — design for the largest subnet's maximum "
            "hosts and allow growth " + ref(9, 7) + ".",
        ],
        "tsq": [
            {"q": "A classmate assigns <b>192.168.10.60/27</b> to a LAN-A PC. "
                  "Correct them.",
             "a": "192.168.10.0/27 covers .0–.31 only — .60 is outside it (and "
                  "outside all three planned blocks: .0–.31, .32–.47, .48–.51). "
                  "Usable LAN-A hosts are .1–.30 " + ref(9, 6) + "."},
            {"q": "Why can 192.168.10.<b>31</b> never be the default gateway for "
                  "LAN-A?",
             "a": "31 is the <b>broadcast address</b> of the /27 — the course's −2 "
                  "rule: subnetwork ID and broadcast cannot be used "
                  + ref(9, 6) + ". Gateways are host addresses (.1 in the plan)."},
            {"q": "Is 192.168.10.<b>40</b>/28 a valid PC address in LAN-B? What "
                  "about 192.168.10.<b>33</b> on G0/1?",
             "a": "Yes to both: /28 usable is .33–.46, so .40 is a fine host and "
                  ".33 (the gateway per the plan) is inside the same subnet "
                  + ref(9, 6) + ". Ranges — not familiar-looking numbers — decide "
                  "validity."},
            {"q": "R1's G0/1 is given 192.168.10.<b>65</b>/28. What fails and "
                  "why?",
             "a": "65 is not in 192.168.10.32/28 (.32–.47) — the interface address "
                  "must belong to the subnet it connects " + ref(9, 4) + ". Fix: "
                  "use the plan's 192.168.10.33/28 " + ref(6, 29) + "."},
        ],
        "quiz_note": "Five questions on planning and verification — marking is "
                     "instant, with the full reasoning.",
        "quiz": [
            {"q": "How many usable host addresses does a /27 subnet provide?", "opts": ["30 usable hosts (2^5 − 2)",
                      "32 usable hosts (2^5)",
                      "31 usable hosts (2^5 − 1)",
                      "27 usable hosts"],
             "a": 0,
             "why": "n=5 remaining host bits → 32 addresses minus subnetwork ID and "
                    "broadcast = 30 " + ref(9, 6) + "."},
            {"q": "After taking 192.168.10.0/27 for LAN-A, what is the network address of the next block — the /28 for LAN-B?", "opts": ["192.168.10.32", "192.168.10.16", "192.168.10.48",
                      "192.168.10.0"],
             "a": 0,
             "why": "The /27 consumes .0–.31, so the next block (the /28) starts at "
                    ".32 " + ref(9, 9) + " " + ref(9, 10) + "."},
            {"q": "192.168.10.60/27 is a valid host address for a PC on LAN-A.", "opts": ["True", "False"], "a": 1,
             "why": "False — usable in .0/27 is .1–.30; .60 lies outside the subnet "
                    "entirely " + ref(9, 6) + "."},
            {"q": "A WAN link needs exactly two usable addresses. Which option is correct?", "opts": ["/30 — 192.168.10.49 and 192.168.10.50 are the usable pair",
                      "/24 — WAN links should get the biggest block",
                      "/27 — reuse the LAN size for consistency",
                      "/29 — five usable addresses are needed"],
             "a": 0,
             "why": "A /30 gives exactly 2 usable addresses — the course's WAN "
                    "choice " + ref(9, 8) + " " + ref(9, 10) + "."},
            {"q": "Which assignment is correct according to the lab plan?", "opts": ["R1 G0/1 = 192.168.10.33 / 255.255.255.240 (LAN-B)",
                      "R1 G0/1 = 192.168.10.1 / 255.255.255.240",
                      "PC1 = 192.168.10.60 / 255.255.255.224 (LAN-A)",
                      "PC0 gateway = 192.168.10.31"],
             "a": 0,
             "why": ".33 is inside LAN-B's .32/28 with the /28 mask; the others put "
                    "an address outside its subnet, use the wrong block, or take "
                    "the broadcast address " + ref(9, 6) + "."},
        ],
        "checklist": [
            "Wrote the plan inputs (subnets required + hosts required)",
            "Calculated /27, /28, /30 with 2^n − 2 and recorded ranges/broadcasts",
            "Built the topology (R1, 2 switches, 2 PCs; R2 optional)",
            "Configured PC0 and PC1 with addresses inside their subnets",
            "Configured R1 G0/0 (.1/27) and G0/1 (.33/28), both enabled",
            "Verified every address against its usable range",
            "Found and corrected all four deliberate addressing mistakes",
            "Cross-subnet ping works both directions",
            "show ip route shows the planned connected subnets",
            "Saved the configuration",
        ],
    },
    # ================= LAB 4 =================
    {
        "id": "lab4", "n": 4, "title": "Network Troubleshooting",
        "objective": (
            "Rebuild Lab 2's working network, then hunt down <b>five realistic "
            "configuration faults</b> — an incorrect subnet mask, an incorrect "
            "default gateway, duplicate IP addresses, incorrect interface "
            "addressing, and an interface that was never enabled. Diagnose each one "
            "with ping and the course's verification commands, correct it, and "
            "re-verify end-to-end. Grounded in the course's own failure states: "
            "IP address conflicts " + ref(2, 37) + ", administratively down "
            "interfaces " + ref(6, 30) + ", gateway rules " + ref(6, 31) + ", and "
            "testing the interface assignment " + ref(2, 38) + "."),
        "assumptions": [
            "<b>Assumption</b> — the five faults are planted for this exercise; the "
            "course teaches the underlying concepts and the verification discipline "
            + ref(2, 38) + " " + ref(6, 30) + " but does not present a "
            "broken-configuration scenario in its slides.",
            "<b>Course basis</b> — the INTENDED addressing table below is the "
            "course's two-LAN scheme " + ref(6, 29) + " " + ref(6, 31) + ".",
            "<b>Assumption</b> — how you inspect PC settings in Packet Tracer "
            "(Desktop → IP Configuration / ipconfig) is PT workflow; the course "
            "requires correct end-device configuration " + ref(2, 33) + " without "
            "naming the tool.",
            "<b>Assumption</b> — fault values (mask 255.255.0.0, gateway .11.1, "
            "duplicate .11.10, G0/0 .254) are chosen teaching mistakes, not course "
            "output.",
        ],
        "devices": [
            "<b>1 × router (R1)</b> — both LAN interfaces " + ref(6, 29) + ".",
            "<b>2 × switches</b> (SW0, SW1) " + ref(5, 24) + ".",
            "<b>4 × PCs</b> (PC0, PC1 on LAN-A; PC2, PC3 on LAN-B) "
            + ref(1, 10) + " — PC3 doubles as a correctly-configured reference "
            "device for comparisons.",
            "<b>6 × copper straight-through cables</b> " + ref(4, 13) + ".",
        ],
        "topo_desc": (
            "Physically the Lab 2 topology plus two extra PCs — the diagram shows "
            "the <b>intended</b> (correct) addressing. The running configuration "
            "contains <b>five faults</b>: PC0's mask, PC1's gateway, a duplicate "
            "address between PC2 and PC3, R1's G0/0 address not matching the plan, "
            "and R1's G0/1 left disabled. Your job: use symptoms + verification "
            "output to locate each fault and bring the network to the table's "
            "state " + ref(1, 14) + "."),
        "topo": None,
        "topo_cap": "Lab 4 topology — intended addressing; five faults are hidden in "
                    "the running configuration.",
        "addr_note": (
            "<b>The reference plan</b> — compare every device's actual settings "
            "against this table (course scheme " + ref(6, 29) + "); anything "
            "different is a finding."),
        "addr_cols": ["Device", "Interface", "IPv4 address", "Subnet mask",
                      "Default gateway"],
        "addr_rows": [
            ["PC0", "FastEthernet0", "192.168.10.10", "255.255.255.0",
             "192.168.10.1"],
            ["PC1", "FastEthernet0", "192.168.10.11", "255.255.255.0",
             "192.168.10.1"],
            ["R1", "GigabitEthernet0/0", "192.168.10.1", "255.255.255.0", "—"],
            ["R1", "GigabitEthernet0/1", "192.168.11.1", "255.255.255.0", "—"],
            ["PC2", "FastEthernet0", "192.168.11.10", "255.255.255.0",
             "192.168.11.1"],
            ["PC3", "FastEthernet0", "192.168.11.11", "255.255.255.0",
             "192.168.11.1"],
        ],
        "steps": [
            ("Build the correct network first",
             "Assemble the topology from the table (Lab 2 build) and configure "
             "EVERYTHING as shown — then the tutor will break five settings on "
             "your copy, or you plant them yourself using the fault list in "
             "troubleshooting Q1–Q5: (1) PC0 mask 255.255.0.0, (2) PC1 gateway "
             "192.168.11.1, (3) PC3 set to 192.168.11.10, (4) R1 G0/0 set to "
             "192.168.10.254, (5) R1 G0/1 left without no shutdown."),
            ("Record baseline symptoms without fixing anything",
             "From EACH PC: ping its LAN neighbours, then its gateway (10.1 or "
             "11.1), then a host on the other network. Write down which tests fail "
             "— this symptom map is your evidence (course testing pattern "
             + ref(2, 38) + ")."),
            ("Gather router evidence",
             "On R1 run <code>show ip interface brief</code>. Compare the "
             "IP-Address/Status/Protocol columns with the plan — two lines will "
             "violate it " + ref(6, 30) + "."),
            ("Compare PC configurations",
             "Open each PC's IP settings and diff them against the plan "
             "side-by-side (PC3 is your clean reference). Look at mask, address "
             "and gateway fields " + ref(2, 33) + " — three of the five faults "
             "live here " + ref(2, 37) + "."),
            ("Fix each fault as you confirm it",
             "Mask → correct it; gateway → point at the PC's own LAN gateway "
             + ref(6, 31) + "; duplicate → give PC3 .11 per plan; G0/0 → "
             "<code>ip address 192.168.10.1 255.255.255.0</code>; G0/1 → "
             "<code>no shutdown</code> " + ref(6, 29) + "."),
            ("Re-verify everything",
             "Repeat the full ping matrix (local, gateway, cross-LAN, both "
             "directions), re-run <code>show ip interface brief</code> "
             "(both up up " + ref(6, 30) + "), confirm no two devices share an "
             "address, then <code>copy running-config startup-config</code>."),
        ],
        "cmds_note": (
            "The diagnostic toolkit — the same commands the course uses to verify "
            "configurations; PC-side checks are Packet Tracer Desktop tools "
            "(assumption)."),
        "cmds": [
            ("ping <target>", "PC command prompt / R1",
             "The symptom test: local vs gateway vs remote targets " + ref(6, 30) + "."),
            ("show ip interface brief", "R1 privileged EXEC",
             "Exposes wrong addresses, and down / administratively down interfaces "
             + ref(6, 30) + "."),
            ("show ip route", "R1 privileged EXEC",
             "Confirms which networks R1 actually believes are connected "
             + ref(6, 14) + "."),
            ("ip address <addr> <mask>", "R1(config-if)",
             "Corrects faulty interface addressing " + ref(6, 29) + "."),
            ("no shutdown", "R1(config-if)",
             "Brings up an interface that was never enabled " + ref(6, 29) + "."),
            ("copy running-config startup-config", "R1 privileged EXEC",
             "Save the repaired configuration " + ref(6, 30) + "."),
        ],
        "verify": [
            ("ping (all 3 targets × 4 PCs)", "every test replies — map: LAN "
             "neighbours, own gateway, far-network hosts"),
            ("show ip interface brief", "G0/0 192.168.10.1 up up · G0/1 "
             "192.168.11.1 up up " + ref(6, 30)),
            ("show ip route", "C 192.168.10.0/24 and C 192.168.11.0/24 "
             + ref(6, 14)),
            ("(PC settings review)", "all six devices match the plan exactly; no "
             "duplicate addresses remain " + ref(2, 37)),
        ],
        "expected": [
            "After all five fixes: cross-LAN pings give <code>!!!!! Success rate "
            "is 100 percent (5/5)</code> in <b>both</b> directions " + ref(6, 30) + ".",
            "<code>show ip interface brief</code> matches the plan — no "
            "'administratively down' rows " + ref(6, 30) + ".",
            "Each PC can ping its own gateway (192.168.10.1 or 192.168.11.1) "
            + ref(6, 31) + ".",
            "PC2 and PC3 now hold .10 and .11 — the conflict from the course's IP "
            "Address Conflicts topic " + ref(2, 37) + " is gone (no flapping "
            "replies).",
            "Your symptom map shows before/after for each fault — that table is the "
            "lab report (course: testing the interface assignment " + ref(2, 38) + ").",
        ],
        "mistakes": [
            "Fixing the first fault you find and declaring victory — symptoms "
            "overlap; re-run the ENTIRE ping matrix after every fix.",
            "Changing the plan to match the device (or vice versa) inconsistently — "
            "decide once: the plan table is the reference " + ref(1, 14) + ".",
            "Confusing <code>administratively down</code> (needs "
            "<code>no shutdown</code>) with a layer-1 problem (cable/port) "
            + ref(6, 30) + ".",
            "Pointing a PC's gateway at a router interface on a DIFFERENT network "
            + ref(6, 31) + " — the classic wrong-gateway fault.",
            "Fixing the duplicate on only one of the two PCs.",
            "Skipping the return direction after repairs (one-way ping ≠ working) "
            + ref(2, 38) + ".",
            "Forgetting to save the repaired configuration " + ref(6, 30) + ".",
        ],
        "tsq": [
            {"q": "<b>Fault 1 — mask.</b> PC0 pings PC1 (192.168.10.11) fine but "
                  "times out to 192.168.11.10 and to 192.168.11.1. Its mask reads "
                  "<code>255.255.0.0</code>. What happens inside PC0, and what is "
                  "the fix?",
             "a": "With /16 PC0 believes 192.168.11.0/16 is <b>local</b> — it ARPs "
                  "for 192.168.11.10 on LAN-A instead of sending to its gateway, so "
                  "remote pings die. Fix: mask <code>255.255.255.0</code> to match "
                  "the plan " + ref(2, 33) + ". (Gateway tests to 192.168.11.1 also "
                  "fail for this PC because that address isn't on-link.)"},
            {"q": "<b>Fault 2 — gateway.</b> PC1's local pings work, but every "
                  "cross-network ping from it fails; its gateway field says "
                  "<code>192.168.11.1</code> while PC1 is on 192.168.10.0/24. Why "
                  "does this break, and what is correct?",
             "a": "A gateway must be reachable on the host's OWN network first "
                  + ref(6, 31) + ". 192.168.11.1 lives on LAN-B, so PC1 can never "
                  "ARP it locally — no route out. Correct: <code>192.168.10.1</code> "
                  "(R1 G0/0 " + ref(6, 29) + ")."},
            {"q": "<b>Fault 3 — duplicate.</b> LAN-B pings are flaky: replies come "
                  "and go, and <code>ipconfig</code> shows PC2 = 192.168.11.10 and "
                  "PC3 = 192.168.11.10. What is happening and how do you resolve it?",
             "a": "Two devices answer the same address — an IP address conflict "
                  + ref(2, 37) + " (ARP ambiguity makes sessions flap). Fix per "
                  "the plan: PC2 keeps .10, PC3 becomes "
                  "<code>192.168.11.11</code> " + ref(6, 31) + "."},
            {"q": "<b>Fault 4 — interface addressing.</b> <code>show ip interface "
                  "brief</code> shows <code>GigabitEthernet0/0 192.168.10.254 … up "
                  "up</code> but the plan says 192.168.10.1. Everything on LAN-A is "
                  "configured with gateway .1. What breaks and what do you type?",
             "a": "The interface's address <b>is</b> LAN-A's gateway — with .254 on "
                  "the router and .1 configured on the PCs, no device answers ARP "
                  "for the gateway, so LAN-A can't leave its network "
                  + ref(6, 31) + ". Fix: <code>interface g0/0</code> → "
                  "<code>ip address 192.168.10.1 255.255.255.0</code> "
                  + ref(6, 29) + " (address must belong to the connected network "
                  + ref(9, 4) + ")."},
            {"q": "<b>Fault 5 — interface not enabled.</b> The same show output "
                  "reads <code>GigabitEthernet0/1 192.168.11.1 … administratively "
                  "down down</code>. What does that state mean and what single "
                  "command clears it?",
             "a": "The address is right but the interface was administratively shut "
                  "— never enabled. Fix: enter the interface and issue "
                  "<code>no shutdown</code> " + ref(6, 29) + "; expect "
                  "<code>%LINK-5-CHANGED … changed state to up</code> "
                  + ref(6, 29) + " (the state itself appears in the course's brief "
                  "output " + ref(6, 30) + ")."},
        ],
        "quiz_note": "Five questions on diagnosis and repair — instant marking with "
                     "the reasoning behind each fix.",
        "quiz": [
            {"q": "PC0 pings PC1 fine but times out to 192.168.11.10; its mask reads 255.255.0.0. What is the first fix?", "opts": ["Compare PC0's settings with the plan and correct the subnet "
                      "mask to 255.255.255.0",
                      "Replace the switch — it is dropping frames",
                      "Give PC0 a default gateway of 192.168.11.1",
                      "Re-address PC0 into 192.168.11.0/24"],
             "a": 0,
             "why": "Local pings work but remote fail with a /16 mask: PC0 treats "
                    "remote networks as local and never uses its gateway — mask "
                    "first, exactly as end-device configuration requires "
                    + ref(2, 33) + "."},
            {"q": "show ip interface brief shows GigabitEthernet0/1 … administratively down down. What is the cause, and what single command fixes it?", "opts": ["The interface was never enabled — run no shutdown",
                      "The cable is wrong — replace it with serial",
                      "The IP address is duplicated — remove it",
                      "Routing is disabled — add a default route"],
             "a": 0,
             "why": "'administratively down' = shutdown mode; the course's fix in "
                    "the transcript is <code>no shutdown</code> " + ref(6, 29) + " "
                    + ref(6, 30) + "."},
            {"q": "Two devices on LAN-B both use 192.168.11.10 — this creates an IP address conflict.", "opts": ["True", "False"], "a": 0,
             "why": "True — the course devotes a slide to IP Address Conflicts "
                    + ref(2, 37) + ": two hosts on one address make every exchange "
                    "ambiguous."},
            {"q": "PC1's gateway field says 192.168.11.1 while PC1 is on 192.168.10.0/24. Why does this break traffic leaving LAN-A?", "opts": ["Its gateway address is not on PC1's network, so it can never "
                      "be reached locally",
                      "PC1 and the gateway are on the same switch port",
                      "The gateway 192.168.11.1 is a broadcast address",
                      "Ping does not work between routers and PCs"],
             "a": 0,
             "why": "The gateway must be a local-network interface " + ref(6, 31) +
                    " — PC1 must use 192.168.10.1, not the other LAN's gateway."},
            {"q": "The plan says G0/0 = 192.168.10.1, but the brief shows 192.168.10.254 up up. What is the correct action?", "opts": ["Re-address G0/0 to 192.168.10.1 255.255.255.0 to match the "
                      "plan the PCs use",
                      "Re-address every PC to 192.168.10.254/24",
                      "Nothing — up up means it is correct",
                      "Shut G0/0 down to stop the mismatch"],
             "a": 0,
             "why": "The interface address is the gateway the plan promises "
                    + ref(6, 29) + " " + ref(6, 31) + "; devices stay consistent "
                    "with the documented plan " + ref(1, 14) + "."},
        ],
        "checklist": [
            "Built the 4-PC topology exactly per the plan (or planted the 5 faults)",
            "Recorded baseline symptoms: local / gateway / remote ping matrix",
            "Collected show ip interface brief output and diffed it to the plan",
            "Compared all four PCs' IP settings (PC3 as reference)",
            "Found & fixed Fault 1 — PC0 subnet mask",
            "Found & fixed Fault 2 — PC1 default gateway",
            "Found & fixed Fault 3 — duplicate address on LAN-B",
            "Found & fixed Fault 4 — R1 G0/0 interface address",
            "Found & fixed Fault 5 — G0/1 never enabled (no shutdown)",
            "Full ping matrix green in both directions",
            "Configuration saved after repairs",
        ],
    },
]


# --------------------------------------------------------------------------
# page body
# --------------------------------------------------------------------------
def render_pt_body():
    """Full <body> inner content for ptlab.html (shell provided by build.py)."""
    chips = "".join(
        f'<a class="chip" href="#{l["id"]}">Lab {l["n"]} · {l["title"]}</a>'
        for l in LABS)
    chips += '<a class="chip" href="#ios-practice">IOS command practice</a>'
    labs = "".join(_lab_html(l) for l in LABS)
    return f"""
<div class="wrap pt" id="pt-root">
  <h1 class="section-title" style="margin-top:30px">Packet Tracer Practical Preparation</h1>
  <p class="section-sub">Four guided configuration labs — build the skills first in the
  official Cisco Packet Tracer application, then perform the identical tasks on real
  equipment. Grounded in the course material, with every assumption labelled.</p>

  <div class="pt-alert"><span class="ic">⚠️</span><div><b>IMPORTANT — this website does
  NOT run Packet Tracer.</b> The pages here explain what to build, which commands to
  type and how to verify the result, but no simulation executes in your browser.
  Open the <b>official Cisco Packet Tracer application</b> on your computer (the free
  version from the Networking Academy / Skills for All) and perform every configuration
  there. Use this page as your lab sheet; use Packet Tracer as your lab bench.</div></div>

  <section class="lab-sec">
    <h2>How to use these labs</h2>
    <p class="lede">Read the lab → build it in Packet Tracer → verify with the given
    commands → mark the checklist → take the self-assessment quiz. Progress is saved
    in your browser.</p>
    <div class="chips">{chips}</div>
    <div class="pt-legend">
      <span class="pt-tag">Course basis</span> — taken from the course PDFs (clickable
      slide links)
      <span class="pt-tag as">Assumption</span> — the course is silent; a clearly
      labelled practice choice
      <span class="pt-tag pt">Packet Tracer</span> — PT application workflow
    </div>
    <ul>
      <li>Every grey <b>slide link</b> opens the exact course slide the step comes from.</li>
      <li><b>Assumption</b> callouts mark anything the course documents do not specify
      (GUI paths, device names, practice addresses) — nothing is invented silently.</li>
      <li>The checklist and quiz state are stored locally in your browser
      (nothing is uploaded, no accounts, no APIs).</li>
    </ul>

    <div class="panel" style="margin-top:16px">
      <div class="pt-ck-head">
        <b>Overall progress across all labs</b>
        <div class="pt-bar" id="pt-overall-bar"><i></i></div>
        <span id="pt-overall-count">0 / 0 tasks across all labs</span>
      </div>
      <p style="margin:6px 0 0;font-size:13.5px;color:var(--muted)">Checklists persist
      with localStorage (key <code>itn-pt-checks-v1</code>) — reload-safe on this
      device. Each lab has its own Reset button.</p>
    </div>

    <h3 style="margin-top:18px">Course map — where each lab is grounded</h3>
    <ul>
      <li><b>Lab 1</b> → addressing end devices (Ch 6 s.33), same-network vs gateway
      (Ch 6 s.31), UTP media (Ch 4), switch basics (Ch 5 s.24), topology diagrams
      (Ch 1 s.14).</li>
      <li><b>Lab 2</b> → the course's own router configuration transcript (Ch 6
      s.28–30), routing table (Ch 6 s.14), default gateways (Ch 6 s.31).</li>
      <li><b>Lab 3</b> → subnetting method, 2<sup>n</sup> − 2 and VLSM (Ch 9
      s.4–10), interface-address rules (Ch 9 s.4).</li>
      <li><b>Lab 4</b> → IP address conflicts (Ch 2 s.37), verification discipline
      (Ch 2 s.38), interface states (Ch 6 s.29–30), gateway rules (Ch 6 s.31).</li>
    </ul>
  </section>

  {labs}

  <section class="lab-sec" id="ios-practice">
    <h2>IOS command practice — configuration vs verification</h2>
    <p class="lede">Twenty short drills on the IOS commands this course actually
    uses: entering configuration modes, assigning IP addresses, enabling
    interfaces, saving the configuration, and verifying status. Every drill is
    tagged either <b>Configuration</b> (it changes the device) or
    <b>Verification</b> (it only reads or tests state), with an explanation and
    a slide link after you answer.</p>

    <div class="pt-alert"><span class="ic">⌨️</span><div><b>This practice area
    does not run IOS.</b> The commands and outputs below are transcribed from the
    course material (Ch 6 s.28–30 router configuration and verification, Ch 2
    s.25–34 device basics, Ch 16 s.28–29 hardening) — typing an answer here
    performs no device action whatsoever. Practise the same commands later in the
    <b>official Cisco Packet Tracer</b> application or on real equipment.</div></div>

    <div class="pt-tbl"><table class="cmp">
      <thead><tr><th>Command (course form)</th><th>Kind</th>
      <th>What it does</th></tr></thead>
      <tbody>
        <tr><td><code>configure terminal</code> (<code>conf t</code>)</td>
          <td><span class="ios-kind kind-config">Configuration</span></td>
          <td>Enter global configuration mode from <code>R1#</code></td></tr>
        <tr><td><code>hostname R1</code></td>
          <td><span class="ios-kind kind-config">Configuration</span></td>
          <td>Set the device name (prompt changes to <code>R1(config)#</code>)</td></tr>
        <tr><td><code>interface gigabitethernet 0/0</code></td>
          <td><span class="ios-kind kind-config">Configuration</span></td>
          <td>Enter interface configuration mode <code>(config-if)#</code></td></tr>
        <tr><td><code>ip address 192.168.10.1 255.255.255.0</code></td>
          <td><span class="ios-kind kind-config">Configuration</span></td>
          <td>Assign the IPv4 address and mask to the interface</td></tr>
        <tr><td><code>no shutdown</code></td>
          <td><span class="ios-kind kind-config">Configuration</span></td>
          <td>Administratively enable the interface</td></tr>
        <tr><td><code>copy running-config startup-config</code></td>
          <td><span class="ios-kind kind-config">Configuration</span></td>
          <td>Save the configuration so it survives a reload</td></tr>
        <tr><td><code>show ip interface brief</code></td>
          <td><span class="ios-kind kind-verify">Verification</span></td>
          <td>List IP addresses, Status and Protocol for every interface</td></tr>
        <tr><td><code>ping 209.165.200.226</code></td>
          <td><span class="ios-kind kind-verify">Verification</span></td>
          <td>Test reachability (<code>!!!!!</code> = 100% success)</td></tr>
      </tbody>
    </table></div>

    <div id="ios-root">
      <div class="panel">
        <p style="margin-top:0">Press start to draw a shuffled set of all twenty
        drills. You get the expected command, an explanation of why it is
        configuration or verification, and the course slide it comes from —
        then a chance to retry anything you missed.</p>
        <div class="pt-tools">
          <button type="button" class="pt-btn" id="ios-start">Start practice set →</button>
        </div>
        <p class="ex-note" id="ios-stats" style="margin-bottom:0"></p>
        <p class="ex-note" style="margin-bottom:0">Lifetime score counters are
        stored <b>only in this browser</b> (localStorage key
        <code>itn-ios-stats-v1</code>) — no accounts, no servers, nothing syncs
        between devices, clearing site data resets them; individual answers are
        not saved. If storage is unavailable the counters last only until you
        reload.</p>
      </div>

      <div class="panel" id="ios-stage" hidden>
        <div class="ios-top">
          <span class="ios-kind" id="ios-kind"></span>
          <span class="ios-progress" id="ios-progress"></span>
        </div>
        <div id="ios-ask"></div>
        <div class="ios-opts" id="ios-opts" hidden></div>
        <div class="ios-input-wrap" id="ios-input-wrap" hidden>
          <input type="text" id="ios-input" autocomplete="off" spellcheck="false"
                 aria-label="Type the IOS command">
        </div>
        <div class="pt-tools">
          <button type="button" class="pt-btn" id="ios-check">Check command</button>
        </div>
        <div class="ios-fb" id="ios-feedback"></div>
        <div class="pt-tools">
          <button type="button" class="pt-btn" id="ios-next" hidden>Next command →</button>
          <button type="button" class="pt-btn ghost" id="ios-retry" hidden>Retry missed commands</button>
          <button type="button" class="pt-btn ghost" id="ios-again" hidden>Start another set</button>
        </div>
      </div>
    </div>
  </section>

  <div class="pt-alert" style="margin-bottom:34px"><span class="ic">ℹ️</span><div>
  <b>Reminder</b> — these exercises prepare you for the official Packet Tracer
  application; the configurations themselves must be completed there (or on real
  equipment). The addressing tables are course-consistent practice plans, labelled
  where the course leaves choices open.</div></div>
</div>
"""

