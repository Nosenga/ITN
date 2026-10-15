#!/usr/bin/env node
/* ============================================================
   Search regression tests (bot.js + itn-site/corpus.json).
   Run:  node site-build/test-search.js
   Locks in the question-aligned behaviour of the ask box:
   required example queries, honest not-found, and off-topic
   negatives returning zero hits. Exits non-zero on failure.
   ============================================================ */
'use strict';

var path = require('path');

var corpus = require(path.join(__dirname, '..', 'itn-site', 'corpus.json'));
global.window = { __ITN__: { passages: corpus } };
global.document = {
  readyState: 'loading',                 // bot.js registers its init but never runs it
  addEventListener: function () {},
  getElementById: function () { return null; },
  querySelectorAll: function () { return []; },
  querySelector: function () { return null; }
};
require('./bot.js');
var A = global.window.ITNAsk;

var pass = 0, fail = 0, failures = [];
function is(name, ok, detail) {
  if (ok) { pass++; } else { fail++; failures.push(name + (detail ? ' — ' + detail : '')); }
}
function top(r) { return r.hits.length ? r.hits[0].p : null; }

console.log('corpusSize:', A.corpusSize);
is('corpus size 425', A.corpusSize === 425, 'got ' + A.corpusSize);

/* ---------- 1. required example queries (question-aligned tops) ---------- */
var r1 = A.search('What is the purpose of ARP?', 6);
is('ARP: has hits', r1.hits.length >= 1, 'hits=' + r1.hits.length);
is('ARP: top hit is ch5 ARP material', top(r1) && top(r1).c === 5 &&
   /ARP|Address Resolution/i.test((top(r1).t || '') + (top(r1).x || '')),
   top(r1) ? 'ch' + top(r1).c + ' ' + top(r1).t : 'none');
is('ARP: top score strong (>=15)', r1.hits[0].s >= 15, 'score=' + r1.hits[0].s.toFixed(2));

var r2 = A.search('What is a switch port and how does it work?', 6);
is('switch port: has hits', r2.hits.length >= 1);
is('switch port: a top-3 hit is Switch Port material',
   r2.hits.slice(0, 3).some(function (h) { return /switch port/i.test(h.p.t || ''); }),
   r2.hits.slice(0, 3).map(function (h) { return h.p.t; }).join(' | '));

var r3 = A.search('difference between TCP and UDP', 6);
is('TCP-UDP: has hits', r3.hits.length >= 2);
var allText3 = r3.hits.map(function (h) { return ((h.p.t || '') + ' ' + (h.p.x || '')).toLowerCase(); }).join(' ||| ');
is('TCP-UDP: results cover both sides', allText3.indexOf('udp') !== -1 && allText3.indexOf('tcp') !== -1,
   'udp=' + (allText3.indexOf('udp') !== -1) + ' tcp=' + (allText3.indexOf('tcp') !== -1));
is('TCP-UDP: top is transport-layer material (ch7 or TCP/UDP title)',
   top(r3) && (top(r3).c === 7 || /transport|TCP|UDP/i.test(top(r3).t || '')),
   top(r3) ? 'ch' + top(r3).c + ' ' + top(r3).t : '');

var r4 = A.search('how many usable hosts are in a /26 subnet', 6);
is('usable hosts: has hits', r4.hits.length >= 1);
is('usable hosts: top hit ch9 subnetting', top(r4) && top(r4).c === 9,
   top(r4) ? 'ch' + top(r4).c : '');
is('usable hosts: top mentions hosts/subnet', /host|subnet/i.test((top(r4).t || '') + (top(r4).x || '')));

var r5 = A.search('what is the network layer', 6);
is('network layer: has hits', r5.hits.length >= 1);
is('network layer: top hit ch6', top(r5) && top(r5).c === 6, top(r5) ? 'ch' + top(r5).c : '');

/* ---------- 2. honest not-found for public vs private ---------- */
var r6 = A.search('difference between public and private IP addresses', 6);
is('public-vs-private: zero answer hits (honest not-found)', r6.hits.length === 0,
   'hits=' + r6.hits.length);
is('public-vs-private: 3 loose chips offered', (r6.loose || []).length === 3,
   'loose=' + (r6.loose || []).length);
var boxN = { innerHTML: '' };
A.renderResults(boxN, 'difference between public and private IP addresses', r6, {});
is('not-found card: honest wording', /couldn't find a relevant explanation/i.test(boxN.innerHTML));
is('not-found card: no invented-answer claim', !/here is the answer|as an AI/i.test(boxN.innerHTML));
is('not-found card: 3 labeled closest-material chips',
   (boxN.innerHTML.match(/rel-chip/g) || []).length === 3 &&
   /Closest related material/i.test(boxN.innerHTML));

/* ---------- 3. off-topic negatives → zero hits ---------- */
['capital of France', 'quantum chromodynamics', 'who won the world cup in 1998'].forEach(function (q) {
  var rn = A.search(q, 6);
  is('negative "' + q + '" → 0 hits', rn.hits.length === 0, 'hits=' + rn.hits.length);
  is('negative "' + q + '" → 0 loose', (rn.loose || []).length === 0, 'loose=' + rn.loose.length);
});

/* ---------- 4. answer-card render smoke ---------- */
var boxA = { innerHTML: '' };
A.renderResults(boxA, 'What is the purpose of ARP?', r1, {});
is('answer card renders excerpts count', /Found <b>\d+<\/b> excerpts/.test(boxA.innerHTML));
is('answer card has source links', /chapter\d+\.html/.test(boxA.innerHTML));

console.log('');
console.log('==========================================');
console.log('SEARCH TESTS: ' + pass + ' passed, ' + fail + ' failed, total ' + (pass + fail));
if (fail) {
  failures.forEach(function (f) { console.log('  ✗ ' + f); });
  process.exit(1);
} else {
  console.log('ALL SEARCH TESTS PASSED');
}
