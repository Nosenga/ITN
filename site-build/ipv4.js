/* ============================================================
   ipv4.js — core IPv4 / subnetting arithmetic
   ------------------------------------------------------------
   Pure functions, no DOM, no dependencies. Used by:
     - the subnetting laboratory page (lab.js)
     - automated tests (node site-build/test-ipv4.js)
   All address maths is done with exact integer arithmetic
   (doubles represent integers exactly up to 2^53; every value
   here is < 2^33), which avoids JavaScript's signed 32-bit
   bitwise pitfalls (e.g. >>> on 0xFFFFFFFF, << by 32).
   UMD-lite: attaches to window.IPV4 / module.exports.
   ============================================================ */
(function (root, factory) {
  'use strict';
  var api = factory();
  if (typeof module === 'object' && module.exports) { module.exports = api; }
  if (root) { root.IPV4 = api; }
})(typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : this),
function () {
  'use strict';

  var TWO32 = 4294967296; // 2^32

  function pow2(n) {
    // exact for integer n in [0, 53]
    if (n < 0 || n > 53) throw new Error('pow2 out of range: ' + n);
    return Math.pow(2, n);
  }

  /* ---------------- parsing / formatting ---------------- */

  function parseIP(str) {
    if (str === null || str === undefined) return { ok: false, err: 'Enter an IPv4 address (e.g. 192.168.1.10).' };
    var s = String(str).trim();
    if (!s) return { ok: false, err: 'Enter an IPv4 address (e.g. 192.168.1.10).' };
    var parts = s.split('.');
    if (parts.length !== 4) {
      return { ok: false, err: 'An IPv4 address needs exactly 4 numbers separated by dots ' +
        '(e.g. 192.168.1.10) — you entered ' + parts.length + ' part' + (parts.length === 1 ? '' : 's') + '.' };
    }
    var octets = [];
    for (var i = 0; i < 4; i++) {
      var p = parts[i];
      if (!/^\d{1,3}$/.test(p)) {
        return { ok: false, err: 'Octet ' + (i + 1) + ' ("' + p + '") is not a whole number between 0 and 255.' };
      }
      var v = parseInt(p, 10);
      if (v > 255) {
        return { ok: false, err: 'Octet ' + (i + 1) + ' is ' + v + ' — IPv4 octets range from 0 to 255.' };
      }
      octets.push(v);
    }
    return { ok: true, octets: octets, int: octetsToInt(octets) };
  }

  function octetsToInt(o) {
    return ((o[0] * 256 + o[1]) * 256 + o[2]) * 256 + o[3];
  }

  function intToOctets(n) {
    var a = Math.floor(n / 16777216); var r = n - a * 16777216;
    var b = Math.floor(r / 65536);     r = r - b * 65536;
    var c = Math.floor(r / 256);       var d = r - c * 256;
    return [a, b, c, d];
  }

  function intToIp(n) { return intToOctets(n).join('.'); }

  function pad(n, width) {
    var s = String(n);
    while (s.length < width) s = '0' + s;
    return s;
  }

  function octetBinary(v) { return pad(v.toString(2), 8); }

  function ipIntBinary(n) { return intToOctets(n).map(octetBinary); }

  /* ---------------- mask helpers ---------------- */

  function maskFromPrefix(p) {
    if (p === 0) return 0;
    return TWO32 - pow2(32 - p);
  }

  function prefixFromMaskInt(m) {
    // contiguity is inherent: only masks of the form 2^32 - 2^(32-k) exist here
    for (var p = 0; p <= 32; p++) {
      if (maskFromPrefix(p) === m) return p;
    }
    return -1;
  }

  function maskToDotted(prefix) { return intToIp(maskFromPrefix(prefix)); }

  /*
    Parse the "mask" input. Accepts:
      dotted mask  : 255.255.255.0   (validated for contiguity)
      CIDR form    : /24  or  24
  */
  function parseMaskInput(str) {
    if (str === null || str === undefined || !String(str).trim()) {
      return { ok: false, err: 'Enter a subnet mask — either dotted (255.255.255.0) or a CIDR prefix (/24 or 24).' };
    }
    var s = String(str).trim();
    if (s.charAt(0) === '/' || /^\d{1,2}$/.test(s)) {
      var numStr = s.replace(/^\//, '');
      if (!/^\d{1,2}$/.test(numStr)) {
        return { ok: false, err: 'The prefix must be a whole number from 0 to 32 (e.g. /24).' };
      }
      var p = parseInt(numStr, 10);
      if (p > 32) {
        return { ok: false, err: 'Prefix /' + p + ' is invalid — CIDR prefixes range from /0 to /32.' };
      }
      return { ok: true, prefix: p, maskInt: maskFromPrefix(p), form: 'cidr' };
    }
    var parsed = parseIP(s);
    if (!parsed.ok) {
      return { ok: false, err: 'Subnet mask problem: ' + parsed.err };
    }
    var m = parsed.int;
    var prefix = prefixFromMaskInt(m);
    if (prefix === -1) {
      return { ok: false, err: 'The subnet mask ' + s + ' is not valid: a mask must be a continuous run of ' +
        '1-bits followed by 0-bits (e.g. 255.255.0.255 is NOT a valid mask).' };
    }
    return { ok: true, prefix: prefix, maskInt: m, form: 'dotted' };
  }

  /* ---------------- private-range check ---------------- */

  function privateRangeOf(int) {
    var a8 = 10 * 16777216;                                   // 10.0.0.0/8
    if (int >= a8 && int < a8 + 16777216) return '10.0.0.0/8';
    var b12 = (172 * 256 + 16) * 65536;                       // 172.16.0.0/12
    if (int >= b12 && int < b12 + 1048576) return '172.16.0.0/12';
    var c16 = (192 * 256 + 168) * 65536;                      // 192.168.0.0/16
    if (int >= c16 && int < c16 + 65536) return '192.168.0.0/16';
    return null;
  }

  /* ---------------- main calculation ---------------- */

  /*
    calc('192.168.1.77', '255.255.255.0')  or  calc('192.168.1.77', '/24')
    also accepts address-with-prefix in the address field when mask field empty.
    Returns { ok:false, error } or a rich result used by UI + workings.
  */
  function calc(addrStr, maskStr) {
    var addr = String(addrStr === undefined || addrStr === null ? '' : addrStr).trim();
    var maskField = String(maskStr === undefined || maskStr === null ? '' : maskStr).trim();

    var addrForParse = addr, prefixSource = maskField;
    if (addr.indexOf('/') !== -1) {
      var bits = addr.split('/');
      if (maskField) {
        return { ok: false, error: 'Enter the prefix in ONE place: either "address/prefix" in the address box ' +
          'OR a mask in the mask box — not both.' };
      }
      if (bits.length !== 2) {
        return { ok: false, error: 'The address/prefix field should look like 192.168.1.10/24.' };
      }
      addrForParse = bits[0];
      prefixSource = '/' + bits[1];
    }

    var ip = parseIP(addrForParse);
    if (!ip.ok) return { ok: false, error: ip.err };

    var mask = parseMaskInput(prefixSource);
    if (!mask.ok) return { ok: false, error: mask.err };

    var prefix = mask.prefix;
    var maskInt = maskFromPrefix(prefix);
    var ipInt = ip.int;
    var block = pow2(32 - prefix);

    var network = Math.floor(ipInt / block) * block;
    var broadcast = network + block - 1;
    var total = block;
    var usable, firstHost = null, lastHost = null, special = null, notes = [];

    if (prefix <= 30) {
      usable = total - 2;
      firstHost = network + 1;
      lastHost = broadcast - 1;
    } else if (prefix === 31) {
      usable = 0;
      special = '31';
      notes.push('/31 has only 2 addresses. Traditionally there is no usable host range ' +
        '(network and broadcast consume both). RFC 3021 allows both addresses to be used ' +
        'directly on point-to-point links.');
    } else { // /32
      usable = 0;
      special = '32';
      notes.push('/32 is a single address — there is no host range. It is used for host routes ' +
        'and loopback/interface endpoints.');
    }

    var octetIdx = Math.floor(prefix / 8);           // 0..4 (4 only when prefix === 32)
    var rem = prefix % 8;
    var boundary = null;
    if (octetIdx < 4) {
      var boundaryOctetMask = intToOctets(maskInt)[octetIdx];
      boundary = {
        octetNumber: octetIdx + 1,                    // 1-based for humans
        remainingBits: rem,
        blockInOctet: rem === 0 ? 256 : pow2(8 - rem),
        maskOctet: boundaryOctetMask
      };
    }

    var privateRange = privateRangeOf(ipInt);

    return {
      ok: true,
      ip: intToIp(ipInt), ipInt: ipInt, ipOctets: intToOctets(ipInt),
      prefix: prefix, cidr: '/' + prefix,
      maskInt: maskInt, mask: intToIp(maskInt),
      maskForm: mask.form,
      network: intToIp(network), networkInt: network,
      broadcast: intToIp(broadcast), broadcastInt: broadcast,
      firstHost: firstHost === null ? null : intToIp(firstHost),
      lastHost: lastHost === null ? null : intToIp(lastHost),
      total: total, usable: usable,
      isPrivate: !!privateRange, privateRange: privateRange,
      block: block, boundary: boundary, special: special, notes: notes,
      binIP: ipIntBinary(ipInt), binMask: ipIntBinary(maskInt),
      binNetwork: ipIntBinary(network), binBroadcast: ipIntBinary(broadcast)
    };
  }

  /* ---------------- planning helpers (used by question generator) ---------------- */

  // smallest prefix p so that 2^(32-p) - 2 >= hosts  (hosts >= 1)
  function prefixForHosts(hosts) {
    if (!isFinite(hosts) || hosts < 1) return null;
    var need = Math.ceil(Math.log(hosts + 2) / Math.LN2);
    if (need < 2) need = 2;            // at least a /30 (4 addresses, 2 usable)
    if (need > 32) return null;
    return 32 - need;
  }

  // smallest new prefix so that 2^(new - base) >= subnets
  function prefixForSubnets(basePrefix, subnets) {
    if (!isFinite(subnets) || subnets < 1) return null;
    var bits = Math.ceil(Math.log(subnets) / Math.LN2);
    if (bits < 1) bits = 1;
    var p = basePrefix + bits;
    if (p > 32) return null;
    return p;
  }

  /*
    Simple first-fit VLSM allocator (largest requirement first).
    basePrefix: starting network prefix (e.g. 24); network taken from base.
    reqs: [{name, hosts}]
    Returns { ok, allocations, remainingFrom, error }
    Each allocation is aligned by construction (cursor advances in power-of-2
    blocks from an aligned start).
  */
  function vlsmAllocate(basePrefix, baseNetInt, reqs) {
    var size = pow2(32 - basePrefix);
    var start = Math.floor(baseNetInt / size) * size;
    var end = start + size;
    var sorted = reqs.slice().map(function (r, i) {
      return { name: r.name, hosts: r.hosts, order: i };
    }).sort(function (a, b) { return b.hosts - a.hosts; });

    var cursor = start, out = [];
    for (var i = 0; i < sorted.length; i++) {
      var p = prefixForHosts(sorted[i].hosts);
      if (p === null) return { ok: false, error: 'Requirement "' + sorted[i].name + '" is too large.' };
      if (p < basePrefix) {
        return { ok: false, error: 'Requirement "' + sorted[i].name + '" (' + sorted[i].hosts +
          ' hosts) needs a block larger than the whole starting network.' };
      }
      var blk = pow2(32 - p);
      if (cursor + blk > end) {
        return { ok: false, error: 'Requirements do not all fit inside ' + intToIp(start) + '/' + basePrefix + '.' };
      }
      out.push({
        name: sorted[i].name, hosts: sorted[i].hosts, prefix: p, cidr: '/' + p,
        network: intToIp(cursor), networkInt: cursor,
        firstHost: p <= 30 ? intToIp(cursor + 1) : null,
        lastHost: p <= 30 ? intToIp(cursor + blk - 2) : null,
        broadcast: intToIp(cursor + blk - 1),
        size: blk
      });
      cursor += blk;
    }
    return { ok: true, allocations: out, start: intToIp(start), end: intToIp(end - 1),
             remaining: end - cursor };
  }

  /* ---------------- answer helpers ---------------- */

  function normalizeAnswer(s) {
    return String(s === null || s === undefined ? '' : s)
      .toLowerCase()
      .replace(/\s+/g, '')
      .replace(/^\/+/, '')
      .replace(/addresses|address|hosts|host/g, '')
      .trim();
  }

  // split a range answer "a - b" / "a to b" / "a–b"
  function parseRangeAnswer(s) {
    var t = String(s || '').trim();
    var m = t.match(/^(.+?)\s*(?:-|–|—|to)+\s*(.+)$/i);
    if (!m) return null;
    var a = parseIP(m[1].trim()), b = parseIP(m[2].trim());
    if (!a.ok || !b.ok) return null;
    return [a.int, b.int];
  }

  function ipInCalcRange(calcResult, int) {
    return int >= calcResult.networkInt && int <= calcResult.broadcastInt;
  }

  /*
    For a WRONG answer that parses as an IP: give a precise, honest hint
    about where that address sits relative to the correct subnet.
  */
  function explainWrongIp(givenStr, c) {
    var p = parseIP(givenStr);
    if (!p.ok) return '';
    var gi = p.int;
    var block = c.block;
    var gNet = Math.floor(gi / block) * block;
    if (gi === c.networkInt) return ' (' + intToIp(gi) + ' is a network address, but not this one.)';
    if (gi === c.broadcastInt) return ' (' + intToIp(gi) + ' is a broadcast address, but not this one.)';
    if (gi === gNet) {
      return ' (' + intToIp(gi) + ' is the network address of the ' +
        (gNet > c.networkInt ? 'NEXT' : 'PREVIOUS') + ' block — check the block size.)';
    }
    if (ipInCalcRange(c, gi)) return ' (' + intToIp(gi) + ' is INSIDE the correct subnet — ' +
      'look for the subnet boundary instead.)';
    var dist = gNet > c.broadcastInt ? 'after' : 'before';
    return ' (' + intToIp(gi) + ' sits in a different block, ' + dist + ' the correct subnet.)';
  }

  /* ---------------- built-in self test ---------------- */

  function selfTest() {
    var checks = [];
    function is(name, got, want) {
      var okStr = String(got) === String(want);
      checks.push({ name: name, ok: okStr, got: got, want: want });
    }

    // ---- representative prefixes: /0 /8 /16 /24 /30 /31 /32 (hand-computed fixtures) ----
    var c;

    c = calc('8.8.8.8', '/0');
    is('/0 network', c.network, '0.0.0.0');
    is('/0 broadcast', c.broadcast, '255.255.255.255');
    is('/0 total', c.total, 4294967296);
    is('/0 usable', c.usable, 4294967294);
    is('/0 first', c.firstHost, '0.0.0.1');
    is('/0 mask', c.mask, '0.0.0.0');
    is('/0 private(8.8.8.8)', c.isPrivate, false);

    c = calc('11.2.3.4', '/8');
    is('/8 network', c.network, '11.0.0.0');
    is('/8 broadcast', c.broadcast, '11.255.255.255');
    is('/8 total', c.total, 16777216);
    is('/8 usable', c.usable, 16777214);
    is('/8 mask', c.mask, '255.0.0.0');
    is('/8 private(11.x)', c.isPrivate, false);

    c = calc('10.1.2.3', '/16');
    is('/16 network', c.network, '10.1.0.0');
    is('/16 broadcast', c.broadcast, '10.1.255.255');
    is('/16 usable', c.usable, 65534);
    is('/16 mask', c.mask, '255.255.0.0');
    is('/16 private(10.x)', c.isPrivate, true);

    c = calc('192.168.1.77', '255.255.255.0');
    is('/24 network', c.network, '192.168.1.0');
    is('/24 broadcast', c.broadcast, '192.168.1.255');
    is('/24 first', c.firstHost, '192.168.1.1');
    is('/24 last', c.lastHost, '192.168.1.254');
    is('/24 total', c.total, 256);
    is('/24 usable', c.usable, 254);
    is('/24 prefix', c.prefix, 24);
    is('/24 private', c.isPrivate, true);

    c = calc('192.168.5.5', '/30');
    is('/30 network', c.network, '192.168.5.4');
    is('/30 broadcast', c.broadcast, '192.168.5.7');
    is('/30 first', c.firstHost, '192.168.5.5');
    is('/30 last', c.lastHost, '192.168.5.6');
    is('/30 total', c.total, 4);
    is('/30 usable', c.usable, 2);

    c = calc('10.0.0.0', '/31');
    is('/31 network', c.network, '10.0.0.0');
    is('/31 broadcast', c.broadcast, '10.0.0.1');
    is('/31 total', c.total, 2);
    is('/31 usable', c.usable, 0);
    is('/31 first', c.firstHost, null);
    is('/31 special', c.special, '31');

    c = calc('203.0.113.5', '/32');
    is('/32 network', c.network, '203.0.113.5');
    is('/32 broadcast', c.broadcast, '203.0.113.5');
    is('/32 total', c.total, 1);
    is('/32 usable', c.usable, 0);
    is('/32 first', c.firstHost, null);
    is('/32 special', c.special, '32');

    // ---- non-octet-aligned prefixes ----
    c = calc('172.16.0.0', '/13');
    is('/13 network', c.network, '172.16.0.0');
    is('/13 broadcast', c.broadcast, '172.23.255.255');
    is('/13 total', c.total, 524288);
    is('/13 mask', c.mask, '255.248.0.0');

    c = calc('192.168.1.128', '/25');
    is('/25 network', c.network, '192.168.1.128');
    is('/25 broadcast', c.broadcast, '192.168.1.255');
    is('/25 first', c.firstHost, '192.168.1.129');
    is('/25 usable', c.usable, 126);

    c = calc('192.168.1.40', '/27');
    is('/27 network', c.network, '192.168.1.32');
    is('/27 broadcast', c.broadcast, '192.168.1.63');
    is('/27 usable', c.usable, 30);

    // ---- private ranges ----
    is('private 172.16', calc('172.16.5.9', '/24').privateRange, '172.16.0.0/12');
    is('private 172.31', calc('172.31.255.1', '/24').isPrivate, true);
    is('public 172.32', calc('172.32.0.1', '/24').isPrivate, false);
    is('private 192.168', calc('192.168.0.1', '/16').isPrivate, true);
    is('public 192.169', calc('192.169.0.1', '/16').isPrivate, false);

    // ---- mask parsing / validation ----
    is('mask /24 -> dotted', parseMaskInput('/24').prefix, 24);
    is('mask 24 -> dotted', parseMaskInput('24').prefix, 24);
    is('mask dotted -> prefix', parseMaskInput('255.255.255.192').prefix, 26);
    is('mask non-contiguous rejected', parseMaskInput('255.255.0.255').ok, false);
    is('mask 255.255.255.30 rejected', parseMaskInput('255.255.255.30').ok, false);
    is('prefix 33 rejected', parseMaskInput('/33').ok, false);
    is('prefix -1 rejected', parseMaskInput('/-1').ok, false);
    is('empty mask rejected', parseMaskInput('').ok, false);

    // ---- address validation ----
    is('octet 256 rejected', parseIP('1.2.3.256').ok, false);
    is('3 octets rejected', parseIP('192.168.1').ok, false);
    is('letters rejected', parseIP('a.b.c.d').ok, false);
    is('empty rejected', parseIP('').ok, false);
    is('octet empty rejected', parseIP('192.168..1').ok, false);

    // ---- address/prefix in one field ----
    c = calc('192.168.1.10/30', '');
    is('inline prefix network', c.network, '192.168.1.8');
    is('inline prefix usable', c.usable, 2);
    is('mask + inline conflict rejected', calc('10.0.0.1/8', '255.0.0.0').ok, false);

    // ---- planning helpers ----
    is('hosts 254 -> /24', prefixForHosts(254), 24);
    is('hosts 30 -> /27', prefixForHosts(30), 27);
    is('hosts 6 -> /29', prefixForHosts(6), 29);
    is('hosts 2 -> /30', prefixForHosts(2), 30);
    is('hosts 1 -> /30', prefixForHosts(1), 30);
    is('hosts 255 -> /23', prefixForHosts(255), 23);
    is('hosts 0 invalid', prefixForHosts(0), null);
    is('/24 into 6 subnets -> /27', prefixForSubnets(24, 6), 27);
    is('/24 into 4 subnets -> /26', prefixForSubnets(24, 4), 26);
    is('/27 into 8 subnets -> /30', prefixForSubnets(27, 8), 30);
    is('/27 into 16 subnets -> /31', prefixForSubnets(27, 16), 31);
    is('/27 into 64 subnets impossible', prefixForSubnets(27, 64), null);
    is('/31 into 4 subnets impossible', prefixForSubnets(31, 4), null);

    // ---- VLSM ----
    var v = vlsmAllocate(24, octetsToInt([192, 168, 1, 0]), [
      { name: 'LAN A', hosts: 30 }, { name: 'LAN B', hosts: 6 }, { name: 'WAN', hosts: 2 }
    ]);
    is('vlsm ok', v.ok, true);
    is('vlsm LAN A', v.allocations[0].network + ' ' + v.allocations[0].cidr, '192.168.1.0 /27');
    is('vlsm LAN B', v.allocations[1].network + ' ' + v.allocations[1].cidr, '192.168.1.32 /29');
    is('vlsm WAN', v.allocations[2].network + ' ' + v.allocations[2].cidr, '192.168.1.40 /30');

    var vOverflow = vlsmAllocate(24, octetsToInt([192, 168, 1, 0]), [{ name: 'X', hosts: 300 }]);
    is('vlsm overflow rejected', vOverflow.ok, false);

    // ---- internal invariants on a sweep of prefixes ----
    for (var p = 0; p <= 32; p++) {
      var cc = calc('172.16.0.99', '/' + p);
      var blk = pow2(32 - p);
      var inv = true;
      if (cc.networkInt % blk !== 0) inv = false;                 // aligned
      if (cc.broadcastInt - cc.networkInt !== blk - 1) inv = false; // block size
      if (cc.total !== blk) inv = false;
      if (cc.prefix <= 30) {
        if (cc.usable !== blk - 2) inv = false;
        if (cc.firstHost !== intToIp(cc.networkInt + 1)) inv = false;
        if (cc.lastHost !== intToIp(cc.broadcastInt - 1)) inv = false;
        if (!(cc.ipInt >= cc.networkInt && cc.ipInt <= cc.broadcastInt)) inv = false;
      } else {
        if (cc.usable !== 0) inv = false;
      }
      is('invariants /' + p, inv, true);
    }

    var passed = checks.filter(function (c) { return c.ok; }).length;
    var failures = checks.filter(function (c) { return !c.ok; });
    return { total: checks.length, passed: passed, failed: failures.length, failures: failures };
  }

  return {
    TWO32: TWO32,
    pow2: pow2,
    parseIP: parseIP,
    parseMaskInput: parseMaskInput,
    maskFromPrefix: maskFromPrefix,
    prefixFromMaskInt: prefixFromMaskInt,
    maskToDotted: maskToDotted,
    intToIp: intToIp,
    octetsToInt: octetsToInt,
    privateRangeOf: privateRangeOf,
    calc: calc,
    prefixForHosts: prefixForHosts,
    prefixForSubnets: prefixForSubnets,
    vlsmAllocate: vlsmAllocate,
    normalizeAnswer: normalizeAnswer,
    parseRangeAnswer: parseRangeAnswer,
    explainWrongIp: explainWrongIp,
    selfTest: selfTest
  };
});
