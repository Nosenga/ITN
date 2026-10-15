# Revision kit content — Chapter 2: Configuring a Network OS
# Grounded in uploads/Chapter 2_ITN_Configuring a Network OS.pdf (slide refs = page numbers).

DATA = {
    "overview": (
        "Chapter 2 is about <b>getting hands-on with the device</b>: what a network operating "
        "system is, how the Cisco IOS CLI is reached and navigated, how to give a device an "
        "identity and lock it down (hostname, passwords, banners, encrypted password display), "
        "how configuration files are managed, and how devices are addressed — dotted-decimal "
        "IPv4 addressing, switch virtual interfaces (SVIs), automatic addressing and conflict "
        "handling — followed by connectivity testing. The chapter closes by stressing that "
        "routers and switches share the same modal, hierarchical CLI and the same initial "
        "configuration steps."
    ),
    "objectives": [
        "Explain what the Cisco IOS is, where it is stored and what it lets you configure "
        "(<a class=\"rev-link\" href=\"#p6\">slides 6–8</a>).",
        "Compare the CLI access methods — console, Telnet, SSH and AUX — and know when each "
        "works (<a class=\"rev-link\" href=\"#p9\">slides 9–11</a>).",
        "Navigate the modal IOS hierarchy and use its help, checking and shortcut keys "
        "(<a class=\"rev-link\" href=\"#p13\">slides 13–22</a>).",
        "Perform basic secure configuration: hostname, enable secret, console/VTY passwords, "
        "password encryption and banners (<a class=\"rev-link\" href=\"#p24\">slides 24–30</a>).",
        "Manage configuration files and address devices — SVI configuration, automatic "
        "addressing and testing connectivity "
        "(<a class=\"rev-link\" href=\"#p31\">slides 31–39</a>).",
    ],
    "concepts": [
        "<b>Cisco IOS</b> — the collection of network operating systems on Cisco devices; the "
        "course focuses on IOS Release 15.x.",
        "<b>Modal (hierarchical) CLI</b> — you must be in the right mode before a command "
        "works.",
        "<b>Out-of-band vs in-band access</b> — console/AUX vs Telnet/SSH over the network.",
        "<b>Configuration files</b> — running configuration vs startup configuration "
        "(reload / erase).",
        "<b>IPv4 dotted-decimal addressing</b> — address + subnet mask identify a device on an "
        "internetwork.",
        "<b>SVI</b> — a switch virtual interface gives a switch a logical (Layer 3) address.",
    ],
    "definitions": [
        {"t": "IOS", "abbr": "Internetwork Operating System",
         "d": "The network operating system used on Cisco devices; on home routers the "
              "equivalent is usually called <i>firmware</i>. It provides options to configure "
              "interfaces and enable routing and switching functions.", "r": 6},
        {"t": "CLI", "abbr": "Command-Line Interface",
         "d": "The primary way services on Cisco IOS devices are accessed; reached via the "
              "console port, the AUX port, Telnet or SSH.", "r": 40},
        {"t": "Console access",
         "d": "Direct connection with a special console cable; works even when no networking "
              "services are configured (<b>out-of-band</b>), so it should be password-protected "
              "and the device kept in a secure room.", "r": 10},
        {"t": "Telnet",
         "d": "Remote CLI access <b>over the network</b>; requires active networking services "
              "and one active, configured interface.", "r": 11},
        {"t": "SSH",
         "abbr": "Secure Shell",
         "d": "Remote login similar to Telnet but with stronger password authentication and "
              "<b>encryption when transporting data</b>.", "r": 11},
        {"t": "AUX port", "abbr": "auxiliary port",
         "d": "An out-of-band connection that uses a telephone line and can be used like a "
              "console port.", "r": 11},
        {"t": "Modal operating system",
         "d": "An OS where the technician must navigate through hierarchical modes before "
              "commands are accepted — routers and switches share this structure and many of "
              "the same commands.", "r": 40},
        {"t": "enable secret",
         "d": "The recommended command for securing Privileged EXEC mode because it "
              "<b>encrypts</b> the password; the older <code>enable password</code> should not "
              "be used.", "r": 27},
        {"t": "VTY lines",
         "d": "Virtual terminal lines that allow access to a device via Telnet; how many are "
              "supported varies by device and IOS version.", "r": 28},
        {"t": "Banner",
         "d": "A message shown to all connected terminals; an important part of the legal "
              "process if someone is prosecuted for breaking in — wording implying a login is "
              "'welcome' or 'invited' is not appropriate.", "r": 30},
        {"t": "SVI", "abbr": "Switch Virtual Interface",
         "d": "A logical interface on a switch (e.g. <code>interface VLAN 1</code>) to which "
              "an IP address and subnet mask are assigned so the switch can be managed on the "
              "network.", "r": 34},
        {"t": "Dotted decimal",
         "d": "The structure of an IPv4 address: four decimal numbers between 0 and 255 "
              "separated by dots; used together with a subnet mask.", "r": 33},
        {"t": "Subnet mask",
         "d": "Determined alongside the address; determines which part of a larger network is "
              "used by an IP address.", "r": 34},
        {"t": "IP address conflict",
         "d": "Two devices configured with the same IP address — the addressing problem the "
              "chapter warns against.", "r": 37},
        {"t": "Running / startup configuration",
         "d": "The active configuration kept in RAM versus the saved copy in NVRAM; the chapter "
              "shows saving it, <code>reload</code> (with 'System configuration has been "
              "modified. Save?'), <code>erase startup-config</code> and, on a switch, "
              "<code>delete vlan.dat</code>.", "r": 31},
    ],
    "explanations": [
        {"t": "Where the IOS lives and why it matters",
         "d": "The IOS is stored in <b>non-volatile storage (flash)</b> so it survives power "
              "loss, can hold multiple versions, and is <b>copied into RAM</b> to run. The "
              "amount of flash and RAM determines which IOS versions/feature sets a device can "
              "use.",
         "e": "Upgrading IOS = putting a newer image in flash; the router boots by loading "
              "from flash into RAM.",
         "r": 7},
        {"t": "Why console is 'out-of-band'",
         "d": "Out-of-band means the connection does <b>not rely on the network being "
              "configured</b> — even a device with no IP addresses at all can be reached "
              "through its console port with a console cable. Telnet and SSH are in-band: they "
              "need active networking services and one active, configured interface.",
         "e": "A brand-new switch with no IP can still be configured by plugging a console "
              "cable into it.",
         "r": 10},
        {"t": "Working with IOS help and shortcuts",
         "d": "The CLI gives <b>context-sensitive help</b> and syntax checking so you can "
              "discover commands as you go. Key shortcuts: <b>Tab</b> completes a partial "
              "command/keyword; <b>Ctrl-A</b> jumps to the start of the line; <b>Ctrl-R</b> "
              "redisplays it; <b>Ctrl-Z</b> exits configuration mode back to user EXEC; "
              "<b>Ctrl-C</b> aborts the current command; up/down arrows scroll through former "
              "commands; Ctrl-shift-6 interrupts an IOS process.",
         "e": "Type <code>sho</code> then Tab — IOS completes <code>show</code>.",
         "r": 21},
        {"t": "Securing access, layer by layer",
         "d": "Three separate protections: (1) <b>Privileged EXEC</b> is guarded with "
              "<code>enable secret</code> (encrypted — not the older <code>enable "
              "password</code>); (2) the <b>console port</b> is password-protected against "
              "physical access, and <b>VTY lines</b> guard remote Telnet/SSH sessions; (3) "
              "password display in the configuration is encrypted so viewers cannot read "
              "passwords — note that removing the encryption service later does <b>not</b> "
              "reverse existing encryption.",
         "e": "Anyone who can read <code>show running-config</code> should still see only "
              "encrypted password strings, not plain text.",
         "r": 29},
        {"t": "Giving a switch its IP address (SVI)",
         "d": "Switches and end devices need IPv4 addresses; addresses can be assigned to "
              "physical ports and virtual interfaces. On a switch you configure an SVI: "
              "<code>interface VLAN 1</code>, then <code>ip address 192.168.10.2 "
              "255.255.255.0</code>, then <code>no shutdown</code> to administratively enable "
              "the interface. Physical ports and VTY lines still need configuring for full "
              "reachability/remote management.",
         "e": "After the SVI has an address, the switch itself can be pinged/managed from a "
              "host on that network.",
         "r": 34},
        {"t": "Hostname rules",
         "d": "Naming devices matters because unnamed devices are hard to identify for "
              "configuration. The guidelines: start with a letter; no spaces; end with a letter "
              "or digit; only letters, digits and dashes; under 64 characters.",
         "e": "<code>Branch-SW1</code> fits every rule; <code>branch sw 1</code> breaks three "
              "of them.",
         "r": 24},
    ],
    "comparisons": [
        {"t": "Console vs Telnet/SSH (access methods)",
         "cols": ["Aspect", "Console", "Telnet / SSH"],
         "rows": [
             ["Band", "Out-of-band — no networking services required",
              "In-band — over the network"],
             ["Prerequisites", "Special console cable; device reachable even unconfigured",
              "Active networking services and one active, configured interface"],
             ["Typical use", "Initial configuration; rescue when network is down",
              "Day-to-day remote management"],
             ["Security note", "Physically secure the device/room",
              "SSH preferred: authentication + encryption"],
         ],
         "note": "AUX is also out-of-band (telephone line), used like a console port.",
         "refs": [9, 10, 11]},
        {"t": "Telnet vs SSH",
         "cols": ["Aspect", "Telnet", "SSH"],
         "rows": [
             ["Purpose", "Remote CLI login over the network", "Remote CLI login over the network"],
             ["Security", "No encryption of transported data mentioned — basic remote login",
              "Stronger password authentication"],
             ["Data protection", "Data sent in clear as far as the chapter's contrast implies",
              "<b>Uses encryption when transporting data</b>"],
             ["Chapter verdict", "Older method", "Similar to Telnet, but more secure"],
         ],
         "note": "Both require active networking services and a configured interface.",
         "refs": [11]},
    ],
    "facts": [
        {"d": "The course's primary focus is <b>Cisco IOS Release 15.x</b>; every networking "
              "device comes with a default IOS that can be upgraded (version or feature set).",
         "r": 6},
        {"d": "IOS is kept in <b>non-volatile storage (flash)</b> and <b>copied to RAM</b> to "
              "run; flash/RAM quantity determines usable IOS.", "r": 7},
        {"d": "CLI access methods: <b>Console, Telnet or SSH, AUX</b>.", "r": 9},
        {"d": "Terminal emulation programs named: <b>PuTTY, Tera Term, SecureCRT, "
              "HyperTerminal, OS X Terminal</b>.", "r": 12},
        {"d": "Shortcut keys: Tab (complete), Ctrl-R (redisplay), Ctrl-A (line start), Ctrl-Z "
              "(exit config mode), Ctrl-C (abort), arrows (command history), Ctrl-shift-6 "
              "(interrupt process).", "r": 21},
        {"d": "<b><code>show version</code></b> displays the IOS version and related device "
              "information.", "r": 22},
        {"d": "Hostname rules: starts with a letter, no spaces, ends with letter/digit, only "
              "letters/digits/dashes, fewer than 64 characters.", "r": 24},
        {"d": "Use <b><code>enable secret</code></b>, not <code>enable password</code> — "
              "enable secret provides greater security because the password is encrypted.",
         "r": 27},
        {"d": "Console must be secured (physical plug-in risk); <b>VTY lines</b> allow Telnet "
              "access; count varies by device/IOS version.", "r": 28},
        {"d": "Password encryption in the configuration is <b>one-way</b>: removing the "
              "encryption service does not reverse the encryption.", "r": 29},
        {"d": "Config file operations: <code>reload</code> asks 'System configuration has been "
              "modified. Save? [yes/no]'; <code>erase startup-config</code> removes the startup "
              "config; switches also need <code>delete vlan.dat</code>.", "r": 31},
        {"d": "IPv4 addresses are <b>dotted decimal — four numbers 0–255</b> — and are always "
              "used with a <b>subnet mask</b>; addresses can go on physical ports and virtual "
              "interfaces.", "r": 33},
        {"d": "SVI configuration pattern: <code>interface VLAN 1</code> → <code>ip address "
              "192.168.10.2 255.255.255.0</code> → <code>no shutdown</code> (administratively "
              "enables the interface).", "r": 34},
        {"d": "Routers and switches share the <b>same modal operating system structure, command "
              "structures and many commands</b>, with identical initial configuration steps.",
         "r": 40},
    ],
    "questions": [
        {"type": "mc",
         "q": "Which CLI access method works even when the device has no networking services "
              "configured?",
         "opts": ["Telnet", "SSH", "Console", "AUX over IP"],
         "a": "C — Console",
         "why": "Console access is out-of-band: the device is accessible even if no networking "
                "services have been configured, using a special console cable (slide 10)."},
        {"type": "tf",
         "q": "For securing Privileged EXEC access mode, the chapter says to use the older "
              "<code>enable password</code> command rather than <code>enable secret</code>.",
         "a": "False",
         "why": "The opposite: use <code>enable secret</code>, not the older "
                "<code>enable password</code>, because enable secret provides greater security "
                "— the password is encrypted (slide 27)."},
        {"type": "short",
         "q": "List the hostname guidelines given in the chapter (any four).",
         "a": "Start with a letter; contain no spaces; end with a letter or digit; use only "
              "letters, digits and dashes; be less than 64 characters long.",
         "why": "Slide 24 lists exactly these — and notes that devices without names are "
                "difficult to identify for configuration purposes."},
        {"type": "mc",
         "q": "What does the <code>no shutdown</code> command do in the SVI configuration?",
         "opts": ["Saves the running configuration",
                  "Administratively enables the interface",
                  "Restarts the switch",
                  "Encrypts all passwords"],
         "a": "B — Administratively enables the interface",
         "why": "Slide 34: after <code>ip address …</code>, <code>no shutdown</code> "
                "administratively enables the interface (the switch still needs physical "
                "ports configured and VTY lines for remote management)."},
        {"type": "short",
         "q": "Where is the IOS stored, and where does it run from?",
         "a": "Stored in non-volatile storage (flash); copied into volatile RAM to run. Flash "
              "and RAM sizes determine which IOS can be used.",
         "why": "Slide 7: non-volatile storage keeps it when power is lost; it can hold "
                "multiple versions and is copied from flash to RAM."},
        {"type": "explain",
         "q": "Explain why the banner message matters legally, and what kind of wording is "
              "inappropriate.",
         "a": "The banner is displayed to all connected terminals and is an important part of "
              "the legal process if someone is prosecuted for breaking into the device. "
              "Wording that implies a login is 'welcome' or 'invited' is not appropriate.",
         "why": "Slide 30 states both points directly."},
        {"type": "tf",
         "q": "SSH provides stronger password authentication and encrypts data in transit, "
              "while Telnet does not encrypt the transported data.",
         "a": "True",
         "why": "Slide 11: SSH is 'similar to Telnet, but utilizes more security — stronger "
                "password authentication, uses encryption when transporting data'."},
        {"type": "explain",
         "q": "A student runs the command that disables the encryption service after seeing "
              "encrypted passwords in <code>running-config</code>, expecting the plain-text "
              "passwords to come back. Why is this wrong?",
         "a": "Because once applied, removing the encryption service does not reverse the "
              "encryption — the stored passwords remain encrypted.",
         "why": "Slide 29 states this explicitly; the encryption of existing entries is "
                "one-way."},
    ],
    "misunderstandings": [
        {"t": "<code>enable password</code> vs <code>enable secret</code>",
         "d": "Both guard Privileged EXEC, but only <code>enable secret</code> <b>encrypts</b> "
              "the password. The chapter explicitly says to use enable secret and avoid the "
              "older enable password (slide 27)."},
        {"t": "\"Remote access works without configuration\"",
         "d": "Telnet/SSH are <b>in-band</b>: they need active networking services and an "
              "active, configured interface. Only console/AUX are out-of-band and available "
              "on an unconfigured device (slides 10–11)."},
        {"t": "Turning off password encryption reveals plain-text passwords",
         "d": "No — removing the encryption service does <b>not reverse</b> encryption already "
              "applied; passwords stay encrypted (slide 29)."},
        {"t": "Configuring only the SVI is enough for a switch",
         "d": "The SVI gives the switch an address, but the chapter notes the switch "
              "<i>still needs</i> physical ports configured and VTY lines set to enable remote "
              "management (slide 34)."},
    ],
    "quick": (
        "<ul>"
        "<li><b>IOS:</b> network OS for Cisco devices (focus: Release 15.x); stored in flash, "
        "runs from RAM; configure interfaces, enable routing/switching.</li>"
        "<li><b>Reach the CLI:</b> console (out-of-band, works unconfigured), Telnet/SSH "
        "(in-band, need configured interface; SSH = stronger auth + encryption), AUX "
        "(telephone line, out-of-band). Tools: PuTTY, Tera Term, SecureCRT, HyperTerminal.</li>"
        "<li><b>Modes:</b> modal, hierarchical — routers and switches share the same structure "
        "and initial configuration steps; context-sensitive help, syntax check, Tab/arrow "
        "shortcuts; <code>show version</code> for versions.</li>"
        "<li><b>Basic config:</b> hostname (letter start, no spaces, letters/digits/dashes, "
        "&lt;64 chars) → secure with <code>enable secret</code> (not enable password), console "
        "password, VTY passwords, encrypt password display (irreversible), set a legal banner "
        "(never 'welcome').</li>"
        "<li><b>Config files:</b> save before <code>reload</code>; <code>erase "
        "startup-config</code> (+ <code>delete vlan.dat</code> on switches) clears saved "
        "config.</li>"
        "<li><b>Addressing:</b> IPv4 = dotted decimal (4 × 0–255) + subnet mask; switch gets "
        "an IP via SVI: <code>interface VLAN 1</code> → <code>ip address …</code> → "
        "<code>no shutdown</code>; avoid address conflicts; test connectivity.</li>"
        "</ul>"
    ),
    "gaps": [
        "Slides on <b>IOS modes and command structure (slides 14–20)</b> and the <b>access/"
        "verification steps (slides 36–39)</b> present much of their detail (mode diagrams, "
        "command syntax parts, DHCP steps, test commands) as figures/animations without "
        "extractable text — review those slides in place for the exact keystrokes; the facts "
        "above only quote what the source text states.",
        "The homework slide lists lab references (2.1.4.6, 2.2.2.5, 2.3.2.4, 2.3.2.5, "
        "2.4.1.1, 2.4.1.2) but no instructions — no lab steps are reproduced here because the "
        "source gives none beyond those titles.",
    ],
}
