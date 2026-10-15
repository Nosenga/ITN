#!/usr/bin/env node
/* ============================================================
   Unit + flow tests for exam.js
   Run:  node site-build/test-exam.js        (after python3 build.py)
   Covers: answer validation, scoring, weak-topic analysis,
   timer behaviour, session save/restore integrity (refresh
   safety), history tracking, and a full DOM flow proving
   answers stay hidden until submit.
   Exits non-zero on any failure.
   ============================================================ */
'use strict';

var fs = require('fs');
var path = require('path');
var EXAM = require('./exam.js');

/* ---------- load the embedded bank from the built page ---------- */
var examPath = path.join(__dirname, '..', 'itn-site', 'exam.html');
if (!fs.existsSync(examPath)) {
  console.error('exam.html not found — run: python3 site-build/build.py');
  process.exit(1);
}
var page = fs.readFileSync(examPath, 'utf8');
var m = page.match(/window\.__ITN_EXAM__=(.*?);<\/script>/s);
if (!m) {
  console.error('bank embed missing from exam.html');
  process.exit(1);
}
var BANK = JSON.parse(m[1]);

var pass = 0, fail = 0, failures = [];
// is(name, got, want): string equality — EXCEPT the informational pattern
// is(name, BOOLEAN_CONDITION, REFERENCE) which passes when the condition is
// true (the reference value is only reported on failure).
function is(name, got, want) {
  var ok = (typeof got === 'boolean' && typeof want !== 'boolean')
    ? (got === true) : (String(got) === String(want));
  if (ok) { pass++; } else { fail++; failures.push({ name: name, got: got, want: want }); }
}
function ok(name, cond) { is(name, !!cond, true); }

/* deterministic rng for shuffle tests */
function lcg(seed) {
  var s = seed >>> 0;
  return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
}
function chans() { return Array.prototype.slice.call(arguments); }

console.log('=== A. bank sanity ===');
is('bank loaded', BANK.length >= 120, BANK.length);
var types = {};
BANK.forEach(function (b) { types[b.ty] = (types[b.ty] || 0) + 1; });
['mc', 'tf', 'short', 'term', 'calc', 'trouble'].forEach(function (t) {
  is('type present: ' + t, types[t] >= 1, types[t]);
});
var minPool = 99;
[1, 2, 3, 4, 5, 6, 7, 9, 10, 16].forEach(function (n) {
  var c = BANK.filter(function (b) { return b.c.indexOf(n) !== -1; }).length;
  if (c < minPool) { minPool = c; }
});
is('every chapter pool >= 10', minPool >= 10, minPool);

console.log('=== B. answer validation ===');
// normalize
is('unicode minus', EXAM.normalize('\u22122'), '-2');
is('case + spaces', EXAM.normalize('  THE  Software '), 'the software');
is('strips !?;"', EXAM.normalize('yes!'), 'yes');
// num grading
var qNum = { gr: { num: 30 } };
is('num plain', EXAM.grade(qNum, '30'), true);
is('num with word', EXAM.grade(qNum, '30 hosts'), true);
is('num spaced', EXAM.grade(qNum, '  30. '), true);
is('num wrong', EXAM.grade(qNum, '31'), false);
is('num junk', EXAM.grade(qNum, 'thirty'), false);
var qNumNeg = { gr: { num: 2 } };
is('num small', EXAM.grade(qNumNeg, '2'), true);
// acc grading
var qAcc = { gr: { acc: ['192.168.10.64'] } };
is('acc exact', EXAM.grade(qAcc, '192.168.10.64'), true);
is('acc in sentence', EXAM.grade(qAcc, 'the network is 192.168.10.64'), true);
is('acc wrong', EXAM.grade(qAcc, '192.168.10.32'), false);
var qAccShort = { gr: { acc: ['/28', '28'] } };
is('acc len2 equality', EXAM.grade(qAccShort, '28'), true);
is('acc len2 no fuzzy', EXAM.grade(qAccShort, '288'), false);
is('acc slash form', EXAM.grade(qAccShort, '/28'), true);
// must grading
var qMust = { gr: { must: ['software', 'flash'] } };
is('must both', EXAM.grade(qMust, 'software runs from flash'), true);
is('must missing one', EXAM.grade(qMust, 'software only'), false);
// groups grading
var qG = { gr: { g: [['fault tolerance'], ['scalab'], ['quality of service', 'qos'],
                     ['security']], n: 4 } };
