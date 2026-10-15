#!/usr/bin/env python3
"""Structural tests for the exam practice page (exam.html).

Run:  python3 site-build/test-exam.py
Verifies: page + embedded bank (size, all six question types, per-chapter
pools >= 10), every required UI control, honest labelling/disclaimers,
site-wide nav integration, no external resources, and that the original
corpus is untouched. Exits non-zero on any failure.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "itn-site")

CHAPTERS = [1, 2, 3, 4, 5, 6, 7, 9, 10, 16]
ALL_PAGES = (["index.html", "lab.html", "ptlab.html", "exam.html"]
             + [f"chapter{n}.html" for n in CHAPTERS])

pass_n = fail_n = 0
failures = []


def chk(name, ok, detail=""):
    global pass_n, fail_n
    if ok:
        pass_n += 1
    else:
        fail_n += 1
        failures.append(name + (" — " + str(detail) if detail else ""))


path = os.path.join(SITE, "exam.html")
chk("exam.html exists", os.path.isfile(path))
html = open(path, encoding="utf-8").read() if os.path.isfile(path) else ""

if html:
    # ---- embedded bank ----
    m = re.search(r"window\.__ITN_EXAM__=(.*?);</script>", html, re.S)
    chk("bank embedded", bool(m))
    bank = json.loads(m.group(1)) if m else []
    chk(f"bank size >= 120 (got {len(bank)})", len(bank) >= 120, len(bank))
    types = {}
    for b in bank:
        types[b["ty"]] = types.get(b["ty"], 0) + 1
    for t in ("mc", "tf", "short", "term", "calc", "trouble"):
        chk(f"question type present: {t}", types.get(t, 0) >= 1, types.get(t))
    chk("supplementary items exist", types.get("trouble", 0) >= 10)
    # unique ids + answerability
    ids = [b["i"] for b in bank]
    chk("unique ids", len(ids) == len(set(ids)))
    bad = [b["i"] for b in bank if not (b.get("e") and b.get("q") and b.get("tp"))]
    chk("every item has explanation+topic", not bad, bad[:5])
    bad_choice = [b["i"] for b in bank if b["ty"] in ("mc", "term", "trouble", "tf")
                  and not (0 <= b.get("a", -1) < len(b.get("o", [])))]
    chk("every choice has in-range answer", not bad_choice, bad_choice[:5])
    for n in CHAPTERS:
        c = sum(1 for b in bank if n in b["c"])
        chk(f"ch{n} pool >= 10 (got {c})", c >= 10, c)

    # ---- required UI ----
    for el_id in ["ex-root", "ex-setup", "ex-quiz", "ex-results", "ex-resume",
                  "ex-resume-text", "ex-resume-yes", "ex-resume-no", "ex-all",
                  "ex-pool-note", "ex-start", "ex-progress", "ex-topic",
                  "ex-type", "ex-src", "ex-timer", "ex-bar", "ex-q", "ex-opts",
                  "ex-short", "ex-input", "ex-submit", "ex-feedback",
                  "ex-verdict", "ex-correct", "ex-why", "ex-next", "ex-score",
                  "ex-pct", "ex-weak-wrap", "ex-weak", "ex-retry", "ex-again",
                  "ex-review", "ex-hist-body"]:
        chk(f"#{el_id}", f'id="{el_id}"' in html)
    for n in CHAPTERS:
        chk(f"chapter selector Ch {n}", f'data-ch="{n}"' in html)
    for L in (10, 20, 30):
        chk(f"length button {L}", f'data-len="{L}"' in html)
    for M in ("untimed", "30", "60"):
        chk(f"mode button {M}", f'data-mode="{M}"' in html)
    chk("one-question progress label", 'id="ex-progress"' in html)
    chk("engine embedded", "validSession" in html and "gradeChoice" in html)
    chk("session key embedded", "itn-exam-session-v1" in html)
    chk("history key embedded", "itn-exam-history-v1" in html)

    # ---- honesty / labelling ----
    chk("no-exam-prediction disclaimer",
        "nothing here predicts" in html and "actual Cisco examination" in html)
    chk("Supplementary labelling explained", "Supplementary" in html)
    chk("persistence limitations explained",
        "do not sync" in html and "localStorage" in html)
    chk("silent-restore refusal stated",
        "nothing is restored silently" in html.lower())
    chk("practice-only badge present", "Practice only" in html)

    # ---- no external resources ----
    ext = re.findall(r'(?:src|href)="https?://[^"]+"', html)
    chk("no external URLs", not ext, ext[:5])

    # ---- nav integration ----
    for fn in ALL_PAGES:
        p = os.path.join(SITE, fn)
        chk(f"{fn} exists", os.path.isfile(p))
        if not os.path.isfile(p):
            continue
        h = open(p, encoding="utf-8").read()
        chk(f"{fn} nav has Exam", 'href="exam.html"' in h)
        chk(f"{fn} nav keeps PT Prep", 'href="ptlab.html"' in h)
        chk(f"{fn} nav keeps IPv4 Lab", 'href="lab.html"' in h)
        chk(f"{fn} nav keeps Chapters", 'class="navdrop' in h)
        chk(f"{fn} nav keeps Ask", "data-open-ask" in h)
    chk("exam marks current",
        'href="exam.html" aria-current="page"' in html)
    idx = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    chk("home card links to exam", 'href="exam.html">Start practising' in idx)

    # ---- preservation ----
    corpus = json.load(open(os.path.join(SITE, "corpus.json"), encoding="utf-8"))
    chk(f"corpus still 425 (got {len(corpus)})", len(corpus) == 425, len(corpus))
    for fn in ("index.html", "lab.html", "ptlab.html",
               *[f"chapter{n}.html" for n in CHAPTERS]):
        p = os.path.join(SITE, fn)
        chk(f"{fn} non-trivial size", os.path.isfile(p)
            and os.path.getsize(p) > 10000)

print("=== Exam practice structural tests ===")
print(f"RESULTS: {pass_n} passed, {fail_n} failed, total {pass_n + fail_n}")
if failures:
    print("FAILURES:")
    for f in failures:
        print("  ✗ " + f)
    sys.exit(1)
print("ALL EXAM STRUCTURAL TESTS PASSED")
