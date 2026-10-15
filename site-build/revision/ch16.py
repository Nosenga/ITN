# Revision kit content — Chapter 16: Network Security Fundamentals
# Grounded in uploads/Chapter16 (Network Security Fundamentals).pdf (slide refs = page numbers).

DATA = {
    "overview": (
        "Module 16 builds from <b>why security matters</b> to <b>hardening real devices</b>. "
        "16.1 covers threats and vulnerabilities: what intruders gain (information theft, "
        "data loss/manipulation, identity theft, disruption of service), the three "
        "vulnerability classes (technological, configuration, security policy) and the four "
        "classes of physical threats. 16.2 classifies attacks: <b>malware</b> (viruses, worms, "
        "Trojans) plus the three network-attack categories — <b>reconnaissance, access, "
        "denial of service</b> — including DDoS botnets. 16.3 gives mitigations: "
        "<b>defense-in-depth</b>, backups, patching, AAA, firewalls/DMZ/SPI and endpoint "
        "security. 16.4 hardens devices: AutoSecure, strong passwords/passphrases, encrypted "
        "passwords, <b>enabling SSH</b> and disabling unused services. The stated module "
        "objective: <i>configure switches and routers with device hardening features to "
        "enhance security</i>."
    ),
    "objectives": [
        "Explain why basic security measures are necessary on network devices — topic "
        "objective for Security Threats and Vulnerabilities "
        "(<a class=\"rev-link\" href=\"#p7\">slides 7–9</a>).",
        "Identify security vulnerabilities — technological, configuration and security-policy "
        "weaknesses (<a class=\"rev-link\" href=\"#p8\">slide 8</a>).",
        "Identify general mitigation techniques — defense-in-depth, backups, patching, AAA, "
        "firewalls, endpoints (<a class=\"rev-link\" href=\"#p17\">slides 17–23</a>).",
        "Configure network devices with hardening features — AutoSecure, passwords, SSH, "
        "service disabling (<a class=\"rev-link\" href=\"#p25\">slides 25–29</a>).",
        "Classify attacks: malware types and the three network-attack categories "
        "(<a class=\"rev-link\" href=\"#p11\">slides 11–14</a>).",
    ],
    "concepts": [
        "<b>Threats vs vulnerabilities</b> — attacks' outcomes vs the degree of weakness "
        "exploited.",
        "<b>Malware family</b> — viruses, worms, Trojan horses: how each spreads.",
        "<b>Three network-attack categories</b> — reconnaissance, access, DoS.",
        "<b>Defense-in-depth</b> — layered devices/services working in tandem.",
        "<b>AAA</b> — authenticate, authorize, account.",
        "<b>Device hardening</b> — defaults are inadequate: change, restrict, encrypt, SSH, "
        "disable.",
    ],
    "definitions": [
        {"t": "Threat actor",
         "d": "An intruder who gains access by modifying software or exploiting software "
              "vulnerabilities.", "r": 7},
        {"t": "Four types of threats (after access)",
         "d": "<b>Information theft; data loss and manipulation; identity theft; disruption "
              "of service</b>.", "r": 7},
        {"t": "Vulnerability",
         "d": "The <b>degree of weakness</b> in a network or a device — some degree is "
              "inherent even in routers, switches, servers and security devices; endpoints "
              "(servers, desktops) are typically the devices under attack.", "r": 8},
        {"t": "Three primary vulnerability classes",
         "d": "<b>Technological</b> (TCP/IP weaknesses, OS weaknesses, network equipment "
              "weaknesses); <b>Configuration</b> (unsecured accounts, easily guessed "
              "passwords, misconfigured services/equipment, insecure defaults); <b>Security "
              "policy</b> (no written policy, no authentication continuity, controls not "
              "applied, changes off-policy, no disaster-recovery plan).", "r": 8},
        {"t": "Four classes of physical threats",
         "d": "<b>Hardware, environmental, electrical, maintenance</b> — e.g. cabling/workstation "
              "damage, humidity extremes, brownouts/total power loss, ESD/poor cabling/poor "
              "labeling.", "r": 35},
        {"t": "Malware", "abbr": "malicious software",
         "d": "Code or software specifically designed to damage, disrupt, steal or inflict "
              "illegitimate action on data, hosts or networks.", "r": 11},
        {"t": "Virus",
         "d": "Malware that inserts itself into and becomes part of another program, spreading "
              "from one computer to another and leaving infections as it travels.", "r": 11},
        {"t": "Worm",
         "d": "Standalone software that does <b>not</b> require a host program or human help "
              "to propagate.", "r": 11},
        {"t": "Trojan horse",
         "d": "Malware that does not reproduce by infecting other files — it spreads through "
              "<b>user interaction</b>, such as opening an e-mail attachment or downloading "
              "and running a file.", "r": 11},
        {"t": "Reconnaissance attack",
         "d": "<b>Discovery and mapping</b> of systems, services or vulnerabilities — e.g. "
              "pinging publicly available IP addresses to find active ones.", "r": 12},
        {"t": "Access attack",
         "d": "<b>Unauthorized manipulation of data, system access, or user privileges</b> — "
              "exploits known weaknesses in authentication, FTP and web services (chapter "
              "example: SSH (port 22) into a trusted host, then Telnet (port 23) to reach "
              "another target; interception to read or modify data in transit).", "r": 13},
        {"t": "DoS", "abbr": "Denial of Service",
         "d": "<b>Disabling or corrupting networks, systems or services</b> — ultimately "
              "preventing authorized people from using a service by consuming system "
              "resources; the most publicized and among the hardest to eliminate, yet "
              "relatively simple to conduct.", "r": 14},
        {"t": "DDoS", "abbr": "Distributed Denial of Service",
         "d": "A DoS attack originating from <b>multiple coordinated sources</b> — infected "
              "hosts called <b>zombies</b> form a <b>botnet</b>, directed by a "
              "<b>command and control (CnC)</b> program.", "r": 14},
        {"t": "Defense-in-depth",
         "abbr": "also 'layered approach'",
         "d": "A combination of networking devices and services <b>working in tandem</b> to "
              "protect users and assets against TCP/IP threats; list given: <b>VPN, ASA "
              "firewall, IPS, ESA/WSA, AAA server</b>.", "r": 17},
        {"t": "AAA", "abbr": "Authentication, Authorization, Accounting ('triple A')",
         "d": "The primary framework for access control on network devices: "
              "<b>authenticate</b> who may access the network, <b>authorize</b> what actions "
              "they may perform, <b>account</b> for what they did — likened to a credit card "
              "(identity, spending limit, itemised record).", "r": 20},
        {"t": "Firewall",
         "d": "Resides <b>between two or more networks</b>, controls the traffic between them "
              "and helps prevent unauthorized access; can grant outside users controlled "
              "access to specific services.", "r": 21},
        {"t": "DMZ", "abbr": "demilitarized zone",
         "d": "A special network where servers accessible to outside users are usually "
              "located, letting administrators apply specific policies to those hosts.",
         "r": 21},
        {"t": "SPI", "abbr": "stateful packet inspection",
         "d": "Firewall technique that tracks internal requests and <b>blocks unsolicited "
              "packets unless specifically permitted</b>; can also recognise and filter "
              "attacks such as DoS.", "r": 22},
        {"t": "Endpoint",
         "d": "An individual computer system or device acting as a network client — laptops, "
              "desktops, servers, smartphones, tablets; securing them is among the hardest "
              "jobs because it involves human nature (policies, training, antivirus, host "
              "IPS, network access control).", "r": 23},
        {"t": "Cisco AutoSecure",
         "d": "Feature for Cisco routers that helps secure the system — needed because "
              "<b>default security settings are usually inadequate</b>.", "r": 25},
        {"t": "Passphrase",
         "d": "A password made of a phrase of many words (spaces allowed — note: on Cisco "
              "routers <b>leading spaces are ignored</b>, spaces after the first character "
              "are not); often easier to remember, longer and harder to guess.", "r": 26},
        {"t": "Backup considerations",
         "d": "Frequency (regular per policy; full monthly/weekly with frequent partials), "
              "storage (offsite rotation), validation (integrity + restoration tests), "
              "security (strong passwords required to restore).", "r": 18},
        {"t": "SSH hardening chain",
         "d": "Six steps: unique hostname → IP domain name → generate RSA key "
              "(<code>crypto key generate rsa general-keys modulus bits</code>; 360–2048 bits, "
              "<b>minimum recommended 1024</b>) → local database username → "
              "<code>login local</code> on vty → <code>transport input ssh|telnet</code> "
              "(by default no vty input session is allowed).", "r": 28},
    ],
    "explanations": [
        {"t": "The attack story end to end",
         "d": "An intruder gets in via software vulnerabilities, hardware attacks or guessed "
              "credentials; if they modify software or exploit vulnerabilities they are a "
              "<b>threat actor</b>. Once inside, four threat types may arise: information "
              "theft, data loss/manipulation, identity theft, disruption of service. The "
              "root causes sit in three vulnerability classes — technological, configuration, "
              "security policy — which is why mitigation addresses all three (patching, "
              "hardening, written policy).",
         "e": "An easily guessed default password is a configuration vulnerability that "
              "enables identity theft as its impact.",
         "r": 7},
        {"t": "How to tell malware apart",
         "d": "<b>Virus</b>: needs to insert itself into another program and travels with "
              "infected hosts. <b>Worm</b>: standalone — no host program, no human help "
              "needed to propagate. <b>Trojan</b>: doesn't reproduce by infecting files at "
              "all — it waits for <b>user interaction</b> (open attachment, run download). "
              "That difference drives response: patch networks stops worms; user training "
              "stops Trojans.",
         "e": "The chapter's worm mitigation — auto-downloading OS security updates and "
              "patching all vulnerable systems — exists precisely because worms need no user.",
         "r": 19},
        {"t": "DoS vs DDoS",
         "d": "DoS consumes system resources so authorized users can't use the service — "
              "simple enough for unskilled actors. <b>DDoS</b> is the same goal from "
              "<b>many coordinated sources</b>: the actor builds infected hosts (<b>zombies</b>), "
              "a <b>botnet</b>, and drives it with a <b>CnC</b> program. Distributed volume is "
              "why DDoS is hard to eliminate — hence staying current on security updates is "
              "the chapter's practical prevention advice.",
         "e": "One PC flooding a server = DoS; thousands of zombie PCs directed by CnC = DDoS.",
         "r": 14},
        {"t": "AAA, with the credit-card analogy",
         "d": "<b>Authenticate</b>: who are you? (card identifies the user) · "
              "<b>Authorize</b>: what may you do? (spending limit) · <b>Account</b>: what did "
              "you actually do? (itemised statement). AAA provides the primary framework to "
              "set up access control on network devices — identity, permission, audit trail.",
         "e": "Login = authenticate; a read-only operator account = authorize; "
              "<code>show</code> command logging = accounting.",
         "r": 20},
        {"t": "Hardening in the order the chapter gives it",
         "d": "1) Defaults are inadequate — change default usernames/passwords immediately. "
              "2) Restrict system resources to authorized individuals. 3) Turn off/uninstall "
              "unnecessary services. 4) Patch before implementation (warehouse devices ship "
              "stale). 5) Enforce strong passwords/passphrases (≥8, preferably 10+, complex, "
              "no dictionary/names/dates, deliberate misspellings, change often, never written "
              "down). 6) Encrypt plaintext passwords, set minimum lengths, deter brute force, "
              "timeout inactive privileged EXEC. 7) Enable SSH (six steps). 8) Disable "
              "unused services (preserve CPU/RAM, remove attack surface).",
         "e": "Out-of-box router → AutoSecure + manual password/SSH work before it touches "
              "the production network.",
         "r": 29},
        {"t": "Why defense-in-depth instead of one silver bullet",
         "d": "No single product covers every path. The layered approach combines devices and "
              "services <b>working in tandem</b> — VPN, ASA firewall, IPS, ESA/WSA, AAA server "
              "— so if one layer is bypassed, others still enforce policy. Backups, patching "
              "and endpoint policies extend the same idea beyond network devices.",
         "e": "Perimeter firewall + IPS + strict AAA + offline backups = depth across "
              "prevention, detection, and recovery.",
         "r": 17},
    ],
    "comparisons": [
        {"t": "Virus vs worm vs Trojan horse",
         "cols": ["Aspect", "Virus", "Worm", "Trojan horse"],
         "rows": [
             ["Form", "Inserts into and becomes part of another program",
              "Standalone software", "Malware disguised as useful software"],
             ["Propagation", "Spreads from computer to computer with infected hosts",
              "No host program and <b>no human help</b> required",
              "<b>User interaction</b> required — open attachment, download/run a file"],
             ["Reproduces by infecting files?", "Yes — needs the host file",
              "Self-propagating without a host file", "No — does not reproduce by infecting "
              "other files"],
             ["Implied countermeasure (chapter's mitigations)", "Patch + antivirus",
              "Security updates from the OS vendor; patch all vulnerable systems; auto-updates",
              "User training / policy (interaction is the trigger)"],
         ],
         "note": "All three are types of malware — 'code or software specifically designed to "
                 "damage, disrupt, steal, or inflict illegitimate action'.",
         "refs": [11, 19]},
        {"t": "DoS vs DDoS",
         "cols": ["Aspect", "DoS", "DDoS"],
         "rows": [
             ["Sources", "One source", "Multiple coordinated sources"],
             ["Mechanism", "Consumes system resources so authorized people cannot use the "
              "service", "Same goal, amplified by a network of infected hosts"],
             ["Infrastructure", "—", "Zombies → a <b>botnet</b>, directed by a "
              "<b>command and control (CnC)</b> program"],
             ["Difficulty", "Relatively simple to conduct — even by an unskilled actor; most "
              "publicized and hard to eliminate", "Same characteristics, larger scale"],
         ],
         "note": "The chapter's prevention advice for both: stay up to date with the latest "
                 "security updates for operating systems and applications.",
         "refs": [14]},
    ],
    "facts": [
        {"d": "Module objective: <b>configure switches and routers with device hardening "
              "features to enhance security</b>.", "r": 5},
        {"d": "After access, four threat types may arise: <b>information theft; data loss and "
              "manipulation; identity theft; disruption of service</b>.", "r": 7},
        {"d": "Three vulnerability classes: <b>technological, configuration, security "
              "policy</b>; endpoints are typically the devices under attack.", "r": 8},
        {"d": "Four physical threat classes: <b>hardware, environmental, electrical, "
              "maintenance</b>; a physical-security plan must be created and implemented.",
         "r": 35},
        {"d": "Network attacks fall into three categories: <b>reconnaissance</b> (discovery/"
              "mapping), <b>access</b> (unauthorized manipulation of data/access/privileges), "
              "<b>denial of service</b> (disabling or corrupting networks/systems/services).",
         "r": 12},
        {"d": "Access-attack example ports: <b>SSH port 22</b>, <b>Telnet port 23</b> "
              "(pivot between trusted hosts).", "r": 13},
        {"d": "DDoS building blocks: <b>zombies</b>, <b>botnet</b>, <b>CnC</b> program.",
         "r": 14},
        {"d": "Defense-in-depth devices/services: <b>VPN, ASA firewall, IPS, ESA/WSA, AAA "
              "server</b>.", "r": 17},
        {"d": "Backups: regular per security policy; full monthly/weekly + frequent partials; "
              "<b>offsite</b> rotation; <b>validated</b> (integrity + restore tests); "
              "protected with <b>strong passwords</b> (required to restore).", "r": 18},
        {"d": "Most effective worm mitigation: <b>security updates from the OS vendor + patch "
              "all vulnerable systems</b>; automate end-system updates.", "r": 19},
        {"d": "AAA = <b>authenticate</b> (who), <b>authorize</b> (what actions), "
              "<b>account</b> (record) — credit-card analogy.", "r": 20},
        {"d": "Firewalls sit <b>between networks</b>; outside-facing servers usually live in "
              "a <b>DMZ</b>; SPI blocks unsolicited packets unless permitted and can filter "
              "DoS-style attacks.", "r": 22},
        {"d": "Password rules: <b>≥8 chars, preferably 10+</b>; complex (upper/lower/numbers/"
              "symbols/spaces); avoid dictionary words, names, dates, usernames, sequences; "
              "deliberate misspellings (Smith = Smyth = 5mYth); change often; never leave "
              "written where visible; on Cisco routers <b>leading spaces are ignored</b> "
              "(later spaces are not) → consider passphrases.", "r": 26},
        {"d": "Extra password hardening: encrypt plaintext passwords, set minimum length, "
              "deter brute-force guessing, <b>disable inactive privileged EXEC access after a "
              "timeout</b>.", "r": 27},
        {"d": "SSH enabling: unique hostname → IP domain name → "
              "<code>crypto key generate rsa general-keys modulus bits</code> (360–2048; "
              "<b>min recommended 1024</b>) → local username database → <code>login "
              "local</code> → <code>transport input ssh|telnet</code> (default: no vty input "
              "allowed).", "r": 28},
        {"d": "Disable unused services to <b>preserve CPU/RAM</b> and prevent exploitation; "
              "default service sets vary by IOS version.", "r": 29},
        {"d": "AutoSecure assists router hardening; <b>default settings are inadequate</b>; "
              "change defaults, restrict access, uninstall unnecessary services, "
              "<b>patch before implementation</b>.", "r": 25},
    ],
    "questions": [
        {"type": "mc",
         "q": "The module objective of Chapter 16 is:",
         "opts": ["Configure switches and routers with device hardening features to enhance "
                  "security",
                  "Design enterprise routing protocols",
                  "Implement wireless controller fleets",
                  "Write a corporate security policy document"],
         "a": "A — Configure switches and routers with device hardening features",
         "why": "Slide 5 states the module objective exactly this way, with topic objectives "
                "supporting it."},
        {"type": "short",
         "q": "Name the four types of threats that may arise after a threat actor gains "
              "access, and the three primary vulnerability classes.",
         "a": "Threats: information theft; data loss and manipulation; identity theft; "
              "disruption of service. Vulnerability classes: technological, configuration, "
              "security policy.",
         "why": "Slides 7 and 8 respectively — and both are recapped in the module summary."},
        {"type": "tf",
         "q": "A worm requires an infected host file and human help to spread, just like a "
              "virus.",
         "a": "False",
         "why": "Worms are standalone and 'do not require a host program or human help to "
                "propagate' — that is the distinction from viruses (slide 11)."},
        {"type": "mc",
         "q": "Which statement correctly separates the three network-attack categories?",
         "opts": ["Reconnaissance = discovery/mapping; access = unauthorized manipulation; "
                  "DoS = disabling/corrupting services",
                  "Reconnaissance = stealing files; access = deleting files; DoS = slowing "
                  "files",
                  "Reconnaissance = malware only; access = physical only; DoS = policy only",
                  "They are three names for the same attack"],
         "a": "A — discovery/mapping · unauthorized manipulation · disabling/corrupting",
         "why": "Slide 12 defines all three categories with those exact phrases."},
        {"type": "tf",
         "q": "A DDoS attack originates from multiple coordinated sources using a botnet of "
              "zombies directed by a CnC program.",
         "a": "True",
         "why": "Slide 14: DDoS 'is similar to a DoS attack, but it originates from multiple, "
                "coordinated sources' — zombies form a botnet run via command and control."},
        {"type": "short",
         "q": "State the three AAA functions and the analogy used for them.",
         "a": "Authentication (who is permitted to access the network), authorization (what "
              "actions they perform while accessing it), accounting (a record of what was "
              "done) — compared to using a credit card (identifies the user, sets the "
              "spending limit, keeps an itemised account).",
         "why": "Slide 20 defines the triple A with the credit-card analogy."},
        {"type": "mc",
         "q": "When enabling SSH, what is the minimum recommended RSA modulus length, and what "
              "is the trade-off of larger keys?",
         "opts": ["1024 bits; larger keys are more secure but take longer to encrypt/decrypt",
                  "360 bits; larger keys are less secure",
                  "2048 bits; larger keys are faster",
                  "512 bits; the size does not matter"],
         "a": "A — minimum 1024 bits; bigger = more secure, slower",
         "why": "Slide 28: modulus bits range 360–2048, 'the minimum recommended modulus "
                "length is 1024 bits', and larger values 'take longer to encrypt and decrypt'."},
        {"type": "short",
         "q": "Give four of the chapter's strong-password guidelines.",
         "a": "Any four of: length ≥8 characters (preferably 10+); complexity (mix of upper/"
              "lower case, numbers, symbols, spaces if allowed); avoid repetition, dictionary "
              "words, sequences, usernames, relative/pet names, biographical details; "
              "deliberately misspell (Smith = Smyth = 5mYth); change often; do not write "
              "passwords down in obvious places.",
         "why": "Slide 26 lists these guidelines verbatim."},
        {"type": "explain",
         "q": "Explain the defense-in-depth (layered) approach and why one security product is "
              "not enough, naming at least three components from the chapter.",
         "a": "Defense-in-depth requires a combination of devices and services working in "
              "tandem to protect users and assets against TCP/IP threats — layers compensate "
              "for each other. The chapter lists VPN, ASA firewall, IPS, ESA/WSA and AAA "
              "server as components implemented together; backups, patching and endpoint "
              "policies extend the layering beyond traffic paths.",
         "why": "Slide 17 defines the layered approach and gives the component list; slides "
                "18–23 supply the complementary measures."},
    ],
    "misunderstandings": [
        {"t": "\"Default device settings are secure enough\"",
         "d": "Explicitly rejected: 'the default values … in most cases, this level of "
              "security is inadequate' — hence AutoSecure, changed default credentials, "
              "restricted access and disabled services (slide 25)."},
        {"t": "Trojans spread like worms",
         "d": "Worms need <b>no human help</b>; Trojans <b>must</b> spread through user "
              "interaction — opening attachments, downloading/running files (slide 11)."},
        {"t": "DoS and DDoS are interchangeable terms",
         "d": "DDoS = coordinated <b>multiple sources</b> (zombies/botnet/CnC); a single-source "
              "resource exhaustion is plain DoS (slide 14)."},
        {"t": "AAA is just login",
         "d": "Three distinct services: authentication (identity), authorization (permitted "
              "actions), accounting (records of what was done) — the credit-card model "
              "(slide 20)."},
        {"t": "A firewall alone equals security",
         "d": "The chapter's position is <b>defense-in-depth</b>: firewalls (plus DMZ/SPI) are "
              "one layer alongside IPS, VPN, AAA server, backups, patching and endpoint "
              "policies (slides 17–23)."},
        {"t": "Long complex passwords must be unmemorable",
         "d": "The <b>passphrase</b> approach — a phrase of many words — is encouraged: easier "
              "to remember, longer, harder to guess (watch: Cisco routers ignore <b>leading</b> "
              "spaces only) (slide 26)."},
    ],
    "quick": (
        "<ul>"
        "<li><b>Why:</b> attacks cost time/money via damage or theft. Threat actor = intruder "
        "who modifies software/exploits vulnerabilities. Impacts: information theft, data loss/"
        "manipulation, identity theft, disruption of service.</li>"
        "<li><b>Vulnerabilities (3):</b> technological, configuration, security policy. "
        "<b>Physical threats (4):</b> hardware, environmental, electrical, maintenance.</li>"
        "<li><b>Malware:</b> virus (needs host program) · worm (standalone, no human) · "
        "Trojan (needs user interaction).</li>"
        "<li><b>Attacks (3):</b> reconnaissance (discover/map) · access (unauthorised "
        "manipulation — SSH 22/Telnet 23 pivots) · DoS/DDoS (consume resources; DDoS = zombies "
        "+ botnet + CnC).</li>"
        "<li><b>Mitigations:</b> defense-in-depth (VPN, ASA firewall, IPS, ESA/WSA, AAA "
        "server); regular validated offsite password-protected backups; patch/auto-update (worm "
        "fix); AAA = authenticate/authorize/account; firewalls between networks + DMZ + SPI; "
        "endpoint policies, antivirus, host IPS, NAC.</li>"
        "<li><b>Harden devices:</b> defaults inadequate → AutoSecure; change defaults; strong "
        "passwords (8+/10+, complex, no dictionary, change often) or passphrases; encrypt "
        "plaintext passwords, min length, brute-force deterrence, inactivity timeout; enable "
        "SSH (hostname → domain → RSA key ≥1024 → local user → login local → transport input "
        "ssh); disable unused services.</li>"
        "</ul>"
    ),
    "gaps": [
        "The <b>four access-attack types</b> (slide 13) are introduced in text but their four "
        "named categories appear only in a figure — the text instead gives SSH/Telnet and "
        "interception examples, which are used above.",
        "The <b>malware bullets</b> (slide 11) extract with mixed column order; only "
        "unambiguous, self-contained statements are quoted (worm = standalone/no human help; "
        "virus = inserts into another program; Trojan = user interaction required).",
        "The <b>physical-threat class labels</b> on slide 9 are cut in extraction — the four "
        "class names are quoted from the module summary (slide 35) instead, with examples "
        "from slide 9's fragments.",
        "Firewall <b>technique names</b> (slide 22) extract as fragments ('on port numbers', "
        "'keywords', SPI behaviour) — only SPI's described behaviour is defined above; check "
        "the slide for the full technique list.",
    ],
}