is('groups all four', EXAM.grade(qG,
  'Fault tolerance, scalability, QoS and security'), true);
is('groups alias long', EXAM.grade(qG,
  'fault tolerance, scalability, quality of service, security'), true);
is('groups n-1 fails', EXAM.grade(qG, 'fault tolerance, scalability, security'), false);
var qPort = { gr: { g: [['25'], ['110'], ['send', 'transfer'], ['retriev']], n: 4 } };
is('short alias token', EXAM.grade(qPort, 'SMTP port 25 sends, POP port 110 retrieves'),
   true);
is('short alias miss', EXAM.grade(qPort, 'SMTP port 25 sends'), false);
// choice grading
is('choice right', EXAM.gradeChoice({ a: 2 }, 2), true);
is('choice wrong', EXAM.gradeChoice({ a: 2 }, 1), false);

console.log('=== C. buildSession: shuffle + materialization ===');
var cfg = { ch: [1, 2, 3, 4, 5, 6, 7, 9, 10, 16], len: 20, mode: 'untimed' };
var sess = EXAM.buildSession(BANK, cfg, 1700000000000, lcg(7));
is('session length', sess.items.length, 20);
is('stage quiz', sess.stage, 'quiz');
is('answers preallocated', sess.ans.length, 20);
is('all null answers', sess.ans.every(function (a) { return a === null; }), true);
is('no endTs untimed', sess.endTs, null);
// ids unique
var idset = {};
ok('ids unique', sess.items.every(function (it) {
  if (idset[it.id]) { return false; } idset[it.id] = 1; return true;
}));
// materialized options faithful
var byId = {};
BANK.forEach(function (b) { byId[b.i] = b; });
var permOk = true, tfFixed = true, choiceCount = 0;
sess.items.forEach(function (it) {
  var q = byId[it.id];
  if (q.ty === 'mc' || q.ty === 'term' || q.ty === 'trouble') {
    choiceCount++;
    var a = it.opts.slice().sort().join('|');
    var b = q.o.slice().sort().join('|');
    if (a !== b) { permOk = false; }
    if (it.opts[it.correct] !== q.o[q.a]) { permOk = false; }
    if (it.opts.length !== q.o.length) { permOk = false; }
  } else if (q.ty === 'tf') {
    if (it.opts.join(',') !== 'True,False') { tfFixed = false; }
    if (it.correct !== q.a) { tfFixed = false; }
  }
});
ok('mc/term/trouble options permuted faithfully', permOk);
ok('tf never shuffled', tfFixed);
ok('session contains choice items', choiceCount > 0);
// timed session endTs
var tsess = EXAM.buildSession(BANK, { ch: [9], len: 10, mode: '30' },
  1700000000000, lcg(3));
is('timed endTs', tsess.endTs, 1700000000000 + 10 * 30 * 1000);
// pool + lengths
is('pool all', EXAM.poolFor(BANK, [1, 2, 3, 4, 5, 6, 7, 9, 10, 16]).length,
   BANK.length);
is('pool ch9 >= 20', EXAM.poolFor(BANK, [9]).length >= 20, true);
is('lengths small pool', EXAM.lengthsAvailable(11).join(','), '10');
is('lengths mid pool', EXAM.lengthsAvailable(25).join(','), '10,20');
is('lengths big pool', EXAM.lengthsAvailable(140).join(','), '10,20,30');
is('lengths none', EXAM.lengthsAvailable(5).length, 0);

