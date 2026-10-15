"""Exam practice bank builder (site-build/exam.py).

Builds the exam question bank embedded into exam.html at build time.

Sources (primary = the course PDFs, via the per-chapter revision kits):
  * revision/chNN.py questions  — multiple choice, true/false, short answer
    (converted with explicit graders so every answer is machine-verifiable);
    'explain' items are excluded (long-form, not auto-gradable).
  * revision/chNN.py definitions — auto-generated terminology questions
    (term ↔ definition), distractors drawn from the same chapter.
  * authored calculation + troubleshooting items — grounded in course slides,
    labelled 'supplementary' where the exact scenario is not in the course text.

Schema per item:
  {i: id, ty: type, tp: topic, c: [chapters], q: text,
   o: [options], a: correct option index        (choice types: mc/term/trouble/tf)
   gr: {acc:[..]} | {must:[..]} | {g:[[aliases]], n:k} | {num:k}   (short/calc)
   disp: text shown as the correct answer       (short/calc),
   e: explanation, s: 'course'|'supp', src: source note}
"""
import importlib.util
import os
import re

BUILD = os.path.dirname(os.path.abspath(__file__))
REV_DIR = os.path.join(BUILD, "revision")

TOPICS = {
    1: "Network fundamentals", 2: "Network devices", 3: "OSI & TCP/IP models",
    4: "Cabling & media", 5: "Switching & ARP", 6: "IPv4 & routing basics",
    7: "Transport layer", 9: "Subnetting", 10: "Application layer",
    16: "Network security",
}
CHAPTERS = list(TOPICS)

# ---------------------------------------------------------------------------
# short-answer graders for the revision-kit shorts, keyed (chapter, q-marker)
# 'g' = groups of aliases; n groups must match. Every answer is verifiable.
# ---------------------------------------------------------------------------
SHORT_SPEC = {
    (1, "four basic characteristics"): {
        "g": [["fault tolerance"], ["scalab"], ["quality of service", "qos"],
              ["security"]], "n": 4},
    (1, "client, a server, or both"): {"must": ["software"]},
    (2, "hostname guidelines"): {
        "g": [["start with a letter", "begins with a letter", "first letter",
               "letter first"], ["no spaces", "without spaces", "not contain spaces",
               "contain no spaces"], ["letters, digits", "letters and digits",
               "dashes", "dash", "hyphen"], ["64"], ["end with a letter", "letter or digit"]],
        "n": 4},
    (2, "where does it run from"): {
        "g": [["flash", "non-volatile", "nonvolatile"], ["ram", "volatile"]],
        "n": 2},
    (3, "before communication occurs"): {
        "g": [["sender"], ["receiver"], ["method"], ["language", "grammar"],
              ["speed", "timing"]], "n": 5},
    (3, "PDU names"): {
        "g": [["bits"], ["frames"], ["packets"], ["segments"], ["data"]],
        "n": 4},
    (4, "UTP cable tester"): {
        "g": [["wire map", "pin", "termination", "shorts"], ["length"],
              ["attenuation", "signal loss"], ["crosstalk"]], "n": 4},
    (4, "copper media"): {
        "g": [["unshielded", "utp"], ["shielded", "stp"], ["coax"]], "n": 3},
    (5, "ARP's two basic functions"): {
        "g": [["resolving", "resolve"], ["table", "mapping", "mappings"]], "n": 2},
    (5, "multicast MAC prefix"): {
        "g": [["01-00-5e", "01005e"], ["224.0.0.0"], ["239.255.255.255"]],
        "n": 3},
    (6, "three limitations of IPv4"): {
        "g": [["depletion", "exhaust"], ["routing-table", "routing table",
               "route table"], ["end-to-end", "nat", "port address"]],
        "n": 3},
    (6, "memory types hold"): {
        "g": [["ram"], ["nvram"], ["flash"]], "n": 3},
    (6, "two verification commands"): {
        "g": [["show ip interface brief", "show ip int brief", "ip interface brief"],
              ["ping"]], "n": 2},
    (7, "three purposes of TCP session"): {
        "g": [["present"], ["active service", "service accepting", "accepting requests"],
              ["intend", "intent", "inform"]], "n": 3},
    (7, "sequence numbers used for"): {
        "g": [["original order", "order", "reassemble"], ["confirm receipt",
               "confirm", "acknowledg", "ack"]], "n": 2},
    (9, "usable-host formula"): {
        "g": [["2^n", "2n", "two"], ["- 2", "-2", "minus 2", "subtract"],
              ["host bits", "remaining host"]], "n": 3},
    (9, "subnetting plan establish"): {
        "g": [["subnets required", "number of subnets"],
              ["host addresses required", "number of host", "host addresses"]],
        "n": 2},
    (9, "planning and documenting"): {
        "g": [["duplicat"], ["access"], ["monitor", "security and performance"]],
        "n": 3},
    (10, "SMTP and POP"): {
        "g": [["25"], ["110"], ["send", "transfer"], ["retriev", "receive"]],
        "n": 4},
    (10, "FTP require two connections"): {
        "g": [["command"], ["file transfer", "file"]], "n": 2},
    (16, "four types of threats"): {
        "g": [["information theft"], ["data loss"], ["identity theft"],
              ["disruption"], ["technological"], ["configuration"],
              ["security policy", "policy"]], "n": 6},
    (16, "three AAA functions"): {
        "g": [["authenticat"], ["authoriz"], ["account"], ["credit card"]],
        "n": 4},
    (16, "strong-password guidelines"): {
        "g": [["eight", "8", "ten", "10", "length"], ["uppercase", "lower",
               "complex", "symbol", "mix"], ["dictionary", "common", "repetit"],
               ["change", "often", "regular"], ["misspell", "smyth", "5mYth"],
               ["write", "desk", "monitor"]], "n": 4},
}

