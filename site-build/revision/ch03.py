# Revision kit content — Chapter 3: Network Protocols and Communication
# Grounded in uploads/Chapter 3_ITN_Network Protocols and Communication.pdf.

DATA = {
    "overview": (
        "Chapter 3 explains <b>the rules that make communication possible</b>: what it takes "
        "for two devices to agree to communicate (sender/receiver, method, language, timing, "
        "acknowledgements), how protocols encode those rules (formatting, pathway sharing, "
        "error messages, session setup/termination), and who standardizes them (IEEE, ISO, "
        "EIA/TIA, ITU, ICANN, IETF). It then introduces the two big models — <b>OSI</b> and "
        "<b>TCP/IP</b> — the benefits of layered models, and how data actually moves: "
        "segmentation, encapsulation, PDUs (data, segment, packet, frame, bits), "
        "de-encapsulation, and communication with local versus remote devices using MAC and "
        "IP addresses."
    ),
    "objectives": [
        "Describe what must be established before communication occurs "
        "(<a class=\"rev-link\" href=\"#p5\">slide 5</a>) and the five timing/delivery rules "
        "(<a class=\"rev-link\" href=\"#p6\">slides 6–10</a>).",
        "Explain what a network protocol suite describes and how application, transport, "
        "internet and network-access protocols interact "
        "(<a class=\"rev-link\" href=\"#p13\">slides 13–15</a>).",
        "Identify the roles of key standards organizations — IEEE, ISO, EIA/TIA, ITU, ICANN "
        "(<a class=\"rev-link\" href=\"#p16\">slides 16–19</a>).",
        "Explain the purpose of the OSI and TCP/IP reference models and the benefits of "
        "layering (<a class=\"rev-link\" href=\"#p20\">slides 20–23</a>).",
        "Trace data through the stack: segmentation, encapsulation, PDUs, de-encapsulation, "
        "and local vs remote communication with MAC and IP addresses "
        "(<a class=\"rev-link\" href=\"#p25\">slides 25–32</a>).",
    ],
    "concepts": [
        "<b>Communication rules</b> — sender/receiver, agreed method, common language, "
        "speed/timing, acknowledgements.",
        "<b>Protocols &amp; suites</b> — e.g. IP, HTTP, DHCP; TCP/IP is the Internet's suite.",
        "<b>Layered reference models</b> — OSI (understanding functions) and TCP/IP "
        "(the implemented Internet standard).",
        "<b>Encapsulation / de-encapsulation</b> — headers added going down, removed going up.",
        "<b>PDUs</b> — data, segment, packet, frame, bits (named per the TCP/IP suite).",
        "<b>MAC vs IP addresses</b> — 48-bit burned-in local identity vs 32-bit (IPv4) / "
        "128-bit (IPv6) logical addressing.",
    ],
    "definitions": [
        {"t": "Protocol",
         "d": "The agreed rules for communication — how messages are formatted, how devices "
              "share pathway information, when error/system messages pass, and how sessions "
              "are set up and terminated.", "r": 13},
        {"t": "Protocol suite (stack)",
         "d": "A stack of cooperating protocols; examples given: <b>IP, HTTP, DHCP</b>; "
              "<b>TCP/IP</b> is the suite used on the Internet.", "r": 13},
        {"t": "Encoding",
         "d": "Representing the message in a transmittable form — the first step after rules "
              "are established.", "r": 6},
        {"t": "Encapsulation",
         "d": "Wrapping data with addressing/labels as it passes down the stack — shown with "
              "the personal-letter analogy (recipient's network, sender's network, recipient "
              "identifier, message content, source identifier, end-of-message marker).",
         "r": 7},
        {"t": "Segmentation",
         "d": "Breaking a long message into pieces that meet the frame size restrictions; each "
              "segment is encapsulated in its own frame with address information, and the "
              "receiver de-encapsulates and reassembles them.", "r": 8},
        {"t": "PDU", "abbr": "Protocol Data Unit",
         "d": "The unit of data at each level, named per the TCP/IP suite: <b>data, segment, "
              "packet, frame, bits</b>.", "r": 26},
        {"t": "Reference model",
         "d": "A layered model whose primary purpose is a <b>clearer understanding of the "
              "functions and processes</b> involved (OSI) / which describes the functions at "
              "each layer of a suite (TCP/IP).", "r": 20},
        {"t": "OSI", "abbr": "Open System Interconnection model",
         "d": "ISO's best-known model; the OSI protocol suite was implemented on "
              "telecommunications equipment, while TCP/IP was implemented for the Internet.",
         "r": 17},
        {"t": "IEEE", "abbr": "Institute of Electrical and Electronics Engineers",
         "d": "Standards body whose <b>802 family</b> deals with LANs and MANs — including "
              "<b>IEEE 802.3</b> (Ethernet) and <b>IEEE 802.11</b> (wireless LAN).", "r": 16},
        {"t": "ISO", "abbr": "International Organization for Standardization",
         "d": "Body best known for the OSI reference model.", "r": 17},
        {"t": "EIA / TIA",
         "abbr": "Electronic Industries Alliance / Telecommunications Industry Association",
         "d": "Standards organizations named for electrical wiring and telecommunications "
              "development.", "r": 19},
        {"t": "ICANN", "abbr": "Internet Corporation for Assigned Names and Numbers",
         "d": "Standards/governance organization listed among bodies governing Internet "
              "resources.", "r": 19},
        {"t": "IPv4 address",
         "d": "A <b>32-bit</b> logical address shown as dotted decimal, e.g. "
              "<code>192.168.10.2</code> (binary <code>11000000.10101000.00001010.00000010</code>).",
         "r": 30},
        {"t": "IPv6 address",
         "d": "A <b>128-bit</b> address (shown as long hexadecimal groups).", "r": 30},
        {"t": "MAC address", "abbr": "also Burned-in Address",
         "d": "A <b>48-bit</b> data-link identity burned into the interface; each host in the "
              "chapter's example carries one alongside its IP address.", "r": 30},
    ],
    "explanations": [
        {"t": "What 'establishing the rules' really means",
         "d": "Before a message is exchanged, five things must be agreed: an <b>identified "
              "sender and receiver</b>, an <b>agreed method</b> of communicating (face-to-face, "
              "telephone, letter…), a <b>common language and grammar</b>, <b>speed and timing "
              "of delivery</b>, and <b>confirmation/acknowledgement requirements</b>. Protocols "
              "are the machine version of exactly these agreements.",
         "e": "Two people on a phone call agree on language (protocol), speak at a pace the "
              "listener can follow (timing), and say 'hello' to confirm the line is live "
              "(acknowledgement).",
         "r": 5},
        {"t": "How protocols interact — the HTTP example",
         "d": "Layers cooperate on one job: the <b>application protocol</b> governs web "
              "client/server interaction; the <b>transport protocol</b> divides the HTTP data "
              "into segments; the <b>Internet protocol</b> encapsulates segments into packets "
              "with IP addresses; the <b>network access protocol</b> formats packets for "
              "transmission over the media.",
         "e": "One web request passes through all four steps without the web app needing to "
              "know about cables or routing.",
         "r": 15},
        {"t": "Why bother with layers? (benefits)",
         "d": "A layered model: helps <b>protocol design</b> (each layer has defined "
              "information and defined interfaces to the layers above/below), <b>fosters "
              "competition</b> between products, <b>prevents technology changes in one layer "
              "from…</b> cascading through the design, and <b>provides a common language</b> "
              "to describe networking functions.",
         "e": "Wi-Fi hardware can improve without forcing every application to change, because "
              "the layers above it keep the same interface.",
         "r": 23},
        {"t": "Encapsulation and de-encapsulation, step by step",
         "d": "Going <b>down</b> the stack, data is segmented, then each segment is "
              "encapsulated with headers (addresses, labels) — PDU names change: data → "
              "segment → packet → frame → bits. At the destination the process <b>reverses</b>: "
              "headers are stripped (de-encapsulation) as the data moves up the stack to be "
              "processed.",
         "e": "The letter analogy: envelope fields (network of recipient, network of sender, "
              "recipient identifier, source identifier, end marker) are added around the "
              "message content and read off at delivery.",
         "r": 27},
        {"t": "Same network vs remote network",
         "d": "When a host talks to a device <b>on its own network</b>, the chapter's example "
              "shows each host has <b>both</b> an IP address and a MAC address, and an <b>ARP "
              "request</b> resolves the neighbour's MAC before frames are exchanged. "
              "Communication with a device on a <b>remote network</b> requires leaving the "
              "local network (routing via an intermediary device).",
         "e": "PC1 (192.168.1.110) reaching FTP server (192.168.1.9) on the same LAN still "
              "needs the server's MAC address — that is the ARP request shown.",
         "r": 31},
        {"t": "Segmentation has a price too",
         "d": "Segmentation lets long messages satisfy frame size limits and can improve "
              "transmission, but the chapter flags a <b>segmenting disadvantage</b> "
              "(more pieces mean more headers/processing and reassembly work at the receiver).",
         "e": "A large file transfer arrives as many frames that must be re-ordered and "
              "reassembled.",
         "r": 25},
    ],
    "comparisons": [
        {"t": "OSI model vs TCP/IP model",
         "cols": ["Aspect", "OSI reference model", "TCP/IP model & suite"],
         "rows": [
             ["Origin", "Best-known model of ISO (ISO's OSI)",
              "TCP/IP suite implemented for the Internet"],
             ["Purpose", "Primary purpose: clearer understanding of the functions and "
              "processes involved",
              "Describes the functions at each layer of protocols within the TCP/IP suite"],
             ["Implementation", "OSI protocol suite was implemented on telecommunications "
              "equipment",
              "Open standard endorsed by the networking industry and ratified by a standards "
              "organization"],
             ["Use", "The most widely used networking model for teaching/analysis",
              "The suite required for transmitting and receiving over the Internet"],
             ["PDU vocabulary", "Layered description of encoding, formatting, segmenting, "
              "encapsulating", "PDUs named per the suite: data, segment, packet, frame, bits"],
         ],
         "note": "Both are introduced as 'the most widely-used networking models'. The stack "
                 "diagrams (layer names/counts) are figures on slides 20–22 — see the gap note "
                 "below; the table quotes only what the source text states.",
         "refs": [17, 20, 21, 33, 34]},
        {"t": "MAC addresses vs IP addresses",
         "cols": ["Aspect", "MAC address", "IP address"],
         "rows": [
             ["Size", "48-bit", "IPv4: 32-bit · IPv6: 128-bit"],
             ["Form", "Burned-in address (e.g. interface hardware identity)",
              "Logical address in dotted decimal (IPv4), e.g. <code>192.168.10.2</code>"],
             ["Role in the chapter", "Data-link identity used in frames on the local network",
              "Logical addressing used to identify the source/destination host (with ARP "
              "bridging the two on the local network)"],
             ["Example from source", "Each host in the example topology carries one "
              "(PC1, PC2, FTP server, R1)",
              "Each device carries one (192.168.1.110, .111, .9, R1 .1)"],
         ],
         "note": "The same-network example shows hosts using both together, with ARP resolving "
                 "IP → MAC on the local network.",
         "refs": [30, 31]},
    ],
    "facts": [
        {"d": "Five prerequisites for communication: identified sender/receiver; agreed "
              "method; common language and grammar; speed and timing of delivery; "
              "confirmation/acknowledgement requirements.", "r": 5},
        {"d": "Message rules also cover <b>encoding, formatting/encapsulation, size "
              "(segmentation)</b> and <b>timing</b> (access method, flow control/windowing, "
              "response timeout).", "r": 9},
        {"d": "Protocols describe: message format; sharing pathway information with other "
              "networks; when error/system messages pass; session setup and termination.",
         "r": 13},
        {"d": "HTTP example across layers: application governs client/server interaction → "
              "transport divides into segments → Internet encapsulates into packets with IP "
              "addresses → network access formats packets for the media.", "r": 15},
        {"d": "IEEE's <b>802 family</b> deals with LANs and MANs; notable standards: "
              "<b>802.3</b> and <b>802.11</b>.", "r": 16},
        {"d": "TCP/IP is the protocol suite used on the Internet; OSI is the model ISO is best "
              "known for.", "r": 17},
        {"d": "Layered models give protocols defined interfaces and a common language, foster "
              "competition, and isolate layer changes.", "r": 23},
        {"d": "Frame size restrictions force segmentation: each piece meets min/max size, is "
              "encapsulated in its own frame with addresses, and is reassembled at the "
              "receiver.", "r": 8},
        {"d": "PDU names by level: <b>bits, frames, packets, segments, data</b> — the summary "
              "lists the TCP/IP names as <b>data, segment, packet, frame, bits</b>.",
         "r": 26},
        {"d": "Address sizes: <b>IPv4 = 32 bits</b>, <b>IPv6 = 128 bits</b>, <b>MAC = 48 "
              "bits</b> (burned-in).", "r": 30},
        {"d": "Most protocols are created by a standards organization such as the <b>IETF or "
              "IEEE</b>; TCP/IP is an open standard endorsed by the industry and ratified by a "
              "standards organization.", "r": 33},
        {"d": "Data passing down the OSI stack is <b>segmented and encapsulated with addresses "
              "and labels</b>; the process is reversed (de-encapsulation) going up the "
              "destination stack.", "r": 33},
    ],
    "questions": [
        {"type": "mc",
         "q": "In the protocol-interaction example, which protocol divides the HTTP message "
              "into smaller segments?",
         "opts": ["Application protocol", "Transport protocol", "Internet protocol",
                  "Network access protocol"],
         "a": "B — Transport protocol",
         "why": "Slide 15: the transport protocol divides the HTTP segment into smaller "
                "pieces/segments; the Internet protocol then encapsulates them into packets."},
        {"type": "tf",
         "q": "A reference model's primary purpose is to give a clearer understanding of the "
              "functions and processes involved.",
         "a": "True",
         "why": "Slide 20 states this as the primary purpose of a reference model."},
        {"type": "short",
         "q": "Name the five things that must be established before communication occurs.",
         "a": "An identified sender and receiver; an agreed method of communicating; a common "
              "language and grammar; speed and timing of delivery; confirmation or "
              "acknowledgement requirements.",
         "why": "Slide 5 lists exactly these five rules."},
        {"type": "short",
         "q": "List the PDU names given for the different levels (four or more).",
         "a": "Bits, frames, packets, segments, data — the summary names the TCP/IP PDUs: data, "
              "segment, packet, frame, bits.",
         "why": "Slides 26 and 34 give the PDU names per level and per the TCP/IP suite."},
        {"type": "mc",
         "q": "Which statement about IEEE is correct according to the chapter?",
         "opts": ["IEEE's 802 family deals with LANs and MANs, including 802.3 and 802.11",
                  "IEEE created the OSI model",
                  "IEEE standards apply only to wireless networks",
                  "IEEE manages IP addresses for the Internet"],
         "a": "A — The 802 family covers LANs/MANs (802.3, 802.11)",
         "why": "Slide 16: 'The IEEE 802 family of standards deals with LANs and MANs', with "
                "802.3 and 802.11 shown. OSI is ISO's model; ICANN relates to names/numbers."},
        {"type": "tf",
         "q": "According to the summary, TCP/IP is an open standard protocol endorsed by the "
              "networking industry and ratified by a standards organization.",
         "a": "True",
         "why": "Chapter summary (slide 34) states this verbatim."},
        {"type": "explain",
         "q": "Explain encapsulation using the chapter's personal-letter analogy, and say what "
              "happens at the receiving host.",
         "a": "Just as a letter carries an envelope with the recipient's location/network, the "
              "sender's location, recipient and source identifiers and an end-of-message "
              "marker around the message content, encapsulation wraps data with addresses and "
              "labels as it moves down the stack. At the receiver the process is reversed — "
              "de-encapsulation — and the messages are reassembled and processed.",
         "why": "Slide 7 gives the letter elements; slides 8 and 27 give the "
                "segmentation/de-encapsulation steps."},
        {"type": "mc",
         "q": "PC1 (192.168.1.110) wants to send a frame to the FTP server on the same LAN. "
              "What does the example topology show is needed first?",
         "opts": ["An ARP request to resolve the server's MAC address",
                  "A DNS query for the server's name",
                  "A route to a remote network",
                  "A new IPv4 address for PC1"],
         "a": "A — An ARP request",
         "why": "Slide 31 shows the same-network example with both IP and MAC addresses and an "
                "ARP request between PC1/S1/R1 so frames can be addressed at data link level."},
    ],
    "misunderstandings": [
        {"t": "Protocol vs protocol suite vs standard",
         "d": "A <b>protocol</b> is one set of rules (HTTP, IP); a <b>suite/stack</b> is a set "
              "of cooperating protocols (TCP/IP); <b>standards organizations</b> (IETF, IEEE) "
              "create/ratify them. The chapter says most protocols come from such bodies "
              "(slides 13, 33)."},
        {"t": "OSI is 'the Internet model'",
         "d": "No — the chapter distinguishes them: OSI (ISO's reference model, implemented on "
              "telecommunications equipment) vs <b>TCP/IP, which was implemented for the "
              "Internet</b> (slide 17). OSI is the teaching/analysis model; TCP/IP is the "
              "suite the Internet runs on."},
        {"t": "MAC address = IP address",
         "d": "Different things: MAC = 48-bit burned-in data-link identity; IPv4 = 32-bit "
              "logical address (IPv6 = 128-bit). The same-network example shows hosts carrying "
              "<b>both</b>, with ARP mapping one to the other (slides 30–31)."},
        {"t": "Segmentation only has advantages",
         "d": "The chapter explicitly notes a <b>segmenting disadvantage</b> alongside the "
              "benefits (slide 25) — more pieces mean more encapsulation overhead and "
              "reassembly at the receiver."},
    ],
    "quick": (
        "<ul>"
        "<li><b>Rules first:</b> sender/receiver, method, language/grammar, timing/speed, "
        "acknowledgements — then encoding, formatting/encapsulation, size limits, timing "
        "(access method, windowing, response timeout).</li>"
        "<li><b>Protocols</b> (IP, HTTP, DHCP) define message format, path sharing, error "
        "messages, session setup/termination; layers cooperate: application → transport "
        "(segments) → internet (packets with IP) → network access (frames on media).</li>"
        "<li><b>Standards:</b> IEEE (802 family: 802.3, 802.11 — LANs/MANs), ISO (OSI), "
        "EIA/TIA, ITU-T, ICANN; most protocols from IETF/IEEE.</li>"
        "<li><b>Models:</b> OSI = understanding functions/processes; TCP/IP = open, "
        "industry-ratified suite the Internet uses. Layering → defined interfaces, common "
        "language, competition, isolated changes.</li>"
        "<li><b>Moving data:</b> segment (frame size limits) → encapsulate with addresses → "
        "PDU names data/segment/packet/frame/bits → destination de-encapsulates upward.</li>"
        "<li><b>Addresses:</b> IPv4 32-bit (192.168.10.2), IPv6 128-bit, MAC 48-bit "
        "burned-in; same-network traffic uses MAC+ARP, remote traffic leaves via "
        "intermediary devices.</li>"
        "</ul>"
    ),
    "gaps": [
        "Slide 23's benefit sentences are partially cut in text extraction (e.g. '…prevents "
        "technology or capability changes in one layer from' and 'fosters competition because "
        "products from different…') — check the slide figure for the full wording.",
        "The <b>message delivery options</b> slide (slide 10), the <b>benefits of a layered "
        "model</b> slide (18) and the <b>OSI/TCP/IP stack diagrams</b> (slides 20–22) are "
        "figure-based — the layer names/counts are not in the extractable text, so no "
        "layer-by-layer table is reproduced here.",
        "The homework slide lists activity/lab titles (3.2.2.5, 3.2.4.5, 3.2.4.6, 3.3.1.5, "
        "3.4.1.2) with no instructions in the source.",
    ],
}