console.log('=== D. scoring, weak topics, retry ===');
// build a synthetic scored session over known questions
var fake = {
  items: [
    { id: BANK[0].i }, { id: BANK[1].i }, { id: BANK[2].i }
  ],
  ans: [{ ok: true }, { ok: false }, { ok: false }]
};
// force topics for determinism
var save0 = BANK[0].tp, save1 = BANK[1].tp, save2 = BANK[2].tp;
BANK[0].tp = 'Alpha'; BANK[1].tp = 'Beta'; BANK[2].tp = 'Beta';
var sc = EXAM.scoreSession(fake);
is('score 1/3', sc.correct + '/' + sc.total, '1/3');
is('pct rounded', sc.pct, 33);
var weak = EXAM.weakTopics(BANK, fake, 3);
is('weak top topic', weak[0].tp, 'Beta');
is('weak miss count', weak[0].wrong + '/' + weak[0].total, '2/2');
is('weak list length', weak.length, 1); // Alpha (wrong=0) excluded
is('retry ids', EXAM.retryIds(fake).join(','), BANK[1].i + ',' + BANK[2].i);
var perfect = { items: fake.items, ans: [{ ok: true }, { ok: true }, { ok: true }] };
is('perfect pct', EXAM.scoreSession(perfect).pct, 100);
is('perfect weak none', EXAM.weakTopics(BANK, perfect).length, 0);
is('perfect retry none', EXAM.retryIds(perfect).length, 0);
var zero = { items: fake.items, ans: [{ ok: false }, { ok: false }, { ok: false }] };
is('zero pct', EXAM.scoreSession(zero).pct, 0);
// missed-by-none topic excluded
BANK[0].tp = save0; BANK[1].tp = save1; BANK[2].tp = save2;

console.log('=== E. timer behaviour ===');
is('untimed null', EXAM.remainingSec(null, 1000), null);
is('future', EXAM.remainingSec(60000, 15000), 45);
is('exact boundary', EXAM.remainingSec(15000, 15000), 0);
is('past clamped', EXAM.remainingSec(1000, 99999), 0);
is('near boundary ceil', EXAM.remainingSec(10000, 9001), 1);

console.log('=== F. history tracking ===');
var h1 = EXAM.pushHistory(null, { pct: 80, correct: 16, total: 20 });
var p1 = JSON.parse(h1);
is('history starts clean', p1.v, EXAM.V);
is('first entry on top', p1.r[0].pct, 80);
var h2 = EXAM.pushHistory(h1, { pct: 90, correct: 18, total: 20 });
var p2 = JSON.parse(h2);
is('newest first', p2.r[0].pct, 90);
is('history length', p2.r.length, 2);
// corrupt history → fresh, not throw
var h3 = EXAM.pushHistory('{corrupt!!', { pct: 50 });
is('corrupt history reset', JSON.parse(h3).r.length, 1);
// cap at 20
var raw = null;
for (var hi = 0; hi < 30; hi++) { raw = EXAM.pushHistory(raw, { pct: hi }); }
is('history capped', JSON.parse(raw).r.length, 20);
is('history keeps newest', JSON.parse(raw).r[0].pct, 29);

console.log('=== G. session save/restore (refresh safety) ===');
var good = JSON.stringify(sess);
var restored = EXAM.validSession(good, BANK);
ok('roundtrip valid', !!restored);
is('restored stage', restored.stage, 'quiz');
is('restored idx', restored.i, 0);
is('restored len', restored.items.length, 20);
function mutant(fn) {
  var o = JSON.parse(good); fn(o); return EXAM.validSession(JSON.stringify(o), BANK);
}
ok('null on bad json', EXAM.validSession('nonsense{', BANK) === null);
ok('null on wrong version', mutant(function (o) { o.v = 99; }) === null);
ok('null on bad stage', mutant(function (o) { o.stage = 'running'; }) === null);
ok('null on bad mode', mutant(function (o) { o.mode = '99'; }) === null);
ok('null on empty ch', mutant(function (o) { o.ch = []; }) === null);
ok('null on missing item id', mutant(function (o) { o.items[0].id = 'nope-999'; }) === null);
ok('null on ans length', mutant(function (o) { o.ans.pop(); }) === null);
ok('null on idx out of range', mutant(function (o) { o.i = 999; }) === null);
ok('null on endTs type', mutant(function (o) { o.endTs = 'soon'; }) === null);
ok('null on draft missing', mutant(function (o) { delete o.draft; }) === null);
ok('null on opts not permutation',
   mutant(function (o) {
     var it = o.items.filter(function (x) { return x.opts && x.opts.length > 1; })[0];
     it.opts[0] = 'corrupted option text';
   }) === null);
