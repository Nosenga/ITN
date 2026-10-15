# Revision kit content — Chapter 1: Exploring the Network
# Grounded in uploads/Chapter 1_ITN_Exploring the Network.pdf (slide refs = page numbers).

DATA = {
    "overview": (
        "Chapter 1 sets the scene for the whole course: what networks are, why they matter in "
        "daily life, and what a network is actually made of. It moves from networks of many "
        "sizes (personal to Internet-scale) through the building blocks — end devices, "
        "intermediary devices, media and services — to the two main network types (LAN and WAN) "
        "and the Internet. It then treats the network as a platform that must be <b>fault "
        "tolerant, scalable, secure</b> and able to provide <b>Quality of Service</b>, and closes "
        "with home networking trends plus the chapter's security threats and solutions."
    ),
    "objectives": [
        "Explain how networks support the way we learn, communicate, work and play "
        "(<a class=\"rev-link\" href=\"#p4\">slide 4</a>).",
        "Identify the three categories of network components — devices, media and services — "
        "and give examples of end devices and intermediary devices "
        "(<a class=\"rev-link\" href=\"#p9\">slides 9–12</a>).",
        "Distinguish LANs, WANs and the Internet, and describe how remote users and businesses "
        "connect to the Internet (<a class=\"rev-link\" href=\"#p15\">slides 15–22</a>).",
        "Describe the four characteristics of modern network architectures: fault tolerance, "
        "scalability, QoS and security (<a class=\"rev-link\" href=\"#p25\">slide 25</a>).",
        "List common external security threats and the security components used against them "
        "(<a class=\"rev-link\" href=\"#p39\">slides 39–40</a>).",
    ],
    "concepts": [
        "<b>Network components</b> — devices, media and services (three categories).",
        "<b>LAN vs WAN</b> — the two most common network infrastructures.",
        "<b>Converged networks</b> — one network carrying voice, video and data.",
        "<b>Fault tolerance &amp; packet switching</b> — redundancy and alternative routes keep "
        "traffic flowing.",
        "<b>QoS</b> — matching packet priority to the type of communication.",
        "<b>Network vs information security</b> — protecting devices, and protecting the data "
        "they carry.",
    ],
    "definitions": [
        {"t": "LAN", "abbr": "Local Area Network",
         "d": "Interconnects end devices in a limited area (home, school, office building or "
              "campus), is usually administered by a single organization, and provides "
              "high-speed bandwidth to its devices.",
         "r": 17},
        {"t": "WAN", "abbr": "Wide Area Network",
         "d": "Interconnects LANs over wide geographical areas (between cities, countries or "
              "continents), is usually administered by multiple service providers, and "
              "typically provides slower-speed links between LANs.",
         "r": 18},
        {"t": "Internet",
         "d": "A conglomerate — a 'network of networks' — not owned by any individual or group; "
              "communication across it relies on common standards from organizations such as "
              "the IETF, ICANN and IAB.",
         "r": 19},
        {"t": "IETF", "abbr": "Internet Engineering Task Force",
         "d": "One of the standards organizations that develop the open technologies and "
              "standards enabling communication across the Internet.", "r": 19},
        {"t": "ICANN", "abbr": "Internet Corporation for Assigned Names and Numbers",
         "d": "Standards/governance organization named in the chapter as part of keeping the "
              "Internet's naming and addressing consistent.", "r": 19},
        {"t": "End device (host)",
         "d": "A source or destination of messages on the network — computers, printers, VoIP "
              "phones, cameras, mobile devices. Each host is identified by an address so other "
              "hosts can specify it as a destination.", "r": 10},
        {"t": "Intermediary device",
         "d": "Connects end devices to the network or links networks: network access devices "
              "(switches, wireless access points), internetworking devices (routers) and "
              "security devices (firewalls).", "r": 11},
        {"t": "QoS", "abbr": "Quality of Service",
         "d": "Mechanisms that give time-sensitive or business-critical communication higher "
              "priority (and undesired traffic lower priority or none), so packet handling "
              "matches the type of communication.", "r": 29},
        {"t": "Fault tolerance",
         "d": "The ability to keep traffic flowing when components fail, achieved with redundant "
              "links and alternative routes.", "r": 25},
        {"t": "Scalability",
         "d": "A network design that can add more users and devices without performance "
              "degrading.", "r": 25},
        {"t": "Converged network",
         "d": "A single network infrastructure carrying voice, video and data together "
              "instead of separate purpose-built networks.", "r": 24},
        {"t": "DoS", "abbr": "Denial of Service attack",
         "d": "Listed among the most common external threats to networks; an attack that "
              "disrupts service rather than stealing data.", "r": 39},
        {"t": "ACL", "abbr": "Access Control List",
         "d": "Listed as a network-security component used to filter traffic as part of "
              "security solutions.", "r": 40},
        {"t": "VPN", "abbr": "Virtual Private Network",
         "d": "Listed among security components as providing secure access to remote users.",
         "r": 40},
        {"t": "IPS", "abbr": "Intrusion Prevention System",
         "d": "A security component named in the chapter's security-solutions slide.",
         "r": 40},
    ],
    "explanations": [
        {"t": "Client, server — or both?",
         "d": "A device's role is decided by its <b>software</b>, not by the hardware. The same "
              "computer can request web pages (client behaviour) and store/deliver e-mail "
              "(server behaviour). In peer-to-peer models, devices act as both at the same time.",
         "e": "A laptop with a web browser is a client when it requests a page; the machine "
              "holding the website is the server for that request.",
         "r": 6},
        {"t": "Why packet switching beat circuit switching for reliability",
         "d": "In a circuit-switched network a dedicated path is reserved; if a link on that "
              "path fails, the call drops. Packet-switched networks cut messages into packets "
              "that can take <b>any available route</b>, so redundancy gives alternative paths "
              "— this is what makes networks fault tolerant.",
         "e": "A failed link only costs the packets in flight; the rest reroute instead of the "
              "whole session dying.",
         "r": 27},
        {"t": "QoS is prioritising, not adding capacity",
         "d": "QoS does not create bandwidth — it decides <b>which traffic gets served first</b>. "
              "Telephony and video are time-sensitive and get priority; e-mail and web "
              "retrieval can wait; peer-to-peer file sharing may be dropped entirely.",
         "e": "During a video conference, the router treats voice packets ahead of a background "
              "software update.",
         "r": 29},
        {"t": "Two security concerns, three primary requirements",
         "d": "The chapter splits security into <b>network infrastructure security</b> "
              "(physically secure devices and their management software) and <b>information "
              "security</b> (protecting data in packets and at rest). To achieve security it "
              "lists three requirements: <b>confidentiality</b> (only authorized recipients read "
              "the data — passwords and encryption), <b>integrity</b> (data not altered in "
              "transit), and <b>availability</b> (timely, reliable access for authorized users).",
         "e": "Firewalls and antivirus support availability/integrity; encryption and passwords "
              "support confidentiality.",
         "r": 33},
        {"t": "Networks of many sizes",
         "d": "The chapter scales the picture from a simple two-computer network up to the "
              "Internet — the largest network, described as a 'network of networks'. The same "
              "components and standards work at every size.",
         "e": "A home Wi-Fi LAN and the global Internet use the same end-device / intermediary "
              "device / media structure.",
         "r": 5},
    ],
    "comparisons": [
        {"t": "LAN vs WAN",
         "cols": ["Aspect", "LAN", "WAN"],
         "rows": [
             ["Geography", "Limited area: home, school, office, campus",
              "Wide areas: cities, countries, continents"],
             ["Administration", "Usually a single organization or individual",
              "Usually multiple service providers"],
             ["Link speed", "High-speed bandwidth to internal devices",
              "Typically slower-speed links between LANs"],
             ["Role", "Connects end devices", "Interconnects LANs"],
         ],
         "note": "Both are 'the two most common types of network infrastructures'. "
                 "Other types named in the chapter: MAN, WLAN, SAN.",
         "refs": [15, 17, 18]},
        {"t": "Circuit-switched vs packet-switched networks",
         "cols": ["Aspect", "Circuit-switched", "Packet-switched"],
         "rows": [
             ["Path", "Dedicated path reserved for the session",
              "Messages split into packets taking any available route"],
             ["Fault tolerance", "A failed path breaks the session",
              "Redundancy allows alternative routes"],
             ["Used in the chapter", "Contrast case for reliability",
              "The basis of reliable modern networks"],
         ],
         "note": "Introduced while explaining fault tolerance.",
         "refs": [26, 27]},
    ],
    "facts": [
        {"d": "There are <b>three categories</b> of network components: <b>devices, media, "
              "services</b>.", "r": 9},
        {"d": "Every host on a network is <b>identified by an address</b>; a host that "
              "initiates communication uses the <b>destination host's address</b>.",
         "r": 10},
        {"d": "Intermediary devices: <b>switches and wireless access points</b> (network access), "
              "<b>routers</b> (internetworking), <b>firewalls</b> (security).", "r": 11},
        {"d": "Network media carry signals as <b>electrical impulses, light impulses or "
              "electromagnetic waves</b>.", "r": 12},
        {"d": "A topology diagram shows the <b>physical location of intermediary devices, "
              "configured ports and cable installation</b>, and identifies devices, ports and "
              "the IP addressing scheme.", "r": 14},
        {"d": "Four architecture characteristics: <b>fault tolerance, scalability, QoS, "
              "security</b>.", "r": 25},
        {"d": "Security has two concerns: <b>network infrastructure security</b> and "
              "<b>information security</b>; three primary requirements: <b>confidentiality, "
              "integrity, availability</b>.", "r": 33},
        {"d": "Common external threats: viruses, worms, Trojan horses; spyware/adware; "
              "zero-day attacks; hacker attacks; DoS attacks; data interception and theft; "
              "identity theft.", "r": 39},
        {"d": "Security solutions: antivirus/antispyware, firewall filtering, dedicated firewall "
              "systems, ACLs, IPS, VPNs.", "r": 40},
        {"d": "Home connection technologies named: <b>powerline networking</b>, <b>wireless "
              "broadband</b> (WISP dish/antenna; cellular-style fixed wireless), alongside DSL "
              "and cable.", "r": 36},
        {"d": "The routing and switching platform is described as <b>the foundation of any "
              "network infrastructure</b>.", "r": 42},
    ],
    "questions": [
        {"type": "mc",
         "q": "According to the chapter, how many categories of network components are there, "
              "and what are they?",
         "opts": ["Two: hardware and software",
                  "Three: devices, media and services",
                  "Four: end devices, routers, switches and firewalls",
                  "Three: LANs, WANs and the Internet"],
         "a": "B — Three: devices, media and services",
         "why": "The Components of a Network slide names exactly three categories: devices, "
                "media and services (slide 9)."},
        {"type": "tf",
         "q": "A WAN is usually administered by a single organization and offers high-speed "
              "links to internal devices.",
         "a": "False",
         "why": "That describes a LAN. WANs interconnect LANs over wide areas, are usually "
                "administered by multiple service providers, and typically provide "
                "slower-speed links (slides 17–18)."},
        {"type": "tf",
         "q": "In a packet-switched network, redundancy allows alternative routes, which is a "
              "basis for fault tolerance.",
         "a": "True",
         "why": "Fault tolerance in packet-switched networks comes from redundant paths; if one "
                "route fails, packets can travel another (slides 25–27)."},
        {"type": "short",
         "q": "Name the four basic characteristics modern network architectures must address.",
         "a": "Fault tolerance, scalability, Quality of Service (QoS), and security.",
         "why": "Slide 25 lists these four to meet user expectations as networks evolve."},
        {"type": "short",
         "q": "What determines whether a device acts as a client, a server, or both?",
         "a": "The software on the device.",
         "why": "Slide 6: 'The software on a device determines its role' — e.g. browser software "
                "makes a device a client for web pages, e-mail server software makes it a "
                "server for mail."},
        {"type": "mc",
         "q": "Which list matches the chapter's three primary requirements for network security?",
         "opts": ["Confidentiality, integrity, availability",
                  "Authentication, authorization, accounting",
                  "Antivirus, firewall, VPN",
                  "Fault tolerance, scalability, QoS"],
         "a": "A — Confidentiality, integrity, availability",
         "why": "Slide 33 lists ensuring confidentiality, maintaining communication integrity "
                "and ensuring availability as the three primary requirements (B is an AAA "
                "triple from a later module, C are solution examples, D are architecture "
                "characteristics)."},
        {"type": "explain",
         "q": "Explain why giving telephony and video higher priority than web page retrieval is "
              "a QoS decision, and what QoS is not.",
         "a": "Time-sensitive communication needs packets delivered promptly, so QoS raises its "
              "priority and lowers that of non-time-sensitive traffic such as web or e-mail. "
              "QoS is prioritising existing capacity — it does not increase bandwidth.",
         "why": "Slide 29 gives exactly these priority examples: increase priority for "
                "telephony/video, decrease for web retrieval/e-mail. QoS = matching packet "
                "priority to communication type (slide 25)."},
        {"type": "explain",
         "q": "Using the chapter's examples, describe the difference between network "
              "infrastructure security and information security.",
         "a": "Network infrastructure security means physically securing devices and preventing "
              "unauthorized access to the management software on them; information security "
              "means protecting the data inside packets in transit and data stored on "
              "network-attached devices.",
         "why": "Slide 32 defines these two types of security concerns; the following slide "
                "adds the confidentiality/integrity/availability requirements that implement "
                "them."},
    ],
    "misunderstandings": [
        {"t": "Confusing client/server with a type of device",
         "d": "Client and server are <b>roles defined by software</b>, not hardware classes. "
              "The same device can be both — the chapter's peer-to-peer slide exists for "
              "exactly this reason (slide 6–7)."},
        {"t": "\"The Internet\" vs \"a network\"",
         "d": "The Internet is not one network owned by someone; it is a <b>conglomerate of "
              "networks</b> ('network of networks') kept interoperable by shared standards "
              "(slides 19, 41). A LAN, by contrast, is usually run by one organization."},
        {"t": "QoS = more bandwidth?",
         "d": "No. QoS is about <b>priority decisions</b> — which packets get served first or "
              "are blocked. More bandwidth is a capacity change; QoS is a scheduling policy "
              "(slides 25, 29)."},
        {"t": "Security = just antivirus",
         "d": "The chapter separates <b>infrastructure</b> and <b>information</b> security and "
              "requires confidentiality, integrity <i>and</i> availability. Antivirus is only "
              "one listed component next to firewalls, ACLs, IPS and VPNs (slides 32–40)."},
    ],
    "quick": (
        "<ul>"
        "<li><b>Scale:</b> networks from two computers to the Internet ('network of networks'); "
        "the Internet's standards come from bodies like IETF, ICANN, IAB.</li>"
        "<li><b>Components:</b> devices (end devices + intermediary: switches/WAPs, routers, "
        "firewalls), media (electrical/light/wireless signals), services.</li>"
        "<li><b>Roles:</b> client/server/both — set by software; hosts are identified by "
        "addresses.</li>"
        "<li><b>Types:</b> LAN = limited area, one administrator, fast; WAN = wide area, "
        "multiple providers, slower links. Also MAN, WLAN, SAN. The Internet interconnects "
        "them all.</li>"
        "<li><b>Platform requirements (4):</b> fault tolerance (redundant, packet-switched "
        "routes), scalability (grow without degrading), QoS (prioritise time-sensitive "
        "traffic), security (infrastructure + information; confidentiality, integrity, "
        "availability).</li>"
        "<li><b>Changing environment:</b> home trends (powerline, wireless broadband) and "
        "threats (viruses/worms/Trojans, spyware, zero-day, hackers, DoS, interception, "
        "identity theft) countered by antivirus, firewalls, ACLs, IPS, VPNs.</li>"
        "</ul>"
    ),
    "gaps": [
        "The <b>Chapter 1: Objectives</b> slide (slide 2) and the <b>Intranet and Extranet</b> "
        "slide (slide 20) contain no extractable text beyond their titles in the source PDF — "
        "objectives above are compiled from the section structure and the chapter Summary "
        "(slides 41–42) rather than quoted from the objectives slide.",
    ],
}
