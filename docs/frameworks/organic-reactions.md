# Organic Reactions: Predict the Product — curriculum framework (draft 1)

Generated from `drills/frameworks/organic-reactions.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**72 learning objectives** in 11 units (52 core): 72 drilled, 0 partly, 0 with no drills. Core: 52 / 52 drilled.

## Big ideas

- **RULES · A few rules predict most products.** Electrons flow from the electron-rich site to the electron-poor one, toward the more stable intermediate, and equilibria run to the weaker acid. Most of a two-semester course is those three sentences applied.
- **REAGENT · A reagent has a job.** Read a reagent as what it does (adds H and OH anti-Markovnikov, removes two hydrogens, swaps OH for a leaving group), not as a name to match to a product.
- **BALANCE · Atoms are conserved.** Know what each reagent adds to or removes from the molecule. A product that does not balance is wrong before you look at where anything went.

## Practices

- **P1 · Predict.** Draw the major product on paper from the reactant and the reagents, in under a minute.
- **P2 · Read the reagent.** Say what a reagent does to a functional group, in a few seconds.
- **P3 · Apply a rule.** Use a counting or comparison rule to decide a direction, a site or a pathway.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · The rules that predict | core | — | 15 | 15 | 0 | 0 |
| 2 · Alkenes and alkynes | core | — | 5 | 5 | 0 | 0 |
| 3 · Alcohols and alkyl halides | core | — | 6 | 6 | 0 | 0 |
| 4 · Aldehydes and ketones | core | — | 6 | 6 | 0 | 0 |
| 5 · Carboxylic acids and their derivatives | core | — | 4 | 4 | 0 | 0 |
| 6 · Benzene and substituted benzenes | core | — | 6 | 6 | 0 | 0 |
| 7 · Making carbon–carbon bonds | core | — | 3 | 3 | 0 | 0 |
| 8 · Mechanisms with curved arrows | core | — | 7 | 7 | 0 | 0 |
| 9 · Physical organic chemistry and practice | extension | — | 13 | 13 | 0 | 0 |
| 10 · Organometallic reagents and catalysis | extension | — | 4 | 4 | 0 | 0 |
| 11 · Spectroscopy for structure | extension | — | 3 | 3 | 0 | 0 |

## Unit 1 · The rules that predict

Big ideas: RULES

### 1.1 Counting



- ● **OR-1.1.A** (fe-chemical:5.B) Find the degrees of unsaturation from a molecular formula.
  - EK: U = ½(2C + 2 + N − H − X); each is a ring or a π bond.
  - Needs: CH-2.6.B, ST-1.4.A
  - P3 · drills: or-degrees-of-unsaturation, co-h-from-dou
- ● **OR-1.1.B** (acs-accm-organic:III.A.2) Give the maximum number of stereoisomers from the number of stereocentres.
  - EK: 2ⁿ, fewer when there is a meso form.
  - Needs: OR-1.1.A
  - P3 · drills: or-stereoisomer-maximum, or-centres-from-max
- ● **OR-1.1.C** Assign the oxidation state of a carbon and say whether a step is an oxidation or a reduction.
  - EK: Bonds to H count −1, bonds to O, N or halogen +1, bonds to C zero.
  - Needs: OR-1.1.B
  - P3 · drills: or-oxidation-level, or-carbon-ox-group

### 1.2 Direction and site



- ● **OR-1.2.A** (acs-accm-organic:VIII.C.2, acs-accm-organic:VIII.D.1) Predict which side an acid–base equilibrium favours from two pKa values, and its equilibrium constant.
  - EK: Toward the weaker acid; K = 10^(pKa of product acid − pKa of starting acid).
  - Needs: OR-1.3.B, OR-1.1.C
  - P3 · drills: or-acid-base-direction, or-acid-base-log-k
- ● **OR-1.2.B** (acs-accm-organic:II.C.2) Decide whether a ring is aromatic, antiaromatic or neither.
  - EK: Cyclic, planar, a p orbital on every atom, then 4n + 2 or 4n π electrons.
  - Needs: OR-1.2.A
  - P3 · drills: or-aromaticity, dat-pi-electron-count
- ● **OR-1.2.C** (acs-accm-organic:I.B.3, acs-accm-organic:IV.E.2, acs-accm-organic:V.D.2) Choose between SN2, E2 and SN1/E1 from the substrate and the reagent.
  - EK: Strong or weak reagent first, then how hindered the carbon is, then how bulky the base.
  - Needs: OR-3.2.B, OR-1.2.B
  - P3 · drills: or-substitution-or-elimination, dat-rate-doubling
- ● **OR-1.2.D** Say where a substituent directs the next electrophile on a benzene ring and whether it speeds or slows the ring.
  - EK: Donors direct ortho/para and activate; acceptors direct meta and deactivate; halogens direct ortho/para but deactivate.
  - Needs: OR-1.2.C
  - P3 · drills: or-directing-effect, or-activator-rank

### 1.3 What makes a site reactive



- ● **OR-1.3.A** (acs-accm-organic:II.E.1, acs-accm-organic:II.F.1, acs-accm-organic:III.B.1) Assign the hybridisation and geometry of an atom and count σ and π bonds.
  - EK: Count the groups around the atom (σ bonds plus lone pairs): four is sp³, three sp², two sp. A lone pair next to a π bond is delocalised, so that atom is sp². Every bond has one σ; a double bond adds one π, a triple bond two.
  - Needs: CH-2.7.B
  - P3 · drills: or-hybridisation, or-sigma-count
- ● **OR-1.3.B** (acs-accm-organic:I.C.1, acs-accm-organic:VIII.C.2, acs-accm-organic:I.B.1) Explain an acidity difference by atom, resonance, induction or orbital, and recall landmark pKa values.
  - EK: The more stable the conjugate base, the stronger the acid. Landmarks: carboxylic acid about 5, phenol and ammonium about 10, water and alcohols about 16, terminal alkyne about 25, amine N–H about 36, alkene 44, alkane above 50.
  - Needs: OR-1.3.A, CH-8.7.A
  - P3 · drills: or-acidity-factor, or-pka-six
- ● **OR-1.3.C** (acs-accm-organic:I.B.2, acs-accm-organic:I.B.3, acs-accm-organic:IV.E.2) Rank leaving groups and nucleophiles.
  - EK: Good leaving groups are weak bases: I⁻ > Br⁻ > Cl⁻ ≫ F⁻, and sulfonates such as tosylate; HO⁻, RO⁻ and H₂N⁻ do not leave. Nucleophilicity follows basicity in polar aprotic solvents; in protic solvents larger, more polarisable anions are better because small ones are held by hydrogen bonds.
  - Needs: OR-1.3.B
  - P3 · drills: or-leaving-group, or-nucleophile-rank
- ● **OR-1.3.D** (acs-accm-organic:VII.F.2, acs-accm-organic:II.D.1) Rank carbocations, radicals and carbanions by stability.
  - EK: Carbocations and radicals: 3° > 2° > 1° > methyl, by hyperconjugation; allylic and benzylic ones are stabilised by resonance; vinyl and aryl cations are very unstable. Alkyl carbanions run the other way; a carbanion next to C=O is stabilised by resonance.
  - Needs: OR-1.3.A, OR-1.3.C
  - P3 · drills: or-carbocation-rank, or-intermediate-facts

### 1.4 Shape and stereochemistry



- ● **OR-1.4.A** (acs-accm-organic:II.F.2, acs-accm-organic:VIII.C.1) Compare conformations: staggered and eclipsed, gauche and anti, axial and equatorial.
  - EK: Staggered beats eclipsed and anti beats gauche. In a chair, a substituent is more stable equatorial because an axial one suffers 1,3-diaxial interactions; the chair with the larger group equatorial wins.
  - Needs: OR-1.3.A, OR-1.3.D
  - P3 · drills: or-eclipsing-strain, or-chair-preference
- ● **OR-1.4.B** (acs-accm-organic:III.E.1, acs-accm-organic:III.A.2) Classify two structures as identical, constitutional isomers, enantiomers or diastereomers, and count stereoisomers when a meso form exists.
  - EK: Enantiomers are non-superimposable mirror images: every stereocentre inverted. Diastereomers differ at some but not all stereocentres, and include cis–trans isomers. A meso compound has stereocentres and an internal mirror plane, so it removes one from the 2ⁿ count.
  - Needs: OR-1.1.B, OR-1.4.A
  - P3 · drills: or-isomer-pair, or-stereoisomer-count
- ● **OR-1.4.C** (acs-accm-organic:III.E.5, acs-accm-organic:IX.C.2) Compute enantiomeric excess from optical rotation and the composition from the excess.
  - EK: ee = observed specific rotation / rotation of the pure enantiomer × 100. A sample with ee per cent excess contains (100 + ee)/2 per cent of the major enantiomer. A racemic mixture has ee 0 and does not rotate light.
  - Needs: OR-1.4.B
  - P3 · drills: or-ee-from-rotation, or-major-from-ee
- ● **OR-1.4.D** (acs-accm-organic:III.B.2, acs-accm-organic:IX.B.1) Assign E or Z to an alkene and rank alkenes by stability.
  - EK: On each alkene carbon, rank the two groups by atomic number at the first point of difference. High-priority groups on the same side is Z, opposite is E. More substituted alkenes are more stable, and trans beats cis.
  - Needs: OR-1.4.B, OR-1.4.C
  - P3 · drills: or-e-z, or-alkene-stability

## Unit 2 · Alkenes and alkynes

Big ideas: RULES, REAGENT, BALANCE

### 2.1 Additions to alkenes



- ● **OR-2.1.A** (acs-accm-organic:I.B.2, acs-accm-organic:V.F.2, fe-chemical:5.B) Predict the product of adding HX or water to an alkene, with and without Markovnikov orientation.
  - EK: The proton goes where it leaves the more stable carbocation; peroxides and boranes reverse the orientation.
  - Needs: OR-2.3.B, OR-1.4.D
  - P1 · P2 · drills: rx-predict-alkene-hbr, rx-reagent-alkene-hbr, rx-predict-alkene-hbr-peroxide, rx-reagent-alkene-hbr-peroxide, rx-predict-alkene-hydration, rx-reagent-alkene-hydration, rx-predict-alkene-hydroboration, rx-reagent-alkene-hydroboration
- ● **OR-2.1.B** (acs-accm-organic:V.F.1) Predict the product of halogenation, halohydrin formation, hydrogenation, epoxidation, dihydroxylation and ozonolysis.
  - EK: Know which additions are syn and which anti, and that ozonolysis cuts the C=C.
  - Needs: OR-2.3.A, OR-2.1.A
  - P1 · P2 · drills: rx-predict-alkene-bromination, rx-reagent-alkene-bromination, rx-predict-alkene-bromohydrin, rx-reagent-alkene-bromohydrin, rx-predict-alkene-hydrogenation, rx-reagent-alkene-hydrogenation, rx-predict-alkene-epoxidation, rx-reagent-alkene-epoxidation, rx-predict-alkene-dihydroxylation, rx-reagent-alkene-dihydroxylation, rx-predict-alkene-ozonolysis, rx-reagent-alkene-ozonolysis

### 2.2 Alkynes



- ● **OR-2.2.A** Predict the product of reducing, hydrating and alkylating an alkyne.
  - EK: Lindlar gives cis, sodium in ammonia trans; hydration gives a ketone, hydroboration an aldehyde; an acetylide is a carbon nucleophile.
  - Needs: OR-2.3.B, OR-2.1.B
  - P1 · P2 · drills: rx-predict-alkyne-lindlar, rx-reagent-alkyne-lindlar, rx-predict-alkyne-dissolving-metal, rx-reagent-alkyne-dissolving-metal, rx-predict-alkyne-hydration, rx-reagent-alkyne-hydration, rx-predict-alkyne-hydroboration, rx-reagent-alkyne-hydroboration, rx-predict-alkyne-alkylation, rx-reagent-alkyne-alkylation

### 2.3 Additions, one rule at a time



- ● **OR-2.3.A** (acs-accm-organic:V.F.1, acs-accm-organic:V.F.2, acs-accm-organic:III.E.3) State the regiochemistry and the stereochemistry each alkene addition gives.
  - EK: Through a carbocation (HX, H₃O⁺): Markovnikov, no stereocontrol. Radical HBr and hydroboration: anti-Markovnikov, hydroboration syn. Br₂ and halohydrins: anti, through a bromonium ion. H₂/Pd, OsO₄ and peroxyacids: syn.
  - Needs: OR-1.3.D, OR-1.4.D
  - P3 · drills: or-addition-regio, or-addition-stereo
- ● **OR-2.3.B** (acs-accm-organic:VII.F.2, acs-accm-organic:V.D.1) Find the carbocation an addition goes through and decide whether it rearranges; recall the alkyne counterparts.
  - EK: The proton adds to give the more stable cation; a 1,2-hydride or methyl shift follows whenever it gives a more stable one. Alkynes: Lindlar gives cis, Na/NH₃ trans; Hg²⁺ hydration gives a methyl ketone, hydroboration an aldehyde.
  - Needs: OR-2.3.A
  - P3 · drills: or-cation-and-shift, or-alkyne-rules

## Unit 3 · Alcohols and alkyl halides

Big ideas: REAGENT, BALANCE

### 3.1 Substitution, elimination and oxidation



- ● **OR-3.1.A** (acs-accm-organic:V.E.1) Predict the product of converting an alcohol to a halide, a tosylate or an ether, and of oxidising it.
  - EK: PBr₃, SOCl₂ and TsCl make leaving groups; PCC stops at the aldehyde, chromic acid goes to the acid.
  - Needs: OR-3.2.D, OR-3.2.C, OR-1.4.D
  - P1 · P2 · drills: rx-predict-sub-pbr3, rx-reagent-sub-pbr3, rx-predict-sub-socl2, rx-reagent-sub-socl2, rx-predict-sub-tosylation, rx-reagent-sub-tosylation, rx-predict-sub-pcc, rx-reagent-sub-pcc, rx-predict-sub-jones, rx-reagent-sub-jones, rx-predict-sub-jones-secondary, rx-reagent-sub-jones-secondary, rx-predict-sub-williamson, rx-reagent-sub-williamson
- ● **OR-3.1.B** (acs-accm-organic:III.E.4) Predict the substitution or elimination product of an alkyl halide, including Zaitsev against Hofmann, and of a Grignard reagent with CO₂.
  - EK: A small base gives the more substituted alkene, a bulky one the less substituted.
  - Needs: OR-3.2.C, OR-1.2.C, OR-3.1.A
  - P1 · P2 · drills: rx-predict-sub-cyanide, rx-reagent-sub-cyanide, rx-predict-sub-e2-zaitsev, rx-reagent-sub-e2-zaitsev, rx-predict-sub-e2-hofmann, rx-reagent-sub-e2-hofmann, rx-predict-sub-grignard-co2, rx-reagent-sub-grignard-co2

### 3.2 Reading the substrate and the reagent



- ● **OR-3.2.A** (acs-accm-organic:V.D.2, acs-accm-organic:III.E.4) Classify an alkyl halide and say which mechanisms it allows.
  - EK: Methyl and 1°: SN2 (E2 only with a bulky base). 2°: all four, decided by the reagent. 3°: no SN2; E2 with a strong base, SN1/E1 with a weak one. Allylic and benzylic react fast by either. Vinyl and aryl: neither SN1 nor SN2.
  - Needs: OR-1.3.C, OR-1.3.D
  - P3 · drills: or-substrate-class, or-mechanism-rate-rank
- ● **OR-3.2.B** (acs-accm-organic:IV.E.1, acs-accm-organic:IV.E.2, acs-accm-organic:I.C.1) Classify a reagent as strong or weak base and nucleophile, and a solvent as protic or aprotic.
  - EK: Strong base, strong nucleophile: HO⁻, RO⁻. Strong bulky base: tert-butoxide, LDA, DBU. Good nucleophile, weak base: I⁻, Br⁻, HS⁻, RS⁻, N₃⁻, NC⁻. Weak both: H₂O, ROH. Polar aprotic solvents (DMSO, DMF, acetone, acetonitrile) speed SN2; protic solvents favour SN1 and E1.
  - Needs: OR-3.2.A
  - P3 · drills: or-reagent-class, or-solvent-class
- ● **OR-3.2.C** (acs-accm-organic:III.E.3, acs-accm-organic:III.E.4) State the stereochemical outcome of SN2, SN1 and E2.
  - EK: SN2: back-side attack, inversion. SN1: planar carbocation, racemisation (often slightly more inversion). E2: H and leaving group anti-periplanar, which in a cyclohexane means both axial; the reaction is stereospecific.
  - Needs: OR-3.2.B, OR-1.4.B
  - P3 · drills: or-stereo-outcome, or-stereo-consequences
- ● **OR-3.2.D** (acs-accm-organic:V.E.1, acs-accm-organic:V.D.1) Predict how far an alcohol is oxidised and how its OH is turned into a leaving group.
  - EK: PCC, Swern and Dess–Martin stop a 1° alcohol at the aldehyde; aqueous chromic acid takes it to the carboxylic acid. 2° alcohols give ketones; 3° alcohols are not oxidised. TsCl keeps the configuration; PBr₃ and SOCl₂/pyridine invert; HX on a 3° alcohol is SN1.
  - Needs: OR-1.1.C, OR-1.3.C, OR-3.2.C
  - P3 · drills: or-alcohol-oxidation, or-oh-to-leaving-group

## Unit 4 · Aldehydes and ketones

Big ideas: RULES, REAGENT

### 4.1 Additions to the carbonyl group and reactions next to it



- ● **OR-4.1.A** (acs-accm-organic:I.G.1, acs-accm-organic:V.E.1) Predict the product of adding a hydride, a Grignard reagent or a Wittig ylide to a ketone.
  - EK: Nucleophiles add to the carbonyl carbon; a Wittig puts C=C exactly where C=O was.
  - Needs: OR-4.2.A, OR-3.2.D
  - P1 · P2 · drills: rx-predict-carbonyl-nabh4, rx-reagent-carbonyl-nabh4, rx-predict-carbonyl-grignard, rx-reagent-carbonyl-grignard, rx-predict-carbonyl-wittig, rx-reagent-carbonyl-wittig
- ● **OR-4.1.B** Predict the product of a ketone with a diol, an amine, and under reductive amination or Wolff–Kishner conditions.
  - EK: Acetals protect; imines form with primary amines; C=O can be taken down to CH₂.
  - Needs: OR-4.2.B, OR-4.1.A
  - P1 · P2 · drills: rx-predict-carbonyl-acetal, rx-reagent-carbonyl-acetal, rx-predict-carbonyl-imine, rx-reagent-carbonyl-imine, rx-predict-carbonyl-reductive-amination, rx-reagent-carbonyl-reductive-amination, rx-predict-carbonyl-wolff-kishner, rx-reagent-carbonyl-wolff-kishner
- ● **OR-4.1.C** Predict the product of alkylating a ketone through its enolate.
  - EK: LDA makes the enolate completely; the α-carbon is the nucleophile.
  - Needs: OR-4.2.C, OR-4.1.B
  - P1 · P2 · drills: rx-predict-carbonyl-lda-alkylation, rx-reagent-carbonyl-lda-alkylation

### 4.2 Carbonyl reasoning



- ● **OR-4.2.A** (acs-accm-organic:III.F.1, acs-accm-organic:VII.C.2) Rank carbonyl compounds by electrophilicity and say which hydride reduces which.
  - EK: Acyl chloride > anhydride > aldehyde > ketone > ester ≈ acid > amide > carboxylate. NaBH₄ reduces aldehydes and ketones; LiAlH₄ also reduces esters, acids and amides (amides to amines); DIBAL-H at −78 °C stops an ester at the aldehyde.
  - Needs: OR-1.3.C
  - P3 · drills: or-carbonyl-electrophilicity, or-hydride-scope
- ● **OR-4.2.B** (acs-accm-organic:VII.C.1, acs-accm-organic:V.E.1) Decide between addition and substitution at a carbonyl, and recognise hemiacetals and acetals.
  - EK: Both begin with a tetrahedral alkoxide. If the carbonyl carbon carries a leaving group it is expelled (substitution); aldehydes and ketones have none (addition). Acetals form with acid and removal of water, survive base and nucleophiles, and so protect a carbonyl.
  - Needs: OR-4.2.A
  - P3 · drills: or-add-or-substitute, or-acetal-facts
- ● **OR-4.2.C** (acs-accm-organic:VIII.C.2, acs-accm-organic:VII.F.1) Recall α-hydrogen pKa values and choose conditions for the kinetic or thermodynamic enolate.
  - EK: α-H of a ketone about 20, an ester about 25, a β-diketone about 9. LDA (its amine has pKa about 36) at −78 °C removes the less hindered proton completely: the kinetic enolate. Alkoxide at room temperature equilibrates to the more substituted, thermodynamic enolate.
  - Needs: OR-1.3.B, OR-4.2.A, OR-4.2.B
  - P3 · drills: or-alpha-pka, or-enolate-choice

## Unit 5 · Carboxylic acids and their derivatives

Big ideas: RULES, REAGENT

### 5.1 Acyl substitution and reduction



- ● **OR-5.1.A** (acs-accm-organic:V.E.1) Predict the product of interconverting acids, acyl chlorides, esters and amides.
  - EK: Addition then elimination; a more reactive derivative can make a less reactive one, not the reverse.
  - Needs: OR-5.2.A, OR-4.2.C
  - P1 · P2 · drills: rx-predict-acyl-acid-chloride, rx-reagent-acyl-acid-chloride, rx-predict-acyl-fischer, rx-reagent-acyl-fischer, rx-predict-acyl-amide, rx-reagent-acyl-amide, rx-predict-acyl-saponification, rx-reagent-acyl-saponification
- ● **OR-5.1.B** Predict the product of reducing an ester or an amide, of adding excess Grignard reagent to an ester, and of a Claisen condensation.
  - EK: LiAlH₄ takes an ester to a primary alcohol and an amide to an amine; two equivalents of Grignard give a tertiary alcohol.
  - Needs: OR-5.2.A, OR-5.1.A
  - P1 · P2 · drills: rx-predict-acyl-lah-ester, rx-reagent-acyl-lah-ester, rx-predict-acyl-grignard-ester, rx-reagent-acyl-grignard-ester, rx-predict-acyl-lah-amide, rx-reagent-acyl-lah-amide, rx-predict-acyl-claisen, rx-reagent-acyl-claisen

### 5.2 Acyl reasoning



- ● **OR-5.2.B** (acs-accm-organic:III.A.1, acs-accm-organic:IX.B.1) Recognise the carboxylic acid derivatives, including cyclic ones, and give their hydrolysis products.
  - EK: Ester RCO₂R′, amide RCONR₂, anhydride (RCO)₂O, acyl chloride RCOCl, nitrile RCN; a cyclic ester is a lactone, a cyclic amide a lactam. Hydrolysis returns the carboxylic acid plus the alcohol, amine, second acid or ammonia.
  - Needs: OR-4.2.A
  - P3 · drills: or-derivative-names, or-hydrolysis-products
- ● **OR-5.2.A** (acs-accm-organic:VIII.A.1, acs-accm-organic:V.E.1) Decide whether an acyl substitution goes forward and what hydrolysis needs.
  - EK: An acyl derivative converts only into a less reactive one: chloride → anhydride → ester → amide, never back without activation. Saponification is irreversible because the acid ends as carboxylate; acid-catalysed hydrolysis is the reverse of Fischer esterification.
  - Needs: OR-5.2.B, OR-4.2.B
  - P3 · drills: or-acyl-forward, or-hydrolysis-conditions

## Unit 6 · Benzene and substituted benzenes

Big ideas: RULES, REAGENT

### 6.1 Electrophilic substitution and side-chain reactions



- ● **OR-6.1.D** (acs-accm-organic:V.D.2) Predict nucleophilic aromatic substitution: when it happens and where.
  - EK: SNAr needs a leaving group with strong withdrawing groups (NO₂) ortho or para to it to stabilise the Meisenheimer complex; F is the best leaving group here. Without them, a strong base can go by benzyne.
  - Needs: OR-1.4.D
  - P1 · drills: or-snar, or-snar-2
- ● **OR-6.1.A** (bruice-8e:18, acs-accm-organic:V.D.2, fe-chemical:5.B) Predict the product of brominating, nitrating and acylating benzene.
  - EK: Substitution, not addition: the ring gets its aromaticity back.
  - Needs: OR-6.2.A, OR-6.1.D
  - P1 · P2 · drills: rx-predict-aromatic-bromination, rx-reagent-aromatic-bromination, rx-predict-aromatic-nitration, rx-reagent-aromatic-nitration, rx-predict-aromatic-acylation, rx-reagent-aromatic-acylation
- ● **OR-6.1.B** (bruice-8e:18) Predict where a second substituent goes on a substituted benzene.
  - EK: Donors: ortho and para. Acceptors: meta.
  - Needs: OR-6.2.B, OR-6.1.A
  - P1 · P2 · drills: rx-predict-aromatic-nitration-toluene, rx-reagent-aromatic-nitration-toluene, rx-predict-aromatic-bromination-nitrobenzene, rx-reagent-aromatic-bromination-nitrobenzene
- ● **OR-6.1.C** (bruice-8e:18) Predict the product of reducing a nitro group and of oxidising or brominating a benzylic position.
  - EK: Nitro to amino; any benzylic C–H side chain to CO₂H; NBS brominates the benzylic carbon.
  - Needs: OR-6.1.B
  - P1 · P2 · drills: rx-predict-aromatic-nitro-reduction, rx-reagent-aromatic-nitro-reduction, rx-predict-aromatic-side-chain-oxidation, rx-reagent-aromatic-side-chain-oxidation, rx-predict-aromatic-benzylic-bromination, rx-reagent-aromatic-benzylic-bromination

### 6.2 Aromatic reasoning



- ● **OR-6.2.A** (acs-accm-organic:I.B.2, acs-accm-organic:V.D.2) Name the electrophile each aromatic substitution uses and the limits of the Friedel–Crafts reactions.
  - EK: Br₂/FeBr₃ gives a polarised bromine, HNO₃/H₂SO₄ gives NO₂⁺, RCl/AlCl₃ a carbocation, RCOCl/AlCl₃ an acylium ion. Alkylation rearranges and over-alkylates; acylation does neither. Neither works on strongly deactivated rings.
  - Needs: OR-1.2.B, OR-1.3.D
  - P3 · drills: or-eas-electrophile, or-friedel-crafts-limits
- ● **OR-6.2.B** (acs-accm-organic:V.A.4, acs-accm-organic:V.F.2) Choose the order of two aromatic substitutions and explain why a group directs where it does.
  - EK: Install first the group whose directing effect puts the second where you want it. Lone-pair donors direct ortho/para by resonance; halogens also do, though they deactivate by induction; groups with a positive or partial positive atom on the ring direct meta.
  - Needs: OR-1.2.D, OR-6.2.A
  - P3 · drills: or-eas-order, or-directing-why

## Unit 7 · Making carbon–carbon bonds

Big ideas: RULES

### 7.1 Condensations and cycloadditions



- ● **OR-7.1.A** (acs-accm-organic:II.E.2) Predict the product of an aldol condensation and of a Diels–Alder reaction.
  - EK: Aldol: new C=C between the α and β carbons. Diels–Alder: a cyclohexene, with the dienophile's geometry kept.
  - Needs: OR-7.2.A, OR-7.2.B, OR-4.2.C
  - P1 · P2 · drills: rx-predict-cc-aldol-condensation, rx-reagent-cc-aldol-condensation, rx-predict-cc-diels-alder, rx-reagent-cc-diels-alder

### 7.2 Carbon–carbon bond reasoning



- ● **OR-7.2.A** (acs-accm-organic:I.B.3, acs-accm-organic:V.E.1) Name the product type of an aldol, Claisen, Michael and Robinson reaction and the conditions each needs.
  - EK: Aldol: β-hydroxy carbonyl, dehydrating on heating to the enone. Claisen: β-keto ester, needing a full equivalent of alkoxide. Michael: 1,5-dicarbonyl. Robinson: Michael then intramolecular aldol. A crossed aldol is clean when one partner has no α-hydrogen.
  - Needs: OR-4.2.C
  - P3 · drills: or-condensation-product-type, or-condensation-conditions
- ● **OR-7.2.B** (acs-accm-organic:II.E.2, acs-accm-organic:III.E.3) State what a Diels–Alder reaction needs and what it preserves.
  - EK: An s-cis diene (best electron-rich) and a dienophile (best electron-poor) join in one concerted step, six π electrons making two σ bonds and a cyclohexene. Dienophile stereochemistry is retained; cyclic dienes favour the endo product.
  - Needs: OR-1.2.B, OR-1.4.D, OR-7.2.A
  - P3 · drills: or-diels-alder-needs, or-diels-alder-outcome

## Unit 8 · Mechanisms with curved arrows

Big ideas: RULES

### 8.1 The four patterns



- ● **OR-8.1.E** (acs-accm-organic:VII.C.3, acs-accm-organic:I.B.2, acs-accm-organic:I.B.3) Read a step's curved arrows: name the nucleophilic and electrophilic atoms and the formal charges that result.
  - EK: An arrow starts at a lone pair or a bond and ends at an atom or bond; the atom that gains a bond from a lone pair loses formal negative charge, the donor gains positive.
  - Needs: OR-1.4.D, ST-3.1.A
  - P1 · drills: or-arrow-read, or-arrow-sites
- ● **OR-8.1.F** (acs-accm-organic:VII.C.1, acs-accm-organic:VIII.G.1) Put the steps of an acid- or base-catalysed carbonyl mechanism in order.
  - EK: Acid catalysis: protonate, add, deprotonate, protonate, eliminate, deprotonate (PADPED for Fischer esterification and acetal formation).
  - Needs: OR-8.1.E
  - P1 · drills: or-mech-order, or-mech-intermediate
- ● **OR-8.1.G** (acs-accm-organic:V.D.1, acs-accm-organic:VII.F.2) Predict carbocation rearrangements by hydride and alkyl shifts.
  - EK: A 1,2-hydride or 1,2-methyl shift happens when it turns a 1° or 2° cation into a more stable 2° or 3° (or resonance-stabilised) one; ring expansion relieves strain.
  - Needs: OR-8.1.F
  - P1 · drills: or-rearrangement, or-rearrangement-2
- ● **OR-8.1.A** (acs-accm-organic:VII.C.3, acs-accm-organic:VII.D.1) Draw the SN2 mechanism: both arrows and the products.
  - EK: Backside attack and loss of the leaving group in one step; inversion.
  - Needs: OR-8.1.G
  - P1 · drills: st-mech-sn2-1, or-sn2-requirements
- ● **OR-8.1.B** Draw the E2 mechanism: three arrows and the products.
  - EK: Base to H, C–H electrons to the π bond, leaving group out; anti-periplanar.
  - Needs: OR-8.1.A
  - P1 · drills: st-mech-e2-1, or-e2-requirements
- ● **OR-8.1.C** Draw the two steps of electrophilic addition of HX to an alkene, with the carbocation.
  - EK: The π bond takes the proton to give the more stable cation; the halide then adds.
  - Needs: OR-8.1.B
  - P1 · drills: st-mech-hbr-addition-1, st-mech-hbr-addition-2
- ● **OR-8.1.D** Draw the two steps of nucleophilic acyl substitution, with the tetrahedral intermediate.
  - EK: Addition to C=O, then elimination of the leaving group.
  - Needs: OR-8.1.C
  - P1 · drills: st-mech-acyl-substitution-1, st-mech-acyl-substitution-2

## Unit 9 · Physical organic chemistry and practice (extension)

Big ideas: RULES

### 9.1 Physical organic chemistry



- ● **OR-9.1.A** (acs-accm-organic:VIII.C.1) Find the axial–equatorial ratio of a substituted cyclohexane from its A-value, or the A-value from the ratio.
  - EK: K = [equatorial]/[axial] = e^(A/RT); at 25 °C, 7.3 kJ/mol (tert-butyl ~20 kJ/mol) puts nearly everything equatorial.
  - Needs: OR-1.4.A, OR-8.1.D, CH-5.6.C
  - P1 · drills: or-a-value-ratio, or-a-value-from-ratio
- ● **OR-9.1.B** (acs-accm-organic:III.E.2) Classify a reaction as regioselective, regiospecific, stereoselective or stereospecific.
  - EK: Specific: different stereoisomeric starting materials give different stereoisomeric products (anti addition, SN2 inversion). Selective: one product forms in excess of the others.
  - Needs: OR-9.1.A
  - P1 · drills: or-specific-selective, or-specific-selective-2
- ● **OR-9.1.C** (acs-accm-organic:VII.F.1, acs-accm-organic:VII.F.2, acs-accm-organic:VII.A.1, acs-accm-general:VII.F.1) Predict kinetic and thermodynamic products and compute a product ratio from a free-energy difference.
  - EK: Low temperature, irreversible: the lower barrier wins (1,2-addition to a diene); high temperature, reversible: the more stable product wins (1,4). Ratio = e^(ΔΔG/RT).
  - Needs: OR-9.1.B
  - P1 · drills: or-control-ratio, or-diene-control
- ● **OR-9.1.D** (acs-accm-organic:VII.B.1) Use a rate law to tell SN1 from SN2 and predict how the rate changes with concentrations.
  - EK: SN2: rate = k[RX][Nu]; SN1: rate = k[RX], independent of the nucleophile.
  - Needs: OR-9.1.C
  - P1 · drills: or-rate-law-factor, or-rate-law-mechanism
- ● **OR-9.1.E** (acs-accm-organic:II.D.1, acs-accm-organic:V.D.3) Estimate the enthalpy of a radical step from bond energies and the product ratio of a radical halogenation.
  - EK: ΔH = Σ bonds broken − Σ bonds formed; product share ∝ (number of H) × (relative reactivity), about 1 : 3.8 : 5 for Cl· at 1°, 2°, 3° and 1 : 82 : 1600 for Br·.
  - Needs: OR-9.1.D
  - P1 · drills: or-radical-step-dh, or-halogenation-share
- ● **OR-9.1.F** () Use the Hammett equation log(k/k₀) = ρσ to predict or interpret substituent effects.
  - EK: σ > 0 for withdrawing groups; ρ > 0 when negative charge builds in the transition state (ester hydrolysis), ρ < 0 when positive charge builds.
  - Needs: OR-9.1.E
  - P1 · drills: or-hammett-rate, or-hammett-rho
- ● **OR-9.1.G** (acs-accm-organic:II.E.2, acs-accm-organic:VI.C.2, acs-accm-inorganic:V.B.1) Apply the Woodward–Hoffmann rules to electrocyclic reactions and cycloadditions, thermal or photochemical.
  - EK: Electrocyclic: 4n electrons conrotatory thermally, 4n + 2 disrotatory; light reverses both. Suprafacial cycloaddition is thermally allowed for 4n + 2 electrons ([4 + 2]), photochemically for 4n ([2 + 2]).
  - Needs: OR-9.1.F
  - P1 · drills: or-electrocyclic-mode, or-cycloaddition-allowed

### 9.2 Synthesis and laboratory practice



- ● **OR-9.2.A** (acs-accm-organic:IV.D.2, acs-accm-organic:V.D.4, acs-accm-inorganic:IX.G.5) Compute atom economy and E-factor, and choose the greener reagent or solvent.
  - EK: Atom economy = M(product)/Σ M(reactants) × 100%; E-factor = mass of waste ÷ mass of product; catalytic and addition reactions score best.
  - Needs: OR-9.1.G
  - P1 · drills: or-atom-economy, or-e-factor
- ● **OR-9.2.B** (acs-accm-organic:I.E.1, acs-accm-organic:V.A.2) Work with molar equivalents, the limiting reagent and the overall yield of a multistep synthesis.
  - EK: Equivalents = mol reagent ÷ mol substrate; overall yield = product of the step yields, so long linear routes lose most of the material.
  - Needs: OR-9.2.A
  - P1 · drills: or-overall-yield, or-equivalents-mass
- ● **OR-9.2.C** (acs-accm-organic:VIII.E.1, acs-accm-organic:VIII.A.1) Compute the equilibrium yield of a Fischer esterification and say how to drive it further.
  - EK: K ≈ 4 for acid + alcohol ⇌ ester + water; excess alcohol or removing water (Dean–Stark, drying agent) pushes it on.
  - Needs: OR-9.2.B
  - P1 · drills: or-fischer-yield, or-drive-equilibrium
- ● **OR-9.2.D** (acs-accm-organic:IX.A.1, acs-accm-organic:IX.A.3) Choose and read a classical chemical test for a functional group.
  - EK: Tollens (aldehydes, silver mirror), 2,4-DNP (aldehydes and ketones, orange solid), iodoform (methyl ketones, yellow solid), Br₂ decolourised (alkenes), Lucas (3° alcohol turns cloudy fastest), FeCl₃ (phenols, violet).
  - Needs: OR-9.2.C
  - P1 · drills: or-chem-tests, or-wet-vs-instrument
- ● **OR-9.2.E** (acs-accm-organic:I.D.1) Place landmark discoveries in organic chemistry and say what each showed.
  - EK: Wöhler's urea (1828) blurred organic and inorganic; Pasteur's tartrate crystals (1848) revealed molecular chirality; Kekulé's benzene (1865); van 't Hoff and Le Bel's tetrahedral carbon (1874).
  - Needs: OR-9.2.D
  - P1 · drills: or-history, or-history-2
- ● **OR-9.2.F** (acs-accm-organic:V.D.1) Classify a transformation as addition, elimination, substitution, rearrangement, oxidation or reduction.
  - EK: Compare formulas: addition gains atoms across a π bond, elimination loses a small molecule, substitution swaps one group, rearrangement keeps the formula, redox changes H/O count at carbon.
  - Needs: OR-9.2.E
  - P1 · drills: or-reaction-type, or-reaction-type-2

## Unit 10 · Organometallic reagents and catalysis (extension)

Big ideas: REAGENT

### 10.1 Organometallic reagents and Pd catalysis



- ● **OR-10.1.A** (acs-accm-organic:I.G.1) Use organolithium and Grignard reagents as strong bases and nucleophiles, counting the equivalents acidic hydrogens consume.
  - EK: R–MgX and R–Li are carbanion-like: every O–H, N–H, S–H or terminal alkyne C–H destroys one equivalent before any C=O addition; D₂O puts D where the metal was.
  - Needs: OR-4.2.C, OR-7.2.B
  - P1 · drills: or-grignard-equivalents, or-organometal-base
- ● **OR-10.1.B** () Choose between Grignard, organolithium and Gilman (cuprate) reagents for 1,2- or 1,4-addition and for coupling.
  - EK: Hard RLi and RMgX add 1,2 to enones; soft R₂CuLi adds 1,4 (conjugate) and couples with alkyl and vinyl halides; cuprates stop at the ketone with acid chlorides.
  - Needs: OR-10.1.A
  - P1 · drills: or-cuprate, or-reagent-choice
- ● **OR-10.1.C** () Name a Pd-catalysed cross-coupling from its partners and track Pd's oxidation state and electron count around the cycle.
  - EK: Suzuki (boronic acid), Stille (stannane), Negishi (organozinc), Heck (alkene), Sonogashira (terminal alkyne, Cu co-catalyst), Buchwald–Hartwig (amine); Pd(0) → oxidative addition Pd(II) → transmetalation → reductive elimination back to Pd(0).
  - Needs: OR-10.1.B
  - P1 · drills: or-coupling-name, or-pd-cycle
- ● **OR-10.1.D** () Predict products of olefin metathesis, homogeneous hydrogenation and hydroformylation.
  - EK: Metathesis swaps alkylidene halves (ring-closing gives a ring plus ethylene); Wilkinson's catalyst hydrogenates the least hindered alkene syn; hydroformylation adds H and CHO across C=C.
  - Needs: OR-10.1.C
  - P1 · drills: or-metathesis, or-catalysis-facts

## Unit 11 · Spectroscopy for structure (extension)

Big ideas: RULES

### 11.1 Reading IR, NMR and mass spectra



- ● **OR-11.1.A** (acs-accm-organic:I.D.2, acs-accm-organic:IX.A.2) Read functional groups from landmark IR bands.
  - EK: O–H broad 3200–3600, acid O–H very broad 2500–3300, N–H 3300–3500 (two bands for NH₂), ≡C–H 3300 sharp, sp² C–H just above 3000 and sp³ just below, C≡N 2250, C≡C 2100–2260, C=O about 1700 cm⁻¹ (ester higher, amide and conjugated lower).
  - Needs: OR-1.3.A
  - P3 · drills: or-ir-landmarks, or-ir-distinguish
- ● **OR-11.1.B** (acs-accm-organic:III.D.2, acs-accm-organic:I.D.2) Use splitting, integration and landmark shifts in a ¹H NMR spectrum.
  - EK: n equivalent neighbours split a signal into n + 1 peaks. Landmarks in ppm: alkyl 0.9–1.5, next to C=O 2–2.5, next to O 3.3–4, vinyl 4.5–6.5, aromatic 6.5–8, aldehyde 9–10, carboxylic acid 10–12.
  - Needs: OR-11.1.A
  - P3 · drills: or-nmr-splitting, or-nmr-shift-landmarks
- ● **OR-11.1.C** (acs-accm-organic:I.A.1, acs-accm-organic:I.D.2) Read a mass spectrum: isotope patterns, the nitrogen rule and common losses.
  - EK: One Br gives M and M + 2 about 1:1; one Cl about 3:1. An odd molecular mass means an odd number of nitrogens. Common losses: 15 CH₃, 18 H₂O, 29 C₂H₅ or CHO; common ions: 43 acylium or propyl, 77 phenyl, 91 benzyl (tropylium).
  - Needs: OR-1.1.A, OR-11.1.B
  - P3 · drills: or-ms-patterns, or-ms-fragments
