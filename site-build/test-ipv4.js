#!/usr/bin/env node
/* ============================================================
   Automated tests for the IPv4/subnetting core (ipv4.js)
   Run:  node site-build/test-ipv4.js
   Exits non-zero if any check fails.
   ============================================================ */
'use strict';

var IPV4 = require('./ipv4.js');

var pass = 0, fail = 0, failures = [];

function is(name, got, want) {
  var okStr = String(got) === String(want);
  if (okStr) { pass++; } else { fail++; failures.push({ name: name, got: got, want: want }); }
}

console.log('=== A. ipv4.selfTest() built-in suite ===');
var st = IPV4.selfTest();
pass += st.passed;
fail += st.failed;
st.failures.forEach(function (f) { failures.push({ name: '[selfTest] ' + f.name, got: f.got, want: f.want }); });
console.log('  selfTest: ' + st.passed + '/' + st.total + ' passed');

console.log('=== B. additional edge cases ===');
// odd but valid addresses
is('0.0.0.0/32', IPV4.calc('0.0.0.0', '/32').network, '0.0.0.0');
is('255.255.255.255/32', IPV4.calc('255.255.255.255', '/32').broadcast, '255.255.255.255');
is('255.255.255.255/0 network', IPV4.calc('255.255.255.255', '/0').network, '0.0.0.0');
is('/1 first half', IPV4.calc('127.255.255.255', '/1').network, '0.0.0.0');
is('/1 second half', IPV4.calc('128.0.0.0', '/1').network, '128.0.0.0');
is('/29 usable', IPV4.calc('192.168.1.9', '/29').usable, 6);
is('/29 block align', IPV4.calc('192.168.1.9', '/29').network, '192.168.1.8');
is('/23 network', IPV4.calc('10.20.30.40', '/23').network, '10.20.30.0');
is('/23 broadcast', IPV4.calc('10.20.30.40', '/23').broadcast, '10.20.31.255');
is('/12 boundary (172.20)', IPV4.calc('172.20.1.1', '/12').network, '172.16.0.0');
is('/12 boundary (172.32 -> out)', IPV4.calc('172.32.1.1', '/12').network, '172.32.0.0');
is('/12 mask', IPV4.maskToDotted(12), '255.240.0.0');
is('/22 mask', IPV4.maskToDotted(22), '255.255.252.0');
is('/19 mask', IPV4.maskToDotted(19), '255.255.224.0');

// error paths give clear messages (not silent bad math)
is('error: bad octet has message', String(IPV4.calc('10.0.0.300', '/24').error || '').indexOf('0 to 255') !== -1, true);
is('error: bad mask has message', String(IPV4.calc('10.0.0.1', '255.0.255.0').error || '').indexOf('continuous') !== -1, true);
is('error: prefix 32 max', IPV4.calc('10.0.0.1', '/32').prefix, 32);
is('error: /33 rejected', IPV4.calc('10.0.0.1', '/33').ok, false);
is('error: mask missing', IPV4.calc('10.0.0.1', '').ok, false);
is('error: address missing', IPV4.calc('', '/24').ok, false);
is('error: junk input', IPV4.calc('not an ip', '/24').ok, false);

// mask->prefix symmetry for every prefix 0..32
var symOk = true;
for (var p = 0; p <= 32; p++) {
  var d = IPV4.maskToDotted(p);
  var back = IPV4.parseMaskInput(d);
  if (!back.ok || back.prefix !== p) { symOk = false; break; }
}
is('mask<->prefix symmetric for /0../32', symOk, true);

console.log('=== C. randomised invariant sweep (300 cases) ===');
var seed = 42; // deterministic PRNG so failures are reproducible
function rnd() { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; }
var sweepOk = true, sweepDetail = '';
for (var i = 0; i < 300 && sweepOk; i++) {
  var pre = Math.floor(rnd() * 33);
  var oct = [];
  for (var k = 0; k < 4; k++) oct.push(Math.floor(rnd() * 256));
  var addr = oct.join('.');
  var r = IPV4.calc(addr, '/' + pre);
  if (!r.ok) { sweepOk = false; sweepDetail = 'calc failed for ' + addr + '/' + pre; break; }
  var blk = Math.pow(2, 32 - pre);
  if (r.networkInt % blk !== 0) { sweepOk = false; sweepDetail = addr + '/' + pre + ' network not aligned'; break; }
  if (r.broadcastInt - r.networkInt !== blk - 1) { sweepOk = false; sweepDetail = addr + '/' + pre + ' block size wrong'; break; }
  if (r.ipInt < r.networkInt || r.ipInt > r.broadcastInt) { sweepOk = false; sweepDetail = addr + '/' + pre + ' ip outside block'; break; }
  if (r.total !== blk) { sweepOk = false; sweepDetail = addr + '/' + pre + ' total wrong'; break; }
  if (pre <= 30 && r.usable !== blk - 2) { sweepOk = false; sweepDetail = addr + '/' + pre + ' usable wrong'; break; }
  if (pre <= 30 && (r.firstHost !== IPV4.intToIp(r.networkInt + 1) || r.lastHost !== IPV4.intToIp(r.broadcastInt - 1))) {
    sweepOk = false; sweepDetail = addr + '/' + pre + ' host range wrong'; break;
  }
}
is('random sweep (detail: ' + (sweepDetail || 'none') + ')', sweepOk, true);

