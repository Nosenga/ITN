/* ============================================================
   Exam Practice Mode (exam.html)
   Pure engine (tested) + DOM wiring (stub-testable).
   Storage: localStorage keys itn-exam-session-v1 / itn-exam-history-v1.
   UMD-lite: window.EXAM / module.exports. No DOM access at load time.
   ============================================================ */
(function (global) {
  'use strict';

  var SESSION_KEY = 'itn-exam-session-v1';
  var HISTORY_KEY = 'itn-exam-history-v1';
  var V = 1;
  var HISTORY_CAP = 20;
  var TYPE_LABEL = {
    mc: 'Multiple choice', tf: 'True / false', short: 'Short answer',
    term: 'Networking terminology', calc: 'Calculation', trouble: 'Troubleshooting'
  };
  var CHOICE = { mc: 1, tf: 1, term: 1, trouble: 1 };

  /* ---------------- pure helpers ---------------- */

  function normalize(s) {
    s = String(s == null ? '' : s).toLowerCase();
    s = s.replace(/\u2212/g, '-')      // unicode minus
         .replace(/[\u2018\u2019]/g, "'")
         .replace(/\s+/g, ' ')
         .replace(/[!?;"'`]/g, '')
         .trim();
    return s;
  }

  function tokens(s) {
    return normalize(s).split(/[^a-z0-9.^]+/).filter(Boolean);
  }

  // Text grading: any one spec present on the question.
  //  {acc:[..]}  equality, or substring when variant length >= 3
  //  {must:[..]} every substring (len>=3) must appear (or exact token for short)
  //  {g:[[aliases]], n:k}  k alias-groups must match
  //  {num:k}  first number in the input must equal k
  function grade(q, input) {
    var gr = q.gr || {};
    var raw = normalize(input);
    var toks = tokens(input);
    if (gr.num != null) {
      var m = String(input == null ? '' : input).replace(',', '.').match(/-?\d+(\.\d+)?/);
      if (!m) { return false; }
      return Number(m[0]) === gr.num;
    }
    if (gr.acc) {
      for (var i = 0; i < gr.acc.length; i++) {
        var v = normalize(gr.acc[i]);
        if (raw === v) { return true; }
        if (v.length >= 3 && raw.indexOf(v) !== -1) { return true; }
      }
      return false;
    }
    if (gr.must) {
      for (var j = 0; j < gr.must.length; j++) {
        var w = normalize(gr.must[j]);
        var hit = w.length >= 3 ? raw.indexOf(w) !== -1 : toks.indexOf(w) !== -1;
        if (!hit) { return false; }
      }
      return true;
    }
    if (gr.g) {
      var n = gr.n || gr.g.length, hitCount = 0;
      for (var k = 0; k < gr.g.length; k++) {
        var aliases = gr.g[k], ok = false;
        for (var a = 0; a < aliases.length; a++) {
          var al = normalize(aliases[a]);
          if (al.length >= 3 ? raw.indexOf(al) !== -1 : toks.indexOf(al) !== -1) {
            ok = true; break;
          }
        }
        if (ok) { hitCount++; }
      }
      return hitCount >= n;
    }
    return false;
  }

  function gradeChoice(q, pickedIdx) {
    return pickedIdx === q.a;
  }

  function shuffle(arr, rng) {
    rng = rng || Math.random;
    var out = arr.slice();
    for (var i = out.length - 1; i > 0; i--) {
      var j = Math.floor(rng() * (i + 1));
      var t = out[i]; out[i] = out[j]; out[j] = t;
    }
    return out;
  }

  function indexBank(bank) {
    var m = {};
    for (var i = 0; i < bank.length; i++) { m[bank[i].i] = bank[i]; }
    return m;
  }

  function topicPool(bank, topic) {
    return bank.filter(function (b) { return b.tp === topic; });
  }

  function poolFor(bank, chapters) {
    var set = {};
    for (var i = 0; i < chapters.length; i++) { set[chapters[i]] = 1; }
    return bank.filter(function (b) {
      for (var j = 0; j < b.c.length; j++) { if (set[b.c[j]]) { return true; } }
      return false;
    });
  }

  /* Weak-topic → suggested next revision activity (course pages only).
     Order matters: first matching rule wins. */
  var REC_RULES = [
    { m: ['subnet', 'addressing'],
      label: 'practise in the IPv4 Lab — generated drills with full worked solutions',
      href: 'lab.html' },
    { m: ['troubleshoot'],
      label: 'work PT Prep Lab 4 (wrong IPs, gateways, interface faults)',
      href: 'ptlab.html#lab4' },
    { m: ['security'], label: 're-read Network Security (Ch 16), then retry',
      href: 'chapter16.html' },
    { m: ['switch'], label: 'revise Switching & ARP (Ch 5), then retry',
      href: 'chapter5.html' },
    { m: ['transport'], label: 'revise the Transport layer (Ch 7), then retry',
      href: 'chapter7.html' },
    { m: ['application'], label: 'revise the Application layer (Ch 10), then retry',
      href: 'chapter10.html' },
    { m: ['osi', 'tcp/ip', 'models'], label: 'revise OSI & TCP/IP models (Ch 3), then retry',
      href: 'chapter3.html' },
    { m: ['cable', 'media'], label: 'revise cabling & media (Ch 4), then retry',
      href: 'chapter4.html' },
    { m: ['routing', 'ipv4'], label: 'revisit IPv4 & routing basics (Ch 6), then retry',
      href: 'chapter6.html' },
    { m: ['devices'], label: 'revisit network devices (Ch 2), then retry',
      href: 'chapter2.html' },
    { m: ['fundamentals'], label: 'revisit network fundamentals (Ch 1), then retry',
      href: 'chapter1.html' }
  ];

  function recFor(topic) {
    var t = String(topic == null ? '' : topic).toLowerCase();
    for (var i = 0; i < REC_RULES.length; i++) {
      for (var j = 0; j < REC_RULES[i].m.length; j++) {
        if (t.indexOf(REC_RULES[i].m[j]) !== -1) { return REC_RULES[i]; }
      }
    }
    return null;
  }

  function lengthsAvailable(poolSize, lens) {
    lens = lens || [10, 20, 30];
    return lens.filter(function (l) { return poolSize >= l; });
  }

  function remainingSec(endTs, now) {
    if (endTs == null) { return null; }
    return Math.max(0, Math.ceil((endTs - now) / 1000));
  }

  function buildSession(bank, cfg, now, rng) {
    now = now || Date.now();
    var map = indexBank(bank);
    var pool = cfg.topic ? topicPool(bank, cfg.topic) : poolFor(bank, cfg.ch);
    var ids = shuffle(pool.map(function (b) { return b.i; }), rng)
      .slice(0, Math.min(cfg.len, pool.length));
    var items = ids.map(function (id) {
      var q = map[id];
      if (CHOICE[q.ty]) {
        if (q.ty === 'tf') {
          return { id: id, opts: q.o.slice(), correct: q.a };
        }
        var presented = shuffle(q.o, rng);
        return { id: id, opts: presented, correct: presented.indexOf(q.o[q.a]) };
      }
      return { id: id };
    });
    var perQ = cfg.mode === 'untimed' ? null : Number(cfg.mode);
    return {
      v: V, stage: 'quiz', ch: cfg.ch.slice(), mode: cfg.mode,
      topic: cfg.topic || null,
      items: items, ans: items.map(function () { return null; }),
      i: 0, draft: '',
      endTs: perQ ? now + items.length * perQ * 1000 : null,
      started: new Date(now).toISOString(), saved: false
    };
  }

  function scoreSession(sess) {
    var correct = 0;
    for (var i = 0; i < sess.ans.length; i++) {
      if (sess.ans[i] && sess.ans[i].ok) { correct++; }
    }
    var total = sess.items.length;
    return { correct: correct, total: total,
             pct: total ? Math.round(correct * 100 / total) : 0 };
  }

  function topicMisses(bank, sess) {
    var map = indexBank(bank), out = {};
    for (var i = 0; i < sess.items.length; i++) {
      var q = map[sess.items[i].id];
      var tp = q.tp;
      if (!out[tp]) { out[tp] = { tp: tp, wrong: 0, total: 0 }; }
      out[tp].total++;
      if (sess.ans[i] && !sess.ans[i].ok) { out[tp].wrong++; }
    }
    return out;
  }

  function weakTopics(bank, sess, topN) {
    topN = topN || 3;
    var groups = topicMisses(bank, sess), list = [];
    for (var k in groups) {
      if (Object.prototype.hasOwnProperty.call(groups, k) && groups[k].wrong > 0) {
        list.push(groups[k]);
      }
    }
    list.sort(function (a, b) {
      if (b.wrong !== a.wrong) { return b.wrong - a.wrong; }
      return (b.wrong / b.total) - (a.wrong / a.total);
    });
    return list.slice(0, topN);
  }

  function retryIds(sess) {
    var out = [];
    for (var i = 0; i < sess.items.length; i++) {
      if (sess.ans[i] && !sess.ans[i].ok) { out.push(sess.items[i].id); }
    }
    return out;
  }

  /* ---------------- history ---------------- */

  function pushHistory(raw, entry) {
    var hist = [];
    try {
      var p = JSON.parse(raw);
      if (p && p.v === V && Object.prototype.toString.call(p.r) === '[object Array]') {
        hist = p.r;
      }
    } catch (e) { /* corrupted → start clean */ }
    hist.unshift(entry);
    hist = hist.slice(0, HISTORY_CAP);
    return JSON.stringify({ v: V, r: hist });
  }

  /* ---------------- session validation (refresh safety) ---------------- */

  function validSession(raw, bank) {
    var s;
    try { s = JSON.parse(raw); } catch (e) { return null; }
    if (!s || typeof s !== 'object') { return null; }
    if (s.v !== V) { return null; }
    if (s.stage !== 'quiz' && s.stage !== 'results') { return null; }
    if (s.mode !== 'untimed' && s.mode !== '30' && s.mode !== '60') { return null; }
    if (Object.prototype.toString.call(s.ch) !== '[object Array]' || !s.ch.length) {
      return null;
    }
    if (s.topic != null && typeof s.topic !== 'string') { return null; }
    if (Object.prototype.toString.call(s.items) !== '[object Array]' || !s.items.length) {
      return null;
    }
    if (Object.prototype.toString.call(s.ans) !== '[object Array]' ||
        s.ans.length !== s.items.length) { return null; }
    if (typeof s.i !== 'number' || s.i < 0 || s.i >= s.items.length) { return null; }
    if (s.endTs != null && typeof s.endTs !== 'number') { return null; }
    if (typeof s.draft !== 'string') { return null; }

    var map = indexBank(bank);
    for (var i = 0; i < s.items.length; i++) {
      var it = s.items[i];
      if (!it || typeof it.id !== 'string' || !map[it.id]) { return null; }
      var q = map[it.id];
      if (CHOICE[q.ty]) {
        // materialized options must be a faithful permutation of the bank's
        if (!Array.isArray(it.opts) || it.opts.length !== q.o.length) { return null; }
        var sorted1 = it.opts.slice().sort().join('\u0001');
        var sorted2 = q.o.slice().sort().join('\u0001');
        if (sorted1 !== sorted2) { return null; }
        if (typeof it.correct !== 'number' || it.correct < 0 ||
            it.correct >= it.opts.length) { return null; }
        if (it.opts[it.correct] !== q.o[q.a]) { return null; }
      } else if (it.opts != null || it.correct != null) { return null; }
      var a = s.ans[i];
      if (a !== null && !(a && typeof a === 'object' && typeof a.ok === 'boolean')) {
        return null;
      }
    }
    return s;
  }

  /* ---------------- DOM wiring ---------------- */

  function init(root, bank, storage, nowFn, setIntervalFn, clearIntervalFn) {
    nowFn = nowFn || function () { return Date.now(); };
    var map = indexBank(bank);
    var sess = null;
    var pickedOpts = -1;
    var timerHandle = null;
    var tickFn = null;

    function byId(id) { return root.getElementById(id); }
    function save() {
      if (sess) { storage.setItem(SESSION_KEY, JSON.stringify(sess)); }
    }
    function clearSession() {
      sess = null;
      try { storage.removeItem(SESSION_KEY); } catch (e) {}
    }
    function show(name) {
      ['setup', 'quiz', 'results'].forEach(function (s) {
        var el = byId('ex-' + s);
        if (el) { el.hidden = (s !== name); }
      });
    }
    function stopTimer() {
      if (timerHandle != null && clearIntervalFn) {
        clearIntervalFn(timerHandle);
        timerHandle = null;
      }
    }
    function startTicking() {
      stopTimer();
      if (sess && sess.endTs != null && setIntervalFn) {
        tickFn = function () { tick(nowFn()); };
        timerHandle = setIntervalFn(tickFn, 250);
      }
    }
    function fmt(sec) {
      var m = Math.floor(sec / 60), s2 = sec % 60;
      return (m < 10 ? '0' : '') + m + ':' + (s2 < 10 ? '0' : '') + s2;
    }
    function tick(now) {
      if (!sess || sess.stage !== 'quiz' || sess.endTs == null) { return; }
      var rem = remainingSec(sess.endTs, now);
      var t = byId('ex-timer');
      if (t) { t.textContent = '⏱ ' + fmt(rem); }
      if (rem <= 0) { finish(true); }
    }

    /* ---------- setup screen ---------- */
    function selectedChapters() {
      var boxes = root.querySelectorAll('input[data-ch]'), out = [];
      for (var i = 0; i < boxes.length; i++) {
        if (boxes[i].checked) { out.push(Number(boxes[i].getAttribute('data-ch'))); }
      }
      return out;
    }
    function syncAll() {
      var boxes = root.querySelectorAll('input[data-ch]');
      var all = byId('ex-all');
      var allOn = true, someOn = false;
      for (var i = 0; i < boxes.length; i++) {
        if (boxes[i].checked) { someOn = true; } else { allOn = false; }
      }
      if (all) { all.checked = allOn; }
      return { boxes: boxes, someOn: someOn, allOn: allOn };
    }
    function syncSetup() {
      var st = syncAll();
      var chs = selectedChapters();
      var pool = poolFor(bank, chs);
      var avail = lengthsAvailable(pool.length);
      var btns = byId('ex-lens').querySelectorAll('button[data-len]');
      for (var i = 0; i < btns.length; i++) {
        var L = Number(btns[i].getAttribute('data-len'));
        var on = avail.indexOf(L) !== -1;
        btns[i].disabled = !on;
        if (on) {
          btns[i].classList.remove('is-off');
        } else {
          btns[i].classList.add('is-off');
          btns[i].classList.remove('is-on');   // never leave a disabled pick active
        }
      }
      // ensure exactly one available length stays selected
      var anyOn = false;
      for (var s = 0; s < btns.length; s++) {
        if (btns[s].classList.contains('is-on') && !btns[s].disabled) { anyOn = true; }
      }
      if (!anyOn && avail.length) {
        var firstAvail = avail[0];
        for (var f = 0; f < btns.length; f++) {
          if (Number(btns[f].getAttribute('data-len')) === firstAvail) {
            btns[f].classList.add('is-on');
          }
        }
      }
      // keep a valid length selected: default first available
      var note = byId('ex-pool-note');
      if (note) {
        note.textContent = chs.length
          ? pool.length + ' questions available for ' + chs.length +
            ' chapter' + (chs.length > 1 ? 's' : '') + ' — session lengths offered ' +
            'up to ' + (avail.length ? Math.max.apply(null, avail) : 0) + '.'
          : 'Select at least one chapter.';
      }
      var start = byId('ex-start');
      if (start) { start.disabled = !chs.length || !avail.length; }
      return avail;
    }
    function currentCfg() {
      var chs = selectedChapters();
      var pool = poolFor(bank, chs);
      var avail = lengthsAvailable(pool.length);
      var btns = byId('ex-lens').querySelectorAll('button[data-len]');
      var len = avail[0] || 10;
      for (var i = 0; i < btns.length; i++) {
        if (btns[i].classList.contains('is-on') &&
            avail.indexOf(Number(btns[i].getAttribute('data-len'))) !== -1) {
          len = Number(btns[i].getAttribute('data-len'));
        }
      }
      var mbtns = byId('ex-modes').querySelectorAll('button[data-mode]');
      var mode = 'untimed';
      for (var j = 0; j < mbtns.length; j++) {
        if (mbtns[j].classList.contains('is-on')) {
          mode = mbtns[j].getAttribute('data-mode');
        }
      }
      return { ch: chs, len: Math.min(len, pool.length), mode: mode };
    }

    function renderHistory() {
      var raw = null;
      try { raw = storage.getItem(HISTORY_KEY); } catch (e) {}
      var hist = [];
      try {
        var p = JSON.parse(raw);
        if (p && p.v === V && Array.isArray(p.r)) { hist = p.r; }
      } catch (e) {}
      var note = byId('ex-hist-note'), wrap = byId('ex-hist-wrap'),
          body = byId('ex-hist-body');
      if (!note) { return; }
      if (!hist.length) {
        note.textContent = 'No attempts yet.';
        wrap.hidden = true;
        return;
      }
      var sum = 0;
      for (var i = 0; i < hist.length; i++) { sum += hist[i].pct; }
      note.textContent = hist.length + ' attempt' + (hist.length > 1 ? 's' : '') +
        ' stored in this browser · average ' + Math.round(sum / hist.length) + '%.';
      wrap.hidden = false;
      body.innerHTML = '';
      for (var k = 0; k < hist.length; k++) {
        var h = hist[k];
        var tr = root.createElement ? root.createElement('tr') : null;
        var row = tr || {};
        var cells = [
          String(h.d || '').replace('T', ' ').slice(0, 16),
          h.topic ? 'Topic · ' + h.topic
            : (Array.isArray(h.ch) ? (h.ch.length === 10 ? 'All chapters'
              : 'Ch ' + h.ch.join(', ')) : '—'),
          h.mode === 'untimed' ? 'Untimed' : (h.mode + ' s/q'),
          h.correct + '/' + h.total + ' (' + h.pct + '%)',
          (h.weak && h.weak.length) ? h.weak.join(' · ') : '—'
        ];
        if (tr) {
          for (var c = 0; c < cells.length; c++) {
            var td = root.createElement('td');
            td.textContent = cells[c];
            row.appendChild(td);
          }
          body.appendChild(row);
        } else {
          // stub-friendly fallback
          var div = { textContent: cells.join(' | ') };
          body.appendChild(div);
        }
      }
    }

    /* ---------- quiz screen ---------- */
    function renderQuiz() {
      var q = map[sess.items[sess.i].id];
      var item = sess.items[sess.i];
      byId('ex-progress').textContent =
        'Q ' + (sess.i + 1) + ' / ' + sess.items.length;
      byId('ex-topic').textContent = q.tp;
      byId('ex-type').textContent = TYPE_LABEL[q.ty] || q.ty;
      byId('ex-src').textContent =
        (q.s === 'course' ? 'Course · ' : 'Supplementary · ') + (q.src || '');
      byId('ex-src').classList[q.s === 'supp' ? 'add' : 'remove']('ex-supp');
      byId('ex-q').innerHTML = q.q;
      var bar = byId('ex-bar');
      if (bar) { bar.style.width = Math.round(sess.i * 100 / sess.items.length) + '%'; }

      pickedOpts = -1;
      var optsWrap = byId('ex-opts'), shortWrap = byId('ex-short');
      optsWrap.innerHTML = '';
      byId('ex-feedback').hidden = true;
      byId('ex-submit').disabled = true;
      byId('ex-submit').hidden = false;
      var tmn = byId('ex-timenote');
      if (tmn) { tmn.hidden = true; }

      if (CHOICE[q.ty]) {
        shortWrap.hidden = true;
        optsWrap.hidden = false;
        var letters = 'ABCDEFGH';
        item.opts.forEach(function (o, idx) {
          var lab = root.createElement ? root.createElement('label') : null;
          var el = lab || { className: '', textContent: '' };
          el.className = 'ex-choice';
          if (lab) {
            var inp = root.createElement('input');
            inp.type = 'radio';
            inp.name = 'ex-q';
            inp.value = String(idx);
            el.appendChild(inp);
            var sp = root.createElement('span');
            sp.innerHTML = '<b>' + letters[idx] + '.</b> ' + o;
            el.appendChild(sp);
            lab.addEventListener('change', function () {
              pickedOpts = idx;
              byId('ex-submit').disabled = false;
              if (sess) { sess.draft = String(idx); save(); }
            });
          } else {
            el.setAttribute && el.setAttribute('data-idx', idx);
          }
          optsWrap.appendChild(el);
        });
        // restore draft pick on resume (pre-submit only)
        if (sess.draft && /^\d+$/.test(sess.draft)) {
          pickedOpts = Number(sess.draft);
          var labs = optsWrap.querySelectorAll ? optsWrap.querySelectorAll('label') : [];
          if (labs[pickedOpts]) {
            var r = labs[pickedOpts].querySelector('input');
            if (r) { r.checked = true; }
            byId('ex-submit').disabled = false;
          }
        }
      } else {
        optsWrap.hidden = true;
        shortWrap.hidden = false;
        var input = byId('ex-input');
        input.disabled = false;
        input.value = sess.draft || '';
        byId('ex-submit').disabled = !input.value.trim();
      }

      // restore already-submitted state on resume
      if (sess.ans[sess.i]) { reveal(false); }

      var timer = byId('ex-timer');
      if (sess.endTs == null) {
        timer.textContent = 'Untimed';
        stopTimer();
      } else {
        tick(nowFn());
        startTicking();
      }
    }

    function reveal(mine) {
      // mine: whether feedback was just produced this click (affects nothing
      // structural — kept for clarity); always renders the locked state.
      var q = map[sess.items[sess.i].id];
      var item = sess.items[sess.i];
      var a = sess.ans[sess.i];
      if (!a) { return; }
      byId('ex-submit').hidden = true;
      var fb = byId('ex-feedback');
      fb.hidden = false;
      byId('ex-verdict').textContent = a.ok
        ? '✓ Correct' : '✗ Incorrect';
      byId('ex-verdict').className = 'ex-verdict ' + (a.ok ? 'ex-ok' : 'ex-bad');
      var correctLine;
      if (CHOICE[q.ty]) {
        correctLine = 'Correct answer: ' + 'ABCDEFGH'[item.correct] + '. ' +
          item.opts[item.correct];
        if (!a.ok && a.picked != null && a.picked >= 0) {
          correctLine = 'Your answer: ' + 'ABCDEFGH'[a.picked] + '. ' +
            item.opts[a.picked] + '  →  ' + correctLine;
        } else if (!a.ok && q.ty !== 'tf' && (a.given != null)) {
          correctLine = 'Your answer: “' + a.given + '”  →  ' + correctLine;
        }
      } else {
        correctLine = 'Correct answer: ' + (q.disp || '');
        if (!a.ok && a.given != null && a.given !== '') {
          correctLine = 'Your answer: “' + a.given + '”  →  ' + correctLine;
        }
      }
      byId('ex-correct').textContent = correctLine;
      byId('ex-why').innerHTML = (q.e || '') +
        ' <span class="ex-src-inline">' + (q.s === 'course' ? 'Course · ' : 'Supplementary · ') +
        (q.src || '') + '</span>';
      // lock inputs
      var inputs = byId('ex-opts').querySelectorAll('input');
      for (var i = 0; i < inputs.length; i++) { inputs[i].disabled = true; }
      byId('ex-input').disabled = true;
      byId('ex-next').textContent =
        (sess.i + 1 >= sess.items.length) ? 'Finish session →' : 'Next question →';
      var bar = byId('ex-bar');
      if (bar) {
        bar.style.width =
          Math.round((sess.i + 1) * 100 / sess.items.length) + '%';
      }
    }

    function submit() {
      if (sess.ans[sess.i]) { return; }
      var q = map[sess.items[sess.i].id];
      var item = sess.items[sess.i];
      if (CHOICE[q.ty]) {
        if (pickedOpts < 0) { return; }
        sess.ans[sess.i] = {
          ok: item.correct === pickedOpts, picked: pickedOpts
        };
        sess.draft = '';
      } else {
        var val = byId('ex-input').value;
        if (!val.trim()) { return; }
        sess.ans[sess.i] = { ok: grade(q, val), given: val };
        sess.draft = '';
      }
      save();
      reveal(true);
    }

    function next() {
      if (sess.i + 1 >= sess.items.length) { finish(false); return; }
      sess.i++;
      sess.draft = '';
      save();
      renderQuiz();
    }

    /* ---------- results ---------- */
    function finish(auto) {
      stopTimer();
      sess.stage = 'results';
      var tnote = byId('ex-timenote');
      if (tnote) { tnote.hidden = !auto; }
      var sc = scoreSession(sess);
      if (!sess.saved) {
        var weak = weakTopics(bank, sess, 3);
        var entry = {
          d: new Date(nowFn()).toISOString(), ch: sess.ch.slice(),
          topic: sess.topic || null,
          mode: sess.mode, correct: sc.correct, total: sc.total, pct: sc.pct,
          weak: weak.map(function (w) { return w.tp + ' (' + w.wrong + ')'; }),
          auto: !!auto
        };
        var raw = null;
        try { raw = storage.getItem(HISTORY_KEY); } catch (e) {}
        try { storage.setItem(HISTORY_KEY, pushHistory(raw, entry)); } catch (e) {}
        sess.saved = true;
      }
      save();
      renderResults(auto);
    }

    function escA(s) {
      return String(s == null ? '' : s)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;')
        .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    function renderRecs(weak) {
      var rec = byId('ex-rec');
      if (!rec) { return; }
      rec.innerHTML = '';
      if (!weak.length) { rec.hidden = true; return; }
      var shown = 0;
      weak.forEach(function (w) {
        var r = recFor(w.tp);
        if (!r) { return; }
        var d = root.createElement ? root.createElement('div') : { className: '', textContent: '' };
        d.className = 'ex-rec-item';
        if (root.createElement) {
          d.innerHTML = '<span class="ex-rec-k">Next step →</span> <b>' +
            escA(w.tp) + ':</b> <a href="' + r.href + '">' + r.label + '</a>';
        } else {
          d.textContent = 'Next step for ' + w.tp + ': ' + r.label + ' → ' + r.href;
        }
        rec.appendChild(d);
        shown++;
      });
      rec.hidden = shown === 0;
    }

    function renderResults(auto) {
      var sc = scoreSession(sess);
      byId('ex-score').textContent = sc.correct + ' / ' + sc.total;
      byId('ex-pct').textContent = sc.pct + '%';
      var grade = sc.pct >= 90 ? 'Excellent — very strong command of this material.'
        : sc.pct >= 70 ? 'Solid pass — a little revision will lock it in.'
        : sc.pct >= 50 ? 'Shaky — review the topics below before retrying.'
        : 'Needs work — revisit the chapters and retry this set.';
      byId('ex-scorenote').textContent = grade + (auto ? ' (Session ended when the timer expired.)' : '');
      var weak = weakTopics(bank, sess, 3);
      var wrap = byId('ex-weak-wrap'), box = byId('ex-weak');
      if (weak.length) {
        wrap.hidden = false;
        box.innerHTML = '';
        weak.forEach(function (w) {
          var el = root.createElement ? root.createElement('span') : { className: '', textContent: '' };
          el.className = 'ex-chip is-weak';
          el.textContent = w.tp + ' — ' + w.wrong + '/' + w.total + ' missed';
          box.appendChild(el);
        });
        renderRecs(weak);
      } else {
        wrap.hidden = true;
      }
      var wrong = retryIds(sess);
      byId('ex-retry').hidden = !wrong.length;
      byId('ex-retry').textContent =
        'Retry incorrect questions (' + wrong.length + ')';

      // review list
      var rev = byId('ex-review');
      rev.innerHTML = '';
      sess.items.forEach(function (item, idx) {
        var q = map[item.id];
        var a = sess.ans[idx];
        var ok = a && a.ok;
        var div = root.createElement ? root.createElement('div') : { className: '', textContent: '' };
        div.className = 'ex-rev ' + (ok ? 'is-ok' : 'is-bad');
        var head = '<div class="ex-rev-h"><span class="ex-mark">' +
          (ok ? '✓' : '✗') + '</span><span class="ex-tag">' +
          (TYPE_LABEL[q.ty] || q.ty) + '</span><span class="ex-tag ex-src' +
          (q.s === 'supp' ? ' ex-supp' : '') + '">' +
          (q.s === 'course' ? 'Course · ' : 'Supplementary · ') + (q.src || '') +
          '</span><span class="ex-tag">' + q.tp + '</span></div>';
        var your, correct;
        if (CHOICE[q.ty]) {
          your = 'Your answer: ' + (a && a.picked != null && a.picked >= 0
            ? 'ABCDEFGH'[a.picked] + '. ' + item.opts[a.picked] : '(not answered)');
          correct = 'Correct: ' + 'ABCDEFGH'[item.correct] + '. ' +
            item.opts[item.correct];
        } else {
          your = 'Your answer: ' + (a && a.given ? '“' + a.given + '”'
            : '(not answered)');
          correct = 'Correct: ' + (q.disp || '');
        }
        div.innerHTML = head + '<p class="ex-rev-q">' + q.q + '</p>' +
          '<p class="ex-rev-y ' + (ok ? 'ex-oktext' : 'ex-badtext') + '">' + your +
          '</p><p class="ex-rev-c">' + correct + '</p>' +
          '<p class="ex-why is-open">' + (q.e || '') + '</p>';
        rev.appendChild(div);
      });
      show('results');
    }

    /* ---------- session actions ---------- */
    function startSession() {
      var cfg = currentCfg();
      if (!cfg.ch.length || !cfg.len) { return; }
      sess = buildSession(bank, cfg, nowFn());
      save();
      show('quiz');
      renderQuiz();
    }

    /* short single-topic quiz (topic chips in setup) */
    function startTopic(topic) {
      var pool = topicPool(bank, topic);
      if (!pool.length) { return false; }
      var chSet = {};
      pool.forEach(function (b) {
        for (var i = 0; i < b.c.length; i++) { chSet[b.c[i]] = 1; }
      });
      var cfg = currentCfg();
      var tcfg = {
        ch: Object.keys(chSet).map(Number),
        len: Math.min(5, pool.length),
        mode: cfg.mode,
        topic: topic
      };
      sess = buildSession(bank, tcfg, nowFn());
      save();
      show('quiz');
      renderQuiz();
      return true;
    }

    function retryWrong() {
      var ids = retryIds(sess);
      if (!ids.length) { return; }
      var chSet = {};
      ids.forEach(function (id) {
        map[id].c.forEach(function (c) { chSet[c] = 1; });
      });
      var ch = Object.keys(chSet).map(Number);
      var items = shuffle(ids).map(function (id) {
        var q = map[id];
        if (CHOICE[q.ty]) {
          if (q.ty === 'tf') { return { id: id, opts: q.o.slice(), correct: q.a }; }
          var pres = shuffle(q.o);
          return { id: id, opts: pres, correct: pres.indexOf(q.o[q.a]) };
        }
        return { id: id };
      });
      sess = {
        v: V, stage: 'quiz', ch: ch, mode: 'untimed', items: items,
        ans: items.map(function () { return null; }), i: 0, draft: '',
        endTs: null, started: new Date(nowFn()).toISOString(),
        saved: false, retry: true
      };
      save();
      show('quiz');
      renderQuiz();
    }

    /* ---------- wiring ---------- */
    function wire() {
      // chapters
      var boxes = root.querySelectorAll('input[data-ch]');
      for (var i = 0; i < boxes.length; i++) {
        (function (b) {
          b.addEventListener('change', function () { syncSetup(); });
        })(boxes[i]);
      }
      var all = byId('ex-all');
      if (all) {
        all.addEventListener('change', function () {
          var on = all.checked;
          var bs = root.querySelectorAll('input[data-ch]');
          for (var k = 0; k < bs.length; k++) { bs[k].checked = on; }
          syncSetup();
        });
      }
      // lengths
      var lenBtns = byId('ex-lens').querySelectorAll('button[data-len]');
      for (var L = 0; L < lenBtns.length; L++) {
        (function (btn) {
          btn.addEventListener('click', function () {
            if (btn.disabled) { return; }
            var bs = byId('ex-lens').querySelectorAll('button[data-len]');
            for (var m = 0; m < bs.length; m++) { bs[m].classList.remove('is-on'); }
            btn.classList.add('is-on');
          });
        })(lenBtns[L]);
      }
      // modes
      var mBtns = byId('ex-modes').querySelectorAll('button[data-mode]');
      for (var M = 0; M < mBtns.length; M++) {
        (function (btn) {
          btn.addEventListener('click', function () {
            var bs = byId('ex-modes').querySelectorAll('button[data-mode]');
            for (var m = 0; m < bs.length; m++) { bs[m].classList.remove('is-on'); }
            btn.classList.add('is-on');
          });
        })(mBtns[M]);
      }
      byId('ex-start').addEventListener('click', startSession);
      var tbtns = root.querySelectorAll
        ? root.querySelectorAll('button[data-topic]') : [];
      for (var ti = 0; ti < tbtns.length; ti++) {
        (function (btn) {
          btn.addEventListener('click', function () {
            startTopic(btn.getAttribute('data-topic'));
          });
        })(tbtns[ti]);
      }
      byId('ex-submit').addEventListener('click', submit);
      byId('ex-next').addEventListener('click', next);
      byId('ex-retry').addEventListener('click', retryWrong);
      byId('ex-again').addEventListener('click', function () {
        clearSession();
        renderHistory();
        syncSetup();
        show('setup');
      });
      var input = byId('ex-input');
      var draftTimer = null;
      input.addEventListener('input', function () {
        byId('ex-submit').disabled = !input.value.trim();
        if (!sess) { return; }
        sess.draft = input.value;
        if (draftTimer) { clearTimeout(draftTimer); }
        draftTimer = setTimeout(save, 400);
      });

      // resume banner
      var raw = null;
      try { raw = storage.getItem(SESSION_KEY); } catch (e) {}
      if (raw) {
        var vs = validSession(raw, bank);
        var banner = byId('ex-resume'), text = byId('ex-resume-text'),
            yes = byId('ex-resume-yes'), no = byId('ex-resume-no');
        if (vs) {
          sess = vs;
          banner.hidden = false;
          var sc = scoreSession(vs);
          text.textContent = vs.stage === 'quiz'
            ? 'Question ' + (vs.i + 1) + ' of ' + vs.items.length +
              (vs.endTs != null ? ' · timed session deadline ' +
                new Date(vs.endTs).toLocaleString() : ' · untimed')
            : 'A finished session (' + sc.correct + '/' + sc.total + ') is ready to review.';
          yes.hidden = false;
          yes.onclick = function () {
            banner.hidden = true;
            if (vs.stage === 'results') { renderResults(false); }
            else if (vs.endTs != null && remainingSec(vs.endTs, nowFn()) <= 0) {
              finish(true);
            } else { show('quiz'); renderQuiz(); }
          };
          no.onclick = function () {
            banner.hidden = true;
            clearSession();
            show('setup');
          };
        } else {
          // damaged/incompatible session — discard with a visible notice
          try { storage.removeItem(SESSION_KEY); } catch (e) {}
          banner.hidden = false;
          text.textContent = 'The saved session could not be validated (storage ' +
            'was empty, damaged or from an incompatible version), so it was ' +
            'discarded — nothing was restored silently. Start a fresh session below.';
          yes.hidden = true;
          no.textContent = 'OK — start fresh';
          no.onclick = function () { banner.hidden = true; };
        }
      }

      renderHistory();
      syncSetup();
      show('setup');
    }

    if (!root.__exWired) {
      root.__exWired = true;
      wire();
    }
    return {
      get session() { return sess; },
      start: startSession, tick: tick, submit: submit, next: next,
      finish: finish, syncSetup: syncSetup, save: save
    };
  }

  var api = {
    SESSION_KEY: SESSION_KEY, HISTORY_KEY: HISTORY_KEY, V: V,
    TYPE_LABEL: TYPE_LABEL, CHOICE: CHOICE,
    normalize: normalize, grade: grade, gradeChoice: gradeChoice,
    shuffle: shuffle, poolFor: poolFor, lengthsAvailable: lengthsAvailable,
    remainingSec: remainingSec, buildSession: buildSession,
    scoreSession: scoreSession, weakTopics: weakTopics, retryIds: retryIds,
    pushHistory: pushHistory, validSession: validSession, init: init,
    topicPool: topicPool, recFor: recFor, REC_RULES: REC_RULES
  };

  if (typeof module === 'object' && module.exports) { module.exports = api; }
  global.EXAM = api;

  if (typeof document !== 'undefined' && document.addEventListener) {
    document.addEventListener('DOMContentLoaded', function () {
      try {
        if (document.getElementById('ex-root') && global.EXAM_BANK &&
            global.localStorage) {
          init(document, global.EXAM_BANK, global.localStorage);
        }
      } catch (e) { /* not the exam page */ }
    });
  }
})(typeof window !== 'undefined' ? window : this);