# ---------------------------------------------------------------------------
# authored calculation items (course-grounded: Ch 9 formula & VLSM slides,
# Ch 6 addressing, Ch 3/6 mask notation)
# ---------------------------------------------------------------------------
CALCS = [
    dict(i="calc-usable-27", c=[9], q="How many usable host addresses does a /27 "
         "subnet provide?", gr={"num": 30}, disp="30 (2^5 − 2)",
         e="n = 5 remaining host bits → 2^5 = 32, minus the subnetwork ID and "
           "broadcast = 30. Course formula: Ch 9 slide 6.",
         src="Ch 9 s.6 (2^n − 2)"),
    dict(i="calc-usable-30", c=[9], q="How many usable host addresses does a /30 "
         "subnet provide?", gr={"num": 2}, disp="2 (2^2 − 2)",
         e="n = 2 → 4 − 2 = 2 usable — exactly enough for a WAN link "
           "(course VLAN example uses /30 for WANs, Ch 9 slide 10).",
         src="Ch 9 s.6, s.10"),
    dict(i="calc-usable-28", c=[9], q="How many usable host addresses does a /28 "
         "subnet provide?", gr={"num": 14}, disp="14 (2^4 − 2)",
         e="n = 4 → 16 − 2 = 14 usable addresses.", src="Ch 9 s.6"),
    dict(i="calc-usable-29", c=[9], q="How many usable host addresses does a /29 "
         "subnet provide?", gr={"num": 6}, disp="6 (2^3 − 2)",
         e="n = 3 → 8 − 2 = 6 usable.", src="Ch 9 s.6"),
    dict(i="calc-total-26", c=[9], q="How many addresses (usable + reserved) are "
         "there in a /26 block?", gr={"num": 64}, disp="64 addresses (2^6)",
         e="n = 6 host bits → 2^6 = 64 total addresses, of which 62 are usable.",
         src="Ch 9 s.6"),
    dict(i="calc-mask-26", c=[6, 9], q="What dotted-decimal subnet mask equals the "
         "prefix /26?", gr={"acc": ["255.255.255.192"]}, disp="255.255.255.192",
         e="/26 leaves 6 host bits: 256 − 64 = 192 in the fourth octet "
           "(mask notation from the course's addressing slides).",
         src="Ch 6 addressing · Ch 9"),
    dict(i="calc-mask-30", c=[6, 9], q="What dotted-decimal subnet mask equals the "
         "prefix /30?", gr={"acc": ["255.255.255.252"]}, disp="255.255.255.252",
         e="/30 → last octet 256 − 4 = 252; 4 addresses, 2 usable.",
         src="Ch 9 s.10 (WAN /30)"),
    dict(i="calc-net-65-28", c=[9], q="What is the network address of "
         "192.168.10.65 with prefix /28?",
         gr={"acc": ["192.168.10.64"]}, disp="192.168.10.64",
         e="/28 blocks are 16 addresses wide: 65 falls in the block starting at "
           "64 (64–79).", src="Ch 9 s.6 (block maths)"),
    dict(i="calc-bcast-48-30", c=[9], q="What is the broadcast address of "
         "192.168.10.48/30?", gr={"acc": ["192.168.10.51"]},
         disp="192.168.10.51",
         e="A /30 block covers .48–.51: .48 network, .49–.50 usable, "
           ".51 broadcast.", src="Ch 9 s.6 (−2 rule)"),
    dict(i="calc-first-32-28", c=[9], q="What is the first usable (host) address "
         "of 192.168.10.32/28?", gr={"acc": ["192.168.10.33"]},
         disp="192.168.10.33",
         e="The /28 network address is .32 (reserved) → first usable is .33.",
         src="Ch 9 s.6"),
    dict(i="calc-borrow-26", c=[9], q="A /24 network is subnetted to /26. How many "
         "bits are borrowed from the host portion?", gr={"num": 2}, disp="2 bits",
         e="26 − 24 = 2 borrowed bits (VLSM slides: mask varies with how "
           "many bits have been borrowed).", src="Ch 9 s.9 (borrowed bits)"),
    dict(i="calc-prefix-12hosts", c=[9], q="Using the course's method, what is the "
         "smallest prefix that provides at least 12 usable host addresses?",
         gr={"acc": ["/28", "28", "255.255.255.240"]}, disp="/28 (14 usable)",
         e="2^4 − 2 = 14 ≥ 12 → /28; /29 would give only 6.",
         src="Ch 9 s.6 + s.7 (design for requirements)"),
    dict(i="calc-subnetof-34-28", c=[9], q="192.168.10.34/28 belongs to which "
         "network address?", gr={"acc": ["192.168.10.32"]},
         disp="192.168.10.32",
         e="/28 blocks: .32–.47 — so .34 sits in the 192.168.10.32 network.",
         src="Ch 9 s.6 (range checks)"),
]

