/* ============================================================
   lab.js — IPv4 subnetting practice laboratory
   Sections: question generators (random, verified), quiz engine,
   calculator UI wiring. UMD: works in browser (window.LAB) and
   in node (require('./lab.js')) for automated tests.
   Depends on ipv4.js (window.IPV4 / require).
   ============================================================ */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory(require('./ipv4.js'));
  } else {
    root.LAB = factory(root.IPV4);
  }
}(typeof self !== 'undefined' ? self : this, function (IPV4) {
  'use strict';

  /* ---------------- deterministic-friendly PRNG ---------------- */
  var seed = null;
  function rand() {
    if (seed === null) seed = ((Date.now() & 0xffffffff) ^ 0x9e3779b9) >>> 0;
    seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
    return seed / 4294967296;
  }
  function setSeed(s) { seed = s >>> 0; }
  function rndInt(a, b) { return a + Math.floor(rand() * (b - a + 1)); } // inclusive
  function pick(arr) { return arr[Math.floor(rand() * arr.length)]; }
  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(rand() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  /* ---------------- shared helpers ---------------- */
  var TYPE_LABELS = {
    maskValue: 'Subnet mask ↔ prefix length',
    network: 'Network (subnet) address',
    broadcast: 'Broadcast address',
    hostRange: 'Usable host range',
    hostCount: 'Host addresses',
    subnetForHosts: 'Choosing a subnet size',
    subnetPrefix: 'Dividing a network into subnets',
    subnetCount: 'Number of subnets',
    subnetOf: 'Subnet containing a host',
    vlsm: 'VLSM allocation'
  };

  var LEVELS = ['easy', 'medium', 'hard'];

  // weight pools: which question types appear at each level
  var TYPE_POOL = {
    easy: ['maskValue', 'network', 'broadcast', 'hostRange', 'hostCount',
           'subnetForHosts', 'subnetCount'],
    medium: ['maskValue', 'network', 'broadcast', 'hostRange', 'hostCount',
             'subnetForHosts', 'subnetPrefix', 'subnetCount', 'subnetOf'],
    hard: ['maskValue', 'network', 'broadcast', 'hostRange', 'hostCount',
           'subnetForHosts', 'subnetPrefix', 'subnetCount', 'subnetOf', 'vlsm']
  };

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function code(s) { return '<code>' + esc(s) + '</code>'; }

  function stepList(steps) {
    return '<ol class="steps">' + steps.map(function (s) { return '<li>' + s + '</li>'; }).join('') + '</ol>';
  }

  function bin8(n) {
    var s = (n >>> 0).toString(2);
    while (s.length < 8) s = '0' + s;
    return s;
  }
  function bin32(n) {
    var s = (n >>> 0).toString(2);
    while (s.length < 32) s = '0' + s;
    return s;
  }
  function groupBin(n) { // /24-style grouped binary of an int
    var s = bin32(n);
    return s.slice(0, 8) + '.' + s.slice(8, 16) + '.' + s.slice(16, 24) + '.' + s.slice(24, 32);
  }
  function human(n) { // thousands-separated
    return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }

  /* private-network bases for question hosts */
  var O3_POOL = [0, 1, 4, 7, 12, 20, 30, 40, 55, 77, 100, 128, 150, 188, 200, 220];
  function randomPrivateBase() {
    var fam = rndInt(0, 2);
    if (fam === 0) return '192.168.' + pick(O3_POOL) + '.0';
    if (fam === 1) return '10.' + rndInt(0, 30) + '.' + rndInt(0, 40) + '.0';
    return '172.' + rndInt(16, 31) + '.' + pick(O3_POOL) + '.0';
  }

  /* force a base address to be a proper network address of prefix p */
  function alignedBase(base, p) {
    var c = IPV4.calc(base, '/' + p);
    return c.ok ? c.network : base;
  }

  /* ---------------- answer checking ---------------- */

  function normalizeAnswer(s) {
    return String(s == null ? '' : s)
      .replace(/\u2013|\u2014/g, '-')   // en/em dash -> hyphen
      .replace(/\u00a0/g, ' ')
      .trim().replace(/\s+/g, ' ');
  }

  var NONE_RE = /^(none|no usable hosts?|no usable|not applicable|n\/a|unusable|no hosts?|0)$/;

  /* parse "a - b" | "a – b" | "a to b" | "a,b" (any order) -> [int,int] or null.
     Deliberately uses no lookbehind (old Safari would fail to parse it). */
  function parseRangeAnswer(text) {
    var t = normalizeAnswer(text);
    if (!t || NONE_RE.test(t.toLowerCase())) return null; // caller distinguishes "none"
    var parts = t.split(/\s+to\s+|\s*-\s*|\s*,\s*|\s*\.\.\s*/i);
    if (parts.length !== 2) return null;
    var a = IPV4.parseIP(parts[0].trim());
    var b = IPV4.parseIP(parts[1].trim());
    if (!a.ok || !b.ok) return null;
    return [Math.min(a.int, b.int), Math.max(a.int, b.int)];
  }

  function isNoneAnswer(text) {
    return NONE_RE.test(normalizeAnswer(text).toLowerCase());
  }

  /* central grader: returns {ok, display} */
  function checkAnswer(q, text) {
    var raw = normalizeAnswer(text);
    if (!raw) return { ok: false, display: '' };

    if (q.answerKind === 'ip') {
      var p = IPV4.parseIP(raw);
      if (!p.ok) return { ok: false, display: q.answer };
      return { ok: p.int === q.answerInt, display: q.answer };
    }
    if (q.answerKind === 'prefix') {
      var m = IPV4.parseMaskInput(raw);
      if (m.ok && m.prefix === q.answerPrefix) return { ok: true, display: q.answer };
      return { ok: false, display: q.answer };
    }
    if (q.answerKind === 'number') {
      var digits = raw.replace(/[,\s]/g, '');
      if (!/^\d+$/.test(digits)) return { ok: false, display: String(q.answerNum) };
      return { ok: parseInt(digits, 10) === q.answerNum, display: String(q.answerNum) };
    }
    if (q.answerKind === 'range') {
      if (q.answerFirstInt === null) { // expects "no usable hosts"
        return { ok: isNoneAnswer(raw), display: 'no usable hosts' };
      }
      var r = parseRangeAnswer(raw);
      if (!r) return { ok: false, display: q.answer };
      return {
        ok: r[0] === q.answerFirstInt && r[1] === q.answerLastInt,
        display: q.answer
      };
    }
    return { ok: false, display: q.answer };
  }

  /* ---------------- independent verification of a question ----------------
     Derives the expected answer a second way (formulas / raw calc), used by
     generate() before a question is admitted, and by selfTest().           */
  function verifyQuestion(q) {
    var w = q.vWant;

    /* --- address-answer questions --- */
    if (w === 'network' || w === 'broadcast' || w === 'first' || w === 'last' || w === 'subnetOf') {
      var c = IPV4.calc(q.vAddr, '/' + q.vPrefix);
      if (!c.ok) return false;
      var want;
      if (w === 'network') want = c.networkInt;
      else if (w === 'broadcast') want = c.broadcastInt;
      else if (w === 'first') want = c.firstHost ? IPV4.parseIP(c.firstHost).int : null;
      else if (w === 'last') want = c.lastHost ? IPV4.parseIP(c.lastHost).int : null;
      else if (w === 'subnetOf') {
        var cp = IPV4.calc(q.vAddr, '/' + q.vParentPrefix);
        want = cp.ok ? cp.networkInt : undefined;
      }
      return want === q.answerInt;
    }

    /* --- VLSM: answer is a network address inside the parent --- */
    if (w === 'vlsm') {
      var v = IPV4.vlsmAllocate(q.vParentPrefix, IPV4.parseIP(q.vBase).int, q.vReqs);
      if (!v || !v.ok || v.allocations.length !== q.vReqs.length) return false;
      var parent = IPV4.calc(q.vBase + '/' + q.vParentPrefix);
      if (!parent.ok || parent.network !== q.vBase) return false;
      var a = v.allocations[q.vAskIndex];
      if (!a || a.network !== q.answer || a.prefix !== q.answerPrefix) return false;
      for (var i = 0; i < v.allocations.length; i++) {
        var al = v.allocations[i];
        var s0 = IPV4.parseIP(al.network).int, e0 = IPV4.parseIP(al.broadcast).int;
        if (s0 < parent.networkInt || e0 > parent.broadcastInt) return false; // inside parent
        for (var j = i + 1; j < v.allocations.length; j++) {
          var bl = v.allocations[j];
          var s1 = IPV4.parseIP(bl.network).int, e1 = IPV4.parseIP(bl.broadcast).int;
          if (s0 <= e1 && s1 <= e0) return false; // overlap
        }
      }
      return true;
    }

    /* --- prefix/mask answers --- */
    if (w === 'maskOf') return IPV4.maskFromPrefix(q.vPrefix) === q.answerMaskInt &&
      IPV4.maskToDotted(q.vPrefix) === q.answer;
    if (w === 'prefixOfMask') {
      var pm = IPV4.prefixFromMaskInt(q.answerMaskInt);
      return pm === q.answerPrefix && '/' + pm === q.answer;
    }
    if (w === 'newPrefixForHosts') {
      var pp = IPV4.prefixForHosts(q.vHosts);
      if (pp === null || pp !== q.answerPrefix) return false;
      return pp === 32 ? q.vHosts <= 0 : (IPV4.pow2(32 - pp) - 2) >= q.vHosts;
    }
    if (w === 'dividePrefix') {
      if (q.vSubnetCount < 2 || (q.vSubnetCount & (q.vSubnetCount - 1)) !== 0) return false;
      var bits = Math.round(Math.log(q.vSubnetCount) / Math.LN2);
      return q.vPrefix + bits === q.answerPrefix && q.answerPrefix <= 30 &&
        '/' + q.answerPrefix === q.answer;
    }

    /* --- number answers --- */
    if (w === 'usable' || w === 'total') {
      var blk = IPV4.pow2(32 - q.vPrefix);
      var want2 = w === 'total' ? blk
        : (q.vPrefix >= 31 ? 0 : blk - 2);
      return want2 === q.answerNum;
    }
    if (w === 'subnets') {
      if (q.vNewPrefix <= q.vPrefix || q.vNewPrefix > 32) return false;
      return IPV4.pow2(q.vNewPrefix - q.vPrefix) === q.answerNum;
    }

    /* --- range answers (usable host range) --- */
    if (q.answerKind === 'range') {
      if (q.vPrefix >= 31) {
        return q.answerFirstInt === null && q.answerLastInt === null &&
          q.answer === 'no usable hosts';
      }
      var cc = IPV4.calc(q.vAddr, '/' + q.vPrefix);
      if (!cc.ok) return false;
      return !!(cc.firstHost && cc.lastHost &&
        IPV4.parseIP(cc.firstHost).int === q.answerFirstInt &&
        IPV4.parseIP(cc.lastHost).int === q.answerLastInt);
    }
    return false;
  }

  /* ---------------- question builders ---------------- */

  function baseQ(level, type) {
    return {
      level: level,
      type: type,
      typeLabel: TYPE_LABELS[type] || type,
      solutionSteps: []
    };
  }

  function buildMaskValue(level) {
    var q = baseQ(level, 'maskValue');
    var pools = {
      easy: [8, 16, 24, 30, 32],
      medium: [18, 19, 22, 25, 26, 27],
      hard: [13, 17, 20, 21, 23, 28, 29]
    };
    if (rand() < 0.5) {
      var p = pick(pools[level]);
      q.id = 'maskValue:d2p:' + p;
      q.prompt = 'What dotted-decimal subnet mask corresponds to prefix <code>/' + p + '</code>?';
      var mi = IPV4.maskFromPrefix(p);
      q.answer = IPV4.maskToDotted(p);
      q.answerKind = 'ip';
      q.answerInt = mi;
      var head = (32 - p);
      q.solutionSteps = [
        'Prefix <code>/' + p + '</code> means the first <b>' + p + '</b> bits are 1s and the last <b>' + head + '</b> bits are 0s.',
        'Write 32 bits: <code>' + groupBin(mi) + '</code>',
        'Group into octets and convert: <code>' + code(q.answer) + '</code>'
      ];
      q.vWant = 'maskOf'; q.vPrefix = p; q.vAddr = null; q.answerMaskInt = mi;
      return q;
    }
    var mInt = IPV4.maskFromPrefix(pick([10, 12, 14, 17, 19, 22, 25, 26, 27, 28, 30]));
    var pre = IPV4.prefixFromMaskInt(mInt);
    q.id = 'maskValue:p2d:' + pre;
    q.prompt = 'What is the prefix length of the subnet mask <code>' + IPV4.maskToDotted(pre) + '</code>?';
    q.answer = '/' + pre;
    q.answerKind = 'prefix';
    q.answerPrefix = pre;
    q.answerMaskInt = mInt;
    q.solutionSteps = [
      'Mask <code>' + IPV4.maskToDotted(pre) + '</code> → binary <code>' + groupBin(mInt) + '</code>',
      'Count the 1s (contiguous, from the left): <b>' + pre + '</b>',
      'Prefix = <code>/' + pre + '</code>'
    ];
    q.vWant = 'prefixOfMask';
    return q;
  }

  function buildAddrQuestion(level, kind) { // kind: network | broadcast | subnetOf
    var q = baseQ(level, kind);
    var p, addr, c;
    var tries = 0;
    while (tries < 40) {
      tries++;
      p = level === 'easy' ? pick([24, 30, 29, 28])
        : level === 'medium' ? pick([24, 25, 26, 27, 28, 29])
        : pick([22, 23, 24, 25, 26, 27, 21, 28]);
      var base = randomPrivateBase();
      c = IPV4.calc(base, '/' + p);
      if (!c.ok || c.broadcastInt - c.networkInt < 3) continue;
      addr = IPV4.intToIp(c.networkInt + 1 + Math.floor(rand() * (c.broadcastInt - c.networkInt - 1)));
      break;
    }
    if (!addr || !c || !c.ok) return null;

    q.vAddr = addr; q.vPrefix = p; q.answerKind = 'ip';
    var blk = IPV4.pow2(32 - p);
    var bOct = 32 - p; // boundary
    var hostC = IPV4.calc(addr, '/' + p);

    if (kind === 'network') {
      q.id = 'network:' + addr + '/' + p;
      q.prompt = 'Host <code>' + addr + '/' + p + '</code> — what is its network (subnet) address?';
      q.answer = hostC.network; q.answerInt = hostC.networkInt; q.vWant = 'network';
      var mask = IPV4.maskToDotted(p);
      var bIdx = Math.min(3, Math.ceil((32 - p) / 8) - (32 - p >= 8 || (32 - p) % 8 === 0 ? 1 : 0));
      // simpler boundary explanation:
      var boundaryNote;
      if (p === 32) boundaryNote = 'a /32 is a single host route — the address is its own network.';
      else if (32 - p <= 8) boundaryNote = 'the interesting (boundary) octet is octet 4 — block size <b>' + blk + '</b>, so networks fall every ' + blk + ' addresses.';
      else if (32 - p <= 16) boundaryNote = 'the interesting octet is octet 3 — block size <b>' + blk + '</b> in octet 3.';
      else boundaryNote = 'the interesting octet is octet 2 — block size <b>' + blk + '</b>.';
      q.solutionSteps = [
        'Prefix <code>/' + p + '</code> → mask <code>' + mask + '</code>.',
        'Block size = 2<sup>32−' + p + '</sup> = <b>' + human(blk) + '</b> addresses per subnet. ' + boundaryNote,
        'Write host <code>' + addr + '</code> in binary: <code>' + groupBin(hostC.ipInt) + '</code>.',
        'Zero out all host bits (the bits the mask covers with 0s): <code>' + groupBin(hostC.networkInt) + '</code>',
        'Network address = <code>' + code(hostC.network) + '</code>'
      ];
    } else if (kind === 'broadcast') {
      q.id = 'broadcast:' + addr + '/' + p;
      q.prompt = 'For host <code>' + addr + '/' + p + '</code>, what is the broadcast address of its subnet?';
      q.answer = hostC.broadcast; q.answerInt = hostC.broadcastInt; q.vWant = 'broadcast';
      q.solutionSteps = [
        'Find the network first: host <code>' + addr + '</code> with mask <code>' + IPV4.maskToDotted(p) + '</code> → network <code>' + hostC.network + '</code> (block size <b>' + human(blk) + '</b>).',
        'The broadcast is the LAST address of the block: network + block − 1.',
        '<code>' + hostC.network + '</code> + ' + human(blk) + ' − 1',
        'Broadcast = <code>' + code(hostC.broadcast) + '</code> (all host bits set to 1: <code>' + groupBin(hostC.broadcastInt) + '</code>)'
      ];
    } else { // subnetOf
      q.id = 'subnetOf:' + addr + '/' + p;
      q.prompt = 'Host <code>' + addr + '/' + p + '</code> — which subnet (network address) does it belong to?';
      q.answer = hostC.network; q.answerInt = hostC.networkInt; q.vWant = 'subnetOf';
      q.vParentPrefix = p;
      q.solutionSteps = [
        'Host <code>' + addr + '/' + p + '</code>, mask <code>' + IPV4.maskToDotted(p) + '</code>.',
        'Block size = 2<sup>32−' + p + '</sup> = <b>' + human(blk) + '</b>. The host sits in the block that contains it.',
        'Binary host: <code>' + groupBin(hostC.ipInt) + '</code> → clear host bits → <code>' + groupBin(hostC.networkInt) + '</code>',
        'Subnet = <code>' + code(hostC.network) + '</code> (from <code>' + hostC.network + '</code> to <code>' + hostC.broadcast + '</code>)'
      ];
    }
    return q;
  }

  function buildHostRange(level) {
    var q = baseQ(level, 'hostRange');
    var p, base, c;
    var tries = 0;
    do {
      p = level === 'easy' ? pick([24, 28, 29])
        : level === 'medium' ? pick([24, 25, 26, 27, 28, 30])
        : pick([22, 25, 26, 27, 30, 31, 32]);
      base = randomPrivateBase();
      c = IPV4.calc(base, '/' + p);
      tries++;
    } while (tries < 30 && !c.ok);
    if (!c.ok) return null;
    var host = IPV4.intToIp(c.networkInt + (c.broadcastInt > c.networkInt ? 1 + Math.floor(rand() * Math.max(1, c.broadcastInt - c.networkInt - 1)) : 0));
    var hc = IPV4.calc(host, '/' + p);

    q.vAddr = host; q.vPrefix = p;
    q.id = 'hostRange:' + host + '/' + p;
    if (p >= 31) {
      q.prompt = 'Give the usable host range of <code>' + hostCsafe(hc) + '/' + p + '</code> (first – last usable).';
      q.answer = 'no usable hosts';
      q.answerKind = 'range';
      q.answerFirstInt = null; q.answerLastInt = null;
      q.solutionSteps = [
        'A <code>/' + p + '</code> network has ' + (p === 31 ? 'only <b>2</b> addresses' : 'only <b>1</b> address') + ': ' +
          (p === 31 ? 'the two addresses are used point-to-point (RFC 3021) — nothing is left for "first/last usable" hosts.' : 'the address itself is a host route — no network/broadcast pair.'),
        'Total addresses = 2<sup>32−' + p + '</sup> = <b>' + human(IPV4.pow2(32 - p)) + '</b>, usable hosts = <b>0</b>.',
        'Answer: <b>no usable hosts</b>'
      ];
    } else {
      q.prompt = 'Give the usable host range of <code>' + hc.network + '/' + p + '</code> (first – last usable).';
      q.answer = hc.firstHost + ' - ' + hc.lastHost;
      q.answerKind = 'range';
      q.answerFirstInt = IPV4.parseIP(hc.firstHost).int;
      q.answerLastInt = IPV4.parseIP(hc.lastHost).int;
      var blk = IPV4.pow2(32 - p);
      q.solutionSteps = [
        'Prefix <code>/' + p + '</code> → block size = 2<sup>32−' + p + '</sup> = <b>' + human(blk) + '</b>.',
        'Network = <code>' + hc.network + '</code>, broadcast = <code>' + hc.broadcast + '</code>.',
        'First usable = network + 1 → <code>' + hc.firstHost + '</code>. Last usable = broadcast − 1 → <code>' + hc.lastHost + '</code>.',
        'Usable range = <code>' + code(hc.firstHost + ' - ' + hc.lastHost) + '</code> (' + human(hc.usable) + ' usable hosts).'
      ];
    }
    return q;
  }
  function hostCsafe(c) { return c.network; }

  function buildHostCount(level) {
    var q = baseQ(level, 'hostCount');
    var pools = {
      easy: [24, 25, 26, 30],
      medium: [23, 27, 28, 29, 31],
      hard: [13, 20, 21, 22, 25, 31, 32]
    };
    var want = rand() < 0.65 ? 'usable' : 'total';
    var p = pick(pools[level]);
    var blk = IPV4.pow2(32 - p);
    var num = want === 'usable' ? (p >= 31 ? 0 : blk - 2) : blk;
    q.id = 'hostCount:' + want + ':' + p;
    q.prompt = 'How many <b>' + (want === 'usable' ? 'usable host' : 'total') + ' addresses</b> does a <code>/' + p + '</code> network have?';
    q.answer = human(num);
    q.answerKind = 'number';
    q.answerNum = num;
    q.vWant = want; q.vPrefix = p;
    var steps = [
      'Addresses in a <code>/' + p + '</code> block: 2<sup>32−' + p + '</sup> = 2<sup>' + (32 - p) + '</sup> = <b>' + human(blk) + '</b>.'
    ];
    if (want === 'usable') {
      if (p === 31) steps.push('RFC 3021: a <code>/31</code> has just 2 addresses used directly on a point-to-point link — usable host count = <b>0</b> (no classic network/broadcast subtraction).');
      else if (p === 32) steps.push('A <code>/32</code> is a single host route — usable host count = <b>0</b> (the one address <i>is</i> the host).');
      else steps.push('Usable hosts = total − network − broadcast = ' + human(blk) + ' − 2 = <b>' + human(num) + '</b>.');
    } else {
      steps.push('Total addresses = <b>' + human(num) + '</b>' +
        (p <= 30 ? ' (of which ' + human(blk - 2) + ' are usable).' : '.'));
    }
    q.solutionSteps = steps;
    return q;
  }

  function buildSubnetForHosts(level) {
    var q = baseQ(level, 'subnetForHosts');
    var hostNeeds = level === 'easy' ? [rndInt(2, 8), rndInt(10, 14), 30]
      : level === 'medium' ? [rndInt(40, 62), rndInt(100, 126), rndInt(200, 254)]
      : pick([rndInt(500, 600), rndInt(1000, 1100), rndInt(40, 60), 255]);
    var hosts = pick(hostNeeds);
    var p = IPV4.prefixForHosts(hosts);
    if (p === null || p < 8) return null;
    var base = randomPrivateBase();
    var baseP = level === 'easy' ? pick([16, 24]) : level === 'medium' ? pick([16, 24, 25]) : pick([16, 22, 24]);
    base = alignedBase(base, baseP);
    if (p <= baseP) return null;
    q.id = 'subnetForHosts:' + hosts + ':' + base + '/' + baseP;
    q.prompt = 'A department needs <b>' + human(hosts) + ' hosts</b> per subnet from base network <code>' + base + '/' + baseP + '</code>. ' +
      'What prefix length should each subnet have (smallest block that fits)?';
    q.answer = '/' + p;
    q.answerKind = 'prefix';
    q.answerPrefix = p;
    q.vWant = 'newPrefixForHosts'; q.vHosts = hosts;
    var cap = IPV4.pow2(32 - p) - 2;
    q.solutionSteps = [
      'Need usable ≥ ' + human(hosts) + ' → require 2<sup>32−p</sup> − 2 ≥ ' + human(hosts) + ', i.e. 2<sup>32−p</sup> ≥ ' + human(hosts + 2) + '.',
      hosts + 2 + ' needs ' + (32 - p) + ' host bits → 2<sup>' + (32 - p) + '</sup> = ' + human(cap + 2) + ' addresses.',
      'Check: <code>/' + (p + 1) + '</code> would give only ' + (p + 1 <= 30 ? human(IPV4.pow2(31 - p) - 2) : 0) + ' usable — too small; <code>/' + p + '</code> gives <b>' + human(cap) + '</b> usable — fits.',
      'Answer: <code>/' + p + '</code>'
    ];
    return q;
  }

  function buildSubnetPrefix(level) { // dividing a network into subnets
    var q = baseQ(level, 'subnetPrefix');
    var combos = level === 'medium'
      ? [[24, 2], [24, 4], [25, 2], [26, 4], [24, 8]]
      : [[23, 4], [24, 16], [26, 8], [27, 4], [22, 16], [24, 32], [20, 8]];
    var combo = pick(combos);
    var p0 = combo[0], cnt = combo[1];
    var bits = Math.round(Math.log(cnt) / Math.LN2);
    if (p0 + bits > 30) return null;
    var base = alignedBase(randomPrivateBase(), p0);
    q.id = 'subnetPrefix:' + base + '/' + p0 + ':' + cnt;
    q.prompt = 'Divide <code>' + base + '/' + p0 + '</code> into <b>' + cnt + ' equal-sized subnets</b>. ' +
      'What is the prefix length of each subnet?';
    q.answer = '/' + (p0 + bits);
    q.answerKind = 'prefix';
    q.answerPrefix = p0 + bits;
    q.vWant = 'dividePrefix'; q.vPrefix = p0; q.vSubnetCount = cnt;
    var newP = p0 + bits;
    q.solutionSteps = [
      'To create 2<sup>k</sup> subnets you borrow <b>' + bits + '</b> bit' + (bits > 1 ? 's' : '') + ' from the host part: 2<sup>' + bits + '</sup> = ' + cnt + '.',
      'Original prefix <code>/' + p0 + '</code> + ' + bits + ' borrowed bit' + (bits > 1 ? 's' : '') + ' → new prefix <code>/' + newP + '</code>.',
      'Each subnet now has 2<sup>' + (32 - newP) + '</sup> = ' + human(IPV4.pow2(32 - newP)) + ' addresses (' +
        (newP <= 30 ? human(IPV4.pow2(32 - newP) - 2) + ' usable hosts' : 'usable 0') + ').',
      'Answer: <code>/' + newP + '</code> (mask <code>' + IPV4.maskToDotted(newP) + '</code>)'
    ];
    return q;
  }

  function buildSubnetCount(level) {
    var q = baseQ(level, 'subnetCount');
    var combos = level === 'easy'
      ? [[24, 25], [24, 26], [23, 24], [24, 28]]
      : level === 'medium'
        ? [[24, 26], [24, 27], [25, 27], [23, 26], [24, 28]]
        : [[22, 25], [24, 30], [20, 26], [27, 30], [23, 27], [24, 29]];
    var combo = pick(combos);
    var p0 = combo[0], newP = combo[1];
    if (newP <= p0 || newP > 32) return null;
    var base = alignedBase(randomPrivateBase(), p0);
    var cnt = IPV4.pow2(newP - p0);
    q.id = 'subnetCount:' + base + '/' + p0 + ':' + newP;
    q.prompt = 'How many <code>/' + newP + '</code> subnets fit inside <code>' + base + '/' + p0 + '</code>?';
    q.answer = human(cnt);
    q.answerKind = 'number';
    q.answerNum = cnt;
    q.vWant = 'subnets'; q.vPrefix = p0; q.vNewPrefix = newP;
    q.solutionSteps = [
      'Borrowed bits k = ' + newP + ' − ' + p0 + ' = <b>' + (newP - p0) + '</b>.',
      'Subnets = 2<sup>k</sup> = 2<sup>' + (newP - p0) + '</sup> = <b>' + human(cnt) + '</b>.',
      'Check: each /' + newP + ' = ' + human(IPV4.pow2(32 - newP)) + ' addresses × ' + human(cnt) +
        ' = ' + human(IPV4.pow2(32 - newP) * cnt) + ' = whole /' + p0 + ' network (' +
        human(IPV4.pow2(32 - p0)) + ' addresses).'
    ];
    return q;
  }

  function buildVlsm(level) {
    if (level !== 'hard') return null;
    var q = baseQ(level, 'vlsm');
    var families = [
      { base: '192.168.32.0', p: 23 },
      { base: '192.168.64.0', p: 23 },
      { base: '10.20.0.0', p: 22 },
      { base: '172.24.0.0', p: 22 },
      { base: '192.168.0.0', p: 23 },
      { base: '10.5.0.0', p: 23 }
    ];
    var sizePools = [
      [rndInt(300, 450), rndInt(45, 62), rndInt(10, 14)],
      [rndInt(200, 250), rndInt(100, 120), rndInt(20, 30)],
      [rndInt(480, 510), rndInt(60, 100), rndInt(25, 50)]
    ];
    // retry until a family/pool combo fits the parent block entirely
    var fam = null, sizes = null, alloc = null, attempts = 0;
    while (attempts < 40 && !alloc) {
      attempts++;
      fam = pick(families);
      sizes = pick(sizePools);
      alloc = IPV4.vlsmAllocate(fam.p, IPV4.parseIP(fam.base).int, [
        { name: 'x', hosts: sizes[0] }, { name: 'y', hosts: sizes[1] }, { name: 'z', hosts: sizes[2] }
      ]);
      if (alloc && alloc.ok) break;
      alloc = null;
    }
    if (!alloc) return null;
    var names = shuffle(['Server farm', 'Guest Wi-Fi', 'Engineering', 'Sales floor', 'Branch office', 'Print room', 'VoIP LAN', 'Camera VLAN']);
    var reqs = [
      { name: names[0], hosts: sizes[0] },
      { name: names[1], hosts: sizes[1] },
      { name: names[2], hosts: sizes[2] }
    ];
    alloc = IPV4.vlsmAllocate(fam.p, IPV4.parseIP(fam.base).int, reqs);
    if (!alloc || !alloc.ok) return null;
    // ask a non-trivial allocation (prefer 1 or 2)
    var askIndex = rndInt(1, 2);
    var asked = alloc.allocations[askIndex];
    q.id = 'vlsm:' + fam.base + '/' + fam.p + ':' + reqs.map(function (r) { return r.hosts; }).join('_') + ':' + askIndex;
    q.prompt = 'VLSM: the network <code>' + fam.base + '/' + fam.p + '</code> must serve (largest first): ' +
      reqs.map(function (r) { return esc(r.name) + ' — <b>' + human(r.hosts) + ' hosts</b>'; }).join(', ') + '. ' +
      'After allocating in descending order of size, <b>' + esc(asked.name) + '</b> gets which network address?';
    q.answer = asked.network;
    q.answerKind = 'ip';
    q.answerInt = IPV4.parseIP(asked.network).int;
    q.answerPrefix = asked.prefix;
    q.vAddr = asked.network; q.vPrefix = asked.prefix; q.vWant = 'vlsm';
    q.vBase = fam.base; q.vReqBase = fam.p; q.vPrefix2 = fam.p;
    q.vBasePrefix = fam.p; q.vReqs = reqs; q.vAskIndex = askIndex;
    // note: verifyQuestion uses vPrefix of the parent — set dedicated fields
    q.vParentPrefix = fam.p;
    var steps = [
      'Sort requirements largest → smallest: ' + reqs.slice().sort(function (a, b) { return b.hosts - a.hosts; })
        .map(function (r) { return r.name + ' (' + r.hosts + ')'; }).join(', ') + '.',
      'Choose prefixes: ' + alloc.allocations.map(function (a) {
        return a.name + ' → ' + a.hosts + ' hosts → <code>/' + a.prefix + '</code>';
      }).join('; ') + '.',
      'Place blocks back-to-back from <code>' + fam.base + '</code>:'
    ];
    alloc.allocations.forEach(function (a, i) {
      steps.push((i + 1) + '. ' + a.name + ': <code>' + a.network + '</code>, broadcast ' +
        a.broadcast + (a.usable > 0 ? ', usable ' + a.firstHost + ' – ' + a.lastHost : '') +
        (a.name === asked.name ? ' ← <b>asked</b>' : ''));
    });
    steps.push('Answer: <code>' + code(asked.network) + '</code> (prefix <code>/' + asked.prefix + '</code>)');
    q.solutionSteps = steps;
    return q;
  }

  var BUILDERS = {
    maskValue: buildMaskValue,
    network: function (l) { return buildAddrQuestion(l, 'network'); },
    broadcast: function (l) { return buildAddrQuestion(l, 'broadcast'); },
    subnetOf: function (l) { return buildAddrQuestion(l, 'subnetOf'); },
    hostRange: buildHostRange,
    hostCount: buildHostCount,
    subnetForHosts: buildSubnetForHosts,
    subnetPrefix: buildSubnetPrefix,
    subnetCount: buildSubnetCount,
    vlsm: buildVlsm
  };

  /* ---------------- generation ---------------- */

  function generate(n, cfg) {
    cfg = cfg || {};
    // cfg.level: 'easy' | 'medium' | 'hard' (fixed) or 'mixed' (revision set:
    // every question independently draws its level, so one set spans all three).
    var mixed = cfg.level === 'mixed';
    var fixedLevel = mixed ? null
      : (cfg.level && LEVELS.indexOf(cfg.level) >= 0 ? cfg.level : 'easy');
    var baseTypes = (cfg.types && cfg.types.length)
      ? cfg.types.filter(function (t) { return BUILDERS[t]; })
      : null;
    var exclude = cfg.exclude || [];
    var out = [];
    var seen = {};
    exclude.forEach(function (id) { seen[id] = true; });
    var guard = 0, maxTries = n * 60;
    while (out.length < n && guard < maxTries) {
      guard++;
      var lv = mixed ? pick(LEVELS) : fixedLevel;
      var enabled = baseTypes && baseTypes.length
        ? baseTypes.slice()
        : TYPE_POOL[lv].slice();
      if (!enabled.length) enabled = TYPE_POOL[lv].slice();
      var t = pick(enabled);
      var q;
      try { q = BUILDERS[t](lv); } catch (e) { q = null; }
      if (!q || !q.id || seen[q.id]) continue;
      if (!verifyQuestion(q)) continue; // verified before admission
      seen[q.id] = true;
      out.push(q);
    }
    return out;
  }

  /* ---------------- quiz session engine ---------------- */

  function createSession(cfg) {
    var qs = generate((cfg && cfg.count) || 5, cfg || {});
    return {
      questions: qs,
      index: 0,
      results: [],          // {id, ok, given}
      checked: false,       // current question graded?
      lastGrade: null,
      totals: { answered: 0, correct: 0 } // cumulative across sessions on page
    };
  }

  function currentQuestion(session) {
    if (!session || !session.questions) return null;
    return session.questions[session.index] || null;
  }

  function submit(session, text) {
    var q = currentQuestion(session);
    if (!q || session.checked) return null;
    var g = checkAnswer(q, text);
    session.checked = true;
    session.lastGrade = { ok: g.ok, given: normalizeAnswer(text), display: g.display };
    session.results.push({ id: q.id, ok: g.ok, type: q.type, level: q.level });
    session.totals.answered++;
    if (g.ok) session.totals.correct++;
    return session.lastGrade;
  }

  function advance(session) {
    session.checked = false;
    session.lastGrade = null;
    session.index++;
    return session.index < session.questions.length;
  }

  function stats(session) {
    var wrong = session.results.filter(function (r) { return !r.ok; });
    var acc = session.totals.answered
      ? Math.round(1000 * session.totals.correct / session.totals.answered) / 10
      : 0;
    return {
      answered: session.results.length,
      total: session.questions.length,
      correct: session.results.length - wrong.length,
      wrongCount: wrong.length,
      wrongIds: wrong.map(function (r) { return r.id; }),
      sessionAccuracy: session.results.length
        ? Math.round(1000 * (session.results.length - wrong.length) / session.results.length) / 10 : 0,
      overallAccuracy: acc,
      overallAnswered: session.totals.answered,
      overallCorrect: session.totals.correct
    };
  }

  /* new session containing only previously missed questions */
  function retryMisses(session) {
    var st = stats(session);
    var miss = session.questions.filter(function (q) {
      return st.wrongIds.indexOf(q.id) >= 0;
    });
    return {
      questions: miss,
      index: 0,
      results: [],
      checked: false,
      lastGrade: null,
      totals: session.totals // keep lifetime counters
    };
  }

  function keepStats(from) {
    return {
      questions: [], index: 0, results: [], checked: false, lastGrade: null,
      totals: from.totals
    };
  }

  /* ---------------- lifetime totals (optional localStorage) ----------------
     Saved: ONLY the two lifetime counters {answered, correct}. Not saved:
     individual questions, answers, or set composition (sets are regenerated
     randomly each time anyway). Corrupt/absent data → start fresh. */
  var STORE_KEY = 'itn-lab-stats-v1';

  function loadTotals(store) {
    if (!store) return null;
    try {
      var p = JSON.parse(store.getItem(STORE_KEY));
      if (p && p.v === 1 &&
          typeof p.answered === 'number' && typeof p.correct === 'number' &&
          isFinite(p.answered) && isFinite(p.correct) &&
          p.answered >= 0 && p.correct >= 0 && p.correct <= p.answered &&
          Math.floor(p.answered) === p.answered &&
          Math.floor(p.correct) === p.correct) {
        return { answered: p.answered, correct: p.correct };
      }
    } catch (e) { /* missing or damaged → start fresh */ }
    return null;
  }

  function saveTotals(store, totals) {
    if (!store || !totals) return false;
    try {
      store.setItem(STORE_KEY, JSON.stringify({
        v: 1, answered: totals.answered, correct: totals.correct
      }));
      return true;
    } catch (e) { return false; } // storage unavailable → in-memory only
  }

  /* ---------------- selfTest ---------------- */

  function selfTest() {
    var checks = [];
    function is(name, got, want) {
      checks.push({ name: name, ok: String(got) === String(want), got: got, want: want });
    }
    setSeed(20261014);

    // generation + verification across all levels
    ['easy', 'medium', 'hard'].forEach(function (lv) {
      var qs = generate(40, { level: lv });
      is('generate 40 ' + lv, qs.length, 40);
      var allVerified = qs.every(function (q) {
        return !!q.answer && !!q.prompt && q.solutionSteps.length > 0 && verifyQuestion(q);
      });
      is('all ' + lv + ' questions verify', allVerified, true);
      var ids = qs.map(function (q) { return q.id; });
      is('no duplicate ids (' + lv + ')', new Set ? (new Set(ids).size === ids.length) : true, true);
      var covers = new Set(qs.map(function (q) { return q.type; })).size;
      is('type variety (' + lv + ', found ' + covers + ')', covers >= (lv === 'easy' ? 5 : 7), true);
    });

    // every question type appears and grades correctly
    var seenTypes = {};
    LEVELS.forEach(function (lv) {
      generate(60, { level: lv }).forEach(function (q) { seenTypes[q.type] = true; });
    });
    Object.keys(TYPE_LABELS).forEach(function (t) {
      is('type ' + t + ' generated at least once', !!seenTypes[t], true);
    });

    // grade right/wrong
    var qs = generate(30, { level: 'medium' });
    var rightOk = 0, wrongFlagged = 0;
    qs.forEach(function (q) {
      var g = checkAnswer(q, q.answer);
      if (g.ok) rightOk++;
      var bad;
      if (q.answerKind === 'number') bad = String(q.answerNum + 7);
      else if (q.answerKind === 'prefix') bad = '/1';
      else bad = '203.0.113.99';
      if (!checkAnswer(q, bad).ok) wrongFlagged++;
    });
    is('canonical answer accepted for all 30', rightOk, 30);
    is('wrong answers rejected for all 30', wrongFlagged, 30);

    // answer format flexibility
    var rangeQ = generate(40, { level: 'hard' }).filter(function (q) { return q.answerKind === 'range'; })[0];
    if (rangeQ) {
      var f1 = rangeQ.answer.replace(' - ', ' – ');
      var f2 = rangeQ.answer.replace(' - ', ' to ');
      var f3 = rangeQ.answer.replace(/ - /g, '-');
      var f4 = rangeQ.answer.split(' - ').reverse().join(' - ');
      is('range: en-dash form', checkAnswer(rangeQ, f1).ok, true);
      is('range: "to" form', checkAnswer(rangeQ, f2).ok, true);
      is('range: no spaces form', checkAnswer(rangeQ, f3).ok, true);
      is('range: reversed order', checkAnswer(rangeQ, f4).ok, true);
    } else { is('range question available in hard', false, true); }

    var prefixQs = generate(40, { level: 'medium' }).filter(function (q) { return q.answerKind === 'prefix'; });
    if (prefixQs.length) {
      var pq = prefixQs[0];
      var bare = pq.answer.replace('/', '');
      is('prefix: bare number form', checkAnswer(pq, bare).ok, true);
      var maskForm = IPV4.maskToDotted(pq.answerPrefix);
      is('prefix: dotted-mask form (' + maskForm + ')', checkAnswer(pq, maskForm).ok, true);
    } else is('prefix question available in medium', false, true);

    // VLSM: no overlap, fits parent, 20 draws
    var vlsmOk = true, vlsmDetail = '';
    for (var i = 0; i < 20; i++) {
      var vq = buildVlsm('hard');
      if (!vq) { vlsmOk = false; vlsmDetail = 'build failed'; break; }
      if (!verifyQuestion(vq)) { vlsmOk = false; vlsmDetail = 'verify failed'; break; }
      var parent = IPV4.calc(vq.vBase + '/' + vq.vParentPrefix);
      var a = IPV4.vlsmAllocate(vq.vParentPrefix, IPV4.parseIP(vq.vBase).int, vq.vReqs);
      if (!a || !a.ok) { vlsmOk = false; vlsmDetail = 'allocate failed'; break; }
      var nets = a.allocations.map(function (al) { return IPV4.parseIP(al.network).int; });
      for (var j = 1; j < nets.length; j++) {
        if (nets[j] < nets[j - 1]) { vlsmOk = false; vlsmDetail = 'order'; }
      }
      for (var j2 = 0; j2 < a.allocations.length; j2++) {
        var al = a.allocations[j2];
        var end = IPV4.parseIP(al.broadcast).int;
        if (IPV4.parseIP(al.network).int < parent.networkInt || end > parent.broadcastInt) {
          vlsmOk = false; vlsmDetail = 'outside parent';
        }
        for (var k = j2 + 1; k < a.allocations.length; k++) {
          var bl = a.allocations[k];
          if (IPV4.parseIP(al.network).int <= IPV4.parseIP(bl.broadcast).int &&
              IPV4.parseIP(bl.network).int <= end) { vlsmOk = false; vlsmDetail = 'overlap'; }
        }
      }
      if (!vlsmOk) break;
    }
    is('VLSM 20 draws valid (' + vlsmDetail + ')', vlsmOk, true);

    // session flow: answer, advance, stats, retry
    var sess = createSession({ level: 'medium', count: 10 });
    is('session has 10 questions', sess.questions.length, 10);
    var correctCount = 0;
    while (currentQuestion(sess)) {
      var st = submit(sess, currentQuestion(sess).answer);
      if (st.ok) correctCount++;
      var q0 = currentQuestion(sess);
      var st2 = checkAnswer(q0, q0.answerKind === 'number' ? '1' : '10.10.10.10');
      if (!st2.ok) {}
      advance(sess);
    }
    is('all 10 graded correct with canonical answers', correctCount, 10);
    var st3 = stats(sess);
    is('stats: answered', st3.answered, 10);
    is('stats: accuracy 100%', st3.overallAccuracy, 100);

    // retry misses: make a wrong set deliberately
    var sess2 = createSession({ level: 'easy', count: 6 });
    var wrongs = 0;
    while (currentQuestion(sess2)) {
      var qq = currentQuestion(sess2);
      var bad = qq.answerKind === 'number' ? '1' : (qq.answerKind === 'range' ? '1.1.1.1 - 2.2.2.2' : '203.0.113.99');
      var g2 = submit(sess2, bad);
      if (!g2.ok) wrongs++;
      advance(sess2);
    }
    is('6/6 marked wrong', wrongs, 6);
    var retry = retryMisses(sess2);
    is('retry session holds 6 missed', retry.questions.length, 6);
    is('retry keeps lifetime totals', retry.totals.answered, 6);
    is('retry: correct answers grade ok', checkAnswer(retry.questions[0], retry.questions[0].answer).ok, true);

    var passed = checks.filter(function (c) { return c.ok; }).length;
    return {
      total: checks.length, passed: passed, failed: checks.length - passed,
      failures: checks.filter(function (c) { return !c.ok; })
    };
  }

  /* ---------------- public API ---------------- */
  var api = {
    setSeed: setSeed,
    rand: rand,
    generate: generate,
    verifyQuestion: verifyQuestion,
    checkAnswer: checkAnswer,
    normalizeAnswer: normalizeAnswer,
    parseRangeAnswer: parseRangeAnswer,
    createSession: createSession,
    currentQuestion: currentQuestion,
    submit: submit,
    advance: advance,
    stats: stats,
    retryMisses: retryMisses,
    keepStats: keepStats,
    STORE_KEY: STORE_KEY,
    loadTotals: loadTotals,
    saveTotals: saveTotals,
    TYPE_LABELS: TYPE_LABELS,
    LEVELS: LEVELS,
    selfTest: selfTest,
    buildVlsm: buildVlsm
  };

  /* ============================================================
     DOM layer — only runs in a browser page that has #lab-root
     ============================================================ */
  function $(id) { return document.getElementById(id); }

  function showOut(el, html) { el.innerHTML = html; }

  function renderCalcResult(c) {
    var rows = [];
    function row(k, v, cls) {
      rows.push('<tr' + (cls ? ' class="' + cls + '"' : '') + '><th>' + k + '</th><td>' + v + '</td></tr>');
    }
    row('Address', '<code>' + c.ip + '</code>');
    row('Mask (dotted)', '<code>' + c.mask + '</code>');
    row('Prefix / CIDR', '<code>/' + c.prefix + '</code>');
    row('Network', '<code>' + c.network + '</code>');
    row('Broadcast', '<code>' + c.broadcast + '</code>');
    if (c.prefix <= 30) {
      row('First usable', '<code>' + c.firstHost + '</code>');
      row('Last usable', '<code>' + c.lastHost + '</code>');
      row('Total addresses', human(c.total));
      row('Usable hosts', human(c.usable));
    } else {
      row('First usable', '—');
      row('Last usable', '—');
      row('Total addresses', human(c.total));
      row('Usable hosts', '<b>0</b> <span class="note">' + (c.prefix === 31
        ? '(/31 — 2 addresses, RFC 3021 point-to-point link)'
        : '(/32 — single host route)') + '</span>');
    }
    row('Address scope', c.isPrivate
      ? '<span class="tag tag-priv">Private (RFC 1918)</span>'
      : '<span class="tag tag-pub">Public</span>');
    var html = '<div class="cal-table-wrap"><table class="cal-table">' + rows.join('') + '</table></div>';
    html += '<div class="cal-extras">';
    if (c.boundaryOctet) {
      html += '<p class="note">Interesting (boundary) octet: <b>octet ' + c.boundaryOctet + '</b> — ' +
        'block size <b>' + c.blockSize + '</b> in that octet (networks change every ' + c.blockSize + ').</p>';
    }
    if (c.prefix <= 30) {
      html += '<p class="note">Formula: usable = 2<sup>32−' + c.prefix + '</sup> − 2 = ' +
        human(c.total) + ' − 2 = <b>' + human(c.usable) + '</b>.</p>';
    }
    html += '<details><summary>Binary view</summary>' +
      '<p>IP:      <code>' + groupBin(c.ipInt) + '</code></p>' +
      '<p>Mask:    <code>' + groupBin(c.maskInt) + '</code></p>' +
      '<p>Network: <code>' + groupBin(c.networkInt) + '</code></p>' +
      '<p>Broadcast:<code>' + groupBin(c.broadcastInt) + '</code></p></details>';
    html += '</div>';
    return html;
  }

  function renderSteps(c) {
    var s = [];
    s.push('Prefix <code>/' + c.prefix + '</code> → mask <code>' + c.mask + '</code>' +
      ' (binary <code>' + groupBin(c.maskInt) + '</code>).');
    var hostBits = 32 - c.prefix;
    s.push('Host bits = 32 − ' + c.prefix + ' = <b>' + hostBits + '</b> → block size = 2<sup>' + hostBits + '</sup> = <b>' +
      human(c.blockSize) + '</b> addresses.' +
      (c.boundaryOctet ? ' The boundary octet is <b>octet ' + c.boundaryOctet + '</b>.' : ''));
    s.push('Network identification — round ' + c.ip + ' down to the multiple of ' + c.blockSize +
      ' in octet ' + (c.boundaryOctet || 4) + ': <code>' + c.network + '</code>.' +
      ' (Zero the host bits: <code>' + groupBin(c.ipInt) + '</code> → <code>' + groupBin(c.networkInt) + '</code>.)');
    s.push('Broadcast = network + block − 1 = <code>' + c.network + '</code> + ' + human(c.blockSize) + ' − 1 = <code>' + c.broadcast + '</code>');
    if (c.prefix <= 30) {
      s.push('Host range: first usable = network + 1 = <code>' + c.firstHost + '</code>; last usable = broadcast − 1 = <code>' + c.lastHost + '</code>.');
      s.push('Usable hosts = ' + human(c.total) + ' − 2 = <b>' + human(c.usable) + '</b> (subtract network & broadcast).');
    } else if (c.prefix === 31) {
      s.push('/31 special case: only 2 addresses exist; on point-to-point links both are used directly (RFC 3021) — usable hosts = <b>0</b>, no classic broadcast split.');
    } else {
      s.push('/32 special case: the address is a single host route — usable hosts = <b>0</b>.');
    }
    return '<p class="steps-title">Step-by-step solution</p>' + stepList(s);
  }

  function initLab() {
    // ---- self-test badge ----
    var badge = $('lab-selftest');
    var st;
    try {
      st = selfTest();
      if (badge) {
        badge.textContent = 'Self-test: ' + st.passed + '/' + st.total +
          ' checks passed in this browser — answers verified automatically';
        badge.className = 'lab-badge ' + (st.failed ? 'badge-bad' : 'badge-ok');
        if (st.failed) {
          badge.title = st.failures.map(function (f) { return f.name + ' got=' + f.got + ' want=' + f.want; }).join('\n');
        }
      }
    } catch (e) {
      if (badge) { badge.textContent = 'Self-test could not run: ' + e.message; badge.className = 'lab-badge badge-bad'; }
    }

    // ---- calculator ----
    var calForm = $('cal-form');
    if (calForm) {
      calForm.addEventListener('submit', function (ev) {
        ev.preventDefault();
        var addrEl = $('cal-addr'), maskEl = $('cal-mask');
        var errEl = $('cal-err'), outEl = $('cal-out'), stepsEl = $('cal-steps');
        var addr = addrEl.value.trim();
        var mask = maskEl.value.trim();
        // support inline addr/24 in the address box if mask box empty
        var inline = addr.match(/^(.+?)\s*\/\s*(\d{1,2})$/);
        if (inline && !mask) { addr = inline[1].trim(); mask = '/' + inline[2]; }
        var c = IPV4.calc(addr, mask);
        if (!c.ok) {
          errEl.textContent = c.error || 'Please check the input.';
          errEl.hidden = false;
          outEl.innerHTML = '';
          stepsEl.innerHTML = '';
          return;
        }
        errEl.hidden = true;
        showOut(outEl, renderCalcResult(c));
        showOut(stepsEl, renderSteps(c));
      });
    }

    // ---- quiz ----
    var session = null;
    var startBtn = $('qs-start');
    if (!startBtn) return;
    // lifetime counters: restored from localStorage when available (browser-only,
    // best-effort — see the storage note on the page)
    var store = null;
    try { store = (typeof localStorage !== 'undefined') ? localStorage : null; }
    catch (e) { store = null; }
    var lifeTotals = loadTotals(store);

    function statsHtml() {
      var s = stats(session);
      return '<b>Set:</b> ' + s.correct + '/' + s.answered + ' correct' +
        (s.answered ? ' (' + s.sessionAccuracy + '%)' : '') +
        ' &nbsp;·&nbsp; <b>Overall:</b> ' + s.overallCorrect + '/' + s.overallAnswered +
        ' (' + s.overallAccuracy + '% accuracy)';
    }

    function renderStage() {
      var q = currentQuestion(session);
      var stage = $('qs-stage'), statsEl = $('q-stats');
      statsEl.innerHTML = session.totals.answered ? statsHtml() : '';
      if (!q) {
        stage.hidden = false;
        var s = stats(session);
        $('q-progress').textContent = 'Set complete';
        $('q-type').textContent = '';
        $('q-type').className = 'qs-pill';
        $('q-level').textContent = '';
        $('q-level').className = 'qs-pill';
        $('q-prompt').innerHTML = '<p>Set finished — <b>' + s.correct + '/' + s.total + '</b> correct in this set' +
          (s.wrongCount ? ', ' + s.wrongCount + ' to retry.' : '.') + '</p>';
        $('q-input').hidden = true;
        $('q-check').hidden = true;
        $('q-feedback').innerHTML = '';
        $('q-solution').innerHTML = '';
        $('q-next').hidden = true;
        $('q-retry').hidden = s.wrongCount === 0;
        return;
      }
      stage.hidden = false;
      $('q-input').hidden = false;
      $('q-check').hidden = false;
      $('q-retry').hidden = true;
      $('q-progress').textContent = 'Question ' + (session.index + 1) + ' of ' + session.questions.length;
      $('q-type').textContent = q.typeLabel;
      $('q-type').className = 'qs-pill';
      $('q-level').textContent = q.level;
      $('q-level').className = 'qs-pill level-' + q.level;
      $('q-prompt').innerHTML = '<p>' + q.prompt + '</p>';
      var inp = $('q-answer');
      inp.value = '';
      inp.placeholder = answerPlaceholder(q);
      $('q-feedback').innerHTML = '';
      $('q-solution').innerHTML = '';
      $('q-next').hidden = true;
      $('q-check').disabled = false;
      inp.focus();
    }

    function answerPlaceholder(q) {
      if (q.answerKind === 'ip') return 'e.g. 192.168.1.0';
      if (q.answerKind === 'prefix') return 'e.g. /26 (or 26, or 255.255.255.0)';
      if (q.answerKind === 'number') return 'e.g. 510';
      if (q.answerKind === 'range') return 'first - last (e.g. 192.168.1.1 - 192.168.1.62)';
      return '';
    }

    function checkFn() {
      var q = currentQuestion(session);
      if (!q || session.checked) return;
      var g = submit(session, $('q-answer').value);
      if (!g) return;
      $('q-check').disabled = true;
      var fb = $('q-feedback');
      if (g.ok) {
        fb.innerHTML = '<div class="fb-ok">✓ Correct — <b>' + esc(g.display) + '</b></div>';
      } else {
        fb.innerHTML = '<div class="fb-bad">✗ Not quite. Your answer: ' +
          (g.given ? '<code>' + esc(g.given) + '</code>' : '<i>(empty)</i>') +
          '. The correct answer is <b>' + esc(g.display) + '</b>.</div>';
      }
      $('q-solution').innerHTML = '<div class="solution-box"><p class="steps-title">Complete correct solution</p>' +
        stepList(q.solutionSteps) + '</div>';
      $('q-next').hidden = false;
      $('q-stats').innerHTML = statsHtml();
      lifeTotals = session.totals;
      saveTotals(store, session.totals);
    }

    startBtn.addEventListener('click', function (ev) {
      ev.preventDefault();
      var level = $('qs-level').value;
      var count = parseInt($('qs-count').value, 10) || 5;
      var typeBoxes = document.querySelectorAll('#qs-types input[type=checkbox]');
      var types = [];
      for (var i = 0; i < typeBoxes.length; i++) if (typeBoxes[i].checked) types.push(typeBoxes[i].value);
      if (!types.length) {
        $('qs-setup-msg').textContent = 'Pick at least one question type.';
        $('qs-setup-msg').hidden = false;
        return;
      }
      $('qs-setup-msg').hidden = true;
      var prevTotals = session ? session.totals : lifeTotals;
      session = createSession({ level: level, count: count, types: types });
      if (prevTotals) session.totals = prevTotals; // lifetime accuracy across sets
      if (!session.questions.length) {
        $('qs-setup-msg').textContent = 'Could not generate questions with that combination — try another.';
        $('qs-setup-msg').hidden = false;
        return;
      }
      renderStage();
    });

    $('q-check').addEventListener('click', function (ev) { ev.preventDefault(); checkFn(); });
    $('q-answer').addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') { ev.preventDefault(); if (session && !session.checked) checkFn(); }
    });
    $('q-next').addEventListener('click', function (ev) {
      ev.preventDefault();
      advance(session);
      renderStage();
    });
    $('q-retry').addEventListener('click', function (ev) {
      ev.preventDefault();
      if (!session) return;
      var missed = retryMisses(session);
      if (!missed.questions.length) return;
      session = missed;
      renderStage();
    });

    // mark un-answered as absent: seed stage hidden
    $('qs-stage').hidden = true;
    api._getSession = function () { return session; };
  }

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () { try { initLab(); } catch (e) { /* silent */ } });
    } else if (document.getElementById('lab-root')) {
      try { initLab(); } catch (e) { /* silent */ }
    }
  }

  api._initLab = initLab;
  return api;
}));