ok('null on correct pointing to wrong text',
   mutant(function (o) {
     var it = o.items.filter(function (x) { return x.opts; })[0];
     it.correct = (it.correct + 1) % it.opts.length;   // may coincide? force:
     var q = byId[it.id];
     if (it.opts[it.correct] === q.o[q.a]) { it.correct = (it.correct + 1) % it.opts.length; }
   }) === null);
// answering mid-session then restoring keeps the answers
sess.ans[0] = { ok: true, picked: 0 };
sess.i = 1;
var restored2 = EXAM.validSession(JSON.stringify(sess), BANK);
ok('answered session valid', !!restored2);
is('answers preserved', restored2.ans[0].ok, true);
is('index preserved', restored2.i, 1);
// results stage with history-saved flag
var res = JSON.parse(JSON.stringify(sess));
res.stage = 'results'; res.saved = true;
ok('results stage valid', !!EXAM.validSession(JSON.stringify(res), BANK));

console.log('=== H. DOM flow with a stubbed document ===');

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
El.prototype.addEventListener = function (ev, fn) {
  (this.listeners[ev] = this.listeners[ev] || []).push(fn);
};
El.prototype.fire = function (ev) {
  var fns = (this.listeners[ev] || []).slice();
  var on = this['on' + ev];
  if (typeof on === 'function') { fns.push(on); }
  for (var i = 0; i < fns.length; i++) { fns[i]({ target: this }); }
};
El.prototype.getAttribute = function (k) {
  return k in this.attrs ? this.attrs[k] : null;
};
El.prototype.setAttribute = function (k, v) { this.attrs[k] = String(v); };
El.prototype._descInputs = function () {
  var out = [];
  this.children.forEach(function (c) {
    if (c.tagName === 'INPUT') { out.push(c); }
    if (c.children && c.children.length) { out = out.concat(c._descInputs()); }
  });
  return out;
};
El.prototype.querySelectorAll = function (sel) {
  if (sel === 'input') { return this._descInputs(); }
  if (sel === 'label') { return this.children.filter(function (c) { return c.tagName === 'LABEL'; }); }
  return [];
};
El.prototype.querySelector = function (sel) {
  if (sel === 'input') {
    var ins = this._descInputs();
    return ins.length ? ins[0] : null;
  }
  return null;
};

