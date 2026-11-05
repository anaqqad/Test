# AI-driven CPS attack simulation: 2026 research opportunities and evidence for estimating AI-agent build effort

Notes compiled 2026-11-05. Budget-limited pass of about 16 search and fetch calls. Primary sources were fetched for METR (time-horizons page, limitations note) and the Anthropic C-compiler post. Most other items come from search-result abstracts and snippets; these are marked [snippet] where I did not open the full paper. Items marked [prior knowledge, not re-verified] come from my training knowledge and were not re-checked in this session. The report writer should verify those before citing them.

Peer-review status key: **PR** = peer-reviewed venue confirmed; **PP** = preprint (arXiv/TechRxiv) with no venue confirmed.

---

## Q1. What gaps in AI-driven CPS attack simulation are unaddressed and publishable in 2026?

### Takeaway
The 2025–2026 frontier has moved from LLM agents in IT networks to the first ICS and substation benchmarks: CritBench (IEC 61850, Apr 2026) and PLCBench (real PLCs in the loop, Aug 2026). Both report that LLMs know the domain but fail at multi-step dynamic interaction, and at turning access into physical impact. No published system we found joins five pieces: (a) CTI- or ATT&CK-for-ICS-driven scenario generation, (b) an LLM/RL attacker acting on (c) a co-simulated grid and network digital twin, with (d) automated physical-impact scoring and (e) detector benchmarking, all in (f) a reproducible, provenance-tracked pipeline. That end-to-end combination, and each of its interfaces, is the clearest publishable gap.

### Cited Findings

