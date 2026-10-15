# ITN Study Hub — Networking Study Website

A **self-contained, static study site** for Cisco's *Introduction to Networks (ITN)*
course material. It turns the ten provided course PDFs (339 slides) into an
interactive, offline-friendly website: searchable chapter pages with slide-level
source links, a client-side Q&A assistant, an IPv4/subnetting lab, Packet Tracer
preparation labs with IOS command drills, and an exam-practice mode — everything
runs in the browser with **no servers, no accounts, no paid APIs, and no external
CDNs**.

**Package:** `itn-study-website.zip` — the complete project: built site
(`itn-site/`), full source (`site-build/`), source course PDFs (`uploads/`),
this README and the gap report.

---

## Pages

| Page | What it is |
|---|---|
| `index.html` | Home — overview of the hub and entry points to every feature |
| `chapter1.html` … `chapter16.html` (10 pages) | One page per available chapter, each containing **every slide of its PDF** (339 slides total) plus a revision kit section |
| `lab.html` | **IPv4 Addressing & Subnetting Lab** |
| `ptlab.html` | **Packet Tracer Practical Preparation** + IOS command practice |
| `exam.html` | **Exam Practice Mode** |
| `corpus.json` | 425-passage searchable corpus used by the Q&A assistant (also embedded in every page) |

**Navigation** (identical on every page): **Home · Chapters ▾** (page-per-chapter
dropdown for all ten chapters) **· IPv4 Lab · PT Prep · Exam · Ask**.

### Chapter pages
Chapters 1–7, 9, 10 and 16: *Exploring the Network · Configuring a Network OS ·
Network Protocols and Communication · Network Access · Ethernet · Network Layer ·
Transport Layer · Subnetting IP Networks · Application Layer · Network Security
Fundamentals*. Each slide is an anchor (`#p14` …), so every reference anywhere in
the site links to the exact source slide. Every chapter also embeds a **revision
kit** (key-point questions, terminology drills, identified source-material gaps)
labelled as course material vs. supplementary study aid.

### Ask box (every page)
A client-side Q&A assistant over the full 425-passage, ten-chapter corpus.
Results are question-aligned, show the chapter/slide they come from, and fall
back honestly ("nothing found") instead of returning unrelated keyword matches.
Everything is computed locally from the embedded corpus — queries never leave
the page.

### IPv4 Lab (`lab.html`)
- **Calculator** — address/mask/CIDR in any common form, with network, broadcast,
  first/last usable, host counts, private/public scope, and a binary view.
- **Step-by-step solutions** — worked arithmetic after every calculation
  (prefix → mask → block size → boundary octet → network/broadcast → range).
- **Practice & quiz** — randomly generated, independently re-verified questions
  in ten types (masks, network/broadcast, ranges, host counts, subnet sizing,
  dividing a network, subnet counting, subnet-of-a-host, VLSM). Difficulty:
  **Easy / Medium / Hard / Mixed (revision set)**; automatic answer checking with
  CIDR ↔ dotted-decimal ↔ bare-number equivalence, explanations for wrong
  answers, the **complete correct solution** shown after each submission,
  running accuracy, and a retry-missed-questions pass.

