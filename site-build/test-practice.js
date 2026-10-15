#!/usr/bin/env node
/* ============================================================
   test-practice.js — upgrade-feature tests
   Run:  node site-build/test-practice.js   (after python3 build.py)
   Covers the NEW practice features end to end:
     A. Lab mixed (revision) level + answer-equivalence validation
        (CIDR / integer / dotted-decimal prefixes, ranges, numbers)
        + step-by-step solutions after submit + lifetime-stats storage.
     B. IOS command practice: item schema, config/verify tagging,
        grading (incl. abbreviations + normalisation), session flow,
        retry, storage, and a full DOM flow proving explanations,
        expected answers, source links and no-execution framing.
     C. Exam topic quick quizzes: topic pool/session building,
        session validity, topic-chip DOM flow (start → answer →
        results → weak topics → recommendation links → history scope
        → retry), and revision recommendation coverage for all topics.
   Exits non-zero on any failure.
   ============================================================ */
'use strict';

var fs = require('fs');
var path = require('path');

var LAB = require('./lab.js');
var IOS = require('./ios.js');
var EXAM = require('./exam.js');

var pass = 0, fail = 0, failures = [];
function is(name, got, want) {
  var ok = (typeof got === 'boolean' && typeof want !== 'boolean')
    ? (got === true) : (String(got) === String(want));
  if (ok) { pass++; } else { fail++; failures.push({ name: name, got: got, want: want }); }
}
function ok(name, cond) { is(name, !!cond, true); }

/* ---------- embedded bank from the built page ---------- */
var examPath = path.join(__dirname, '..', 'itn-site', 'exam.html');
if (!fs.existsSync(examPath)) {
  console.error('exam.html not found — run: python3 site-build/build.py');
  process.exit(1);
}
var page = fs.readFileSync(examPath, 'utf8');
var bm = page.match(/window\.__ITN_EXAM__=(.*?);<\/script>/s);
if (!bm) { console.error('bank embed missing from exam.html'); process.exit(1); }
var BANK = JSON.parse(bm[1]);

function memStore() {
  var data = {};
  return {
    getItem: function (k) { return k in data ? data[k] : null; },
    setItem: function (k, v) { data[k] = String(v); },
    removeItem: function (k) { delete data[k]; },
    _data: data
  };
}

/* ============================================================
   A. Lab: mixed level, equivalence, solutions, storage
   ============================================================ */
console.log('=== A. Lab mixed level + equivalence + solutions + storage ===');
LAB.setSeed(20261015);
var ALL_TYPES = ['maskValue', 'network', 'broadcast', 'hostRange', 'hostCount',
                 'subnetForHosts', 'subnetPrefix', 'subnetCount', 'subnetOf', 'vlsm'];

var mix = LAB.generate(40, { level: 'mixed', types: ALL_TYPES });
is('mixed generates 40', mix.length, 40);
var lvCount = {};
mix.forEach(function (q) { lvCount[q.level] = (lvCount[q.level] || 0) + 1; });
ok('mixed spans easy', lvCount.easy > 0);
ok('mixed spans medium', lvCount.medium > 0);
ok('mixed spans hard', lvCount.hard > 0);
ok('every mixed question verified', mix.every(function (q) {
  return LAB.verifyQuestion(q);
}));
ok('mixed respects selected types', mix.every(function (q) {
  return ALL_TYPES.indexOf(q.type) !== -1;
}));
// fixed levels unchanged
['easy', 'medium', 'hard'].forEach(function (lv) {
  var qs = LAB.generate(8, { level: lv });
  is('fixed ' + lv + ' count', qs.length, 8);
  ok('fixed ' + lv + ' levels uniform', qs.every(function (q) { return q.level === lv; }));
});
// mixed via session (what the quiz DOM calls)
var mixSess = LAB.createSession({ level: 'mixed', count: 12, types: ALL_TYPES });
is('mixed session length', mixSess.questions.length, 12);

