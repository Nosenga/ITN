# Revision kit content — Chapter 9: Subnetting IP Networks
# Grounded in uploads/Chapter 9 (Subnetting IP Networks).pdf (slide refs = page numbers).

DATA = {
    "overview": (
        "Chapter 9 is the <b>subnetting workshop</b>: why large networks are divided "
        "(broadcast control, traffic reduction, performance), what to plan first (number of "
        "subnets, number of host addresses), and the core formula — <b>2<sup>n</sup></b> usable "
        "hosts where <b>n = remaining host bits</b>, minus 2 for the subnetwork ID and "
        "broadcast address. It then shows how traditional fixed-size subnetting <b>wastes "
        "addresses</b> (WAN links need only two) and how <b>VLSM</b> divides the network into "
        "unequal parts (LANs get /27s, WAN links /30s in the worked example). Section 9.2 "
        "covers planning and documenting address allocation (no duplication, access control, "
        "monitoring; clients usually via DHCP), and 9.3 flags IPv6 design considerations."
    ),
    "objectives": [
        "Explain why large networks are segmented into subnets and what a router/interface "
        "must have for subnets to communicate "
        "(<a class=\"rev-link\" href=\"#p4\">slide 4</a>).",
        "Plan a subnet from two inputs — subnets required and host addresses required — and "
        "apply the 2<sup>n</sup> − 2 formula "
        "(<a class=\"rev-link\" href=\"#p6\">slides 5–7</a>).",
        "Explain how traditional subnetting wastes addresses and how VLSM solves it "
        "(<a class=\"rev-link\" href=\"#p8\">slides 8–10</a>).",
        "State the purposes of a documented network addressing plan and the role of DHCP for "
        "client addresses (<a class=\"rev-link\" href=\"#p12\">slide 12</a>).",
        "Recognise the IPv6 design considerations raised for larger networks "
        "(<a class=\"rev-link\" href=\"#p13\">slide 13</a>).",
    ],
    "concepts": [
        "<b>Segmentation</b> — containing broadcast traffic, reducing overall traffic, "
        "improving performance.",
        "<b>Subnet plan</b> — subnets required + host addresses required drive everything.",
        "<b>Usable hosts = 2<sup>n</sup> − 2</b> — subnetwork ID and broadcast are never "
        "assignable.",
        "<b>Traditional vs variable-length</b> — equal allocations waste space; VLSM sizes "
        "each subnet to need.",
        "<b>Address planning</b> — documented allocation prevents duplication and supports "
        "access control/monitoring.",
        "<b>Default gateways</b> — each subnet's router interface is the exit for its hosts.",
    ],
    "definitions": [
        {"t": "Subnet (subnetwork)",
         "d": "A smaller network space created by segmenting a large network into smaller "
              "groups of devices and services.", "r": 4},
        {"t": "Reasons for subnetting",
         "d": "Control traffic by <b>containing broadcast traffic within each "
              "subnetwork</b>, and <b>reduce overall network traffic to improve "
              "performance</b>.", "r": 4},
        {"t": "Default gateway (in subnets)",
         "d": "The router interface attached to a LAN; devices on that network/subnet use it "
              "to reach other networks. Each router interface needs an <b>IPv4 host address "
              "belonging to the network/subnet it is connected to</b>.", "r": 4},
        {"t": "Subnetting plan inputs",
         "d": "The two questions to answer first: <b>number of subnets required</b> and "
              "<b>number of host addresses required</b>.", "r": 6},
        {"t": "Host-bits formula",
         "d": "<b>2<sup>n</sup></b> gives the number of addresses where n = the number of "
              "<b>remaining host bits</b>; subtract <b>2</b> because the <b>subnetwork ID and "
              "broadcast address cannot be used</b> on each subnet.", "r": 6},
        {"t": "Traditional subnetting",
         "d": "Allocating the <b>same number of addresses to every subnet</b> — subnets that "
              "need fewer end up with unused (wasted) addresses; WAN links only need two.",
         "r": 8},
        {"t": "VLSM", "abbr": "Variable Length Subnet Mask",
         "d": "Also called 'subnetting a subnet' — divides a network space into <b>unequal "
              "parts</b>; the mask varies with how many bits are borrowed for each subnet; "
              "the network is first subnetted, then subnets are resubnetted — more efficient "
              "use of addresses.", "r": 9},
        {"t": "Addressing plan",
         "d": "A planned, documented allocation of network addresses — done to <b>prevent "
              "duplication of addresses, provide and control access, and monitor security and "
              "performance</b>.", "r": 12},
        {"t": "DHCP-assigned client addresses",
         "d": "Client addresses are <b>usually dynamically assigned using DHCP</b> "
              "(mechanism detailed in Chapter 10).", "r": 12},
    ],
    "explanations": [
        {"t": "Why the router and its interface address matter",
         "d": "Devices on different networks/subnets can only communicate <b>through a "
              "router</b>. Every router interface must carry an IPv4 host address in the "
              "subnet it connects to — that address <b>is</b> the default gateway for the "
              "hosts on that LAN. Subnetting without a gateway traps hosts inside their own "
              "broadcast domain.",
         "e": "Hosts on 192.168.10.0/24 use R1's G0/0 address as their gateway; R1's G0/0 must "
              "hold a valid .x host address of that same subnet.",
         "r": 4},
        {"t": "Using the formula end to end",
         "d": "Start from the plan questions: how many subnets? how many hosts per subnet? "
              "For hosts: count <b>remaining host bits n</b> → 2<sup>n</sup> total addresses → "
              "−2 usable (subnetwork ID and broadcast are reserved). Design to the "
              "<b>largest subnet's</b> maximum host count, balance subnets vs hosts there, and "
              "<b>allow growth</b> in each subnet.",
         "e": "30 hosts need 2<sup>5</sup> = 32 addresses → 30 usable → exactly /27-sized "
              "blocks (matches the VLSM example's LAN allocation).",
         "r": 7},
        {"t": "Where traditional subnetting goes wrong",
         "d": "Fixed allocation gives every subnet the same block. Big subnets get what they "
              "need; small ones don't — and <b>WAN links, which need only two addresses</b>, "
              "still receive whole equal-sized blocks. The leftovers are simply wasted.",
         "e": "Ten WAN links each handed a /24 would burn 2,540 addresses for traffic that "
              "needs 20.",
         "r": 8},
        {"t": "How VLSM fixes the waste",
         "d": "VLSM lets mask length <b>vary per subnet</b> according to borrowed bits: size "
              "large LANs bigger, tiny WAN links smaller — 'subnetting a subnet'. The worked "
              "example: <b>each LAN gets a /27</b>, <b>each WAN link a /30</b>, so LAN and WAN "
              "segments are addressed with <b>minimum waste</b>.",
         "e": "/30 = 4 addresses = exactly network, two endpoints, broadcast — no waste on a "
              "point-to-point link.",
         "r": 10},
        {"t": "Why document the addressing plan",
         "d": "Documented allocation exists to <b>prevent duplicate addresses</b>, to "
              "<b>provide and control access</b>, and to <b>monitor security and "
              "performance</b>. Client addresses are usually left to DHCP dynamically, while "
              "the plan still defines the pools.",
         "e": "A static address outside the documented plan breaks access control lists and "
              "makes incidents harder to trace.",
         "r": 12},
    ],
    "comparisons": [
        {"t": "Traditional subnetting vs VLSM",
         "cols": ["Aspect", "Traditional subnetting", "VLSM"],
         "rows": [
             ["Block sizes", "Same number of addresses for every subnet",
              "Unequal parts — mask varies with bits borrowed per subnet"],
             ["Method", "One level of subnetting", "Network first subnetted, then subnets are "
              "resubnetted"],
             ["Waste", "Subnets needing fewer addresses have unused (wasted) addresses — WAN "
              "links need only two",
              "LANs and WANs addressed with minimum waste (example: LANs /27, WAN links /30)"],
             ["Efficiency", "Lower on mixed workloads", "More efficient use of addresses"],
         ],
         "note": "VLSM is also called 'subnetting a subnet'.",
         "refs": [8, 9, 10]},
    ],
    "facts": [
        {"d": "Segment large networks to: <b>contain broadcast traffic</b> in each "
              "subnetwork and <b>reduce overall traffic / improve performance</b>.", "r": 4},
        {"d": "A router is <b>necessary</b> for devices on different networks/subnets to "
              "communicate; each interface needs a host address <b>in the connected "
              "subnet</b>; hosts use that interface as their <b>default gateway</b>.", "r": 4},
        {"d": "Plan inputs: <b>number of subnets required</b>, <b>number of host addresses "
              "required</b>.", "r": 6},
        {"d": "<b>2<sup>n</sup> − 2 usable hosts</b>, n = remaining host bits; −2 because the "
              "<b>subnetwork ID and broadcast address cannot be used</b>.", "r": 6},
        {"d": "Design rules: balance subnets/hosts for the <b>largest subnet</b>, accommodate "
              "the <b>maximum hosts</b> per subnet, <b>allow for growth</b>.", "r": 7},
        {"d": "WAN links need only <b>two addresses</b> — traditional equal allocation wastes "
              "the rest.", "r": 8},
        {"d": "VLSM: unequal division; mask depends on bits borrowed; "
              "<b>subnet, then resubnet</b>.", "r": 9},
        {"d": "VLSM example sizing: <b>LANs = /27, WAN links = /30</b> — minimum waste.",
         "r": 10},
        {"d": "Addressing-plan purposes: <b>prevent duplication</b>, <b>provide and control "
              "access</b>, <b>monitor security and performance</b>; client addresses usually "
              "<b>dynamic via DHCP</b>.", "r": 12},
    ],
    "questions": [
        {"type": "mc",
         "q": "Which two goals are given for segmenting a large network into subnets?",
         "opts": ["Contain broadcast traffic and reduce overall traffic / improve performance",
                  "Increase broadcast traffic and add more addresses",
                  "Eliminate the need for routers",
                  "Assign the same address to every device"],
         "a": "A — Contain broadcasts, reduce traffic, improve performance",
         "why": "Slide 4: create smaller groups 'to control traffic by containing broadcast "
                "traffic within each subnetwork' and 'reduce overall network traffic and "
                "improve network performance'."},
        {"type": "short",
         "q": "Write the usable-host formula from the chapter and explain both parts.",
         "a": "Usable hosts = 2<sup>n</sup> − 2, where n is the number of remaining host bits. "
              "2<sup>n</sup> counts all addresses in the block; 2 is subtracted because the "
              "subnetwork ID and the broadcast address cannot be assigned to hosts.",
         "why": "Slide 6 gives the formula and the reason for the minus 2 verbatim."},
        {"type": "tf",
         "q": "In traditional subnetting, every subnet receives the same number of addresses, "
              "so a WAN link that needs only two addresses may waste the rest of its block.",
         "a": "True",
         "why": "Slide 8: traditional subnetting 'uses the same number of addresses' for each "
                "subnet; 'WAN links only need two addresses', leaving unused (wasted) "
                "addresses."},
        {"type": "mc",
         "q": "In the VLSM example, what mask sizes are assigned?",
         "opts": ["/27 for LANs and /30 for WAN links", "/24 for LANs and /24 for WANs",
                  "/30 for LANs and /27 for WANs", "/28 for every link"],
         "a": "A — /27 for LANs, /30 for WAN links",
         "why": "Slide 10: 'Each LAN will be assigned a subnet with /27 mask. Each WAN link "
                "will be assigned a subnet with /30 mask.'"},
        {"type": "short",
         "q": "What two numbers must your subnetting plan establish first?",
         "a": "The number of subnets required, and the number of host addresses required.",
         "why": "Slide 6 'Subnetting Based on Host Requirements' lists exactly these two."},
        {"type": "explain",
         "q": "Why must each router interface hold an IPv4 host address belonging to the "
              "subnet it connects to, and what do hosts on that subnet use it for?",
         "a": "Devices on different networks/subnets can only communicate via a router. An "
              "interface's address must belong to its own subnet so it can act as an endpoint "
              "there; hosts on that LAN use the interface's address as their <b>default "
              "gateway</b> to leave the subnet.",
         "why": "Slide 4 states both requirements — interface host address in the connected "
                "subnet, and devices using that interface as default gateway."},
        {"type": "short",
         "q": "Give three reasons for planning and documenting network address allocation.",
         "a": "Preventing duplication of addresses; providing and controlling access; "
              "monitoring security and performance.",
         "why": "Slide 12 lists these three purposes."},
    ],
    "misunderstandings": [
        {"t": "Usable hosts = 2<sup>n</sup>",
         "d": "Every subnet also has a <b>subnetwork ID and a broadcast address</b> — both "
              "unassignable — so usable = 2<sup>n</sup> − 2 (slide 6)."},
        {"t": "WAN links need 'a real subnet' like LANs",
         "d": "A point-to-point WAN needs only <b>two</b> addresses; giving it an equal-sized "
              "block is exactly the waste traditional subnetting creates (slide 8) — VLSM's "
              "/30 fixes it (slide 10)."},
        {"t": "VLSM is just subnetting twice",
         "d": "It is planned <b>unequal</b> division: the mask varies with borrowed bits per "
              "subnet, first subnetting then resubnetting, to minimise waste (slide 9)."},
        {"t": "Subnetting is only about security",
         "d": "The chapter's stated first goals are <b>containing broadcast traffic and "
              "reducing traffic for performance</b> (slide 4); security/access control comes "
              "via the addressing plan (slide 12)."},
    ],
    "quick": (
        "<ul>"
        "<li><b>Why subnet:</b> contain broadcasts per subnetwork; cut overall traffic; "
        "improve performance. Routers connect subnets; each router interface = a host address "
        "in its subnet = the LAN's default gateway.</li>"
        "<li><b>Plan:</b> how many subnets? how many hosts? Design for the largest subnet's "
        "max hosts and allow growth.</li>"
        "<li><b>Formula:</b> 2<sup>n</sup> − 2 usable hosts (n = remaining host bits; −2 = "
        "subnetwork ID + broadcast are reserved).</li>"
        "<li><b>Traditional wastes:</b> equal blocks for everyone; WAN links need only two "
        "addresses.</li>"
        "<li><b>VLSM:</b> unequal parts, mask varies with borrowed bits, subnet-then-resubnet; "
        "example: LANs /27, WANs /30 → minimum waste.</li>"
        "<li><b>Plan document:</b> prevents duplicate addresses, enables access control, "
        "supports security/performance monitoring; clients usually get addresses via DHCP.</li>"
        "</ul>"
    ),
    "gaps": [
        "The <b>IPv6 Design Considerations</b> slide (13), <b>The Plan</b> slide (5) and the "
        "<b>Chapter 9 Summary</b> slides (14–15) contain title-only text in the source "
        "extraction — IPv6 design specifics are not present in the material beyond the section "
        "heading, so nothing is asserted about them here.",
        "This chapter is short (15 slides); its knowledge-check questions are drawn from the "
        "formula, VLSM and planning slides. For more subnetting drill with instant checking, "
        "use the site's <a href=\"lab.html\">IPv4 Lab</a> (generated practice on exactly these "
        "skills).",
    ],
}
