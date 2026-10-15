#!/usr/bin/env node
/* ============================================================
   Unit tests for pt.js (checklist persistence + quiz grading)
   Run:  node site-build/test-pt.js
   Exits non-zero if any check fails.
   ============================================================ */
'use strict';

var PT = require('./pt.js');

var pass = 0, fail = 0, failures = [];
function is(name, got, want) {
  var ok = String(got) === String(want);
  if (ok) { pass++; } else { fail++; failures.push({ name: name, got: got, want: want }); }
}
function ok(name, cond) { is(name, !!cond, true); }

console.log('=== A. pure state helpers ===');
is('readState(null)', JSON.stringify(PT.readState(null)), '{}');
is('readState(undefined)', JSON.stringify(PT.readState(undefined)), '{}');
is('readState(bad json)', JSON.stringify(PT.readState('{oops')), '{}');
is('readState(array)', JSON.stringify(PT.readState('[1,2]')), '{}');
is('readState(string)', JSON.stringify(PT.readState('"x"')), '{}');
is('readState drops non-true', JSON.stringify(PT.readState('{"a":true,"b":0,"c":"y"}')),
   '{"a":true}');
is('writeState sorted', PT.writeState({ 'lab2-1': true, 'lab1-1': true, 'zz': false }),
   '{"lab1-1":true,"lab2-1":true}');
is('roundtrip', JSON.stringify(PT.readState(PT.writeState({ 'lab1-3': true }))),
   '{"lab1-3":true}');

var s1 = PT.toggle({}, 'lab1-1');
is('toggle adds', s1['lab1-1'], true);
var s2 = PT.toggle(s1, 'lab1-1');
is('toggle removes', s1['lab1-1'], true);          // original untouched
is('toggle removed key', 'lab1-1' in s2, false);
var s3 = PT.toggle(PT.toggle({ 'lab1-1': true }, 'lab2-1'), 'lab1-1');
is('clearPrefix keeps other labs', JSON.stringify(PT.clearPrefix(s3, 'lab1')),
   '{"lab2-1":true}');

is('progress empty', JSON.stringify(PT.progress({}, ['a', 'b', 'c', 'd'])),
   '{"done":0,"total":4,"pct":0}');
is('progress partial', JSON.stringify(PT.progress({ a: true, b: true }, ['a', 'b', 'c'])),
   '{"done":2,"total":3,"pct":67}');
is('progress full', JSON.stringify(PT.progress({ a: true }, ['a'])),
   '{"done":1,"total":1,"pct":100}');

console.log('=== B. gradeQuiz ===');
var qs = [{ correct: 2 }, { correct: 0 }, { correct: 1 }];
var r = PT.gradeQuiz(qs, [2, 0, 1]);
is('all correct', r.score + '/' + r.total, '3/3');
r = PT.gradeQuiz(qs, [0, 1, 1]);
is('two wrong', r.score, 1);
r = PT.gradeQuiz(qs, [-1, -1, -1]);
is('unanswered = wrong', r.score, 0);
is('results shape', r.results.length + ':' + r.results[0].ok + ':' + r.results[0].correct,
   '3:false:2');
r = PT.gradeQuiz([{ correct: 0 }], []);
is('missing answer tolerated', r.score + '/' + r.total, '0/1');

console.log('=== C. DOM wiring with a stubbed root ===');

function El(attrs) {
  this.attrs = attrs || {};
  this.listeners = {};
  this.checked = false;
  this.style = {};
  this.textContent = '';
  this.hidden = false;
  this.classList = (function (self) {
    var set = {};
    return {
      add: function (c) { set[c] = 1; self._cls = set; },
      remove: function (c) { delete set[c]; },
      has: function (c) { return !!set[c]; },
      set: set
    };
  })(this);
}
El.prototype.getAttribute = function (k) {
  return Object.prototype.hasOwnProperty.call(this.attrs, k) ? this.attrs[k] : null;
};
El.prototype.addEventListener = function (ev, fn) {
  (this.listeners[ev] = this.listeners[ev] || []).push(fn);
};
El.prototype.fire = function (ev) {
  var fns = this.listeners[ev] || [];
  for (var i = 0; i < fns.length; i++) { fns[i](); }
};
El.prototype.closest = function (sel) {
  return (sel === 'label' && this._label) ? this._label : null;
};

// checklist fixtures: lab1 (2 tasks) + lab2 (1 task)
var box1a = new El({ 'data-ck': 'lab1-1' }), box1b = new El({ 'data-ck': 'lab1-2' }),
    box2a = new El({ 'data-ck': 'lab2-1' });
[box1a, box1b, box2a].forEach(function (b) {
  b._label = new El({});
  b._label.classList = (function (self) {
    var set = {};
    return { add: function (c) { set[c] = 1; }, remove: function (c) { delete set[c]; },
             has: function (c) { return !!set[c]; } };
  })(b._label);
});
var fill1 = new El({}), fill2 = new El({}), fillAll = new El({});
var bar1 = new El({ 'data-ptbar': 'lab1' });
bar1.querySelector = function (sel) { return sel === 'i' ? fill1 : null; };
var bar2 = new El({ 'data-ptbar': 'lab2' });
bar2.querySelector = function (sel) { return sel === 'i' ? fill2 : null; };
var cnt1 = new El({}), cnt2 = new El({}), cntAll = new El({});
var reset1 = new El({ 'data-ptreset': 'lab1' });

