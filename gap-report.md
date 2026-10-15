# ITN Study Website — Course-Material Gap Report

_Audit date: 2026-10-15. Method: (1) page-level coverage — every page of the 10 provided
source PDFs vs. the built chapter pages; (2) index-level coverage — every meaningful word in
each PDF vs. `corpus.json` (what the Ask search can retrieve); (3) question-bank coverage —
`exam.html`'s 140 items vs. the prioritised topic list. Sources = `uploads/*.pdf` only.
Nothing below asserts anything about lecture content beyond these files._

**Sources present (10 decks, 339 slides):** Ch 1 (42), Ch 2 (43), Ch 3 (35), Ch 4 (46),
Ch 5 (35, +1 duplicate "Tagged" deck, identical → unused), Ch 6 (33), Ch 7 (26), Ch 9 (15),
Ch 10 (26), Ch 16 (38).

---

## 1. Verified complete (no action needed)

- **Page coverage: 339/339 slides appear on their chapter pages** — zero pages missing from
  any chapter page. Build VERIFY passes (417 extracted-line checks).
- **Navigation sections** are declared for every chapter and every slide maps to one.
- **Exam bank covers all eight priority areas** (counts of matching items):
  ARP 13 · IPv4/subnetting 43 (incl. VLSM/hosts 20) · network layer/routing 24 ·
  TCP 13 / UDP 8 / TCP-vs-UDP 8 · DNS 10 · DHCP 10 · HTTP/HTTPS 5 · email 6 ·
  Ethernet/MAC 20 · switching 18 · IOS config & verification 30 · security 18 ·
  troubleshooting 13 · port numbers 10. **No priority topic is absent from the bank.**
- **ARP, Ethernet/MAC, switching, IOS configuration, subnetting basics, TCP/UDP transport,
  DNS, DHCP, email protocols, security threats** are all present in both pages and search
  index with substantive passages.

## 2. Gap group A — content EXISTS on the page but is NOT searchable (indexing bugs)

Root cause: `build_passages()` drops a heading's text when a heading-only group is
discarded at slide end, or when a small group is merged into the previous group (the
heading field is not carried over). A second bug letter-spaces table labels. These are
supported by the sources and will be **fixed**:

| # | Topic & what's missing from search | Source | "Exists under a heading?" distinction |
|---|---|---|---|
| A1 | **Multiplexing**: “Different conversations can be interleaved/multiplexed”, reliability bullets, complexity — 0 index hits | Ch 3 PDF p25 | Page shows them under *Benefits of Message Segmentation*; only the **index** lost them |
| A2 | **Access attacks**: “Password attacks – brute force, trojan horse, packet sniffers”, “Trust exploitation” — 0 index hits | Ch 16 PDF p13 | Page shows them under *Access Attacks*; index lost the heading group |
| A3 | **Password hardening**: `service password-encryption`, `passwords min-length`, `login block-for`, `exec-timeout` — 0 index hits | Ch 16 PDF p27 | Page shows them under *Additional Password Security*; index lost them |
| A4 | **DNS top-level domains**: `.com/.org/.au/.jp/.co` examples — 0 index hits | Ch 10 PDF p19 | Page shows the TLD list; index keeps only 8 fragment words |
| A5 | **Port-number slide labels** rendered/searchable as “V O I P”, “H T T P S”, “I P T V” — `HTTPS`/`VoIP` unfindable | Ch 7 PDF p12 | Page displays letter-splits; fix joins them to VOIP/HTTPS/IPTV |
| A6 | Smaller residue across ch1/2/4/5/6/7/9 (divider words: *introduction, layered, structure*; ch9 *benefits, determining, masking, segmentation*; ch3 *udp, dns, voip, conversations…*) | respective PDFs | Same bug family; re-audit after fix confirms remainder |

## 3. Gap group B — genuinely unavailable in the provided sources (cannot be fixed honestly)

These stay **unresolved by design** — adding them would mean inventing material:

| # | Topic | Finding | Status |
|---|---|---|---|
| B1 | **Chapters 8, 11–15** | No PDFs exist in the project. Page/section numbers beyond the ten decks are **not implied requirements**. | Absent source → not built |
| B2 | **Ch 1 Objectives text** | PDF p2 contains only the title “Chapter 1: Objectives”; the body is not in the text layer. | Title indexed; no body to add |
| B3 | **Ch 9 IPv6 design/summary** | PDF p13/p14 contain only section titles (“9.3 Design Considerations for IPv6”, “9.3 Summary”); bodies are figures. | Title-only indexing stands |
| B4 | **TCP flag names (SYN/ACK)** | Handshake prose is fully covered (Ch 7 p17–p21, steps 1–3). The flag-label diagrams (p18–19) are images; flag tokens don't occur in extractable text. | Handshake covered under *Three-Way Handshake*; flag labels unindexable without OCR |
| B5 | **Port-number table values** | Ch 7 p12's table is an image; text layer holds only the labels (fixed by A5). Port numbers themselves can't be quoted as text. | Labels fixed; cells unindexable |
| B6 | **HTTPS details** | Ch 10 p13 is titled “HTTP and HTTPS” but its bullets describe HTTP only. | Title indexed; no HTTPS body in source → none written |
| B7 | **Public vs private IP comparison** | The pair “public/private” does not occur anywhere in Ch 6 (the only corpus “private” hit is Ch 1 p40 security). | Honest not-found + closest matches remain correct behaviour |
| B8 | **DHCP “DORA”** | Not present in any source text; DHCP Operation (Ch 10 p21–23) is covered without the mnemonic. | Unresolved — no source |
| B9 | **Dedicated troubleshooting sections** | The word “troubleshooting” occurs in no provided deck; closest source material is Ch 2 verification/testing and Ch 16 mitigation. Exam “Troubleshooting” items are **supplementary-labelled**. | No source section to add; labelling preserved |

## 4. Actions taken (implemented)

1. **Fix A1–A6** in `build.py`:
   - `build_passages`: heading-only groups are no longer discarded at slide end, and a
     small group's heading is folded into the merged passage — heading text (attack
     types, hardening commands, TLD lists, multiplexing bullets…) now survives into `x`;
   - sub-3-word fragments (e.g. ch1 p28 “layered structure”) are folded onto the slide's
     passage instead of being dropped;
   - `build_blocks`: letter-spaced table labels are joined (`V O I P` → `VOIP`,
     `H T T P S` → `HTTPS`) so the page shows and search matches the real words;
   - slide **kickers** (section banners like “Benefits of Variable Length Subnet
     Masking”) are persisted as passage field `bk`, and `bot.js` indexes them alongside
     section/title/heading.
2. `corpus.json` and the in-page search index regenerate automatically from the build
   (417 → **425 passages**; every page re-embeds the corpus). No navigation or page
   structure changes were required.
3. Search ranking guards added for honesty: synonym set corrected (`learn` no longer
   maps to `dynamic`; `simultaneously` maps to collision/contention terms) and an
   *unanswerable-question* gate so keyword coincidences are never presented as answers.

## 5. Verification results

| Check | Result |
|---|---|
| Build VERIFY (extracted lines ⊆ HTML) | **OK** (417 line checks, 10 chapters) |
| Final word-level index audit vs. PDFs | **0 missing words** (footers excluded by design) |
| Search retrieval of newly indexed material | **12/12** (password attacks, exec-timeout, multiplexing, TLDs, kickers, VOIP/HTTPS, layered structure…) |
| Search regression suites | **27/27 + 102/102** |
| Full project battery | **8/8 suites green** (27+102+184+172+293+248+126+49 = 1,201 assertions) |
| Link crawl | **1,709 internal links — 0 broken files, 0 broken anchors**; all 14 pages link all 10 chapters |
| HTTP | **15/15 pages return 200** |
| Package | `itn-study-website.zip` regenerated (6,399,113 B, 16 entries) |

## 6. Remains unresolved (source material unavailable — nothing invented)

Group B1–B9 above all stand: Ch 8 / 11–15 decks absent from the project; Ch 1
Objectives, Ch 9 IPv6 design/summary are figure-only in the PDFs (titles indexed);
TCP SYN/ACK flag labels and the port-number table cells exist only inside slide images
(handshake prose and the VOIP/HTTPS/IPTV labels are indexed); HTTPS has no body text
beyond its slide title; the public-vs-private IP comparison and the DORA mnemonic do not
occur in any source deck; no provided deck contains a dedicated “troubleshooting”
section — supplementary-labelled exam items remain clearly marked as such.
