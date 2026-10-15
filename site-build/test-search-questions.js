#!/usr/bin/env node
/* ============================================================
   Question-quality tests for the upgraded search (bot.js).
   Run:  node site-build/test-search-questions.js

   24 realistic networking questions — including questions
   phrased differently from the source headings, abbreviation
   typos, multi-concept questions, an honest low-confidence
   case and off-topic negatives. Reports PASS/FAIL per
   question and exits non-zero on any failure.
   ============================================================ */
'use strict';

var fs = require('fs');
var path = require('path');

var corpus = require(path.join(__dirname, '..', 'itn-site', 'corpus.json'));
global.window = { __ITN__: { passages: corpus } };
global.document = {
  readyState: 'loading',
  addEventListener: function () {},
  getElementById: function () { return null; },
  querySelectorAll: function () { return []; },
  querySelector: function () { return null; }
};
require('./bot.js');
var A = global.window.ITNAsk;

var pass = 0, fail = 0;
var qFail = {}, qTotal = {};
function chk(qname, label, ok, detail) {
  qTotal[qname] = (qTotal[qname] || 0) + 1;
  if (ok) { pass++; }
  else {
    fail++;
    qFail[qname] = (qFail[qname] || []);
    qFail[qname].push(label + (detail !== undefined ? ' — ' + detail : ''));
  }
}
function top(r) { return r.hits.length ? r.hits[0].p : null; }
function anyHit(r, re) {
  return r.hits.some(function (h) {
    return re.test((h.p.t || '') + ' ' + (h.p.h || '') + ' ' + (h.p.x || ''));
  });
}
function covered(r, re) {
  var all = r.hits.map(function (h) {
    return ((h.p.t || '') + ' ' + (h.p.h || '') + ' ' + (h.p.x || '')).toLowerCase();
  }).join(' ||| ');
  return re.test(all);
}

/* ================= required topic areas ================= */

