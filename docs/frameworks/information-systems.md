# Information Systems — curriculum framework (draft 1)

Generated from `drills/frameworks/information-systems.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**53 learning objectives** in 8 units (0 core): 0 drilled, 0 partly, 53 with no drills. Core: 0 / 0 drilled.

## Big ideas

- **VAL · IT creates value only through the business.** Technology pays off when it changes a process, decision or product; an investment is judged by the business outcome it enables, in money and risk.
- **ALIGN · Strategy, architecture and governance must line up.** Decision rights, the enterprise architecture and the portfolio translate business strategy into systems; misalignment shows up as duplicate systems, shadow IT and stranded spend.
- **RISK · Risk is managed, never eliminated.** Security, continuity and compliance are trade-offs priced against impact and likelihood, with controls chosen to bring residual risk inside appetite.
- **DATA · Data is an organisational asset.** Data has owners, quality, lineage and a lifecycle; its value depends on governance and integration as much as on storage technology.
- **SOCIO · Information systems are sociotechnical.** People, process and technology change together; adoption, incentives and ethics decide whether a technically sound system succeeds.

## Practices

- **P1 · Frame the business problem.** State the goal, stakeholders, constraints and what decision the analysis supports.
- **P2 · Quantify.** Put numbers on value, cost, risk, schedule and service levels — NPV, TCO, ALE, EVM, availability.
- **P3 · Model.** Represent processes, data, architecture and requirements in a standard notation (BPMN, ER, capability map, use case).
- **P4 · Choose and justify.** Compare options against explicit criteria and recommend one, naming the trade-off accepted.
- **P5 · Govern and control.** Assign decision rights, controls, metrics and review cycles so the choice stays on track.
- **P6 · Weigh people and ethics.** Account for adoption, change, privacy, fairness, law and sustainability.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · IS strategy and governance | extension | — | 8 | 0 | 0 | 8 |
| 2 · Enterprise architecture | extension | — | 5 | 0 | 0 | 5 |
| 3 · Systems analysis, development and deployment | extension | — | 6 | 0 | 0 | 6 |
| 4 · Data, information and analytics management | extension | — | 10 | 0 | 0 | 10 |
| 5 · IT infrastructure and service operations | extension | — | 7 | 0 | 0 | 7 |
| 6 · Business continuity and information assurance | extension | — | 7 | 0 | 0 | 7 |
| 7 · Innovation, organisational change and entrepreneurship | extension | — | 6 | 0 | 0 | 6 |
| 8 · Ethics, impacts and sustainability | extension | — | 4 | 0 | 0 | 4 |

## Unit 1 · IS strategy and governance (extension)

Big ideas: VAL, ALIGN

### 1.1 Strategic value of IT

Book: msis2016 §ISSG

- ○ **IS-1.1.A** Classify a described system by its strategic role (cost leadership, differentiation, focus) and the Porter value-chain activity it changes.
  - EK: IT advantage lasts only if hard to copy — complementary processes and data, not the technology itself.
  - P1
- ○ **IS-1.1.B** Place each application of a portfolio in the McFarlan grid (support, factory, turnaround, strategic) from its current and future impact.
  - EK: Strategic = high current and future impact; factory = high current, low future; the quadrant sets how it should be governed and funded.
  - P3 · P4

### 1.2 IT investment appraisal

Book: msis2016 §ISSG, §ISMO

- ○ **IS-1.2.A** Compute NPV, ROI and payback period of an IT project from its cash flows and discount rate, and accept or reject it.
  - EK: NPV = Σ CF_t/(1 + r)^t − I₀; accept if NPV > 0; payback ignores the time value of money and later flows.
  - P2 · P4
- ○ **IS-1.2.B** Compute total cost of ownership over a horizon for build, buy (licence) and SaaS options, including hidden costs.
  - EK: TCO = acquisition + implementation + operation + support + exit; licences are often < 30% of TCO.
  - P2 · P4
- ○ **IS-1.2.C** Rank a set of proposed projects by a weighted scoring model under a budget constraint.
  - EK: Score = Σ weight × rating; pick in score-per-cost order until the budget binds, checking dependencies.
  - P2 · P4

### 1.3 Governance frameworks and decision rights

Book: msis2016 §ISSG

- ○ **IS-1.3.A** Assign decision rights for an IT decision domain (principles, architecture, infrastructure, applications, investment) to a governance archetype for a scenario.
  - EK: Weill & Ross archetypes: business monarchy, IT monarchy, federal, duopoly, feudal, anarchy; investment is usually business-led.
  - P5
- ○ **IS-1.3.B** Match a governance need to the framework that addresses it — COBIT, ITIL, ISO/IEC 27001, NIST CSF, TOGAF.
  - EK: COBIT governs and audits IT overall; ITIL runs services; 27001 certifies an ISMS; NIST CSF organises cyber risk; TOGAF develops architecture.
  - P5 · P4
- ○ **IS-1.3.C** Build a RACI matrix for a described process and find its defects (no A, several A's, no R).
  - EK: Exactly one Accountable per activity; at least one Responsible; Consulted is two-way, Informed one-way.
  - P5

## Unit 2 · Enterprise architecture (extension)

Big ideas: ALIGN, DATA

### 2.1 Architecture domains and method

Book: msis2016 §EARC

- ○ **IS-2.1.A** Assign an artefact or decision to its architecture domain (business, data, application, technology) and to the TOGAF ADM phase that produces it.
  - EK: ADM: Preliminary, A Vision, B Business, C Information Systems (data + application), D Technology, E Opportunities, F Migration, G Governance, H Change.
  - P3
- ○ **IS-2.1.B** Build a capability map for a described organisation and mark the capabilities where heat-mapped investment should go.
  - EK: Capabilities say what the business does, independent of org chart and systems; they are stable while processes change.
  - P3 · P4

### 2.2 Application portfolio and integration

Book: msis2016 §EARC, §SDAD

- ○ **IS-2.2.A** Classify applications as Tolerate, Invest, Migrate or Eliminate from their business value and technical fit.
  - EK: Gartner TIME: high value + good fit ⇒ invest; high value + poor fit ⇒ migrate; low + good ⇒ tolerate; low + poor ⇒ eliminate.
  - P4
- ○ **IS-2.2.B** Choose an integration style (file transfer, shared database, API/RPC, messaging, event streaming) for a described pair of systems and count point-to-point links avoided by a hub.
  - EK: n systems point-to-point need n(n − 1)/2 links; a bus or hub needs n; asynchronous messaging decouples availability.
  - P4 · P2
- ○ **IS-2.2.C** Identify which migration strategy a cloud move uses (rehost, replatform, refactor, repurchase, retire, retain) from its description.
  - EK: Rehost = lift-and-shift; refactor rewrites for cloud-native; repurchase moves to SaaS.
  - Needs: CS-18.2.A
  - P4

## Unit 3 · Systems analysis, development and deployment (extension)

Big ideas: VAL, SOCIO

### 3.1 Process and requirements modelling

Book: msis2016 §SDAD

- ○ **IS-3.1.A** Model a described business process in BPMN with pools, lanes, gateways and events, and spot the hand-off that causes delay.
  - EK: Exclusive gateway = one path; parallel = all paths; message flows cross pools, sequence flows stay inside one.
  - P3
- ○ **IS-3.1.B** Write a use case (actor, preconditions, main flow, extensions) or user stories with acceptance criteria from an interview transcript.
  - EK: Story = as a <role> I want <goal> so that <benefit>; INVEST: independent, negotiable, valuable, estimable, small, testable.
  - P3 · P1
- ○ **IS-3.1.C** Prioritise a requirement list with MoSCoW or Kano and justify which items fall out of a release.
  - EK: Must / Should / Could / Won't (this time); Kano: basic, performance and delighter features age into basics.
  - P4

### 3.2 Project scheduling and control

Book: msis2016 §SDAD, §ISMO

- ○ **IS-3.2.A** Find the critical path, project duration and each activity's slack from an activity-on-node network — auto-checked.
  - EK: Forward pass gives earliest start/finish, backward pass latest; slack = LS − ES; zero-slack activities form the critical path.
  - P2
- ○ **IS-3.2.B** Compute earned-value metrics (PV, EV, AC, CV, SV, CPI, SPI, EAC) from a status report and say whether the project is over budget or late.
  - EK: CPI = EV/AC, SPI = EV/PV; < 1 means over cost or behind; EAC = BAC/CPI if the trend continues.
  - P2 · P5
- ○ **IS-3.2.C** Choose a delivery approach (predictive, agile, hybrid) and a deployment strategy (big bang, phased, parallel, pilot, blue-green, canary) for a described rollout.
  - EK: Parallel running costs most and risks least; canary exposes a small share of users first; regulated or fixed-scope work leans predictive.
  - P4

## Unit 4 · Data, information and analytics management (extension)

Big ideas: DATA, VAL

### 4.1 Data requirements and management

Book: msis2016 §DATA-11, §DATA-12, §DATA-13, §DATA-16, §DATA-20

- ○ **IS-4.1.A** Capture a scenario's data requirements as a conceptual model and choose the data-management technology the domain needs.
  - EK: Conceptual (entities, relationships) → logical (tables, keys) → physical; the access pattern and consistency need pick the store.
  - Needs: CS-7.1.A, CS-7.6.A
  - P3 · P4
- ○ **IS-4.1.B** Compute data-quality scores (completeness, validity, uniqueness, timeliness) for a sample table and name the root cause of the worst one.
  - EK: Completeness = non-null / total; uniqueness = distinct keys / rows; quality problems are fixed at the source process, not downstream.
  - P2
- ○ **IS-4.1.C** Assign data owner, steward and custodian roles for a data domain and write the policy decision each makes.
  - EK: Owner is accountable (business); steward defines meaning and quality rules; custodian (IT) operates storage and access.
  - P5

### 4.2 Warehousing and integration

Book: msis2016 §DATA-18, §DATA-19, §DATA-22

- ○ **IS-4.2.A** Design a star schema for a described analytic question: declare the grain, the fact table measures and the dimensions.
  - EK: State the grain first; facts are additive numeric measures at that grain; dimensions carry descriptive attributes, denormalised.
  - Needs: CS-7.1.A
  - P3
- ○ **IS-4.2.B** Choose the slowly-changing-dimension type (1, 2, 3) for an attribute whose history does or doesn't matter, and show the resulting rows.
  - EK: Type 1 overwrites; type 2 adds a new row with effective dates and a surrogate key; type 3 keeps a previous-value column.
  - P4 · P3
- ○ **IS-4.2.C** Choose between ETL into a warehouse, ELT into a lakehouse and streaming ingestion for a described data volume, variety and latency need.
  - EK: ELT pushes transformation to scalable storage; streaming fits seconds-level latency; schema-on-read trades governance for flexibility.
  - P4
- ○ **IS-4.2.D** Write the SQL aggregation that answers a business question over a star schema — auto-checked by result set.
  - EK: Join the fact to the needed dimensions, filter on dimension attributes, GROUP BY the reporting level.
  - Needs: CS-7.2.A, IS-4.2.A
  - P2

### 4.3 Analytics for decisions

Book: msis2016 §DATA-23, §DATA-24

- ○ **IS-4.3.A** Match a business question to descriptive, diagnostic, predictive or prescriptive analytics and to a method (dashboard, cohort, regression, classification, optimisation).
  - EK: Descriptive = what happened; diagnostic = why; predictive = what will; prescriptive = what to do.
  - P4 · P1
- ○ **IS-4.3.B** Compute the expected profit of acting on a classifier's predictions from its confusion matrix and the cost of each error.
  - EK: Expected value = Σ count × payoff per cell; the best threshold depends on error costs, not accuracy.
  - Needs: CS-13.2.A
  - P2 · P4
- ○ **IS-4.3.C** Define a KPI for a described objective with formula, target, owner and data source, and flag a vanity metric.
  - EK: A KPI ties to a decision and has a target; vanity metrics (raw sign-ups, page views) move without changing outcomes.
  - P5

## Unit 5 · IT infrastructure and service operations (extension)

Big ideas: VAL, RISK

### 5.1 Infrastructure and sourcing

Book: msis2016 §INFR

- ○ **IS-5.1.A** Size the servers or cloud instances a described workload needs at peak with headroom, and the cost of each option.
  - EK: Capacity = peak demand / (per-unit capacity × target utilisation); size for peak, not average.
  - Needs: CS-18.2.B
  - P2
- ○ **IS-5.1.B** Choose IaaS, PaaS, SaaS or on-premises for a described system and state who manages each layer under the shared-responsibility model.
  - EK: The provider takes more layers as you move IaaS → PaaS → SaaS; data and identity stay the customer's responsibility in every model.
  - P4 · P5
- ○ **IS-5.1.C** Recommend in-house, outsourced, offshored or cloud sourcing for a function using transaction-cost reasoning.
  - EK: Outsource commodity, well-specified work; keep asset-specific, strategic, hard-to-monitor work inside.
  - P4

### 5.2 Service management

Book: msis2016 §ISMO

- ○ **IS-5.2.A** Classify a described event as an incident, problem, service request or change, and the change as standard, normal or emergency.
  - EK: Incident = restore service fast; problem = find the root cause; standard changes are pre-approved and low-risk.
  - P5
- ○ **IS-5.2.B** Compute SLA attainment, MTTR and allowed downtime from an incident log and decide whether a credit is owed.
  - EK: Availability = (agreed time − downtime) / agreed time; MTTR = total repair time / incidents.
  - Needs: CS-6.5.A
  - P2 · P5
- ○ **IS-5.2.C** Prioritise an incident from its impact and urgency using a priority matrix.
  - EK: Priority = f(impact, urgency): high/high = P1; priority sets the response and resolution targets.
  - P4
- ○ **IS-5.2.D** Choose a vendor by a weighted evaluation of a set of RFP responses and name the contract terms that protect exit.
  - EK: Weight criteria before scoring; protect exit with data-portability, termination-assistance and escrow clauses.
  - P4 · P2

## Unit 6 · Business continuity and information assurance (extension)

Big ideas: RISK

### 6.1 IS risk management

Book: msis2016 §BCIA-5, §BCIA-6, §BCIA-7

- ○ **IS-6.1.A** Score risks on a likelihood × impact matrix and choose a treatment (avoid, mitigate, transfer, accept) for each.
  - EK: Inherent risk before controls, residual after; accept only within the stated risk appetite.
  - P2 · P4
- ○ **IS-6.1.B** Compute ALE before and after a proposed control and its return on security investment.
  - EK: ROSI = (ALE_before − ALE_after − control cost) / control cost.
  - Needs: CS-11.4.B
  - P2
- ○ **IS-6.1.C** Classify a control as preventive, detective or corrective and administrative, technical or physical.
  - EK: Defense in depth layers control types so one failure is caught by another.
  - P5

### 6.2 Continuity and recovery

Book: msis2016 §BCIA-2, §BCIA-4, §BCIA-8

- ○ **IS-6.2.A** Derive RTO and RPO for a business process from a business-impact analysis, and pick the recovery site and backup frequency that meet them.
  - EK: RPO = tolerable data loss ⇒ backup or replication interval; RTO = tolerable downtime ⇒ hot, warm or cold site.
  - P1 · P4
- ○ **IS-6.2.B** Compute what a full, incremental or differential backup schedule must restore after a failure on a given day, and the worst-case data loss.
  - EK: Incremental restore = last full + every incremental since; differential = last full + latest differential; loss = time since last backup.
  - P3 · P2

### 6.3 Security programme and audit

Book: msis2016 §BCIA-1, §BCIA-3, §BCIA-9

- ○ **IS-6.3.A** Map a described control to its NIST CSF 2.0 function (Govern, Identify, Protect, Detect, Respond, Recover).
  - EK: Govern was added in 2.0 for strategy and supply-chain risk; the functions run concurrently, not as a sequence.
  - P5
- ○ **IS-6.3.B** Identify the segregation-of-duties conflict in a described set of user roles and propose the compensating control.
  - EK: No one person should both initiate and approve, or both hold assets and record them; where SoD can't be split, add review.
  - Needs: CS-11.1.A
  - P5 · P6

## Unit 7 · Innovation, organisational change and entrepreneurship (extension)

Big ideas: SOCIO, VAL

### 7.1 Adoption and change

Book: msis2016 §IOCE

- ○ **IS-7.1.A** Predict adoption of a described system from TAM/UTAUT factors and name the intervention that raises it.
  - EK: Perceived usefulness and ease of use drive intention; UTAUT adds social influence and facilitating conditions.
  - P6
- ○ **IS-7.1.B** Place a described organisation's change effort in a change model (Lewin, Kotter, ADKAR) and name the step it skipped.
  - EK: Kotter: urgency, coalition, vision, communicate, empower, short-term wins, consolidate, anchor; skipping urgency stalls most efforts.
  - P6
- ○ **IS-7.1.C** Locate a technology's adopters on the diffusion curve and decide how to cross the chasm to the early majority.
  - EK: Innovators 2.5%, early adopters 13.5%, early majority 34%; the early majority buys whole-product solutions and references.
  - P4 · P6

### 7.2 Digital business models

Book: msis2016 §IOCE

- ○ **IS-7.2.A** Fill a business model canvas for a described digital venture and identify its riskiest assumption.
  - EK: Nine blocks: segments, value proposition, channels, relationships, revenue, resources, activities, partners, costs; test the riskiest first.
  - P3 · P1
- ○ **IS-7.2.B** Compute customer lifetime value and CAC payback for a subscription product and decide whether growth is profitable.
  - EK: LTV ≈ ARPU × gross margin / churn; healthy SaaS often wants LTV/CAC ≥ 3 and payback < 12 months.
  - P2
- ○ **IS-7.2.C** Identify the network effects (direct, indirect/two-sided) in a platform and the side to subsidise.
  - EK: Subsidise the side whose participation most attracts the other and that is more price-sensitive.
  - P4

## Unit 8 · Ethics, impacts and sustainability (extension)

Big ideas: SOCIO, RISK, DATA

### 8.1 Privacy and regulation

Book: msis2016 §ETIS, §DATA-17

- ○ **IS-8.1.A** Determine whether GDPR, CCPA/CPRA, HIPAA or FERPA applies to a described data flow and the lawful basis or consent it needs.
  - EK: GDPR follows EU data subjects; CCPA/CPRA covers qualifying businesses handling California residents' data; HIPAA covers health data of covered entities; FERPA covers education records.
  - P6 · P5
- ○ **IS-8.1.B** Decide when a data-protection impact assessment is required and list the privacy-by-design measures for a described system.
  - EK: High-risk processing (large-scale sensitive data, profiling, monitoring) needs a DPIA; minimise, pseudonymise, limit retention, default to private.
  - Needs: CS-16.1.C
  - P6

### 8.2 Responsible and sustainable IS

Book: msis2016 §ETIS

- ○ **IS-8.2.A** Analyse a described IS decision with stakeholder, utilitarian and rights-based reasoning and recommend an action.
  - EK: Identify every affected stakeholder; consequences and duties can disagree — state which one governs and why.
  - P6
- ○ **IS-8.2.B** Compare the lifetime carbon and cost of keeping versus refreshing a hardware fleet, including embodied emissions.
  - EK: Embodied carbon of manufacture often exceeds years of use-phase emissions for end-user devices; extending life is usually greener.
  - P2 · P6
