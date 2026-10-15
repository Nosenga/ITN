/* ============================================================
   Packet Tracer Practical Preparation (ptlab.html)
   - checklist persistence (localStorage) with progress bars
   - self-assessment quiz grading (immediate feedback)
   No DOM access at load time. UMD-lite: window.PT / module.exports.
   ============================================================ */
(function (global) {
  'use strict';

  var STORAGE_KEY = 'itn-pt-checks-v1';

  /* ---------- pure state helpers ---------- */

  // Parse stored JSON into a clean {key: true} map. Anything invalid → {}.
  function readState(raw) {
    if (!raw || typeof raw !== 'string') { return {}; }
    var obj;
    try { obj = JSON.parse(raw); } catch (e) { return {}; }
    if (!obj || typeof obj !== 'object' || Object.prototype.toString.call(obj) === '[object Array]') {
      return {};
    }
    var out = {};
    for (var k in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, k) && obj[k] === true) { out[k] = true; }
    }
    return out;
  }

  // Deterministic JSON for storage (keys sorted).
  function writeState(state) {
    var keys = [];
    for (var k in state) {
      if (Object.prototype.hasOwnProperty.call(state, k) && state[k] === true) { keys.push(k); }
    }
    keys.sort();
    var out = {};
    for (var i = 0; i < keys.length; i++) { out[keys[i]] = true; }
    return JSON.stringify(out);
  }

  // Toggle one checklist key (returns a NEW object).
  function toggle(state, key) {
    var out = {};
    for (var k in state) {
      if (Object.prototype.hasOwnProperty.call(state, k)) { out[k] = state[k]; }
    }
    if (out[key] === true) { delete out[key]; } else { out[key] = true; }
    return out;
  }

  // Remove every key with the given prefix (used by per-lab reset).
  function clearPrefix(state, prefix) {
    var out = {};
    for (var k in state) {
      if (Object.prototype.hasOwnProperty.call(state, k) && k.indexOf(prefix) !== 0) {
        out[k] = state[k];
      }
    }
    return out;
  }

  // Progress of a set of keys (e.g. all keys of one lab).
  function progress(state, keys) {
    var total = keys.length, done = 0;
    for (var i = 0; i < keys.length; i++) { if (state[keys[i]] === true) { done++; } }
    return { done: done, total: total, pct: total ? Math.round(done * 100 / total) : 0 };
  }

  // Grade a quiz: questions = [{correct: idx}], answers = [chosen idx|-1].
  function gradeQuiz(questions, answers) {
    var results = [], score = 0;
    for (var i = 0; i < questions.length; i++) {
      var chosen = typeof answers[i] === 'number' ? answers[i] : -1;
      var ok = chosen === questions[i].correct;
      if (ok) { score++; }
      results.push({ ok: ok, chosen: chosen, correct: questions[i].correct });
    }
    return { score: score, total: questions.length, results: results };
  }

  /* ---------- DOM wiring (tested with a stubbed root) ---------- */

  // root: anything with querySelectorAll(sel) (document qualifies).
  // store: anything with getItem/setItem (localStorage qualifies).
  function init(root, store) {
    var state = readState(store.getItem(STORAGE_KEY));

    function persist() { store.setItem(STORAGE_KEY, writeState(state)); }

    function labKeys(prefix) {
      var els = root.querySelectorAll('input[data-ck^="' + prefix + '-"]'), keys = [];
      for (var i = 0; i < els.length; i++) { keys.push(els[i].getAttribute('data-ck')); }
      return keys;
    }

    function refresh() {
      // per-lab bars: <div class="pt-bar" data-ptbar="lab1"> <i></i> </div>
      //               <span data-ptcount="lab1">3 / 8</span>
      var bars = root.querySelectorAll('[data-ptbar]');
      for (var i = 0; i < bars.length; i++) {
        var id = bars[i].getAttribute('data-ptbar');
        var p = progress(state, labKeys(id));
        var fill = bars[i].querySelector('i');
        if (fill) { fill.style.width = p.pct + '%'; }
        var count = root.querySelectorAll('[data-ptcount="' + id + '"]');
        for (var j = 0; j < count.length; j++) {
          count[j].textContent = p.done + ' / ' + p.total + ' tasks';
        }
      }
      // overall
      var all = root.querySelectorAll('input[data-ck]');
      var allKeys = [];
      for (var a = 0; a < all.length; a++) { allKeys.push(all[a].getAttribute('data-ck')); }
      var op = progress(state, allKeys);
      var obar = root.querySelectorAll('#pt-overall-bar i');
      for (var b = 0; b < obar.length; b++) { obar[b].style.width = op.pct + '%'; }
      var ocount = root.querySelectorAll('#pt-overall-count');
      for (var c = 0; c < ocount.length; c++) {
        ocount[c].textContent = op.done + ' / ' + op.total + ' tasks across all labs';
      }
    }

    function reflect(input) {
      var key = input.getAttribute('data-ck');
      var on = state[key] === true;
      input.checked = on;
      var lab = input.closest ? input.closest('label') : null;
      if (lab) {
        if (on) { lab.classList.add('pt-done'); } else { lab.classList.remove('pt-done'); }
      }
    }

    // wire checkboxes
    var boxes = root.querySelectorAll('input[data-ck]');
    for (var i = 0; i < boxes.length; i++) {
      (function (box) {
        reflect(box);
        if (box.addEventListener) {
          box.addEventListener('change', function () {
            state = toggle(state, box.getAttribute('data-ck'));
            persist();
            reflect(box);
            refresh();
          });
        }
      })(boxes[i]);
    }

    // per-lab reset buttons carry a data-ptreset attribute (lab1, lab2, …)
    var resets = root.querySelectorAll('[data-ptreset]');
    for (var r = 0; r < resets.length; r++) {
      (function (btn) {
        if (!btn.addEventListener) { return; }
        btn.addEventListener('click', function () {
          var prefix = btn.getAttribute('data-ptreset');
          state = clearPrefix(state, prefix);
          persist();
          var mine = root.querySelectorAll('input[data-ck^="' + prefix + '-"]');
          for (var m = 0; m < mine.length; m++) { reflect(mine[m]); }
          refresh();
        });
      })(resets[r]);
    }

    // quizzes: a form marked with a data-ptq attribute holding radio inputs;
    // the correct option of each question carries a data-correct marker.
    var forms = root.querySelectorAll('form[data-ptq]');
    for (var f = 0; f < forms.length; f++) {
      (function (form) {
        var btn = form.querySelector('[data-ptq-grade]');
        if (!btn || !btn.addEventListener) { return; }
        btn.addEventListener('click', function () {
          var items = form.querySelectorAll('.ptq-item');
          var questions = [], answers = [];
          for (var q = 0; q < items.length; q++) {
            var opts = items[q].querySelectorAll('input[type="radio"]');
            var chosen = -1, correct = -1;
            for (var o = 0; o < opts.length; o++) {
              var val = parseInt(opts[o].getAttribute('value'), 10);
              if (opts[o].getAttribute('data-correct') !== null) { correct = val; }
              if (opts[o].checked) { chosen = val; }
              var lab = opts[o].closest ? opts[o].closest('label') : null;
              if (lab) { lab.classList.remove('ptq-opt-ok', 'ptq-opt-bad'); }
            }
            questions.push({ correct: correct });
            answers.push(chosen);
          }
          var res = gradeQuiz(questions, answers);
          // paint per-item feedback
          for (var q2 = 0; q2 < items.length; q2++) {
            var r2 = res.results[q2];
            var opts2 = items[q2].querySelectorAll('input[type="radio"]');
            for (var o2 = 0; o2 < opts2.length; o2++) {
              var l2 = opts2[o2].closest ? opts2[o2].closest('label') : null;
              if (!l2) { continue; }
              var v2 = parseInt(opts2[o2].getAttribute('value'), 10);
              if (opts2[o2].getAttribute('data-correct') !== null) {
                l2.classList.add('ptq-opt-ok');            // always show the right one
              } else if (v2 === r2.chosen && !r2.ok) {
                l2.classList.add('ptq-opt-bad');            // your wrong pick
              }
            }
            if (r2.ok) { items[q2].classList.add('ptq-good'); }
            else { items[q2].classList.add('ptq-bad'); }
            items[q2].classList.add('ptq-graded');
          }
          var scoreEl = form.querySelector('.ptq-score');
          if (scoreEl) {
            scoreEl.hidden = false;
            scoreEl.textContent = 'Score: ' + res.score + ' / ' + res.total +
              (res.score === res.total ? ' — perfect!' : '');
            if (res.score === res.total) { scoreEl.classList.add('ptq-perfect'); }
          }
          var retry = form.querySelector('[data-ptq-retry]');
          if (retry) { retry.hidden = false; }
        });
        var retry = form.querySelector('[data-ptq-retry]');
        if (retry && retry.addEventListener) {
          retry.addEventListener('click', function () {
            var radios = form.querySelectorAll('input[type="radio"]');
            for (var r3 = 0; r3 < radios.length; r3++) { radios[r3].checked = false; }
            var items = form.querySelectorAll('.ptq-item');
            for (var i3 = 0; i3 < items.length; i3++) {
              var cl = items[i3].classList;
              cl.remove('ptq-good', 'ptq-bad', 'ptq-graded');
              var opts = items[i3].querySelectorAll('label');
              for (var j3 = 0; j3 < opts.length; j3++) {
                opts[j3].classList.remove('ptq-opt-ok', 'ptq-opt-bad');
              }
            }
            var scoreEl = form.querySelector('.ptq-score');
            if (scoreEl) { scoreEl.hidden = true; scoreEl.classList.remove('ptq-perfect'); }
            retry.hidden = true;
          });
        }
      })(forms[f]);
    }

    refresh();
    return { state: state, refresh: refresh, persist: persist };
  }

  var api = {
    STORAGE_KEY: STORAGE_KEY,
    readState: readState,
    writeState: writeState,
    toggle: toggle,
    clearPrefix: clearPrefix,
    progress: progress,
    gradeQuiz: gradeQuiz,
    init: init
  };

  if (typeof module === 'object' && module.exports) { module.exports = api; }
  global.PT = api;
  if (typeof document !== 'undefined' && document.addEventListener) {
    document.addEventListener('DOMContentLoaded', function () {
      try {
        if (document.querySelector('input[data-ck]') && global.localStorage) {
          init(document, global.localStorage);
        }
      } catch (e) { /* page without checklist — nothing to do */ }
    });
  }
})(typeof window !== 'undefined' ? window : this);
