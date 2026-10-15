# Revision kit content — Chapter 6: Network Layer
# Grounded in uploads/Chapter 6 ITN (Network Layer).pdf (slide refs = page numbers).

DATA = {
    "overview": (
        "Chapter 6 explains <b>OSI Layer 3</b> end to end. It starts with the network layer's "
        "four basic processes — <b>addressing, encapsulation, routing, de-encapsulation</b> — "
        "and the characteristics of IP (connectionless, best effort, media independent), then "
        "contrasts <b>IPv4's limitations</b> with <b>IPv6</b> (address space, packet handling, "
        "no NAT, integrated security). Section 6.2 covers <b>routing decisions</b>: host and "
        "router routing tables, default gateways, and how to read <code>show ip route</code> "
        "entries (codes, administrative distance, metrics, next hops). Section 6.3 tours the "
        "router as a computer — RAM, ROM, NVRAM, flash, interfaces, bootset, "
        "<code>show version</code>. Section 6.4 configures a router: mode navigation, "
        "passwords/banners, LAN interfaces, verification with "
        "<code>show ip interface brief</code> and <code>ping</code>, and host default "
        "gateways."
    ),
    "objectives": [
        "Describe the four basic processes of the network layer and its role as OSI Layer 3 "
        "(<a class=\"rev-link\" href=\"#p2\">slides 2–6</a>).",
        "Explain IPv4's limitations and the improvements IPv6 brings "
        "(<a class=\"rev-link\" href=\"#p7\">slides 7–9</a>).",
        "Explain host and router forwarding decisions, default gateways and routing-table "
        "structures (<a class=\"rev-link\" href=\"#p11\">slides 11–16</a>).",
        "Identify router hardware and memory components and what each stores "
        "(<a class=\"rev-link\" href=\"#p18\">slides 18–26</a>).",
        "Configure and verify router interfaces and host/switch default gateways "
        "(<a class=\"rev-link\" href=\"#p28\">slides 28–32</a>).",
    ],
    "concepts": [
        "<b>Four network-layer processes</b> — addressing, encapsulation, routing, "
        "de-encapsulation.",
        "<b>IP characteristics</b> — connectionless, best effort, media independent.",
        "<b>Routing tables</b> — connected (C/L) vs learned remote routes (S, R, D, O…).",
        "<b>Default gateway</b> — the exit path for traffic beyond the local network.",
        "<b>Router memory model</b> — RAM / ROM / NVRAM / flash and their files.",
        "<b>IPv4 vs IPv6</b> — depletion, NAT and header issues vs 2¹²⁸ addresses, "
        "simplified header, integrated security.",
    ],
    "definitions": [
        {"t": "Network layer (Layer 3)",
         "d": "Provides services that allow end devices to exchange data across the network "
              "using four basic processes: <b>addressing end devices, encapsulation, routing, "
              "de-encapsulating</b>.", "r": 2},
        {"t": "Routing",
         "d": "The network-layer process of choosing the path for packets toward their "
              "destination network — the core of a router's job.", "r": 2},
        {"t": "Default gateway",
         "d": "The router interface a host sends to when the destination is <b>not</b> on the "
              "local network; hosts keep a local routing table (direct connection, local "
              "network route, local default route — e.g. "
              "<code>ip route 0.0.0.0 0.0.0.0 s2/0</code>).", "r": 12},
        {"t": "Routing table",
         "d": "The router's list of known destinations: how each network was learned, the "
              "destination network, the interface/next hop used to reach it "
              "(<code>show ip route</code>).", "r": 14},
        {"t": "C / L entries",
         "abbr": "connected / local",
         "d": "<code>C</code> = the destination network is <b>directly connected</b> on a named "
              "interface; <code>L</code> = the router's own <b>local</b> interface address "
              "(shown as a /32 host route).", "r": 15},
        {"t": "Administrative distance",
         "d": "The <b>trustworthiness of the route source</b> — the first number in brackets, "
              "e.g. <code>[90/2170112]</code> → AD 90 (EIGRP).", "r": 16},
        {"t": "Metric",
         "d": "The <b>cost to reach the remote network</b> — the second bracketed number "
              "(here 2170112).", "r": 16},
        {"t": "Next hop",
         "d": "The IP address of the next router on the path "
              "(<code>via 209.165.200.226</code>) to reach a remote network.", "r": 16},
        {"t": "RAM",
         "d": "Volatile memory holding the <b>running IOS, running configuration file, IP "
              "routing and ARP tables, packet buffer</b>.", "r": 20},
        {"t": "ROM",
         "d": "Non-volatile memory holding <b>bootup instructions, basic diagnostic software "
              "and a limited IOS</b>.", "r": 20},
        {"t": "NVRAM",
         "d": "Non-volatile storage of the <b>startup configuration file</b>.", "r": 20},
        {"t": "Flash",
         "d": "Non-volatile storage of the <b>IOS</b> and other system files.", "r": 20},
        {"t": "IPv4",
         "abbr": "Internet Protocol version 4",
         "d": "The network-layer protocol the Internet is still largely based on; an IPv4 "
              "packet contains the <b>IP header and the payload</b>; 32-bit dotted-decimal "
              "addresses (~4 billion).", "r": 33},
        {"t": "IPv6", "abbr": "Internet Protocol version 6",
         "d": "Successor protocol with 128-bit addresses — <b>8 groups of four hex characters "
              "separated by colons</b> (2¹²⁸ ≈ 340 undecillion addresses).", "r": 9},
        {"t": "NAT", "abbr": "Network Address Translation",
         "d": "Referenced by the chapter as part of IPv4's 'lack of end-to-end connectivity'; "
              "IPv6 <b>eliminates the need for NAT</b>.", "r": 7},
        {"t": "ICMP",
         "abbr": "Internet Control Message Protocol",
         "d": "The protocol behind <code>ping</code> — the chapter's verification traffic "
              "('Sending 5, 100-byte ICMP Echos … Success rate is 100 percent').", "r": 30},
    ],
    "explanations": [
        {"t": "The four processes working together",
         "d": "To move data end-to-end the network layer: (1) <b>addresses</b> end devices "
              "with IP addresses, (2) <b>encapsulates</b> the payload into packets with IP "
              "headers, (3) <b>routes</b> packets hop by hop toward the destination network, "
              "and at the destination (4) <b>de-encapsulates</b> so upper layers see the "
              "original data.",
         "e": "A web request from your PC to a server across the Internet exercises all four "
              "on every router it crosses.",
         "r": 2},
        {"t": "Reading a remote routing-table entry",
         "d": "<code>D 10.1.1.0/24 [90/2170112] via 209.165.200.226, 00:00:05, "
              "Serial0/0/0</code> — piece by piece: <b>D</b> = how it was learned (EIGRP); "
              "<b>10.1.1.0/24</b> = destination network; <b>90</b> = administrative distance "
              "(trustworthiness); <b>2170112</b> = metric (cost); <b>via 209.165.200.226</b> "
              "= next-hop IP; <b>00:00:05</b> = time since discovery; <b>Serial0/0/0</b> = "
              "outgoing interface.",
         "e": "If two sources advertise the same network, the lower administrative distance "
              "is more trusted and wins.",
         "r": 16},
        {"t": "Connected vs remote entries",
         "d": "Connected entries come from configuring an interface with an address: "
              "<code>C</code> identifies the destination network and its interface; "
              "<code>L</code> is the router's own address on that interface (/32). Remote "
              "entries are learned via a routing protocol or static configuration and carry "
              "next-hop, AD, metric, elapsed time and outgoing interface.",
         "e": "<code>C 192.168.10.0/24 is directly connected, GigabitEthernet0/0</code> + "
              "<code>L 192.168.10.1/32</code> appear as soon as you configure G0/0 with "
              ".1/24 and bring it up.",
         "r": 15},
        {"t": "Router memory — what lives where",
         "d": "<b>RAM</b> (volatile): running IOS + running config + routing/ARP tables + "
              "packet buffer. <b>NVRAM</b>: startup config (loaded at boot). <b>Flash</b>: the "
              "IOS image and system files. <b>ROM</b>: bootup instructions, diagnostics, "
              "limited IOS. This is why <code>copy running-config startup-config</code> "
              "matters: it copies RAM's active config into NVRAM so it survives power-off.",
         "e": "Power cycle → RAM cleared → router boots IOS from flash, loads startup-config "
              "from NVRAM.",
         "r": 20},
        {"t": "When a host needs a default gateway",
         "d": "A host always keeps a local routing table (direct connection, local network "
              "route, local default route). Traffic to a device <b>on the same network</b> "
              "needs no gateway; traffic to <b>another network</b> must go to the default "
              "gateway's interface. The chapter's two diagrams label exactly these cases: "
              "'Default Gateway not needed' vs 'Default Gateway needed'.",
         "e": "PC1 talking to PC2 in 192.168.10.0/24: direct. PC1 reaching 192.168.11.0/24: "
              "via R1's .1 interface.",
         "r": 31},
        {"t": "IPv4's three limitations → IPv6's answers",
         "d": "IPv4 faces <b>address depletion</b>, <b>routing table expansion</b> and "
              "<b>lack of end-to-end connectivity (NAT)</b>. IPv6 answers with <b>increased "
              "address space</b> (4 billion → 340 undecillion), <b>improved packet handling</b>, "
              "<b>eliminating the need for NAT</b>, and <b>integrated security</b>; its "
              "simplified header adds routing efficiency, simplified extension headers and "
              "per-flow processing.",
         "e": "2¹²⁸ addresses ≈ 'many trillions for every human on the planet' — the chapter's "
              "own phrasing.",
         "r": 8},
    ],
    "comparisons": [
        {"t": "IPv4 vs IPv6",
         "cols": ["Aspect", "IPv4", "IPv6"],
         "rows": [
             ["Address size", "32-bit (~4,000,000,000 addresses)",
              "128-bit — 8 groups of four hex chars separated by colons; 2¹²⁸ ≈ 340 undecillion"],
             ["Status", "Still the most widely used network-layer protocol; Internet largely "
              "based on it", "Successor with vastly increased address space"],
             ["NAT", "Lack of end-to-end connectivity → NAT needed",
              "Eliminates the need for NAT"],
             ["Packet handling", "Standard header (IP header + payload)",
              "Simplified header: better routing efficiency, simplified extension headers, "
              "per-flow processing"],
             ["Security", "Not integrated in the protocol itself",
              "Integrated security"],
             ["Address example", "<code>192.168.10.2</code> (dotted decimal)",
              "<code>DB52:AA12:5478:001A:EE45:AA25:BB12:FF12</code>"],
         ],
         "note": "IPv4's limitations as listed: address depletion, routing table expansion, "
                 "lack of end-to-end connectivity (NAT).",
         "refs": [7, 8, 9, 33]},
    ],
    "facts": [
        {"d": "Network layer = <b>OSI Layer 3</b>; four processes: <b>addressing, "
              "encapsulation, routing, de-encapsulation</b>.", "r": 2},
        {"d": "IP characteristics: <b>connectionless</b>, <b>best effort delivery</b>, "
              "<b>media independent</b>.", "r": 6},
        {"d": "Legacy network-layer protocols mentioned: IPX, AppleTalk, CLNS/DECNet — IPv4 "
              "and IPv6 are today's protocols.", "r": 3},
        {"d": "IPv4 limitations: <b>address depletion, routing-table expansion, lack of "
              "end-to-end connectivity (NAT)</b>.", "r": 7},
        {"d": "IPv6 benefits: <b>increased address space, improved packet handling, no NAT "
              "needed, integrated security</b>; 4 billion vs 340 undecillion addresses.",
         "r": 8},
        {"d": "Host local routing table contents: <b>direct connection, local network route, "
              "local default route</b> (example: "
              "<code>ip route 0.0.0.0 0.0.0.0 s2/0</code>).", "r": 12},
        {"d": "<code>show ip route</code> codes: <b>L</b> local, <b>C</b> connected, <b>S</b> "
              "static, <b>R</b> RIP, <b>O</b> OSPF, <b>D</b> EIGRP, <b>*</b> candidate "
              "default…", "r": 14},
        {"d": "Remote-entry fields: learned-by source, destination network, <b>administrative "
              "distance (trustworthiness), metric, next-hop IP, elapsed time, outgoing "
              "interface</b>.", "r": 16},
        {"d": "Memory: <b>RAM</b> = running IOS/config, routing &amp; ARP tables, buffers; "
              "<b>NVRAM</b> = startup config; <b>flash</b> = IOS; <b>ROM</b> = bootup "
              "instructions, diagnostics, limited IOS.", "r": 20},
        {"d": "<code>show version</code> shows IOS version (e.g. 15.2(4)M1), uptime, last "
              "reload reason, interfaces, memory sizes and the configuration register.",
         "r": 26},
        {"d": "Basic configuration flow: <code>enable</code> → <code>configure terminal</code> "
              "→ <code>hostname</code> → <code>enable secret</code> → <code>line console 0</code> "
              "/ <code>line vty 0 4</code> with password + login → <code>service "
              "password-encryption</code> → <code>banner motd</code> → <code>copy running-config "
              "startup-config</code>.", "r": 28},
        {"d": "Interface configuration: <code>interface gigabitethernet 0/0</code> → "
              "<code>ip address 192.168.10.1 255.255.255.0</code> → <code>description</code> → "
              "<code>no shutdown</code> (state changes to up).", "r": 29},
        {"d": "Verification: <code>show ip interface brief</code> (status/protocol, addresses) "
              "and <code>ping</code> — 'Sending 5, 100-byte ICMP Echos … Success rate is 100 "
              "percent (5/5)'.", "r": 30},
        {"d": "An IPv4 packet = <b>IP header + payload</b>; the IPv6 simplified header offers "
              "routing efficiency, simplified extension headers, per-flow processing.",
         "r": 33},
    ],
    "questions": [
        {"type": "mc",
         "q": "Which set lists the four basic processes of the network layer?",
         "opts": ["Addressing, encapsulation, routing, de-encapsulation",
                  "Encoding, framing, switching, forwarding",
                  "Authentication, authorization, accounting, auditing",
                  "ARP, DNS, DHCP, ICMP"],
         "a": "A — Addressing, encapsulation, routing, de-encapsulation",
         "why": "Slide 2 (and the summary) names exactly these four processes for OSI "
                "Layer 3."},
        {"type": "tf",
         "q": "IP is described as connectionless and providing best effort delivery.",
         "a": "True",
         "why": "Slides 4–5 are titled 'IP – Connectionless' and 'Best Effort Delivery' — "
                "characteristics of the IP protocol."},
        {"type": "mc",
         "q": "In the entry <code>D 10.1.1.0/24 [90/2170112] via 209.165.200.226</code>, what "
              "does 90 represent?",
         "opts": ["The administrative distance (trustworthiness of the route source)",
                  "The metric to reach the network",
                  "The interface number",
                  "The number of hops"],
         "a": "A — administrative distance",
         "why": "Slide 16: the first bracketed number identifies the administrative distance "
                "(trustworthiness); the second (2170112) is the metric."},
        {"type": "short",
         "q": "Name the three limitations of IPv4 listed in the chapter.",
         "a": "Address depletion; Internet routing-table expansion; lack of end-to-end "
              "connectivity (NAT).",
         "why": "Slide 7 'Limitations of IPv4' lists exactly these three."},
        {"type": "short",
         "q": "Which memory types hold (a) the running configuration, (b) the startup "
              "configuration, and (c) the IOS image?",
         "a": "(a) RAM, (b) NVRAM, (c) flash.",
         "why": "Slide 20's memory table: RAM = running config (plus IOS/tables/buffers); "
                "NVRAM = startup configuration; flash = IOS and other system files."},
        {"type": "mc",
         "q": "After configuring an interface, which command pair correctly assigns an address "
              "and brings the interface up?",
         "opts": ["<code>ip address 192.168.10.1 255.255.255.0</code> then "
                  "<code>no shutdown</code>",
                  "<code>ip address 192.168.10.1/24</code> then <code>startup</code>",
                  "<code>address 192.168.10.1</code> then <code>up</code>",
                  "<code>ip address 192.168.10.1 255.255.255.0</code> then <code>reload</code>"],
         "a": "A — ip address … then no shutdown",
         "why": "Slide 29 shows exactly this sequence inside "
                "<code>interface gigabitethernet 0/0</code>, with '%LINK-5-CHANGED … state to "
                "up' messages following <code>no shutdown</code>."},
        {"type": "explain",
         "q": "A PC and a switch both sit on 192.168.10.0/24 with the router at .1. When is a "
              "default gateway needed, and what is configured on the switch versus the host?",
         "a": "Traffic to another network (e.g. 192.168.11.0/24) needs a default gateway — "
              "the host's local table carries a local default route to the router's "
              "interface. Traffic within the same network needs none. The host is given the "
              "gateway via its IP configuration; a switch that must be managed from other "
              "networks also needs a default gateway configured (the chapter shows both "
              "cases as separate slides).",
         "why": "Slides 12 and 31–32: hosts maintain a local routing table with a local "
                "default route; the diagrams contrast 'Default Gateway not needed' vs 'needed' "
                "and there is a dedicated 'Default Gateway on a Switch' slide."},
        {"type": "short",
         "q": "Which two verification commands appear in the chapter, and what does each show?",
         "a": "<code>show ip interface brief</code> — addresses, status and protocol of every "
              "interface; <code>ping</code> — ICMP reachability (example: 5/5, 100 percent).",
         "why": "Slide 30 shows both outputs verbatim."},
    ],
    "misunderstandings": [
        {"t": "A default gateway is always required",
         "d": "Only for traffic <b>leaving the local network</b>. The chapter's diagrams show "
              "'Default Gateway not needed' for same-network communication (slide 31)."},
        {"t": "<code>C</code> and <code>L</code> are the same",
         "d": "<code>C</code> is the <b>connected destination network</b> "
              "(<code>192.168.10.0/24</code>); <code>L</code> is the router's <b>own local "
              "address</b> on that interface (<code>192.168.10.1/32</code>) — both appear when "
              "you configure the interface (slide 15)."},
        {"t": "Switches and routers use the same tables",
         "d": "Routers make network-layer forwarding decisions from a <b>routing table</b> "
              "(connected + learned routes with next hops and metrics); switches forward on "
              "MAC tables (Chapter 5) and depend on routers between subnetworks."},
        {"t": "Best effort = no design behind delivery",
         "d": "The chapter presents connectionless, best-effort, media-independent IP as "
              "<b>characteristics</b> of the protocol (slides 4–6); reliability functions live "
              "in upper layers (see Chapter 7), while IPv6 still improves packet handling "
              "with its simplified header (slide 33)."},
    ],
    "quick": (
        "<ul>"
        "<li><b>Layer 3 four processes:</b> address end devices → encapsulate into packets → "
        "route → de-encapsulate. IP = connectionless, best effort, media independent.</li>"
        "<li><b>IPv4 limits:</b> address depletion, routing-table growth, NAT/end-to-end "
        "problems. <b>IPv6 answers:</b> 128-bit (8 colon groups; 340 undecillion), improved "
        "packet handling, no NAT, integrated security; simplified header → routing efficiency, "
        "extension headers, per-flow processing.</li>"
        "<li><b>Host tables:</b> direct connection, local network route, local default route "
        "— gateway needed only off-subnet.</li>"
        "<li><b>Reading <code>show ip route</code>:</b> code (C/L/S/R/D/O, * = candidate "
        "default) + destination + [AD/metric] + via (next hop) + time + outgoing interface; "
        "C = connected network, L = own local address.</li>"
        "<li><b>Router anatomy:</b> it's a computer — RAM (running IOS/config, routing &amp; "
        "ARP tables, buffers), NVRAM (startup config), flash (IOS), ROM (boot/diagnostics); "
        "<code>show version</code> reports versions, memory, interfaces, config register.</li>"
        "<li><b>Configure:</b> enable → conf t → hostname → enable secret → line console/vty "
        "passwords → service password-encryption → banner motd → save (<code>copy running-config "
        "startup-config</code>); interface: ip address + description + no shutdown; verify with "
        "<code>show ip interface brief</code> and <code>ping</code>.</li>"
        "</ul>"
    ),
    "gaps": [
        "<b>Private vs public IP addresses</b> (a comparison you may expect here) is <b>not "
        "covered anywhere in this chapter's source material</b> — and a full-corpus search "
        "finds no slide that contrasts them — so no comparison is presented rather than "
        "fabricating one. RFC 1918 private addressing would need additional source material.",
        "The <b>host and router forwarding-decision</b> slides (11, 13), <b>bootset/boot-up</b> "
        "(25), <b>LAN/WAN interface</b> details (23–24), <b>default gateway on a switch</b> "
        "(32) and part of the router-configuration walkthrough are figure/output-based — the "
        "text above quotes only commands and outputs actually present in the extraction.",
        "IP connectionless/best-effort/media-independent characteristics are named by slide "
        "titles (4–6) without further body text — deep behaviour is not expanded in this "
        "deck's extractable text.",
    ],
}
