#!/usr/bin/env python3
"""Structural tests for the chapter revision kit.

Run:  python3 site-build/test_revision.py
Verifies, for every chapter page:
  * the revision kit exists with all 8 required sections
  * 5–10 knowledge-check questions, every answer hidden behind <details>
  * all four question types present per chapter
  * source/supplementary/practice badges and the gaps block
  * every internal slide link (#pN) resolves to a real anchor
  * every corpus passage anchor still exists (content preservation)
Exits non-zero on any failure.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "itn-site")

CHAPTERS = [1, 2, 3, 4, 5, 6, 7, 9, 10, 16]
REQUIRED_HEADINGS = [
    "Chapter overview", "Key definitions", "Concept explanations",
    "Comparisons", "Important facts", "Knowledge check",
    "Common misunderstandings", "Quick revision",
]
QUESTION_TYPES = ["Multiple choice", "True or false", "Short answer", "Explanation"]

corpus = json.load(open(os.path.join(SITE, "corpus.json"), encoding="utf-8"))
by_file = {}
for p in corpus:
    by_file.setdefault(p["f"], []).append(p)

pass_n = fail_n = 0
failures = []


def chk(name, ok, detail=""):
    global pass_n, fail_n
    if ok:
        pass_n += 1
    else:
        fail_n += 1
        failures.append(name + (" — " + str(detail) if detail else ""))


def check_chapter(n):
    fn = f"chapter{n}.html"
    path = os.path.join(SITE, fn)
    chk(f"ch{n}: page exists", os.path.isfile(path))
    if not os.path.isfile(path):
        return
    html = open(path, encoding="utf-8").read()

    # kit + sections
    chk(f"ch{n}: #revision present", 'id="revision"' in html)
    sec_count = html.count('class="rev-sec"')
    chk(f"ch{n}: rev-sec count >= 8 (got {sec_count})", sec_count >= 8)
    for h in REQUIRED_HEADINGS:
        chk(f"ch{n}: heading '{h}'", h in html)

    # badges: source / study note / practice
    chk(f"ch{n}: 'From the course PDFs' badge", "From the course PDFs" in html)
    chk(f"ch{n}: 'Study note' badge", "Study note" in html)
    chk(f"ch{n}: 'Practice' badge", ">Practice</span>" in html)

    # TOC entry
    chk(f"ch{n}: TOC has revision-kit link", 'href="#revision">★ Revision kit' in html)

    # knowledge check
    kc = html.count('class="kc-item"')
    chk(f"ch{n}: kc items 5–10 (got {kc})", 5 <= kc <= 10, kc)
    ans = html.count('<details class="kc-ans"')
    chk(f"ch{n}: every answer behind details ({ans}/{kc})", ans == kc, f"{ans} vs {kc}")
    for t in QUESTION_TYPES:
        chk(f"ch{n}: question type '{t}'", t in html)
    chk(f"ch{n}: not-exam disclaimer", "not</b> lecturer or examination questions" in html
       or "not lecturer or exam questions" in html
       or "they are <b>not</b> lecturer or examination questions" in html)

    # comparisons (tables) + gaps
    cmp_n = html.count('class="cmp"')
    chk(f"ch{n}: at least one comparison table/gap block",
       cmp_n >= 1 or 'class="rev-gap"' in html, cmp_n)
    if n == 6:  # private-vs-public gap must be visible here
        chk("ch6: private-vs-public gap stated", "Private vs public IP addresses" in html)
    chk(f"ch{n}: gaps block present", "Identified source-material gaps" in html)

    # internal slide links resolve
    targets = set(re.findall(r'href="#(p\d+)"', html))
    missing = [t for t in targets if f'id="{t}"' not in html]
    chk(f"ch{n}: all #{' '.join(list(targets)[:0])}slide links resolve"
       if not missing else f"ch{n}: broken slide links", not missing, missing[:8])

    # preservation: every corpus passage anchor for this page still exists
    anchors = [p["a"] for p in by_file.get(fn, [])]
    lost = [a for a in anchors if f'id="{a}"' not in html]
    chk(f"ch{n}: all {len(anchors)} passage anchors preserved", not lost, lost[:8])

    # original sections/slides still present
    chk(f"ch{n}: original section headers intact",
       html.count('class="sec"') >= 3 or f'Chapter {n}' in html)


def check_global():
    idx = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    chk("home: lab card still present", 'href="lab.html"' in idx)
    lab = open(os.path.join(SITE, "lab.html"), encoding="utf-8").read()
    chk("lab: page intact", 'id="lab-root"' in lab and "vlsmAllocate" in lab)
    for n in CHAPTERS:
        html = open(os.path.join(SITE, f"chapter{n}.html"), encoding="utf-8").read()
        chk(f"global: ch{n} nav has Home + Chapters + Lab + Ask",
           'href="index.html"' in html and "navdrop" in html
           and 'href="lab.html"' in html and "data-open-ask" in html)
        # search feature untouched
        chk(f"global: ch{n} has ask/search wiring",
           "window.__ITN__" in html and "ITNAsk" in html)


print("=== Revision kit structural tests ===")
for n in CHAPTERS:
    check_chapter(n)
check_global()

print(f"\nRESULTS: {pass_n} passed, {fail_n} failed, total {pass_n + fail_n}")
if failures:
    print("FAILURES:")
    for f in failures:
        print("  ✗ " + f)
    sys.exit(1)
print("ALL REVISION TESTS PASSED")