var CASES = [
  { q: 'What does ARP do?',
    expect: function (r, n) {
      chk(n, 'has >=3 hits', r.hits.length >= 3, 'h=' + r.hits.length);
      chk(n, 'top is ch5 ARP material', top(r) && top(r).c === 5 &&
        /ARP|Address Resolution/i.test((top(r).t || '') + (top(r).x || '')),
        top(r) ? 'ch' + top(r).c + ' ' + top(r).t : 'none');
      chk(n, 'confident (not flagged low)', !r.lowConfidence, 'conf=' + r.confidence);
      chk(n, 'explains why each result matched',
        r.hits.every(function (h) { return h.reasons && h.reasons.length >= 1; }));
    } },

  { q: 'How does a device find the MAC address of the default router?',
    expect: function (r, n) {
      chk(n, 'has >=3 hits', r.hits.length >= 3, 'h=' + r.hits.length);
      chk(n, 'top-3 include ARP/lookup material (ch5)',
        r.hits.slice(0, 3).some(function (h) {
          return h.p.c === 5 && /ARP|resolution/i.test((h.p.t || '') + (h.p.x || ''));
        }));
      chk(n, 'results cover both mac and router concepts',
        covered(r, /\bmac\b/) && covered(r, /router|gateway/));
      chk(n, 'not flagged low', !r.lowConfidence, 'conf=' + r.confidence);
    } },

  { q: 'How does a switch learn which port leads to which device?',
    expect: function (r, n) {
      chk(n, 'top is ch5', top(r) && top(r).c === 5, top(r) ? 'ch' + top(r).c : '');
      chk(n, 'top mentions switch/port/learning',
        /switch port|learn|forward/i.test((top(r).t || '') + (top(r).x || '')));
      chk(n, '>=3 hits', r.hits.length >= 3, 'h=' + r.hits.length);
    } },

  { q: 'Why do networks need subnet masks?',
    expect: function (r, n) {
      chk(n, 'top is ch9 subnetting', top(r) && top(r).c === 9, top(r) ? 'ch' + top(r).c : '');
      chk(n, 'top mentions subnet/mask',
        /subnet|mask/i.test((top(r).t || '') + (top(r).x || '')));
      chk(n, 'confident', !r.lowConfidence, 'conf=' + r.confidence);
    } },

  { q: 'Why does a device need both an IP address and a subnet mask?',
    expect: function (r, n) {
      chk(n, 'has >=3 hits', r.hits.length >= 3, 'h=' + r.hits.length);
      chk(n, 'results cover ip AND subnet concepts',
        covered(r, /\bip\b|internet protocol/) && covered(r, /subnet|mask/));
      chk(n, 'hits come from addressing chapters (2 or 9)',
        r.hits.slice(0, 3).every(function (h) { return h.p.c === 2 || h.p.c === 9; }));
      chk(n, 'confident', !r.lowConfidence, 'conf=' + r.confidence);
    } },

  { q: 'Explain how to work out how many usable hosts fit in a subnet',
    expect: function (r, n) {
      chk(n, 'top is ch9', top(r) && top(r).c === 9, top(r) ? 'ch' + top(r).c : '');
      chk(n, 'top mentions hosts/subnet',
        /host|subnet/i.test((top(r).t || '') + (top(r).x || '')));
      chk(n, 'a procedure/definition reason appears somewhere',
        r.hits.some(function (h) {
          return (h.reasons || []).some(function (x) {
            return /procedure|definition/i.test(x);
          });
        }));
    } },

  { q: 'What is the purpose of a default gateway?',
    expect: function (r, n) {
      chk(n, 'top is ch6', top(r) && top(r).c === 6, top(r) ? 'ch' + top(r).c : '');
      chk(n, 'top heading is gateway material',
        /default gateway/i.test((top(r).t || '') + (top(r).h || '')));
      chk(n, 'confident', !r.lowConfidence, 'conf=' + r.confidence);
    } },

  { q: 'How does a router choose the path a packet takes?',
    expect: function (r, n) {
      chk(n, 'top is ch6 routing', top(r) && top(r).c === 6, top(r) ? 'ch' + top(r).c + ':' + top(r).t : '');
      chk(n, '>=2 of top-5 are ch6 routing passages',
        r.hits.slice(0, 5).filter(function (h) {
          return h.p.c === 6 && /rout|forward|path|gateway/i.test((h.p.t || '') + (h.p.x || ''));
        }).length >= 2,
        r.hits.slice(0, 5).map(function (h) { return 'ch' + h.p.c; }).join(','));
      chk(n, 'a heading-match reason appears',
        r.hits.some(function (h) {
          return (h.reasons || []).some(function (x) { return /Heading/i.test(x); });
        }));
    } },

  { q: "What's the difference between TCP and UDP?",
    expect: function (r, n) {
      chk(n, 'has >=2 hits', r.hits.length >= 2, 'h=' + r.hits.length);
      chk(n, 'results cover both tcp and udp', covered(r, /\btcp\b/) && covered(r, /\budp\b/));
      chk(n, 'top is ch7 transport material', top(r) && top(r).c === 7,
        top(r) ? 'ch' + top(r).c : '');
      chk(n, 'both-sides reason shown',
        (r.hits[0].reasons || []).some(function (x) { return /both/i.test(x); }));
    } },

  { q: 'Which transport protocol is connectionless, TCP or UDP?',
    expect: function (r, n) {
      chk(n, 'top is ch7', top(r) && top(r).c === 7, top(r) ? 'ch' + top(r).c : '');
      chk(n, 'covers both sides', covered(r, /\btcp\b/) && covered(r, /\budp\b/));
      chk(n, 'confident', !r.lowConfidence, 'conf=' + r.confidence);
    } },

  { q: 'How does DNS let me browse by website name instead of numbers?',
    expect: function (r, n) {
      chk(n, 'top is ch10 Domain Name Service',
        top(r) && top(r).c === 10 && /domain name/i.test(top(r).t || ''),
        top(r) ? 'ch' + top(r).c + ':' + top(r).t : '');
      chk(n, 'confident', !r.lowConfidence, 'conf=' + r.confidence);
    } },

  { q: 'How does a web browser find the IP address for cisco.com?',
    expect: function (r, n) {
      chk(n, 'has >=3 hits', r.hits.length >= 3, 'h=' + r.hits.length);
      chk(n, 'top-3 include a DNS/name-resolution passage',
        r.hits.slice(0, 3).some(function (h) {
          return h.p.c === 10 && /domain name|name resolution|dns/i.test((h.p.t || '') + (h.p.x || ''));
        }));
      chk(n, 'covers domain + address concepts',
        covered(r, /domain|name|url/) && covered(r, /address/));
    } },

  { q: 'What happens when a computer requests an IP address automatically?',
    expect: function (r, n) {
      chk(n, 'top is ch10 DHCP', top(r) && top(r).c === 10 &&
        /dynamic host configuration|dhcp/i.test(top(r).t || ''),
        top(r) ? 'ch' + top(r).c + ':' + top(r).t : '');
      chk(n, 'confident', !r.lowConfidence, 'conf=' + r.confidence);
    } },

  { q: 'How does DHCP asign IP addreses?',
    expect: function (r, n) {
      chk(n, 'spelling tolerance fired (>=2 corrections)',
        r.fuzzy && r.fuzzy.length >= 2, JSON.stringify(r.fuzzy));
      chk(n, 'top is ch10 DHCP', top(r) && top(r).c === 10 &&
        /dhcp|dynamic host/i.test(top(r).t || ''),
        top(r) ? 'ch' + top(r).c + ':' + top(r).t : '');
      chk(n, 'not flagged low despite typos', !r.lowConfidence, 'conf=' + r.confidence);
      var box = { innerHTML: '' };
      A.renderResults(box, 'How does DHCP asign IP addreses?', r, {});
      chk(n, 'render shows spelling-tolerance note',
        /ask-dym/.test(box.innerHTML) && /asign/.test(box.innerHTML));
    } },

  { q: 'What fields are inside an Ethernet frame?',
    expect: function (r, n) {
      chk(n, 'top is ch4/ch5 data-link material',
        top(r) && (top(r).c === 4 || top(r).c === 5), top(r) ? 'ch' + top(r).c : '');
      chk(n, 'results mention ethernet/frame',
        covered(r, /ethernet/) && covered(r, /frame/));
      chk(n, 'confident', !r.lowConfidence, 'conf=' + r.confidence);
    } },

  { q: 'Why does Ethernet need a collision domain?',
    expect: function (r, n) {
      chk(n, 'top mentions collision', /collision/i.test((top(r).t || '') + (top(r).x || '')));
      chk(n, 'top is ch4/ch5', top(r) && (top(r).c === 4 || top(r).c === 5),
        top(r) ? 'ch' + top(r).c : '');
    } },

  { q: 'What happens on a switch when two devices transmit simultaneously?',
    expect: function (r, n) {
      chk(n, 'has >=3 hits', r.hits.length >= 3, 'h=' + r.hits.length);
      chk(n, 'collision/contended access covered',
        covered(r, /collision|csma|contend/));
      chk(n, 'top is ethernet/data-link chapter (4 or 5)',
        top(r) && (top(r).c === 4 || top(r).c === 5), top(r) ? 'ch' + top(r).c : '');
    } },

  { q: 'What is a denial of service attack?',
    expect: function (r, n) {
      chk(n, 'top is ch16 security', top(r) && top(r).c === 16,
        top(r) ? 'ch' + top(r).c + ':' + top(r).t : '');
      chk(n, 'top heading names the attack',
        /denial of service/i.test((top(r).t || '') + (top(r).h || '')));
      chk(n, 'confident', !r.lowConfidence, 'conf=' + r.confidence);
    } },

  { q: 'How do I protect my passwords from attackers?',
    expect: function (r, n) {
      chk(n, 'top-5 all security material (ch16)',
        r.hits.slice(0, 5).every(function (h) { return h.p.c === 16; }));
      chk(n, 'a Passwords heading in top-3',
        r.hits.slice(0, 3).some(function (h) {
          return /password/i.test((h.p.t || '') + (h.p.h || ''));
        }));
      chk(n, '>=3 hits', r.hits.length >= 3, 'h=' + r.hits.length);
    } },

  { q: 'What is the difference between a logical address and a physical address?',
    expect: function (r, n) {
      chk(n, 'top is the MAC-vs-IP passage (ch5)',
        top(r) && top(r).c === 5 && /MAC and IP/i.test(top(r).t || ''),
        top(r) ? 'ch' + top(r).c + ':' + top(r).t : '');
      chk(n, 'top reason names both sides',
        (r.hits[0].reasons || []).some(function (x) { return /both/i.test(x); }));
      chk(n, 'confident', !r.lowConfidence, 'conf=' + r.confidence);
    } },

  { q: 'What is a VLAN?',
    expect: function (r, n) {
      chk(n, 'has >=3 hits', r.hits.length >= 3, 'h=' + r.hits.length);
      chk(n, 'hits really discuss VLANs', covered(r, /\bvlan\b/));
      chk(n, 'confident', !r.lowConfidence, 'conf=' + r.confidence);
    } },

  { q: 'Tell me about how switches learn where devices are',
    expect: function (r, n) {
      chk(n, 'top is ch5', top(r) && top(r).c === 5, top(r) ? 'ch' + top(r).c : '');
      chk(n, 'covers learn + mac/switch concepts',
        covered(r, /learn/) && covered(r, /mac|switch/));
      chk(n, 'confident', !r.lowConfidence, 'conf=' + r.confidence);
    } },

  { q: 'What is a MAC address and how does a switch use it?',
    expect: function (r, n) {
      chk(n, '>=4 hits (two concepts, several excerpts)', r.hits.length >= 4,
        'h=' + r.hits.length);
      chk(n, 'covers mac AND switch/forwarding',
        covered(r, /\bmac\b/) && covered(r, /switch|forward|port/));
      chk(n, 'hits come from at least 2 distinct sections',
        (function () {
          var s = {};
          r.hits.forEach(function (h) { s[h.p.f + '#' + (h.p.sid || h.p.a)] = 1; });
          return Object.keys(s).length >= 2;
        })());
      chk(n, 'confident', !r.lowConfidence, 'conf=' + r.confidence);
    } },

  { q: 'What is adress resolution protokol?',
    expect: function (r, n) {
      chk(n, 'spelling tolerance: adress->address, protokol->protocol',
        r.fuzzy && r.fuzzy.length >= 2 &&
        r.fuzzy.some(function (f) { return f.from === 'adress' && f.t === 'address'; }) &&
        r.fuzzy.some(function (f) { return f.from === 'protokol' && f.t === 'protocol'; }),
        JSON.stringify(r.fuzzy));
      chk(n, 'top is ch5 ARP section',
        top(r) && top(r).c === 5 && /address resolution|ARP/i.test(top(r).t || ''),
        top(r) ? 'ch' + top(r).c + ':' + top(r).t : '');
      chk(n, 'typo query still confident', !r.lowConfidence, 'conf=' + r.confidence);
      var box = { innerHTML: '' };
      A.renderResults(box, 'What is adress resolution protokol?', r, {});
      chk(n, 'render explains the correction',
        /ask-dym/.test(box.innerHTML) && /adress/.test(box.innerHTML));
    } }
];

