#!/usr/bin/env python3
"""test-practice.py — structural tests for the practical-preparation upgrade.

Run:  python3 site-build/test-practice.py     (after python3 site-build/build.py)

Covers the built pages:
  * lab.html   — Mixed (revision) difficulty option, storage note,
                 single practice system (no duplicates).
  * ptlab.html — new IOS command practice section: disclaimer (no IOS
                 execution), config/verify tagging, embedded script,
                 storage note; plus an independent re-check of the four
                 PT scenario labs (objectives, devices, topologies,
                 addressing tables, verification, common mistakes,
                 expected results).
  * exam.html  — topic quick-quiz chips, recommendation container,
                 embedded startTopic/REC_RULES wiring, single setup.
  * link targets of the new recommendation/IOS references exist.
Exits non-zero on any failure.
"""
import os
import re
import sys

BUILD = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BUILD, "..", "itn-site")

pass_n = fail_n = 0
failures = []


def chk(name, ok, detail=""):
    global pass_n, fail_n
    if ok:
        pass_n += 1
    else:
        fail_n += 1
        failures.append((name, detail))
        print(f"  FAIL: {name} {detail}")


def read(fn):
    p = os.path.join(SITE, fn)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------- lab.html
print("=== lab.html ===")
lab = read("lab.html")
chk("lab.html exists", lab is not None)
if lab:
    m = re.search(r'<select id="qs-level">(.*?)</select>', lab, re.S)
    chk("qs-level select present", bool(m))
    opts = re.findall(r'<option value="([^"]+)"', m.group(1)) if m else []
    chk("levels easy/medium/hard kept", opts[:3] == ["easy", "medium", "hard"], opts)
    chk("mixed (revision) option added", "mixed" in opts, opts)
    chk("mixed option labelled as revision",
        bool(re.search(r'value="mixed">[^<]*revision', lab)))
    chk("lede mentions Mixed", "Pick <b>Mixed</b>" in lab)
    chk("lifetime stats storage key documented",
        "itn-lab-stats-v1" in lab)
    chk("storage limits explained (no sync / clearing)",
        "clearing site data resets them" in lab)
    chk("individual answers not stored note",
        "questions and answers are not" in lab)
    # single practice system — no duplicates
    chk("one Practice & quiz section", lab.count("Practice &amp; quiz") == 1,
        lab.count("Practice &amp; quiz"))
    chk("one qs-start button", lab.count('id="qs-start"') == 1)
    chk("one qs-level select", lab.count('id="qs-level"') == 1)
    # embedded engine carries the new API
    chk("lab.js embedded loadTotals", "loadTotals" in lab)
    chk("lab.js embedded mixed level", "cfg.level === 'mixed'" in lab)

