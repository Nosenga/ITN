/* ============================================================
   ios.js — Cisco IOS command practice (exam-style drills)
   This file NEVER executes IOS: every item is a static example
   modelled on the course's own IOS transcripts (Ch 6 s.28–30,
   Ch 2 s.25–34, Ch 16 s.28–29). Pure engine (node-testable) +
   DOM wiring for #ios-root on ptlab.html.
   Storage (browser-only, best-effort): itn-ios-stats-v1 holds
   only lifetime counters {answered, correct}.
   UMD: window.IOS / module.exports.
   ============================================================ */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.IOS = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var STORE_KEY = 'itn-ios-stats-v1';

  /* ---------------- item bank (course-grounded) ----------------
     ty:   'select' (choose the command / meaning) or 'fill' (type it)
     kind: 'config' (changes the device) or 'verify' (reads/tests state)
     acc:  accepted fill-in answers; graded after normalisation
           (lowercase, collapsed whitespace, trimmed)
     disp: canonical command shown as the expected answer
     ref:  source label; href: chapter slide anchor
  ---------------------------------------------------------------- */
  var ITEMS = [
    { id: 'ios-01', ty: 'select', kind: 'config',
      ask: 'You are at the privileged EXEC prompt <code>R1#</code>. Which command moves you into <b>global configuration mode</b>?',
      o: ['configure terminal', 'show ip interface brief',
          'copy running-config startup-config', 'ping 209.165.200.226'],
      a: 0, disp: 'configure terminal',
      e: 'Configuration command. The course transcript shows <code>Router# configure terminal</code> → <code>Enter configuration commands, one per line.</code> → <code>R1(config)#</code> — the <code>(config)#</code> prompt confirms global configuration mode. The other choices are verification or configuration-management commands run from EXEC mode.',
      ref: 'Ch 6 · slide 28', href: 'chapter6.html#p28' },

    { id: 'ios-02', ty: 'select', kind: 'config',
      ask: 'Which command renames the device to <code>R1</code> (entered in global configuration mode)?',
      o: ['hostname R1', 'enable secret class',
          'show ip interface brief', 'copy running-config startup-config'],
      a: 0, disp: 'hostname R1',
      e: 'Configuration command. Transcript: <code>Router(config)# hostname R1</code> and the prompt immediately becomes <code>R1(config)#</code>. The other options set a password, verify interfaces, or save the configuration — none changes the device name.',
      ref: 'Ch 6 · slide 28', href: 'chapter6.html#p28' },

    { id: 'ios-03', ty: 'select', kind: 'config',
      ask: 'The course secures privileged EXEC access with an <b>encrypted</b> secret. Which command does the transcript run?',
      o: ['enable secret class', 'enable password class',
          'password cisco', 'service password-encryption'],
      a: 0, disp: 'enable secret class',
      e: 'Configuration command. Transcript: <code>R1(config)# enable secret class</code>. Chapter 2 (s.27) states the rule directly: <i>“Use the enable secret command, not the older enable password command”</i> — it provides greater security because the secret is stored encrypted. <code>password cisco</code> configures line passwords (console/VTY) in the same transcript, not privileged EXEC.',
      ref: 'Ch 6 · slide 28', href: 'chapter6.html#p28' },

    { id: 'ios-04', ty: 'select', kind: 'config',
      ask: 'An interface you configured still shows <code>administratively down</code>. Which command enables it?',
      o: ['no shutdown', 'shutdown', 'enable', 'exit'],
      a: 0, disp: 'no shutdown',
      e: 'Configuration command. After <code>ip address …</code> the transcript runs <code>no shutdown</code> and IOS replies <code>%LINK-5-CHANGED: Interface GigabitEthernet0/0, changed state to up</code>. Chapter 2 (s.34): <i>“no shutdown – Administratively enables the interface.”</i> <code>shutdown</code> does the opposite; <code>enable</code> and <code>exit</code> move between modes.',
      ref: 'Ch 6 · slide 29', href: 'chapter6.html#p29' },

    { id: 'ios-05', ty: 'select', kind: 'config',
      ask: 'Which command saves the running configuration so it survives a reload?',
      o: ['copy running-config startup-config', 'configure terminal',
          'show ip interface brief', 'ping 209.165.200.226'],
      a: 0, disp: 'copy running-config startup-config',
      e: 'Configuration-management command (changes what is stored, so it sits on the configuration side — it is not a <code>show</code> verification command). Transcript: <code>R1# copy running-config startup-config</code> → <code>Destination filename [startup-config]?</code> → <code>Building configuration... [OK]</code>.',
      ref: 'Ch 6 · slide 28', href: 'chapter6.html#p28' },

    { id: 'ios-06', ty: 'select', kind: 'verify',
      ask: 'Which of these is a <b>verification</b> command — it reads state without changing the device?',
      o: ['show ip interface brief', 'configure terminal',
          'no shutdown', 'hostname R1'],
      a: 0, disp: 'show ip interface brief',
      e: 'Verification command: <code>R1# show ip interface brief</code> lists each interface\'s IP address, Status and Protocol and changes nothing. <code>configure terminal</code>, <code>no shutdown</code> and <code>hostname</code> all alter the configuration.',
      ref: 'Ch 6 · slide 30', href: 'chapter6.html#p30' },

    { id: 'ios-07', ty: 'select', kind: 'config',
      ask: 'Which of these is a <b>configuration</b> command — it changes the device?',
      o: ['hostname R1', 'show ip interface brief', 'show ip route',
          'ping 209.165.200.226'],
      a: 0, disp: 'hostname R1',
      e: '<code>hostname</code> writes to the running configuration (a configuration command). <code>show ip interface brief</code> and <code>show ip route</code> only display state, and <code>ping</code> only sends test packets — all three are verification/testing commands.',
      ref: 'Ch 6 · slide 28', href: 'chapter6.html#p28' },

    { id: 'ios-08', ty: 'select', kind: 'verify',
      ask: 'In <code>show ip interface brief</code>, interface <code>Serial0/0/1</code> shows <code>unassigned</code>, Status <code>administratively down</code>, Protocol <code>down</code>. What does that mean?',
      o: ['The interface was disabled by configuration and has no IP address',
          'The cable is unplugged but the configuration is correct',
          'The interface is working normally',
          'The router is still booting'],
      a: 0, disp: 'Disabled by configuration, no IP address',
      e: 'Reading verification output: <i>administratively down</i> means the interface was shut down in configuration (missing <code>no shutdown</code> or an explicit <code>shutdown</code>), and <i>unassigned</i> means no <code>ip address</code> is configured. Working interfaces in the same table read <code>up / up</code>. PT Prep Lab 4 uses exactly this fault pattern.',
      ref: 'Ch 6 · slide 30', href: 'chapter6.html#p30' },

    { id: 'ios-09', ty: 'select', kind: 'verify',
      ask: 'A ping replies <code>Sending 5, 100-byte ICMP Echos …: !!!!! Success rate is 100 percent (5/5)</code>. What does it show?',
      o: ['All 5 echo replies arrived — the target is reachable',
          'All 5 packets were lost',
          'Only 2 of the 5 replies arrived',
          'The ping command failed because it is not allowed here'],
      a: 0, disp: 'All 5 replies arrived (reachable)',
      e: 'Verification/testing command: each <code>!</code> is one reply; five of five with <code>Success rate is 100 percent (5/5)</code> means full reachability. The course transcript pings <code>209.165.200.226</code> and gets exactly that result (a <code>.</code> would be a timeout).',
      ref: 'Ch 6 · slide 30', href: 'chapter6.html#p30' },

    { id: 'ios-10', ty: 'select', kind: 'config',
      ask: 'From interface configuration mode <code>R1(config-if)#</code>, which command returns you to global configuration mode <code>R1(config)#</code>?',
      o: ['exit', 'show ip interface brief', 'enable',
          'copy running-config startup-config'],
      a: 0, disp: 'exit',
      e: 'Mode-navigation (configuration side): every configuration block in the transcript ends with <code>exit</code> to step back one level — e.g. <code>… changed state to up R1(config-if)# exit R1(config)#</code>. The other choices either cannot run in configuration mode or would leave it to EXEC mode.',
      ref: 'Ch 6 · slide 29', href: 'chapter6.html#p29' },

    { id: 'ios-11', ty: 'fill', kind: 'config',
      ctx: 'R1#',
      ask: 'Type the command from the course transcript that enters global configuration mode (the transcript uses its abbreviation on this line).',
      acc: ['conf t', 'configure terminal'], disp: 'configure terminal',
      e: 'Configuration command. The transcript opens LAN configuration with <code>R1# conf t</code> (abbreviation of <code>configure terminal</code>, shown in full on the Router Configuration Steps slide). Both the full form and the abbreviation shown in the course are accepted here.',
      ref: 'Ch 6 · slide 29', href: 'chapter6.html#p29' },

    { id: 'ios-12', ty: 'fill', kind: 'config',
      ctx: 'R1(config)#',
      ask: 'Type the command that renames this device to <code>R1</code>.',
      acc: ['hostname R1'], disp: 'hostname R1',
      e: 'Configuration command: <code>Router(config)# hostname R1</code> — the prompt itself changes to <code>R1(config)#</code>, so you can see the effect immediately.',
      ref: 'Ch 6 · slide 28', href: 'chapter6.html#p28' },

    { id: 'ios-13', ty: 'fill', kind: 'config',
      ctx: 'R1(config)#',
      ask: 'Type the command that opens the configuration mode of interface <code>GigabitEthernet0/0</code>.',
      acc: ['interface GigabitEthernet 0/0', 'interface GigabitEthernet0/0',
            'interface g0/0', 'int g0/0', 'int GigabitEthernet 0/0'],
      disp: 'interface GigabitEthernet 0/0',
      e: 'Configuration command — interface configuration mode: transcript <code>R1(config)# interface gigabitethernet 0/0</code> → prompt <code>R1(config-if)#</code>. IOS accepts the course\'s abbreviations too (<code>int g0/1</code> appears for the second interface), so abbreviated forms of this same command are accepted.',
      ref: 'Ch 6 · slide 29', href: 'chapter6.html#p29' },

    { id: 'ios-14', ty: 'fill', kind: 'config',
      ctx: 'R1(config-if)#  (GigabitEthernet0/0)',
      ask: 'Type the command that assigns <code>192.168.10.1</code> with mask <code>255.255.255.0</code> to this interface.',
      acc: ['ip address 192.168.10.1 255.255.255.0',
            'ip add 192.168.10.1 255.255.255.0'],
      disp: 'ip address 192.168.10.1 255.255.255.0',
      e: 'Configuration command — the address and mask must both be given in one line: transcript <code>R1(config-if)# ip address 192.168.10.1 255.255.255.0</code>. The abbreviation <code>ip add …</code> is used for the second interface in the same transcript and is accepted.',
      ref: 'Ch 6 · slide 29', href: 'chapter6.html#p29' },

    { id: 'ios-15', ty: 'fill', kind: 'config',
      ctx: 'R1(config-if)#',
      ask: 'Type the command that labels this interface <code>Link to LAN-10</code>.',
      acc: ['description Link to LAN-10', 'des Link to LAN-10'],
      disp: 'description Link to LAN-10',
      e: 'Configuration command — <code>description</code> stores a label shown in configs and <code>show</code> output; it does not affect traffic. Transcript: <code>R1(config-if)# description Link to LAN-10</code> (with the abbreviation <code>des Link to LAN-11</code> on the next interface).',
      ref: 'Ch 6 · slide 29', href: 'chapter6.html#p29' },

    { id: 'ios-16', ty: 'fill', kind: 'config',
      ctx: 'R1(config-if)#',
      ask: 'Type the command that administratively enables this interface (the opposite of <code>shutdown</code>).',
      acc: ['no shutdown', 'no shut'], disp: 'no shutdown',
      e: 'Configuration command: transcript <code>R1(config-if)# no shutdown</code> → <code>%LINK-5-CHANGED: Interface GigabitEthernet0/0, changed state to up</code>. The transcript\'s own abbreviation <code>no shut</code> is also accepted. Without it, verification shows <code>administratively down</code>.',
      ref: 'Ch 6 · slide 29', href: 'chapter6.html#p29' },

    { id: 'ios-17', ty: 'fill', kind: 'config',
      ctx: 'R1#',
      ask: 'Type the command that saves the current configuration to NVRAM so it survives a reload.',
      acc: ['copy running-config startup-config'],
      disp: 'copy running-config startup-config',
      e: 'Configuration-management command (not a verification <code>show</code>): transcript <code>R1# copy running-config startup-config</code> → <code>Destination filename [startup-config]?</code> → <code>Building configuration... [OK]</code>. It writes the running configuration into the startup configuration.',
      ref: 'Ch 6 · slide 28', href: 'chapter6.html#p28' },

    { id: 'ios-18', ty: 'fill', kind: 'verify',
      ctx: 'R1#',
      ask: 'Type the verification command that lists every interface\'s IP address, Status and Protocol in one table.',
      acc: ['show ip interface brief'], disp: 'show ip interface brief',
      e: 'Verification command — reads only, changes nothing: transcript <code>R1# show ip interface brief</code> produces the table with <code>Status</code> and <code>Protocol</code> columns (rows such as <code>GigabitEthernet0/0 … up up</code>). The course transcript uses the full form; that exact command is expected here.',
      ref: 'Ch 6 · slide 30', href: 'chapter6.html#p30' },

    { id: 'ios-19', ty: 'fill', kind: 'verify',
      ctx: 'R1#',
      ask: 'Type the command from the transcript that tests reachability to <code>209.165.200.226</code>.',
      acc: ['ping 209.165.200.226'], disp: 'ping 209.165.200.226',
      e: 'Verification/testing command — it sends test packets and changes no configuration: transcript <code>R1# ping 209.165.200.226</code> → <code>!!!!! Success rate is 100 percent (5/5)</code>.',
      ref: 'Ch 6 · slide 30', href: 'chapter6.html#p30' },

    { id: 'ios-20', ty: 'fill', kind: 'config',
      ctx: 'R1(config)#',
      ask: 'Type the command that begins console-port line configuration.',
      acc: ['line console 0'], disp: 'line console 0',
      e: 'Configuration command — it moves from global config to line configuration mode: transcript <code>R1(config)# line console 0</code> → <code>R1(config-line)# password cisco</code> → <code>login</code> → <code>exit</code>.',
      ref: 'Ch 6 · slide 28', href: 'chapter6.html#p28' }
  ];

  /* ---------------- grading ---------------- */

  function norm(s) {
    return String(s == null ? '' : s)
      .replace(/\s+/g, ' ')
      .trim()
      .toLowerCase();
  }

  function check(item, given) {
    if (!item) { return { ok: false, display: '' }; }
    if (item.ty === 'select') {
      var idx = typeof given === 'number' ? given : parseInt(given, 10);
      return {
        ok: idx === item.a,
        display: item.disp || (item.o ? item.o[item.a] : '')
      };
    }
    var g = norm(given);
    if (!g) { return { ok: false, display: item.disp }; }
    var acc = item.acc || [];
    for (var i = 0; i < acc.length; i++) {
      if (norm(acc[i]) === g) { return { ok: true, display: item.disp }; }
    }
    return { ok: false, display: item.disp };
  }

  /* ---------------- session engine (mirrors lab.js quiz flow) ---------------- */

  function shuffle(arr, rng) {
    rng = rng || Math.random;
    var out = arr.slice();
    for (var i = out.length - 1; i > 0; i--) {
      var j = Math.floor(rng() * (i + 1));
      var t = out[i]; out[i] = out[j]; out[j] = t;
    }
    return out;
  }

  function createSession(opts) {
    opts = opts || {};
    var pool = ITEMS.slice();
    var qs = opts.ids
      ? opts.ids.map(function (id) {
          for (var i = 0; i < ITEMS.length; i++) {
            if (ITEMS[i].id === id) { return ITEMS[i]; }
          }
          return null;
        }).filter(Boolean)
      : shuffle(pool, opts.rng);
    return {
      questions: qs,
      index: 0,
      results: [],                       // {id, ok, kind, ty}
      checked: false,
      lastGrade: null,
      totals: { answered: 0, correct: 0 }
    };
  }

  function currentQuestion(session) {
    if (!session || !session.questions) { return null; }
    return session.questions[session.index] || null;
  }

  function submit(session, given) {
    var q = currentQuestion(session);
    if (!q || session.checked) { return null; }
    var res = check(q, given);
    session.checked = true;
    session.lastGrade = {
      ok: res.ok,
      given: q.ty === 'select' ? given : String(given == null ? '' : given).trim(),
      display: res.display
    };
    session.results.push({ id: q.id, ok: res.ok, kind: q.kind, ty: q.ty });
    session.totals.answered++;
    if (res.ok) { session.totals.correct++; }
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
      overallAccuracy: acc,
      overallAnswered: session.totals.answered,
      overallCorrect: session.totals.correct
    };
  }

  function retryMisses(session) {
    var st = stats(session);
    var miss = session.questions.filter(function (q) {
      return st.wrongIds.indexOf(q.id) >= 0;
    });
    return {
      questions: miss, index: 0, results: [], checked: false,
      lastGrade: null, totals: session.totals
    };
  }

  /* ---------------- lifetime totals (optional localStorage) ---------------- */

  function loadTotals(store) {
    if (!store) { return null; }
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
    if (!store || !totals) { return false; }
    try {
      store.setItem(STORE_KEY, JSON.stringify({
        v: 1, answered: totals.answered, correct: totals.correct
      }));
      return true;
    } catch (e) { return false; }
  }

  /* ---------------- DOM wiring (ptlab.html #ios-root) ---------------- */

  function init(doc, storage) {
    var rootEl = doc.getElementById('ios-root');
    if (!rootEl) { return null; }

    var store = storage || null;
    var lifeTotals = loadTotals(store);
    var session = null;

    function $(id) { return doc.getElementById(id); }

    function statsLine() {
      if (!session || !session.totals.answered) { return ''; }
      var t = session.totals;
      return '<b>Set:</b> ' + stats(session).correct + '/' +
        stats(session).answered + ' correct &nbsp;·&nbsp; <b>Lifetime:</b> ' +
        t.correct + '/' + t.answered + ' (' +
        (t.answered ? Math.round(1000 * t.correct / t.answered) / 10 : 0) + '%)';
    }

    function renderStage() {
      var q = currentQuestion(session);
      var stage = $('ios-stage');
      if (!q) {
        var s = stats(session);
        $('ios-progress').textContent = 'Set complete';
        $('ios-kind').textContent = '';
        $('ios-kind').className = 'ios-kind';
        $('ios-ask').innerHTML = '<p>Set finished — <b>' + s.correct + '/' +
          s.total + '</b> correct' + (s.wrongCount
            ? ', ' + s.wrongCount + ' to retry.' : '.') + '</p>';
        $('ios-input-wrap').hidden = true;
        $('ios-opts').hidden = true;
        $('ios-opts').innerHTML = '';
        $('ios-check').hidden = true;
        $('ios-feedback').innerHTML = '';
        $('ios-next').hidden = true;
        $('ios-retry').hidden = s.wrongCount === 0;
        $('ios-again').hidden = false;
        $('ios-stats').innerHTML = statsLine();
        stage.hidden = false;
        return;
      }
      stage.hidden = false;
      $('ios-check').hidden = false;
      $('ios-retry').hidden = true;
      $('ios-again').hidden = true;
      $('ios-progress').textContent = 'Question ' + (session.index + 1) +
        ' of ' + session.questions.length;
      var kindEl = $('ios-kind');
      kindEl.textContent = q.kind === 'config'
        ? 'Configuration command' : 'Verification command';
      kindEl.className = 'ios-kind kind-' + q.kind;
      $('ios-ask').innerHTML = (q.ctx
        ? '<p class="ios-prompt"><code>' + q.ctx.replace(/</g, '&lt;') + '</code></p>'
        : '') + '<p>' + q.ask + '</p>';
      var fb = $('ios-feedback');
      fb.innerHTML = '';
      $('ios-next').hidden = true;
      $('ios-check').disabled = false;
      var optsWrap = $('ios-opts'), inpWrap = $('ios-input-wrap');
      if (q.ty === 'select') {
        inpWrap.hidden = true;
        optsWrap.hidden = false;
        optsWrap.innerHTML = '';
        q.o.forEach(function (o, idx) {
          var b = doc.createElement('button');
          b.type = 'button';
          b.className = 'ios-opt';
          b.setAttribute('data-idx', String(idx));
          b.innerHTML = '<code>' + o.replace(/</g, '&lt;') + '</code>';
          b.addEventListener('click', function () {
            var all = optsWrap.querySelectorAll('.ios-opt');
            for (var i = 0; i < all.length; i++) {
              all[i].classList.remove('is-on');
              all[i].setAttribute('aria-pressed', 'false');
            }
            b.classList.add('is-on');
            b.setAttribute('aria-pressed', 'true');
            session.picked = idx;
            $('ios-check').disabled = false;
          });
          optsWrap.appendChild(b);
        });
        session.picked = -1;
        $('ios-check').disabled = true;
      } else {
        optsWrap.hidden = true;
        optsWrap.innerHTML = '';
        inpWrap.hidden = false;
        var inp = $('ios-input');
        inp.value = '';
        inp.focus();
      }
      $('ios-stats').innerHTML = statsLine();
    }

    function checkFn() {
      var q = currentQuestion(session);
      if (!q || session.checked) { return; }
      var given = q.ty === 'select' ? session.picked : $('ios-input').value;
      if (q.ty === 'select' && (given == null || given < 0)) { return; }
      if (q.ty === 'fill' && !String(given).trim()) { return; }
      var g = submit(session, given);
      if (!g) { return; }
      $('ios-check').disabled = true;
      var kindLabel = q.kind === 'config'
        ? 'Configuration' : 'Verification';
      var fb = $('ios-feedback');
      var head = g.ok
        ? '<div class="fb-ok">✓ Correct</div>'
        : '<div class="fb-bad">✗ Not quite. ' +
          (q.ty === 'select'
            ? (g.given != null && g.given >= 0 && q.o[g.given]
                ? 'Your answer: <code>' +
                  String(q.o[g.given]).replace(/</g, '&lt;') + '</code>. '
                : '')
            : 'Your answer: <code>' +
              String(g.given).replace(/&/g, '&amp;').replace(/</g, '&lt;') +
              '</code>. ') +
          'Expected: <b>' + String(g.display).replace(/</g, '&lt;') + '</b>.</div>';
      fb.innerHTML = head +
        '<div class="ios-exp"><span class="ios-kind kind-' + q.kind + '">' +
        kindLabel + ' command</span> ' + q.e +
        ' <span class="ex-src-inline"><a href="' + q.href + '">Course · ' +
        q.ref + '</a></span></div>';
      if (q.ty === 'fill') {
        var inp = $('ios-input');
        inp.disabled = true;
      } else {
        var btns = $('ios-opts').querySelectorAll('.ios-opt');
        for (var i = 0; i < btns.length; i++) { btns[i].disabled = true; }
      }
      $('ios-next').hidden = false;
      $('ios-next').textContent = (session.index + 1 >= session.questions.length)
        ? 'Finish set →' : 'Next command →';
      $('ios-stats').innerHTML = statsLine();
      lifeTotals = session.totals;
      saveTotals(store, session.totals);
    }

    var startBtn = $('ios-start');
    if (!startBtn) { return null; }
    startBtn.addEventListener('click', function (ev) {
      ev.preventDefault();
      session = createSession();
      if (lifeTotals) { session.totals = lifeTotals; }
      renderStage();
    });
    $('ios-check').addEventListener('click', function (ev) {
      ev.preventDefault(); checkFn();
    });
    $('ios-input').addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') { ev.preventDefault(); if (session && !session.checked) { checkFn(); } }
    });
    $('ios-next').addEventListener('click', function (ev) {
      ev.preventDefault();
      if (!session) { return; }
      var inp = $('ios-input');
      if (inp) { inp.disabled = false; }
      advance(session);
      renderStage();
    });
    $('ios-retry').addEventListener('click', function (ev) {
      ev.preventDefault();
      if (!session) { return; }
      var miss = retryMisses(session);
      if (!miss.questions.length) { return; }
      session = miss;
      renderStage();
    });
    $('ios-again').addEventListener('click', function (ev) {
      ev.preventDefault();
      session = createSession();
      if (lifeTotals) { session.totals = lifeTotals; }
      renderStage();
    });

    $('ios-stats').innerHTML = lifeTotals
      ? '<b>Lifetime:</b> ' + lifeTotals.correct + '/' + lifeTotals.answered +
        ' correct across previous sets (stored in this browser).'
      : '';

    return {
      get session() { return session; },
      start: function () {
        session = createSession();
        if (lifeTotals) { session.totals = lifeTotals; }
        renderStage();
      }
    };
  }

  if (typeof document !== 'undefined' && document.addEventListener) {
    document.addEventListener('DOMContentLoaded', function () {
      try {
        if (document.getElementById('ios-root') && typeof localStorage !== 'undefined') {
          init(document, localStorage);
        }
      } catch (e) { /* not the ios section */ }
    });
  }

  return {
    ITEMS: ITEMS,
    STORE_KEY: STORE_KEY,
    norm: norm,
    check: check,
    shuffle: shuffle,
    createSession: createSession,
    currentQuestion: currentQuestion,
    submit: submit,
    advance: advance,
    stats: stats,
    retryMisses: retryMisses,
    loadTotals: loadTotals,
    saveTotals: saveTotals,
    init: init
  };
}));
