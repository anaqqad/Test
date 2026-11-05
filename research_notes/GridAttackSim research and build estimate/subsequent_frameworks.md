# Follow-up frameworks by the GridAttackSim authors (Le, Anwar, Loke, Beuran, Tan) and JAIST/Deakin collaborators after 2020

Method note (applies to all sections): papers were verified via Crossref metadata (api.crossref.org) and publisher/repository pages. Source code was inspected by shallow-cloning each public GitHub repository on 2026-11-05 and reading README, CHANGES, CONTRIBUTORS, requirements and key source files. "Size" means the working tree without `.git`; "py lines" means the total lines of all `.py` files, which I counted myself. Commit dates come from `git log`. The GitHub REST API was not available in this session, so star and fork counts are not given. Two org listings were read from GitHub web pages: [crond-jaist repositories](https://github.com/orgs/crond-jaist/repositories) and [cyb3rlab repositories](https://github.com/orgs/cyb3rlab/repositories). Labels used below: **Verified** = seen in a primary source or in the code. **Interpretation** = my reading. **Unknown** = not found.

Context on the lab structure: JAIST's CROND NEC-endowed chair, which built GridAttackSim and CyRIS, "ceased to exist in March 2021". Development moved to the JAIST Cybersecurity Research Lab (Beuran lab) under the GitHub org `cyb3rlab`. The older `crond-jaist` repos carry a notice that they will get no further updates ([crond-jaist/cyris README](https://github.com/crond-jaist/cyris); [crond-jaist/cytrone README](https://github.com/crond-jaist/cytrone)).

## Q1. GridAttackAnalyzer (2022): what it is, how it is built, what the code actually does

### Takeaway
GridAttackAnalyzer is real and published: T. D. Le, M. Ge, A. Anwar, S. W. Loke, R. Beuran, R. Doss, Y. Tan, *Sensors* 22(13):4795, 2022, DOI 10.3390/s22134795. It is **not a simulator**. It is a Tkinter desktop tool that builds HARM attack graphs and attack trees from CVSS v2 data and computes static security metrics. Power-grid GLM files are only parsed into a topology graph; GridLAB-D is never run. The code (BSD-3, about 3.5k lines of Python) was released in 2021, before the journal paper, and has not been developed since February 2022.

### Cited Findings
- **Bibliographic (verified):** "GridAttackAnalyzer: A Cyber Attack Analysis Framework for Smart Grids". Authors: Tan Duy Le, Mengmeng Ge, Adnan Anwar, Seng W. Loke, Razvan Beuran, Robin Doss, Yasuo Tan. Published in *Sensors* (MDPI), 2022, DOI 10.3390/s22134795 — [Crossref](https://api.crossref.org/works/10.3390%2FS22134795); [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC9268941/); [DBLP record](https://dblp.org/rec/journals/sensors/LeGALBDT22).
- **Precursor (verified):** T. D. Le, M. Ge, P. T. Duy, H. D. Hoang, A. Anwar, S. W. Loke, R. Beuran, Y. Tan, "CVSS Based Attack Analysis Using a Graphical Security Model: Review and Smart Grid Case Study", SGIoT 2020, LNICST, DOI 10.1007/978-3-030-69514-9_11. The README cites this paper and does not cite the Sensors paper — [Crossref query](https://api.crossref.org/works?query.author=Razvan+Beuran&filter=from-pub-date:2021-01-01); [GridAttackAnalyzer README](https://github.com/crond-jaist/GridAttackAnalyzer).
- **(1) Problem (verified):** The paper says "It would be challenging to build a real smart grid system for cybersecurity experimentation and validation purposes". It proposes analytical attack modelling with graphical security models plus real vulnerability (CVE/CVSS) data as the alternative — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9268941/).
- **(2) Architecture (verified, README):** Smart Grid Model, Database (devices and vulnerabilities), Attack Scenarios (entry points, targets, vulnerabilities), Database Manager, Attack Analysis Manager, Attack Model Generator, and Attack Model Evaluator (attack graph plus security metrics) — [README](https://github.com/crond-jaist/GridAttackAnalyzer).
- **(2) Architecture, actual code (verified by me):**
  - `GridAttackAnalyzer.py` (923 lines) is a Tkinter GUI. It shells out with `os.system` to `Scripts/NetGen.py`, `glmMap.py` and `plotMetrics.py`, and opens results with `libreoffice` and `firefox`.
  - `Scripts/` holds `AttackGraph.py`, `AttackTree.py`, `Harm.py` (HARM = attack graph upper layer plus attack tree lower layer), `SecurityEvaluator.py` (401 lines), `NetGen.py` (648 lines), `Network.py`, `Node.py`, `Vulnerability.py` and `glmMap.py` (converts GLM to a graph).
  - The attack library is `database.json`, which maps devices to CVE lists with "CVSS_Base_Score_2.0", "Impact_Subscore" and "Exploitability_Subscore".
  - Total: 3,498 lines of Python, 29 files, about 3.0 MB — [repo](https://github.com/crond-jaist/GridAttackAnalyzer); [developer_guide.md](https://github.com/crond-jaist/GridAttackAnalyzer/blob/master/developer_guide.md).
- **(3) Technologies (verified):**
  - Python 3, Tkinter, graphviz, numpy==1.14.6, pyvis, pandas and matplotlib (`requirements.txt`).
  - Tested on Ubuntu 18.04.
  - GLM feeder files are included: IEEE_4_Node, IEEE_13_Node and R4-12.47-2 — [repo](https://github.com/crond-jaist/GridAttackAnalyzer).
- **(4) Simulation/emulation (verified absence):** No call to `gridlabd`, ns-3 or FNCS anywhere in the code. The only external processes are the Python helper scripts, LibreOffice and Firefox (my grep of `os.system` and `subprocess`). Interpretation: this is analytical attack-graph analysis, not co-simulation — [repo](https://github.com/crond-jaist/GridAttackAnalyzer).
- **(5) Attack scenarios:**
  - Only multi-step vulnerability exploitation through CVEs on IoT and smart-grid devices, from user-chosen entry points to targets.
  - The paper's five case-study scenarios: single-type multiple-entry; multi-type; with patches applied; multiple-target attack on EMS/DRP; and attacks starting from substation local terminals.
  - The case study uses the PNNL R4-12.47-2 feeder (352 houses) and a HAN/NAN/WAN network with gateway, smart meter, concentrator, FEP, SCADA, ICCP and EMS/DRP.
  - The paper says only vulnerability-exploitation attacks are modelled, unlike GridAttackSim's jamming, DNS and injection attacks — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9268941/).
  - The repo claims "three smart grid models, more than 20 types of smart grid devices, and 40 types of vulnerabilities" — [CHANGES/README](https://github.com/crond-jaist/GridAttackAnalyzer).
- **Metrics (verified):**
  - Attack success probability, attack cost, attack impact and attack risk at node, path and network level, plus return on attack.
  - Number of paths (NP), mean path length (MPL) and mode path length (MoPL); these functions are in `SecurityEvaluator.py`.
  - Paths are banded by likelihood: almost certain, likely, possible, unlikely, rare — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9268941/); [SecurityEvaluator.py](https://github.com/crond-jaist/GridAttackAnalyzer/blob/master/Scripts/SecurityEvaluator.py).
- **(6) GUI (verified):** Yes, Tkinter. The workflow is: select model, smart meter connection, CVEs and devices, then "Generate File", optional manual edit, "Run", and view the attack graph (pyvis HTML) and metrics plots — [README](https://github.com/crond-jaist/GridAttackAnalyzer).
- **User study (verified):** 10 cybersecurity PhD candidates (5 from JAIST, 5 external). All reproduced the case study. SUS mean was 72.2 (SD 10.2, range 60–90) — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9268941/).
- **(7) Automated scenario generation:**
  - Partial. `NetGen.py` automatically generates the IoT network, attack-analysis file and HARM from GUI selections.
  - There is no generation of novel attack scenarios; entry points and targets are chosen by the user — [developer_guide.md](https://github.com/crond-jaist/GridAttackAnalyzer/blob/master/developer_guide.md).
- **(8) Source code (verified):** https://github.com/crond-jaist/GridAttackAnalyzer
  - License: BSD 3-Clause, © 2021 JAIST.
  - Language: Python.
  - Only release tag: `1.0`.
  - First commit 2021-03-12. Last commit 2022-02-15 ("Updated license text to have it recognized by GitHub").
  - 10 commits; 3.0 MB.
  - CONTRIBUTORS: Tan Duy Le (main developer), Mengmeng Ge (revised the AG/AT/HARM implementation), Jin B. Hong (initial AG/AT/HARM). Maintainer: Razvan Beuran — [repo](https://github.com/crond-jaist/GridAttackAnalyzer).
- **(9) Improvements over GridAttackSim (verified plus interpretation):**
  - GridAttackSim is a GridLAB-D/ns-3/FNCS co-simulation of attacks such as jamming, DNS and injection; it is 1,059 lines of Python plus GLM and ns-3 C++.
  - GridAttackAnalyzer adds CVE/CVSS-based attack-path enumeration, HARM models, quantitative risk metrics, extensible device and vulnerability databases, and a user study.
  - It drops physical simulation entirely — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9268941/); [GridAttackSim repo](https://github.com/crond-jaist/GridAttackSim).
  - The two tools were later presented together as a "general smart grid cybersecurity architecture implemented in two systems" in T. D. Le, H. P. T. Nguyen, K.-T. Huynh, R. Beuran, "Smart Grid Cyber-Attack Analysis and Countermeasures", RIVF 2022, pp. 590–595, DOI 10.1109/RIVF55975.2022.10013873 — [Crossref](https://api.crossref.org/works/10.1109%2FRIVF55975.2022.10013873); [author PDF](https://www.jaist.ac.jp/~razvan/publications/smart_grid_attack_analysis_countermeasures.pdf).
- **GitHub metadata quirk:** GitHub's language detector labels GridAttackSim "Zimpl" — [crond-jaist org page](https://github.com/orgs/crond-jaist/repositories). Interpretation: this is a misclassification caused by the many `.glm`, `.player` and ns-3 files; the repo is Python plus ns-3 C++ plus GridLAB-D models.

### Inferences
- **(10) Reusable parts:**
  - The HARM attack-graph and attack-tree engine with path metrics: `AttackGraph.py`, `AttackTree.py`, `Harm.py`, `SecurityEvaluator.py`.
  - The device→CVE→CVSS JSON schema.
  - The GLM→graph mapper (`glmMap.py`).
  - Together these can serve as a "planning/risk layer" that picks attack paths, which a next-generation simulator then executes against a co-simulated grid.
  - Caveats: the code uses CVSS v2 only, pins numpy 1.14.6, uses Tkinter and shell-outs, and has had no maintenance since 2022. Expect a rewrite rather than a direct import.
- The natural next step was never published as a framework: feeding GridAttackAnalyzer's attack paths into GridAttackSim's co-simulation to compute physical impact. That gap is an opportunity.

### Gaps
- I did not find a GitHub link in the part of the Sensors article I read (its ref. [43] was truncated). The repo is clearly the same tool, given the same authors, description and contributors.
- No later GridAttackAnalyzer or GridAttackSim version, journal extension, or fork from these authors was found after 2022. Tan Duy Le's Crossref-indexed output from 2023 to 2026 moves to other topics (elderly-care smart homes, LLM task allocation, traffic forecasting) — [Crossref query](https://api.crossref.org/works?query.author=Tan+Duy+Le+Anwar&filter=from-pub-date:2021-01-01).

## Q2. PenGym: RL pentesting agents trained in real environments (NASim + CyRIS)

### Takeaway
PenGym is real, but the journal year is 2025 (volume 148, January 2025), and it was published online in 2024. The paper is H. P. T. Nguyen, K. Hasegawa, K. Fukushima, R. Beuran, "PenGym: Realistic training environment for reinforcement learning pentesting agents", *Computers & Security* 148:104140, DOI 10.1016/j.cose.2024.104140. A conference version appeared at ICISSP 2024. The code at github.com/cyb3rlab/PenGym (BSD-3, about 3.8k lines of Python) implements a Gymnasium/NASim-compatible environment. Its actions are real nmap and Metasploit (pymetasploit3) operations against KVM VMs built by CyRIS. The repo ships only random and deterministic demo agents, not the RL training code.

### Cited Findings
- **Bibliographic (verified):**
  - Journal: *Computers & Security*, vol. 148, 2025, article 104140, DOI 10.1016/j.cose.2024.104140, issue date 2025-01 — [Crossref](https://api.crossref.org/works/10.1016/j.cose.2024.104140).
  - Conference: T. Nguyen, Z. Chen, K. Hasegawa, K. Fukushima, R. Beuran, "PenGym: Pentesting Training Framework for Reinforcement Learning Agents", ICISSP 2024, pp. 498–509, DOI 10.5220/0012367300003648 — [SciTePress](https://www.scitepress.org/PublishedPapers/2024/123673).
  - A JAIST press release accompanied the journal paper — [EurekAlert](https://www.eurekalert.org/news-releases/1061846); [AlphaGalileo](https://alphagalileo.org/Item-Display/ItemId/251219).
  - A JAIST thesis version exists — [JAIST DSpace abstract](https://dspace.jaist.ac.jp/dspace/bitstream/10119/19357/4/abstract.pdf).
- **(1) Problem:** RL pentesting agents are usually trained in abstract simulators such as NASim and transfer poorly to real networks. PenGym provides training environments with actual hosts and vulnerabilities — [ICISSP paper](https://www.scitepress.org/Papers/2024/123673/123673.pdf); [README](https://github.com/cyb3rlab/PenGym).
- **(2) Architecture (verified, README and code):**
  - The core is the **Action/State Module**. It (i) converts the RL agent's actions into real actions in a cyber range, and (ii) interprets outcomes into state and reward.
  - **CyRIS** creates the cyber range from **RangeDB** descriptions.
  - The API is the same as Gymnasium, so any Gym-compliant agent can be used — [README](https://github.com/cyb3rlab/PenGym).
  - Code layout:
    - `pengym/envs/host_vector.py` (1,286 lines): actions `do_service_scan`, `do_os_scan`, `do_exploit`, `do_e_ssh`, `do_e_http`, `do_e_ftp`, `do_e_samba`, `do_e_smtp`, `do_process_scan`, `do_privilege_escalation`, `do_pe_proftpd`, `do_pe_cron`, `do_pe_pkexec`.
    - `pengym/envs/network.py` (302 lines): overrides NASim traffic-permission logic.
    - `pengym/utilities.py` (703 lines): host and bridge maps, firewall restore.
    - `pengym/cyber_range_creation/range_description_creation.py` (519 lines) and `firewall_script_creation.py` (327 lines): auto-generate the CyRIS YAML and firewall scripts from a PenGym/NASim scenario.
    - `pengym/envs/scripts/*.exp`: expect scripts for firewall and gateway changes inside VMs.
    - `database/scenarios/*.yml`: tiny, tiny-small, tiny-hard, small-linear, small-honeypot, medium, medium-single-site, medium-multi-site — [repo](https://github.com/cyb3rlab/PenGym).
- **(3) Technologies (verified):**
  - Python 3; NASim (pip `nasim`, which pulls in gymnasium); python-nmap with nmap; Metasploit via `msfrpcd` and `pymetasploit3`; tkinter.
  - CyRIS on KVM; guest VMs must be Ubuntu 20.04.
  - Vulnerable service packages: vsftpd-2.3.4, proftpd-1.3.3, samba-4.5.9, opensmtpd-6.6.1p1, httpd-2.4.49 — [README](https://github.com/cyb3rlab/PenGym).
- **(4) Simulation/emulation:**
  - Dual mode: real execution in the cyber range, and/or NASim simulation (`-n` enables NASim simulation, `-d` disables cyber-range execution).
  - The CHANGES file says v0.2 fixed NASim logical-simulation issues (NASim upstream issues 45–47) — [README/CHANGES](https://github.com/cyb3rlab/PenGym).
  - The thesis reports that agents trained in original NASim did poorly in the real environment, while PenGym-trained agents reached the goal in all trials. A revised NASim performed comparably — [JAIST thesis abstract](https://dspace.jaist.ac.jp/dspace/bitstream/10119/19357/4/abstract.pdf).
- **(5) Attack actions:** OS scan, service scan, process scan, subnet scan, exploits against ssh/ftp/http/samba/smtp, and privilege escalation via proftpd, cron or pkexec. Firewalls and segments are multi-subnet, with up to the "medium-multi-site" scenario. IT-only; no CPS or ICS protocols — [repo](https://github.com/cyb3rlab/PenGym).
- **(6) GUI:** None; CLI only (`run.py`) — [README](https://github.com/cyb3rlab/PenGym).
- **(7) Automated scenario generation:**
  - Yes for **range generation**: a PenGym/NASim scenario YAML is turned into a CyRIS description plus firewall scripts automatically (v0.2).
  - Attack scenarios themselves are the NASim-derived YAMLs; there is no generator of new topologies — [CHANGES](https://github.com/cyb3rlab/PenGym).
- **RL code (verified absence):** `run.py` supports only `--agent_type random/deterministic`. The deterministic agent replays a 16-step path for `medium-multi-site`. No DQN/PPO, torch or stable-baselines code is in the repo (my grep). The RL agents evaluated in the papers are therefore not included — [run.py](https://github.com/cyb3rlab/PenGym/blob/main/run.py).
- **(8) Source code (verified):** https://github.com/cyb3rlab/PenGym
  - License: BSD 3-Clause, © 2023 JAIST and KDDI Research.
  - Language: Python plus bash and expect.
  - First commit 2023-07-28. Last commit 2024-12-19 ("Update LICENSE to be recognized by GitHub").
  - 29 commits; 772 KB; 3,805 lines of Python.
  - Git tags show only `0.1`, but CHANGES documents v0.2.
  - Contributors: H. P. T. Nguyen, R. Beuran, Zhi Chen, Kento Hasegawa and Kazuhide Fukushima (KDDI Research) — [repo](https://github.com/cyb3rlab/PenGym).
  - Third-party fork: [blocksek/pengym](https://github.com/blocksek/pengym).
- **(9) Improvements:**
  - Over AutoPentest-DRL (2021; MulVAL attack graph → DQN → optional nmap/Metasploit execution; 1,126 lines of Python): PenGym makes the real environment the *training* environment, not just the execution target. It is Gym-API-compatible and builds the range automatically from scenario files — [AutoPentest-DRL README](https://github.com/crond-jaist/AutoPentest-DRL).
  - Over NASim: realism, and it fixes NASim's modelling bugs.
  - Reported result (secondary source): PenGym-trained agents needed 7.72 steps on average versus 11.95 for simulation-trained agents. This figure came from a search-engine summary and I did not verify it in the paper.

### Inferences
- **(10) Reusable parts:**
  - The **pattern** is the most valuable piece: a Gymnasium environment whose abstract actions are bound to real tool executions, with a mapping from simulated host IDs to real IPs and a reset mechanism (firewall/gateway restore).
  - The scenario→CyRIS range compiler.
  - For a CPS attack simulator, the action set would need OT actions (Modbus/DNP3/IEC 61850/MQTT read-write, PLC logic changes) and a physical-process reward from a power or building simulator. PenGym provides none of that.

### Gaps
- Exact algorithms, hyperparameters and performance figures from the C&S journal paper were not read; ScienceDirect blocked fetching.
- The 7.72 vs 11.95 step figure is unverified, as noted above.

## Q3. SBCSE: Smart Building Control System Emulator (2024 conference, 2026 journal)

### Takeaway
SBCSE is verified in two versions:
- Conference: X. Weng, R. Beuran, IEEE PRDC 2024, pp. 220–223, DOI 10.1109/PRDC63035.2024.00041.
- Journal: X. Weng, R. Beuran, Y. Tan, "SBCSE: Emulation platform for smart building control system security testing", *International Journal of Critical Infrastructure Protection* vol. 53, 2026, article 100852, DOI 10.1016/j.ijcip.2026.100852.

The code (github.com/cyb3rlab/SBCSE, BSD-3, about 10.1k lines of Python, last commit 2026-05-29) emulates an MQTT-based building control system: BOS, RPF robot platform, robots, elevators and broker. It was built from a real building's logs. It has a Kivy GUI, YAML scenarios, MITM/DDoS/BAC attacks with countermeasures, network-fault injection, Atheris fuzzing and Maude formal verification. Inspection shows that some attacks are partly *modelled* (state machines that assume success) rather than executed at the network level.

### Cited Findings
- **Bibliographic (verified):**
  - Journal: IJCIP vol. 53, article 100852, published July 2026, authors Xiaoqi Weng, Razvan Beuran, Yasuo Tan — [Crossref](https://api.crossref.org/works/10.1016/j.ijcip.2026.100852).
  - Conference: PRDC 2024 — [Crossref query](https://api.crossref.org/works?query.author=Razvan+Beuran&filter=from-pub-date:2021-01-01); [author PDF](https://www.jaist.ac.jp/~razvan/publications/smart_building_control_system_emulation.pdf).
  - Master's theses: X. Weng (2025), http://hdl.handle.net/10119/19784, and J. Wu, "Formal and Experimental Verification of Robot Control Protocols for Smart Buildings" (2025), http://hdl.handle.net/10119/19793 — [SBCSE README](https://github.com/cyb3rlab/SBCSE); [JAIST DSpace abstract](https://dspace.jaist.ac.jp/dspace/bitstream/10119/19784/4/abstract.pdf).
- **(1) Problem (verified):** Evaluating smart building control technologies in real buildings is "costly, risky, and resource constrained". Existing simulators (Open-SBS, HVAC energy simulators) do not integrate building operating systems with IoT devices or robots. SBCSE targets threat analysis and countermeasure validation — [PRDC paper](https://www.jaist.ac.jp/~razvan/publications/smart_building_control_system_emulation.pdf).
- **(2) Architecture (verified, paper and code):**
  - Emulated components: BOS (building OS), MQTT-Broker, ELV (elevators), ROB (autonomous robots), RPF (external robot platform). The design came from "a smart building prototype from a certain construction company" and its communication and robot-trajectory logs.
  - Modules and their directories:
    - Network Communication Module: `mqtt_communication_module/`, with per-component message handlers (`bosmsghandler.py`, `elvmsghandler.py`, `robmsghandler.py`, `rpfmsghandler.py`), an Authenticator, TLS `certs`, `network_disturb.py`, `load_scalability.py` and `cpu_monitor.py`.
    - Device Motion Module: `device_motion_module/elevator.py`, `servicerobot.py`, `routes`.
    - RPF Control Protocol Module: `control_protocol/rcp.py` (automaton-based).
    - Utilities: `utils/`, including time acceleration in `timesim.py`.
    - Simulator Modules: `simulator/bossim.py`, `elvsim.py`, `robsim.py`, `rpfsim.py`.
    - Security Attack Module: `security_attack_module/` with `MITM.py`, `DDoS.py`, `BAC/` and `scene_switcher.py`.
    - User Interface: `interface.py` plus `interface/layout.kv`.
  - Sources: [repo](https://github.com/cyb3rlab/SBCSE); [PRDC paper](https://www.jaist.ac.jp/~razvan/publications/smart_building_control_system_emulation.pdf).
- **(3) Technologies (verified):** Python, paho-mqtt with a Mosquitto broker, MQTT and MQTTS (TLS), Kivy GUI, PyYAML, SQLAlchemy plus bcrypt (user management for BAC), psutil, numpy and scipy. Fuzzing uses Google Atheris (libFuzzer) and optionally Coverage.py. Formal verification uses Maude (`formal_verification/*.maude`: MQTT.maude, config.maude, utils.maude) — [README](https://github.com/cyb3rlab/SBCSE); [docs/fuzzing.md](https://github.com/cyb3rlab/SBCSE/blob/main/docs/fuzzing.md).
- **(4) Simulation/emulation (verified plus interpretation):**
  - Real MQTT messaging runs over a real broker between software components. Device motion (robots, elevators) is simulated, with time acceleration (`sim_speed`).
  - Validation compared SBCSE communication flows with the real building logs (elevator–BOS–RPF) and found them matching — [PRDC paper](https://www.jaist.ac.jp/~razvan/publications/smart_building_control_system_emulation.pdf).
  - 2025–2026 commits added network disturbance (fault) injection with one-way delay and loss, scalability and load tests, and improved experiment logging — [git history](https://github.com/cyb3rlab/SBCSE/commits).
  - Interpretation: this is a protocol-level emulation of a building control plane, not a physical (thermal/energy) building simulation.
- **(5) Attacks (verified):**
  - Implemented attacks: MITM (target BOS or RPF), DDoS against the MQTT broker (connection flooding "C" or publish flooding "P"), and Broken Access Control (BOS or RPF).
  - Countermeasures: MQTTS/TLS against MITM, plus authentication and access control.
  - Malware and social-engineering scenarios were designed but are "not possible at this time" because there is no human simulation module — [docs/security_testing.md](https://github.com/cyb3rlab/SBCSE/blob/main/docs/security_testing.md); [CHANGES](https://github.com/cyb3rlab/SBCSE/blob/main/CHANGES).
- **Implementation depth (verified by reading code):**
  - `MITM.py` is a state machine. Its scan and listen steps are marked "Assuming success", and it fails only if the protocol is MQTTS. It does not perform ARP spoofing or real interception.
  - `DDoS.py` uses real paho-mqtt botnet clients against the broker.
  - Interpretation: attack *effects* are partly scripted, so realism varies by attack — [MITM.py](https://github.com/cyb3rlab/SBCSE/blob/main/security_attack_module/MITM.py); [DDoS.py](https://github.com/cyb3rlab/SBCSE/blob/main/security_attack_module/DDoS.py).
- **(6) GUI (verified):** Yes, Kivy. It configures protocols, robots, elevators, attacks and targets, and shows logs — [README](https://github.com/cyb3rlab/SBCSE).
- **(7) Automated scenario generation (verified, limited):**
  - `utils/testyaml.py`, added 2026-05-29, generates scenario YAMLs with N robots and tasks for load and scalability tests.
  - `fuzzer/fuzzing_utils.py` has `generate_scenario(seed)` for fuzzing.
  - There is no automated *attack*-scenario generation; attacks are selected manually in YAML or the GUI — [commit caa462c](https://github.com/cyb3rlab/SBCSE/commit/caa462c3190e006bfc49b1bbb0d254b9524b8fa1).
- **(8) Source code (verified):** https://github.com/cyb3rlab/SBCSE
  - License: BSD 3-Clause, © 2025 JAIST.
  - Language: Python.
  - No git tags, but CHANGES documents v1.0.
  - First commit 2025-05-23. Last commit 2026-05-29.
  - 28 commits, all by `rzvnbr` (Beuran); 2.7 MB; 135 files; 10,112 lines of Python.
  - Contributors: Xiaoqi Weng, Jingting Wu, Razvan Beuran — [repo](https://github.com/cyb3rlab/SBCSE).
- **(9) Improvements (interpretation):**
  - Compared with GridAttackSim/Analyzer, SBCSE is the lab's first *emulation* of a real CPS control plane derived from real logs.
  - It adds countermeasure validation, protocol fuzzing and formal verification, which none of the earlier grid tools had.
  - It moves from power grids to building automation and robotics.

### Inferences
- **(10) Reusable parts:**
  - The MQTT component-emulator pattern: per-device message handlers plus simulators plus a broker.
  - The YAML scenario schema with `attack_scenario: {scenario_name, target}`.
  - The `scene_switcher` plug-in point for new attacks.
  - The network-disturbance injector.
  - The Atheris and Maude verification harnesses.
  - All are directly reusable as an "OT protocol layer" template. For realism, the MITM and BAC modules would need replacing with real network-level attacks (e.g., ARP spoofing in Mininet or containers).

### Gaps
- The IJCIP 2026 full text was not accessible (ScienceDirect returned 403), so journal-only additions are unknown; the git history suggests disturbance injection and scalability tests.
- I could not confirm whether the real building or vendor is named.

## Q4. Beuran-lab foundation tools (CyRIS, CyTrONE, CyPROM, CyLMS, AutoPentest-DRL, IoTrain, CyATP, KYPO collaboration)

### Takeaway
All the older CROND tools are open source under BSD-3 and written in Python. CyRIS, CyTrONE, CyPROM and CyLMS were migrated to `cyb3rlab` and kept alive through 2024–2025 (Python 3, Ubuntu 24.04, AWS support). The CROND-only tools are frozen at February 2022: AutoPentest-DRL, GridAttackSim, GridAttackAnalyzer, CyATP and IoTrain-Sim/Lab. CyRIS (range instantiation from YAML on KVM or AWS) and CyPROM (Trigger-Action-Branching dynamic attack scenarios) are the most reusable bases for automated scenario execution.

### Cited Findings
- **CyRIS:**
  - Builds cyber ranges from YAML descriptions plus base VM images on KVM (or AWS since v1.2). Features: system configuration, tool installation, incident emulation (including traffic-capture emulation with noise PCAPs), content and clone management, and Windows guests (v1.1).
  - Version history: v1.3 converted to Python 3 (January 2024); v1.4 validated on Ubuntu 24.04 (March 2025).
  - Repo: https://github.com/cyb3rlab/cyris. BSD-3; last commit 2025-08-29; tags 1.3 and 1.4; 5,149 lines of Python.
  - Sources: [cyb3rlab/cyris CHANGES](https://github.com/cyb3rlab/cyris/blob/master/CHANGES); [crond-jaist/cyris README](https://github.com/crond-jaist/cyris).
  - AWS paper: R. Beuran, Z. Zhang, Y. Tan, "AWS EC2 Public Cloud Cyber Range Deployment", IEEE EuroS&PW 2022, DOI 10.1109/EuroSPW55150.2022.00051 — [Crossref query](https://api.crossref.org/works?query.author=Razvan+Beuran&filter=from-pub-date:2021-01-01).
- **CyTrONE:**
  - An integrated training framework. It uploads training content to an LMS (Moodle via CyLMS), creates the range via CyRIS, and can use CyPROM for dynamic elements such as real-time attacks.
  - The new repository is cyb3rlab/cytrone (BSD-3, tag 1.3, last updated March 2025). The crond-jaist copy has 392 KB of code — [crond-jaist/cytrone README](https://github.com/crond-jaist/cytrone); [cyb3rlab org](https://github.com/orgs/cyb3rlab/repositories).
  - A web UI exists: crond-jaist/cytrone-ui-web (Perl, last updated 2022-03) — [crond-jaist org](https://github.com/orgs/crond-jaist/repositories).
- **CyPROM:**
  - Scenario progression management using a "Trigger-Action-Branching" mechanism that drives attack, forensics and defense training in dynamic environments.
  - v0.2 has 16 action modules (command execution, dictionary attack, content crawling, injection attack, network scanning, DoS) and 11 example scenarios. It uses nmap in the range.
  - Repo: https://github.com/cyb3rlab/CyPROM. BSD-3; last commit 2024-12-19; 3,607 lines of Python — [cyb3rlab/CyPROM README and CHANGES](https://github.com/cyb3rlab/CyPROM).
- **CyLMS:** LMS (Moodle) integration. The crond-jaist copy is frozen with a notice pointing to cyb3rlab/cylms (last updated March 2025) — [crond-jaist/cylms](https://github.com/crond-jaist/cylms); [cyb3rlab org](https://github.com/orgs/cyb3rlab/repositories).
- **AutoPentest-DRL:**
  - Pipeline: MulVAL attack graph → simplified attack tree → DQN finds an attack path → optional execution with nmap and Metasploit on a real network.
  - Requirements: gym, torch, graphviz, among others.
  - Repo: https://github.com/crond-jaist/AutoPentest-DRL. BSD-3; commits 2021-03-30 to 2022-02-15; 1,126 lines of Python — [README](https://github.com/crond-jaist/AutoPentest-DRL).
- **IoT training tools:**
  - IoTrain-Sim: IoT training on the Cooja simulator (C, 2019–2022).
  - IoTrain-Lab: FIT/IoT-LAB testbed (C, 2020–2022).
  - Both are BSD-3 — [crond-jaist org](https://github.com/orgs/crond-jaist/repositories).
  - Paper: R. Beuran, J. Wang, M. Zhao, Y. Tan, "IoT security training for system developers: Methodology and tools", *Internet of Things* 2023, DOI 10.1016/j.iot.2023.100931 — [Crossref query](https://api.crossref.org/works?query.author=Razvan+Beuran&filter=from-pub-date:2021-01-01).
- **CyATP** (Cybersecurity Awareness Training Platform) and **topology-generator** (a random network topology generator, last updated 2021) also exist under crond-jaist — [crond-jaist org](https://github.com/orgs/crond-jaist/repositories).
- **KYPO (Masaryk University) collaboration (verified):** R. Beuran, J. Vykopal, D. Belajová, P. Čeleda, Y. Tan, Y. Shinoda, "Capability Assessment Methodology and Comparative Analysis of Cybersecurity Training Platforms", *Computers & Security* 2023, DOI 10.1016/j.cose.2023.103120 — [Crossref query](https://api.crossref.org/works?query.author=Razvan+Beuran&filter=from-pub-date:2021-01-01).
- **Book (verified):** R. Beuran, *Cybersecurity Education and Training*, Springer 2025, DOI 10.1007/978-981-96-0555-2. It has chapters on cyber ranges, attack training, IoT security training and a detailed CyTrONE case study — [Crossref query](https://api.crossref.org/works?query.author=Razvan+Beuran&filter=from-pub-date:2021-01-01).

### Inferences
- CyRIS (declarative YAML → VMs/networks) plus CyPROM (event-driven attack-scenario engine) plus PenGym (Gym adapter) together form a usable "IT side" toolchain for a cyber-physical attack simulator.
- None of them includes OT protocols or physical-process models. Those would have to come from GridAttackSim-style co-simulation (GridLAB-D/ns-3/HELICS) or SBCSE-style protocol emulation.

### Gaps
- I did not inspect the cyb3rlab copies of CyTrONE and CyLMS in detail beyond their metadata.
- I found no public KYPO–JAIST shared codebase.

## Q5. Other post-2020 work from these authors relevant to CPS/ICS attack simulation, AI pentesting, transactive energy and digital twins

### Takeaway
After 2022 there are no further smart-grid attack-simulation frameworks from the Le/Beuran line. Beuran's lab moved to:
- AI for offense and defense: PenGym, the CMARL-ACD multi-agent RL attacker/defender, and RAF-AG (CTI-report-to-attack-path generation).
- LLM security tooling: CyLLM-DAP, CodeEnhancer, LLM-based ABAC policy generation, defending LLMs against obfuscated input.
- Intent-driven secure system design.
- SBCSE for buildings.

Adnan Anwar (Deakin) continued smart-grid security on the power side: false data injection surveys and detection, Deakin microgrid digital twin, P2P energy trading, and 2026 market-manipulation attacks. None of these produced an attack-simulation tool comparable to GridAttackSim, as far as I found.

### Cited Findings
- **CMARL-ACD (verified code; paper under review):**
  - A competitive multi-agent RL framework in which attacker and defender agents co-evolve.
  - Simulation side: an extended NASim with a simulated IDS that has noisy alerts (SSH false positives) and benign background traffic. Training paradigms are MAPPO and IPPO, on torch 2.7, torchrl and tensordict.
  - Policies are validated *without retraining* on a real KVM testbed with Snort IDS, Metasploit plus nmap, iptables blocking and Docker decoys. The `real-testbed/` side is evaluation-only.
  - Repo: https://github.com/cyb3rlab/CMARL-ACD. License MIT (derived from NASim); commits 2026-06-12 to 2026-06-23; 35,616 lines of Python including the vendored NASim; 89 MB with trained checkpoints.
  - README reference: T. C. Nguyen and R. Beuran, *Computers & Security* (under review), 2026 — [README](https://github.com/cyb3rlab/CMARL-ACD).
- **RAF-AG:**
  - K. Mai, J. Lee, R. Beuran, R. Hotchi, S. E. Ooi, T. Kuroda, Y. Tan, "RAF-AG: Report analysis framework for attack path generation", *Computers & Security* 2025, DOI 10.1016/j.cose.2024.104125 — [Crossref query](https://api.crossref.org/works?query.author=Razvan+Beuran&filter=from-pub-date:2021-01-01).
  - Generates MITRE ATT&CK technique-ID attack paths from CTI reports through graph alignment against an ATT&CK-procedure knowledge graph. Stack: spaCy 3.5, coreferee, snorkel, networkx, mitreattack-python, tensorflow_hub.
  - Repo: https://github.com/cyb3rlab/RAF-AG. BSD-3; last commit 2025-09-21; 7,531 lines of Python — [README](https://github.com/cyb3rlab/RAF-AG).
- **LLM-related Beuran-lab work (verified bibliographic):**
  - CyLLM-DAP (ICISSP 2025, DOI 10.5220/0013094800003899; repo cyb3rlab/CyLLM-DAP).
  - "LLM-Based Fine-Grained ABAC Policy Generation" (ICISSP 2025, DOI 10.5220/0013225500003899).
  - CodeEnhancer (*Knowledge-Based Systems* 2026, DOI 10.1016/j.knosys.2026.115925).
  - "POSTER: Defending LLMs Against Non-natural Language Obfuscated Attacks" (LNCS 2026, DOI 10.1007/978-981-92-6843-6_46; repo LLMSafeguardEval-NonNL).
  - "Human-in-the-Loop for Machine Learning in Offensive Cybersecurity" (ICAIIC 2025, DOI 10.1109/ICAIIC64266.2025.10920815).
  - Sources: [Crossref query](https://api.crossref.org/works?query.author=Razvan+Beuran&filter=from-pub-date:2021-01-01); [cyb3rlab org](https://github.com/orgs/cyb3rlab/repositories).
- **Intent-driven secure design (with NEC):**
  - SecureWeaver (ACM CPSIoTSec 2022, DOI 10.1145/3510547.3517923).
  - "Intent-Driven Secure System Design: Methodology and Implementation" (*Computers & Security* 2023, DOI 10.1016/j.cose.2022.102955).
  - "AI-based Intent-Driven Secure System Designer" (APNOMS 2025, DOI 10.23919/APNOMS67058.2025.11181426).
  - Source: [Crossref query](https://api.crossref.org/works?query.author=Razvan+Beuran&filter=from-pub-date:2021-01-01).
- **IoT IDS:** FedMSE, a semi-supervised federated-learning IoT IDS (*Computers & Security* 2025, DOI 10.1016/j.cose.2025.104337) — [Crossref query](https://api.crossref.org/works?query.author=Razvan+Beuran&filter=from-pub-date:2021-01-01).
- **Anwar (Deakin) smart-grid and CPS work after 2020 (verified bibliographic):**
  - IEC 61850 GOOSE vulnerability and impact analysis (*Sensors* 2021, DOI 10.3390/s21041554).
  - False data injection attack taxonomy (*Renewable and Sustainable Energy Reviews* 2022, DOI 10.1016/j.rser.2022.112423).
  - FDI defence taxonomy (*ACM Computing Surveys* 2023, DOI 10.1145/3592797).
  - FDI threats in active distribution systems (*FGCS* 2023, DOI 10.1016/j.future.2022.10.021).
  - "DμDT: the Deakin University Microgrid Digital Twin" (APPEEC 2022, DOI 10.1109/APPEEC53445.2022.10072197).
  - Blockchain P2P energy trading (*IEEE Transactions on Smart Grid* 2021, DOI 10.1109/TSG.2021.3056147).
  - HiCoOB P2P trading consensus (*IEEE Transactions on Smart Grid* 2023, DOI 10.1109/TSG.2022.3231218).
  - IIoT testbed and datasets (SMART GENCON 2022, DOI 10.1109/SMARTGENCON56628.2022.10083609).
  - PSO-based moving target defense against FDI (SmartGridComm 2025).
  - Learning-based stealthy load-redistribution attacks for market price manipulation (A. Anwar, A. Mahmood, IEEE PESGM 2026, DOI 10.1109/PESGM58988.2026.11693770).
  - Sources: [Crossref Anwar query](https://api.crossref.org/works?query.author=Adnan+Anwar&query.bibliographic=false+data+injection+smart+grid+digital+twin+cyber-physical&filter=from-pub-date:2021-01-01); [Crossref Anwar+Loke query](https://api.crossref.org/works?query.author=Adnan+Anwar+Seng+Loke&filter=from-pub-date:2021-01-01).
- **Loke and Anwar (non-security energy work):** IoT-based smart home/office energy management (SmartGridComm 2022; VTC2022-Spring) — [Crossref Anwar+Loke query](https://api.crossref.org/works?query.author=Adnan+Anwar+Seng+Loke&filter=from-pub-date:2021-01-01).

### Inferences
- **Next-generation design:**
  - Combine GridAttackSim's GridLAB-D/ns-3 co-simulation (physical layer), GridAttackAnalyzer's HARM/CVSS path planner, PenGym/CMARL-ACD's Gym interface and sim-to-real methodology (attacker and defender agents), CyRIS-style declarative range instantiation, CyPROM-style trigger-action scenario progression, SBCSE-style protocol emulation with fuzzing and fault injection, and RAF-AG-style CTI-to-ATT&CK path generation for automatic scenario seeding.
  - Anwar's FDI, market-manipulation and digital-twin work supplies the physical-impact attack models that GridAttackSim lacked (FDI on state estimation, price manipulation in transactive markets).
- **Licensing and maturity:**
  - Everything is BSD-3 except CMARL-ACD (MIT), so it is permissive to reuse.
  - The grid-specific code is stale (2021–2022, Ubuntu 18.04, numpy 1.14). The actively maintained code is IT/RL-oriented (PenGym, CMARL-ACD, CyRIS) and building-oriented (SBCSE).

### Gaps
- No LLM-driven *pentest agent* framework from the Beuran lab was found. Searches returned only other groups' work (PentestAgent, AutoPentester and others), and the "Human-in-the-Loop for ML in Offensive Cybersecurity" paper was not read.
- I found no paper from these authors explicitly on transactive-energy *attack simulation* or digital-twin-based *attack* emulation. Anwar's DμDT is a forecasting digital twin, not a security testbed, judging by its title; the paper was not read.
- Crossref author queries are relevance-ranked and may miss some papers. DBLP and Beuran's JAIST publication list were blocked by bot protection or a 403 in this session.