# ---------------------------------------------------------------------------
# authored troubleshooting scenarios
# ---------------------------------------------------------------------------
TROUBLES = [
    dict(i="tr-mask-local", c=[6], q="PC0 can ping every host on its own LAN but "
         "nothing on other networks. Its subnet mask reads 255.255.0.0 while the "
         "plan says 255.255.255.0. What best explains the failure?",
         o=["The /16 mask makes remote networks look local, so the PC never uses "
            "its default gateway",
            "The switch is dropping frames because the cables are crossover",
            "The default gateway address is a broadcast address, so no host may "
            "hold it",
            "The router has no ARP entry for the destination host"],
         a=0, e="With mask 255.255.0.0 the PC treats 192.168.11.0/16 as on-link and "
              "ARPs directly instead of sending via the gateway — local traffic "
              "still works, remote traffic dies. Fix the mask to match the plan.",
         s="supp", src="Supplementary scenario · course rules Ch 6 s.31, Ch 9"),
    dict(i="tr-admin-down", c=[6], q="R1's show ip interface brief shows "
         "GigabitEthernet0/1 … administratively down down. What is the cause "
         "and the fix?",
         o=["The interface was never enabled — enter it and run no shutdown",
            "The copper cable is faulty — replace the straight-through cable",
            "The address duplicates another interface — re-address it",
            "A routing protocol is missing — configure a default route"],
         a=0, e="'Administratively down' means the interface is administratively "
              "shut down; no shutdown brings it up (the course transcript shows "
              "exactly this, Ch 6 slides 29–30).",
         s="course", src="Ch 6 s.29–30"),
    dict(i="tr-duplicate", c=[2], q="Two hosts on the same LAN are both configured "
         "with 192.168.11.10. What problem does this create?",
         o=["An IP address conflict — communication becomes unreliable until one "
            "host is re-addressed",
            "Nothing — duplicate addresses are normal on switched networks",
            "A broadcast storm that immediately fills the switch's MAC table",
            "The switch blocks both ports until the addresses differ by a full "
            "subnet"],
         a=0, e="Two interfaces answering the same address make every exchange "
              "ambiguous (ARP confusion) — the course covers IP address "
              "conflicts, Ch 2 slide 37.",
         s="course", src="Ch 2 s.37 (IP Address Conflicts)"),
    dict(i="tr-wrong-gw-net", c=[6], q="A host on 192.168.11.0/24 has its default "
         "gateway set to 192.168.10.1. What happens when it tries to reach a "
         "remote network?",
         o=["It fails — the gateway must be reachable on the host's own network "
            "before it can forward anywhere",
            "It works — any router interface can act as a default gateway",
            "It works only if the host's mask is changed to 255.255.0.0",
            "The switch forwards the frames to 192.168.10.1 automatically"],
         a=0, e="A gateway is used via layer-2 delivery on the local network "
              "first — 192.168.10.1 is not on 192.168.11.0/24, so it can never "
              "be reached (course: default gateway on a host, Ch 6 slide 31).",
         s="course", src="Ch 6 s.31"),
    dict(i="tr-plan-mismatch", c=[6, 9], q="The plan says R1's G0/0 = "
         "192.168.10.1, but the router shows 192.168.10.254 (up up) while every "
         "PC on LAN-A uses gateway 192.168.10.1. What must you do?",
         o=["Re-address G0/0 to 192.168.10.1 so it matches the plan the PCs use",
            "Re-address every PC to 192.168.10.254 to match the router",
            "Nothing — .254 answers gateway pings because it is in the subnet",
            "Shut G0/0 down until the addressing team approves a change"],
         a=0, e="The interface address is the gateway the PCs were promised — "
              "with .254 on the router, ARP for .1 gets no answer and LAN-A "
              "cannot leave its network. One side must change; the documented "
              "plan wins (Ch 6 s.29/31, Ch 9 s.4).",
         s="supp", src="Supplementary scenario · course rules Ch 6 s.29, s.31"),
    dict(i="tr-dns-name", c=[10], q="A user can reach a server by IP address "
         "(172.15.10.5) but typing its name fails. Which service is implicated?",
         o=["DNS — resolving names to numeric addresses",
            "DHCP — assigning IP addresses from a pool",
            "ARP — mapping IPv4 addresses to MAC addresses",
            "FTP — transferring files between client and server"],
         a=0, e="Name → address is exactly DNS's job (Ch 10 slide 18); IP "
              "connectivity proves the path itself works.",
         s="course", src="Ch 10 s.18 · address example s.12"),
    dict(i="tr-no-gw", c=[6], q="A PC has a correct IP address and subnet mask but "
         "no default gateway configured. What is the result?",
         o=["Same-network communication works; traffic to other networks fails",
            "All communication fails immediately",
            "All communication works — gateways are optional everywhere",
            "Only inbound connections work; outbound is always blocked"],
         a=0, e="On-link traffic needs only switch forwarding; anything beyond the "
              "local network needs a gateway (course: 'Default Gateway not "
              "needed' vs 'needed', Ch 6 slide 31).",
         s="course", src="Ch 6 s.31"),
    dict(i="tr-link-first", c=[5], q="A PC cannot reach its gateway; its settings "
         "match the plan, but the switch port toward the router shows no link "
         "indicator. What is the best first action?",
         o=["Check the physical layer first — link indicators, cabling and switch "
            "port",
            "Change the PC's subnet mask to /16",
            "Add a static DNS entry for the gateway",
            "Increase the ping timeout to 10 seconds"],
         a=0, e="No link light = no layer-1 connection, so every higher-layer "
              "check is pointless — verify cables/ports (copper media, Ch 4; "
              "switch ports connect devices, Ch 5 s.24) before re-addressing.",
         s="supp", src="Supplementary scenario · course rules Ch 4, Ch 5 s.24"),
    dict(i="tr-voip-udp", c=[7], q="A VoIP application sends small audio packets. "
         "Occasional loss is acceptable, but delay is not. Which transport choice "
         "matches the course's guidance?",
         o=["UDP — low overhead, no retransmission delay",
            "TCP — guaranteed ordered delivery of every packet",
            "ICMP — used only for echo request/reply messages",
            "ARP — resolves the destination's MAC address"],
         a=0, e="The chapter places DNS, VoIP and similar apps on UDP precisely "
              "because they tolerate small loss and cannot tolerate delay "
              "(reliability trade-off, Ch 7 slides 8–13).",
         s="course", src="Ch 7 s.8–13"),
    dict(i="tr-botnet", c=[16], q="An attacker floods a service from many infected "
         "hosts coordinated by a command-and-control program. What is this called?",
         o=["DDoS — a denial-of-service attack from multiple coordinated sources",
            "A reconnaissance attack that maps systems and services",
            "Privilege escalation through an authentication weakness",
            "A man-in-the-middle interception of traffic"],
         a=0, e="Zombies form a botnet directed by CnC to launch a DDoS — the "
              "course's definition (Ch 16 slide 14).",
         s="course", src="Ch 16 s.14"),
]


