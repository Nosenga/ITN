# Revision kit content — Chapter 10: Application Layer
# Grounded in uploads/Chapter 10_ITN_Application Layer.pdf (slide refs = page numbers).

DATA = {
    "overview": (
        "Chapter 10 covers the top of the stack: the <b>application layer as the interface "
        "between user programs and the network</b>, plus the presentation layer (coding, "
        "compression, encryption) and session layer (managing dialogs) whose functionality "
        "modern applications absorb. It compares <b>peer-to-peer</b> with <b>client-server</b> "
        "models, then tours the well-known protocols: <b>HTTP/HTTPS</b> (web, GET/POST/PUT), "
        "<b>SMTP/POP/IMAP</b> (sending vs retrieving mail — and how POP and IMAP differ), "
        "<b>DNS</b> (name → numeric address, nslookup), <b>DHCP</b> (dynamic addresses from a "
        "leased pool) and <b>FTP</b> (two connections: commands/replies + file transfer), and "
        "ends with the encapsulation checklist for getting data through the internetwork."
    ),
    "objectives": [
        "Explain what the application layer provides and how it relates to presentation and "
        "session functions (<a class=\"rev-link\" href=\"#p2\">slides 2–5</a>).",
        "Compare the peer-to-peer and client-server communication models "
        "(<a class=\"rev-link\" href=\"#p6\">slides 6–9</a>).",
        "Describe HTTP(S) and the URL/GET flow for web retrieval "
        "(<a class=\"rev-link\" href=\"#p11\">slides 11–13</a>).",
        "Compare email protocols — SMTP for transfer, POP and IMAP for retrieval (with ports) "
        "(<a class=\"rev-link\" href=\"#p14\">slides 14–17</a>).",
        "Explain DNS, nslookup, DHCP leasing and FTP's two connections "
        "(<a class=\"rev-link\" href=\"#p18\">slides 18–24</a>).",
    ],
    "concepts": [
        "<b>Application layer</b> — interface between user applications and the underlying "
        "network; protocols exchange data between programs.",
        "<b>Apps vs services vs protocols</b> — programs you use vs background connectors vs "
        "agreed rules.",
        "<b>Presentation + session</b> — coding/compression/encryption and dialog management, "
        "usually folded into the app.",
        "<b>P2P vs client-server</b> — equal peers with per-request roles vs dedicated "
        "service providers.",
        "<b>Protocol portfolio</b> — HTTP(S), SMTP/POP/IMAP, DNS, DHCP, FTP.",
        "<b>Address/name services</b> — DNS resolves names; DHCP leases addresses from pools.",
    ],
    "definitions": [
        {"t": "Application layer",
         "d": "Provides the <b>interface between the applications we use to communicate and "
              "the underlying network</b>; application layer protocols exchange data between "
              "programs running on source and destination hosts.", "r": 2},
        {"t": "Application vs service vs protocol (from the summary)",
         "d": "<b>Applications</b> = programs the user interacts with that initiate data "
              "transfer on request; <b>services</b> = background programs connecting the "
              "application layer to lower layers; <b>protocols</b> = agreed rules/processes "
              "letting services on one device exchange data with a range of devices.",
         "r": 26},
        {"t": "Presentation layer",
         "d": "Coding and conversion of application data, <b>data compression</b>, and "
              "<b>encryption for transmission / decryption on receipt</b>; also coding "
              "standards for video and graphics.", "r": 4},
        {"t": "Session layer",
         "d": "Functions that <b>create and maintain dialogs</b> between source and "
              "destination applications — initiating dialogs, keeping them active and "
              "restarting sessions.", "r": 4},
        {"t": "Peer-to-peer (P2P)",
         "d": "Both devices are <b>equal</b> in the communication; client/server roles are "
              "set <b>per request</b>; in P2P applications both act as client and server at "
              "the same time.", "r": 6},
        {"t": "Client-server model",
         "d": "One side provides services (server), the other requests them (client) — the "
              "model web browsers and e-mail clients assume "
              "(<i>client/server basics from Chapter 1, slide 6</i>).", "r": 8},
        {"t": "HTTP", "abbr": "Hypertext Transfer Protocol",
         "d": "Used to publish and retrieve HTML pages; specifies a <b>request/response "
              "protocol</b>; common messages: <b>GET</b> (client request for data), <b>POST</b> "
              "and <b>PUT</b> (send messages that upload data to the web server).", "r": 13},
        {"t": "URL parts (as the browser sees them)",
         "d": "<code>http</code> = the protocol/scheme; <code>www.cisco.com</code> = the "
              "server name (resolved to a numeric address); <code>index.html</code> = the "
              "specific file requested — then a <b>GET</b> request is sent and the server "
              "returns HTML for the browser to format.", "r": 12},
        {"t": "SMTP", "abbr": "Simple Mail Transfer Protocol",
         "d": "<b>Sends (transfers) e-mail</b>; SMTP processes must run on both client and "
              "server; <b>uses port 25</b>.", "r": 15},
        {"t": "POP / POP3", "abbr": "Post Office Protocol",
         "d": "Lets a workstation <b>retrieve</b> mail from a mail server — mail is "
              "<b>downloaded to the client and deleted on the server</b>; <b>uses port "
              "110</b>; desirable for ISPs because it relieves them of storing large mail "
              "volumes.", "r": 15},
        {"t": "IMAP", "abbr": "Internet Message Access Protocol",
         "d": "Another retrieval protocol: <b>copies</b> of messages are downloaded while "
              "<b>originals stay on the server until manually deleted</b> — the contrast with "
              "POP.", "r": 17},
        {"t": "DNS", "abbr": "Domain Name Service",
         "d": "Resolves a URL/host <b>name to its numeric network address</b>.", "r": 18},
        {"t": "TLD", "abbr": "top-level domain",
         "d": "The suffix level of DNS names (the hierarchy slide gives examples such as "
              "organization/industry endings — shown as a figure).", "r": 19},
        {"t": "nslookup",
         "d": "Operating-system utility to <b>manually query name servers</b> to resolve a "
              "host name — used to troubleshoot name resolution and verify name-server "
              "status.", "r": 20},
        {"t": "DHCP", "abbr": "Dynamic Host Configuration Protocol",
         "d": "Lets a host <b>obtain an IP address dynamically</b>: the DHCP server chooses "
              "one from a configured range (<b>pool</b>) and <b>leases</b> it for a set "
              "period; used for general-purpose end-user hosts.", "r": 21},
        {"t": "FTP", "abbr": "File Transfer Protocol",
         "d": "Data transfers between client and server; requires <b>two connections</b> — one "
              "for <b>commands and replies</b>, one for the <b>actual file transfer</b>.",
         "r": 24},
        {"t": "MDA", "abbr": "mail delivery agent (in the mail flow)",
         "d": "The chapter notes mail transfer components can also solve issues like "
              "<b>virus scanning and spam filtering</b>.", "r": 16},
    ],
    "explanations": [
        {"t": "Where presentation and session went",
         "d": "Most applications (web browsers using HTTP, e-mail clients using SMTP/POP) "
              "<b>incorporate the functionality of the application, presentation and session "
              "layers</b>. So the 'layers' still exist as functions — coding/conversion, "
              "compression, encryption, dialog management — but live inside the software you "
              "run.",
         "e": "When your browser encrypts a connection and resumes a session after a brief "
              "drop, it is performing presentation and session work itself.",
         "r": 3},
        {"t": "Web page fetch, step by step (the chapter's flow)",
         "d": "1) Browser interprets the URL: scheme <code>http</code>, server name, file "
              "name. 2) The server name is resolved to a numeric address. 3) Using HTTP "
              "requirements, a <b>GET request</b> is sent. 4) The server sends the page's "
              "<b>HTML code</b>. 5) The browser deciphers the HTML and formats the page.",
         "e": "Every page load you have ever done repeats these five steps.",
         "r": 12},
        {"t": "The three e-mail jobs — and the POP/IMAP split",
         "d": "<b>SMTP transfers mail</b> (both ends run SMTP; port 25). <b>POP retrieves</b> "
              "(port 110): download then <b>delete on server</b> — light storage burden, good "
              "for ISPs. <b>IMAP also retrieves</b>, but keeps <b>originals on the server "
              "until manually deleted</b>, with copies local — better for multi-device "
              "access. Retrieval is where POP and IMAP compete; SMTP is always the sender's "
              "transfer protocol.",
         "e": "Check mail on two devices? IMAP keeps the master copy server-side; POP's "
              "download-and-delete would strip it after the first device.",
         "r": 17},
        {"t": "DHCP leasing in plain language",
         "d": "A host needing an address <b>contacts the DHCP server and requests one</b>; "
              "the server picks from a configured <b>pool</b> and <b>leases</b> it for a set "
              "period. Lease = temporary, renewable ownership — which is why addresses can "
              "change, and why planned/static assignments belong in the addressing plan "
              "(Chapter 9).",
         "e": "Laptop joins the office network: DHCP hands it an address from the pool for a "
              "few hours.",
         "r": 21},
        {"t": "FTP's two-connection design",
         "d": "FTP needs <b>two separate connections between client and server</b>: one for "
              "<b>commands and replies</b> (control), one for the <b>actual file transfer</b> "
              "(data). Separating them lets control messages flow while bulk data moves.",
         "e": "During a large upload you can still issue commands because they travel on the "
              "separate connection.",
         "r": 24},
        {"t": "Getting data through the internetwork (the layer checklist)",
         "d": "The chapter's closing slide lists what travels at each step as data moves "
              "through the stack: <b>code, compress, encrypt</b>, segment (with port #, seq #) "
              "and add <b>source &amp; destination IP addresses</b> and <b>source &amp; "
              "destination MAC addresses</b> — the whole journey in one line, matching the "
              "encapsulation story of Chapter 3.",
         "e": "One e-mail attachment touches presentation (encode/compress/encrypt), "
              "transport (port + sequence), network (IPs) and data link (MACs).",
         "r": 25},
    ],
    "comparisons": [
        {"t": "Peer-to-peer vs client-server",
         "cols": ["Aspect", "Peer-to-peer", "Client-server"],
         "rows": [
             ["Relationship", "Both devices are <b>equal</b> in the communication",
              "One side serves, the other requests"],
             ["Roles", "Client and server roles set <b>per request</b>",
              "Roles are fixed by the model"],
             ["Same time?", "Both act as client and server <b>at the same time</b>",
              "Server provides, clients consume"],
             ["In the course", "Peer-to-peer applications slide",
              "Web browsers (HTTP) and e-mail clients (SMTP/POP) incorporate the model"],
         ],
         "note": "Chapter 1's baseline: clients request services, servers provide them, and "
                 "software determines the role.",
         "refs": [6, 7, 3]},
        {"t": "POP vs IMAP (mail retrieval)",
         "cols": ["Aspect", "POP (POP3)", "IMAP"],
         "rows": [
             ["Job", "Retrieve mail from a mail server", "Retrieve mail from a mail server"],
             ["What happens to the server copy",
              "Mail is <b>downloaded to the client and deleted on the server</b>",
              "<b>Originals kept on the server</b> until manually deleted; copies downloaded"],
             ["Port", "110", "(chapter does not state IMAP's port)"],
             ["Fit", "Desirable for ISPs — relieves large mail storage on servers",
              "Retrieval where server-side originals matter (multi-device)"],
         ],
         "note": "Both retrieve; SMTP (port 25) is the separate transfer/send protocol.",
         "refs": [15, 17]},
    ],
    "facts": [
        {"d": "Application layer = the <b>interface between applications and the underlying "
              "network</b>; protocols exchange data between programs on source and "
              "destination hosts.", "r": 2},
        {"d": "Most applications incorporate <b>application, presentation and session</b> "
              "functionality; protocol families named: DNS, HTTP, DHCP, FTP; transfer/retrieval "
              "via SMTP, IMAP, POP.", "r": 3},
        {"d": "Presentation: coding/conversion, <b>compression, encryption/decryption</b>; "
              "Session: create/maintain <b>dialogs</b>, keep them active, restart sessions.",
         "r": 4},
        {"d": "Three everyday protocols: <b>HTTP</b> to browse the web, <b>SMTP</b> to send "
              "e-mail, <b>POP</b> to receive e-mail.", "r": 11},
        {"d": "URL parts: scheme (<code>http</code>), server name, file name → GET → server "
              "returns HTML → browser formats the page.", "r": 12},
        {"d": "HTTP messages: <b>GET</b> (request data); <b>POST / PUT</b> (upload data to "
              "the web server); request/response protocol.", "r": 13},
        {"d": "<b>SMTP: transfer mail, port 25</b>, SMTP processes on both client and server; "
              "<b>POP: retrieve, port 110</b>, download-and-delete, ISP-friendly storage.",
         "r": 15},
        {"d": "<b>IMAP retrieves</b> by keeping <b>originals on the server until manually "
              "deleted</b>; mail components can also do <b>virus scanning and spam "
              "filtering</b>.", "r": 17},
        {"d": "<b>DNS resolves URL names to numeric addresses</b>; <b>nslookup</b> manually "
              "queries name servers to troubleshoot/verify status.", "r": 20},
        {"d": "DHCP: request → server picks from a configured <b>pool</b> → <b>lease</b> for "
              "a set period; for general-purpose end-user hosts.", "r": 21},
        {"d": "<b>FTP needs two connections</b>: commands/replies + file transfer.", "r": 24},
        {"d": "End-to-end checklist: code, compress, encrypt segment, port #, seq #, "
              "source &amp; destination IP addresses, source &amp; destination MAC addresses.",
         "r": 25},
        {"d": "Summary definitions: applications initiate transfer at user request; services "
              "are background connectors to lower layers; protocols are the agreed rules.",
         "r": 26},
    ],
    "questions": [
        {"type": "mc",
         "q": "What does the application layer provide, according to the chapter?",
         "opts": ["The interface between the applications we use and the underlying network",
                  "Encryption of all traffic on the wire",
                  "The physical signaling of bits",
                  "Routing between IP subnetworks"],
         "a": "A — the interface between applications and the underlying network",
         "why": "Slide 2 states this directly and adds that application layer protocols "
                "exchange data between programs on the source and destination hosts."},
        {"type": "tf",
         "q": "With POP, mail is downloaded from the server to the client and deleted on the "
              "server, whereas IMAP keeps originals on the server until they are manually "
              "deleted.",
         "a": "True",
         "why": "Slides 15/17 (POP download-and-delete) and slide 17 (IMAP: 'Original "
                "messages are kept on the server until manually deleted')."},
        {"type": "short",
         "q": "Name the ports stated for SMTP and POP, and the job each protocol does.",
         "a": "SMTP — transferring (sending) mail — port 25; POP — retrieving mail — "
              "port 110.",
         "why": "Slide 15: SMTP 'uses port 25'; POP 'uses port 110'; both jobs described "
                "there."},
        {"type": "mc",
         "q": "A URL is interpreted as <code>http</code> / <code>www.cisco.com</code> / "
              "<code>index.html</code>. What do the three parts mean, and what is sent next?",
         "opts": ["Protocol (scheme), server name, file name — then a GET request",
                  "Server name, protocol, file name — then a DNS response",
                  "Protocol, user name, password — then a POST request",
                  "File name, host, port — then an ARP request"],
         "a": "A — scheme, server name, file name → GET request",
         "why": "Slide 12's numbered flow: browser interprets protocol/server/file, resolves "
                "the numeric address, sends a GET; the server returns HTML to format."},
        {"type": "short",
         "q": "Why does FTP require two connections?",
         "a": "One connection carries commands and replies; the other carries the actual "
              "file transfer.",
         "why": "Slide 24: 'To successfully transfer data, FTP requires two connections between "
                "the client and the server, one for commands and replies, the other for the "
                "actual file transfer.'"},
        {"type": "explain",
         "q": "Explain what DHCP does when a host joins the network, using the terms "
              "'pool' and 'lease'.",
         "a": "The host requests an address; the DHCP server chooses one from a configured "
              "range of addresses called a pool and leases it to the host for a set period. "
              "DHCP is used for general-purpose hosts such as end-user devices.",
         "why": "Slide 21 describes this sequence verbatim."},
        {"type": "mc",
         "q": "Which pair correctly matches a protocol to its function in the chapter?",
         "opts": ["DNS — resolves a name to a numeric address; nslookup — manual queries to "
                  "name servers",
                  "SMTP — retrieves mail; POP — sends mail",
                  "FTP — assigns IP addresses; DHCP — transfers files",
                  "HTTP — encrypts e-mail; IMAP — browses the web"],
         "a": "A — DNS resolves names; nslookup queries name servers",
         "why": "Slides 18 and 20 give both functions; the others invert or misassign the "
                "protocols listed across slides 11–24."},
        {"type": "explain",
         "q": "Using the presentation and session descriptions, show where 'compress, encrypt, "
              "keep the dialog alive' fits — and why the chapter says most applications "
              "incorporate all three layers.",
         "a": "Compression and encryption/decryption are <b>presentation</b> functions; "
              "creating, maintaining and restarting dialogs is <b>session</b> work. Web "
              "browsers and e-mail clients fold application + presentation + session "
              "functionality into one program, so users experience them as part of the app "
              "rather than separate layers.",
         "why": "Slides 3–4 provide the three layer descriptions and the 'incorporate' "
                "statement."},
    ],
    "misunderstandings": [
        {"t": "The application layer is the application itself",
         "d": "The <b>layer</b> is the interface and the set of protocols (HTTP, SMTP, DNS…) "
              "exchanging data between programs; <b>applications</b> are the user-facing "
              "programs, <b>services</b> the background connectors (summary, slide 26)."},
        {"t": "POP and IMAP are interchangeable",
         "d": "Both retrieve, but POP <b>deletes the server copy after download</b> (port "
              "110) while IMAP <b>keeps originals on the server</b> until manually deleted — "
              "different behaviour matters across devices (slides 15, 17)."},
        {"t": "DNS assigns addresses / DHCP resolves names",
         "d": "Opposite roles: <b>DNS</b> resolves names → numeric addresses; <b>DHCP</b> "
              "hands out the addresses themselves from a pool (slides 18, 21)."},
        {"t": "HTTPS is explained as 'HTTP plus a lock icon'",
         "d": "The chapter's HTTP/HTTPS slide describes HTTP's request/response and message "
              "types; it does <b>not</b> state HTTPS's security mechanism in the extractable "
                "text — treat HTTPS specifics as outside this deck (slide 13, gap note below)."},
        {"t": "Peer-to-peer means 'no clients or servers'",
         "d": "Roles still exist — they're simply <b>set per request</b>, with both devices "
              "acting as client and server at the same time (slides 6–7)."},
    ],
    "quick": (
        "<ul>"
        "<li><b>Application layer:</b> interface between user programs and the network; "
        "protocols move data between programs. Apps (user-facing) vs services (background) vs "
        "protocols (agreed rules).</li>"
        "<li><b>Presentation:</b> coding/conversion, compression, encryption/decryption. "
        "<b>Session:</b> dialogs — start, keep alive, restart. Modern apps fold both in.</li>"
        "<li><b>Models:</b> P2P = equal peers, roles per request, both roles at once; "
        "client-server = dedicated server vs requesting clients.</li>"
        "<li><b>Web:</b> URL = scheme + server + file → resolve → GET → HTML returned → "
        "browser formats. HTTP messages: GET, POST, PUT.</li>"
        "<li><b>E-mail:</b> SMTP sends (port 25) · POP retrieves, download-and-delete "
        "(port 110) · IMAP retrieves, originals stay on server. MDA can scan for viruses/"
        "spam.</li>"
        "<li><b>DNS</b> name → numeric address; <b>nslookup</b> queries/troubleshoots name "
        "servers. <b>DHCP</b> leases addresses from a pool to end-user hosts.</li>"
        "<li><b>FTP:</b> two connections — commands/replies + file transfer. End-to-end: code, "
        "compress, encrypt, segment (port#, seq#) + IP and MAC addresses.</li>"
        "</ul>"
    ),
    "gaps": [
        "The <b>client-server model</b> slides (8–9), <b>DNS hierarchy</b> (19), "
        "<b>DHCP operation</b> (23) and parts of the mail-flow slides are figure-based — the "
        "DHCP message exchange steps in particular are not in the extractable text, so no "
        "step list is given here (client/server basics are quoted from Chapter 1 slide 6 "
        "instead, cross-referenced).",
        "<b>HTTPS</b> appears only in a slide title alongside HTTP — the security properties "
        "of HTTPS are not stated in this chapter's extractable text, so none are asserted.",
        "The chapter outline slide lists section '10.2 Well-Known Application Layer Protocols "
        "and Services' — no separate text was found for a 10.3; the summary (26) closes the "
        "chapter.",
    ],
}
