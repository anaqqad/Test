# Tech stack status (Nov 2026) and state of the art for smart-grid cyber-physical attack simulation (beyond GridAttackSim)

Method note: research date 2026-11-05. Versions and dates come from PyPI JSON API, the npm registry, Docker Hub API, nsnam.org and GitHub pages, all fetched today. Direct GitHub API access was blocked in this environment, so GitHub stars and last-commit dates could not be pulled. Several GitHub release pages show day and month without a year; where I inferred the year, the note says so. "Inference" marks anything not stated directly by a source.

## Q1. Status in 2026 of the core co-simulation stack (GridLAB-D, ns-3, FNCS, HELICS, TESP, mosaik, OpenDSS, pandapower, GridPACK, PowerWorld)

### Takeaway
The GridAttackSim triad (GridLAB-D + ns-3 + FNCS) is out of date in 2026. FNCS has no releases and is not developed; HELICS 3.x (v3.7.0, Sept 2026) is its maintained successor. The weak link is the official HELICS-ns-3 module: its README says it does not work with ns-3.36 or newer, while ns-3 itself is at 3.49 (Oct 2026). mosaik 3.7 (Python, LGPL) and pandapower 3.5 are the most actively released Python-native alternatives.

### Cited Findings
**GridLAB-D**
- Latest full release is v5.3.0 ("Latest", dated "07 Jan", year not shown), which includes macOS Intel and CMake deprecation fixes. A **v6.0 pre-release** tag is dated "30 Oct" with no release notes. v5.0 introduced a major build/CMake refactor and fixed the FNCS CMake option. — [gridlab-d releases](https://github.com/gridlab-d/gridlab-d/releases)
- The official SLAC Docker images `gridlabd/slac-master` were last updated in 2019 (`release-4.2.0`, 2019-12-04), so no current official Docker image was found. — [Docker Hub API: gridlabd/slac-master](https://hub.docker.com/r/gridlabd/slac-master)
- The FNCS build option still exists in GridLAB-D 5.x (v5.0 notes "FNCS CMake option fixes"). — [gridlab-d releases](https://github.com/gridlab-d/gridlab-d/releases)

**ns-3**
- The latest release is **ns-3.49**, announced 2026-10-07. Earlier releases: ns-3.48 (2026-06-02), ns-3.47 (2026-02-16), ns-3.46 (2025-10-01) and ns-3.46.1 (allinone, 2025-12-17). Releases come 2–3 times per year as source archives. — [nsnam.org releases](https://www.nsnam.org/releases/); [nsnam news index 2026](https://www.nsnam.org/news/2026/) (post slugs `ns-3-49-released.html` on 2026/10/07, `ns-3-48-released.html` on 2026/06/02, `ns-3-47-released.html` on 2026/02/16); [ns-3.45 release news](https://www.nsnam.org/news/2025/06/01/ns-3-45-released.html)
- **Python bindings**: the PyPI package `ns3` (cppyy-based wheels, GPL-2.0-only) is at **3.44.post0 (2025-03-28)**, five releases behind the C++ release. — [PyPI ns3](https://pypi.org/project/ns3/)
- No official ns-3 Docker image was found on Docker Hub (`nsnam/ns3` returns "object not found"). — Docker Hub API query (negative result)

**FNCS**
- The FNCS repo has no releases. Its README still pins ZeroMQ 3.2.4 and CZMQ 3.0.0-rc1 and clones from an old GridOPTICS URL. It has no archive banner and no pointer to HELICS. — [FNCS/fncs](https://github.com/FNCS/fncs)

**HELICS**
- Releases: **v3.7.0 ("09 Sep"; Docker tag v3.7.0 last updated 2026-09-09)**, a major release that makes **C++20 the minimum standard** and adds broker startup controls; v3.6.1 (25 Feb 2025); v3.6.0 (10 Dec, 2024 by inference). — [HELICS releases](https://github.com/GMLC-TDC/HELICS/releases); [Docker Hub helics/helics](https://hub.docker.com/r/helics/helics) (tags `latest`/`builder` updated 2026-11-01)
- Python: PyPI `helics` is at **3.6.1 (2025-02-28)**, BSD licence, requires Python ≥3.8. As of today the PyPI wheel lags the C++ 3.7.0 release. — [PyPI helics](https://pypi.org/project/helics/)
- **helics-ns3 module**: GPL-2.0. The README says "This version of the helics-ns3 module WILL NOT WORK with ns-3.36 or newer", targets ns-3.35, and uses the WAF build (`./waf configure --with-helics=...`). It requires HELICS ≥3 built with `-DHELICS_BUILD_CXX_SHARED_LIB=ON`. — [GMLC-TDC/helics-ns3](https://github.com/GMLC-TDC/helics-ns3)
- An NSF REU project (Clarkson) set out to integrate ns-3 into HELICS, a sign that the integration still takes project-level effort. — [Clarkson REU](http://reu-hpc.clarkson.edu/zhang20a.html)

**PNNL TESP**
- PyPI `tesp-support` is at **1.3.8 (2026-09-11)**, BSD-3-Clause, Python ≥3.10. — [PyPI tesp-support](https://pypi.org/project/tesp-support/)
- Docker images `pnnl/tesp:1.3.7_ubuntu_24.04.1` (2026-02-05) and `1.3.6_ubuntu_22.04.1` (2024-12-15). — [Docker Hub pnnl/tesp](https://hub.docker.com/r/pnnl/tesp)

**mosaik (OFFIS)**
- `mosaik` **3.7.1 (2026-10-14)**, LGPL, Python ≥3.12. `mosaik-api-v3` 3.0.16 (2026-08-25), MIT. — [PyPI mosaik](https://pypi.org/project/mosaik/); [PyPI mosaik-api-v3](https://pypi.org/project/mosaik-api-v3/)
- The mosaik 3.0 paper describes combining time-stepped and discrete-event simulation, which is what coupling a network simulator to a power simulator needs. — [arXiv 2410.16937](https://arxiv.org/pdf/2410.16937)
- A 2026 arXiv paper builds a mosaik-based platform with five federates, including OpenDSS. — [arXiv 2609.03118 "Efficient Co-simulator Integration with Application to Smart Grids"](https://arxiv.org/pdf/2609.03118) (seen as a search snippet only; contents not verified)

**OpenDSS Python stacks**
- `OpenDSSDirect.py`: last stable **0.9.4 (2024-03-29)**; pre-releases **0.10.0b1/b2 (2026-02-20/26)**. `dss-python` stable 0.15.7 (2024-03-29); **0.16.0b2 (2026-02-26)**, BSD-3-Clause. — [PyPI opendssdirect.py](https://pypi.org/project/opendssdirect.py/); [PyPI dss-python](https://pypi.org/project/dss-python/)
- `py-dss-interface` **2.3.0 (2026-02-16)**, MIT, Python ≥3.9 (EPRI wrapper, Radatz). — [PyPI py-dss-interface](https://pypi.org/project/py-dss-interface/)

**pandapower / SimBench / pandapipes**
- `pandapower` **3.5.6 (2026-10-07)**, Python ≥3.10. `simbench` **1.6.3 (2026-09-22)**, Python ≥3.11. `pandapipes` 0.16.0 (2026-10-16). — [PyPI pandapower](https://pypi.org/project/pandapower/); [PyPI simbench](https://pypi.org/project/simbench/); [PyPI pandapipes](https://pypi.org/project/pandapipes/)

**GridPACK**
- Name collision: the PyPI package `gridpack` (0.5.4) is an **unrelated** compression library (showkeyjar/gridpack), not PNNL GridPACK. — [PyPI gridpack](https://pypi.org/project/gridpack/)

### Inferences
- A 2026 GridAttackSim-like build should replace FNCS with HELICS 3.7. The FNCS build option survives in GridLAB-D, but FNCS has no releases and its dependencies are pinned to 2013-era ZeroMQ.
- The main integration risk is **HELICS ↔ ns-3**. The official module documents only ns-3.35 (WAF, 2021-era), while current ns-3 uses CMake (since 3.36) and is at 3.49. A team should expect to port the module, pin ns-3.35 in a container, or drop ns-3 for an emulator (Mininet/containerlab) bridged through HELICS or mosaik. The pinned ns-3.35 also has to build alongside HELICS 3.7, which requires C++20 (inference; not tested).
- TESP's Docker images (Ubuntu 24.04) bundle GridLAB-D + HELICS + supporting tools. They are probably the lowest-pain way to get a working GridLAB-D/HELICS build in 2026 (inference from image tags; contents not inspected).
- For a Python-first team, mosaik + pandapower/OpenDSS (dss-python) is the most actively released stack. OpenDSSDirect.py has been in beta since Feb 2026, so pin versions.

### Gaps
- Years of the GridLAB-D v5.3.0 and v6.0-pre tags were not shown on the release page. GridLAB-D licence was not confirmed on the page (historically BSD-style; unverified here).
- FNCS last-commit date, and whether helics-ns3 has an unreleased CMake branch for ns-3 ≥3.36, could not be checked because the GitHub API was blocked.
- PNNL GridPACK (GridOPTICS/GridPACK) latest release not verified.
- **PowerWorld** licensing (commercial; free educational/limited-bus versions) was not verified in this session.
- No official PyPI release of HELICS 3.7.0 was found as of today.

## Q2. Network emulation / cyber-range infrastructure (Mininet, Mininet-WiFi, CORE, Containerlab, OMNeT++, minimega/phenix, Docker/K8s)

### Takeaway
Containerlab (v0.82.0, Oct 2026) and OMNeT++ (6.5.0, Oct 2026) are the most actively released. CORE 9.2.x is maintained and supports Docker/Podman nodes. Mininet and Mininet-WiFi look stagnant, with old Docker images and Travis CI. Sandia's phenix/minimega is the open-source backbone of SCEPTRE.

### Cited Findings
- **Containerlab** latest **v0.82.0, 2026-10-23**. — [srl-labs/containerlab releases](https://github.com/srl-labs/containerlab/releases)
- **OMNeT++ 6.5.0, 2026-10-29**, a bugfix release. It is installed via `opp_env` (Nix-based), with Windows support through a WSL image, and Docker is offered. — [omnetpp.org/download](https://omnetpp.org/download/)
- **CORE 9.2.1** ("19 May", year not shown). 9.1.0 made Docker nodes use `docker exec` and added Podman and compose support. 9.0.0 refactored the gRPC client. Python ≥3.10 has been required since 9.2.0. — [coreemu/core releases](https://github.com/coreemu/core/releases)
- **Mininet-WiFi**: no releases listed. The README recommends Ubuntu ≥16.04, the prebuilt VM is Lubuntu 20.04, CI badges point to travis-ci.org, and Docker requires `--privileged` and host networking. — [intrig-unicamp/mininet-wifi](https://github.com/intrig-unicamp/mininet-wifi)
- **Mininet**: the PyPI `mininet` package last uploaded 2.3.0.dev6 (2020-09-24). The popular community Docker image `iwaseyusuke/mininet` was last updated 2023-05-22. — [PyPI mininet](https://pypi.org/project/mininet/); [Docker Hub iwaseyusuke/mininet](https://hub.docker.com/r/iwaseyusuke/mininet)
- **phenix** (Sandia) is the orchestration layer for SCEPTRE on top of **minimega** (VM manager). An OSTI record lists phenix v7.0 under GPL-3.0 at github.com/sandialabs/sceptre-phenix. — [OSTI DOE Code 134097](https://www.osti.gov/doecode/biblio/134097); [SCEPTRE docs glossary](https://sandialabs.github.io/sceptre-docs/glossary.html)

### Inferences
- For a modern cyber range, containerlab (or Docker Compose/K8s) plus real protocol stacks in containers is the pragmatic choice. ns-3 suits only packet-level simulation, and its HELICS coupling is fragile (see Q1).
- minimega/phenix is the most mature open-source option for VM-based OT emulation, but it is heavyweight (KVM-based). Inference; host requirements not verified.

### Gaps
- Mininet's latest GitHub release (2.3.1b4?) and commit activity were not verified (GitHub blocked). CORE's 9.2.1 year was not verified. minimega's latest version was not verified.
- Kubernetes-based cyber-range frameworks (e.g. KYPO) were not researched in this session.

## Q3. ICS protocol and OT attack tooling (pymodbus, opendnp3, libiec61850, IEC 104, OpenPLC, ScadaBR, Conpot, Caldera OT)

### Takeaway
pymodbus is very active (3.16.2, 2026-11-03). **opendnp3 has been archived/EOL since 2022-09-01**, which is a trap for anyone copying older testbeds. libiec61850 is maintained (1.6.2.1). MITRE Caldera for OT offers Modbus/DNP3/BACnet/Profinet/IEC 61850 attack plugins but no IEC 104 plugin. Conpot's packaging is stale.

### Cited Findings
- **pymodbus 3.16.2 (2026-11-03)**, BSD-3-Clause, Python ≥3.10. — [PyPI pymodbus](https://pypi.org/project/pymodbus/)
- **opendnp3**: "archived by the owner on Sep 1, 2022", read-only, Apache-2.0. The README states end-of-life and suggests maintaining an internal fork or a commercial library (Step Function I/O). — [dnp3/opendnp3](https://github.com/dnp3/opendnp3)
- DNP3 Python wrappers are stale: `dnp3-python` 0.3.0b2 (2024-11-13); `pydnp3` 0.1.0 (2018). — [PyPI dnp3-python](https://pypi.org/project/dnp3-python/); [PyPI pydnp3](https://pypi.org/project/pydnp3/)
- **libiec61850** latest **1.6.2.1** ("24 Sep", year not shown). — [mz-automation/libiec61850 releases](https://github.com/mz-automation/libiec61850/releases). PyPI `pyiec61850` (unofficial) is at 1.5.2a1 (2023-10-04). — [PyPI pyiec61850](https://pypi.org/project/pyiec61850/)
- **IEC 60870-5-104**: PyPI `c104` 2.2.1 (2025-04-23), GPL-3.0 (Python bindings for lib60870). — [PyPI c104](https://pypi.org/project/c104/)
- **Conpot** (ICS honeypot): PyPI 0.6.0 (2018-08-09, GPL-2). Docker `honeynet/conpot:latest` last updated 2019-02-04. — [PyPI conpot](https://pypi.org/project/conpot/); [Docker Hub honeynet/conpot](https://hub.docker.com/r/honeynet/conpot)
- **MITRE Caldera** latest **v5.3.0** ("24 April"; probably 2025, inferred from v5.1.0 referencing CVE-2025-27364). — [mitre/caldera releases](https://github.com/mitre/caldera/releases)
- **Caldera for OT** plugins: Modbus, DNP3, BACnet, Profinet (DCP only), IEC 61850 (MMS only), and GEMS. Apache-2.0. Installed by cloning into `caldera/plugins` and enabling in `conf/local.yml`. IEC 104 is not listed. — [mitre/caldera-ot](https://github.com/mitre/caldera-ot)

### Inferences
- Recommended protocol stack for a 2026 build: pymodbus (Modbus/TCP), libiec61850 (MMS/GOOSE), c104/lib60870 (IEC 104), and for DNP3 either the archived opendnp3 pinned in a container or Step Function's Rust `dnp3` library (check its licence; not verified here). Caldera-OT provides ready-made ATT&CK-for-ICS-style adversary actions against Modbus, DNP3 and IEC 61850 targets.
- Conpot is effectively unmaintained as packaged; use it only as a reference.

### Gaps
- OpenPLC (v3 vs the newer Autonomy-Logic runtime/v4) status: openplcproject.com reset the connection and the GitHub API was blocked, so this was not verified.
- ScadaBR status not verified.
- Step Function I/O Rust `dnp3` licence and version not verified.
- libiec61850 and lib60870 licensing (GPLv3 + commercial dual licence is commonly reported) not confirmed from the fetched page.

## Q4. Telemetry, visualization and web stack (Grafana/InfluxDB/TimescaleDB, Cytoscape.js, React Flow, Sigma.js, FastAPI/React)

### Takeaway
The front-end and API libraries are all actively released under MIT. I could not verify the telemetry DB and Grafana versions in this session.

### Cited Findings
- `cytoscape` **3.34.4 (2026-10-15)**, MIT. — [npm cytoscape](https://www.npmjs.com/package/cytoscape)
- `@xyflow/react` (React Flow v12) **12.12.1 (2026-11-02)**, MIT. The legacy `reactflow` package was last released at 11.11.4 (2024-06-20). — [npm @xyflow/react](https://www.npmjs.com/package/@xyflow/react); [npm reactflow](https://www.npmjs.com/package/reactflow)
- `sigma` **4.0.4 (2026-10-27)**, MIT. `graphology` 0.26.0 (2025-01-26). — [npm sigma](https://www.npmjs.com/package/sigma); [npm graphology](https://www.npmjs.com/package/graphology)
- `react` **19.3.1 (2026-10-14)**, MIT. `fastapi` **0.162.0 (2026-10-23)**, MIT, Python ≥3.10. — [npm react](https://www.npmjs.com/package/react); [PyPI fastapi](https://pypi.org/project/fastapi/)

### Inferences
- Topology views: React Flow suits editable topology diagrams of tens to hundreds of nodes; Sigma.js (WebGL) suits large graphs; Cytoscape.js sits between them and has graph algorithms built in. This is general knowledge and was not benchmarked here.

### Gaps
- Grafana, InfluxDB (v3 licensing changes) and TimescaleDB versions and licences were not verified (GitHub blocked; not searched due to budget).

## Q5. Competing / complementary frameworks and testbeds (non-GridAttackSim groups)

### Takeaway
No 2024–2026 open-source extension of GridAttackSim by other groups was found. Citations are mainly surveys. The same JAIST group followed up with GridAttackAnalyzer (attack graphs, 2022). The notable current competitors are Sandia SCEPTRE (open-source phenix/minimega), SG-ML (auto-generated smart-grid cyber ranges, built on the iTrust EPIC testbed, 2025 preprint), mosaik-based co-simulation, and a growing family of RL cyber-defense gyms (CybORG/CAGE, CyberBattleSim, NASim, Cyberwheel) plus Grid2Op for grid control.

### Cited Findings
**GridAttackSim lineage and citations**
- Original paper: Le et al., *Electronics* 9(8):1218, 2020. Stack: GridLAB-D + ns-3 + FNCS. Code at crond-jaist/GridAttackSim. — [MDPI](https://www.mdpi.com/2079-9292/9/8/1218); [GitHub](https://github.com/crond-jaist/GridAttackSim)
- GridAttackAnalyzer (same group, *Sensors* 2022) takes an attack-graph approach. — [PMC9268941](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9268941/)
- Cited in a 2024 survey on smart-grid simulation and vulnerability testing (describes its six modules) and in a 2025 arXiv survey on LLM-based autonomous cyberattack agents. — [Preprints.org 202402.0047](https://www.preprints.org/manuscript/202402.0047); [arXiv 2505.12786](https://arxiv.org/pdf/2505.12786)
- A "Smart Grid Cybersecurity Experimentation: Architecture and Methodology" paper appears alongside it (ResearchGate). — [ResearchGate 352838964](https://www.researchgate.net/publication/352838964_Smart_Grid_Cybersecurity_Experimentation_Architecture_and_Methodology) (author group not verified)

**Sandia SCEPTRE / phenix / minimega**
- SCEPTRE is Sandia's ICS/SCADA emulation capability. It captures cyber-physical impacts and supports hardware-in-the-loop. Open-source packages are on Sandia's GitHub; Firewheel is excluded from open source. — [Sandia Emulytics](https://sandia.gov/emulytics); [SCEPTRE docs](https://sandialabs.github.io/sceptre-docs); [SCEPTRE providers](https://sandialabs.github.io/sceptre-docs/13-providers.html)
- 2025 OSTI paper "SCEPTRE: A Cyber-Physical Emulation Capability". — [OSTI 2999077](https://www.osti.gov/biblio/2999077)

**SG-ML (iTrust/SUTD + partners)**
- XML modelling language (built on IEC 61850 SCL and IEC 61131 PLCopen XML, plus custom schemas for attack injection and scenarios). A processor instantiates a smart-grid cyber range from the model; it was demonstrated by replicating the **EPIC** testbed. arXiv 2509.10568 (Sept 2025, preprint), earlier 2404.00869 (2024). — [arXiv 2509.10568](https://arxiv.org/html/2509.10568v1); [arXiv 2404.00869 review](https://fugumt.com/fugumt/paper_check/2404.00869v1_enmode)

**DSSnet, PowerCyber, other testbeds**
- DSSnet pairs a power distribution simulator with an SDN network emulator, synchronized by container-based virtual time. — [CPS-VO](https://archive.cps-vo.org/node/56336); [OSTI 1493432](https://www.osti.gov/biblio/1493432)
- An RWTH poster (2020) criticizes DSSnet for abstracting away energy-sector protocols. — [RWTH poster](https://www.comsys.rwth-aachen.de/fileadmin/papers/2020/2020-henze-ccs-cybersecurity.pdf)
- PowerCyber: a hardware-based testbed at Iowa State, federated with US Army Research Laboratory resources. — [IET CPS (DOAJ)](https://doaj.org/article/13e4f237859446b596f86b18aa3b0952)
- A 2024 arXiv paper on multi-stage attack/defense simulation in smart grids lists OMNeT++, ns-3 and mosaik as software co-simulation tools. — [arXiv 2412.06255](https://arxiv.org/pdf/2412.06255)

**PNNL GridSTAGE**
- Exists: github.com/pnnl/GridSTAGE. A MATLAB + Power System Toolbox framework that generates adversarial PMU data (FDI: ramp, step, random, replay, freezing; DoS: delay, packet loss) on, e.g., IEEE 68-bus. A third-party listing shows the repo last updated around Aug 2022. — [OSTI 1788186](https://www.osti.gov/biblio/1788186); [relatedrepos listing](https://relatedrepos.com/gh/pnnl/GridSTAGE)

**RL / autonomous cyber-defense gyms**
- **CAGE Challenge 4** (CybORG): released 20 Feb 2024, competition ended 10 May 2024, results published 2025. — [cage-challenge-4](https://github.com/cage-challenge/cage-challenge-4)
- **CyberBattleSim** (Microsoft): MIT, Docker supported, not archived. It models abstract enterprise networks, not OT. — [microsoft/CyberBattleSim](https://github.com/microsoft/CyberBattleSim)
- **NASim**: PyPI 0.12.0 (2023-05-14), MIT, stale. — [PyPI nasim](https://pypi.org/project/nasim/)
- **Cyberwheel** (ORNL): MIT, a networkx-based RL simulator with simulation and emulation (CSET '24), with train/evaluate/visualizer/run modes. — [ORNL publication](https://www.ornl.gov/publication/towards-high-fidelity-training-environment-autonomous-cyber-defense-agents); [CSET'24 slides](https://cset24.isi.edu/slides/cset2024-slides-weber.pdf); [ORNL/cyberwheel (via listing)](https://awesome.ecosyste.ms/projects/github.com%2Fornl%2Fcyberwheel)
- **Grid2Op** (RTE): `grid2op` **1.12.6 (2026-10-14)**, MPL-2.0. `lightsim2grid` 1.3.0 (2026-11-03). This is power-grid control RL; it can model adversarial line attacks, but it is not a network/cyber simulator. — [PyPI grid2op](https://pypi.org/project/grid2op/); [PyPI lightsim2grid](https://pypi.org/project/lightsim2grid/)

### Inferences
- No single open-source tool clearly "surpasses" GridAttackSim on all axes. SCEPTRE/phenix exceeds it on emulation fidelity (real protocol stacks, HIL) but is heavy. SG-ML exceeds it on automated range generation from standard IEC models, though its code release is unverified. mosaik-based platforms exceed it on maintainability and Python integration. RL gyms (CybORG, Cyberwheel) add autonomous agents but lack power-physics coupling. Combining an RL gym with a grid simulator (Grid2Op/pandapower) is an open niche.
- Reusable backends that are actively maintained and open source as of late 2026: HELICS, TESP (Docker), mosaik, pandapower/SimBench, dss-python, ns-3 (without the HELICS module), OMNeT++, containerlab, CORE, pymodbus, libiec61850, Caldera + caldera-ot, Grid2Op.

### Gaps
- **SGSim**: no source found confirming a smart-grid simulator by this name. Do not cite it without verification.
- **SecureCPS**, **CyPhER**, **CybORG++**, **Cyberwheel** release dates, and EU smart-grid cyber-range projects were not verified in this session.
- No papers that explicitly extend GridAttackSim's codebase were found. Google Scholar citation lists were not accessible.
- Whether SG-ML's processor code is publicly released is unverified.
- EPIC/SWaT access terms (iTrust testbeds are physical; datasets are available on request) were not verified here.
- INL testbeds (e.g. CyberCore) were not researched.
