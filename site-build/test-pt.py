#!/usr/bin/env python3
"""Structural tests for the Packet Tracer preparation page (ptlab.html).

Run:  python3 site-build/test-pt.py
Verifies:
  * the page exists with all 4 labs x 11 required sections
  * checklists (inputs, progress bars, reset) and quiz wiring (20 questions)
  * inline topology SVGs, addressing/command tables, assumption labels
  * the honest 'website does not run Packet Tracer' messaging
  * every cross-page course link (chapterN.html#pM) resolves
  * 'PT Prep' nav link on every page of the site; home card present
Exits non-zero on any failure.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "itn-site")

CHAPTERS = [1, 2, 3, 4, 5, 6, 7, 9, 10, 16]
ALL_PAGES = (["index.html", "lab.html", "ptlab.html"]
             + [f"chapter{n}.html" for n in CHAPTERS])

SEC_TITLES = ["Objective", "Required devices", "Network topology description",
              "IP addressing table", "Step-by-step configuration instructions",
              "Relevant Cisco IOS commands", "Verification commands",
              "Expected results", "Common mistakes",
              "Troubleshooting questions", "Self-assessment quiz"]

pass_n = fail_n = 0
failures = []


def chk(name, ok, detail=""):
    global pass_n, fail_n
    if ok:
        pass_n += 1
    else:
        fail_n += 1
        failures.append(name + (" — " + str(detail) if detail else ""))


# ---------------- ptlab.html ----------------
path = os.path.join(SITE, "ptlab.html")
chk("ptlab.html exists", os.path.isfile(path))
html = open(path, encoding="utf-8").read() if os.path.isfile(path) else ""

if html:
    chk("pt-root present", 'id="pt-root"' in html)
    chk("page title", "Packet Tracer Practical Preparation" in html)

    # honest PT messaging (twice: top + closing)
    chk("'does NOT run Packet Tracer' banner",
        "does\n  NOT run Packet Tracer" in html or "NOT run Packet Tracer" in html)
    chk("official app named", html.count("official Cisco Packet Tracer") >= 2)
    chk("pt-alert blocks >= 2", html.count('class="pt-alert"') >= 2)

    # 4 labs
    for i in (1, 2, 3, 4):
        chk(f"lab{i} section", f'id="lab{i}"' in html)
    chk("LAB badges 1-4",
        all(f"<span class=\"pt-n\">LAB {i}</span>" in html for i in (1, 2, 3, 4)))

    # 11 numbered sections per lab = 44
    n_sec = html.count('<h3><span class="n">')
    chk(f"11 numbered sections x4 (got {n_sec})", n_sec == 44, n_sec)
    for t in SEC_TITLES:
        chk(f"section heading x4: {t}", html.count(t) >= 4, html.count(t))

    # checklist
    n_ck = html.count('type="checkbox" data-ck=')
    chk(f"checklist inputs >= 35 (got {n_ck})", n_ck >= 35, n_ck)
    chk("4 reset buttons", len(re.findall(r'data-ptreset="lab\d+"', html)) == 4)
    chk("progress bars >= 9 (4 header + 4 checklist + overall)",
        html.count('data-ptbar=') >= 8 and 'id="pt-overall-bar"' in html)
    chk("overall count element", 'id="pt-overall-count"' in html)
    chk("storage key embedded", "itn-pt-checks-v1" in html)
    chk("PT script embedded (gradeQuiz)", "gradeQuiz" in html)

    # quiz
    chk("4 quiz forms", len(re.findall(r'<form class="ptq" data-ptq=', html)) == 4)
    n_q = html.count('class="ptq-item"')
    chk(f"20 quiz questions (got {n_q})", n_q == 20, n_q)
    n_correct = len(re.findall(r'value="\d+" data-correct=', html))
    chk(f"one correct marker per question (got {n_correct})", n_correct == 20, n_correct)
    chk("4 Check-answers buttons", html.count("data-ptq-grade>") == 4)
    chk("20 explanations", html.count('class="ptq-why"') == 20)
    chk("quiz score elements", html.count('class="ptq-score"') == 4)

    # diagrams + tables
    n_svg = html.count("<svg")
    chk(f"topology SVGs >= 4 (got {n_svg})", n_svg >= 4, n_svg)
    n_tbl = html.count('class="cmp"')
    chk(f"addressing/command tables >= 8 (got {n_tbl})", n_tbl >= 8, n_tbl)

    # course grounding + assumptions
    n_ref = html.count('class="rev-link" href="chapter')
    chk(f"course slide links >= 40 (got {n_ref})", n_ref >= 40, n_ref)
    n_as = html.count('class="pt-assume"')
    chk(f"assumption callouts >= 4 (got {n_as})", n_as >= 4, n_as)
    chk("assumption legend tag", 'class="pt-tag as"' in html)
    chk("course-basis legend tag", 'class="pt-tag"' in html)

    # key course-grounded commands present verbatim
    for c in ["no shutdown", "show ip interface brief",
              "Success rate is 100 percent",
              "copy running-config startup-config",
              "configure terminal", "hostname R1",
              "2<sup>n</sup> − 2", "%LINK-5-CHANGED"]:
        chk(f"command/phrase present: {c[:40]}", c in html)

    # lab4 five faults mentioned
    for f in ["255.255.0.0", "duplicate", "administratively down", "192.168.10.254",
              "192.168.11.1"]:
        chk(f"lab4 fault evidence: {f}", f in html)

    # cross-page course links resolve
    links = set(re.findall(r'href="(chapter\d+\.html)#(p\d+)"', html))
    missing = []
    cache = {}
    for fn, anchor in links:
        if fn not in cache:
            p = os.path.join(SITE, fn)
            cache[fn] = open(p, encoding="utf-8").read() if os.path.isfile(p) else ""
        if f'id="{anchor}"' not in cache[fn]:
            missing.append(f"{fn}#{anchor}")
    chk(f"all {len(links)} cross-page course links resolve", not missing, missing[:8])

    # search/ask wiring intact on ptlab
    chk("ask box wiring", "window.__ITN__" in html and "ITNAsk" in html
        and "data-open-ask" in html)

# ---------------- site-wide nav + home ----------------
for fn in ALL_PAGES:
    p = os.path.join(SITE, fn)
    chk(f"{fn} exists", os.path.isfile(p))
    if not os.path.isfile(p):
        continue
    h = open(p, encoding="utf-8").read()
    chk(f"{fn} nav has PT Prep", 'href="ptlab.html"' in h)
    chk(f"{fn} nav keeps IPv4 Lab", 'href="lab.html"' in h)
    chk(f"{fn} nav keeps Chapters dropdown", 'class="navdrop' in h)
    chk(f"{fn} nav keeps Ask", "data-open-ask" in h)

pt = open(os.path.join(SITE, "ptlab.html"), encoding="utf-8").read() \
    if os.path.isfile(os.path.join(SITE, "ptlab.html")) else ""
chk("ptlab marks itself current in nav", 'href="ptlab.html" aria-current="page"' in pt)
idx = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
chk("home card links to PT prep", 'href="ptlab.html">Open the PT Prep labs' in idx)

# corpus untouched (search regression prerequisite)
corpus = json.load(open(os.path.join(SITE, "corpus.json"), encoding="utf-8"))
chk(f"corpus still 425 passages (got {len(corpus)})", len(corpus) == 425, len(corpus))

# original pages still present
for fn in ("lab.html", "index.html"):
    chk(f"{fn} intact", os.path.getsize(os.path.join(SITE, fn)) > 10000)

print("=== Packet Tracer prep structural tests ===")
print(f"RESULTS: {pass_n} passed, {fail_n} failed, total {pass_n + fail_n}")
if failures:
    print("FAILURES:")
    for f in failures:
        print("  ✗ " + f)
    sys.exit(1)
print("ALL PT PREP TESTS PASSED")
