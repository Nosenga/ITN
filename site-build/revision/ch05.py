# Revision kit content — Chapter 5: Ethernet
# Grounded in uploads/Chapter 5_ITN_Ethernet - Tagged (1).pdf (slide refs = page numbers).

DATA = {
    "overview": (
        "Chapter 5 is the Ethernet deep dive. It places Ethernet in the IEEE 802.2/802.3 "
        "standards, splits the data link layer into <b>LLC</b> (control information, "
        "upper/lower layer communication) and <b>MAC</b> (frame encapsulation + media access, "
        "implemented in the NIC), and works through frame mechanics: delimiting, MAC "
        "addressing, CRC error detection, frame sizes (64–1518 bytes) and unicast/multicast/"
        "broadcast communication. Section 5.2 covers <b>ARP</b> — resolving IPv4 addresses to "
        "MAC addresses, building ARP tables, local vs remote (gateway) resolution and cache "
        "expiry. Section 5.3 covers <b>LAN switches</b> — MAC-based forwarding/filtering, "
        "collision domains, cut-through switching, buffering — and finishes with <b>Layer 3 "
        "switching</b> (SVIs, routed ports, EtherChannel)."
    ),
    "objectives": [
        "Explain the LLC and MAC sublayers and the MAC sublayer's two responsibilities "
        "(<a class=\"rev-link\" href=\"#p2\">slides 2–8</a>).",
        "Describe Ethernet addressing: 48-bit MAC addresses, OUI rules, frame processing and "
        "frame size limits (<a class=\"rev-link\" href=\"#p9\">slides 9–11</a>).",
        "Distinguish unicast, multicast and broadcast communication and give the multicast "
        "ranges (<a class=\"rev-link\" href=\"#p12\">slides 12–15</a>).",
        "Describe ARP's two functions, its operation on local and remote networks, and how "
        "ARP table entries expire (<a class=\"rev-link\" href=\"#p17\">slides 17–22</a>).",
        "Explain how switches make forwarding decisions and compare Layer 2 with Layer 3 "
        "switching (<a class=\"rev-link\" href=\"#p24\">slides 24–34</a>).",
    ],
    "concepts": [
        "<b>LLC + MAC</b> — one protocol-facing, one media-facing sublayer of Layer 2.",
        "<b>Frame encapsulation</b> — header (addresses) + payload + trailer (CRC).",
        "<b>MAC addresses</b> — 48-bit, 12 hex digits, OUI + unique NIC identity.",
        "<b>ARP</b> — IPv4 → MAC resolution, cached in an ARP table.",
        "<b>Switching</b> — MAC-address-table-based forwarding/filtering; collision domains "
        "per port.",
        "<b>Layer 3 switching</b> — SVIs, routed ports, EtherChannel for inter-subnet work.",
    ],
    "definitions": [
        {"t": "Ethernet",
         "d": "One of the most widely used LAN technologies; operates in the data link and "
              "physical layers; a family defined by <b>IEEE 802.2 and 802.3</b>; supports "
              "10 / 100 / 1000 / 10,000 / 40,000 / 100,000 Mbps (100 Gbps).", "r": 2},
        {"t": "LLC", "abbr": "Logical Link Control",
         "d": "Upper data link sublayer: handles communication between upper and lower layers "
              "and takes network protocol data, adding control information to help deliver the "
              "packet to the destination.", "r": 4},
        {"t": "MAC sublayer", "abbr": "Media Access Control",
         "d": "Lower data link sublayer, implemented in hardware (NIC), with two primary "
              "responsibilities: <b>data encapsulation</b> and <b>media access control</b>.",
         "r": 4},
        {"t": "Data encapsulation (MAC)",
         "d": "Frame assembly before transmission and disassembly on reception: the MAC layer "
              "adds a header and trailer around the network layer PDU.", "r": 5},
        {"t": "Frame delimiting",
         "d": "Identifying the group of bits that make up a frame and synchronising "
              "transmitting and receiving nodes.", "r": 5},
        {"t": "CRC", "abbr": "Cyclic Redundancy Check",
         "d": "Error-detection value in each Ethernet frame's <b>trailer</b>, covering the "
              "frame contents.", "r": 5},
        {"t": "MAC address",
         "d": "A <b>48-bit</b> binary value expressed as <b>12 hexadecimal digits</b>; the "
              "physical address added to Ethernet headers so frames reach the right node.",
         "r": 9},
        {"t": "OUI", "abbr": "Organizationally Unique Identifier",
         "d": "The vendor's assigned identifier that IEEE requires as the <b>first 3 bytes</b> "
              "of every MAC address; the last 3 bytes must be unique for all addresses with "
              "that OUI.", "r": 9},
        {"t": "Runt frame (collision fragment)",
         "d": "An Ethernet frame shorter than the 64-byte minimum — dropped by the receiving "
              "device.", "r": 11},
        {"t": "Unicast / broadcast / multicast",
         "d": "Unicast = delivered to the single NIC whose MAC matches the frame's destination; "
              "broadcast = a Layer 2 broadcast to <b>all</b> devices (as ARP requests are); "
              "multicast = a special group value — MACs beginning <code>01-00-5E</code>, with "
              "IPv4 multicast addresses 224.0.0.0–239.255.255.255.",
         "r": 14},
        {"t": "ARP", "abbr": "Address Resolution Protocol",
         "d": "Provides two basic functions: <b>resolving IPv4 addresses to MAC addresses</b> "
              "and <b>maintaining a table of those mappings</b>.", "r": 17},
        {"t": "ARP table (ARP cache)",
         "d": "Mappings of IPv4 ↔ MAC learned as frames arrive (source IP and MAC recorded); "
              "entries are removed by a cache timer after unused periods, or manually with "
              "commands.", "r": 21},
        {"t": "Switch",
         "d": "Intermediary device that connects end devices, performs <b>switching and "
              "filtering based only on the MAC address</b>, builds a <b>MAC address table</b> "
              "for forwarding decisions, and depends on routers to pass data between IP "
              "subnetworks.", "r": 24},
        {"t": "Cut-through switching",
         "d": "Forwarding method with the <b>lowest level of latency</b>: the switch forwards "
              "a packet immediately after reading the address — most network errors and "
              "collisions occur in the first 64 bytes, which is what it has seen.", "r": 29},
        {"t": "SVI", "abbr": "Switch Virtual Interface",
         "d": "A logical interface on a Layer 3 switch associated with a VLAN.", "r": 33},
        {"t": "Routed port",
         "d": "A physical port on a Layer 3 switch configured to act as a router port.", "r": 33},
        {"t": "Layer 3 EtherChannel",
         "d": "A logical interface associated with a bundle of routed ports (port "
              "aggregation).", "r": 33},
        {"t": "CSMA", "abbr": "Carrier Sense Multiple Access",
         "d": "Ethernet's media-sharing method: first detect whether the media carries a "
              "signal; if none, transmit; simultaneous transmissions collide and corrupt the "
              "data.", "r": 7},
    ],
    "explanations": [
        {"t": "What the MAC sublayer actually does",
         "d": "Two jobs: <b>(1) Data encapsulation</b> — assemble frames before transmission "
              "and disassemble on reception; add header (delimiting, physical addressing) and "
              "trailer (CRC error detection) around the Layer 3 PDU. <b>(2) Media access "
              "control</b> — place frames onto media and remove them; if several devices "
              "transmit at once they collide, so Ethernet uses CSMA to control sharing.",
         "e": "The header carries source/destination MACs; the trailer's CRC lets the receiver "
              "detect corruption before accepting the frame.",
         "r": 5},
        {"t": "How a NIC decides what to do with a frame",
         "d": "Every incoming frame's destination MAC is compared with the device's physical "
              "MAC stored in the NIC's RAM. <b>No match → discard.</b> <b>Match → pass the "
              "frame up the OSI layers</b> for de-encapsulation and processing.",
         "e": "A switch-port mirror shows broadcast frames hitting every NIC, but only the "
              "intended recipient keeps one — everyone else's NIC discarded it.",
         "r": 10},
        {"t": "ARP, step by step (local network)",
         "d": "A node needs the destination MAC for an IPv4 address on its Ethernet link. It "
              "sends a <b>Layer 2 broadcast</b>; the node whose IP matches the request "
              "<b>replies</b> with its MAC. Meanwhile nodes record source IP/MAC pairs from "
              "passing frames into the ARP table. If nobody replies, the packet is dropped "
              "because a frame cannot be created.",
         "e": "PC1 pinging 192.168.1.5 for the first time broadcasts; the reply caches "
              "192.168.1.5 ↔ its MAC for all later frames.",
         "r": 19},
        {"t": "ARP when the destination is NOT local",
         "d": "If the destination IPv4 host is on the local network, frames use its MAC "
              "directly. If it is <b>not</b>, the source must send to its <b>gateway</b>: it "
              "uses ARP to learn the MAC of the <b>router interface serving as the gateway</b> "
              "(requesting it if the entry isn't already cached) and addresses frames there.",
         "e": "Reaching a server on another subnet: your PC ARPs for the default gateway's "
              "MAC, not the server's.",
         "r": 20},
        {"t": "Why switches beat hubs (collision domains)",
         "d": "The chapter's collision-domain slide contrasts one collision domain with five — "
              "each switch port isolates its own collision domain, and the summary notes that "
              "<b>replacing hubs with switches reduced the probability of frame collisions on "
              "half-duplex links</b>.",
         "e": "Five PCs on one hub share a single collision domain; on a switch each PC gets "
              "its own.",
         "r": 26},
        {"t": "Cut-through: speed over verification",
         "d": "Cut-through forwards <b>as soon as the address is read</b> — lowest latency — "
              "and relies on the observation that most errors/collisions occur in the first "
              "64 bytes. The trade-off (implied by that fact): corrupted frames later in the "
              "payload are forwarded rather than filtered.",
         "e": "Latency-sensitive fabrics prefer cut-through; error-sensitive paths may prefer "
              "full-frame checking (the other method shown in the slide figure).",
         "r": 29},
        {"t": "Physical vs logical address — the person analogy",
         "d": "The <b>MAC address</b> never changes, is assigned to the NIC ('physically'), "
              "like a person's <b>name</b>. The <b>IP address</b> depends on where the host is "
              "located, is assigned logically by an administrator, like a person's "
              "<b>address</b>. Both are required to communicate — just as both name and "
              "address are needed to send a letter.",
         "e": "Move your laptop to another network: its MAC (name) stays, its IP (address) "
              "changes.",
         "r": 15},
    ],
    "comparisons": [
        {"t": "Layer 2 switch vs router / Layer 3 switching",
         "cols": ["Aspect", "Layer 2 switch (Ethernet switch)", "Router / Layer 3 function"],
         "rows": [
             ["Decision basis", "Switching and filtering <b>based only on the MAC address</b>",
              "Passes data <b>between IP subnetworks</b> (switches depend on routers for this)"],
             ["Table used", "MAC address table built from observed MACs",
              "Routing between IP subnetworks"],
             ["Interfaces on a Layer 3 switch", "Access ports for end devices",
              "SVI (logical, per VLAN), routed port (physical, acts as router port), "
              "Layer 3 EtherChannel (bundle of routed ports)"],
             ["Chapter context", "5.3 LAN Switches", "Layer 2 versus Layer 3 Switching slide"],
         ],
         "note": "The chapter introduces Layer 3 switching with three interface types and a "
                 "configuration example for a routed port.",
         "refs": [24, 32, 33]},
        {"t": "MAC address vs IP address (physical vs logical)",
         "cols": ["Aspect", "MAC address", "IP address"],
         "rows": [
             ["Nature", "<b>Physical</b> — physically assigned to the host NIC",
              "<b>Logical</b> — assigned logically by a network administrator"],
             ["Change", "Does not change", "Based on where the host is actually located"],
             ["Analogy", "A person's <b>name</b>", "A person's <b>address</b>"],
             ["Needed for", "Frame delivery on the local Ethernet",
              "Locating the host across networks"],
         ],
         "note": "Both are required for communication — like both name and address to send a "
                 "letter. (Sizes: MAC 48-bit / IPv4 32-bit — see Chapter 3.)",
         "refs": [15]},
    ],
    "facts": [
        {"d": "Ethernet = most widely used LAN technology; standards define <b>both Layer 2 "
              "protocols and Layer 1 technologies</b> (IEEE 802.2/802.3); bandwidths up to "
              "100,000 Mbps (100 Gbps).", "r": 2},
        {"d": "MAC sublayer responsibilities: <b>data encapsulation</b> (frame assembly/"
              "disassembly, header+trailer) and <b>media access control</b> (placement/removal "
              "of frames on media).", "r": 5},
        {"d": "Header carries the <b>physical (MAC) address</b>; trailer carries a <b>CRC</b> "
              "for error detection.", "r": 5},
        {"d": "MAC address: <b>48-bit / 12 hex digits</b>; IEEE rule: <b>OUI = first 3 bytes</b> "
              "of the vendor; last 3 bytes unique per vendor.", "r": 9},
        {"d": "Example MAC notations: <code>00-05-9A-3C-78-00</code>, "
              "<code>00:05:9A:3C:78:00</code>, <code>0005.9A3C.7800</code>.", "r": 10},
        {"d": "NIC behaviour: destination MAC mismatch → <b>discard</b>; match → pass up the "
              "OSI layers for de-encapsulation.", "r": 10},
        {"d": "Ethernet II / IEEE 802.3: <b>minimum frame 64 bytes, maximum 1518 bytes</b>; "
              "&lt;64 = 'collision fragment' / runt; out-of-size frames are dropped.", "r": 11},
        {"d": "Multicast MACs begin <b>01-00-5E</b>; IPv4 multicast range "
              "<b>224.0.0.0 – 239.255.255.255</b>.", "r": 14},
        {"d": "ARP functions: <b>resolve IPv4 → MAC</b> and <b>maintain the mapping table</b>; "
              "requests are Layer 2 broadcasts; no reply → packet dropped (no frame can be "
              "created).", "r": 19},
        {"d": "Remote destination → ARP for the <b>gateway router interface's MAC</b>; ARP "
              "cache entries age out via a timer and can be removed manually.", "r": 21},
        {"d": "Switches: forward/filter on <b>MAC only</b>, build a <b>MAC address table</b>, "
              "and <b>depend on routers</b> to pass data between IP subnetworks.", "r": 24},
        {"d": "Cut-through = <b>lowest latency</b> — forwards right after reading the address; "
              "most errors/collisions occur in the <b>first 64 bytes</b>.", "r": 29},
        {"d": "Layer 3 interface types: <b>SVI</b> (logical per VLAN), <b>routed port</b> "
              "(physical, acts as router port), <b>Layer 3 EtherChannel</b> (bundle of routed "
              "ports).", "r": 33},
        {"d": "Summary: replacing hubs with switches <b>reduced collision probability on "
              "half-duplex links</b>; Ethernet uses ARP to map destinations against known "
              "network-layer addresses.", "r": 35},
    ],
    "questions": [
        {"type": "mc",
         "q": "What are the minimum and maximum Ethernet frame sizes, and what is a frame "
              "shorter than the minimum called?",
         "opts": ["64 and 1518 bytes; a runt (collision fragment)",
                  "64 and 512 bytes; a jabber",
                  "46 and 1500 bytes; a giant",
                  "128 and 1518 bytes; a fragment"],
         "a": "A — 64 and 1518 bytes; runt / collision fragment",
         "why": "Slide 11: Ethernet II and IEEE 802.3 define minimum 64 bytes, maximum 1518; "
                "under 64 is a 'collision fragment' or 'runt frame', and out-of-size frames "
                "are dropped."},
        {"type": "tf",
         "q": "IEEE requires a vendor to place its assigned OUI in the LAST three bytes of every "
              "MAC address it issues.",
         "a": "False",
         "why": "The OUI must be the <b>first 3 bytes</b>; the last 3 bytes must be unique "
                "within that OUI (slide 9)."},
        {"type": "short",
         "q": "State ARP's two basic functions.",
         "a": "1) Resolving IPv4 addresses to MAC addresses; 2) maintaining a table of those "
              "mappings.",
         "why": "Slide 17 lists exactly these two functions."},
        {"type": "mc",
         "q": "Your PC wants to send a frame to a host on a different network. Which MAC "
              "address does ARP resolve?",
         "opts": ["The MAC of the router interface serving as the gateway",
                  "The MAC of the remote host",
                  "The MAC of the DNS server",
                  "No MAC — remote hosts don't use MAC addresses"],
         "a": "A — the gateway router interface's MAC",
         "why": "Slide 20: if the destination is not on the local network, the source uses ARP "
                "to determine the MAC of the router interface serving as the gateway (or "
                "broadcasts for it if not cached)."},
        {"type": "tf",
         "q": "An Ethernet switch performs switching and filtering based only on MAC addresses "
              "and relies on routers to pass traffic between IP subnetworks.",
         "a": "True",
         "why": "Slide 24 states both points directly."},
        {"type": "short",
         "q": "Give the multicast MAC prefix and the IPv4 multicast address range.",
         "a": "MAC prefix 01-00-5E; IPv4 multicast range 224.0.0.0 to 239.255.255.255.",
         "why": "Slide 14 gives both values."},
        {"type": "explain",
         "q": "Explain what happens when a frame arrives at a NIC whose destination MAC does "
              "not match, and what happens when it does.",
         "a": "No match: the device discards the frame. Match with the device's physical MAC "
              "stored in RAM: the NIC passes the frame up the OSI layers, where "
              "de-encapsulation takes place.",
         "why": "Slide 10 walks through exactly this two-branch decision."},
        {"type": "mc",
         "q": "Which statement about cut-through switching is correct?",
         "opts": ["Lowest latency — forwards right after reading the address",
                  "Highest latency — waits for the full frame and CRC check",
                  "Filters frames by IP address",
                  "Only used on Layer 3 switch routed ports"],
         "a": "A — lowest latency, immediate forwarding after the address",
         "why": "Slide 29: 'Lowest level of latency — immediately forwards a packet after "
                "reading the address', justified by most errors/collisions occurring in the "
                "first 64 bytes."},
    ],
    "misunderstandings": [
        {"t": "MAC address vs IP address",
         "d": "MAC = <b>physical, permanent, NIC-assigned</b> (like a person's name); IP = "
              "<b>logical, location-based, administrator-assigned</b> (like a person's "
              "address). Communication needs <b>both</b> (slide 15)."},
        {"t": "A switch sends to everyone (broadcast)",
         "d": "Switches forward and filter <b>based on the MAC address table</b> (slide 24). "
              "Broadcasts happen when a protocol sends them — e.g. ARP requests — or to an "
              "unknown destination, not because switches are hubs."},
        {"t": "ARP works the same for local and remote destinations",
         "d": "Local: ARP resolves the <b>destination host's</b> MAC. Remote: frames go to the "
              "<b>gateway router interface's</b> MAC instead — a different ARP target "
              "(slide 20)."},
        {"t": "Small frames are fine",
         "d": "Anything under <b>64 bytes</b> is a runt/collision fragment and is "
              "<b>dropped</b>; over 1518 is also dropped (slide 11)."},
        {"t": "Switching happened at Layer 3",
         "d": "Basic switching/filtering is <b>MAC-only (Layer 2)</b>. Inter-subnet traffic "
              "needs routers — or a Layer 3 switch using SVIs, routed ports or EtherChannels "
              "(slides 24, 32–33)."},
    ],
    "quick": (
        "<ul>"
        "<li><b>Ethernet</b> = IEEE 802.2 (LLC) + 802.3 (MAC/physical), most used LAN tech, up "
        "to 100 Gbps; operates at data link + physical layers.</li>"
        "<li><b>MAC sublayer:</b> encapsulation (header = delimiting + MAC addressing; trailer "
        "= CRC) and media access (CSMA: sense carrier → transmit → collisions possible).</li>"
        "<li><b>Addresses:</b> 48-bit / 12 hex digits; OUI = first 3 bytes (vendor), last 3 "
        "unique. NIC: mismatch → discard; match → pass up. Notation examples: "
        "<code>00-05-9A-3C-78-00</code> / <code>0005.9A3C.7800</code>.</li>"
        "<li><b>Frames:</b> 64–1518 bytes (runt = &lt;64, dropped). Unicast (one NIC), "
        "broadcast (all — like ARP requests), multicast (01-00-5E; 224.0.0.0–239.255.255.255).</li>"
        "<li><b>ARP:</b> resolve IPv4→MAC + maintain table; L2 broadcast, matching host "
        "replies, no reply → drop; remote targets = gateway router MAC; cache times out or "
        "cleared manually.</li>"
        "<li><b>Switches:</b> MAC-table decisions, filter/forward by MAC, one collision domain "
        "per port, cut-through = lowest latency; depend on routers between subnets.</li>"
        "<li><b>Layer 3 switching:</b> SVI (logical/VLAN), routed port (physical as router), "
        "EtherChannel (bundle). MAC = physical (name), IP = logical (address) — both needed.</li>"
        "</ul>"
    ),
    "gaps": [
        "Frame <b>forwarding methods</b> (slide 28), <b>duplex / Auto-MDIX / collision-domain</b> "
        "figures (25–27), <b>memory buffering</b> (30), <b>fixed vs modular</b> (31) and "
        "<b>unicast/broadcast MAC</b> slides (12–13) are figure/title-based in the text "
        "extraction — only cut-through has descriptive text, so only it is defined above.",
        "The routed-port configuration example (slide 34) shows its commands as figures; the "
        "text names the <code>switchport</code> mode but not the full command sequence.",
    ],
}