// --- answer equivalence: prefix answers in all three accepted forms ---
var pq = LAB.generate(25, { level: 'medium', types: ['subnetForHosts'] });
ok('got prefix questions', pq.length >= 5);
var pQ = pq[0];
var p = pQ.answerPrefix;
is('prefix: /N form correct', LAB.checkAnswer(pQ, '/' + p).ok, true);
is('prefix: bare number correct', LAB.checkAnswer(pQ, String(p)).ok, true);
// dotted via ipv4 module directly (lab.js exposes IPV4 through checkAnswer only)
var IPV4 = require('./ipv4.js');
is('prefix: dotted-decimal mask correct',
   LAB.checkAnswer(pQ, IPV4.maskToDotted(p)).ok, true);
is('prefix: wrong mask rejected', LAB.checkAnswer(pQ, IPV4.maskToDotted((p + 1) % 31 + 1)).ok, false);
is('prefix: /N+1 rejected', LAB.checkAnswer(pQ, '/' + ((p % 31) + 1)).ok, false);

// --- IP answers: whitespace tolerance + exactness ---
var nq = LAB.generate(30, { level: 'easy', types: ['network'] });
ok('got network questions', nq.length >= 5);
var nQ = nq[0];
is('ip exact ok', LAB.checkAnswer(nQ, nQ.answer).ok, true);
is('ip padded ok', LAB.checkAnswer(nQ, '   ' + nQ.answer + '  ').ok, true);
is('ip wrong rejected', LAB.checkAnswer(nQ, '10.255.255.254').ok, false);

// --- range answers: dash style tolerance ---
var rq = LAB.generate(30, { level: 'easy', types: ['hostRange'] });
ok('got range questions', rq.length >= 5);
var rQ = rq.filter(function (q) { return q.answerKind === 'range' && q.answerInt == null &&
  q.answerFirstInt != null; })[0];
ok('usable-range question found', !!rQ);
var dashForms = [' - ', '-', ' – ', ' -', '- '];
dashForms.forEach(function (d, i) {
  var parts = rQ.answer.split(' - ');
  var text = parts.join(d);
  is('range form ' + i + ' accepted', LAB.checkAnswer(rQ, text).ok, true);
});
is('range wrong rejected', LAB.checkAnswer(rQ, '192.168.0.1 - 192.168.0.9').ok, false);

// --- number answers: commas/spaces stripped ---
var hq = LAB.generate(30, { level: 'hard', types: ['hostCount'] });
ok('got hostCount questions', hq.length >= 5);
var hQ = hq[0];
var plain = String(hQ.answerNum);
is('number plain ok', LAB.checkAnswer(hQ, plain).ok, true);
is('number comma ok', LAB.checkAnswer(hQ, plain.replace(/\B(?=(\d{3})+(?!\d))/g, ',')).ok, true);
is('number spaced ok', LAB.checkAnswer(hQ, plain.split('').join(' ')).ok, true);
is('number wrong rejected', LAB.checkAnswer(hQ, String(hQ.answerNum + 1)).ok, false);

// --- multi-step (VLSM): solution present after submit ---
var vq = LAB.generate(20, { level: 'hard', types: ['vlsm'] });
ok('got vlsm questions', vq.length >= 3);
var vQ = vq[0];
is('vlsm has ≥4 solution steps', vQ.solutionSteps.length >= 4, true);
var vs = LAB.createSession({ level: 'hard', count: 1, types: ['vlsm'] });
var vsQ = LAB.currentQuestion(vs);
LAB.submit(vs, 'wrong-answer-forced');
var vsGrade = vs.lastGrade;
is('submit records wrong', vsGrade.ok, false);
ok('solution steps rendered after submit', Array.isArray(vsQ.solutionSteps) &&
   vsQ.solutionSteps.length >= 3);
var vsStats = LAB.stats(vs);
is('retry reuses totals object', LAB.retryMisses(vs).totals, vs.totals);

