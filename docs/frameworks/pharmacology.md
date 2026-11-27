# Pharmacology — curriculum framework (draft 1)

Generated from `drills/frameworks/pharmacology.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**33 learning objectives** in 8 units (33 core): 33 drilled, 0 partly, 0 with no drills. Core: 33 / 33 drilled.

## Big ideas

- **PD · What the drug does to the body.** A drug acts by binding a target; how much binds is set by affinity and concentration, and what the binding does is set by efficacy.
- **PK · What the body does to the drug.** Absorption, distribution, metabolism and excretion set the concentration at the target over time; clearance and volume of distribution are the two independent parameters and half-life follows from them.
- **CLASS · Learn the class, then the exception.** Drugs in a class share a mechanism, and most of their uses and adverse effects follow from it.

## Practices

- **P1 · Compute.** Carry a pharmacodynamic or pharmacokinetic relation to a number.
- **P2 · Identify.** Name the mechanism, class or effect from a description.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Pharmacodynamics | core | — | 5 | 5 | 0 | 0 |
| 2 · Pharmacokinetics | core | — | 7 | 7 | 0 | 0 |
| 3 · Safety and variation | core | — | 4 | 4 | 0 | 0 |
| 4 · Autonomic drugs | core | — | 3 | 3 | 0 | 0 |
| 5 · Cardiovascular and renal drugs | core | — | 4 | 4 | 0 | 0 |
| 6 · Central nervous system and pain | core | — | 4 | 4 | 0 | 0 |
| 7 · Chemotherapy | core | — | 3 | 3 | 0 | 0 |
| 8 · Endocrine and other systems | core | — | 3 | 3 | 0 | 0 |

## Unit 1 · Pharmacodynamics

Big ideas: PD

### 1.1 Drugs and targets



- ● **RX-1.1.A** (iuphar-core-concepts:C1, iuphar-core-concepts:C2, iuphar-core-concepts:C4) Name the classes of drug target and the kinds of drug-target interaction.
  - EK: Most drugs act on receptors, enzymes, ion channels or transporters. An agonist binds and activates; an antagonist binds without activating and blocks the agonist. Binding may be reversible or irreversible, at the agonist's own (orthosteric) site or at an allosteric site.
  - P2 · drills: px-target-class, px-interaction-types
- ● **RX-1.1.B** (iuphar-core-concepts:C5, iuphar-core-concepts:C7, iuphar-core-concepts:C8) Read a dose-response curve for potency and efficacy.
  - EK: Response = Emax × C ÷ (C + EC50) for the simplest case. Potency is how little drug is needed (a lower EC50 is more potent); efficacy is the maximum response the drug can produce. A partial agonist has a lower Emax than a full agonist whatever its potency.
  - Needs: RX-1.1.A
  - P1 · drills: px-fractional-response, px-potency-efficacy
- ● **RX-1.1.C** (iuphar-core-concepts:C6) Compute receptor occupancy from affinity.
  - EK: The dissociation constant Kd is the concentration at which half the receptors are occupied; a lower Kd is a higher affinity. Fractional occupancy = [L] ÷ ([L] + Kd).
  - Needs: RX-1.1.B
  - P1 · drills: px-occupancy, px-concentration-for-occupancy
- ● **RX-1.1.D** (iuphar-core-concepts:C2, iuphar-core-concepts:C8) Tell competitive from non-competitive antagonism and compute a dose ratio.
  - EK: A competitive antagonist shifts the agonist curve to the right without lowering the maximum, and more agonist overcomes it; the dose ratio is 1 + [B] ÷ KB. A non-competitive or irreversible antagonist lowers the maximum response.
  - Needs: RX-1.1.C
  - P1 · drills: px-dose-ratio, px-antagonist-curve
- ● **RX-1.1.E** (iuphar-core-concepts:C3, iuphar-core-concepts:C9) Quantify selectivity and explain why it is lost at high dose.
  - EK: Selectivity is preferential affinity for one target over another, measured as the ratio of the two Kd or IC50 values. It is relative: at a high enough concentration the second target is occupied too, which is where many adverse effects come from.
  - Needs: RX-1.1.D
  - P1 · drills: px-selectivity-ratio, px-selectivity-concepts

## Unit 2 · Pharmacokinetics

Big ideas: PK

### 2.1 The fate of a drug



- ● **RX-2.1.A** (iuphar-core-concepts:C10) Predict ionisation and absorption from pKa and pH.
  - EK: The un-ionised form crosses membranes. For a weak acid the un-ionised fraction is 1 ÷ (1 + 10^(pH − pKa)); for a weak base it is 1 ÷ (1 + 10^(pKa − pH)). A drug is trapped on the side of a membrane where it is more ionised: weak acids in alkaline fluid, weak bases in acidic fluid.
  - Needs: RX-1.1.E, CH-8.9.C
  - P1 · drills: px-unionised-acid, px-ion-trapping
- ● **RX-2.1.B** (iuphar-core-concepts:C11) Compute bioavailability and explain first-pass metabolism.
  - EK: Bioavailability F is the fraction of a dose reaching the systemic circulation unchanged: F = (AUC oral ÷ AUC IV) × (dose IV ÷ dose oral). An intravenous dose has F = 1. Oral drugs pass through the gut wall and liver first, which can remove much of the dose.
  - Needs: RX-2.1.A
  - P1 · drills: px-bioavailability, px-first-pass
- ● **RX-2.1.C** (iuphar-core-concepts:C12, iuphar-core-concepts:C13) Compute and interpret the volume of distribution.
  - EK: Vd = amount of drug in the body ÷ plasma concentration. It is an apparent volume: a drug held in plasma by protein binding has a Vd near plasma volume, while a lipophilic drug stored in tissue can have a Vd of hundreds of litres.
  - Needs: RX-2.1.B
  - P1 · drills: px-volume-of-distribution, px-vd-size
- ● **RX-2.1.D** (iuphar-core-concepts:C14) Describe drug metabolism and the effect of enzyme induction and inhibition.
  - EK: Phase I reactions (oxidation, reduction, hydrolysis; mostly cytochrome P450) add or expose a functional group; phase II reactions conjugate (glucuronide, sulfate, acetyl, glutathione) and usually make the drug more water soluble. Inducers raise enzyme levels and lower other drugs' concentrations; inhibitors do the opposite. A prodrug is activated by metabolism.
  - Needs: RX-2.1.C
  - P2 · drills: px-phase, px-induce-inhibit
- ● **RX-2.1.E** (iuphar-core-concepts:C15, iuphar-core-concepts:C16) Tell first-order from zero-order elimination and compute what remains.
  - EK: In first-order elimination a constant fraction is removed per unit time, so the half-life is constant and the concentration falls exponentially. In zero-order elimination a constant amount is removed per unit time because the enzymes are saturated (ethanol, high-dose phenytoin and aspirin).
  - Needs: RX-2.1.D
  - P1 · drills: px-first-order-remaining, px-order
- ● **RX-2.1.F** (iuphar-core-concepts:C17, iuphar-core-concepts:C18) Relate half-life, clearance and volume of distribution.
  - EK: Clearance is the volume of plasma cleared of drug per unit time: CL = dose ÷ AUC for an intravenous dose. Half-life depends on both independent parameters: t½ = 0.693 × Vd ÷ CL.
  - Needs: RX-2.1.E
  - P1 · drills: px-half-life, px-clearance-from-auc
- ● **RX-2.1.G** (iuphar-core-concepts:C19) Design a loading and a maintenance dose for a target steady-state concentration.
  - EK: At steady state the rate in equals the rate out: maintenance dosing rate = CL × Css ÷ F. A loading dose fills the volume at once: loading dose = Vd × Css ÷ F. Without a loading dose, steady state is reached in about four to five half-lives.
  - Needs: RX-2.1.F
  - P1 · drills: px-maintenance-rate, px-loading-dose

## Unit 3 · Safety and variation

Big ideas: PD, PK

### 3.1 When the response is not the one intended



- ● **RX-3.1.A** (iuphar-core-concepts:C22) Compute a therapeutic index and say what a narrow one requires.
  - EK: Therapeutic index = TD50 ÷ ED50 (LD50 ÷ ED50 in animal studies). A drug with a low index (warfarin, digoxin, lithium, phenytoin, aminoglycosides) needs careful dosing and often monitoring of plasma levels or effect.
  - Needs: RX-2.1.G
  - P1 · drills: px-therapeutic-index, px-narrow-index
- ● **RX-3.1.B** (iuphar-core-concepts:C20, iuphar-core-concepts:C21) Classify adverse drug reactions and explain tolerance.
  - EK: Type A (augmented) reactions are dose-related extensions of the drug's pharmacology and are predictable; type B (bizarre) reactions are unrelated to dose, often immune or genetic, and unpredictable. Tolerance is a reduced response on repeated dosing, from pharmacodynamic change (receptor down-regulation) or pharmacokinetic change (enzyme induction).
  - Needs: RX-3.1.A
  - P2 · drills: px-adr-type, px-tolerance
- ● **RX-3.1.C** (iuphar-core-concepts:C23) Classify drug interactions.
  - EK: Pharmacokinetic interactions change another drug's concentration (absorption, binding, metabolism, excretion). Pharmacodynamic interactions change its effect at the same concentration: additive (the sum), synergistic (more than the sum) or antagonistic (less).
  - Needs: RX-3.1.B
  - P2 · drills: px-combined-effect, px-interaction-kind
- ● **RX-3.1.D** (iuphar-core-concepts:C24) Adjust for individual variation in drug handling.
  - EK: Age, body size, organ function, genetics and other drugs change the response to a standard dose. Renal function is estimated by the Cockcroft-Gault equation: creatinine clearance (mL/min) = (140 − age) × weight (kg) ÷ (72 × serum creatinine in mg/dL), multiplied by 0.85 for women.
  - Needs: RX-3.1.C
  - P1 · drills: px-cockcroft-gault, px-variation

## Unit 4 · Autonomic drugs

Big ideas: CLASS

### 4.1 Cholinergic and adrenergic drugs



- ● **RX-4.1.A** () Predict the effects of muscarinic agonists and antagonists.
  - EK: Muscarinic activation slows the heart, constricts the pupil and bronchi, increases secretions and gut and bladder motility. Antimuscarinics (atropine and relatives) do the opposite: fast heart, dilated pupils, dry mouth, constipation, urinary retention. Acetylcholinesterase inhibitors raise acetylcholine at both muscarinic and nicotinic synapses.
  - Needs: RX-1.1.E, HP-5.3.A
  - P2 · drills: px-muscarinic-effect, px-cholinergic-drugs
- ● **RX-4.1.B** () Match adrenoceptor subtypes to their effects and agonists.
  - EK: Alpha-1: vasoconstriction, pupil dilation. Alpha-2: reduces central sympathetic outflow. Beta-1: raises heart rate and contractility. Beta-2: bronchodilation and vasodilation in skeletal muscle. Epinephrine acts on all four; phenylephrine is alpha-1 selective, salbutamol beta-2 selective.
  - Needs: RX-4.1.A
  - P2 · drills: px-adrenoceptor, px-adrenergic-agonists
- ● **RX-4.1.C** () Predict the effects and hazards of adrenoceptor antagonists.
  - EK: Beta blockers lower heart rate, contractility and renin; non-selective ones can cause bronchospasm and mask the warning signs of hypoglycaemia. Alpha-1 blockers relax vessels and the bladder neck and can cause postural hypotension.
  - Needs: RX-4.1.B
  - P2 · drills: px-beta-blockers, px-blocker-effect

## Unit 5 · Cardiovascular and renal drugs

Big ideas: CLASS

### 5.1 Heart, vessels, kidney and blood



- ● **RX-5.1.A** () Give the mechanism and signature adverse effect of each antihypertensive class.
  - EK: ACE inhibitors block angiotensin II formation (cough, high potassium, angioedema); angiotensin receptor blockers block its receptor without the cough; dihydropyridine calcium channel blockers dilate arterioles (ankle swelling, gingival overgrowth); thiazides reduce sodium reabsorption; beta blockers reduce cardiac output and renin.
  - Needs: RX-4.1.C, HP-8.3.C, HP-12.1.C
  - P2 · drills: px-antihypertensive-mechanism, px-antihypertensive-adverse
- ● **RX-5.1.B** () Place each diuretic class on the nephron and predict its electrolyte effects.
  - EK: Loop diuretics block the Na-K-2Cl carrier in the thick ascending limb (most powerful; lose potassium, calcium). Thiazides block Na-Cl in the distal tubule (lose potassium, retain calcium). Potassium-sparing drugs act in the collecting duct (spironolactone blocks aldosterone; amiloride blocks the sodium channel). Carbonic anhydrase inhibitors act in the proximal tubule; osmotic diuretics throughout.
  - Needs: RX-5.1.A
  - P2 · drills: px-diuretic-site, px-diuretic-electrolytes
- ● **RX-5.1.C** () Match antithrombotic and lipid-lowering drugs to their mechanisms.
  - EK: Warfarin blocks vitamin K recycling (factors II, VII, IX, X; monitored by INR; reversed by vitamin K). Heparin potentiates antithrombin (reversed by protamine). Direct oral anticoagulants inhibit factor Xa or thrombin. Aspirin irreversibly inhibits platelet cyclooxygenase; clopidogrel blocks the platelet P2Y12 receptor. Statins inhibit HMG-CoA reductase.
  - Needs: RX-5.1.B
  - P2 · drills: px-antithrombotic-mechanism, px-antithrombotic-monitoring
- ● **RX-5.1.D** () Classify cardiac drugs for arrhythmia, angina and heart failure.
  - EK: Vaughan Williams classes: I sodium channel blockers, II beta blockers, III potassium channel blockers (amiodarone), IV calcium channel blockers (verapamil, diltiazem). Nitrates relieve angina by venodilation through nitric oxide. Digoxin inhibits Na+/K+-ATPase.
  - Needs: RX-5.1.C
  - P2 · drills: px-vaughan-williams, px-cardiac-drugs

## Unit 6 · Central nervous system and pain

Big ideas: CLASS

### 6.1 Anaesthesia, mood and pain



- ● **RX-6.1.A** () Explain how local anaesthetics act and compute the amount in a cartridge.
  - EK: Local anaesthetics block voltage-gated sodium channels from inside the axon, in their charged form, after crossing the membrane uncharged; small pain fibres are blocked first. Amides (lidocaine, articaine, bupivacaine) are metabolised in the liver, esters by plasma esterases. A 1% solution contains 10 mg/mL.
  - Needs: RX-4.1.C
  - P1 · drills: px-cartridge-mg, px-local-anaesthetic
- ● **RX-6.1.B** () Match central nervous system drug classes to their mechanisms.
  - EK: Benzodiazepines increase the frequency of GABA-A channel opening (reversed by flumazenil). SSRIs block serotonin reuptake. Typical antipsychotics block dopamine D2 receptors (movement disorders). Levodopa replaces dopamine in Parkinson disease. Many antiepileptics block sodium channels (phenytoin, carbamazepine).
  - Needs: RX-6.1.A
  - P2 · drills: px-cns-mechanism, px-cns-adverse
- ● **RX-6.1.C** () Compare opioids, NSAIDs and paracetamol.
  - EK: Opioids act on mu receptors (analgesia, respiratory depression, constipation, pinpoint pupils; reversed by naloxone). NSAIDs inhibit cyclooxygenase, reducing prostaglandins (gastric irritation, kidney injury, bleeding). Paracetamol is analgesic and antipyretic with little anti-inflammatory action; overdose injures the liver and is treated with acetylcysteine.
  - Needs: RX-6.1.B
  - P2 · drills: px-analgesic-class, px-analgesic-mechanism
- ● **RX-6.1.D** () Interpret MAC for inhaled anaesthetics and name the intravenous agents.
  - EK: MAC is the alveolar concentration at which half of patients do not move to a surgical stimulus: a lower MAC means a more potent agent. Solubility in blood sets the speed of onset: a low blood-gas partition coefficient gives fast induction and recovery. Propofol is the usual intravenous induction agent; ketamine blocks NMDA receptors.
  - Needs: RX-6.1.C
  - P2 · drills: px-mac, px-anaesthetic-facts

## Unit 7 · Chemotherapy

Big ideas: CLASS

### 7.1 Drugs against microbes and tumours



- ● **RX-7.1.A** () Give the signature adverse effects and dosing pattern of antibacterial classes.
  - EK: Penicillins: allergy. Aminoglycosides: kidney and inner-ear toxicity, concentration-dependent killing. Tetracyclines: tooth discolouration in children, chelated by calcium and antacids. Fluoroquinolones: tendon injury. Macrolides: enzyme inhibition, QT prolongation. Beta-lactams kill in a time-dependent way.
  - Needs: RX-3.1.D
  - P2 · drills: px-antibacterial-adverse, px-kill-pattern
- ● **RX-7.1.B** () Match antifungal and antiviral drugs to their targets.
  - EK: Azoles inhibit ergosterol synthesis; polyenes (amphotericin B, nystatin) bind ergosterol and make pores; echinocandins inhibit cell-wall glucan synthesis. Aciclovir is activated by viral thymidine kinase and inhibits viral DNA polymerase; oseltamivir inhibits influenza neuraminidase.
  - Needs: RX-7.1.A
  - P2 · drills: px-antifungal, px-antiviral
- ● **RX-7.1.C** () State the principles of cancer chemotherapy and its common toxicities.
  - EK: Cytotoxic drugs kill a constant fraction of cells per dose and hit dividing cells hardest, so bone marrow, gut lining, hair follicles and oral mucosa suffer. Antimetabolites act in S phase, vinca alkaloids and taxanes in M phase; alkylating agents are not phase-specific. Signature toxicities: doxorubicin heart, cisplatin kidney, bleomycin lung, vincristine nerves.
  - Needs: RX-7.1.B
  - P2 · drills: px-chemo-toxicity, px-chemo-principles

## Unit 8 · Endocrine and other systems

Big ideas: CLASS

### 8.1 Hormones, airways and gut



- ● **RX-8.1.A** () Match drugs for diabetes to their mechanisms and hazards.
  - EK: Metformin lowers hepatic glucose output (does not cause hypoglycaemia alone; rare lactic acidosis). Sulfonylureas close beta-cell potassium channels to release insulin (hypoglycaemia). SGLT2 inhibitors block renal glucose reabsorption (genital infection). GLP-1 agonists enhance glucose-dependent insulin release and slow gastric emptying. Insulin replaces the hormone.
  - Needs: RX-5.1.D, HP-7.1.C
  - P2 · drills: px-diabetes-mechanism, px-hypoglycaemia-risk
- ● **RX-8.1.B** () Describe corticosteroid and thyroid drug actions and hazards.
  - EK: Glucocorticoids suppress inflammation and immunity by changing gene transcription; long courses cause adrenal suppression (taper, never stop abruptly), osteoporosis, high glucose, infection risk and oral candidiasis with inhalers. Levothyroxine replaces T4; thionamides (carbimazole, propylthiouracil) block thyroid hormone synthesis.
  - Needs: RX-8.1.A
  - P2 · drills: px-corticosteroid, px-thyroid
- ● **RX-8.1.C** () Match respiratory and gastrointestinal drugs to their mechanisms.
  - EK: Beta-2 agonists and antimuscarinics dilate the bronchi; inhaled corticosteroids control airway inflammation; leukotriene antagonists block one inflammatory pathway. Proton pump inhibitors irreversibly block the H+/K+-ATPase; H2 antagonists block histamine on the parietal cell; antacids neutralise acid already secreted.
  - Needs: RX-8.1.B
  - P2 · drills: px-asthma-role, px-acid-drugs