// quiz fixture: one question, correct = option 1, user picks option 0
var opt0 = new El({ value: '0' }), opt1 = new El({ value: '1', 'data-correct': '1' });
var lbl0 = new El({}), lbl1 = new El({});
opt0._label = lbl0; opt1._label = lbl1;
lbl0.classList = new Cls(); lbl1.classList = new Cls();
function Cls() {
  var set = {};
  this.add = function () { for (var i = 0; i < arguments.length; i++) { set[arguments[i]] = 1; } };
  this.remove = function () { for (var i = 0; i < arguments.length; i++) { delete set[arguments[i]]; } };
  this.has = function (c) { return !!set[c]; };
  this.set = set;
}
var item = new El({}); item.classList = new Cls();
item.querySelectorAll = function (sel) {
  return sel === 'input[type="radio"]' ? [opt0, opt1] : [];
};
item.querySelectorAll_labels = null;
var gradeBtn = new El({}), retryBtn = new El({}), scoreEl = new El({});
var form = new El({ 'data-ptq': 'lab1' });
form.querySelector = function (sel) {
  if (sel === '[data-ptq-grade]') { return gradeBtn; }
  if (sel === '[data-ptq-retry]') { return retryBtn; }
  if (sel === '.ptq-score') { return scoreEl; }
  return null;
};
form.querySelectorAll = function (sel) {
  if (sel === '.ptq-item') { return [item]; }
  if (sel === 'input[type="radio"]') { return [opt0, opt1]; }
  return [];
};

var root = {
  querySelectorAll: function (sel) {
    if (sel === 'input[data-ck]') { return [box1a, box1b, box2a]; }
    if (sel.indexOf('data-ck^="lab1-') !== -1) { return [box1a, box1b]; }
    if (sel.indexOf('data-ck^="lab2-') !== -1) { return [box2a]; }
    if (sel === '[data-ptbar]') { return [bar1, bar2]; }
    if (sel.indexOf('data-ptcount="lab1"') !== -1) { return [cnt1]; }
    if (sel.indexOf('data-ptcount="lab2"') !== -1) { return [cnt2]; }
    if (sel === '#pt-overall-bar i') { return [fillAll]; }
    if (sel === '#pt-overall-count') { return [cntAll]; }
    if (sel === '[data-ptreset]') { return [reset1]; }
    if (sel === 'form[data-ptq]') { return [form]; }
    if (sel === 'input[data-ck]') { return [box1a, box1b, box2a]; }
    return [];
  },
  querySelector: function () { return null; }
};
// gate in pt.js init: document.querySelector('input[data-ck]') — root above used for init only

var store = (function () {
  var data = {};
  return {
    getItem: function (k) { return Object.prototype.hasOwnProperty.call(data, k) ? data[k] : null; },
    setItem: function (k, v) { data[k] = v; },
    _data: data
  };
})();

var api = PT.init(root, store);
ok('init returns state', api && typeof api.state === 'object');

// initial progress: 0 tasks
is('initial lab1 count', cnt1.textContent, '0 / 2 tasks');
is('initial overall count', cntAll.textContent, '0 / 3 tasks across all labs');
is('initial bar width', fill1.style.width, '0%');

// check a box → persist + refresh
box1a.checked = true;
box1a.fire('change');
is('persisted key', store.getItem(PT.STORAGE_KEY), '{"lab1-1":true}');
is('lab1 count after check', cnt1.textContent, '1 / 2 tasks');
is('lab1 bar width', fill1.style.width, '50%');
is('overall count after check', cntAll.textContent, '1 / 3 tasks across all labs');
is('label marked done', box1a._label.classList.has('pt-done'), true);

// uncheck → removed
box1a.checked = false;
box1a.fire('change');
is('key removed', store.getItem(PT.STORAGE_KEY), '{}');
is('lab1 count back', cnt1.textContent, '0 / 2 tasks');

// check both lab1 + one lab2, then reset lab1
box1a.checked = true; box1a.fire('change');
box1b.checked = true; box1b.fire('change');
box2a.checked = true; box2a.fire('change');
is('all three checked', store.getItem(PT.STORAGE_KEY),
   '{"lab1-1":true,"lab1-2":true,"lab2-1":true}');
is('overall full', cntAll.textContent, '3 / 3 tasks across all labs');
reset1.fire('click');
is('reset cleared lab1 only', store.getItem(PT.STORAGE_KEY), '{"lab2-1":true}');
is('reset unchecked lab1 boxes', box1a.checked + ',' + box1b.checked, 'false,false');
is('lab2 box kept', box2a.checked, true);
is('lab2 count after reset', cnt2.textContent, '1 / 1 tasks');

// quiz grading: user chose 0, correct is 1
opt0.checked = true;
gradeBtn.fire('click');
is('score shown', scoreEl.textContent, 'Score: 0 / 1');
is('score visible', scoreEl.hidden, false);
ok('correct option marked ok', lbl1.classList.has('ptq-opt-ok'));
ok('wrong pick marked bad', lbl0.classList.has('ptq-opt-bad'));
ok('item graded', item.classList.has('ptq-graded') && item.classList.has('ptq-bad'));
is('retry revealed', retryBtn.hidden, false);

// retry resets
retryBtn.fire('click');
is('retry cleared score', scoreEl.hidden, true);
is('retry unchecked', opt0.checked, false);
is('retry ungraded', item.classList.has('ptq-graded'), false);

// now pick the correct answer
opt1.checked = true;
gradeBtn.fire('click');
is('perfect score', scoreEl.textContent, 'Score: 1 / 1 — perfect!');
ok('perfect badge', scoreEl.classList.has('ptq-perfect'));
ok('item good', item.classList.has('ptq-good'));

console.log('==========================================');
console.log('RESULTS: ' + pass + ' passed, ' + fail + ' failed, total ' + (pass + fail));
if (fail) {
  failures.forEach(function (f) {
    console.log('  ✗ ' + f.name + ': got=' + f.got + ' want=' + f.want);
  });
  process.exit(1);
}
console.log('ALL PT JS TESTS PASSED');