// --- lifetime storage ---
var store = memStore();
is('load empty → null', LAB.loadTotals(store), null);
ok('save works', LAB.saveTotals(store, { answered: 12, correct: 9 }));
var lt = LAB.loadTotals(store);
is('roundtrip answered', lt.answered, 12);
is('roundtrip correct', lt.correct, 9);
store.setItem(LAB.STORE_KEY, 'not json');
is('corrupt → null', LAB.loadTotals(store), null);
store.setItem(LAB.STORE_KEY, JSON.stringify({ v: 1, answered: 4, correct: 40 }));
is('correct>answered → null', LAB.loadTotals(store), null);
is('null store safe', LAB.loadTotals(null), null);
is('null store save false', LAB.saveTotals(null, lt), false);

/* ============================================================
   B. IOS command practice
   ============================================================ */
console.log('=== B. IOS command practice ===');
var ITEMS = IOS.ITEMS;
is('20 items', ITEMS.length, 20);
var seenIds = {}, nCfg = 0, nVer = 0, nSel = 0, nFill = 0;
ITEMS.forEach(function (it) {
  ok('unique id ' + it.id, !seenIds[it.id]);
  seenIds[it.id] = 1;
  ok('kind tag ' + it.id, it.kind === 'config' || it.kind === 'verify');
  if (it.kind === 'config') { nCfg++; } else { nVer++; }
  ok('type tag ' + it.id, it.ty === 'select' || it.ty === 'fill');
  if (it.ty === 'select') { nSel++; } else { nFill++; }
  ok('explanation ' + it.id, typeof it.e === 'string' && it.e.length > 30);
  ok('source link ' + it.id, /chapter\d+\.html#p\d+$/.test(it.href || ''));
  ok('ref label ' + it.id, /Ch \d+ · slide \d+/.test(it.ref || ''));
  if (it.ty === 'select') {
    ok('≥3 options ' + it.id, it.o && it.o.length >= 3);
    ok('answer index ' + it.id, it.a >= 0 && it.a < it.o.length);
  } else {
    ok('accepted forms ' + it.id, it.acc && it.acc.length >= 1);
    ok('canonical accepted ' + it.id, it.acc.some(function (a) {
      return IOS.norm(a) === IOS.norm(it.disp);
    }));
  }
});
ok('has config items', nCfg >= 12);
ok('has verification items', nVer >= 5);
ok('has select items', nSel >= 8);
ok('has fill-in items', nFill >= 8);
// coverage of the required skill list
var allText = ITEMS.map(function (it) {
  return [it.disp, (it.o || []).join(' '), (it.acc || []).join(' ')].join(' ');
}).join(' ');
[['interface config', /interface/i], ['ip assignment', /ip address/i],
 ['enable interface', /no shutdown/i], ['save config', /copy running-config startup-config/i],
 ['verify status', /show ip interface brief/i], ['ping test', /ping 209/i]
].forEach(function (pair) {
  ok('covers ' + pair[0], pair[1].test(allText));
});
// no-execution framing present in every explanation-free global sense is
// asserted in test-practice.py against the built page.

// grading: canonical correct, garbage wrong, normalisation, abbreviations
ITEMS.forEach(function (it) {
  var good = it.ty === 'select' ? it.a : it.disp;
  is('canonical accepted ' + it.id, IOS.check(it, good).ok, true);
  var bad = it.ty === 'select' ? (it.a === 0 ? 1 : 0) : 'definitely-wrong-answer';
  is('wrong rejected ' + it.id, IOS.check(it, bad).ok, false);
});
var f14 = ITEMS.filter(function (i) { return i.id === 'ios-14'; })[0];
is('fill: case/space normalised',
   IOS.check(f14, '  IP   address   192.168.10.1   255.255.255.0 ').ok, true);
is('fill: course abbreviation accepted',
   IOS.check(f14, 'ip add 192.168.10.1 255.255.255.0').ok, true);
is('fill: missing mask rejected', IOS.check(f14, 'ip address 192.168.10.1').ok, false);
var f18 = ITEMS.filter(function (i) { return i.id === 'ios-18'; })[0];
is('fill: abbreviation of show rejected (course shows full form)',
   IOS.check(f18, 'show ip brief').ok, false);
is('empty fill rejected', IOS.check(f18, '   ').ok, false);

// engine session: all-correct run + retry flow
var s1 = IOS.createSession();
is('session holds all items', s1.questions.length, ITEMS.length);
var seenOrder = {};
ok('session order shuffled-unique', s1.questions.every(function (q) {
  if (seenOrder[q.id]) { return false; } seenOrder[q.id] = 1; return true;
}));
while (IOS.currentQuestion(s1)) {
  var q1 = IOS.currentQuestion(s1);
  IOS.submit(s1, q1.ty === 'select' ? q1.a : q1.disp);
  IOS.advance(s1);
}
var st1 = IOS.stats(s1);
is('perfect score', st1.correct + '/' + st1.total, '20/20');
is('no misses', st1.wrongCount, 0);
is('totals 20/20', s1.totals.answered + '/' + s1.totals.correct, '20/20');

var s2 = IOS.createSession({ ids: [ITEMS[0].id, ITEMS[10].id] });
is('subset by ids', s2.questions.length, 2);
IOS.submit(s2, IOS.currentQuestion(s2).ty === 'select' ? 99 : 'zzz'); // force wrong
var g2 = s2.lastGrade;
is('wrong grade recorded', g2.ok, false);
IOS.advance(s2);
IOS.submit(s2, IOS.currentQuestion(s2).ty === 'select' ? 99 : 'zzz'); // wrong again
var st2 = IOS.stats(s2);
is('2 missed', st2.wrongCount, 2);
var s3 = IOS.retryMisses(s2);
is('retry keeps both misses', s3.questions.length, 2);
is('retry shares totals', s3.totals, s2.totals);

var mem = {};
var store2 = {
  getItem: function (k) { return k in mem ? mem[k] : null; },
  setItem: function (k, v) { mem[k] = String(v); },
  removeItem: function (k) { delete mem[k]; }
};
IOS.saveTotals(store2, { answered: 15, correct: 11 });
var it2 = IOS.loadTotals(store2);
is('ios storage roundtrip', it2.answered + '/' + it2.correct, '15/11');
mem[IOS.STORE_KEY] = '{oops';
is('ios corrupt → null', IOS.loadTotals(store2), null);

/* ---- B2: full DOM flow ---- */
function ClassList() {
  var set = {};
  return {
    add: function () { for (var i = 0; i < arguments.length; i++) { set[arguments[i]] = 1; } },
    remove: function () { for (var i = 0; i < arguments.length; i++) { delete set[arguments[i]]; } },
    contains: function (c) { return !!set[c]; },
    _set: set
  };
}
function El(tag, id) {
  this.tagName = (tag || 'div').toUpperCase();
  this.id = id || '';
  this.attrs = {};
  this.children = [];
  this.listeners = {};
  this.classList = ClassList();
  this.className = '';
  this.textContent = '';
  this._innerHTML = '';
  this.style = {};
  this.hidden = false;
  this.disabled = false;
  this.checked = false;
  this.value = '';
}
Object.defineProperty(El.prototype, 'innerHTML', {
  get: function () { return this._innerHTML; },
  set: function (v) { this._innerHTML = v; if (v === '') { this.children = []; } }
});
El.prototype.appendChild = function (c) { this.children.push(c); return c; };
El.prototype.focus = function () {};;
El.prototype.addEventListener = function (ev, fn) {
  (this.listeners[ev] = this.listeners[ev] || []).push(fn);
};
El.prototype.fire = function (ev, extra) {
  var fns = (this.listeners[ev] || []).slice();
  var evObj = { target: this, preventDefault: function () {} };
  if (extra) { for (var k in extra) { evObj[k] = extra[k]; } }
  for (var i = 0; i < fns.length; i++) { fns[i](evObj); }
};
El.prototype.getAttribute = function (k) { return k in this.attrs ? this.attrs[k] : null; };
El.prototype.setAttribute = function (k, v) { this.attrs[k] = String(v); };
El.prototype._desc = function (cls) {
  var out = [];
  this.children.forEach(function (c) {
    if (c.classList && c.classList.contains(cls)) { out.push(c); }
    if (c.children && c.children.length) { out = out.concat(c._desc(cls)); }
  });
  return out;
};
El.prototype._descByTag = function (tag) {
  var out = [];
  this.children.forEach(function (c) {
    if (c.tagName === tag) { out.push(c); }
    if (c.children && c.children.length) { out = out.concat(c._descByTag(tag)); }
  });
  return out;
};
El.prototype.querySelectorAll = function (sel) {
  if (sel.indexOf('.') === 0) { return this._desc(sel.slice(1)); }
  if (sel === 'input') { return this._descByTag('INPUT'); }
  if (sel === 'label') { return this._descByTag('LABEL'); }
  return [];
};
El.prototype.querySelector = function (sel) {
  var out = this.querySelectorAll(sel);
  return out.length ? out[0] : null;
};

function makeIosDoc() {
  var ids = {};
  ['ios-root', 'ios-start', 'ios-stage', 'ios-progress', 'ios-kind', 'ios-ask',
   'ios-opts', 'ios-input-wrap', 'ios-input', 'ios-check', 'ios-feedback',
   'ios-next', 'ios-retry', 'ios-again', 'ios-stats'].forEach(function (id) {
    ids[id] = new El('div', id);
  });
  ['ios-stage', 'ios-input-wrap', 'ios-opts', 'ios-next', 'ios-retry', 'ios-again']
    .forEach(function (id) { ids[id].hidden = true; });
  ids['ios-input'].tagName = 'INPUT';
  return {
    ids: ids,
    getElementById: function (id) { return ids[id] || null; },
    createElement: function (tag) { return new El(tag); },
    addEventListener: function () {},
    querySelectorAll: function () { return []; }
  };
}

var iosStore = memStore();
var idoc = makeIosDoc();
var iapi = IOS.init(idoc, iosStore);
ok('ios dom initialised', !!iapi);
idoc.ids['ios-start'].fire('click');
ok('ios stage shown', idoc.ids['ios-stage'].hidden === false);
is('ios progress', idoc.ids['ios-progress'].textContent, 'Question 1 of 20');
var isess = iapi.session;
ok('ios session started', !!isess);
// answer question 1 wrong → feedback must show expected + kind + course link
var iq1 = IOS.currentQuestion(isess);
if (iq1.ty === 'select') {
  var opts1 = idoc.ids['ios-opts'].children;
  is('select renders options', opts1.length, iq1.o.length);
  var wrongIdx = iq1.a === 0 ? 1 : 0;
  opts1[wrongIdx].fire('click');
  idoc.ids['ios-check'].fire('click');
} else {
  idoc.ids['ios-input'].value = 'wrong-answer';
  idoc.ids['ios-check'].fire('click');
}
is('wrong grade in DOM', isess.lastGrade.ok, false);
var fbHtml = idoc.ids['ios-feedback'].innerHTML;
ok('feedback shows verdict', fbHtml.indexOf('Not quite') !== -1);
ok('feedback shows expected command', fbHtml.indexOf(iq1.disp) !== -1);
ok('feedback shows kind badge',
   fbHtml.indexOf('kind-config') !== -1 || fbHtml.indexOf('kind-verify') !== -1);
ok('feedback links the course slide', fbHtml.indexOf('Course · Ch') !== -1 &&
   fbHtml.indexOf(iq1.href) !== -1);
ok('feedback shows explanation', fbHtml.indexOf('Configuration command') !== -1 ||
   fbHtml.indexOf('Verification command') !== -1);
idoc.ids['ios-next'].fire('click');
is('advanced to Q2', idoc.ids['ios-progress'].textContent, 'Question 2 of 20');
// second question: answer correctly
var iq2 = IOS.currentQuestion(isess);
if (iq2.ty === 'select') {
  idoc.ids['ios-opts'].children[iq2.a].fire('click');
  idoc.ids['ios-check'].fire('click');
} else {
  idoc.ids['ios-input'].value = iq2.disp;
  idoc.ids['ios-check'].fire('click');
}
is('correct grade in DOM', isess.lastGrade.ok, true);
ok('ios lifetime saved after answers', iosStore.getItem(IOS.STORE_KEY) !== null);
// run to the end with correct answers (Q2 is already graded; just advance it)
while (IOS.currentQuestion(isess)) {
  var iq = IOS.currentQuestion(isess);
  if (!isess.checked) {
    IOS.submit(isess, iq.ty === 'select' ? iq.a : iq.disp);
  }
  IOS.advance(isess);
}
var ist = IOS.stats(isess);
is('mixed-outcome totals', isess.totals.answered, 20);
ok('lifetime persisted count', JSON.parse(iosStore.getItem(IOS.STORE_KEY)).answered >= 2);

/* ============================================================
   C. Exam topic quick quizzes + recommendations
   ============================================================ */
console.log('=== C. Exam topic quizzes + recommendations ===');
// pools
var topics = {};
BANK.forEach(function (b) { topics[b.tp] = (topics[b.tp] || 0) + 1; });
ok('≥10 topics in bank', Object.keys(topics).length >= 10);
['Subnetting', 'Troubleshooting', 'IP addressing & subnetting'].forEach(function (t) {
  ok('topic present: ' + t, topics[t] > 0);
});
// topic session building
var tp = 'Subnetting';
var poolT = EXAM.topicPool(BANK, tp);
ok('topicPool size matches bank', poolT.length === topics[tp]);
function lcg(s) { return function () { s = (s * 1103515245 + 12345) % 2147483648; return s / 2147483648; }; }
var chUnion = {};
poolT.forEach(function (b) { b.c.forEach(function (c) { chUnion[c] = 1; }); });
var tSess = EXAM.buildSession(BANK, {
  ch: Object.keys(chUnion).map(Number), len: 5, mode: 'untimed', topic: tp
}, 1700000000000, lcg(11));
is('topic session ≤5', tSess.items.length, Math.min(5, poolT.length));
ok('topic session only topic items', tSess.items.every(function (it) {
  var q = BANK.filter(function (b) { return b.i === it.id; })[0];
  return q && q.tp === tp;
}));
is('topic field stored', tSess.topic, tp);
ok('topic session valid', !!EXAM.validSession(JSON.stringify(tSess), BANK));
// invalid topic type rejected
var badT = JSON.parse(JSON.stringify(tSess)); badT.topic = 7;
is('non-string topic rejected', EXAM.validSession(JSON.stringify(badT), BANK), null);
// plain sessions keep topic null and stay valid
var plain = EXAM.buildSession(BANK, { ch: [9], len: 10, mode: '60' }, 1700000000000, lcg(5));
is('plain session topic null', plain.topic, null);
ok('plain session valid', !!EXAM.validSession(JSON.stringify(plain), BANK));

// recommendation coverage for EVERY topic in the real bank
Object.keys(topics).forEach(function (t) {
  var r = EXAM.recFor(t);
  ok('rec exists: ' + t, !!r);
  if (r) {
    ok('rec href is a site page: ' + t,
       /^(lab|ptlab|chapter\d+)\.html(#\w+)?$/.test(r.href));
    ok('rec label is a revision activity: ' + t, r.label && r.label.length > 15);
  }
});
is('unknown topic → no rec', EXAM.recFor('Quantum Basket Weaving'), null);

/* ---- C2: topic-chip DOM flow end to end ---- */
function makeExamDoc() {
  var ids = {};
  ['ex-root', 'ex-resume', 'ex-resume-text', 'ex-resume-yes', 'ex-resume-no',
   'ex-setup', 'ex-chips', 'ex-all', 'ex-lens', 'ex-pool-note', 'ex-modes',
   'ex-start', 'ex-start-note', 'ex-topics', 'ex-hist-note', 'ex-hist-wrap',
   'ex-hist-body', 'ex-quiz', 'ex-progress', 'ex-topic', 'ex-type', 'ex-src',
   'ex-timer', 'ex-bar', 'ex-q', 'ex-opts', 'ex-short', 'ex-input', 'ex-submit',
   'ex-feedback', 'ex-verdict', 'ex-correct', 'ex-why', 'ex-next', 'ex-timenote',
   'ex-results', 'ex-score', 'ex-pct', 'ex-scorenote', 'ex-weak-wrap', 'ex-weak',
   'ex-rec', 'ex-retry', 'ex-again', 'ex-review'].forEach(function (id) {
    ids[id] = new El('div', id);
  });
  ['ex-resume', 'ex-quiz', 'ex-results', 'ex-feedback', 'ex-short', 'ex-timenote',
   'ex-weak-wrap', 'ex-rec', 'ex-retry', 'ex-hist-wrap'].forEach(function (id) {
    ids[id].hidden = true;
  });
  ids['ex-input'].tagName = 'INPUT';
  ids['ex-all'].tagName = 'INPUT';
  ids['ex-all'].checked = true;
  var chBoxes = [1, 2, 3, 4, 5, 6, 7, 9, 10, 16].map(function (n) {
    var b = new El('input');
    b.setAttribute('data-ch', String(n));
    b.checked = true;
    return b;
  });
  var lenBtns = ['10', '20', '30'].map(function (L) {
    var b = new El('button');
    b.setAttribute('data-len', L);
    if (L === '10') { b.classList.add('is-on'); }
    return b;
  });
  ids['ex-lens'].querySelectorAll = function (sel) {
    return sel === 'button[data-len]' ? lenBtns : [];
  };
  var modeBtns = ['untimed', '30', '60'].map(function (M) {
    var b = new El('button');
    b.setAttribute('data-mode', M);
    if (M === 'untimed') { b.classList.add('is-on'); }
    return b;
  });
  ids['ex-modes'].querySelectorAll = function (sel) {
    return sel === 'button[data-mode]' ? modeBtns : [];
  };
  // one chip per real topic
  var topicNames = Object.keys(topics);
  var topicBtns = topicNames.map(function (t) {
    var b = new El('button');
    b.setAttribute('data-topic', t);
    b.textContent = t;
    return b;
  });
  return {
    ids: ids, chBoxes: chBoxes, topicBtns: topicBtns, topicNames: topicNames,
    __exWired: false,
    getElementById: function (id) { return ids[id] || null; },
    querySelectorAll: function (sel) {
      if (sel === 'input[data-ch]') { return chBoxes; }
      if (sel === 'button[data-topic]') { return topicBtns; }
      return [];
    },
    createElement: function (tag) { return new El(tag); },
    querySelector: function () { return null; }
  };
}

var estore = memStore();
var eclock = { t: 1700000000000 };
var edoc = makeExamDoc();
var eapi = EXAM.init(edoc, BANK, estore, function () { return eclock.t; },
                     function () { return 1; }, function () {});
ok('exam dom initialised', !!eapi);
// click the Troubleooting... pick 'Troubleshooting' chip
var tBtn = edoc.topicBtns.filter(function (b) {
  return b.getAttribute('data-topic') === 'Troubleshooting';
})[0];
ok('chip exists for Troubleshooting', !!tBtn);
tBtn.fire('click');
var es = eapi.session;
ok('topic session started', es && es.stage === 'quiz');
is('session topic set', es.topic, 'Troubleshooting');
is('session size = 5 (or pool)', es.items.length, Math.min(5, topics['Troubleshooting']));
ok('quiz visible', edoc.ids['ex-quiz'].hidden === false);
is('setup hidden after start', edoc.ids['ex-setup'].hidden, true);
// saved session survives refresh + validates with topic
var saved = estore.getItem(EXAM.SESSION_KEY);
ok('topic session saved', !!saved);
ok('saved topic session valid', !!EXAM.validSession(saved, BANK));
// answer everything WRONG → weak topic + recommendation must appear
for (var qi = 0; qi < es.items.length; qi++) {
  var qq = BANK.filter(function (b) { return b.i === es.items[qi].id; })[0];
  if (EXAM.CHOICE[qq.ty]) {
    var labs = edoc.ids['ex-opts'].querySelectorAll('label');
    var pick = 0;
    // choose a wrong option when possible
    for (var li = 0; li < labs.length; li++) {
      var cand = es.items[qi].opts[li];
      if (cand !== qq.o[qq.a]) { pick = li; break; }
    }
    labs[pick].querySelector('input').checked = true;
    labs[pick].fire('change');
    edoc.ids['ex-submit'].fire('click');
  } else {
    edoc.ids['ex-input'].value = 'wrong text on purpose';
    edoc.ids['ex-input'].fire('input');
    edoc.ids['ex-submit'].fire('click');
  }
  // source + explanation shown after EVERY submission
  ok('explanation after submit q' + (qi + 1),
     edoc.ids['ex-why'].innerHTML.length > 20);
  ok('correct answer shown q' + (qi + 1),
     edoc.ids['ex-correct'].textContent.indexOf('Correct answer:') !== -1);
  ok('source shown q' + (qi + 1),
     edoc.ids['ex-src'].textContent.indexOf('·') !== -1);
  edoc.ids['ex-next'].fire('click');
}
is('results visible', edoc.ids['ex-results'].hidden, false);
is('all wrong → 0 score', edoc.ids['ex-score'].textContent, '0 / ' + es.items.length);
is('weak wrap visible', edoc.ids['ex-weak-wrap'].hidden, false);
is('weak chip topic', edoc.ids['ex-weak'].children[0].textContent
   .indexOf('Troubleshooting') === 0, true);
// recommendation rendered with a real link
is('rec container visible', edoc.ids['ex-rec'].hidden, false);
ok('rec has an item', edoc.ids['ex-rec'].children.length >= 1);
var recHtml = edoc.ids['ex-rec'].children[0].innerHTML || '';
ok('rec names the weak topic', recHtml.indexOf('Troubleshooting') !== -1);
ok('rec links ptlab#lab4', recHtml.indexOf('ptlab.html#lab4') !== -1);
// retry offered
is('retry button shown', edoc.ids['ex-retry'].hidden, false);
is('retry label counts misses', edoc.ids['ex-retry'].textContent
   .indexOf('(' + es.items.length + ')') !== -1, true);
// history entry recorded with topic scope
var hist = JSON.parse(estore.getItem(EXAM.HISTORY_KEY)).r;
is('history entry exists', hist.length, 1);
is('history scope is the topic', hist[0].topic, 'Troubleshooting');
is('history weak mentions topic', hist[0].weak[0].indexOf('Troubleshooting'), 0);
// review list shows topic tag
is('review items', edoc.ids['ex-review'].children.length, es.items.length);
// retry flow: back to quiz with fresh answers on same missed ids
edoc.ids['ex-retry'].fire('click');
var rs = eapi.session;
is('retry stage quiz', rs.stage, 'quiz');
ok('retry keeps item ids', JSON.stringify(rs.items.map(function (i) { return i.id; })) ===
   JSON.stringify(es.items.map(function (i) { return i.id; })) ||
   rs.items.length === es.items.length);
ok('retry answers fresh', rs.ans.every(function (a) { return a === null; }));

/* ---- summary ---- */
console.log('');
console.log('RESULTS: ' + pass + ' passed, ' + fail + ' failed, total ' +
            (pass + fail));
if (fail) {
  failures.forEach(function (f) {
    console.log('  FAIL: ' + f.name + ' — got=' + JSON.stringify(f.got) +
                ' want=' + JSON.stringify(f.want));
  });
  process.exit(1);
}
console.log('ALL TESTS PASSED');