def _load_revision():
    data = {}
    if not os.path.isdir(REV_DIR):
        return data
    for fn in sorted(os.listdir(REV_DIR)):
        m = re.fullmatch(r"ch(\d{2})\.py", fn)
        if not m:
            continue
        path = os.path.join(REV_DIR, fn)
        spec = importlib.util.spec_from_file_location("exrev" + m.group(1), path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        data[int(m.group(1))] = mod.DATA
    return data


def _strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&lt;", "<") \
        .replace("&gt;", ">").replace("&nbsp;", " ").strip()


def _revision_items(rev):
    items = []
    for n in sorted(rev):
        data = rev[n]
        topic = TOPICS[n]
        mc_i = tf_i = sh_i = 0
        for q in data["questions"]:
            ty = q["type"]
            if ty == "explain":
                continue                                   # not auto-gradable
            base = dict(tp=topic, c=[n], s="course",
                        src=f"Ch {n} · course material (revision set)")
            if ty == "mc":
                m = re.match(r"^([A-H])\s*[—–-]\s*", q["a"])
                assert m, f"ch{n} mc answer unparsed: {q['a'][:60]}"
                idx = ord(m.group(1)) - 65
                assert 0 <= idx < len(q["opts"]), f"ch{n} mc letter out of range"
                # sanity: the letter's option must actually match the answer text
                items.append(dict(base, i=f"rev{n}-mc{mc_i}", ty="mc", q=q["q"],
                                  o=list(q["opts"]), a=idx, e=q["why"]))
                mc_i += 1
            elif ty == "tf":
                assert q["a"] in ("True", "False"), q["a"]
                items.append(dict(base, i=f"rev{n}-tf{tf_i}", ty="tf", q=q["q"],
                                  o=["True", "False"],
                                  a=0 if q["a"] == "True" else 1, e=q["why"]))
                tf_i += 1
            elif ty == "short":
                spec = None
                for (cn, marker), sp in SHORT_SPEC.items():
                    if cn == n and marker in q["q"]:
                        spec = sp
                        break
                assert spec, f"no grader for ch{n} short: {q['q'][:60]}"
                items.append(dict(base, i=f"rev{n}-sh{sh_i}", ty="short", q=q["q"],
                                  gr=spec, disp=_strip_tags(q["a"]), e=q["why"]))
                sh_i += 1
    return items


def _term_items(rev, per_chapter=5):
    """Terminology questions from definitions — deterministic spread sample."""
    items = []
    for n in sorted(rev):
        defs = [d for d in rev[n].get("definitions", [])
                if d.get("t") and d.get("d")]
        if not defs:
            continue
        picks = []
        if len(defs) <= per_chapter:
            picks = list(range(len(defs)))
        else:
            for k in range(per_chapter):
                picks.append(int(round(k * (len(defs) - 1) / (per_chapter - 1))))
            picks = sorted(set(picks))
        terms = [d["t"] for d in defs]
        topic = TOPICS[n]
        for j, di in enumerate(picks):
            d = defs[di]
            # distractors: other terms from the same chapter
            others = [t for t in terms if t != d["t"]]
            wrong = []
            for k in range(4):
                wrong.append(others[(di + 1 + k * 2) % len(others)])
            # de-dup distractors
            seen, opts = set(), []
            for w in wrong + others:
                if w not in seen and w != d["t"]:
                    seen.add(w)
                    opts.append(w)
                if len(opts) == 4:
                    break
            assert len(opts) == 4, (n, d["t"])
            clean_def = _strip_tags(d["d"])
            q_text = f"Which networking term is defined as: “{clean_def}”?"
            e = f"<b>{d['t']}</b>" + (f" = {d['abbr']}." if d.get("abbr") else ".") \
                + f" {clean_def}"
            src = (f"Ch {n} slide {d['r']}" if d.get("r") else f"Ch {n} definitions")
            items.append(dict(i=f"term{n}-{j}", ty="term", tp=topic, c=[n],
                              q=q_text, o=[d["t"]] + opts, a=0, e=e,
                              s="course", src=src))
    return items


def build_bank():
    rev = _load_revision()
    assert rev, "revision kits not found"
    bank = _revision_items(rev) + _term_items(rev)
    for c in CALCS:
        bank.append(dict(i=c["i"], ty="calc", tp="IP addressing & subnetting",
                         c=list(c["c"]), q=c["q"], gr=c["gr"], disp=c["disp"],
                         e=c["e"], s="course", src=c["src"]))
    for t in TROUBLES:
        bank.append(dict(i=t["i"], ty="trouble", tp="Troubleshooting",
                         c=list(t["c"]), q=t["q"], o=list(t["o"]), a=t["a"],
                         e=t["e"], s=t["s"], src=t["src"]))

    # ---- validation: unambiguous, verifiable, unique ----
    ids = [b["i"] for b in bank]
    assert len(ids) == len(set(ids)), "duplicate ids"
    for b in bank:
        assert b["ty"] in ("mc", "tf", "short", "term", "calc", "trouble"), b["i"]
        assert b["q"] and b["e"], b["i"]
        assert b["c"], b["i"]
        if b["ty"] in ("mc", "term", "trouble"):
            assert len(b["o"]) >= 3, b["i"]
            assert 0 <= b["a"] < len(b["o"]), b["i"]
        if b["ty"] == "tf":
            assert b["o"] == ["True", "False"] and b["a"] in (0, 1), b["i"]
        if b["ty"] in ("short", "calc"):
            assert any(k in b["gr"] for k in ("acc", "must", "g", "num")), b["i"]
            assert b.get("disp"), b["i"]
        assert b["s"] in ("course", "supp"), b["i"]
    # per-chapter pools must support a 10-question session
    for n in CHAPTERS:
        pool = [b for b in bank if n in b["c"]]
        assert len(pool) >= 10, f"chapter {n} pool too small: {len(pool)}"
    # no duplicate question texts
    texts = [_norm_q(b["q"]) for b in bank]
    assert len(texts) == len(set(texts)), "duplicate question text"
    return bank


def _norm_q(s):
    return re.sub(r"\s+", " ", s.strip().lower())[:80]


def render_exam_body():
    """Static body content for exam.html (interactive parts built by exam.js)."""
    ch_boxes = []
    for n in CHAPTERS:
        title = TOPICS[n]
        ch_boxes.append(
            f'<label class="ex-chip"><input type="checkbox" data-ch="{n}" checked> '
            f'<span>Ch {n} <small>{title}</small></span></label>')
    # topic quick-quiz chips: one per topic tag present in the bank
    bank = build_bank()
    tp_counts = {}
    for b in bank:
        tp_counts[b["tp"]] = tp_counts.get(b["tp"], 0) + 1

    def _esc(s):
        return (s.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))

    topic_chips = "".join(
        f'<button type="button" class="ex-chip ex-topic" data-topic="{_esc(tp)}">'
        f'{_esc(tp)} <small>{n} questions</small></button>'
        for tp, n in sorted(tp_counts.items(), key=lambda kv: (-kv[1], kv[0])))
    return f"""
<div class="wrap" id="ex-root">
  <h1 class="section-title" style="margin-top:30px">Exam Practice Mode</h1>
  <p class="section-sub">Independent, self-checked practice sessions built only from
  this site's course material (plus clearly labelled supplementary items). One question
  at a time, optional timer, scoring, weak-topic analysis and a retry pass — everything
  runs locally in your browser.</p>

  <div class="pt-alert"><span class="ic">📘</span><div><b>Practice only.</b> These are
  study drills written from the course PDFs — <b>nothing here predicts, mirrors or
  claims to represent the actual Cisco examination</b> (question wording, mix and
  difficulty of a real exam are unknown and unstated). Each item shows its source:
  <b>Course</b> (grounded in a specific chapter) or <b>Supplementary</b> (general
  networking practice built on course concepts).</div></div>

  <div id="ex-resume" class="pt-alert" hidden><span class="ic">⟳</span><div>
    <b>A previous practice session was found.</b> <span id="ex-resume-text"></span>
    <div class="pt-tools">
      <button type="button" class="pt-btn" id="ex-resume-yes">Resume session</button>
      <button type="button" class="pt-btn ghost" id="ex-resume-no">Discard &amp; start fresh</button>
    </div>
    <p style="margin:.6em 0 0;font-size:13.5px">Nothing is restored silently: if the
    saved session is incomplete or damaged it is discarded with a notice, never
    partially resumed.</p>
  </div></div>

  <section id="ex-setup">
    <div class="ex-card">
      <h2>1 · Choose your chapters</h2>
      <div class="ex-chips" id="ex-chips">
        <label class="ex-chip ex-all"><input type="checkbox" id="ex-all" checked>
          <span>All chapters</span></label>
        {''.join(ch_boxes)}
      </div>
      <h2>2 · Session length</h2>
      <div class="ex-opts" id="ex-lens">
        <button type="button" class="ex-opt" data-len="10">10 questions</button>
        <button type="button" class="ex-opt" data-len="20">20 questions</button>
        <button type="button" class="ex-opt" data-len="30">30 questions</button>
      </div>
      <p class="ex-note" id="ex-pool-note">—</p>
      <h2>3 · Mode</h2>
      <div class="ex-opts" id="ex-modes">
        <button type="button" class="ex-opt is-on" data-mode="untimed">
          Untimed <small>practice &amp; review</small></button>
        <button type="button" class="ex-opt" data-mode="30">
          Timed <small>30 s per question</small></button>
        <button type="button" class="ex-opt" data-mode="60">
          Timed <small>60 s per question</small></button>
      </div>
      <p class="ex-note">Untimed sessions double as review mode — no countdown runs,
      and answers appear only after you submit each question. In timed mode the
      countdown keeps running even if you reload or leave the tab: the deadline is
      stored as an absolute time.</p>
      <div class="pt-tools" style="margin-top:14px">
        <button type="button" class="pt-btn" id="ex-start">Start practice session →</button>
        <span class="ex-note" id="ex-start-note"></span>
      </div>
    </div>

    <div class="ex-card">
      <h2>Topic quick quizzes</h2>
      <p class="ex-note" style="margin-top:0">Short five-question quizzes on a
      single topic — a fast alternative to a full chapter session. Each quiz
      starts immediately (the mode selected above applies), and the usual review,
      source links, weak-topic analysis and retry buttons work exactly the same.
      Questions are always drawn only from this site's course-based material.</p>
      <div class="ex-chips" id="ex-topics">{topic_chips}</div>
    </div>

    <div class="ex-card">
      <h2>Your results history</h2>
      <p class="ex-note" id="ex-hist-note">No attempts yet.</p>
      <div class="pt-tbl" id="ex-hist-wrap" hidden>
        <table class="cmp"><thead><tr><th>Date</th><th>Scope</th><th>Mode</th>
        <th>Score</th><th>Weak topics</th></tr></thead>
        <tbody id="ex-hist-body"></tbody></table>
      </div>
      <p class="ex-note">Stored only in this browser (localStorage key
      <code>itn-exam-history-v1</code>) — no accounts, no servers. Results do not sync
      between devices or browsers, and clearing site data removes them; the current
      architecture has no backend, so this local-storage approach is the reliable
      option available.</p>
    </div>
  </section>

  <section id="ex-quiz" hidden>
    <div class="ex-topbar">
      <span class="ex-progress" id="ex-progress">Q 1 / 1</span>
      <span class="ex-tag" id="ex-topic"></span>
      <span class="ex-tag" id="ex-type"></span>
      <span class="ex-tag ex-src" id="ex-src"></span>
      <span class="ex-timer" id="ex-timer">Untimed</span>
    </div>
    <div class="ex-bar"><i id="ex-bar"></i></div>
    <div class="ex-card">
      <div id="ex-q" class="ex-q"></div>
      <div id="ex-opts" class="ex-opts"></div>
      <div id="ex-short" class="ex-short" hidden>
        <label for="ex-input" class="ex-note">Your answer:</label>
        <input type="text" id="ex-input" autocomplete="off" spellcheck="false"
               placeholder="Type your answer…">
      </div>
      <div class="pt-tools">
        <button type="button" class="pt-btn" id="ex-submit">Submit answer</button>
      </div>
      <div id="ex-feedback" class="ex-fb" hidden>
        <p class="ex-verdict" id="ex-verdict"></p>
        <p class="ex-correct" id="ex-correct"></p>
        <p class="ex-why" id="ex-why"></p>
        <div class="pt-tools">
          <button type="button" class="pt-btn" id="ex-next">Next question →</button>
        </div>
      </div>
    </div>
    <p class="ex-note" id="ex-timenote" hidden>⏱ Time is up — the session was scored
    with the answers you had given.</p>
  </section>

  <section id="ex-results" hidden>
    <div class="ex-card ex-scorecard">
      <div class="ex-score" id="ex-score">0 / 0</div>
      <div class="ex-pct" id="ex-pct">0%</div>
      <p class="ex-note" id="ex-scorenote"></p>
      <div id="ex-weak-wrap" hidden>
        <h2>Weak topics from this session</h2>
        <div class="ex-chips" id="ex-weak"></div>
        <div id="ex-rec" class="ex-rec" hidden></div>
        <p class="ex-note">Topics you missed most, ranked — revise those chapters
        first, then run a focused session on them.</p>
      </div>
      <div class="pt-tools">
        <button type="button" class="pt-btn" id="ex-retry" hidden>Retry incorrect
          questions</button>
        <button type="button" class="pt-btn ghost" id="ex-again">New session</button>
      </div>
    </div>
    <div class="ex-card">
      <h2>Review — your answers vs correct answers</h2>
      <div id="ex-review"></div>
    </div>
  </section>
</div>
"""
