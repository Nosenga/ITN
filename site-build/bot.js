/* ============================================================
   ITN question search — client-side lexical search engine
   ------------------------------------------------------------
   This is a LOCAL information-retrieval search (BM25-style
   ranking + stemming + intent detection + abbreviation/domain
   expansion). It is NOT an AI model and calls no external
   services or APIs. All displayed explanation text is quoted
   verbatim from the course material; badges and match notes
   are clearly marked as system-added.
   ============================================================ */
(function () {
  'use strict';

  var D = window.__ITN__;
  if (!D || !D.passages || !D.passages.length) { console.warn('__ITN__ corpus missing'); return; }

  var TOTAL = D.passages.length;

  /* ---------------- tokenizing / stemming ---------------- */
  var STOP = {};
  ('a an the and or but if then else of in on at to from by for with about as is are was were be been being ' +
   'do does did doing have has had this that these those it its i you he she we they them your our their ' +
   'what which who whom when where why how not nor too very can will just should would could may might must ' +
   'any all each few more most other such only own same also into over under again further once here ' +
   'there both don now tell please me your mine ours us hi hello there\'s lets get give show show me ' +
   'my across towards perhaps maybe actually ' +
   'information info details detail something anything one two per').split(/\s+/)
    .forEach(function (w) { STOP[w] = 1; });

  /* Question-scaffold words: removed from the coverage denominator so passages
     aren't penalised for missing "explain"/"purpose", but they still score. */
  var SCAFFOLD = {};
  ('explain explains explained explaining describe describes described description ' +
   'define defined definition meanings meaning purposes purpose roles role ' +
   'functions function used uses using use works working work ' +
   'know knows knew want wants wanted need needs needing getting ' +
   'try tries tried help helps mean means meant happen happens happened ' +
   'wonder wonders wondering look looking looking for look for ' +
   'travel travels travelled travelling visiting visit')
    .split(/\s+/).forEach(function (w) { SCAFFOLD[w] = 1; });

  /* Question-glue words (comparison phrasing) — also excluded from coverage. */
  var GLUE = {};
  ('difference differences differenc between compare compared compar comparison versus than vs')
    .split(/\s+/).forEach(function (w) { GLUE[w] = 1; });

  var CONTRACTIONS = [
    ["what's", "what is"], ["what're", "what are"], ["where's", "where is"],
    ["when's", "when is"], ["why's", "why is"], ["how's", "how is"],
    ["who's", "who is"], ["that's", "that is"], ["there's", "there is"],
    ["it's", "it is"], ["they're", "they are"], ["you're", "you are"],
    ["we're", "we are"], ["i'm", "i am"], ["i've", "i have"],
    ["doesn't", "does not"], ["don't", "do not"], ["isn't", "is not"],
    ["aren't", "are not"], ["wasn't", "was not"], ["weren't", "were not"],
    ["can't", "can not"], ["won't", "will not"], ["shouldn't", "should not"],
    ["wouldn't", "would not"], ["couldn't", "could not"], ["haven't", "have not"],
    ["hasn't", "has not"], ["let's", "let us"]
  ];

  /* Related networking terms — broadens natural-language phrasing.
     (Related-term expansion, weight ~0.42; not an AI model.) */
  var SYN = {
    tcp: ['transmission', 'control', 'protocol', 'reliable', 'connection'],
    udp: ['user', 'datagram', 'connectionless', 'unreliable'],
    mac: ['media', 'access', 'control', 'physical', 'address', 'nic'],
    arp: ['address', 'resolution', 'cache', 'mapping'],
    ip: ['internet', 'protocol', 'logical', 'address'],
    ipv4: ['ip', 'version', 'address'],
    ipv6: ['ip', 'address', 'extension', 'header', 'nat'],
    routing: ['router', 'route', 'forward', 'table', 'path'],
    router: ['routing', 'route', 'forward', 'anatomy', 'boot'],
    switch: ['switching', 'switches', 'forward', 'frame', 'port'],
    learn: ['learning', 'learns', 'mac', 'table', 'built'],
    ethernet: ['lan', '802', 'frame', 'ieee'],
    handshake: ['three', 'way', 'session', 'establish', 'syn', 'ack'],
    gateway: ['default', 'router', 'host'],
    multicast: ['group', '01', '00', '5e'],
    broadcast: ['ff', 'ff', 'all', 'devices'],
    unicast: ['single', 'destination'],
    csma: ['carrier', 'sense', 'multiple', 'access', 'collision'],
    dns: ['domain', 'name', 'system', 'resolve', 'lookup', 'url'],
    voip: ['voice', 'telephony', 'ip', 'phone'],
    sip: ['session', 'initiation', 'voip'],
    nat: ['network', 'address', 'translation', 'private'],
    svi: ['switch', 'virtual', 'interface', 'vlan'],
    nic: ['network', 'interface', 'card'],
    crc: ['cyclic', 'redundancy', 'check', 'error'],
    oui: ['vendor', 'organization', 'first', 'bytes'],
    duplex: ['half', 'full', 'collision'],
    runt: ['collision', 'fragment', 'minimum', '64'],
    window: ['size', 'flow', 'control', 'acknowledgement'],
    ack: ['acknowledgement', 'confirm', 'receipt'],
    reassembly: ['reassemble', 'segments', 'original', 'order'],
    multiplexing: ['multiplexed', 'interleaved', 'conversations'],
    segment: ['segmentation', 'transport', 'header'],
    segmentation: ['segment', 'divide', 'pieces'],
    packet: ['network', 'layer', 'ip'],
    frame: ['ethernet', 'data', 'link', 'header', 'trailer'],
    pdu: ['protocol', 'data', 'unit'],
    osi: ['model', 'layer'],
    lan: ['local', 'area', 'ethernet'],
    wan: ['wide', 'area', 'remote', 'serial'],
    topology: ['diagram', 'physical', 'layout'],
    converged: ['convergence', 'voice', 'video', 'data'],
    tftp: ['trivial', 'file', 'transfer'],
    snmp: ['simple', 'network', 'management'],
    dhcp: ['dynamic', 'host', 'configuration', 'assign', 'automatic'],
    difference: ['reliable', 'reliability', 'overhead', 'connectionless', 'stateless', 'trade', 'burden'],
    compare: ['reliable', 'reliability', 'overhead', 'connectionless', 'stateless'],
    versus: ['difference', 'compared'],
    save: ['copy', 'startup', 'running', 'configuration'],
    store: ['memory', 'buffering', 'flash', 'nvram'],
    subnet: ['subnetting', 'segmentation', 'mask', 'network'],
    vlsm: ['variable', 'length', 'subnet', 'mask'],
    attack: ['attacks', 'malware', 'threat', 'denial'],
    firewall: ['mitigation', 'defense', 'security'],
    ssh: ['secure', 'shell', 'telnet', 'password'],
    malware: ['virus', 'worm', 'trojan', 'ransomware'],
    nat64: ['ipv6', 'nat'],
    cut: ['through', 'fast', 'forward', 'fragment', 'store'],
    buffering: ['memory', 'store', 'forward'],
    boot: ['bootup', 'reload', 'ios', 'flash', 'rom', 'nvram'],
    vlan: ['virtual', 'lan', 'switch'],
    etherchannel: ['bundle', 'ports', 'aggregation', 'layer'],
    auto: ['mdix', 'crossover', 'straight'],
    mdix: ['crossover', 'auto'],
    collision: ['domain', 'csma', 'cd', 'half'],
    de: ['encapsulation'],
    encapsulation: ['header', 'trailer', 'frame', 'pdu'],
    deencapsulation: ['remove', 'header', 'receive'],
    reliability: ['reliable', 'acknowledgement', 'delivery'],
    flow: ['control', 'window', 'regulate'],
    stateful: ['state', 'track', 'session'],
    stateless: ['state', 'udp'],
    ospf: ['open', 'shortest', 'path', 'routing'],
    administrative: ['distance', 'trustworthiness', 'metric'],
    metric: ['hop', 'cost', 'distance'],
    depletion: ['exhaustion', 'addresses', 'shortage'],
    public: ['internet', 'global'],
    private: ['internal', 'local', 'rfc1918'],
    usable: ['hosts', 'addresses', 'subtract', '2'],
    calculate: ['determine', 'compute', 'number', 'formula'],
    path: ['route', 'routing', 'forward', 'metric', 'hop', 'table', 'best'],
    automatically: ['dynamic', 'assign', 'dhcp', 'lease', 'server'],
    automatic: ['dynamic', 'assign', 'dhcp'],
    protect: ['password', 'security', 'mitigation', 'defense', 'attack'],
    browser: ['web', 'http', 'url', 'browse', 'server'],
    website: ['web', 'host', 'domain', 'url', 'name'],
    web: ['http', 'url', 'internet'],
    security: ['threat', 'attack', 'malware', 'password', 'defense', 'vulnerability'],
    find: ['resolve', 'lookup', 'name'],
    decide: ['choose', 'select', 'forward', 'best'],
    choose: ['select', 'decide', 'best'],
    pick: ['choose', 'select', 'best'],
    latency: ['delay', 'performance', 'real-time'],
    simultaneously: ['collision', 'contend', 'contending', 'csma', 'simultaneous'],
    transmit: ['transmission', 'collision', 'media']
  };

  /* Bidirectional abbreviations <-> full forms (recognised either way). */
  var ABB = [
    ['arp', ['address', 'resolution', 'protocol']],
    ['address resolution protocol', ['arp']],
    ['mac', ['media', 'access', 'control']],
    ['media access control', ['mac']],
    ['ip', ['internet', 'protocol']],
    ['internet protocol', ['ip']],
    ['tcp', ['transmission', 'control', 'protocol']],
    ['transmission control protocol', ['tcp']],
    ['udp', ['user', 'datagram', 'protocol']],
    ['user datagram protocol', ['udp']],
    ['dns', ['domain', 'name', 'system', 'service']],
    ['domain name system', ['dns']],
    ['domain name service', ['dns']],
    ['dhcp', ['dynamic', 'host', 'configuration', 'protocol']],
    ['dynamic host configuration protocol', ['dhcp']],
    ['http', ['hypertext', 'transfer', 'protocol']],
    ['hypertext transfer protocol', ['http']],
    ['https', ['hypertext', 'transfer', 'protocol', 'secure', 'tls', 'ssl']],
    ['smtp', ['simple', 'mail', 'transfer', 'protocol']],
    ['simple mail transfer protocol', ['smtp']],
    ['pop', ['post', 'office', 'protocol']],
    ['imap', ['internet', 'message', 'access', 'protocol']],
    ['ftp', ['file', 'transfer', 'protocol']],
    ['file transfer protocol', ['ftp']],
    ['tftp', ['trivial', 'file', 'transfer', 'protocol']],
    ['snmp', ['simple', 'network', 'management', 'protocol']],
    ['nat', ['network', 'address', 'translation']],
    ['network address translation', ['nat']],
    ['lan', ['local', 'area', 'network']],
    ['local area network', ['lan']],
    ['wan', ['wide', 'area', 'network']],
    ['wide area network', ['wan']],
    ['qos', ['quality', 'of', 'service']],
    ['quality of service', ['qos']],
    ['vlan', ['virtual', 'local', 'area', 'network']],
    ['virtual local area network', ['vlan']],
    ['svi', ['switch', 'virtual', 'interface']],
    ['switch virtual interface', ['svi']],
    ['vlsm', ['variable', 'length', 'subnet', 'masking', 'subnet']],
    ['variable length subnet masking', ['vlsm']],
    ['variable length subnet masks', ['vlsm']],
    ['osi', ['open', 'systems', 'interconnection', 'reference', 'model']],
    ['open systems interconnection', ['osi']],
    ['pdu', ['protocol', 'data', 'unit']],
    ['protocol data unit', ['pdu']],
    ['crc', ['cyclic', 'redundancy', 'check']],
    ['cyclic redundancy check', ['crc']],
    ['oui', ['organizationally', 'unique', 'identifier', 'vendor']],
    ['ssh', ['secure', 'shell']],
    ['secure shell', ['ssh']],
    ['voip', ['voice', 'over', 'ip', 'telephony']],
    ['voice over ip', ['voip']],
    ['csma', ['carrier', 'sense', 'multiple', 'access']],
    ['carrier sense multiple access', ['csma']],
    ['aaa', ['authentication', 'authorization', 'accounting']],
    ['authentication authorization accounting', ['aaa']],
    ['dos', ['denial', 'of', 'service']],
    ['denial of service', ['dos', 'ddos']],
    ['ddos', ['distributed', 'denial', 'service']],
    ['utp', ['unshielded', 'twisted', 'pair']],
    ['unshielded twisted pair', ['utp']],
    ['stp', ['shielded', 'twisted', 'pair']],
    ['shielded twisted pair', ['stp']],
    ['ios', ['internetwork', 'operating', 'system']],
    ['internetwork operating system', ['ios']],
    ['nat', ['network', 'address', 'translation']],
    ['wisp', ['wireless', 'internet', 'service', 'provider']],
    ['slip', ['serial', 'line', 'internet', 'protocol']],
    ['ppp', ['point', 'to', 'point', 'protocol']],
    ['rfc', ['request', 'for', 'comments']],
    ['mtu', ['maximum', 'transmission', 'unit']],
    ['dns', ['domain', 'name']]
  ];

  /* Multi-word concepts recognised as single units (query side + strong bonus). */
  var PHRASES = [
    'network layer', 'transport layer', 'data link layer', 'physical layer',
    'application layer', 'session layer', 'presentation layer',
    'mac address', 'ip address', 'arp table', 'mac address table', 'routing table',
    'default gateway', 'collision domain', 'broadcast domain',
    'three-way handshake', 'three way handshake', 'flow control', 'window size',
    'sequence number', 'acknowledgement number', 'session termination',
    'runt frame', 'frame size', 'frame forwarding', 'cut-through switching',
    'fragment-free switching', 'half duplex', 'full duplex', 'auto-mdix',
    'carrier sense', 'cyclic redundancy check', 'logical link control',
    'media access control', 'address resolution protocol',
    'transmission control protocol', 'user datagram protocol',
    'domain name system', 'dynamic host configuration protocol',
    'hypertext transfer protocol', 'simple mail transfer protocol',
    'file transfer protocol', 'network address translation',
    'local area network', 'wide area network', 'quality of service',
    'subnet mask', 'subnetting', 'variable length subnet mask',
    'usable host', 'host requirements', 'network security', 'security threats',
    'denial of service', 'defense-in-depth', 'reference model', 'osi model',
    'protocol data unit', 'encapsulation', 'de-encapsulation',
    'switch virtual interface', 'virtual local area network',
    'public address', 'private address', 'ethernet frame', 'arp cache',
    'startup configuration', 'running configuration', 'enable secret',
    'logical address', 'physical address', 'name resolution',
    'name server', 'domain name', 'ip addressing', 'address table'
  ];

  var RE_TOK = /\d{1,3}(?:\.\d{1,3}){3}|[a-z0-9]+(?:\.[a-z0-9]+)*/g;

  function stem(w) {
    if (w.length < 4) return w;
    if (/[a-z0-9]$/.test(w) === false) return w;
    if (/ies$/.test(w)) return w.slice(0, -3) + 'y';
    if (/sses$/.test(w)) return w.slice(0, -2);
    if (/ing$/.test(w)) { var s1 = w.slice(0, -3); return s1.length >= 3 ? s1 : w; }
    if (/ed$/.test(w)) { var s2 = w.slice(0, -2); return s2.length >= 3 ? s2 : w; }
    if (/olve$/.test(w)) return w.slice(0, -1);
    if (/es$/.test(w) && !/(ss|us|is|as|os)$/.test(w)) return w.slice(0, -2);
    if (/s$/.test(w) && !/(ss|us|is|as|os)$/.test(w)) return w.slice(0, -1);
    return w;
  }

  function tokenize(text, keepStops) {
    var out = [];
    if (!text) return out;
    var m, lower = String(text).toLowerCase();
    RE_TOK.lastIndex = 0;
    while ((m = RE_TOK.exec(lower)) !== null) {
      var w = m[0].replace(/^\.+|\.+$/g, '');
      if (!w) continue;
      if (!keepStops && STOP[w]) continue;
      if (w.length < 2 && !/^\d/.test(w)) continue;
      out.push(w);
    }
    return out;
  }

  function stemAll(toks) { return toks.map(stem); }

  function preprocess(q) {
    q = String(q || '').toLowerCase().replace(/[?]+/g, ' ');
    for (var i = 0; i < CONTRACTIONS.length; i++) {
      var pair = CONTRACTIONS[i];
      q = q.replace(new RegExp('\\b' + pair[0].replace(/'/g, "'") + '\\b', 'g'), pair[1]);
    }
    return q.replace(/\s+/g, ' ').trim();
  }

  function escRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  /* ---------------- build BM25 index over passages ---------------- */
  var K1 = 1.4, B = 0.72;
  var passages = D.passages;
  var N = passages.length;
  var df = {}, avgdl = 0;

  passages.forEach(function (p, i) {
    p._i = i;
    var titleStr = (p.s || '') + ' ' + (p.t || '') + ' ' + (p.h || '') + ' ' + (p.bk || '');
    var tf = Object.create(null), tfH = Object.create(null), dl = 0;
    stemAll(tokenize(p.x)).forEach(function (t) { tf[t] = (tf[t] || 0) + 1; dl++; });
    stemAll(tokenize(titleStr)).forEach(function (t) { tfH[t] = (tfH[t] || 0) + 1; });
    p._tf = tf; p._tfh = tfH; p._dl = dl;
    avgdl += dl;
    var seen = Object.create(null);
    Object.keys(tf).concat(Object.keys(tfH)).forEach(function (t) {
      if (!seen[t]) { seen[t] = 1; df[t] = (df[t] || 0) + 1; }
    });
    p._raw = (' ' + (p.x || '') + ' ' + titleStr + ' ').toLowerCase().replace(/\s+/g, ' ');
    // markers computed from source text only (used for badges / intent boosts)
    p._def = /\b(is|are|was|were)\s+(a|an|the|used|defined|known|called|responsible|short|one|made|based)\b/i
      .test(((p.h || '') + ' ' + (p.x || '').slice(0, 160)));
    p._ex = /for example|e\.g\.|example:|for instance|such as/i.test((p.x || '').slice(0, 500));
  });
  avgdl = avgdl / N || 1;

  function idf(term) {
    var d = df[term] || 0;
    return Math.log(1 + (N - d + 0.5) / (d + 0.5));
  }

  /* ---------------- question understanding ---------------- */
  function detectIntent(low) {
    return {
      compare: /\bdifference\b|\bdiffer\b|\bcompare\b|\bcomparison\b|\bversus\b|\bvs\b/.test(low),
      defin: /^(what\s+(is|are)\b|what's|define\b|definition\b|meaning\b)/.test(low),
      explainLong: /^(explain|describe|tell me about|overview of)\b/.test(low),
      why: /\bwhy\b|\bpurpose\b|\bfunction\b|\brole\b|\bobjective\b|\bused for\b|\bwhat for\b/.test(low),
      how: /^(how (do|does|can|should|is|to)\b|how do i\b|how can i\b)|\bsteps?\b|\bcalculate\b|\bdetermine\b|\bconfigure\b/.test(low),
      whatDoes: /^what (does|do)\b/.test(low),
      types: /\btypes?\b|\bkinds?\b|\bexamples?\b/.test(low)
    };
  }

  function detectPhrases(low) {
    var found = [];
    for (var i = 0; i < PHRASES.length; i++) {
      var ph = PHRASES[i];
      if (low.indexOf(ph) !== -1) found.push(ph);
    }
    return found;
  }

  /* focus terms = content words minus scaffold/glue */
  function focusOf(low) {
    var raw = tokenize(low);
    var out = [], seen = Object.create(null);
    raw.forEach(function (w) {
      if (SCAFFOLD[w] || GLUE[w] || STOP[w]) return;
      var st = stem(w);
      if (seen[st]) return;
      seen[st] = 1;
      out.push({ raw: w, stem: st });
    });
    return out;
  }

  /* comparison: "difference between X and Y" / "X vs Y" -> two sides */
  function parseSides(low) {
    var m = low.match(/\bbetween\s+(.+?)\s+and\s+(.+)$/);
    if (m) return [focusOf(m[1]), focusOf(m[2])];
    m = low.match(/\b(.+?)\s+(?:vs\.?|versus)\s+(.+)$/);
    if (m) return [focusOf(m[1]), focusOf(m[2])];
    return null;
  }

  function sideHits(p, side) {
    if (!side || !side.length) return false;
    for (var i = 0; i < side.length; i++) {
      // every word of a multi-word side must appear — keyword-only overlap
      // with one word is never enough to present a passage as an answer.
      if (!p._tf[side[i].stem] && !p._tfh[side[i].stem]) return false;
    }
    return true;
  }

  /* ---------------- query expansion ---------------- */
  function expand(low, qRaw, dispMap) {
    var seen = Object.create(null), expanded = [];

    function add(st, w, disp) {
      st = typeof st === 'string' && st.indexOf(' ') === -1 ? stem(st) : st;
      if (seen[st]) return;
      seen[st] = 1;
      expanded.push({ t: st, w: w, disp: disp });
    }

    // direct query terms (full weight)
    qRaw.forEach(function (r) { add(r, 1, dispMap[stem(r)] || r); });

    // abbreviations / full forms (0.55)
    var padded = ' ' + low.replace(/[^a-z0-9\s-]/g, ' ') + ' ';
    ABB.forEach(function (entry) {
      var key = entry[0], words = entry[1], hit = false;
      if (key.indexOf(' ') !== -1) {
        hit = padded.indexOf(' ' + key + ' ') !== -1;
      } else {
        hit = qRaw.indexOf(key) !== -1;
      }
      if (!hit) return;
      words.forEach(function (w) { add(w, 0.55, w); });
    });

    // related networking terms (0.42)
    Object.keys(seen).slice().forEach(function (origStem) {
      var syns = SYN[origStem] || SYN[origStem + 'e'] || [];
      syns.forEach(function (s) { add(s, 0.42, s.toLowerCase()); });
    });
    qRaw.forEach(function (orig) {
      var syns = SYN[orig] || SYN[orig + 'e'] || SYN[stem(orig)] || [];
      syns.forEach(function (s) { add(s, 0.42, s.toLowerCase()); });
    });

    return expanded;
  }

  /* ---------------- spelling tolerance ---------------- */
  /* Small vocabulary: only consulted for query tokens the index has never
     seen (df === 0). Bounded edit distance, best match wins; the fuzzy
     term only ever SCORES on passages that already matched a real query
     word, so unrelated queries can never manufacture a hit. */
  var VOCAB = Object.keys(df);

  function boundedDist(a, b, maxD) {
    var la = a.length, lb = b.length;
    if (Math.abs(la - lb) > maxD) return maxD + 1;
    var prev = new Int32Array(lb + 1), cur = new Int32Array(lb + 1);
    for (var j = 0; j <= lb; j++) prev[j] = j;
    for (var i = 1; i <= la; i++) {
      cur[0] = i;
      var best = cur[0];
      for (var j2 = 1; j2 <= lb; j2++) {
        var cost = a.charCodeAt(i - 1) === b.charCodeAt(j2 - 1) ? 0 : 1;
        var v = prev[j2 - 1] + cost;
        if (prev[j2] + 1 < v) v = prev[j2] + 1;
        if (cur[j2 - 1] + 1 < v) v = cur[j2 - 1] + 1;
        cur[j2] = v;
        if (v < best) best = v;
      }
      if (best > maxD) return maxD + 1;
      var t = prev; prev = cur; cur = t;
    }
    return prev[lb];
  }

  function fuzzyFind(tok) {
    if (/[0-9]/.test(tok) || tok.length < 5) return null;
    var maxD = tok.length >= 9 ? 2 : 1;
    var best = null, bestD = maxD + 1, bestDf = -1;
    for (var i = 0; i < VOCAB.length; i++) {
      var v = VOCAB[i];
      if (v.length < 5 || v === tok) continue;
      if (Math.abs(v.length - tok.length) > maxD) continue;
      var d = boundedDist(tok, v, maxD);
      if (d <= maxD && (d < bestD || (d === bestD && df[v] > bestDf))) {
        best = v; bestD = d; bestDf = df[v];
      }
    }
    return (best && bestDf >= 3) ? best : null;
  }

  /* ---------------- search ---------------- */
  function search(question, limit) {
    limit = limit || 6;
    var low = preprocess(question);
    var qRaw = tokenize(low);                       // content tokens (STOP removed)
    if (!qRaw.length) return { hits: [], related: [], terms: [], question: question, focus: [], intent: {} };

    var intent = detectIntent(low);
    var phrases = detectPhrases(low);
    var focus = focusOf(low);
    var sides = intent.compare ? parseSides(low) : null;

    var dispMap = {};
    qRaw.forEach(function (r) {
      var st = stem(r);
      if (!dispMap[st]) dispMap[st] = r;
    });

    // highlight terms: query words + related/abbrev words
    var terms = {};
    tokenize(low, true).forEach(function (w) {
      if (!STOP[w]) { terms[w] = 1; terms[stem(w)] = 1; }
      (SYN[w] || []).forEach(function (s) { terms[s.toLowerCase()] = 1; });
    });
    phrases.forEach(function (ph) { ph.split(/\s+/).forEach(function (w) { terms[w] = 1; }); });
    ABB.forEach(function (entry) {
      if ((' ' + low + ' ').indexOf(' ' + entry[0] + ' ') !== -1 || qRaw.indexOf(entry[0]) !== -1) {
        entry[1].forEach(function (w) { terms[w] = 1; });
      }
    });
    var termsArr = Object.keys(terms);

    // coverage denominator: focus only (glue + scaffold excluded)
    var dTotal = Math.max(1, focus.length);

    var expanded = expand(low, qRaw, dispMap);

    // domain-shaped tokens (cisco.com) imply name-resolution material
    var hasDomain = /\b[a-z0-9-]{2,}\.(?:com|org|net|edu|gov|io|za|info|web|co)\b/.test(low);
    if (hasDomain) {
      ['domain', 'name', 'url', 'resolved'].forEach(function (w) {
        var st = stem(w);
        if (df[st] !== undefined) expanded.push({ t: st, w: 0.5, disp: w });
      });
    }

    // spelling tolerance for tokens the corpus has never seen
    var fuzzyList = [];
    qRaw.forEach(function (r) {
      var st = stem(r);
      if (df[st] !== undefined) return;
      var tgt = fuzzyFind(r);
      if (tgt) fuzzyList.push({ from: r, t: tgt });
    });
    fuzzyList.forEach(function (f) {
      if (df[f.t] !== undefined) expanded.push({ t: f.t, w: 0.5, disp: f.from });
    });

    var scores = new Float64Array(N);
    var matchedPer = [];

    expanded.forEach(function (e) {
      var idfV = idf(e.t);
      if (idfV <= 0 && e.w === 1) idfV = 0.2;
      if (df[e.t] === undefined && e.w < 1) return;
      for (var i = 0; i < N; i++) {
        var p = passages[i];
        var tf = (p._tf[e.t] || 0) + 2.3 * (p._tfh[e.t] || 0);
        if (!tf) continue;
        var denom = tf + K1 * (1 - B + B * (p._dl / avgdl));
        scores[i] += e.w * idfV * (tf * (K1 + 1)) / denom;
        if (e.w === 1) {
          (matchedPer[i] = matchedPer[i] || Object.create(null))[e.t] = e.disp || e.t;
        }
      }
    });

    /* spelling-tolerance scoring: gated — a fuzzy term only counts on a
       passage that already matched a real (full-weight) query word, so it
       can refine a match but never invent one. */
    var fuzzyPer = [];
    if (fuzzyList.length) {
      for (var fi = 0; fi < N; fi++) {
        if (!matchedPer[fi]) continue;
        for (var fj = 0; fj < fuzzyList.length; fj++) {
          var fz = fuzzyList[fj];
          var pF = passages[fi];
          var tfF = (pF._tf[fz.t] || 0) + 2.3 * (pF._tfh[fz.t] || 0);
          if (!tfF) continue;
          var denF = tfF + K1 * (1 - B + B * (pF._dl / avgdl));
          scores[fi] += 0.5 * idf(fz.t) * (tfF * (K1 + 1)) / denF;
          (fuzzyPer[fi] = fuzzyPer[fi] || Object.create(null))[fz.from] = 1;
        }
      }
    }

    // n-gram phrase bonus + domain-concept phrase bonus
    var qWords = tokenize(low);
    for (var i = 0; i < N; i++) {
      var raw = passages[i]._raw, bonus = 0;
      if (qWords.length >= 4) {
        for (var j = 0; j + 3 <= qWords.length; j++) {
          if (raw.indexOf(' ' + qWords.slice(j, j + 3).join(' ')) !== -1) bonus += 1.6;
        }
      }
      if (qWords.length >= 2) {
        for (var k = 0; k + 2 <= qWords.length; k++) {
          if (raw.indexOf(' ' + qWords.slice(k, k + 2).join(' ')) !== -1) bonus += 0.9;
        }
      }
      for (var ph = 0; ph < phrases.length; ph++) {
        if (raw.indexOf(' ' + phrases[ph]) !== -1) bonus += 2.4;
      }
      var core = low.trim();
      if (core.length > 6 && raw.indexOf(' ' + core + ' ') !== -1) bonus += 5;
      scores[i] += Math.min(bonus, 14);
    }

    // intent-aware adjustments (source-text based)
    var focusStems = focus.map(function (f) { return f.stem; });
    var primary = focus.length
      ? focus.slice().sort(function (a, b) { return idf(b.stem) - idf(a.stem); })[0].stem
      : null;

    function focusInHeading(p) {
      if (!focusStems.length) return 0;
      var head = stemAll(tokenize((p.h || '') + ' ' + (p.t || '')));
      if (!head.length) return 0;
      var hs = Object.create(null);
      head.forEach(function (t) { hs[t] = 1; });
      var hit = 0;
      focusStems.forEach(function (t) { if (hs[t]) hit++; });
      return hit / focusStems.length;
    }

    for (var i2 = 0; i2 < N; i2++) {
      var p2 = passages[i2];
      var bump = 0;

      // definition / explanation: heading names the concept, or definitional wording
      if ((intent.defin || intent.explainLong || intent.whatDoes) && focusStems.length) {
        if (focusInHeading(p2) >= 0.5) bump += 3.5;
        else if (p2._def && p2._tf[primary]) bump += 1.6;
      }
      // purpose: purpose wording near the concept
      if ((intent.why || intent.whatDoes) && primary) {
        if (focusInHeading(p2) >= 0.5 &&
            /\bpurpose\b|\bused to\b|\bused for\b|\bresponsible\b|\bprovides\b|\benables\b|\bfunction/i.test(p2._raw)) {
          bump += 2.4;
        } else if (p2._tfh['purpose'] && p2._tf[primary]) bump += 1.4;
      }
      // procedure: prefer step/CLI material
      if (intent.how && primary && p2._tf[primary]) {
        if (p2.k === 'code') bump += 2.2;
        else if (/\bstep\b|\bcommand\b|\bconfigur|\bcalculat|\bformula\b|\benter\b/i.test(p2._raw)) bump += 1.4;
      }
      // types: prefer passages that enumerate types
      if (intent.types && primary && p2._tf[primary] && /\btype[s]? of\b/i.test(p2._raw)) bump += 1.6;

      // universal heading alignment: a passage whose heading names the
      // question's own concepts is almost always the right one
      if (focusStems.length) {
        var fhU = focusInHeading(p2);
        if (fhU >= 0.5) bump += 1.5;
        else if (fhU > 0 && primary && p2._tfh[primary]) bump += 0.8;
      }

      // comparison: both sides = strong; one side only = demote
      if (sides && sides[0].length && sides[1].length) {
        var s1 = sideHits(p2, sides[0]), s2 = sideHits(p2, sides[1]);
        if (s1 && s2) bump += 4;
        else if (s1 || s2) scores[i2] *= 0.6;
        else scores[i2] *= 0.75;
      }
      scores[i2] += bump;
    }

    /* Focus-token coverage: each key term of the question is "covered" by a
       passage when the term itself, one of its synonyms/abbreviations, or a
       spelling-corrected form appears in that passage. Used for the ranking
       penalty AND for the confidence estimate shown to the user. */
    var fuzzyByFrom = Object.create(null);
    fuzzyList.forEach(function (f) { fuzzyByFrom[f.from] = f.t; });
    var focusRelated = focus.map(function (f) {
      var set = Object.create(null);
      set[f.stem] = 1;
      if (fuzzyByFrom[f.raw]) set[stem(fuzzyByFrom[f.raw])] = 1;
      var sList = SYN[f.raw] || SYN[f.stem] || [];
      sList.forEach(function (w) { set[stem(w)] = 1; });
      ABB.forEach(function (entry) {
        if (entry[0] === f.raw || entry[0] === f.stem ||
            entry[1].indexOf(f.raw) !== -1) {
          entry[1].forEach(function (w) { set[stem(w)] = 1; });
          set[stem(entry[0])] = 1;
        }
      });
      return Object.keys(set);
    });

    function focusCovered(i) {
      var n = 0;
      for (var fj = 0; fj < focusRelated.length; fj++) {
        var rel = focusRelated[fj], hit = false;
        for (var fk = 0; fk < rel.length; fk++) {
          if (passages[i]._tf[rel[fk]] || passages[i]._tfh[rel[fk]]) { hit = true; break; }
        }
        if (hit) n++;
      }
      return n;
    }

    function rawMatched(i) {
      var set = Object.create(null);
      if (matchedPer[i]) {
        Object.keys(matchedPer[i]).forEach(function (k) {
          if (!GLUE[k] && !SCAFFOLD[k]) set[k] = 1;
        });
      }
      if (fuzzyPer[i]) Object.keys(fuzzyPer[i]).forEach(function (k) { set[k] = 1; });
      return Object.keys(set).length;
    }

    // coverage penalty: ignore passages that miss the question's actual concepts
    for (var i3 = 0; i3 < N; i3++) {
      if (rawMatched(i3) / dTotal < 0.34) scores[i3] *= 0.45;
    }

    /* Rank by a coverage-weighted score: passages that address more of the
       question's key concepts rise. Raw scores are kept for the relevance
       floors so filtering behaviour stays conservative. */
    var ranked = [];
    for (var r = 0; r < N; r++) {
      if (scores[r] > 0) {
        var covR = dTotal ? focusCovered(r) / dTotal : 0;
        ranked.push({ p: passages[r], s: scores[r], m: matchedPer[r],
                      sw: scores[r] * (0.55 + 0.45 * Math.min(1, covR)) });
      }
    }
    ranked.sort(function (a, b) { return b.sw - a.sw; });

    // main hits: best passage per slide (max 2), decent relevance floor.
    // For comparison questions a passage must actually mention BOTH sides —
    // keyword-only overlap is never shown as an answer.
    var strictCompare = !!(sides && sides[0].length && sides[1].length);
    var out = [], perSlide = {};

    /* Unanswerable-question gate: when at least half the question's key terms
       have no possible match in the corpus (no df, no synonym, no spelling
       correction) and the best candidate still covers under a third of the
       question, there is no relevant material — show nothing rather than
       dressing up a keyword-only coincidence as an answer. */
    var impossible = 0;
    for (var im = 0; im < focusRelated.length; im++) {
      var relIm = focusRelated[im], can = false;
      for (var im2 = 0; im2 < relIm.length; im2++) {
        if (df[relIm[im2]] !== undefined) { can = true; break; }
      }
      if (!can) impossible++;
    }
    var unanswerable = focusRelated.length > 0 &&
      (impossible / focusRelated.length >= 0.5) &&
      (!ranked.length || (focusCovered(ranked[0].p._i) / dTotal) < 0.34);
    if (unanswerable) { ranked = []; }

    for (var q2 = 0; q2 < ranked.length && out.length < limit; q2++) {
      var cand = ranked[q2], key = cand.p.f + '#' + cand.p.a;
      if (strictCompare &&
          !(sideHits(cand.p, sides[0]) && sideHits(cand.p, sides[1]))) continue;
      perSlide[key] = (perSlide[key] || 0) + 1;
      if (perSlide[key] > 2) continue;
      if (out.length === 0 && cand.s < 0.55) break;
      if (out.length > 0 && cand.s < 0.4) break;
      cand.matched = Object.keys(cand.m || {}).slice(0, 7)
        .map(function (k) { return cand.m[k]; });
      cand.coverN = focusCovered(cand.p._i);
      out.push(cand);
    }

    // why-relevant notes (system-added; excerpt text stays verbatim)
    var sideLabel = sides && sides[0].length && sides[1].length
      ? [sides[0].map(function (f) { return f.raw; }).join(' '),
         sides[1].map(function (f) { return f.raw; }).join(' ')]
      : null;
    out.forEach(function (cand) {
      var pR = cand.p, rs = [];
      if (sideLabel && sideHits(pR, sides[0]) && sideHits(pR, sides[1])) {
        rs.push('Discusses both \u201c' + sideLabel[0] + '\u201d and \u201c' + sideLabel[1] + '\u201d');
      }
      var fhR = focusInHeading(pR);
      if (fhR >= 0.5) rs.push('Heading matches your key terms');
      else if (fhR > 0) rs.push('Heading partly matches your key terms');
      var phR = null;
      for (var pz = 0; pz < phrases.length; pz++) {
        if (pR._raw.indexOf(' ' + phrases[pz]) !== -1) { phR = phrases[pz]; break; }
      }
      if (phR) rs.push('Contains the phrase \u201c' + phR + '\u201d');
      if ((intent.defin || intent.explainLong || intent.whatDoes) && pR._def) {
        rs.push('Definition-style wording for this concept');
      }
      if (intent.how && /\bstep\b|\bcommand\b|\bconfigur|\bcalculat|\bformula\b/.test(pR._raw)) {
        rs.push('Includes the procedure / steps involved');
      }
      rs.push('Matches ' + Math.min(dTotal, cand.coverN) + ' of your ' +
              dTotal + ' key term' + (dTotal === 1 ? '' : 's'));
      cand.reasons = rs;
    });

    /* Confidence: mainly how many of the question's key terms (incl.
       synonyms / spelling-corrected forms) the top passage actually covers.
       When confidence is low the UI offers these as closest matches and asks
       the user to refine — it never presents them as a confirmed answer. */
    var confidence = 0;
    if (out.length) {
      var covTop = Math.min(1, focusCovered(out[0].p._i) / dTotal);
      confidence = 0.35 * Math.min(1, out[0].s / 6) + 0.65 * covTop * covTop;
      if (strictCompare) confidence = Math.max(confidence, 0.7);
    }
    var lowConfidence = !!out.length && confidence < 0.45;

    // related sections: other sections/chapters that also match (for "may also help")
    var used = {}, related = [];
    out.forEach(function (h) { used[h.p.f + '#' + h.p.a] = 1; });
    var bestScore = out.length ? out[0].s : 0;
    var perSection = {};
    for (var r2 = 0; r2 < ranked.length && related.length < 4; r2++) {
      var cand2 = ranked[r2], p3 = cand2.p;
      if (out.length && cand2.s < Math.max(0.5, bestScore * 0.15)) break;
      if (used[p3.f + '#' + p3.a]) continue;
      var secKey = p3.f + '#' + (p3.sid || p3.a);
      if (perSection[secKey]) continue;
      perSection[secKey] = 1;
      related.push({ p: p3, s: cand2.s });
    }

    // when nothing relevant: closest material (clearly labelled downstream)
    var loose = [];
    if (!out.length) {
      var seenS = {};
      for (var r3 = 0; r3 < ranked.length && loose.length < 3; r3++) {
        if (ranked[r3].s < 0.32) break;
        var lp = ranked[r3].p;
        if (seenS[lp.f + '#' + lp.a]) continue;
        seenS[lp.f + '#' + lp.a] = 1;
        loose.push({ p: lp, s: ranked[r3].s });
      }
    }

    return {
      hits: out, related: related, loose: loose, terms: termsArr,
      question: question, focus: focus.map(function (f) { return f.raw; }),
      intent: intent, phrases: phrases,
      fuzzy: fuzzyList, confidence: confidence, lowConfidence: lowConfidence
    };
  }

  /* ---------------- snippet + highlighting ---------------- */
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function buildPattern(terms) {
    var parts = terms.filter(function (t) { return t && t.length >= 2; })
      .map(function (t) { return escRe(t); });
    if (!parts.length) return null;
    parts.sort(function (a, b) { return b.length - a.length; });
    try { return new RegExp('\\b(' + parts.join('|') + ')\\b', 'gi'); } catch (e) { return null; }
  }

  function highlight(str, terms) {
    var re = buildPattern(terms);
    if (!re) return esc(str);
    var out = '', last = 0, m;
    re.lastIndex = 0;
    while ((m = re.exec(str)) !== null) {
      out += esc(str.slice(last, m.index));
      out += '<mark>' + esc(m[0]) + '</mark>';
      last = m.index + m[0].length;
      if (m.index === re.lastIndex) re.lastIndex++;
    }
    out += esc(str.slice(last));
    return out;
  }

  function makeSnippet(text, terms, maxLen) {
    maxLen = maxLen || 430;
    if (!text) return '';
    if (text.length <= maxLen) return text;
    var pos = -1;
    var re = buildPattern(terms);
    if (re) {
      var m; re.lastIndex = 0;
      while ((m = re.exec(text)) !== null) { pos = m.index; break; }
    }
    if (pos < 0) pos = 0;
    // prefer starting at a sentence boundary before the match
    var start = Math.max(0, pos - Math.floor(maxLen * 0.35));
    var sent = text.lastIndexOf('. ', pos);
    if (sent !== -1 && pos - sent < 90) start = sent + 2;
    var end = Math.min(text.length, start + maxLen);
    if (start > 0) { var sp = text.indexOf(' ', start); if (sp > -1 && sp - start < 25) start = sp + 1; }
    if (end < text.length) { var pe = text.lastIndexOf(' ', end); if (pe - start > 80) end = pe; }
    var frag = text.slice(start, end).trim();
    return (start > 0 ? '… ' : '') + frag + (end < text.length ? ' …' : '');
  }

  /* ---------------- rendering ---------------- */
  function badgeHtml(kind) {
    if (kind === 'def') return '<span class="res-badge tag def">Definition</span>';
    if (kind === 'ex') return '<span class="res-badge tag ex">Example</span>';
    if (kind === 'cli') return '<span class="res-badge tag cli">CLI / configuration</span>';
    return '';
  }

  function computeBadges(hit, result) {
    var p = hit.p, out = '';
    var intent = result.intent || {};
    var focus = (result.focus || []).map(function (f) { return stem(f); });
    var headStems = stemAll(tokenize(p.h || ''));
    var headHit = 0;
    focus.forEach(function (f) { if (headStems.indexOf(f) !== -1) headHit++; });
    var headFrac = focus.length ? headHit / focus.length : 0;
    if ((intent.defin || intent.explainLong) && (headFrac >= 0.5 || (p._def && focus.length && p._tf[focus[0]]))) {
      out += badgeHtml('def');
    }
    if (p._ex) out += badgeHtml('ex');
    if (p.k === 'code') out += badgeHtml('cli');
    return out;
  }

  function renderResults(container, question, result, opts) {
    opts = opts || {};
    var hits = result.hits, related = result.related || [], loose = result.loose || [];
    var base = opts.baseDir || '';
    var html = '';
    html += '<div class="ask-q"><span class="qi">Q:</span><span>' + esc(question) + '</span></div>';

    if (result.lowConfidence) {
      html += '<div class="ask-lowconf"><b>Low confidence — please refine your question.</b> ' +
        'The passages below are the <i>closest matches</i> we could find, not a confirmed ' +
        'answer. Try adding more specific key terms from the course (for example ' +
        '<i>ARP</i>, <i>subnet mask</i>, <i>routing table</i>, <i>DHCP</i>), or browse ' +
        'the suggested chapters below.</div>';
    }

    if (result.fuzzy && result.fuzzy.length) {
      html += '<div class="ask-dym">Spelling tolerance applied — matched ' +
        result.fuzzy.slice(0, 3).map(function (f) {
          return '“' + esc(f.from) + '” → “' + esc(f.t) + '”';
        }).join(', ') + ' against the course index.</div>';
    }

    if (!hits.length) {
      html += '<div class="ask-none"><b>We couldn\'t find a relevant explanation in the ' +
        'course material</b> for this question.<br>' +
        'The search only shows what actually exists in Chapters 1–16 — it never invents ' +
        'answers, quotes or sources. Try rephrasing with key terms from the material ' +
        '(e.g. <i>ARP</i>, <i>subnet mask</i>, <i>three-way handshake</i>, <i>MAC address</i>), ' +
        'or browse the chapter pages.</div>';
      if (loose.length) {
        html += '<div class="related"><div class="rel-h">Closest related material ' +
          '<span class="rel-note">(related, but not an exact answer to your question)</span></div>';
        loose.forEach(function (l) {
          var p = l.p;
          html += '<a class="rel-chip" href="' + esc(base + p.f + '#' + p.a) + '">' +
            'Ch ' + p.c + ' · ' + esc(p.t || 'slide') + ' →</a>';
        });
        html += '</div>';
      }
      container.innerHTML = html;
      if (opts.scroll && container.scrollTop !== undefined) container.scrollTop = 0;
      return;
    }

    html += '<div class="ask-intro">Found <b>' + hits.length + '</b> excerpt' +
      (hits.length > 1 ? 's' : '') + ' from the course material — most relevant first.' +
      '<span class="ask-src-note">Excerpt text is quoted verbatim from your course PDFs; ' +
      'badges and match notes are added by the search system.</span></div>';

    hits.forEach(function (hit, idx) {
      var p = hit.p;
      var head = p.h && p.h !== p.t ? p.h : '';
      var snip = makeSnippet(p.x, result.terms, opts.short ? 320 : 430);
      var slideLink = base + p.f + '#' + p.a;
      var secLink = base + p.f + '#' + (p.sid || p.a);
      var matched = hit.matched && hit.matched.length
        ? '<span class="res-match">System match: <em>' + hit.matched.map(esc).join(', ') + '</em></span>'
        : '';
      var figTag = p.g ? '<span class="res-fig" title="This slide contains a figure">🖼 figure on slide</span>' : '';
      html += '<article class="res-card' + (idx === 0 ? ' best' : '') + '">' +
        (idx === 0 ? '<span class="res-badge">Most relevant</span>' :
          '<span class="res-badge rel">Relevant</span>') +
        computeBadges(hit, result) +
        '<div class="res-src">' +
          '<a class="res-ch" href="' + esc(base + p.f) + '">Chapter ' + p.c + '</a>' +
          (p.s ? ' · <a class="res-sec" href="' + esc(secLink) + '">' + esc(p.s) + '</a>' : '') +
          (p.a ? ' · slide ' + esc(String(p.a).replace(/^p/, '')) : '') +
          ' ' + figTag +
        '</div>' +
        (head ? '<div class="res-head">' + esc(head) + '</div>' : '') +
        '<div class="res-head res-title">' + esc(p.t || 'Excerpt') +
          ' <span class="res-exact">verbatim source text</span></div>' +
        '<div class="res-snippet">' + highlight(snip, result.terms) + '</div>' +
        (hit.reasons && hit.reasons.length
          ? '<div class="res-why"><b>Why this matched:</b> ' +
            hit.reasons.map(esc).join(' · ') +
            ' <span class="res-sys">(system-generated note — excerpt text is verbatim)</span></div>'
          : '') +
        '<div class="res-meta">' + matched +
        '<a class="res-link" href="' + esc(slideLink) + '">Open this slide in context →</a>' +
        '</div></article>';
    });

    if (related.length) {
      html += '<div class="related"><div class="rel-h">Related sections that may also help</div>';
      related.forEach(function (rel) {
        var p = rel.p;
        html += '<a class="rel-chip" href="' + esc(base + p.f + '#' + (p.sid || p.a)) + '">' +
          'Ch ' + p.c + (p.s ? ' · ' + esc(p.s) : '') + ' · ' + esc(p.t || 'slide') + ' →</a>';
      });
      html += '</div>';
    }

    container.innerHTML = html;
    if (opts.scroll && container.scrollTop !== undefined) container.scrollTop = 0;
  }

  var SAMPLES = [
    'Explain the network layer.',
    'What is the purpose of ARP?',
    'How does a switch learn MAC addresses?',
    'Explain the difference between TCP and UDP.',
    'How do I calculate the number of usable host addresses?',
    'What is the difference between a public and private IP address?',
    'What is a runt frame?',
    'How does subnetting improve network performance?'
  ];

  function chipHtml() {
    return SAMPLES.map(function (s) {
      return '<button type="button" class="chip" data-q="' + esc(s) + '">' + esc(s) + '</button>';
    }).join('');
  }

  function emptyStateHtml() {
    return '<div class="ask-empty"><div class="big">Ask anything from the course material</div>' +
      'Type a question below — the search goes through every slide passage and shows the ' +
      'matching excerpts with their chapter and section.' +
      '<div class="chips" id="askChips">' + chipHtml() + '</div></div>';
  }

  /* ---------------- widget wiring ---------------- */
  function askInto(container, question, opts) {
    question = (question || '').trim();
    if (!question) return false;
    container.innerHTML = '<div class="ask-loading"><span class="spin"></span>' +
      'Searching the course material…</div>';
    setTimeout(function () {
      var res = search(question, opts && opts.limit || 6);
      renderResults(container, question, res, opts);
    }, 160);
    return true;
  }

  function clearResults(container) { container.innerHTML = emptyStateHtml(); }

  function wireField(inputEl, clearBtn, onChange) {
    function sync() { if (clearBtn) clearBtn.hidden = !inputEl.value; }
    inputEl.addEventListener('input', sync);
    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        inputEl.value = '';
        sync();
        inputEl.focus();
        if (onChange) onChange();
      });
    }
    sync();
  }

  function initWidget() {
    if (document.getElementById('askFab')) return;
    var fab = document.createElement('button');
    fab.id = 'askFab'; fab.className = 'ask-fab'; fab.type = 'button';
    fab.setAttribute('aria-label', 'Ask a question');
    fab.innerHTML = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M8 9h8M8 13h5"/></svg>';

    var panel = document.createElement('div');
    panel.id = 'askPanel'; panel.className = 'ask-panel'; panel.hidden = true;
    panel.innerHTML =
      '<header><span class="t">Ask a question' +
      '<small>Local search over all 10 chapters — runs in your browser</small></span>' +
      '<button type="button" aria-label="Close" id="askClose">✕</button></header>' +
      '<div class="ask-results" id="askResults">' + emptyStateHtml() + '</div>' +
      '<form class="ask-input" id="askForm" autocomplete="off">' +
      '<span class="ask-field"><input type="text" id="askInput" ' +
      'placeholder="e.g. What is the purpose of ARP?" aria-label="Your question">' +
      '<button type="button" class="ask-clear" id="askClear" hidden aria-label="Clear question">✕</button></span>' +
      '<button type="submit">Search</button></form>';

    document.body.appendChild(fab);
    document.body.appendChild(panel);

    var results = document.getElementById('askResults');
    var input = document.getElementById('askInput');
    var clearBtn = document.getElementById('askClear');

    function open(prefill) {
      panel.hidden = false;
      fab.style.transform = 'scale(.92)';
      if (prefill) { input.value = prefill; }
      input.focus();
    }
    fab.addEventListener('click', function () {
      panel.hidden = !panel.hidden;
      if (!panel.hidden) { fab.style.transform = 'scale(.92)'; input.focus(); }
      else fab.style.transform = '';
    });
    document.getElementById('askClose').addEventListener('click', function () {
      panel.hidden = true; fab.style.transform = '';
    });
    document.getElementById('askForm').addEventListener('submit', function (e) {
      e.preventDefault();
      askInto(results, input.value, { scroll: true, short: true, limit: 5 });
    });
    wireField(input, clearBtn, function () { clearResults(results); });
    results.addEventListener('click', function (e) {
      var chip = e.target.closest ? e.target.closest('.chip') : null;
      if (chip && chip.dataset.q) {
        input.value = chip.dataset.q;
        if (clearBtn) clearBtn.hidden = false;
        askInto(results, chip.dataset.q, { scroll: true, short: true, limit: 5 });
      }
    });

    document.addEventListener('click', function (e) {
      var t = e.target.closest ? e.target.closest('[data-open-ask]') : null;
      if (t) { e.preventDefault(); open(t.getAttribute('data-open-ask') || ''); }
    });
  }

  /* ---------------- hero ask box (home page) ---------------- */
  function initHero() {
    var form = document.getElementById('heroAskForm');
    if (!form) return;
    var input = document.getElementById('heroAskInput');
    var out = document.getElementById('heroAskResults');
    var clearBtn = document.getElementById('heroClear');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      askInto(out, input.value, { limit: 6 });
      out.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
    wireField(input, clearBtn, function () { out.innerHTML = ''; });
    out.addEventListener('click', function (e) {
      var chip = e.target.closest ? e.target.closest('.chip') : null;
      if (chip && chip.dataset.q) { input.value = chip.dataset.q; askInto(out, chip.dataset.q, { limit: 6 }); }
    });
    var hc = document.getElementById('heroChips');
    if (hc) hc.innerHTML = chipHtml();
  }

  function ready(fn) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  ready(function () {
    try { initWidget(); } catch (e) { console.error('widget', e); }
    try { initHero(); } catch (e) { console.error('hero', e); }
    try { initScrollspy(); } catch (e) {}
    try { initNavDrop(); } catch (e) {}
  });

  function initNavDrop() {
    document.addEventListener('click', function (e) {
      var d = document.querySelector('.navdrop[open]');
      if (d && !d.contains(e.target)) d.removeAttribute('open');
    });
  }

  function initScrollspy() {
    var toc = document.querySelector('.toc');
    if (!toc) return;
    var links = Array.prototype.slice.call(toc.querySelectorAll('a[href^="#"]'));
    var targets = links.map(function (a) { return document.querySelector(a.getAttribute('href')); })
      .filter(Boolean);
    if (!targets.length || !('IntersectionObserver' in window)) return;
    var seen = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { seen[en.target.id] = en.isIntersecting ? en.intersectionRatio : 0; });
      var bestId = null, best = 0;
      Object.keys(seen).forEach(function (id) { if (seen[id] > best) { best = seen[id]; bestId = id; } });
      if (bestId) {
        links.forEach(function (a) {
          a.classList.toggle('active', a.getAttribute('href') === '#' + bestId);
        });
      }
    }, { rootMargin: '-70px 0px -55% 0px', threshold: [0, .2, .6] });
    targets.forEach(function (t) { io.observe(t); });
  }

  // public API (kept compatible with the previous implementation)
  window.ITNAsk = {
    search: search,
    askInto: askInto,
    renderResults: renderResults,
    corpusSize: TOTAL
  };
})();
