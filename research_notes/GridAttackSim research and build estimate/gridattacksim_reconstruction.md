# GridAttackSim: reconstruction of architecture and implementation (Le, Anwar, Loke, Beuran, Tan, Electronics 2020, 9(8), 1218)

Source base and labelling conventions (read first):
- **Paper full text.** mdpi.com returned HTTP 403 (Akamai block) for the /htm, /pdf and /xml URLs from this environment. The full 21-page published PDF was obtained from co-author R. Beuran's JAIST page ([JAIST mirror PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)). Its PDF metadata title is "GridAttackSim: A Cyber Attack Simulation Framework for Smart Grids", it was created on 2020-07-29 (the publication date), and it carries the MDPI header "Electronics 2020, 9, 1218; doi:10.3390/electronics9081218". It is the published version. Canonical page: [MDPI](https://www.mdpi.com/2079-9292/9/8/1218). A Deakin repository copy also exists ([Deakin figshare](https://deakin.figshare.com/articles/journal_contribution/GridAttackSim_a_cyber_attack_simulation_framework_for_smart_grids/20695144)).
- **Additional primary sources found:**
  - T. D. Le's JAIST doctoral dissertation, "Smart Grid Cybersecurity Experimentation: Architecture and Methodology" (March 2021, 123 pp.). Chapter 4 is an expanded GridAttackSim chapter ([JAIST dspace](https://dspace02.jaist.ac.jp/dspace/bitstream/10119/17476/12/paper.pdf)).
  - The **official source code**, which was released after the paper: [github.com/crond-jaist/GridAttackSim](https://github.com/crond-jaist/GridAttackSim), tag `1.0`, commits dated 2021-03-05 to 2022-02-15, BSD-3-Clause. I cloned and read the repository.
- **Labels.** [Paper §X] = documented in the Electronics paper. [Dissertation §X] = documented in the 2021 thesis. [Repo: file] = observed in the released code (an external primary source). [External source] = third-party documentation. [Inferred] = my reasoning, not stated by the authors.
- **No arXiv preprint found.** Searches for GridAttackSim returned only MDPI, Deakin, JAIST and aggregator copies.

---

## 1. Summary of every figure, table, listing and algorithm in the paper

### Takeaway
The paper has 6 figures and 3 tables, and no numbered algorithms or code listings. Figure 2 is the only listing, an fncs.zpl example shown as a figure. The quantitative content is concentrated in Table 3 (the attack-to-variable mapping) and Figures 5–6 (the case-study results).

### Cited Findings
- **Figure 1: "The smart grid attack co-simulation framework — architecture of GridAttackSim."** [Paper §3] — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
  - Top band "Scenario Generation":
    - Attack Pattern Library, with sub-boxes Attack Type, Attack Target and Attack Schedule.
    - Preprocessing: a raw GridLAB-D .glm, with the parameters Prefix, Total Houses and Market ID, feeds "Add Controller Objects", which produces the main GridLAB-D .glm, and "Generate FNCS Communication Configuration files", which produces a .txt file and a .zpl file.
    - The main ns-3 (.cc) file.
    - These outputs become the "Network Model" and "Grid Model".
  - Middle: the "Model Manager".
  - Bottom band "Smart Grid Simulation":
    - ns-3 process: ns-3 core, Time Sync Module, Simulated Communication Network, Network Application Module.
    - FNCS Broker in the centre.
    - GridLAB-D process: GridLAB-D core, Time Sync Module, Interface Module, Other GridLAB-D Modules.
- **Figure 2: "An example of the fncs.zpl format."** [Paper §3.1] It is a commented ZPL listing with these fields:
  - `name = GLD1`: required, and unique across the co-simulation.
  - `time_delta = 1s`: the smallest time step of the simulator.
  - `broker = tcp://localhost:5570`
  - a `values` block holding `lookup_key`, `topic = some_topic`, `default = 50`, `type = int` (marked "currently unused") and `list = false` (whether incoming values queue up or overwrite).
  - This is the generic FNCS ZPL template, not a GridAttackSim-specific file. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Figure 3: "Smart grid attack co-simulation (GridAttackSim) desktop application (GUI)."** [Paper §4] It is a screenshot only. The repo screenshot and code show:
  - combo boxes for Smart Grid Model, Application, Attack Category and Attack Type
  - buttons Show Model, Run Simulation, Load Results and Show Charts
  - an "Output Files" list box

  — [Repo README](https://github.com/crond-jaist/GridAttackSim/blob/master/README.md); [Repo GridAttackSim.py](https://github.com/crond-jaist/GridAttackSim/blob/master/GridAttackSim.py)
- **Figure 4: "(a) The network model and (b) the power grid model of IEEE 13 node test feeder with 73 Houses."** [Paper §4.1]
  - Panel (a) shows four clusters (Cluster 1–3 with 20 nodes each, Cluster 4 with 13 nodes). Each cluster is a CSMA/CD bus whose "Index 0" node connects by point-to-point links to a central (market/aggregator) node.
  - Panel (b) is a graph rendering of the 13-node GLM. It is probably produced by the bundled `glmMap.py`, a PNNL GLM-to-Graphviz script [Inferred, from repo].
  - The dissertation's version (Fig. 4.4) labels the clusters "CSMA/CA" instead of "CSMA/CD". The two documents are inconsistent here. — [Dissertation](https://dspace02.jaist.ac.jp/dspace/bitstream/10119/17476/12/paper.pdf)
- **Figure 5: "Channel jamming attack with the simple test feeder."** [Paper §5.1] It plots normal and jamming runs over 24 h:
  - (a) total load in kW, y-axis 0–2000
  - (b) market-clearing quantity
  - (c) market-clearing price in $/kWh, 0–4
  - (d) a bar chart of economic impact: energy consumption 103.2% and bill amount 97.1%, against 100% for normal operation
- **Figure 6: "Injection Attack with IEEE 13 Node."** [Paper §5.2] It plots the 13:00–22:00 window for normal operation, a High Maximum Capacity Bid (200 kW) and a Low Maximum Capacity Bid (50 kW):
  - (a) total load, y-axis 0–250 kW
  - (b) clearing quantity
  - (c) clearing price
  - (d) bars: energy 107.6% (high) and 103.2% (low); bill 18.1% (high) and 153.1% (low); normal = 100%
- **Table 1: "Co-simulation tools for smart grid."** [Paper §2] 19 tools with last update, power simulator, network simulator, OS and supported attacks:
  - EPOCHS (2006, PSLF/ns-2)
  - Hybrid Simulator (2011, OpenDSS/ns-2)
  - VPNET (2011, VTB/OPNET)
  - PowerNet (2011, Modelica/ns-2)
  - TASSCS (2011, PowerWorld/RINSE; compromised HMI, DoS)
  - GECO (2012, PSLF/ns-2)
  - SCADASim (2012, MATLAB-Simulink/OMNeT++; DoS, MitM, eavesdropping, spoofing)
  - NeSSi2 (2013; DoS)
  - SGsim (2014, OpenDSS/OMNeT++)
  - GridSpice (2014, MATPOWER+GridLAB-D)
  - ScorePlus (2015, GridLAB-D/CORE; malicious code)
  - InterPSS (2015)
  - Simulating Smart Grid (2015, GridLAB-D/ns-2)
  - ASTORIA (2016, PYPOWER/ns-3; malicious software infection, DoS)
  - CPSA (2017, MATLAB+PowerWorld/GridSim; Trojans)
  - FNCS (2018, GridLAB-D/ns-3; none)
  - SimApi (2019, EnergyPlus)
  - ERIGrid (2019, PowerFactory+MATLAB/ns-3+mosaik)
  - HELICS (2019, GridLAB-D/ns-3; Win/Linux/macOS; none)

  — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Table 2: "Attack pattern library structure."** [Paper §3.2]
  - Attack Type: `type_id`, `type_name`, `description`, `affected_value` ("the values need to be changed on the simulation system to conduct an attack")
  - Attack Target: `target_id`, `target_name`, `description`, `file` ("core system files need to be over-written")
  - Attack Schedule: `schedule_id`, `description`, `file` ("the .glm file where the attack schedule is defined"), `start_time`, `end_time`
- **Table 3: "The configuration of the attack pattern library."** [Paper §4.3] Columns are Type / Variants / Assets Affected / Emulation Approach / Target Components / Variables Affected:
  - Channel Jamming. Variant: DDoS. Asset: communication networks. Emulation: data rate/delay. Targets and variables:
    - Cluster: `data_rate_cluster`, `delay_cluster`
    - Point-to-Point: `data_rate_point_to_point`, `delay_point_to_point`
    - Cluster + P2P combination: all four
  - Malicious Code. Variants: exploit kits, virus, worms, trojans, malware. Asset: end-point systems. Emulation: price. Target: Control Center. Variables: `proxy_clear_price`, `proxy_price_cap`.
  - Injection Attacks, two variants:
    - Malicious code injection: asset control systems, emulation "Maximum Capacity Bid", target the auction system, variable `max_capacity_reference_bid_quantity`.
    - Malformed data injection: asset end-point systems, emulation "Comfort Level", target the controller inside the house, variable `comfort_level`.
  - Replay of Messages. Asset: communication networks. Emulation: data rate/delay. Targets: Cluster (`delay_cluster`) and Point-to-Point (`delay_point_to_point`).
- **Abbreviations list and 30 references.** No numbered algorithms or code listings. No "Supplementary Materials" or "Data Availability Statement" sections. Back matter consists only of Author Contributions, "Funding: This research received no external funding" and Conflicts of Interest. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Additional tables and figures in the dissertation (Chapter 4 and Chapter 6):**
  - Table 4.2 extends paper Table 3 with "Normal Value" and "New Value" columns and adds a DNS-attack group.
  - Table 6.1 is a functionality comparison: GridAttackSim is the only tool with "Y" in all of extendable power-grid model, network model, attack type and attack schedule.
  - Fig. 6.1 is the SUS questionnaire.
  - Table 6.3 gives the SUS results.

  — [Dissertation](https://dspace02.jaist.ac.jp/dspace/bitstream/10119/17476/12/paper.pdf)

### Inferences
- [Inferred] Figure 1 maps almost one-to-one onto the released files:
  - "Add Controller Objects" corresponds to adding `auction` and `fncs_msg` objects to the GLM.
  - ".txt file" is `fncs_msg.txt`.
  - ".zpl file" is `fncs.zpl`.
  - "Main ns-3 (.cc) file" is `ns-3.cc`.
  - "Model Manager" corresponds to `GridAttackSim.py` together with `attack_broker.py`.

### Gaps
- Figures 3–6 are raster or vector images. Exact time-series values beyond those quoted in the text cannot be extracted reliably from the PDF text layer.

---

## 2. Physical grid modelling (GridLAB-D models, feeders, houses, market, GLM files)

### Takeaway
The models are small PNNL/IEEE distribution feeders with residential houses whose HVACs bid into a GridLAB-D `market` module double-auction (transactive) market. The paper describes three feeder types: the PNNL "simple test feeder", IEEE 4-node and IEEE 13-node. The release ships five GLM models. There are no IEEE 123-node or PNNL taxonomy feeders in GridAttackSim; a taxonomy feeder, R4-12.47-2, appears only in the sister tool GridAttackAnalyzer.

### Cited Findings
- **Preprocessing input.** [Paper §3.1] The input is "a raw IEEE test feeder file in GridLAB-D format (.glm) … initially created by PNNL". "GLM append" adds the `auction` object and the `fncs_msg` object to connect GridLAB-D to the FNCS broker. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Feeders.** [Paper §4.1.2] Simple test feeder plus IEEE 4-node and 13-node test feeders.
  - Simple test feeder: "created by PNNL to test the function of FNCS". It has a three-phase swing bus at 7200 V nominal, 1500 kW per phase (4500 kW total), a total-load meter between substation transformer and loads, and residential loads on triplex meters.
  - IEEE 13-node: 4.16 kV, with shunt capacitors, regulators and unbalanced loads. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Houses.** [Paper §4.1] "Each smart grid model has a specific number of houses that act as residential loads… equipped with a HVAC system, which is controlled by a specific passive controller." — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Market (DR/DP).** [Paper §4.2]
  - Houses submit quantity/price bids to an auction. The substation sets reference prices and maximum capacity. The supplier bids maximum power and price.
  - The market cycle is "typically from 5 to 15 min". Supply bids are sorted ascending and demand bids descending; the intersection gives the clearing price and quantity.
  - The HVAC controller then shifts its thermostat band or hysteresis.
  - "All bids and price signals are transmitted via the … ns-3 model." — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Scale claim.** [Paper §7] "The current framework supports three types of test feeder… The maximum number of houses … can be up to 1000 houses." — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Released models.** [Repo: Database/] Five models are selectable in the GUI: `1_Node_255_Houses`, `4_Nodes_1_House`, `4_Nodes_492_Houses`, `13_Nodes_15_Houses` and `13_Nodes_73_Houses`. — [Repo developer_guide.md](https://github.com/crond-jaist/GridAttackSim/blob/master/developer_guide.md)
- **Counted objects in the release** (`object house` / `object controller` / LinkModel size):
  - 13_Nodes_73: 73 / 73 / 73
  - 13_Nodes_15: 15 / 15 / 15
  - 4_Nodes_1: 1 / 1 / 1
  - 4_Nodes_492: 500 houses / 492 controllers / 492
  - 1_Node_255_Houses: 250 / 250 / 250, with prefix `C250_` and market `Market2`

  The paper says 255 houses and a 250-node network for the simple feeder. — [Repo Database](https://github.com/crond-jaist/GridAttackSim/tree/master/Database)
- **13-node 73-house GLM** [Repo: Database/13_Nodes_73_Houses/GridLab-D.glm]:
  - Clock: 2009-07-21 00:00 to 2009-07-22 00:00 (timezone EST+5EDT).
  - Settings: `#set minimum_timestep=60`; modules connection, tape, climate, residential, powerflow (FBS solver) and market.
  - Climate: `climate` object with `WA-Seattle.tmy2`.
  - `auction Market_1`:
    - `unit kW; period 300; price_cap 3.78; init_price 0.042676; init_stdev 2000`
    - `capacity_reference_object substation_transformer`
    - a `player` driving `capacity_reference_bid_price` from `AEP_RT_LMP.player`
    - `max_capacity_reference_bid_quantity 250`
    - a recorder writing `capacity_reference_bid_price, current_market.clearing_price, current_market.clearing_quantity` every 60 s to `baseprice_clearedprice_clearedquantity.csv`
  - Substation transformer recorder: `power_out_real` every 60 s to `totalload.csv`.
  - Each house has a market `controller` (`bid_mode ON; control_mode RAMP; period 300; proxy_clear_price 0.042676; proxy_price_cap 3.78; range_high 5; range_low -3; slider_setting 0.5`).
  - Water heaters have `passive_controller` objects (`control_mode PROBABILITY_OFF; comfort_level 1.00`). — [Repo GLM](https://github.com/crond-jaist/GridAttackSim/blob/master/Database/13_Nodes_73_Houses/GridLab-D.glm)
- **Simple test feeder GLM** [Repo: Database/1_Node_255_Houses/GridLab-D.glm]:
  - The same 24 h window, but weather from `ColumbusWeather2009_2a.csv` rather than Seattle.
  - `max_capacity_reference_bid_quantity 1500`, with a commented-out alternative bound to a GLM schedule `max_capacity_reference_bid_quantity_attack`, defined in an included `max_capacity_reference_bid_quantity.glm`.
  - The directory README is the FNCS-Tutorial README ("Step-by-step guide for building and running FNCS, ns-3, and GridLAB-D"). — [Repo 1_Node_255_Houses](https://github.com/crond-jaist/GridAttackSim/tree/master/Database/1_Node_255_Houses)
- **Sister tool's feeder.** [Dissertation §8.1] GridAttackAnalyzer, not GridAttackSim, used "PNNL Taxonomy Feeders R4-12.47-2". — [Dissertation](https://dspace02.jaist.ac.jp/dspace/bitstream/10119/17476/12/paper.pdf)

### Inferences
- [Inferred] The model set is essentially the PNNL FNCS tutorial "demo-gld-ns3" case (one market, ~250 houses), extended with IEEE 4- and 13-node variants. The evidence:
  - the tutorial README is copied verbatim
  - the commented ns-3.19 `firstN` build lines in `compile-ns3.sh`
  - `ns-3.cc` is structurally identical to the tutorial's `firstN.cc`
- [Inferred] "Passive controller" in the paper is loose wording. HVAC devices actually use GridLAB-D's market `controller` (RAMP mode). `passive_controller` is used only on water heaters, which is where `comfort_level` lives. The "malformed data injection / comfort level" attack therefore affects water-heater load shedding, not the HVAC thermostat.
- [Inferred] The paper says the 13-node default maximum capacity bid is 150 kW, but the released 73-house GLM contains 250 kW. The released file may be a leftover from an attack run (the dissertation lists 250 kW as an attack value) and does not match the paper's baseline.
- [Inferred] The "up to 1000 houses" claim is not demonstrated in the release, whose largest model has 492 controllers. The ns-3 code limits a market to 255 groups of 20 (5,100 nodes).

### Gaps
- No IEEE 123-node, IEEE 37-node or taxonomy feeder is used in GridAttackSim. No smart-meter object model beyond GridLAB-D `triplex_meter` and `meter` is described.
- The paper does not state the GridLAB-D version. The install guide builds GridLAB-D from the `develop` branch of gridlab-d/gridlab-d with FNCS (around 2019–2020, likely the 4.x line [Inferred]).

---

## 3. Communication network modelling (ns-3 version, topology, protocols, node mapping)

### Takeaway
The network is a simple wired ns-3 model:
- one ns-3 node per house controller (smart meter)
- houses grouped into CSMA buses of 20 (each with a 21st edge node, index 0)
- each bus's edge node joined by a point-to-point link to a single market/aggregator node
- UDP transport, static plus Nix-vector routing

It uses PNNL's FNCS-patched ns-3.26 and its `FncsApplication`, which carries GridLAB-D messages as UDP packets so that they experience network delay and loss.

### Cited Findings
- **Topology and protocols.** [Paper §4.1.1]
  - Nodes represent smart meters in residential loads. They are organized into small groups forming local networks.
  - Each meter has an IP address "mapped to the given name for each residential load from the GridLAB-D model".
  - Group data are "routed to a data aggregator by an edge network node through a point-to-point communication connection".
  - UDP was chosen over TCP for lower delay.
  - "The ns-3 CSMA device models a simple Ethernet bus network … CSMA/CD"; the CSMA model is used "to define data rates and delay values". — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Defaults stated in the paper.** [Paper §5] Data rate is 4 Mbps for point-to-point and 10 Gbps for the LANs; delay is 3 ms for both. The dissertation's Table 4.2 instead lists the cluster default as **10 Mbps**. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf); [Dissertation](https://dspace02.jaist.ac.jp/dspace/bitstream/10119/17476/12/paper.pdf)
- **ns-3 version.** [Repo: installation_guide.md; compile-ns3.sh]
  - The guide clones `https://github.com/FNCS/ns-3.26` ("our FNCS version of ns-3"), configured with `--with-fncs --with-zmq --disable-python`.
  - The model is compiled with g++ against `ns3.26-*-debug` libraries: applications, fncs, nix-vector-routing, internet, bridge, csma, point-to-point, mpi, stats, network, core.
  - It links `-lfncs -lczmq -lzmq`. — [Repo installation_guide.md](https://github.com/crond-jaist/GridAttackSim/blob/master/installation_guide.md); [Repo compile-ns3.sh](https://github.com/crond-jaist/GridAttackSim/blob/master/Database/13_Nodes_73_Houses/compile-ns3.sh)
- **Network construction in `ns-3.cc`.** [Repo: Database/13_Nodes_73_Houses/ns-3.cc]
  - It reads `LinkModelGLDNS3.txt` (e.g., `73 Market_1 HOUSE_`) and computes groups = (n+19)/20.
  - Per group it creates 21 CSMA nodes with subnet `10.<net>.<group>.0/24`.
  - A single market node gets a P2P link to each group's node 0, with subnet `11.<net>.<group>.0/24`.
  - Routing: `Ipv4ListRoutingHelper` (static, priority 0; NixVector, priority 10).
  - It installs `FncsApplicationHelper(prefix, 1)` on the 20 host nodes per group (named `HOUSE_1…`) and on the market node (named after the market).
  - The simulator implementation is `FncsSimulatorImpl`. Applications run from 0 to 259200 s. — [Repo ns-3.cc](https://github.com/crond-jaist/GridAttackSim/blob/master/Database/13_Nodes_73_Houses/ns-3.cc)
- **Default link parameters in code.** [Repo: ns-3.cc]
  - `data_rate_peer_to_peer = 40000000;//40000000 bps = 4 Mbps` (the value is actually 40 Mbps)
  - `delay_peer_to_peer = 3`
  - `data_rate_cluster = 10000000; //10 Mbps`
  - `delay_cluster = 3`
  - In `1_Node_255_Houses/ns-3.cc` these are hard-coded instead: CSMA `DataRateValue(10000000)` with 3 ms delay, and P2P `"4Mbps"` with `"3ms"`. — [Repo ns-3.cc](https://github.com/crond-jaist/GridAttackSim/blob/master/Database/13_Nodes_73_Houses/ns-3.cc)
- **How FncsApplication carries messages.** [External source: FNCS/ns-3.26]
  - The FNCS simulator implementation polls `fncs::get_events()`.
  - For topics of the form `simname/from@to/topic`, it looks up the `FncsApplication` instances named `fncs_<from>` and `fncs_<to>`. It then calls `from_app->Send(to_app, topic, value)`, which packs `topic=value` into a UDP packet and schedules `Socket::SendTo` to the destination node's address.
  - On receipt, `HandleRead` calls `fncs::publish(topic, value)`, which delivers the message on to GridLAB-D.
  - So the delay and loss that GridLAB-D sees come from the ns-3 path. — [FNCS ns-3.26 repo](https://github.com/FNCS/ns-3.26) (files `src/fncs/model/fncs-simulator-impl.cc`, `src/applications/model/fncs-application.cc`)

### Inferences
- [Inferred] The paper's 4 Mbps / 10 Gbps / 3 ms defaults, the thesis's 4 Mbps / 10 Mbps, and the code's 40 Mbps (comment "4 Mbps") / 10 Mbps disagree. Anyone rebuilding should treat the paper numbers as nominal and verify the values against the code they actually run.
- [Inferred] The network is wired (CSMA bus plus P2P). The "wireless jamming" story of §5.1 is therefore emulated abstractly by degrading wired-link rate and delay; there is no SINR or PHY model. The "CSMA/CA" label in the dissertation figure suggests the authors thought of it as wireless-like, but ns-3's `CsmaNetDevice` is an Ethernet-style bus.
- [Inferred] Every group always allocates 20 host nodes, so 73 houses give 80 FNCS apps. Unused names (HOUSE_74..80) simply receive no traffic.
- [Inferred] Packet loss in the jamming case (−20.14% delivery ratio) presumably comes from queue overflow on the lower-rate links. The paper does not say which queue model or how delivery ratio was measured.

### Gaps
- No ns-3 trace, pcap or FlowMonitor configuration is described or found in the code. How the "packet delivery ratio" was computed is undocumented.
- No IEC 61850, DNP3, Modbus or other SCADA/AMI protocol is modelled; the only messages are FNCS topic=value strings over UDP.

---

## 4. FNCS co-simulation coupling (broker, time sync, message types, ZPL/config)

### Takeaway
There are two federates, ns-3 (`ns3_1`) and GridLAB-D, plus `fncs_broker 2`, each launched in its own xterm.
- GridLAB-D's `connection` module object `fncs_msg` is configured by `fncs_msg.txt`. It routes the market's clearing price, market ID and 24 h mean/stdev to each house, and subscribes each controller's bid and the house's proxy_* properties to ns-3-relayed topics.
- ns-3's `fncs.zpl` subscribes to every `HOUSE_i@Market_1/*` topic.
- Time is synchronised by FNCS's conservative time_request/grant protocol.

### Cited Findings
- **Preprocessing outputs.** [Paper §3.1]
  - The communication-config generator takes market ID, total number of houses and controller name prefix as input, and outputs a .txt (ns-3 ↔ broker) and a .zpl.
  - The .zpl subscribes to "market ID, submit bid state, market clearing price, average price, and the price's standard deviation".
  - Each simulator needs its own fncs.zpl in its working directory. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Broker role.** [Paper §3.5] Every federated simulator registers with the broker. "The time synchronization steps are calculated in conjunction with the next time steps in the simulators and depending on whether there are messages in transit." — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **ZPL contents.** [Repo: fncs.zpl, generated by creat_zpl_file.py]
  - `name = ns3_1`, `time_delta = 1ns`, `broker = tcp://localhost:5570`.
  - Per house i, values for `fncs_msg/HOUSE_i@Market_1/submit_bid_state` and `fncs_msg/Market_1@HOUSE_i/{clearPrice,mktID,avgPrice,stdevPrice}` (type string, list false). That is 2194 lines for 73 houses.
  - The generator hard-codes `while (index < 74)` and `Market_1`/`HOUSE_`, so each model has its own copy.
  - There is a typo `ttype = string` on the clearPrice entries. — [Repo fncs.zpl](https://github.com/crond-jaist/GridAttackSim/blob/master/Database/13_Nodes_73_Houses/fncs.zpl); [Repo creat_zpl_file.py](https://github.com/crond-jaist/GridAttackSim/blob/master/Database/13_Nodes_73_Houses/creat_zpl_file.py)
- **GridLAB-D side.** [Repo: fncs_msg.txt, GLM]
  - The GLM declares `object fncs_msg { parent Market_1; route "function:controller/submit_bid_state -> auction/submit_bid_state"; option "transport:hostname localhost, port 5570"; configure fncs_msg.txt; }`.
  - `fncs_msg.txt` (730 lines for 73 houses) contains, per house:
    - `route "commit:Market_1.current_market.clearing_price -> HOUSE_i/clearPrice; 0"`
    - routes for `market_id`, `current_price_mean_24h` (listed twice) and `current_price_stdev_24h`
    - `subscribe "function:auction/submit_bid_state <- ns3_1/ONE_NODE/HOUSE_i@Market_1/submit_bid_state"`
    - `subscribe "precommit:HOUSE_i.proxy_clear_price <- ns3_1/ONE_NODE/Market_1@HOUSE_i/clearPrice"`, plus the same for `proxy_market_id`, `proxy_average` and `proxy_standard_deviation`. — [Repo fncs_msg.txt](https://github.com/crond-jaist/GridAttackSim/blob/master/Database/13_Nodes_73_Houses/fncs_msg.txt)
- **Launch script.** [Repo: run.sh]
  - Sets `FNCS_LOG_STDOUT=no` and `FNCS_LOG_FILE=yes`.
  - Runs `xterm -e ./run_ns-3 LinkModelGLDNS3.txt &`, `xterm -e gridlabd run_GridLab-D.glm &` and `xterm -e fncs_broker 2 &`. — [Repo run.sh](https://github.com/crond-jaist/GridAttackSim/blob/master/Database/13_Nodes_73_Houses/run.sh)
- **ns-3 side of time sync.** [External source: FNCS ns-3.26] `FncsSimulatorImpl` requests the next event time with `fncs::time_request(NextTs())`. It advances to the granted time and then drains `fncs::get_events()`. — [FNCS ns-3.26](https://github.com/FNCS/ns-3.26)
- **Speed claim.** [Paper §2] The precursor study found that GridLAB-D+ns-3+FNCS "can improve the speed of co-simulation by 20%". The baseline for this comparison is not given. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)

### Inferences
- [Inferred] The message types are therefore exactly five string topics per house:
  - `submit_bid_state` (house → market)
  - `clearPrice`, `mktID`, `avgPrice`, `stdevPrice` (market → house)
- [Inferred] There is no explicit YAML config. All configuration is ZPL plus GridLAB-D's `fncs_msg` route/subscribe text. (YAML config arrived later in FNCS/TESP and HELICS uses JSON.)
- [Inferred] GridLAB-D's step (`minimum_timestep=60`) and the market period (300 s) bound how often messages are generated. ns-3 runs at 1 ns resolution. Delays of 3–400 ms matter only when they push a bid past the market-clearing instant, which is consistent with the paper's explanation of "delayed re-bids".

### Gaps
- The paper does not give the FNCS version. The install guide clones FNCS master, whose last tag is v2.3.2 (2017-04-20) [External source, below].
- No measurement of co-simulation wall-clock time per run is reported.

---

## 5. Attack injection: attack library, implementation, parameters, scheduling

### Takeaway
Every attack is implemented as a **static, pre-run parameter overwrite**: a text substitution in a copy of the ns-3 C++ source (link data rate and delay) or of the GLM (market or controller properties), followed by recompile and rerun. There is no packet-level attack logic (no packet dropping, modification, spoofing or genuine replay), and none of the released code applies the JSON start/end time. The "attack schedule" is documented in the paper, but the release shows it only as unused GLM schedule files and a commented-out schedule hook.

### Cited Findings
- **Library format.** [Paper §3.2] A "standardized configuration JSON format file" defines attack type ("what"), target ("where") and schedule ("when"), following Tundis et al. 2017 [ref 16]. It is claimed to allow "reconfiguration at run-time". — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Taxonomy.** [Paper §4.3]
  - Categories come from ENISA (2015), which builds on NISTIR 7628 among others. Two of ENISA's six categories are used: (1) nefarious activity and (2) eavesdropping/interception/hijacking.
  - "The nine typical attack types… are organized into four groups, comprising channel jamming, malicious code, injection attacks, and replay of messages."
  - "The attack simulations … have been conducted by altering the input values of GridLAB-D and ns-3 simulators." — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **The nine library entries as released** [Repo: attack_library.json v1.0, "created": "2020-01-01"]. Each entry is listed as id, name, affected values, file:
  1. Channel Jamming – Cluster: `delay_cluster=100, data_rate_cluster=1000000`, file `ns-3.cc`. Schedule `schedule_1`, 12:00–18:00.
  2. Channel Jamming – Peer-to-Peer: `data_rate_peer_to_peer=1000000, delay_peer_to_peer=100`, file `ns-3.cc`.
  3. DNS attacks – Cluster: `data_rate_cluster=5000000, delay_cluster=50`, file `ns-3.cc`.
  4. DNS attacks – Peer-to-Peer: `data_rate_peer_to_peer=1000000, delay_peer_to_peer=10`, file `ns-3.cc`.
  5. Injection Attacks – Control Systems: `max_capacity_reference_bid_quantity=100`, file `GridLab-D.glm`.
  6. Injection Attacks – End-point Systems: `comfort_level=0.1`, file `GridLab-D.glm`.
  7. Malicious Code – End-point Systems: `proxy_clear_price=7.8, proxy_price_cap=5.9`, file `GridLab-D.glm`.
  8. Replay of Messages – Cluster: `data_rate_cluster=2000000, delay_cluster=50`, file `ns-3.cc`.
  9. Replay of Messages – Peer-to-Peer: `data_rate_peer_to_peer=3000000, delay_peer_to_peer=70`, file `ns-3.cc`.

  Entries 2–9 have the literal placeholder schedule `"start_time": "start_time", "end_time": "end_time"`. — [Repo attack_library.json](https://github.com/crond-jaist/GridAttackSim/blob/master/attack_library.json)
- **Dissertation Table 4.2 values (Normal → New).** These differ from the JSON:
  - Jamming: cluster 10 Mbps → 1 Mbps and 3 ms → 100 ms; P2P 4 Mbps → 0.5 Mbps and 3 ms → 100 ms; and the combination of both.
  - DNS flood: delay_cluster or delay_peer_to_peer 3 ms → 400 ms.
  - Injection, max capacity bid: 150 kW → 250 kW (high) or 150 kW → 50 kW (low).
  - Injection, comfort_level: 1 → 0.1.
  - Malicious code: proxy_clear_price 0.042676 → 3.8; proxy_price_cap 3.8 → 7.6. — [Dissertation](https://dspace02.jaist.ac.jp/dspace/bitstream/10119/17476/12/paper.pdf)
- **Injection mechanism.** [Repo: attack_broker.py] For each selected attack:
  - It copies `ns-3.cc`→`run_ns-3.cc` and `GridLab-D.glm`→`run_GridLab-D.glm`.
  - For the ns-3 target, it replaces the marker comment `//Flag` with `//Flag\n\t<key> = <value>;//`, which overrides the global variables after their defaults are set in `main()`.
  - For GLM targets, it does a global `str.replace(key, key + " " + value + ";//")`, so `max_capacity_reference_bid_quantity 250;` becomes `max_capacity_reference_bid_quantity 100;// 250;`.
  - It then runs `./compile-ns3.sh run_ns-3.cc`, then `./run.sh`, and polls the xterm PID until it exits.
  - Schedule fields are only printed (`print('- Start Time: ' …)`); they are never applied. — [Repo attack_broker.py](https://github.com/crond-jaist/GridAttackSim/blob/master/attack_broker.py)
- **Attack selection.** [Repo: GridAttackSim.py] The GUI passes only the first character of the attack-type combo string (`combo_attack_type.get()[0:1]`) to `python attack_broker.py <model_dir>/ <id>`. — [Repo GridAttackSim.py](https://github.com/crond-jaist/GridAttackSim/blob/master/GridAttackSim.py)
- **Schedule files.** [Repo: " attack_schedule.glm"]
  - Each model directory contains a file literally named ` attack_schedule.glm`, with a leading space. It defines a GridLAB-D cron-style `schedule schedule_1 { 0-9 0 * * * 0.00; … }` of 10-minute fractional values. It is not `#include`d by any released GLM.
  - Only the simple feeder includes `max_capacity_reference_bid_quantity.glm` (a schedule `max_capacity_reference_bid_quantity_attack` with hour-band values of 1125 kW, with a commented-out 500 kW band at 08:00–14:00). The line binding it to the auction is commented out. — [Repo 13_Nodes_73_Houses](https://github.com/crond-jaist/GridAttackSim/tree/master/Database/13_Nodes_73_Houses); [Repo 1_Node_255_Houses](https://github.com/crond-jaist/GridAttackSim/tree/master/Database/1_Node_255_Houses)
- **Paper's case-study schedule.** [Paper §5.2] For the injection attack, "the attack schedule was set as specified by the peak hours, which are from 14:00 to 21:00". The paper does not say how that window was enforced. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Paper's jamming emulation.** [Paper §5.1] Delays were increased "until the total load, cleared market price, and cleared quantity had been significantly affected": data rates 4 Mbps → 0.5 Mbps (P2P) and 10 Gbps → 1 Gbps (LAN), delays 3 ms → 100 ms. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)

### Inferences
- [Inferred] Mapping of the user's attack list to the implementation:
  - **FDI / data tampering**: modelled as changing the market's `max_capacity_reference_bid_quantity`, the controllers' `proxy_clear_price`/`proxy_price_cap` or water-heater `comfort_level` in the GLM. This is a configuration change at t=0, not a message modification in transit.
  - **DoS / jamming / DNS flood**: modelled as lower link data rate and higher propagation delay on CSMA and/or P2P links.
  - **Replay**: modelled only as higher delay and lower rate. No messages are recorded and re-injected.
  - **MitM**: listed in the ENISA category text but not implemented.
- [Inferred] Because `proxy_clear_price` is a precommit FNCS subscription target, the "malicious code" overwrite of its initial value is likely overwritten by the first relayed price message. Only `proxy_price_cap` would persist, so this attack may have little effect. This needs testing.
- [Inferred, code reading, not executed] In the released simple-feeder model:
  - `ns-3.cc` has no `//Flag` marker, so the network attacks 1–4 and 8–9 would silently do nothing on that model. Yet the paper's jamming case used that feeder, so the authors must have edited it manually.
  - The global string replace for `max_capacity_reference_bid_quantity` would also corrupt the `#include "max_capacity_reference_bid_quantity.glm"` line.
- [Inferred] The 14:00–21:00 injection window in §5.2 was most likely implemented by binding a GLM `schedule` to the auction property (the pattern visible, commented out, in the simple feeder), or by manual GLM edits. JSON start/end times are not used by the code.
- [Inferred] Attack magnitude is set only via `affected_value`. Target selection is coarse: all CSMA links, all P2P links, the one auction, or all controllers. There is no per-node targeting.

### Gaps
- No documented implementation of time-windowed network attacks. ns-3 link attributes are set once at build time; no `Simulator::Schedule` changes are present.
- No ns-3 attacker node, traffic generator (e.g., UDP flood), packet corruption or replay application exists in the release.

---

## 6. Model management, orchestration, GUI, results collection, visualization, case-study numbers

### Takeaway
- **Model manager:** a Python 3 Tkinter desktop application (`GridAttackSim.py`) that shells out to a Python 2-style `attack_broker.py`.
- **Simulator launch:** `run.sh` opens three xterms.
- **Results:** GridLAB-D tape `recorder`s write CSV files (total load, clearing price and quantity). These are renamed per run and plotted with matplotlib embedded in Tk.
- **Comparison:** normal vs. attack is done by overlaying selected CSVs.
- **Outcomes:** the reported 24 h effects are a few percent in energy or bill for jamming, and up to −81.9% / +53.1% bill changes for capacity-bid injection.

### Cited Findings
- **Model manager role.** [Paper §3.6] It manages scenario composition and execution: it wakes the preprocessing module, loads the grid and network models, calls the attack library if an attack is selected, updates the model cores, runs ns-3, GridLAB-D and the broker, then loads and visualizes results. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **GUI framework.** [Paper §4] "a smart grid co-simulation application was created using the Python programming language. Tkinter … was utilized to build the … desktop application." — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Running and results.** [Paper §4.4]
  - "Three terminal windows are opened, one for the ns-3 process, one for GridLAB-D operation, and the last for the fncs_broker."
  - Outputs are CSV files from GridLAB-D tape-module `recorder` and `collector` objects: power load, clearing price, clearing quantity and node voltages.
  - "Currently, line graphs and bar graphs are supported." — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **GUI code.** [Repo: GridAttackSim.py]
  - Model list: the five models. Application: DR, DP, or both.
  - Attack categories: None, Nefarious Activity (attacks 1–7), Eavesdropping/Interception/Hijacking (attacks 8–9).
  - "Show Model" runs `glmMap.py` (a PNNL script) and opens it with the graphviz `Source.view()`.
  - After each run it renames `baseprice_clearedprice_clearedquantity.csv` → `price_<attack>_<timestamp>.csv` and `totalload.csv` → `totalload_<attack>_<timestamp>.csv`.
  - "Load Results" lists `t*`/`p*` CSVs, filtered by application.
  - "Show Charts" calls `plot_result.py`, which uses pandas and matplotlib `FigureCanvasTkAgg` with `skiprows=9` to read the GridLAB-D CSV headers. — [Repo GridAttackSim.py](https://github.com/crond-jaist/GridAttackSim/blob/master/GridAttackSim.py); [Repo plot_result.py](https://github.com/crond-jaist/GridAttackSim/blob/master/plot_result.py)
- **No database.** No MySQL or other DB is used; the results are flat CSV only [Repo, all files].
- **Test environment.** [Paper §5] Intel Core i7 3.1 GHz, 64-bit Linux, 16 GB DDR3. One-day run from 2009-07-21 00:00 to 2009-07-22 00:00 with NSRDB Seattle weather. The release targets Ubuntu 16.04 LTS only. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf); [Repo README](https://github.com/crond-jaist/GridAttackSim/blob/master/README.md)
- **Case 1: channel jamming, simple test feeder.** [Paper §5.1]
  - Setup: 255 houses and a 250-node ns-3 network in groups of 20; price cap $3.78; maximum capacity bid 1500 kW.
  - Peak runs from ~16:00 to midnight, and price hits the cap (~$3.8/kWh) for ~5 h.
  - Under attack, the price drops to ~$1 at ~22:00 and the load fluctuates above 1600 kW. Clearing-quantity curves are identical.
  - Packet delivery ratio falls by 20.14%.
  - Energy consumption is +3.2% and bill −2.9%, i.e. a utility loss over 24 h. Mitigation reference: [28]. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Case 2: injection attack, IEEE 13-node.** [Paper §5.2]
  - Setup: 73 houses and 73 ns-3 nodes in groups of 20; price cap $3.78; maximum capacity bid 150 kW. Attack window 14:00–21:00, shown 13:00–22:00.
  - Fake 200 kW: energy 107.6%, peak load 210 kW, bill 18.1% (utility loses 81.9% of revenue in the 9 h window). The price hits the cap only for ~2 h from 18:00.
  - Fake 50 kW: price pinned at $3.78 for the whole attack, energy 103.2%, peak load ~200 kW, bill 153.1%.
  - Detection references: [29, 30]. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **User study.** [Dissertation §6.2] 10 PhD students (5 from JAIST, 5 external) all reproduced the case studies. GridAttackSim SUS scores: mean 74.3, SD 9.5, min 55, max 87.5. — [Dissertation](https://dspace02.jaist.ac.jp/dspace/bitstream/10119/17476/12/paper.pdf)

### Inferences
- [Inferred] The "Application" selector does not change the simulation; it only filters which CSVs are listed (totalload for DR, price for DP). DR and DP are always active through the market and controllers.
- [Inferred] The paper says the GUI loads voltages, but voltage recorders are not wired into the GUI pipeline in the release, which handles only `price_*` and `totalload_*` files. Bill and energy percentages (Fig. 5d/6d) are not computed by the released code. They were presumably calculated offline from the price × load CSVs.
- [Inferred] `attack_broker.py` parses `pgrep` output with `str.split('\n')` on bytes, and the GUI invokes it with `python` rather than `python3`. It therefore relies on Python 2.7 being `python`, as on Ubuntu 16.04, and would raise TypeError under Python 3.
- [Inferred] The "normal" baseline run uses attack type "None", which passes "N" as the ID. No library entry matches, so the files are copied unchanged and run.

### Gaps
- The exact formula for "bill amount" and "economic impact" (Σ clearing price × load? per-house bills?) is not given.
- No statistical repetition, random-seed control or confidence intervals are reported.

---

## 7. Extensibility and configuration flow (user → simulators)

### Takeaway
To extend GridAttackSim you add a model directory with a GLM and generated FNCS files, or add a JSON entry whose `affected_value` keys match a variable in `ns-3.cc` (below the `//Flag` marker) or a property name in the GLM. The configuration flow is: GUI selections → `attack_broker.py` → string-patched copies of the model files → g++ build → three xterms (ns-3, GridLAB-D, broker) → CSV → plot.

### Cited Findings
- **Extensibility claims.** [Paper §1, §6] "our simulator not only features a set of built-in attack profiles but also allows researchers … to develop new ones". The framework is "extendable … due to our extendable attack pattern library structure". — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Developer guide** [Repo: developer_guide.md]:
  - New topology: create a directory like the existing ones and run `python3 creat_zpl_file.py` and `python3 creat_rout_and_subscribe.py`. These take total houses, market ID and controller prefix, and generate `fncs.zpl` and `fncs_msg.txt`.
  - New attack: add an object with `attack_type{type_id,type_name,description,affected_value}`, `attack_component{component_id,component_name,description,file}` and `attack_schedule{schedule_id,description,start_time,end_time}`. To tune an existing attack, "change the values of the affected values". — [Repo developer_guide.md](https://github.com/crond-jaist/GridAttackSim/blob/master/developer_guide.md)
- **Naming.** The JSON uses `attack_component`, while the paper's Table 2 calls the same sub-module "Attack Target" (`target_id`, `target_name`). — [Repo attack_library.json](https://github.com/crond-jaist/GridAttackSim/blob/master/attack_library.json); [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)

### Inferences
- [Inferred] Adding an attack is not purely declarative:
  - The GUI's attack list is hard-coded in `GridAttackSim.py`, and IDs are parsed from the first character only, so IDs ≥ 10 would break.
  - Any new ns-3 variable must also be declared and used in each model's `ns-3.cc`.
  - Behavioural attacks (packet drop, modification, replay, spoofing) would need new ns-3 application code. The JSON overwrite model cannot express them.
- [Inferred] The preprocessing generators hard-code house counts and names (e.g., `while (index < 74)`, `Market_1`), so the "automatic" generation in Figure 1 means per-model scripts edited by hand.

### Gaps
- No plugin API, schema validation or tests exist in the release.

---

## 8. Availability of code, data, Docker, supplementary material

### Takeaway
The paper itself has no supplementary material or data-availability statement. Official source code was published in March 2021 at crond-jaist/GridAttackSim (BSD-3-Clause, v1.0, no activity since February 2022), together with the sister repo GridAttackAnalyzer. No Docker image was found; the install path is a manual Ubuntu 16.04 build of FNCS, FNCS-ns-3.26 and GridLAB-D following the PNNL FNCS tutorial.

### Cited Findings
- **Paper back matter.** It ends with Author Contributions, Funding ("no external funding") and Conflicts of Interest; there are no Supplementary Materials or Data Availability sections [Paper, back matter]. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Code release.** "The source code of GridAttackSim and GridAttackAnalyzer have been uploaded on Github", citing `https://github.com/crond-jaist/GridAttackSim` (2021) [Dissertation §8.1]. — [Dissertation](https://dspace02.jaist.ac.jp/dspace/bitstream/10119/17476/12/paper.pdf)
- **Repository facts.**
  - Tag `1.0`. Commits run from 2021-03-05 ("Added grid topology database", "Added program files", …) to 2022-02-15 (license text).
  - `CHANGES`: "GridAttackSim v1.0 — first public release … five smart grid topologies, two smart grid applications, and an attack library with four types of attacks".
  - `CONTRIBUTORS`: initial implementation by Tan Duy Le; maintainer Razvan Beuran.
  - About 45 MB, mostly GLM, player and weather files and the prebuilt binaries `ns-3` and `run_ns-3`. — [Repo](https://github.com/crond-jaist/GridAttackSim)
- **Sister repo.** GridAttackAnalyzer: tag `1.0`, last commit 2022-02-15. — [GridAttackAnalyzer repo](https://github.com/crond-jaist/GridAttackAnalyzer)
- **Platform.** "Developed and tested exclusively using the Ubuntu 16.04 LTS operating system… nor has this software been tested on Windows." The guide's dependencies are `automake libtool autoconf libczmq-dev libxerces-c-dev`, plus a patch to GridLAB-D `climate/climate.cpp` (`#include <math.h>` → `<cmath>`). — [Repo installation_guide.md](https://github.com/crond-jaist/GridAttackSim/blob/master/installation_guide.md)

### Inferences
- [Inferred] The repo includes prebuilt Linux binaries (`ns-3`, `run_ns-3`, `firstN`) compiled against a specific `$FNCS_INSTALL`. They will not run elsewhere without rebuilding.
- [Inferred] I did not query GitHub stars or issues: the GitHub API was blocked in this environment, and only a git clone worked.

### Gaps
- No Docker or VM image was found in the repo or in search results. A Docker Hub search was not performed.
- The README links to a GitHub "releases" page; I could not query it via the API, but the tag `1.0` exists.

---

## 9. Background and 2026 status of the tool stack (GridLAB-D, ns-3, FNCS, HELICS, TESP)

### Takeaway
GridAttackSim was built directly on the 2014–2017-era PNNL **FNCS** stack (FNCS master, FNCS-patched ns-3.26, GridLAB-D develop with FNCS). It was **not** built on TESP; there is no TESP code or reference. Upstream development of FNCS stopped around 2017–2018, and HELICS is its successor. By November 2026, HELICS (v3.7.0), TESP (v1.3.8, HELICS-based), GridLAB-D (v6.0 tag) and ns-3 (3.47/3.48+) are all active, while FNCS and FNCS/ns-3.26 are dormant.

### Cited Findings
- **FNCS as described in the paper.** [Paper §2 and ref 15: Ciraci et al. 2014] FNCS is an HPC co-simulation platform whose broker manages GridLAB-D ↔ ns-3 communication "in configurable time steps". — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **FNCS repository status** (git tags and last commit, retrieved 2026-11-05). FNCS/fncs: latest tag v2.3.2, dated 2017-04-20; last commit on the default branch 2018-12-18. FNCS/ns-3.26: last commit 2017-08-15 ("Remove development model for GMLC TDC"). — [FNCS repo](https://github.com/FNCS/fncs); [FNCS ns-3.26](https://github.com/FNCS/ns-3.26)
- **HELICS.** Latest tag v3.7.0, dated 2026-09-09. The default branch had commits on 2026-11-01. — [HELICS repo](https://github.com/GMLC-TDC/HELICS)
- **TESP.** Latest tag v1.3.8, dated 2026-09-11.
  - The README says TESP "utilizes the HELICS co-simulation framework" to coordinate GridLAB-D, EnergyPlus, AMES/PSST, PYPOWER and ns-3.
  - The changelog notes v1.1.1 "Updated examples from Helics2.8 to Helics3.0" and v1.3.0 "Upgrade all models (GridLAB-D, EnergyPlus, NS3) to work with HELICS 3.4".
  - The overview docs still describe "TESP Rev 1 components federated through FNCS and/or HELICS". — [TESP repo](https://github.com/pnnl/tesp); [TESP docs](https://tesp.readthedocs.io/)
- **FNCS → HELICS transition.** Third-party projects describe FNCS as HELICS's predecessor. A 2023 arXiv paper uses HELICS "instead of FNCS" between GridLAB-D and ns-3. I found no explicit formal FNCS deprecation notice. — [arXiv 2307.09633](https://arxiv.org/pdf/2307.09633); [TESP PyPI](https://pypi.org/project/tesp-support/1.3.0/)
- **GridLAB-D.** Tags include v5.3.0 (2025-01-06) and v6.0 (2026-10-14). The default branch's last commit was 2025-05-28 (the release/v5.3 merge). — [GridLAB-D repo](https://github.com/gridlab-d/gridlab-d)
- **ns-3.**
  - ns-3.47 was released 2026-02-16 [nsnam news](https://www.nsnam.org/news/2026/02/16/ns-3-47-released.html).
  - ns-3.48 was released around 2026-06-02 according to the nsnam wiki.
  - The nsnam homepage reportedly lists ns-3.49, but the roadmap says September 2026; I could not confirm an exact 3.49 date. — [nsnam wiki](https://www.nsnam.org/wiki); [nsnam.org](https://www.nsnam.org)
- **Paper's Table 1.** It lists FNCS (2018) and HELICS (2019) with "N/A" built-in attack support. The authors were aware of HELICS but chose FNCS [Paper §2, Table 1]. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)

### Inferences
- [Inferred] GridAttackSim did not build on TESP. Its install path is the FNCS-Tutorial `demo-gld-ns3`, and one model's README is that tutorial's README. Its controller and auction setup is the classic GridLAB-D market module of PNNL's FNCS demo, not TESP's Python agents.
- [Inferred] Rebuilding today on modern ns-3 (3.4x, CMake-based, C++20) would require porting `FncsApplication` and `FncsSimulatorImpl`, or switching to the HELICS ns-3 module (`helics-ns3`). GridLAB-D 5.x/6.x supports HELICS natively, and FNCS support in current GridLAB-D builds should be verified before relying on it.

### Gaps
- I did not verify whether GridLAB-D v6.0 still compiles the FNCS `connection` module. The exact maintenance status of FNCS-tutorial repos was not checked beyond the tags and commit dates above.

---

## 10. Limitations: author-stated and identified

### Takeaway
The authors acknowledge a basic network model, a few small feeders and a limited attack set. The code review finds deeper issues:
- attacks are static parameter overrides with no timing in the released code
- there is no packet-level adversary
- "wireless jamming" is emulated on wired links
- the paper, thesis and code disagree on parameters
- there is no validation against real data or hardware

### Cited Findings
- **Author-stated: network model.** "The main problem faced in this research is the design of the network model… our basic network model should not be treated as the only solution." Future work: more network models, test feeders, applications and attack types [Paper §7]. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Author-stated: scale.** Three feeder types, at most 1000 houses; each iteration jointly solves the power and communication models [Paper §7]. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Author-stated: integration difficulties.** Time scales, synchronization, transmission delays and model reuse, which the authors say FNCS handles [Paper §6]. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)
- **Author-stated: future feeders.** EPRI representative feeders, PG&E prototypical feeders, LV benchmark feeders, an agent-based test feeder and a DG-protection test feeder [Dissertation §8.2]. — [Dissertation](https://dspace02.jaist.ac.jp/dspace/bitstream/10119/17476/12/paper.pdf)
- **Precursor limitations.** The precursor supported one model and two attack types, with no GUI, framework design or attack schedule [Paper §2]. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf)

### Inferences
- [Inferred] **Attack realism.**
  - Attacks are whole-run parameter changes. FDI is a changed configuration constant, not falsified telemetry on the wire.
  - Replay and DNS attacks are indistinguishable from jamming: all are delay or rate changes.
  - There is no attacker node, no traffic or cryptography model, and no detection or IDS loop.
- [Inferred] **Schedule gap.** The paper headlines "attack schedule" capability, but the released `attack_broker.py` ignores start/end times and the schedule GLMs are not included. Reproducing the 14:00–21:00 window needs manual GLM work.
- [Inferred] **Parameter inconsistencies** between paper, thesis and code:
  - LAN 10 Gbps vs 10 Mbps
  - P2P 4 Mbps vs 40 Mbps
  - 13-node maximum capacity bid 150 vs 250 kW
  - injection values 50/200 vs 50/250 vs 100 kW
  - malicious-code values 3.8/7.6 vs 7.8/5.9
  - 255 vs 250 houses
  - CSMA/CD vs CSMA/CA
  - Seattle vs Columbus weather for the simple feeder
- [Inferred] **Validation.** The results are "supported by relevant works" qualitatively only. There is no comparison with field data, no hardware-in-the-loop and no repeated runs. The physical effects reported are market or economic (price, load, bill). Voltage and protection impacts are not analysed.
- [Inferred] **Fidelity.** Distribution feeders are small (≤13 buses). The single market has a uniform topology, and transmission-level effects are absent. The network has no wireless PHY, despite the jamming narrative.
- [Inferred] **Engineering fragility.**
  - It is tied to Ubuntu 16.04, Python 2/3 mixing, xterm, and the dormant FNCS and ns-3.26.
  - Global string replacement in GLMs can corrupt unrelated lines (e.g., `#include` names).
  - The simple-feeder `ns-3.cc` lacks the `//Flag` hook.

### Gaps
- No independent replication of GridAttackSim results was found. The SUS study reports that 10 PhD students reproduced the case studies, but this was run by the authors.

---

## 11. Precursor and related works by Tan Duy Le et al.

### Takeaway
GridAttackSim extends Le, Anwar, Beuran and Loke, "Smart Grid Co-Simulation Tools: Review and Cybersecurity Case Study" (icSmartGrid 2019). That paper surveyed co-simulation tools and ran FDI and jamming case studies on the IEEE 13-node feeder with GridLAB-D+FNCS+ns-3. GridAttackSim is part of Le's 2021 JAIST PhD, alongside GridAttackAnalyzer, and was followed by a 2022 RIVF summary paper.

### Cited Findings
- **Precursor paper.** Ref [7]: Le, T.D.; Adnan, A.; Beuran, R.; Seng, W.L., "Smart Grid Co-Simulation Tools: Review and Cybersecurity Case Study", IEEE icSmartGrid 2019, Newcastle, 9–11 Dec 2019. The paper cites pp. 273–280; the dissertation and repo cite pp. 39–45.
  - It concluded that GridLAB-D+FNCS+ns-3 is promising.
  - It ran two simple case studies on the IEEE 13-node feeder only, covering one model and two attack types, without a GUI or scheduler [Paper §2]. — [Paper PDF](https://www.jaist.ac.jp/~razvan/publications/gridattacksim_framework.pdf); [IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/8990712)
- **Precursor abstract.** It "applied these tools with the IEEE 13 Node Test Feeder Model to examine the impact of security threats on smart grid demand/response and dynamic pricing applications", with fake data injection and jamming attacks, and reports a 20% co-simulation speed improvement. — [Deakin DRO record](https://dro.deakin.edu.au/articles/conference_contribution/Smart_Grid_Co-Simulation_Tools_Review_and_Cybersecurity_Case_Study/20712694)
- **Related outputs** [Dissertation, Publications]:
  - "CVSS Based Attack Analysis using a Graphical Security Model: Review and Smart Grid Case Study" (SGIoT 2020)
  - "GridAttackAnalyzer: Cyber Attack Analysis Framework for Smart Grids" (under review at Elsevier SEGAN as of 2021)
  - Dissertation: "Smart Grid Cybersecurity Experimentation: Architecture and Methodology" (JAIST, March 2021) — [Dissertation](https://dspace02.jaist.ac.jp/dspace/bitstream/10119/17476/12/paper.pdf)
- **Follow-up paper.** Le, Nguyen, Huynh and Beuran, "Smart Grid Cyber-Attack Analysis and Countermeasures", RIVF 2022. It summarizes GridAttackSim and GridAttackAnalyzer as implementations of a general smart-grid cybersecurity architecture. — [RIVF 2022 PDF](https://www.jaist.ac.jp/~razvan/publications/smart_grid_attack_analysis_countermeasures.pdf)

### Inferences
- [Inferred] The JSON attack library and the GUI were the main additions over the 2019 paper. So were the extra feeders (simple, 4-node, 13-node with 15/73 houses, 4-node with 492 houses) and the ENISA-based taxonomy. The core co-simulation (FNCS demo plus 13-node GLM plus capacity-bid FDI plus delay-based jamming) is largely carried over.

### Gaps
- I could not obtain the full text of the icSmartGrid 2019 paper. The JAIST link returned an HTML error page instead of a PDF, and the Deakin copy is embargoed. Its exact numeric results are therefore not included here.
- No smart-grid attack-simulation conference papers by Le predating icSmartGrid 2019 were found. The dissertation's publication list shows none.
