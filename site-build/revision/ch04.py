# Revision kit content — Chapter 4: Network Access
# Grounded in uploads/Chapter 4_ITN_Network Access.pdf (slide refs = page numbers).

DATA = {
    "overview": (
        "Chapter 4 covers the bottom two layers in practice. <b>4.1</b> introduces the "
        "physical layer: its standards (RJ connectors, TIA-568 cabling, IEEE 802.3/802.11/"
        "802.15) and the principles of bandwidth and throughput. <b>4.2</b> is a survey of "
        "<b>media</b> — copper (UTP, STP, coaxial), fiber optic, and wireless — including UTP "
        "design/testing, fiber's four industry uses, a direct fiber-vs-copper comparison and "
        "the 802.11/802.15/802.16 wireless standards. <b>4.3</b> moves up to the data link "
        "layer: LLC and MAC sublayers, topologies, media-access methods (controlled vs "
        "contention), duplex, and the frame with its Layer 2 address."
    ),
    "objectives": [
        "Explain the purpose of the physical layer and what its standards address "
        "(<a class=\"rev-link\" href=\"#p4\">slides 4–6</a>).",
        "Distinguish bandwidth from throughput and name the factors that reduce throughput "
        "(<a class=\"rev-link\" href=\"#p7\">slides 7–8</a>).",
        "Compare copper, fiber and wireless media: construction, properties, testing and "
        "standards (<a class=\"rev-link\" href=\"#p11\">slides 11–26</a>).",
        "Describe the data link layer's sublayers (LLC and MAC) and how devices gain access "
        "to the media (<a class=\"rev-link\" href=\"#p28\">slides 28–43</a>).",
        "Recognise frames and Layer 2 addressing, and relate the TCP/IP network access layer "
        "to OSI Layers 1–2 (<a class=\"rev-link\" href=\"#p44\">slides 44–46</a>).",
    ],
    "concepts": [
        "<b>Physical layer standards</b> — physical components, encoding technique, signaling "
        "method.",
        "<b>Throughput vs capacity</b> — bits actually delivered per period, reduced by "
        "traffic and latency.",
        "<b>Copper vs fiber vs wireless</b> — cost, distance, EMI immunity, skills.",
        "<b>LLC + MAC sublayers</b> — LLC lets several protocols coexist on one network; MAC "
        "controls access.",
        "<b>Media access methods</b> — controlled (no collisions, token) vs contention "
        "(CSMA/CD, CSMA/CA).",
        "<b>Frames &amp; Layer 2 addresses</b> — the data link PDU and its hardware "
        "identifiers.",
    ],
    "definitions": [
        {"t": "Physical layer (Layer 1)",
         "d": "Provides the means to transport the <b>bits</b> that make up a data link layer "
              "frame across the network media; its standards address <b>physical components, "
              "frame encoding technique and signaling method</b>.", "r": 46},
        {"t": "Throughput",
         "d": "The number of bits transferred across the media over a given period of time; "
              "influenced by the amount of traffic, type of traffic, and latency/delays from "
              "the number of devices between source and destination.", "r": 8},
        {"t": "EMI / RFI",
         "abbr": "electromagnetic / radio-frequency interference",
         "d": "Interference copper must be designed against; UTP counters it indirectly "
              "(cancellation, twist rates) rather than with a shield.", "r": 16},
        {"t": "Crosstalk",
         "d": "Interference between wire pairs; limited by cancellation and by varying the "
              "number of twists per pair — a parameter checked when testing UTP.",
         "r": 16},
        {"t": "UTP", "abbr": "Unshielded Twisted Pair",
         "d": "The most common copper networking media; no shielding — instead cancellation "
              "and precise twist counts (pairs are twisted differently, e.g. orange less than "
              "blue) to limit crosstalk and outside EMI/RFI.", "r": 46},
        {"t": "STP", "abbr": "Shielded Twisted Pair",
         "d": "Twisted pair with foil/braided shields around the pairs or cable to fight "
              "interference.", "r": 14},
        {"t": "Coaxial cable",
         "d": "The third main copper type used in networking (with UTP and STP).", "r": 12},
        {"t": "Attenuation",
         "d": "Loss of signal strength — one of the parameters a UTP tester measures "
              "(with wire map, cable length and crosstalk).", "r": 19},
        {"t": "LLC", "abbr": "Logical Link Control sublayer",
         "d": "Data link sublayer that <b>makes it possible for several protocols to coexist "
              "and be transported over the same network</b>.", "r": 29},
        {"t": "MAC", "abbr": "Media Access Control sublayer",
         "d": "Data link sublayer that controls how devices access the media; the method "
              "depends on <b>topology and media sharing</b>.", "r": 32},
        {"t": "Topology (physical vs logical)",
         "d": "Physical topology = where devices/cables actually are; logical topology = how "
              "traffic is expected to flow (e.g. a logical point-to-point path may exist over "
              "media only one router uses).", "r": 35},
        {"t": "Controlled access",
         "d": "Media access where only one station transmits at a time — others wait their "
              "turn, <b>no collisions</b>; may use token passing (Token Ring IEEE 802.5, "
              "FDDI).", "r": 40},
        {"t": "Contention-based access",
         "d": "Media access where stations may transmit at any time, collisions exist, and "
              "mechanisms resolve contention: <b>CSMA/CD</b> for 802.3 Ethernet, "
              "<b>CSMA/CA</b> for 802.11 wireless.", "r": 41},
        {"t": "Frame",
         "d": "The data link layer PDU; the physical layer transports its bits across the "
              "media.", "r": 46},
        {"t": "Layer 2 address",
         "d": "The data link layer's address carried in frames (MAC addressing — see Chapter "
              "5).", "r": 45},
        {"t": "CSMA/CA", "abbr": "Carrier Sense Multiple Access with Collision Avoidance",
         "d": "The access mechanism used by <b>802.11 wireless</b> networks.", "r": 41},
        {"t": "CSMA/CD", "abbr": "Carrier Sense Multiple Access with Collision Detection",
         "d": "The access mechanism used by <b>802.3 Ethernet</b> networks.", "r": 41},
    ],
    "explanations": [
        {"t": "Why UTP works without a shield",
         "d": "UTP uses two tricks instead of shielding: <b>cancellation</b> — wires in a "
              "circuit are placed so their magnetic fields cancel each other (and outside "
              "EMI/RFI) — and <b>controlled twist rates</b> — precise twists per metre "
              "specified by standard (orange pair is twisted less than the blue pair).",
         "e": "That's why untwisting a cable too far at the connector invites crosstalk — "
              "the design relies on the twists.",
         "r": 16},
        {"t": "Reading the fiber-vs-copper table",
         "d": "Fiber wins on almost every physical property — distance (up to 100 km vs "
              "1–100 m), EMI/electrical immunity (complete), bandwidth ceiling (100 Gbps vs "
              "10 Gbps) — but loses on cost, installation skill and safety handling, which "
              "are 'highest' for fiber and 'lowest' for copper.",
         "e": "Copper suits an office floor run; fiber suits a building backbone or links "
              "between cities.",
         "r": 24},
        {"t": "Choosing an access method follows the topology",
         "d": "The MAC method depends on <b>topology and media sharing</b>. Shared-media "
              "designs that schedule turns (token ring/FDDI) give <b>no collisions</b>; "
              " Ethernet/Wi-Fi let anyone talk and resolve collisions: CD on wired, CA on "
              "wireless (CA because a wireless station cannot hear a collision while "
              "transmitting — avoidance instead).",
         "e": "Same office, two technologies: an Ethernet hub segment uses CSMA/CD; the Wi-Fi "
              "association uses CSMA/CA.",
         "r": 41},
        {"t": "Throughput is not the same as the label on the box",
         "d": "Throughput = bits actually transferred per period. It drops with (1) the "
              "amount of traffic, (2) the type of traffic, and (3) latency added by every "
              "device between source and destination — so a '1 Gbps' link can deliver far "
              "less in a busy, deeply nested path.",
         "e": "A busy office link at peak hour: same hardware, lower throughput than at "
              "night.",
         "r": 8},
        {"t": "LLC and MAC split the work",
         "d": "The data link layer splits into <b>LLC</b> (lets several protocols coexist and "
              "be transported over the same network) and <b>MAC</b> (decides how/when a device "
              "uses the media). Different MAC technologies sit under the same LLC: 802.3 "
              "Ethernet, 802.11 Wi-Fi, 802.15 Bluetooth.",
         "e": "One PC can use Ethernet and Wi-Fi simultaneously because LLC abstracts which "
              "MAC is underneath.",
         "r": 29},
        {"t": "Physical layer standards you should recognise",
         "d": "<b>ISO 8877</b> adopted RJ connectors (RJ-11, RJ-45); <b>ISO 11801</b> is a "
              "network cabling standard similar to EIA/TIA 568; <b>TIA-568-C</b> is the "
              "telecommunications cabling standard used by nearly all voice/video/data "
              "networks (RJ-45 pinouts); <b>TIA-598-C</b> fiber color coding; <b>TIA-942</b> "
              "data centre infrastructure; <b>G.992</b> ADSL; <b>IEEE 802.3/802.11/802.15</b> "
              "Ethernet/Wi-Fi/Bluetooth.",
         "e": "A cabling exam question about pinouts points to TIA-568-C; fiber colour coding "
              "points to TIA-598-C.",
         "r": 6},
    ],
    "comparisons": [
        {"t": "Fiber vs copper (from the chapter's table)",
         "cols": ["Property", "Copper (UTP-class)", "Fiber optic"],
         "rows": [
             ["Bandwidth supported", "10 Mbps – 10 Gbps", "10 Mbps – 100 Gbps"],
             ["Distance", "Relatively short (1 – 100 m)", "Relatively high (1 – 100,000 m)"],
             ["Immunity to EMI/RFI", "Low", "High (completely immune)"],
             ["Immunity to electrical hazards", "Low", "High (completely immune)"],
             ["Media &amp; connector costs", "Lowest", "Highest"],
             ["Installation skills", "Lowest", "Highest"],
             ["Safety precautions", "Lowest", "Highest"],
         ],
         "note": "Values exactly as listed on the Fiber versus Copper slide.",
         "refs": [24]},
        {"t": "Controlled access vs contention-based access",
         "cols": ["Aspect", "Controlled access", "Contention-based access"],
         "rows": [
             ["Transmitting", "Only one station at a time; others wait their turn",
              "Stations can transmit at any time"],
             ["Collisions", "No collisions", "Collisions exist; mechanisms resolve contention"],
             ["Method", "May use token passing", "CSMA/CD (802.3 Ethernet), CSMA/CA (802.11 "
              "wireless)"],
             ["Examples in chapter", "Token Ring (IEEE 802.5), FDDI", "Ethernet, Wi-Fi"],
         ],
         "note": "The MAC method depends on topology and media sharing.",
         "refs": [32, 40, 41]},
    ],
    "facts": [
        {"d": "Physical layer standards address three areas: <b>physical components, frame "
              "encoding technique, signaling method</b>.", "r": 46},
        {"d": "Standards: ISO 8877 (RJ connectors), ISO 11801 (cabling, like EIA/TIA 568), "
              "TIA-568-C (cabling, RJ-45 pinouts), TIA-569-B (pathways/spaces), TIA-598-C "
              "(fiber color coding), TIA-942 (data centres), G.992 (ADSL), IEEE 802.3/802.11/"
              "802.15.", "r": 6},
        {"d": "Throughput factors: <b>amount of traffic, type of traffic, latency/delays from "
              "the number of devices</b> between source and destination.", "r": 8},
        {"d": "Three copper types: <b>UTP, STP, coaxial</b>; UTP is the most common.", "r": 46},
        {"d": "Every copper termination is a point of possible <b>signal loss and noise "
              "introduction</b>.", "r": 17},
        {"d": "UTP test parameters: <b>wire map, cable length, attenuation (signal loss), "
              "crosstalk</b>.", "r": 19},
        {"d": "Fiber's four industry uses: <b>enterprise backbones, FTTH/access (always-on "
              "broadband), long-haul (ISP/inter-country), submarine</b>.", "r": 20},
        {"d": "Wireless concerns: <b>coverage area, interference, security</b>.", "r": 25},
        {"d": "802.11 variants: a = 54 Mbps/5 GHz; b = 11 Mbps/2.4 GHz; g = 54 Mbps/2.4 GHz "
              "(b-compatible); n = 600 Mbps (2.4 &amp; 5 GHz); ac = 1 Gbps/5 GHz; ad = 7 Gbps "
              "(2.4/5/60 GHz).", "r": 26},
        {"d": "IEEE 802.15 (Bluetooth): up to 3 Mb/s, pairing over 1–100 m; IEEE 802.16: up to "
              "1 Gbps, point-to-multipoint wireless broadband.", "r": 26},
        {"d": "Data link layer splits into <b>LLC and MAC</b>; LLC enables several protocols "
              "to coexist over the same network; related families: 802.3 Ethernet, 802.11 "
              "Wi-Fi, 802.15 Bluetooth.", "r": 29},
        {"d": "Token passing examples: <b>Token Ring (IEEE 802.5), FDDI</b> — controlled "
              "access with no collisions.", "r": 40},
        {"d": "The TCP/IP <b>network access layer equals OSI Layer 2 + Layer 1</b>.", "r": 46},
    ],
    "questions": [
        {"type": "mc",
         "q": "Which standard gives the RJ-45 pinouts used by nearly all voice, video and data "
              "networks?",
         "opts": ["TIA-568-C", "TIA-598-C", "ISO 8877", "G.992"],
         "a": "A — TIA-568-C",
         "why": "Slide 6: TIA-568-C is the telecommunications cabling standard used by nearly "
                "all voice/video/data networks (568-C: RJ-45 pinouts). TIA-598-C is fiber "
                "colour coding, ISO 8877 adopted RJ connectors, G.992 is ADSL."},
        {"type": "tf",
         "q": "UTP cable counters EMI/RFI with a foil shield wrapped around its pairs.",
         "a": "False",
         "why": "UTP does <b>not</b> use shielding — it relies on cancellation and precise "
                "twist rates (slide 16). The foil/braided shields describe STP (slide 14)."},
        {"type": "short",
         "q": "List the four parameters a UTP cable tester should check after installation.",
         "a": "Wire map (proper pin termination, shorts), cable length, signal loss due to "
              "attenuation, and crosstalk.",
         "why": "Slide 19 lists exactly these four."},
        {"type": "mc",
         "q": "Which access mechanism is used by 802.11 wireless networks?",
         "opts": ["CSMA/CD", "CSMA/CA", "Token passing", "FDDI"],
         "a": "B — CSMA/CA",
         "why": "Slide 41: CSMA/CD for 802.3 Ethernet, CSMA/CA for 802.11 wireless. Token "
                "passing (Token Ring, FDDI) is the controlled-access alternative."},
        {"type": "tf",
         "q": "In a controlled-access method such as token passing, collisions cannot occur "
              "because only one station transmits at a time.",
         "a": "True",
         "why": "Slide 40: one station at a time, devices wait their turn, no collisions."},
        {"type": "short",
         "q": "Name the three main types of copper media used in networking.",
         "a": "Unshielded twisted pair (UTP), shielded twisted pair (STP), and coaxial cable.",
         "why": "Summary slide 46 states all three and notes UTP is the most common."},
        {"type": "explain",
         "q": "A network needs a 5 km link between two buildings with heavy electrical "
              "machinery nearby. Using the chapter's fiber-vs-copper table, justify fiber.",
         "a": "Distance: copper is 'relatively short (1–100 m)' while fiber reaches "
              "1–100,000 m, so 5 km rules copper out. EMI: copper's EMI/RFI immunity is low, "
              "fiber is completely immune — essential near electrical machinery. The trade-off "
              "is cost, installation skill and safety precautions, which are highest for fiber.",
         "why": "All four points come straight from the Fiber versus Copper table (slide 24)."},
        {"type": "mc",
         "q": "What is the main purpose of the LLC sublayer?",
         "opts": ["To make several protocols coexist and be transported over the same network",
                  "To detect collisions on Ethernet",
                  "To encode bits onto the media",
                  "To assign IP addresses to hosts"],
         "a": "A — protocols coexisting on one network",
         "why": "Slide 29: LLC 'makes it possible for several protocols to coexist and to be "
                "transported over the same network'."},
    ],
    "misunderstandings": [
        {"t": "\"Unshielded\" = unprotected against interference",
         "d": "UTP has no shield but is engineered against EMI/RFI/crosstalk via "
              "<b>cancellation and twist rates</b>; STP instead adds foil/braided shields "
              "(slides 12–16)."},
        {"t": "Bandwidth = what you actually get (throughput)",
         "d": "Throughput is the measured <b>bits transferred per period</b>, reduced by "
              "traffic volume, traffic type and latency from intermediate devices (slide 8) — "
              "it is the real-world figure, not the link's headline capability."},
        {"t": "All networks handle collisions the same way",
         "d": "No: controlled access (token) has <b>no collisions</b>; contention-based "
              "Ethernet uses <b>CSMA/CD</b> and wireless uses <b>CSMA/CA</b> — different "
              "mechanisms for shared media (slides 40–41)."},
        {"t": "Physical topology = logical topology",
         "d": "Physical = where devices/cables are; logical = how traffic is expected to flow. "
              "The chapter's point-to-point slides show a logical path can differ from who "
              "physically owns the media (slides 33–36)."},
    ],
    "quick": (
        "<ul>"
        "<li><b>Layer 1:</b> transports the bits of data link frames; standards cover physical "
        "components, encoding and signaling (RJ via ISO 8877; TIA-568-C pinouts; TIA-598-C "
        "fiber colours; 802.3/802.11/802.15).</li>"
        "<li><b>Throughput</b> = bits per period; drops with traffic amount, traffic type and "
        "device latency.</li>"
        "<li><b>Copper:</b> UTP (most common; cancellation + twists, no shield), STP (shielded), "
        "coax. Test UTP for wire map, length, attenuation, crosstalk — every termination risks "
        "loss/noise.</li>"
        "<li><b>Fiber:</b> longer reach (to 100 km), 100 Gbps, fully immune to EMI/electrical "
        "hazards — but highest cost/skill/safety needs; used in backbones, FTTH, long-haul, "
        "submarine.</li>"
        "<li><b>Wireless:</b> concerns = coverage, interference, security; 802.11a/b/g/n/ac/ad "
        "(up to 7 Gbps), 802.15 Bluetooth (3 Mb/s, 1–100 m), 802.16 (1 Gbps point-to-multipoint). "
        "Wi-Fi uses CSMA/CA.</li>"
        "<li><b>Layer 2:</b> LLC (protocols coexist) + MAC (media access: controlled/token — no "
        "collisions — vs contention CSMA/CD|CA); frames carry Layer 2 addresses; TCP/IP network "
        "access layer = OSI L1 + L2.</li>"
        "</ul>"
    ),
    "gaps": [
        "The <b>Bandwidth</b> slide (7), <b>half-/full-duplex</b> slide (37), <b>frame "
        "structure</b> slides (44–45) and several topology slides (33–43) present key detail "
        "as figures — the extractable text has titles only, so no frame-field table or duplex "
        "definitions are reproduced here.",
        "The outline slide lists a section '4.4 Media Access Control' that is covered inside "
        "4.3 in this deck's structure — no separate 4.4 text content exists beyond the "
        "media-access slides shown.",
    ],
}