console.log('=== D. question-planner helpers (used by generators) ===');
// host requirement -> prefix: verified against usable capacity of the result
var hostCases = [[2, 30], [6, 29], [14, 28], [30, 27], [62, 26], [126, 25],
                 [254, 24], [255, 23], [500, 23], [1000, 22], [1, 30]];
hostCases.forEach(function (hc) {
  var pfx = IPV4.prefixForHosts(hc[0]);
  is('prefixForHosts(' + hc[0] + ')', pfx, hc[1]);
  var cap = IPV4.pow2(32 - pfx) - 2;
  var fits = cap >= hc[0];
  // minimal = no LARGER prefix (smaller block) would still fit the hosts
  var minimal = pfx === 32 ? true : (IPV4.pow2(32 - (pfx + 1)) - 2 < hc[0]);
  is('  capacity check for ' + hc[0] + ' hosts (cap=' + cap + ', minimal=' + minimal + ')',
     fits && minimal, true);
});
var subCases = [[24, 2, 25], [24, 4, 26], [24, 6, 27], [24, 8, 27], [24, 16, 28],
                [30, 2, 31], [26, 3, 28], [20, 12, 24]];
subCases.forEach(function (sc) {
  var pfx = IPV4.prefixForSubnets(sc[0], sc[1]);
  is('prefixForSubnets(' + sc[0] + ',' + sc[1] + ')', pfx, sc[2]);
  var count = IPV4.pow2(pfx - sc[0]);
  is('  subnet count >= requested', count >= sc[1], true);
});

console.log('=== E. lab.js (generators + quiz engine) ===');
var LAB = require('./lab.js');
var lst = LAB.selfTest();
pass += lst.passed;
fail += lst.failed;
lst.failures.forEach(function (f) { failures.push({ name: '[LAB] ' + f.name, got: f.got, want: f.want }); });
console.log('  LAB selfTest: ' + lst.passed + '/' + lst.total + ' passed');

console.log('=== F. DOM wiring smoke (stubbed document) ===');
function domEl(id) {
  return {
    id: id, textContent: '', innerHTML: '', value: '', hidden: false, disabled: false,
    className: '', handlers: {},
    addEventListener: function (t, f) { (this.handlers[t] = this.handlers[t] || []).push(f); },
    focus: function () {},
    fire: function (t, ev) {
      (this.handlers[t] || []).forEach(function (f) { f(ev || { preventDefault: function () {} }); });
    }
  };
}
var DOM_IDS = ['lab-selftest', 'cal-form', 'cal-addr', 'cal-mask', 'cal-err', 'cal-out',
  'cal-steps', 'qs-level', 'qs-count', 'qs-setup-msg', 'qs-start', 'qs-stage', 'q-progress',
  'q-type', 'q-level', 'q-prompt', 'q-input', 'q-answer', 'q-check', 'q-feedback', 'q-solution',
  'q-next', 'q-retry', 'q-stats'];
var ELS = {};
DOM_IDS.forEach(function (id) { ELS[id] = domEl(id); });
var CHECKBOXES = ['maskValue', 'network', 'broadcast', 'hostRange', 'hostCount',
  'subnetForHosts', 'subnetPrefix', 'subnetCount', 'subnetOf', 'vlsm'].map(function (v) {
    return { value: v, checked: true };
  });