**A1. LLM-driven adversary simulation and autonomous pentesting (IT networks)**
- **Incalmo** (Singer, Lucas, Adiga, Jain, Bauer, Sekar; CMU, with an Anthropic affiliation per alphaXiv). It separates LLM high-level planning (declarative tasks) from execution by expert agents, with auxiliary services that track context and acquired assets. It introduces **MHBench**: 40 emulated networks of 22–50 hosts. Incalmo acquires critical assets in **37/40** environments; prior state-of-the-art LLM systems succeed in **3/40**. Successful attacks took **12–54 minutes** and cost **≤ $15** in LLM credits. Smaller LLMs (Haiku 3.5) succeed in most environments. arXiv 2501.16466, first posted Jan 2025, v4 in Nov 2025 (v3 was titled "On the Feasibility of Using LLMs to Autonomously Execute Multi-host Network Attacks" and used 10 networks). **PP** (no USENIX venue confirmed in search) — [arXiv](https://arxiv.org/abs/2501.16466); [alphaXiv overview](https://www.alphaxiv.org/overview/2501.16466)
- **CAI (Cybersecurity AI)**, Alias Robotics. An "open, bug bounty-ready" framework for building security-testing agents "at human-competitive levels", built on six pillars (Agents, Tools, …). arXiv 2504.06017, Apr 2025, **PP**. Follow-ups: attack/defense CTF evaluation (arXiv 2510.17521), a prompt-injection attack on AI hackers (arXiv 2508.21669), and a game-theoretic attack/defense guidance paper (arXiv 2601.05887). [snippet] — [GitHub](https://github.com/aliasrobotics/cai); [ResearchGate](https://www.researchgate.net/publication/390601558_CAI_An_Open_Bug_Bounty-Ready_Cybersecurity_AI); [2510.17521](https://arxiv.org/pdf/2510.17521); [2508.21669](https://arxiv.org/pdf/2508.21669); [2601.05887](https://arxiv.org/pdf/2601.05887)
- **PentestGPT**: arXiv 2308.06782 (2023). **VulnBot**, a multi-agent collaborative pentest framework: arXiv 2501.13411 (2025). Both appear as citations in CAI-related reference lists. [snippet] — [CAI paper refs](https://pinzger.github.io/papers/Vilches2026-CAI.pdf)
- [prior knowledge, not re-verified] PentestGPT was published at USENIX Security 2024 (Deng et al.). AutoAttacker is arXiv [2403.01038](https://arxiv.org/abs/2403.01038) (2024). HackSynth is arXiv [2412.01778](https://arxiv.org/abs/2412.01778) (Dec 2024). Cybench (CTF benchmark) is arXiv [2408.08926](https://arxiv.org/abs/2408.08926), reportedly at ICLR 2025. The search did not return these, so check venues.
- Survey "Forewarned is Forearmed: A Survey on LLM-based Agents in Autonomous Cyberattacks" (arXiv 2505.12786, May 2025, **PP**). It cites **AttackLLM** (Ahmed, 2025), which reportedly generates ICS attack patterns that exceed human-crafted ones in quality and diversity. I saw only the survey's description, not the original. [snippet] — [arXiv](https://arxiv.org/html/2505.12786v2)

**A2. LLM agents for OT/ICS and grid attack tasks (the newest and thinnest area)**
- **CritBench** (Keppler, Gstür, Hagenmeyer; KIT). An open-source framework for evaluating LLM agents on offensive tasks in **IEC 61850 digital substations**. It has **81 challenges**, including 30 traffic-analysis tasks, across PCAP, SCD/CID and VM-interaction categories, covering MMS, GOOSE, Sampled Values and IEC 60870-5-104. Finding: SOTA LLMs "possess internalized, domain-specific knowledge of standards… However, their performance degrades in dynamic interactions." arXiv 2604.06019 (Apr 2026). Listed with an ACM DL DOI (10.1145/3765611.3815141) as an oral at **ACM EnergySP '26**, so **PR (workshop/symposium)**. — [arXiv](https://arxiv.org/abs/2604.06019); [ACM DL](https://dl.acm.org/doi/10.1145/3765611.3815141); [GitHub](https://github.com/GKeppler/CritBench); [EnergySP '26](https://energysp.github.io/)
- **PLCBench: "Can Autonomous LLM Agents Turn PLC Access into Sustained Physical Impact?"** The authors call it the first real-PLC hardware-in-the-loop framework, pairing vendor-native PLC interaction with closed-loop process simulation and independent outcome checks. Across **5 LLMs × 4 commercial PLCs × 4 workloads**, **75/240 episodes (31.3%)** reached physical impact, with at least one success in every PLC-workload configuration. There are two distinct bottlenecks: acquiring the PLC interface, and converting access into impact. Richer process observation raised post-write objective attainment **from 44.2% to 64.0%**. The authors argue that benchmarks stopping at "an accepted write" understate physical risk, and they release a software-only reproduction pipeline. arXiv 2608.26882 (Aug 2026), **PP**. [snippet; abstract-level] — [arXiv PDF](https://arxiv.org/pdf/2608.26882); [summary](https://tldr.takara.ai/p/2608.26882)
- An AI agent placed in the AI top-10 of the **Dragos OT CTF 2025** (arXiv 2511.05119, Nov 2025, **PP**). Only the title and reference list were seen. — [arXiv](https://arxiv.org/pdf/2511.05119)

**A3. RL attackers and defenders, CAGE, multi-agent cyber simulation**
- **CAGE Challenge 4** is a scalable multi-agent RL gym for autonomous cyber defence, built on CybORG. It has multiple defending agents with limited communication, partial observability and a shared reward. **Note: it is an enterprise-network gym, not a grid simulator.** — [ResearchGate](https://www.researchgate.net/publication/396739017_CAGE_challenge_4_A_scalable_multi-agent_reinforcement_learning_gym_for_autonomous_cyber_defence); [CybORG++ arXiv 2410.16324](https://arxiv.org/pdf/2410.16324)
- "Large Language Models are Autonomous Cyber Defenders" (arXiv 2505.04843, **PP**) compares LLM and RL defenders on CAGE-4. In the search snippets, RL approaches beat all-LLM approaches on CAGE-4. One snippet reports RL+RL at 78.5% disruption success versus 18.0% for the strongest LLM configuration; the exact provenance of those numbers within the paper was not verified. [snippet] — [arXiv](https://arxiv.org/html/2505.04843v2)
- Hierarchical multi-agent RL for cyber network defense (arXiv 2410.17351; RLJ/RLC 2025, **PR**); MARL for autonomous cyber defence (AAAI 2025, **PR**). — [RLC 2025](https://rlj.cs.umass.edu/2025/papers/RLJ_RLC_2025_77.pdf); [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/35158/37313)
- Grid-side RL: adversarial training for RL power-system control on L2RPN/**Grid2Op** (arXiv 2110.08956). The search found no work that couples CAGE-style cyber gyms with Grid2Op physics. — [arXiv](https://arxiv.org/pdf/2110.08956)
- arXiv 2605.09792 combines attack-path modeling with RL for mitigation planning (2026, **PP**, title only). — [arXiv](https://arxiv.org/pdf/2605.09792)

**A4. CTI to attack scenarios, attack graphs, ATT&CK for ICS**
- **GARAGE**: "Characterizing the Automation Boundary in LLM-based Attack Graph Generation" (arXiv 2607.18108, Jul 2026, **PP**, title only). — [arXiv](https://arxiv.org/pdf/2607.18108)
- "An Automated Framework for Extracting Reachable Attack Chains from CTI Reports" (arXiv 2607.19742, 2026, **PP**, title only). — [arXiv](https://arxiv.org/pdf/2607.19742)
- Symbolic attack-chain generation from Atomic Red Team techniques, studying predicate-representation granularity (arXiv 2608.00143, **PP**, title only). — [arXiv](https://arxiv.org/pdf/2608.00143)
- TechRxiv preprint (3 Sep 2025) on automating CTI and attack-chain generation with LLMs plus knowledge graphs and ATT&CK mapping, for reproducible attack simulations (**PP**). — [TechRxiv](https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.175693745.57950884/v1)
- MITRE ATT&CK applications survey (arXiv 2502.10825). — [arXiv](https://arxiv.org/pdf/2502.10825)
- "AI-Agent Application Threat Assessment with Attack Graphs" (arXiv 2506.02859). — [arXiv](https://arxiv.org/pdf/2506.02859)
- [prior knowledge, not re-verified] MulVAL (Ou, Govindavajhala, Appel; USENIX Security 2005) is the canonical logic-based attack-graph generator.

**A5. Digital twins, co-simulation and impact (grid)**
- Al-Qirim et al. (2025, SAGE journal, **PR**) build a knowledge-graph and digital-twin framework for smart-grid SCADA CTI. It visualizes the impact of FDIA, remote-tripping command injection and reconfiguration attacks. — [SAGE](https://journals.sagepub.com/doi/10.1177/18479790251328183)
- **GenAI-FDIA**: physics-informed generative models for false data injection attacks (arXiv 2605.18873, 2026, **PP**, title only). — [arXiv](https://arxiv.org/pdf/2605.18873)
- **NATIG**-style testbed: a co-simulation framework (GridLAB-D + HELICS + ns-3) for network attack generation and monitoring, described as "stand-alone, containerized, and reusable" (arXiv 2307.09633, 2023). — [arXiv](https://arxiv.org/abs/2307.09633)
- Simulation of multi-stage attack and defense in smart grids (arXiv 2412.06255, Dec 2024, **PP**). — [arXiv](https://arxiv.org/pdf/2412.06255)
- Cybersecurity analysis of distribution-grid operation with co-simulation (OSTI 1646564; national-lab report). — [OSTI](https://www.osti.gov/servlets/purl/1646564)
- Real-time mitigation in IEC 61850/62351 substations (arXiv 2511.18748). — [arXiv](https://arxiv.org/pdf/2511.18748)

**A6. Automated defensive evaluation and reproducibility**
- The search found no paper on automated detector benchmarking driven by LLM- or RL-generated CPS attacks, and none on Nix- or provenance-based reproducibility for CPS-security co-simulation. CritBench and PLCBench release code and a "software-only reproduction pipeline" (PLCBench), but those are benchmark releases, not provenance frameworks. — [PLCBench](https://tldr.takara.ai/p/2608.26882); [CritBench GitHub](https://github.com/GKeppler/CritBench)

### Inferences
- **Gap 1 (strongest): LLM/RL attacker in a closed loop with grid physics and a network co-simulation.** CritBench tests the protocol and VM layer. PLCBench tests single PLC-to-process loops. Incalmo and MHBench test IT multi-host networks. None combines a multi-host IT/OT network with a power-flow or dynamic grid model (e.g., pandapower, Grid2Op or GridLAB-D via HELICS) and scores attacks by physical consequence (load shed, frequency or voltage violations). That would extend PLCBench's insight, that "accepted write" understates risk, to the grid level.
- **Gap 2: Incalmo-style abstraction layers for OT.** Incalmo showed that a high-level task abstraction raised success from 3/40 to 37/40 in IT. CritBench and PLCBench both find that dynamic multi-step interaction is the bottleneck. An OT action abstraction (for example "read IED dataset", "issue GOOSE trip", "modify setpoint", with expert executors) is a natural, testable contribution.
- **Gap 3: CTI/ATT&CK-for-ICS to executable scenario.** 2026 preprints (GARAGE, CTI-to-reachable-chains, Atomic Red Team chains) target IT attack graphs. Grounding generated chains in a specific grid digital twin, and checking executability by running them, appears open.
- **Gap 4: LLM-versus-RL head-to-head on a grid.** On CAGE-4, RL appears to beat LLM defenders. No equivalent comparison exists for grid attackers or defenders. A Grid2Op plus cyber-layer gym is a candidate shared benchmark.
- **Gap 5: Attack-generator-driven detector benchmarking with impact-weighted metrics, plus reproducibility.** Measuring IDS performance on agent-generated, physically consequential attacks, with hermetic builds (Nix or containers) and provenance, is an under-served engineering-science contribution. It would also strengthen reproducibility claims, which matter for venues such as EnergySP and SmartGridComm.
- Safety framing matters. PLCBench withholds non-disclosable code. A 2026 paper on autonomous grid attack agents will need a responsible-disclosure and dual-use section.

### Gaps
- Full abstracts or results for GARAGE, GenAI-FDIA, 2607.19742, 2608.00143 and the Dragos OT CTF paper were not retrieved.
- Venues for PentestGPT, AutoAttacker, HackSynth and Cybench were not re-verified in this session.
- No source was found for RL false-data-injection attacks on Grid2Op specifically (2023–2026), or for Grid2Op adversarial-agent papers beyond the 2021 adversarial-training work.
- Lab evaluations (Anthropic, OpenAI, Google cyber evaluations and system cards) were not fetched in this pass.
- The search turned up no work on MulVAL-style attack graphs combined with LLMs for ICS.

---

## Q2. How fast do AI agents complete multi-hour or multi-day software tasks, and how much human supervision do they need?

### Takeaway
The best-documented multi-day autonomous build is Anthropic's C compiler, released Feb 2026. Sixteen parallel Opus 4.6 agents produced about 100k lines of Rust in about two weeks for just under $20k. The result was only possible because a human expert built the test harness, CI and oracles, and it still has major gaps. The METR RCT (early-2025 tools) found experienced developers were **19% slower** with AI on their own repositories, despite believing they were faster. Overall, effort shifts toward verification and harness design rather than disappearing, and the gain depends heavily on having a strong automated oracle.

### Cited Findings

**Anthropic C-compiler case study** (Nicholas Carlini, Safeguards team, "Building a C compiler with a team of parallel Claudes", Anthropic Engineering blog, **5 Feb 2026**; primary source fetched) — [Anthropic](https://www.anthropic.com/engineering/building-c-compiler)
- Setup: **16 parallel Claude (Opus 4.6) agents**, nearly **2,000 Claude Code sessions** over **two weeks**, **just under $20,000** in API cost, about **2 billion input and 140 million output tokens**.
- Output: a Rust C compiler written from scratch, about **100,000 lines**, with no dependencies beyond the Rust std library. It builds a bootable **Linux 6.9 on x86, ARM and RISC-V**, compiles QEMU, FFmpeg, SQLite, Postgres and Redis, and runs Doom. It reports a **99% pass rate on most compiler test suites, including the GCC torture tests**.
- Human role: the human designed the test harness, verifiers and CI pipeline, and watched for failure modes to write new tests. They wrote the agent loop and prompt, set up progress files and READMEs, and designed the feedback to limit "context pollution" and "time blindness" (e.g., `--fast` sampling, summarized logs). They used **GCC as a known-good oracle** so agents could parallelize work on the kernel. They set the high-level design (SSA IR, GCC compatibility) but no implementation details. There was no orchestration agent; agents claimed tasks via file locks.
- Stated failure modes and limits:
  - No 16-bit real-mode code generator: output exceeded 60 KB against Linux's 32 KB limit, so it calls GCC for that phase on x86.
  - The assembler and linker are buggy, and the demo used GCC's.
  - It is not a drop-in replacement, and many projects still fail to build.
  - Generated code is less efficient than GCC with optimizations disabled.
  - Code quality is "reasonable" but below expert level.
  - **New features and fixes often broke existing functionality**, which is why the CI was added.
  - The author says it "has nearly reached the limits of Opus's abilities."
  - Earlier models: Opus 4 could barely produce a functional compiler; Opus 4.5 passed test suites but could not compile large real projects.
  - The author warns that passing tests does not mean the job is done.

**METR developer-productivity RCT** (Becker, Rush, Barnes, Rein; "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity", arXiv 2507.09089, July 2025, **PP**)
- **16 experienced developers** completed **246 tasks** (about **2.0 hours average**) on mature repos they contribute to (about **23,000 stars** on average), with AI allowed or disallowed per task. The trial ran **Feb–Jun 2025** with early-2025 tools.
- Result: AI **increased completion time by about 19%**. Developers forecast a **24% speedup** beforehand and afterward believed they had been **sped up by 20%**.
- Caveat from the authors: this does not mean AI fails to help in general, especially for less experienced developers or unfamiliar codebases.
- Sources: [arXiv](https://web3.arxiv.org/pdf/2507.09089); [Simon Willison, 12 Jul 2025](https://simonwillison.net/2025/Jul/12/ai-open-source-productivity/); [Diginomica](https://diginomica.com/node/29061)
- A separate trial with 96 Google engineers reportedly found about 21% faster completion on an enterprise task (secondary report; primary source not fetched). — [letsdatascience summary](https://letsdatascience.com/blog/developers-thought-ai-made-them-faster-the-data-said-otherwise)

**SWE-bench (benchmark saturation; snapshots conflict, treat with caution)**
- SWE-bench Verified is near saturation.
  - Vals.ai (updated 1 Sep 2026): Claude Opus 5 with the mini-SWE-agent harness at **97.00%**. — [Vals.ai](https://www.vals.ai/benchmarks/swebench)
  - llm-stats (Nov 2026): top score **0.950**. — [llm-stats](https://llm-stats.com/benchmarks/swe-bench-verified)
  - The differences come from harnesses and dates. These are aggregators, not swebench.com.
- **SWE-bench Pro**, Scale AI's standardized public set: a top score of **61.5%** (Muse Spark 1.1) and GPT-5.4 (xHigh) at **59.1%**, per an Oct 2026 Morph aggregator. A vendor-reported 89.9% for Claude Opus 5.5 (as of 28 Sep 2026) is **not comparable** to the standardized number. — [Morph](https://www.morphllm.com/swe-bench-pro)
- Benchmark-validity critiques: SWE-ABS shows "inflated success rates on test-based benchmarks" (arXiv 2603.00520). PAIChecker reports PR–issue misalignment in SWE-bench-like sets (arXiv 2607.28587). SWE-Bench Pro Verified (arXiv 2609.08149). — [2603.00520](https://arxiv.org/pdf/2603.00520); [2607.28587](https://arxiv.org/pdf/2607.28587); [2609.08149](https://arxiv.org/pdf/2609.08149)

**Human effort for comparable CPS co-simulation testbeds**
- HELICS has been used to couple ns-3 and GridLAB-D in several studies: a Riverside Public Utilities DERMS study, distributed OPF (arXiv 2212.04615), and NATIG (GridLAB-D + HELICS + ns-3, containerized). HELICS was developed under the DOE Grid Modernization Lab Consortium, with PNNL and other labs (GMLC project slides). The HELICS overview paper is Hardy et al., IEEE Access 2024. — [HELICS IEEE Access 2024](https://faculty.sites.iastate.edu/tesfatsi/archive/tesfatsi/HELICSCoSimFramework.HardyEtAl.IEEEAccess2024.pdf); [GMLC/PNNL slides](https://www.energy.gov/sites/prod/files/2017/08/f35/PNNL_HHuang_GMLC%20Project_Development%20of%20Integrated%20Transmission,%20Distribution%20and%20Communication%20(TDC)%20Models.pdf); [NATIG-type arXiv 2307.09633](https://arxiv.org/abs/2307.09633); [arXiv 2212.04615](https://arxiv.org/pdf/2212.04615)
- **No source found** that quantifies team size, person-years, or installation difficulty for HELICS, TESP, GridLAB-D + ns-3, or SCEPTRE.

### Inferences
- For a GridAttackSim build with Claude Code, the C-compiler case suggests that the decisive cost is **building oracles**: power-flow reference solutions, protocol conformance tests and end-to-end scenario checks. Agent typing time matters less. Where an oracle exists (pandapower/OpenDSS results, Wireshark dissectors for MMS/GOOSE/104), agents can run in parallel. Where it doesn't (attack realism, physical plausibility), expect heavy human review.
- Expect the regression churn the C-compiler post describes ("new features often broke existing functionality"). Budget for CI from day one.
- Native-build and integration pain is the plausible weak spot: HELICS/ns-3 C++ builds, GridLAB-D, and Windows versus Linux. The C-compiler project avoided external dependencies by design, and METR notes that messier, higher-context tasks fall below benchmark horizons. This is an inference; the search turned up no direct study of agents on native co-simulation builds.
- The METR RCT shows that perceived speedups can be badly miscalibrated, so the effort estimate should rest on measured milestones, not on felt productivity.

### Gaps
- METR has not published a follow-up RCT with 2026 tools. I did not verify whether one exists.
- Anthropic, OpenAI or Google reports on other multi-day builds beyond the C compiler were not retrieved.
- There is no quantitative data on human effort for HELICS, TESP, SCEPTRE or similar testbeds (team size, person-years, PhD timelines). The report writer should treat any such figure as unsupported unless sourced elsewhere.
- No systematic study of agent failure rates on environment setup or native C/C++ builds was found.

---

## Q3. What is the 50%-success task-length horizon of frontier agents per the latest METR data?

### Takeaway
On METR's Time Horizon 1.1 suite, the top published 50% horizon is an **early version of Claude Mythos Preview** (added to METR's page **8 May 2026**). It was reported as **about 16+ hours (95% CI about 8.5–55 hours)**; the data-file value is roughly 17 hours. METR itself says **measurements above 16 hours are unreliable** with the current task suite. METR's time-horizons page says it has been **"no longer actively updated" since 8 Sep 2026**. For context, Claude Opus 4.6 was about **12 hours** (after a 3 Mar 2026 correction from about 14.5 h), and GPT-5 was about **2 h 17 min** (Aug 2025).

### Cited Findings
- METR time-horizons page (fetched 2026-11-05):
  - It is "no longer actively updated" as of **8 Sep 2026**.
  - The main chart uses **Time Horizon 1.1** ("same methodology… larger task suite"). TH 1.0 dates from Mar 2025.
  - The page notes: "**Measurements above 16 hrs are unreliable with our current task suite**" (added 8 May 2026).
  - Models added: **Claude Mythos Preview (early), 8 May 2026**; Gemini 3.1 Pro (15 Apr 2026); GPT-5.4 (10 Apr 2026); Claude Opus 4.6 and GPT-5.3-Codex (20 Feb 2026); GPT-5.2 (4 Feb 2026); Claude Opus 4.5 (19 Dec 2025).
  - The only explicit number in the page text is **GPT-5 at about 2 h 17 min** (50%). Per-model values are in a data file (`benchmark_results_1_1.yaml`) that I did not retrieve.
  - Source: [METR time horizons](https://metr.org/time-horizons/)
- Mythos figure (secondary sources quoting METR):
  - A "minimum 50%-time-horizon of 16 hours (95% CI: 8.5–55 hours)", and more than 2× the next-best model on the 80% horizon. — [OfficeChai](https://officechai.com/ai/claude-mythos-shows-50-time-horizon-of-16-hours-on-metr-benchmark/); [gentic.news](https://gentic.news/article/claude-mythos-preview-doubles-metr)
  - A leaderboard mirror lists about **1044.78 minutes (about 17.4 h)** on v1.1. — [datalearner](https://www.datalearner.com/benchmarks/metr-time-horizons-v1-1)
  - One search summary gives an 80% horizon of about 3 h 6 min for the same model. Unverified. — [agitracker](https://agitracker.io/blog/metr-time-horizons-2026/)
  - **Conflict:** outlets report "16 h" (a lower bound) versus "17.4 h" (the point estimate in the data file).
- Opus 4.6: first reported at about 14.5 h, then **corrected to about 12 h** after METR fixed a modeling bug on **3 Mar 2026**. This comes from search summaries of secondary sources; I did not see METR's correction notice directly. — [agitracker](https://agitracker.io/blog/metr-time-horizons-2026/); [Wikipedia: METR](https://en.wikipedia.org/wiki/METR)
- METR "Clarifying limitations of time horizon" (22 Jan 2026, primary, fetched) — [METR note](https://metr.org/notes/2026-01-22-time-horizon-limitations/)
  - The time horizon is "the amount of serial human labor they can replace with a 50% success rate". It is not how long an AI can work autonomously, and AIs are often much faster than humans.
  - "Error bars have historically been a factor of ~2 in each direction."
  - The horizon is "40-100x lower for visual computer use tasks."
  - "Low-context tasks are isolated and don't require prior knowledge about a codebase." Real work is messier and higher-context.
  - "Top engineers, e.g. lab employees, would be faster"; baseline conventions "could affect time horizon by >1.25x."
  - A 50% horizon of X hours does not mean tasks under X hours can safely be delegated.
  - 99%+ horizons "cannot be fit at all" with current benchmarks.
  - The long-run trend is about **one doubling every 6–7 months**. Some third-party analyses claim a faster post-2023 doubling (about 4 months); these are not METR's own figure. — [AI 2027 tracker](https://ai2027-tracker.com/predictions/metr-doubling/)

### Inferences
- For effort estimation, a 12–17 h 50% horizon means a frontier agent completes about half of well-specified, low-context, self-contained tasks that would take a skilled human 1–2 working days. METR's own caveats imply the rate is lower for messy, high-context integration work, which is what a HELICS/ns-3/grid co-simulator mostly is. The 80% horizon is several times shorter, so it is the more relevant planning number for "delegate and expect it to work."
- A multi-week simulator build is far beyond any single-task horizon. It would need decomposition into horizon-sized tasks with automated oracles, as in the C-compiler project.

### Gaps
- I did not retrieve METR's `benchmark_results_1_1.yaml`. Exact per-model 50% and 80% values and confidence intervals for Opus 4.6, GPT-5.4, Gemini 3.1 Pro and Mythos therefore come from secondary sources.
- I did not find whether METR has measured any model released after May 2026 (e.g., Claude Opus 5 / 5.5, which SWE-bench aggregators list). The page has not been actively updated since 8 Sep 2026.
- The Opus 4.6 correction (about 14.5 h to about 12 h) was not confirmed on metr.org directly.
