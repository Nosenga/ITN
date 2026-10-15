# Revision kit content — Chapter 7: Transport Layer
# Grounded in uploads/Chapter 7_ITN_Transport Layer.pdf (slide refs = page numbers).

DATA = {
    "overview": (
        "Chapter 7 is about <b>how applications get their data, intact and in order — or "
        "fast, without guarantees</b>. It opens with the transport layer's role: temporary "
        "sessions between applications, tracking conversations, segmentation and reassembly, "
        "and identifying the right application. It covers <b>multiplexing</b> (many "
        "conversations interleaved, distinguished by header + port numbers), the "
        "<b>reliability trade-off</b> (acknowledged delivery costs overhead), then the two "
        "protocols themselves: <b>TCP</b> (RFC 793 — connection-oriented, reliable, ordered, "
        "flow-controlled, stateful) versus <b>UDP</b> (RFC 768 — connectionless, unreliable, "
        "stateless, low overhead). Section 7.2 walks through the <b>three-way handshake</b>, "
        "session termination, sequence numbers, acknowledgements, window size and UDP "
        "datagram reassembly — and closes with the layer's three main services: multiplexing, "
        "segmentation/reassembly and error checking."
    ),
    "objectives": [
        "State the transport layer's responsibilities and its three main services "
        "(<a class=\"rev-link\" href=\"#p3\">slides 3–8</a>, summary).",
        "Explain conversation multiplexing and how port numbers separate applications "
        "(<a class=\"rev-link\" href=\"#p5\">slides 5–12</a>).",
        "Compare TCP and UDP feature by feature and match real applications to each "
        "(<a class=\"rev-link\" href=\"#p9\">slides 9–13</a>).",
        "Describe how a TCP session is established (three-way handshake) and terminated "
        "(<a class=\"rev-link\" href=\"#p17\">slides 17–22</a>).",
        "Explain reliability mechanisms: sequence numbers, acknowledgements, window size and "
        "reassembly (<a class=\"rev-link\" href=\"#p23\">slides 23–25</a>).",
    ],
    "concepts": [
        "<b>Temporary sessions</b> — the transport layer establishes sessions between "
        "applications and delivers data between them.",
        "<b>Multiplexing &amp; ports</b> — many simultaneous conversations interleaved; ports "
        "identify the application.",
        "<b>Segmentation &amp; reassembly</b> — split data into segments with headers; "
        "rebuild streams at the destination.",
        "<b>Reliability trade-off</b> — acknowledged delivery vs overhead; the application "
        "developer chooses.",
        "<b>TCP vs UDP</b> — stateful/reliable/ordered vs stateless/connectionless/low "
        "overhead.",
        "<b>Flow control via window size</b> — how much may be sent before an acknowledgement "
        "is required.",
    ],
    "definitions": [
        {"t": "Transport layer",
         "d": "Responsible for <b>establishing a temporary communication session between two "
              "applications</b> and delivering data between them; TCP/IP uses TCP and UDP.",
         "r": 3},
        {"t": "Multiplexing", "abbr": "conversation multiplexing",
         "d": "Enabling many communications from many users to be <b>interleaved on the same "
              "network at the same time</b>; each segment gets a header to identify it so both "
              "sending and receiving work with multiple applications running.", "r": 5},
        {"t": "Segmentation",
         "d": "The transport layer dividing application data into manageable pieces and "
              "adding a header for delivery; the destination <b>reassembles</b> them into "
              "application data streams.", "r": 3},
        {"t": "Port numbers",
         "d": "TCP and UDP use port numbers to <b>differentiate between applications</b> — "
              "the header field that gets each segment to the right application.", "r": 11},
        {"t": "TCP", "abbr": "Transmission Control Protocol",
         "d": "<b>RFC 793</b>; connection-oriented (creates a session), reliable delivery "
              "(retransmits lost/corrupt data), ordered data reconstruction, flow control, "
              "<b>stateful</b> (tracks the session).", "r": 9},
        {"t": "UDP", "abbr": "User Datagram Protocol",
         "d": "<b>RFC 768</b>; connectionless, unreliable delivery, no ordered "
              "reconstruction, no flow control, <b>stateless</b>. Used by DNS, video "
              "streaming, VoIP.", "r": 10},
        {"t": "Connection-oriented vs connectionless",
         "d": "Connection-oriented (TCP) <b>creates a session</b> first; connectionless (UDP) "
              "sends without establishing one.", "r": 9},
        {"t": "Stateful vs stateless",
         "d": "TCP is stateful — it <b>tracks the session</b>; UDP is stateless — it keeps no "
              "session state.", "r": 10},
        {"t": "Flow control",
         "d": "Regulating the amount of data transmitted — TCP feature implemented with "
              "<b>window size</b>: the amount of data a source may transmit before an "
              "acknowledgement must be received.", "r": 24},
        {"t": "Sequence number",
         "d": "Used to <b>reassemble segments into their original order</b> (ordered delivery).",
         "r": 23},
        {"t": "Acknowledgement number",
         "d": "Used <b>together with the sequence number to confirm receipt</b> of data.",
         "r": 24},
        {"t": "Window size",
         "d": "The amount of data a source can transmit <b>before an acknowledgement must be "
              "received</b>.", "r": 24},
        {"t": "Three-way handshake",
         "d": "TCP's session-establishment process: confirm the destination device is present, "
              "verify it has an active service accepting requests on the intended port, and "
              "inform it that the source intends to establish a session on that port.",
         "r": 17},
        {"t": "Netstat",
         "d": "A tool used to <b>examine TCP connections</b> that are open and running on a "
              "networked host.", "r": 14},
        {"t": "RFC",
         "abbr": "Request for Comments",
         "d": "The documents defining protocols — TCP is defined in <b>RFC 793</b>, UDP in "
              "<b>RFC 768</b>.", "r": 9},
    ],
    "explanations": [
        {"t": "The reliability trade-off in one sentence",
         "d": "Reliable delivery 'ensures all data arrives' using acknowledgements and "
              "retransmission — but 'makes larger demands on the network, more overhead'. UDP "
              "gives 'just the basic functions for delivery — no reliability' with less "
              "overhead. <b>There is a trade-off between the value of reliability and the "
              "burden it places on the network</b>, so application developers choose per "
              "application.",
         "e": "File transfer needs every byte (TCP); a live voice call needs low delay more "
              "than perfect loss (UDP).",
         "r": 8},
        {"t": "Why UDP still exists (and wins sometimes)",
         "d": "UDP is simple, connectionless and stateless — for apps that can <b>tolerate "
              "small loss</b> or <b>cannot tolerate delay</b>. The chapter lists: DNS, "
              "SNMP, DHCP, TFTP, IP telephony/VoIP and online games (plus video streaming from "
              "the UDP slide).",
         "e": "In VoIP, a retransmitted voice packet arriving late is useless — dropping it "
              "and moving on beats waiting.",
         "r": 13},
        {"t": "What the three-way handshake is checking",
         "d": "Before data flows, TCP must: (1) establish the destination device is "
              "<b>present on the network</b>; (2) verify it has an <b>active service "
              "accepting requests on the destination port</b> the client intends to use; "
              "(3) inform it that the source <b>intends to establish a session</b> on that "
              "port. Only then is the session up — and TCP, being stateful, tracks it.",
         "e": "Opening a web session: the client must confirm something is actually listening "
              "on the server's port before sending the request.",
         "r": 17},
        {"t": "How ordered, confirmed delivery works",
         "d": "<b>Sequence numbers</b> reassemble segments into original order even if they "
              "arrive shuffled. <b>Sequence + acknowledgement numbers</b> are used together to "
              "<b>confirm receipt</b>. <b>Window size</b> paces the sender: that much data may "
              "be in flight before an ACK must come back — flow control in practice.",
         "e": "Window size 3 segments → send 3, wait for ACK, then send more — the receiver "
              "never gets overwhelmed.",
         "r": 24},
        {"t": "Multiplexing: how two users' downloads don't mix",
         "d": "Many conversations are interleaved on the network simultaneously. Each segment "
              "carries a <b>header identifying it</b> (ports) so the receiving host can hand "
              "each stream to the correct application — the summary describes ports as a "
              "'tunnel' from the transport layer to the right application.",
         "e": "Your browser and music stream run at once: different ports route each stream "
              "back to its own application.",
         "r": 5},
        {"t": "Segmentation from the layer's own perspective",
         "d": "The transport layer divides data from the application into segments, adds a "
              "header to identify and manage each segment, uses that header to reassemble "
              "them, and passes the result to the correct application — the chapter calls "
              "these the layer's three main services together with multiplexing and error "
              "checking.",
         "e": "A large file arrives as many segments; sequence numbers rebuild it byte-for-byte "
              "before the application sees it.",
         "r": 26},
    ],
    "comparisons": [
        {"t": "TCP vs UDP",
         "cols": ["Aspect", "TCP (RFC 793)", "UDP (RFC 768)"],
         "rows": [
             ["Connection", "Connection-oriented — creates a session between source and "
              "destination", "Connectionless"],
             ["Delivery", "Reliable — retransmits lost or corrupt data",
              "Unreliable delivery — just basic functions"],
             ["Ordering", "Ordered data reconstruction (numbering/sequencing)",
              "No ordered data reconstruction"],
             ["Flow control", "Yes — regulates the amount of data transmitted",
              "No flow control"],
             ["State", "Stateful — tracks the session", "Stateless"],
             ["Overhead", "Larger demands on the network — more overhead", "Less overhead"],
             ["Typical applications (from the chapter)", "Reliable delivery apps (e.g. file/web "
              "transfer style traffic)", "DNS, video streaming, VoIP, SNMP, DHCP, TFTP, IP "
              "telephony, online games"],
         ],
         "note": "The chapter's rule: developers choose based on 'the trade-off between the "
                 "value of reliability and the burden it places on the network'.",
         "refs": [8, 9, 10, 13]},
    ],
    "facts": [
        {"d": "Transport layer role: establish a <b>temporary session between two "
              "applications</b> and deliver data between them; TCP/IP uses TCP and UDP.",
         "r": 3},
        {"d": "Its duties: track individual communications, segment for manageability and "
              "reassemble at the destination, identify the proper application for each "
              "stream.", "r": 3},
        {"d": "<b>Multiplexing:</b> many users' communications interleaved on the same network "
              "at the same time; header added to each segment to identify it.", "r": 5},
        {"d": "Reliability comparison: acknowledged delivery = more overhead; basic delivery = "
              "no reliability, less overhead; the app developer chooses the protocol.",
         "r": 8},
        {"d": "TCP = RFC 793, connection-oriented, reliable, ordered, flow-controlled, "
              "<b>stateful</b>.", "r": 9},
        {"d": "UDP = RFC 768, connectionless, unreliable, unordered, no flow control, "
              "<b>stateless</b>; apps: <b>DNS, video streaming, VoIP</b>.", "r": 10},
        {"d": "<b>Port numbers differentiate applications</b>; <b>netstat</b> examines open, "
              "running TCP connections on a host.", "r": 14},
        {"d": "UDP low-overhead users: apps that <b>tolerate small loss</b> or <b>cannot "
              "tolerate delay</b> — DNS, SNMP, DHCP, TFTP, VoIP, online games.", "r": 13},
        {"d": "Handshake purposes: destination is <b>present</b>; has an <b>active service "
              "accepting on the target port</b>; is <b>informed of the intent</b> to "
              "establish the session.", "r": 17},
        {"d": "<b>Sequence numbers</b> restore original order; <b>seq + ack numbers confirm "
              "receipt</b>; <b>window size</b> = data allowed in flight before an ACK is due.",
         "r": 24},
        {"d": "Summary — three main services: <b>multiplexing, segmentation and reassembly, "
              "error checking</b>; ports are a 'tunnel' to the right application; transport "
              "functions matter for QoS and security.", "r": 26},
        {"d": "The layer map places <b>segments, TCP/UDP, windowing, ACK, sequence numbers "
              "and ports</b> at the transport layer.", "r": 2},
    ],
    "questions": [
        {"type": "mc",
         "q": "According to the summary, what are the three main services of the transport "
              "layer?",
         "opts": ["Multiplexing, segmentation and reassembly, and error checking",
                  "Routing, addressing, and forwarding",
                  "Encryption, authentication, and accounting",
                  "Framing, media access, and error detection"],
         "a": "A — Multiplexing, segmentation and reassembly, and error checking",
         "why": "The chapter summary states these three main services and explains dividing "
                "data into segments, adding headers, reassembling and passing data to the "
                "correct application."},
        {"type": "tf",
         "q": "TCP is a stateful protocol that tracks the session, while UDP is stateless.",
         "a": "True",
         "why": "TCP slide (9): 'Stateful protocol — tracks the session'; UDP slide (10): "
                "'Stateless protocol'."},
        {"type": "mc",
         "q": "A game developer needs minimal delay and can tolerate losing an occasional "
              "packet. Which protocol fits, and why?",
         "opts": ["UDP — connectionless, no flow control, less overhead",
                  "TCP — retransmission guarantees nothing is lost",
                  "TCP — because games need ordered delivery above all",
                  "Either — the chapter says the protocols are interchangeable"],
         "a": "A — UDP",
         "why": "UDP is for applications that 'can tolerate small loss of data' and 'cannot "
                "tolerate delay' — online games are listed as UDP users (slides 10, 13)."},
        {"type": "short",
         "q": "State the three purposes of TCP session establishment listed in the chapter.",
         "a": "1) Establish the destination device is present on the network; 2) verify it has "
              "an active service accepting requests on the destination port the client "
              "intends to use; 3) inform the destination that the source intends to establish "
              "a session on that port.",
         "why": "Slide 17 lists these three bullet points for connection establishment and "
                "termination."},
        {"type": "short",
         "q": "What are sequence numbers used for, and what do sequence and acknowledgement "
              "numbers do together?",
         "a": "Sequence numbers reassemble segments into their original order; together with "
              "acknowledgement numbers they confirm receipt of data.",
         "why": "Slides 23 and 24 state both functions."},
        {"type": "mc",
         "q": "Window size refers to:",
         "opts": ["The amount of data a source can transmit before an acknowledgement must be "
                  "received",
                  "The maximum size of a UDP datagram",
                  "The number of applications on a host",
                  "The time a session stays open"],
         "a": "A — data allowed in flight before an ACK is required",
         "why": "Slide 24 defines window size exactly this way — it is TCP's flow-control "
                "mechanism."},
        {"type": "explain",
         "q": "Why might an application designer deliberately choose UDP even though it is "
              "called 'unreliable'? Support your answer with examples from the chapter.",
         "a": "Because reliability costs overhead, and some applications value low delay or "
              "low overhead over perfect delivery. The chapter lists DNS, SNMP, DHCP, TFTP, "
              "VoIP/IP telephony and online games as UDP users, and notes UDP serves apps "
              "that can tolerate small loss or cannot tolerate delay — plus there is an "
              "explicit trade-off between the value of reliability and the burden it places "
              "on the network.",
         "why": "Slides 8, 10 and 13 give the trade-off and the application lists."},
        {"type": "tf",
         "q": "Port numbers allow TCP and UDP to differentiate between applications, and "
              "<code>netstat</code> can show open TCP connections on a host.",
         "a": "True",
         "why": "Slide 11 (ports differentiate applications) and slide 14 (netstat examines "
                "open, running TCP connections)."},
    ],
    "misunderstandings": [
        {"t": "\"UDP is unreliable, so it's bad\"",
         "d": "Unreliable is a <b>design choice</b> for low overhead/low delay. The chapter "
              "lists DNS, VoIP, streaming and games as deliberate UDP users and frames it as "
              "a trade-off, not a defect (slides 8, 13)."},
        {"t": "Ports identify devices",
         "d": "Ports <b>differentiate applications</b> on hosts — the header gets each segment "
              "to the right application ('tunnel' to the application — summary, slide 26)."},
        {"t": "Multiplexing means one conversation at a time",
         "d": "It is the opposite: many users' communications are <b>interleaved on the same "
              "network at the same time</b>; headers/ports keep them apart (slide 5)."},
        {"t": "The handshake moves data",
         "d": "The three-way handshake <b>establishes and verifies the session</b> (device "
              "present, service listening, intent declared) — it is setup, not the data "
              "transfer itself (slide 17)."},
    ],
    "quick": (
        "<ul>"
        "<li><b>Role:</b> temporary sessions between applications; three main services — "
        "multiplexing, segmentation &amp; reassembly, error checking; ports tunnel data to the "
        "right application.</li>"
        "<li><b>Multiplexing:</b> many conversations interleaved; each segment's header "
        "identifies it.</li>"
        "<li><b>TCP (RFC 793):</b> connection-oriented, reliable (retransmit lost/corrupt), "
        "ordered (sequence numbers), flow control (window size), stateful — more overhead.</li>"
        "<li><b>UDP (RFC 768):</b> connectionless, unreliable, unordered, no flow control, "
        "stateless — less overhead; DNS, SNMP, DHCP, TFTP, VoIP, video, games.</li>"
        "<li><b>Handshake:</b> confirm destination present → service active on target port → "
        "session intent declared; session later terminated the same way.</li>"
        "<li><b>Reliability internals:</b> seq# = original order; seq#+ack# = confirm receipt; "
        "window size = bytes allowed before an ACK must return.</li>"
        "<li><b>Tools:</b> netstat shows open TCP connections. Choose by trade-off: value of "
        "reliability vs burden on the network.</li>"
        "</ul>"
    ),
    "gaps": [
        "The three-way handshake <b>step slides (19–21)</b> and session termination (22) show "
        "their detail (flag names such as SYN/ACK and the packet exchange) as figures — the "
        "extractable text carries the three purposes but not the flag names, so none are "
        "quoted here beyond 'three-way handshake'.",
        "The <b>port numbers</b> slide (12) lists well-known ports as a figure (only 'HTTPS' "
        "text extracted) — no numeric port table is reproduced; check the slide for values.",
        "Datagram reassembly (slide 25) is title-only in the extraction — UDP's reassembly "
        "story is told by the summary's segmentation/reassembly wording instead.",
    ],
}