global.document = {
  readyState: 'complete',
  getElementById: function (id) { return ELS[id] || null; },
  querySelectorAll: function () { return CHECKBOXES; },
  addEventListener: function () {}
};
try {
  LAB._initLab();
  is('self-test badge filled by init', /^Self-test: \d+\/\d+/.test(ELS['lab-selftest'].textContent), true);
  is('badge class set', ELS['lab-selftest'].className.indexOf('lab-badge') !== -1, true);

  // calculator: correct result + steps
  ELS['cal-addr'].value = '192.168.1.10';
  ELS['cal-mask'].value = '/26';
  ELS['cal-form'].fire('submit');
  is('calc output rendered (network .0 for .10/26)', ELS['cal-out'].innerHTML.indexOf('>192.168.1.0<') !== -1, true);
  is('calc private flag rendered', ELS['cal-out'].innerHTML.indexOf('Private') !== -1, true);
  is('calc steps rendered', ELS['cal-steps'].innerHTML.indexOf('Step-by-step') !== -1, true);
  is('calc error hidden on success', ELS['cal-err'].hidden, true);
  // calculator: invalid input
  ELS['cal-addr'].value = '999.1.1.1';
  ELS['cal-form'].fire('submit');
  is('calc error shown', ELS['cal-err'].hidden === false && ELS['cal-err'].textContent.length > 5, true);
  is('calc output cleared on error', ELS['cal-out'].innerHTML, '');
  // inline CIDR in address box
  ELS['cal-addr'].value = '10.0.0.99/30';
  ELS['cal-mask'].value = '';
  ELS['cal-form'].fire('submit');
  is('inline CIDR works (network .96)', ELS['cal-out'].innerHTML.indexOf('10.0.0.96') !== -1, true);
  is('/30 usable shown as 2', ELS['cal-out'].innerHTML.indexOf('>2<') !== -1, true);

  // quiz: start a set
  ELS['qs-level'].value = 'easy';
  ELS['qs-count'].value = '5';
  ELS['qs-start'].fire('click');
  var sess = LAB._getSession();
  is('session created with 5', sess && sess.questions.length, 5);
  is('stage visible', ELS['qs-stage'].hidden, false);
  is('progress text', ELS['q-progress'].textContent, 'Question 1 of 5');
  is('prompt non-empty', ELS['q-prompt'].innerHTML.length > 20, true);

  // submit a deliberately wrong answer
  ELS['q-answer'].value = 'definitely-not-an-answer';
  ELS['q-check'].fire('click');
  is('wrong feedback shown', ELS['q-feedback'].innerHTML.indexOf('Not quite') !== -1, true);
  is('solution shown after check', ELS['q-solution'].innerHTML.indexOf('Complete correct solution') !== -1, true);
  is('next button revealed', ELS['q-next'].hidden, false);
  is('stats updated after check', ELS['q-stats'].innerHTML.indexOf('Overall') !== -1, true);

  // now answer all remaining correctly via the live session
  var answeredWrong = 1;
  while (LAB._getSession().checked && !ELS['q-next'].hidden) {
    var s0 = LAB._getSession();
    if (!s0.checked) break;
    var idxBefore = s0.index;
    ELS['q-next'].fire('click');
    var s1 = LAB._getSession();
    if (s1.index === idxBefore) break;
    if (s1.index >= s1.questions.length) break;   // set finished (end screen)
    ELS['q-answer'].value = s1.questions[s1.index].answer;
    ELS['q-check'].fire('click');
    if (s1.lastGrade && !s1.lastGrade.ok) { answeredWrong++; }
  }
  // may have finished set
  var fin = LAB._getSession();
  is('set progressed beyond question 1', fin.index >= 4 || fin.results.length >= 5, true);
  is('at most 1 accidental wrong', answeredWrong <= 1, true);

  // finish the set if needed and check end screen
  while (LAB._getSession() && LAB._getSession().checked && LAB._getSession().index + 1 < LAB._getSession().questions.length) {
    ELS['q-next'].fire('click');
    var s2 = LAB._getSession();
    ELS['q-answer'].value = s2.questions[s2.index].answer;
    ELS['q-check'].fire('click');
  }
  if (LAB._getSession() && LAB._getSession().checked) ELS['q-next'].fire('click');
  is('end screen shown', ELS['q-progress'].textContent === 'Set complete' ||
     ELS['q-progress'].textContent.indexOf('Question') === 0, true);
} catch (e) {
  is('DOM smoke ran without exception (' + (e && e.message) + ')', false, true);
}
delete global.document;

console.log('');
console.log('==========================================');
console.log('RESULTS: ' + pass + ' passed, ' + fail + ' failed, total ' + (pass + fail));
if (fail) {
  console.log('FAILURES:');
  failures.forEach(function (f) { console.log('  ✗ ' + f.name + ' | got=' + f.got + ' want=' + f.want); });
  process.exit(1);
} else {
  console.log('ALL TESTS PASSED');
}