function makeDoc() {
  var ids = {};
  ['ex-root', 'ex-resume', 'ex-resume-text', 'ex-resume-yes', 'ex-resume-no',
   'ex-setup', 'ex-chips', 'ex-all', 'ex-lens', 'ex-pool-note', 'ex-modes',
   'ex-start', 'ex-start-note', 'ex-hist-note', 'ex-hist-wrap', 'ex-hist-body',
   'ex-quiz', 'ex-progress', 'ex-topic', 'ex-type', 'ex-src', 'ex-timer',
   'ex-bar', 'ex-q', 'ex-opts', 'ex-short', 'ex-input', 'ex-submit',
   'ex-feedback', 'ex-verdict', 'ex-correct', 'ex-why', 'ex-next', 'ex-timenote',
   'ex-results', 'ex-score', 'ex-pct', 'ex-scorenote', 'ex-weak-wrap', 'ex-weak',
   'ex-retry', 'ex-again', 'ex-review'].forEach(function (id) {
    ids[id] = new El('div', id);
  });
  // default hidden states (mirroring exam.html markup)
  ['ex-resume', 'ex-quiz', 'ex-results', 'ex-feedback', 'ex-short',
   'ex-timenote', 'ex-weak-wrap', 'ex-retry', 'ex-hist-wrap'].forEach(function (id) {
    ids[id].hidden = true;
  });
  // structure helpers
  ids['ex-input'].tagName = 'INPUT';
  ids['ex-all'].tagName = 'INPUT';
  ids['ex-all'].checked = true;
  // chapter checkboxes
  var chapters = [1, 2, 3, 4, 5, 6, 7, 9, 10, 16];
  var chBoxes = chapters.map(function (n) {
    var b = new El('input');
    b.setAttribute('data-ch', String(n));
    b.checked = true;
    return b;
  });
  // length buttons
  var lenBtns = ['10', '20', '30'].map(function (L) {
    var b = new El('button');
    b.setAttribute('data-len', L);
    b.classList.add(L === '10' ? 'is-on' : '');
    b.classList.remove('');
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
  var doc = {
    ids: ids, chBoxes: chBoxes, lenBtns: lenBtns, modeBtns: modeBtns,
    __exWired: false,
    getElementById: function (id) { return ids[id] || null; },
    querySelectorAll: function (sel) {
      if (sel === 'input[data-ch]') { return chBoxes; }
      return [];
    },
    createElement: function (tag) { return new El(tag); },
    querySelector: function () { return null; }
  };
  return doc;
}
function memStore() {
  var data = {};
  return {
    getItem: function (k) { return k in data ? data[k] : null; },
    setItem: function (k, v) { data[k] = String(v); },
    removeItem: function (k) { delete data[k]; },
    _data: data
  };
}

var store = memStore();
var clock = { t: 1700000000000 };
var intervalFn = function () { return 1; };   // no real timers in tests
var clearFn = function () {};
var doc = makeDoc();
var api = EXAM.init(doc, BANK, store, function () { return clock.t; },
                    intervalFn, clearFn);

// setup visible, quiz/results hidden
is('setup visible', doc.ids['ex-setup'].hidden, false);
is('quiz hidden', doc.ids['ex-quiz'].hidden, true);
is('results hidden', doc.ids['ex-results'].hidden, true);
is('no resume banner (empty store)', doc.ids['ex-resume'].hidden, true);

// select only chapter 9
doc.chBoxes.forEach(function (b) {
  b.checked = b.getAttribute('data-ch') === '9';
});
doc.ids['ex-all'].checked = false;
doc.chBoxes.forEach(function (b) { b.fire('change'); });
ok('pool note mentions ch9 pool', /questions available for 1 chapter/.test(
   doc.ids['ex-pool-note'].textContent));
var pool9 = EXAM.poolFor(BANK, [9]).length;
is('pool count correct', doc.ids['ex-pool-note'].textContent.indexOf(
   pool9 + ' questions available') === 0, true);
is('10 enabled', doc.lenBtns[0].disabled, false);
is('20 enabled', doc.lenBtns[1].disabled, false);
is('30 state follows pool', doc.lenBtns[2].disabled, pool9 < 30);

// start
doc.ids['ex-start'].fire('click');
var s = api.session;
is('session started', s && s.stage, 'quiz');
is('quiz visible', doc.ids['ex-quiz'].hidden, false);
is('progress Q1', doc.ids['ex-progress'].textContent, 'Q 1 / ' + s.items.length);
is('untimed timer label', doc.ids['ex-timer'].textContent, 'Untimed');

// answer every question; first Q check the reveal rule
for (var qi = 0; qi < s.items.length; qi++) {
  var qIdx = s.i;
  var q = BANK.filter(function (b) { return b.i === s.items[qIdx].id; })[0];
  if (qi === 0) {
    is('feedback hidden before submit', doc.ids['ex-feedback'].hidden, true);
    is('submit visible', doc.ids['ex-submit'].hidden, false);
  }
  if (EXAM.CHOICE[q.ty]) {
    var labels = doc.ids['ex-opts'].querySelectorAll('label');
    is('option count matches item', labels.length, s.items[qIdx].opts.length);
    var pick = 0;                          // sometimes right, sometimes wrong
    var inp = labels[pick].querySelector('input');
    inp.checked = true;
    labels[pick].fire('change');
    is('submit enabled after pick', doc.ids['ex-submit'].disabled, false);
  } else {
    doc.ids['ex-input'].value = 'sample answer ' + qi;
    doc.ids['ex-input'].fire('input');
    is('submit enabled after typing', doc.ids['ex-submit'].disabled, false);
  }
  doc.ids['ex-submit'].fire('click');
  if (qi === 0) {
    is('feedback shown after submit', doc.ids['ex-feedback'].hidden, false);
    var v = doc.ids['ex-verdict'].textContent;
    ok('verdict is ✓ or ✗', v.indexOf('Correct') !== -1 || v.indexOf('Incorrect') !== -1);
    ok('explanation revealed', doc.ids['ex-why'].innerHTML.length > 10);
    is('submit hidden after submit', doc.ids['ex-submit'].hidden, true);
  }
  ok('answer recorded', s.ans[qIdx] && typeof s.ans[qIdx].ok === 'boolean');
  // mid-session persistence integrity (refresh simulation)
  if (qi === 1) {
    var mid = store.getItem(EXAM.SESSION_KEY);
    var midOk = EXAM.validSession(mid, BANK);
    ok('mid-session save valid', !!midOk);
    is('mid-session index', midOk.i, s.i);
    is('mid-session answered count',
       midOk.ans.filter(function (a) { return a !== null; }).length,
       s.ans.filter(function (a) { return a !== null; }).length);
  }
  doc.ids['ex-next'].fire('click');
}

// results
is('results visible', doc.ids['ex-results'].hidden, false);
var finalScore = EXAM.scoreSession(s);
is('score text', doc.ids['ex-score'].textContent,
   finalScore.correct + ' / ' + finalScore.total);
is('pct text', doc.ids['ex-pct'].textContent, finalScore.pct + '%');
var histRaw = store.getItem(EXAM.HISTORY_KEY);
var hist = JSON.parse(histRaw).r;
is('history has 1 entry', hist.length, 1);
is('history entry score', hist[0].correct, finalScore.correct);
// weak topics or none
if (finalScore.correct < finalScore.total) {
  is('weak list shown', doc.ids['ex-weak-wrap'].hidden, false);
  is('retry button shown', doc.ids['ex-retry'].hidden, false);
} else {
  is('retry hidden when perfect', doc.ids['ex-retry'].hidden, true);
}
ok('review list populated', doc.ids['ex-review'].children.length === s.items.length);

// refresh at results: new doc, same store → resume banner, no history duplication
var doc2 = makeDoc();
var api2 = EXAM.init(doc2, BANK, store, function () { return clock.t; },
                     intervalFn, clearFn);
is('resume banner shown', doc2.ids['ex-resume'].hidden, false);
ok('resume text mentions finished session',
   /finished session/.test(doc2.ids['ex-resume-text'].textContent));
doc2.ids['ex-resume-yes'].fire('click');
is('results restored', doc2.ids['ex-results'].hidden, false);
var hist2 = JSON.parse(store.getItem(EXAM.HISTORY_KEY)).r;
is('no duplicate history on resume', hist2.length, 1);

// refresh mid-quiz: resume continues at the same index with state intact
var store2 = memStore();
var doc3 = makeDoc();
var api3 = EXAM.init(doc3, BANK, store2, function () { return clock.t; },
                     intervalFn, clearFn);
doc3.chBoxes.forEach(function (b) { b.checked = false; });
doc3.chBoxes.forEach(function (b) {
  if (b.getAttribute('data-ch') === '9') { b.checked = true; }
});
doc3.chBoxes.forEach(function (b) { b.fire('change'); });
doc3.ids['ex-start'].fire('click');
var s3 = api3.session;
// answer Q1 only
var firstQ = BANK.filter(function (b) { return b.i === s3.items[0].id; })[0];
if (EXAM.CHOICE[firstQ.ty]) {
  var l0 = doc3.ids['ex-opts'].querySelectorAll('label')[0];
  l0.querySelector('input').checked = true;
  l0.fire('change');
} else {
  doc3.ids['ex-input'].value = 'persist me';
  doc3.ids['ex-input'].fire('input');
}
doc3.ids['ex-submit'].fire('click');
var savedMid = store2.getItem(EXAM.SESSION_KEY);
var doc4 = makeDoc();
var api4 = EXAM.init(doc4, BANK, store2, function () { return clock.t; },
                     intervalFn, clearFn);
is('resume banner mid-quiz', doc4.ids['ex-resume'].hidden, false);
doc4.ids['ex-resume-yes'].fire('click');
is('quiz restored visible', doc4.ids['ex-quiz'].hidden, false);
is('restored at Q1', doc4.ids['ex-progress'].textContent, 'Q 1 / ' + s3.items.length);
is('submitted state revealed on resume', doc4.ids['ex-feedback'].hidden, false);
is('answer survived refresh', api4.session.ans[0].ok,
   JSON.parse(savedMid).ans[0].ok);

// damaged session → discarded with notice (never silent)
var store3 = memStore();
store3.setItem(EXAM.SESSION_KEY, '{half-corrupt');
var doc5 = makeDoc();
EXAM.init(doc5, BANK, store3, function () { return clock.t; },
          intervalFn, clearFn);
is('corrupt banner shown', doc5.ids['ex-resume'].hidden, false);
ok('corrupt notice text',
   /discarded/.test(doc5.ids['ex-resume-text'].textContent));
is('corrupt session removed from storage', store3.getItem(EXAM.SESSION_KEY), null);
is('resume-yes hidden for corrupt', doc5.ids['ex-resume-yes'].hidden, true);

// timed expiry: give a live quiz session a past deadline → tick finishes it
var store4 = memStore();
var doc6 = makeDoc();
var api6 = EXAM.init(doc6, BANK, store4, function () { return clock.t; },
                     intervalFn, clearFn);
doc6.ids['ex-start'].fire('click');            // all chapters, length 10
var s6 = api6.session;
s6.mode = '30';
s6.endTs = clock.t + 5 * 1000;                 // 5 s left
api6.tick(clock.t);
is('timer shows 00:05', doc6.ids['ex-timer'].textContent, '⏱ 00:05');
is('still in quiz', s6.stage, 'quiz');
api6.tick(clock.t + 6000);                     // deadline passed
is('expired → results', doc6.ids['ex-results'].hidden, false);
is('expiry note shown', doc6.ids['ex-timenote'].hidden, false);
is('scorenote mentions timer',
   /timer expired/.test(doc6.ids['ex-scorenote'].textContent), true);
ok('expiry history entry flagged auto',
   JSON.parse(store4.getItem(EXAM.HISTORY_KEY)).r[0].auto === true);
// unanswered questions count as wrong
var sc6 = EXAM.scoreSession(s6);
is('expiry scoring totals', sc6.total, 10);
is('expiry pct range', sc6.pct >= 0 && sc6.pct <= 100, true);

// retry-incorrect builds an untimed session of only the wrong ids
var store5 = memStore();
var doc7 = makeDoc();
var api7 = EXAM.init(doc7, BANK, store5, function () { return clock.t; },
                     intervalFn, clearFn);
doc7.ids['ex-start'].fire('click');
var s7 = api7.session;
// force wrong answers on first three, finish quickly
for (var k7 = 0; k7 < 3; k7++) {
  s7.ans[k7] = { ok: false, picked: -1, given: 'x' };
}
s7.i = s7.items.length - 1;
s7.stage = 'quiz';
doc7.ids['ex-next'].fire('click');             // finishes (last question)
is('retry visible', doc7.ids['ex-retry'].hidden, false);
doc7.ids['ex-retry'].fire('click');
var r = api7.session;
is('retry stage', r.stage, 'quiz');
is('retry only wrong items', r.items.length, 3);
is('retry untimed', r.endTs, null);
is('retry index reset', r.i, 0);
is('retry answers fresh', r.ans.every(function (a) { return a === null; }), true);

console.log('==========================================');
console.log('RESULTS: ' + pass + ' passed, ' + fail + ' failed, total ' + (pass + fail));
if (fail) {
  failures.forEach(function (f) {
    console.log('  ✗ ' + f.name + ': got=' + f.got + ' want=' + f.want);
  });
  process.exit(1);
}
console.log('ALL EXAM JS TESTS PASSED');