### PT Prep (`ptlab.html`)
Four guided configuration labs — build each topology in the **official Cisco
Packet Tracer application**, using this page as the lab sheet:
1. PCs and a switch (addressing end devices, same network vs. gateway)
2. Router interfaces (the course's own router configuration transcript)
3. Connecting different networks (subnetting + VLSM planning)
4. Troubleshooting wrong IPs, gateways and interface states

Each lab includes objective, required devices, topology diagram (SVG), addressing
table, step-by-step configuration, verification commands, expected results,
common mistakes, checklists with progress bars (saved locally), quizzes with
explanations, and clickable slide links — with **Assumption** tags wherever the
course leaves a choice open.

**IOS command practice** — 20 drills on the commands the course actually uses
(interface configuration, IP assignment, `no shutdown`, saving configs,
`show ip interface brief`, `ping` …). Every item is tagged **Configuration**
(changes the device) or **Verification** (reads/tests state) and answered with an
explanation plus the source slide.

### Exam Practice (`exam.html`)
- **Chapter sessions** — pick chapters, length (10/20/30) and mode (untimed, 30 s
  or 60 s per question), with an absolute-time countdown that survives reloads.
- **Topic quick quizzes** — 5-question single-topic quizzes (12 topics) for fast,
  focused sessions.
- After each submission: correct answer, explanation, and the Course /
  Supplementary source line; at the end: score, review list, **weak-topic chips
  with a "Next step" revision recommendation** (e.g. subnetting → the IPv4 Lab,
  troubleshooting → PT Lab 4), one-click **retry of incorrect questions**, a
  results history table, and resume-after-reload of unfinished sessions.
- Every item is labelled **Course** (grounded in a specific chapter) or
  **Supplementary**; the bank is built only from this site's material.

---

## Content sources & honesty rules

- Primary source is the provided course PDFs (`uploads/` — 339 slides);
  the build's **VERIFY** step fails unless every extracted line appears in the
  generated HTML.
- Chapters 8 and 11–15 are **not present in the source material** — they are
  absent from the site rather than invented.
- The site **does not run Packet Tracer or IOS**: labs and command drills are
  static instructions/transcripts; practice happens in the official app or on
  real equipment.
- Exam practice is study drill material only — **nothing here predicts, mirrors
  or claims to represent the actual Cisco examination**.
- No paid services, no external APIs, no AI claims; sources are never invented.

## Storage & privacy (browser-local only)

| Key | Page | Stores |
|---|---|---|
| `itn-lab-stats-v1` | lab | Lifetime quiz counters `{answered, correct}` only |
| `itn-ios-stats-v1` | ptlab | Lifetime IOS-drill counters only |
| `itn-pt-checks-v1` | ptlab | Lab checklists + quiz state |
| `itn-exam-session-v1` / `itn-exam-history-v1` | exam | Unfinished session (for resume) + last 20 results |

Nothing is uploaded, there are no accounts, and nothing syncs between devices;
clearing site data resets these counters. If storage is unavailable, features
keep working for the current page session. These limits are stated on the pages
themselves.

---

## Project layout

```
site-build/                 # source (edit here, then rebuild)
  build.py                  # builds itn-site/ from uploads/ + these sources
  ptlabs.py, exam.py        # PT labs & exam bank generators
  ipv4.js, lab.js, ios.js   # lab, subnetting, IOS-practice engines
  pt.js, exam.js, bot.js    # PT page, exam mode, Q&A engine
  revision/                 # revision-kit source data
  style.css                 # single stylesheet (inlined into pages)
  test_*.js / test_*.py     # 10 test suites
itn-site/                   # built site (static, deployable as-is)
itn-study-website.zip       # downloadable package of itn-site/
uploads/                    # source course PDFs
```

## Build & test

```bash
pip install pymupdf                      # build-time dependency (open source)
cd site-build
python3 build.py                         # ends with: VERIFY OK — 425 passages

# test suites (all must exit 0)
python3 test_revision.py                 # 293
node    test-ipv4.js                     # 248
node    test-search.js                   # 27
node    test-search-questions.js         # 102 (Q&A regression)
python3 test-exam.py                     # 184
node    test-exam.js                     # ~170 (0 failures)
python3 test-pt.py                       # 126
node    test-pt.js                       # 49
node    test-practice.js                 # 383 (mixed/IOS/topic flows)
python3 test-practice.py                 # 82  (built-page structure)
```

**Run locally:**

```bash
python3 -m http.server 8000 --directory itn-site
# → http://localhost:8000/
```

Regenerate the downloadable package after any rebuild:

```bash
rm itn-study-website.zip && zip -r itn-study-website.zip itn-site
```