# ---------------------------------------------------------------- ptlab.html
print("=== ptlab.html ===")
pt = read("ptlab.html")
chk("ptlab.html exists", pt is not None)
if pt:
    chk("ios-practice section", 'id="ios-practice"' in pt)
    chk("ios-root container", 'id="ios-root"' in pt)
    chk("no-execution disclaimer",
        "This practice area\n    does not run IOS" in pt or "does not run IOS" in pt)
    chk("names official app (>=2 page-wide)", pt.count("official Cisco Packet Tracer") >= 2,
        pt.count("official Cisco Packet Tracer"))
    chk("states answers perform no device action",
        "performs no device action" in pt)
    chk("course transcript basis cited",
        "Ch 6 s.28–30" in pt)
    chk("storage key documented", "itn-ios-stats-v1" in pt)
    chk("storage limits explained",
        "clearing site data resets them" in pt)
    chk("ios.js embedded (root.IOS)", "root.IOS = factory()" in pt)
    chk("ios.js embedded init guard", "ios-root" in pt and "DOMContentLoaded" in pt)
    # config vs verification distinction in static markup
    chk("config kind badges >=6",
        pt.count('<span class="ios-kind kind-config">Configuration</span>') >= 6,
        pt.count('<span class="ios-kind kind-config">Configuration</span>'))
    chk("verify kind badges >=2",
        pt.count('<span class="ios-kind kind-verify">Verification</span>') >= 2,
        pt.count('<span class="ios-kind kind-verify">Verification</span>'))
    chk("cheat-sheet table with core commands",
        "copy running-config startup-config" in pt and
        "show ip interface brief" in pt and "no shutdown" in pt)
    chk("start button present", 'id="ios-start"' in pt)
    chk("check/retry buttons present",
        'id="ios-check"' in pt and 'id="ios-retry"' in pt)
    chk("chip links to IOS practice",
        'href="#ios-practice">IOS command practice' in pt)
    # single IOS system
    chk("one ios-practice section", pt.count('id="ios-practice"') == 1)
    chk("one ios-start button", pt.count('id="ios-start"') == 1)
    # must not disturb the PT test invariants
    n_h3 = pt.count('<h3><span class="n">')
    chk("numbered h3 sections still 44", n_h3 == 44, n_h3)
    chk("ptq quiz forms still 4", pt.count('<form class="ptq" data-ptq=') == 4)
    chk("no data-ptq-grade leaked into ios section",
        pt.count("data-ptq-grade>") == 4, pt.count("data-ptq-grade>"))
    chk("no data-ck leaked", pt.count("data-ptreset=") == 4)

    # --- independent re-check of the four PT scenario labs (req. 3) ---
    for i in (1, 2, 3, 4):
        chk(f"lab{i} present", f'id="lab{i}"' in pt)
    for title in ("Objective", "Required devices", "Network topology description",
                  "IP addressing table", "Verification commands",
                  "Expected results", "Common mistakes"):
        n = pt.count(title)
        chk(f"scenario element x4: {title}", n >= 4, n)
    chk("troubleshooting scenario faults present",
        "administratively down" in pt and "duplicate" in pt and "192.168.11.1" in pt)
    chk("addressing/connecting-networks scenario present",
        "VLSM" in pt and "192.168.10.0/24" in pt)
    chk("does NOT run Packet Tracer banner kept",
        "NOT run Packet Tracer" in pt)
    n_svg = len(re.findall(r"<svg", pt))
    chk("topology SVGs >=4", n_svg >= 4, n_svg)

# ---------------------------------------------------------------- exam.html
print("=== exam.html ===")
ex = read("exam.html")
chk("exam.html exists", ex is not None)
if ex:
    chk("topic chips container", 'id="ex-topics"' in ex)
    n_chips = ex.count('class="ex-chip ex-topic"')
    chk("topic chips >=10", n_chips >= 10, n_chips)
    chk("subnetting topic chip", "data-topic=" in ex and "IP addressing &amp; subnetting" in ex)
    chk("troubleshooting topic chip", "Troubleshooting" in ex)
    chk("topic quiz heading + explanation",
        "Topic quick quizzes" in ex and "five-question quizzes" in ex)
    chk("mode-selected note", "the mode selected above applies" in ex)
    chk("recommendation container", 'id="ex-rec"' in ex)
    chk("one ex-topics / one ex-setup / one ex-quiz",
        ex.count('id="ex-topics"') == 1 and ex.count('id="ex-setup"') == 1 and
        ex.count('id="ex-quiz"') == 1)
    # embedded engine
    chk("exam.js embedded startTopic", "function startTopic" in ex)
    chk("exam.js embedded recFor rules", "REC_RULES" in ex and "recFor" in ex)
    chk("exam.js embedded data-topic wiring", "button[data-topic]" in ex)
    chk("history stores topic scope", "h.topic ? 'Topic · '" in ex)
    # practice-only framing preserved
    chk("real-exam disclaimer kept",
        "nothing here predicts, mirrors or" in ex)
    chk("storage note kept", "itn-exam-history-v1" in ex)

# ---------------------------------------------------------------- links
print("=== new link targets ===")
# recommendation + IOS practice references must point at real files/anchors
for fn in ("lab.html", "ptlab.html", "chapter1.html", "chapter2.html",
           "chapter3.html", "chapter4.html", "chapter5.html", "chapter6.html",
           "chapter7.html", "chapter10.html", "chapter16.html"):
    chk(f"{fn} exists", os.path.isfile(os.path.join(SITE, fn)))
ch6 = read("chapter6.html")
if ch6:
    for p in ("p28", "p29", "p30"):
        chk(f"chapter6.html anchor {p}", f'id="{p}"' in ch6)
pt2 = read("ptlab.html")
if pt2:
    chk("ptlab anchor lab4", 'id="lab4"' in pt2)

# ---------------------------------------------------------------- summary
print()
print(f"RESULTS: {pass_n} passed, {fail_n} failed, total {pass_n + fail_n}")
if fail_n:
    for name, detail in failures:
        print(f"  FAIL: {name} {detail}")
    sys.exit(1)
print("ALL TESTS PASSED")