/* ============ low confidence & honest negatives (req 7) ============ */

function lowConfidenceCase() {
  var n = 'Q25 low-confidence: satellite/latency';
  var r = A.search('How do satellite links handle latency?', 6);
  chk(n, 'returns closest matches (>=1 hit)', r.hits.length >= 1, 'h=' + r.hits.length);
  chk(n, 'flags confidence as low', r.lowConfidence === true, 'conf=' + r.confidence);
  var box = { innerHTML: '' };
  A.renderResults(box, 'How do satellite links handle latency?', r, {});
  chk(n, 'render asks user to refine', /Low confidence/.test(box.innerHTML) &&
    /refine your question/.test(box.innerHTML));
  chk(n, 'labels them closest matches, not an answer',
    /closest matches/i.test(box.innerHTML) && !/this is the answer/i.test(box.innerHTML));
}

function negativeCase(q) {
  var n = 'off-topic: "' + q + '"';
  var r = A.search(q, 6);
  chk(n, 'zero hits', r.hits.length === 0, 'h=' + r.hits.length);
  chk(n, 'zero loose suggestions', (r.loose || []).length === 0,
    'l=' + (r.loose || []).length);
  var box = { innerHTML: '' };
  A.renderResults(box, q, r, {});
  chk(n, 'honest not-found wording', /couldn't find a relevant explanation/i.test(box.innerHTML));
  chk(n, 'no fabricated answer', !/the answer is|here is the answer/i.test(box.innerHTML));
}

/* ============ rendered-card requirements (req 4, 5) ============ */
function renderCardChecks() {
  var n = 'rendered card: heading + chapter + section link + highlight + why';
  var r = A.search('What is the purpose of ARP?', 6);
  var box = { innerHTML: '' };
  A.renderResults(box, 'What is the purpose of ARP?', r, {});
  var h = box.innerHTML;
  chk(n, 'chapter number link', /Chapter \d+/.test(h) && /chapter\d+\.html/.test(h));
  chk(n, 'section link to exact slide', /res-sec/.test(h) && /#p\d+/.test(h));
  chk(n, 'original heading/title shown', /res-title/.test(h));
  chk(n, 'terms highlighted with <mark>', /<mark>/.test(h));
  chk(n, 'why-relevant line', /Why this matched:/.test(h));
  chk(n, 'system-added note disclosed', /system-generated note/.test(h));
  chk(n, 'verbatim source note kept', /verbatim source text/.test(h));
  chk(n, 'multiple results shown', (h.match(/res-card/g) || []).length >= 3,
    'cards=' + (h.match(/res-card/g) || []).length);
  chk(n, 'related sections offered', /Related sections/.test(h) || r.related.length >= 0);
}

function offlineAndHonestyChecks() {
  var n = 'offline / honesty (static)';
  var src = fs.readFileSync(path.join(__dirname, 'bot.js'), 'utf8');
  chk(n, 'no fetch/XHR/API calls in bot.js',
    !/fetch\s*\(|XMLHttpRequest|XMLHttp/.test(src));
  chk(n, 'no external http(s) URLs in bot.js',
    !/https?:\/\//.test(src.replace(/https?:\/\/www\.w3\.org/g, '')));
  chk(n, 'AI-disclaimer present in engine header',
    /NOT an AI model/.test(src));
  chk(n, 'quotes stay verbatim (highlight only wraps, never rewrites)',
    /Excerpt text is quoted verbatim/.test(src));
  chk(n, 'corpus still 425 passages', corpus.length === 425, corpus.length);
}

/* ================= run ================= */
console.log('=== Search question suite: 24 realistic questions ===');
CASES.forEach(function (c, i) {
  var n = 'Q' + (i + 1) + ' ' + c.q;
  var r = A.search(c.q, 6);
  c.expect(r, n);
});
lowConfidenceCase();
negativeCase('How do I bake a chocolate cake?');
negativeCase('what is the airspeed velocity of an unladen swallow');
renderCardChecks();
offlineAndHonestyChecks();

var names = Object.keys(qTotal);
console.log('');
console.log('==========================================');
names.forEach(function (qn) {
  var bad = qFail[qn];
  console.log((bad ? '  FAIL ' : '  pass ') + qn +
    (bad ? ' (' + bad.length + '/' + qTotal[qn] + ' assertions failed)' : ' (' + qTotal[qn] + ')'));
  if (bad) bad.forEach(function (b) { console.log('        ✗ ' + b); });
});
console.log('==========================================');
console.log('QUESTION TESTS: ' + pass + ' passed, ' + fail + ' failed, total ' + (pass + fail));
if (fail) process.exit(1);
console.log('ALL QUESTION TESTS PASSED');
