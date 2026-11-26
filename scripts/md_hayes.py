"""Register the Hayes group's own training materials as standards for Molecular Simulation (MD) and add them to its
basis. Idempotent. Run before scripts/second_specs/md2.py's items are inserted. Usage: python3 scripts/md_hayes.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ORI = [("EXP", "Expectations: group goals, values, hours, group meeting, publication and conference norms"),
       ("START", "Startup: cluster, Slack and office access"),
       ("CL1", "Cluster: bash and linux, logging in to hpc3, the shell-novice tutorial"),
       ("CL2", "Cluster: lab storage — home, CRSP and BeeGFS quotas, group paths, permissions and the sticky bit"),
       ("CL3", "Cluster: ssh keys"),
       ("CL4", "Cluster: the SLURM queue — login versus compute nodes, interactive jobs and sbatch, and the options -p, -A, --time, --gres, --mem"),
       ("LIT", "Literature: the foundational λ-dynamics, MSλD, ALF, implicit-constraint and BLaDE papers, and the large-sequence-space applications"),
       ("TUT1", "Tutorial 1: molecular dynamics in CHARMM — running CHARMM, CHARMM-GUI setup, propka protonation, periodic boundaries, ions, and BLaDE equilibration and production"),
       ("TUT2", "Tutorial 2: multisite λ dynamics — system.inp against step5_production.inp, alchemical_definitions.inp, toppar soft link, the aa_stream patch/select/delete/blocksetup streams, and alf_info.py"),
       ("TUT3", "Tutorial 3: adaptive landscape flattening — runflat, runprod and postprocess, the flattening and production schedules, best practice for loss, bias and implicit constraints, and cleanup"),
       ("TUT4", "Tutorial 4: CHARMM scripting and engines — titles, set/calc, @ and @@, ? values, stream, if/goto, and the standard, DOMDEC, BLaDE and OpenMM engines"),
       ("INST", "Installation: CHARMM and pyCHARMM builds, ALF, conda, and the module set used on hpc3"),
       ("ETC", "Etcetera: conferences and other useful links")]
EXA = [("SYS", "The four example systems: benzene-derivative solvation, p38 ligand binding, protein G site-saturation folding, T4 lysozyme side-chain mutation"),
       ("PREP", "The per-system prep directory: alf_info.py, nsubs, nblocks, ncentral, nreps, toppar and the build scripts"),
       ("TMPL", "The templates directory: subsetAll.sh job chaining with SLURM dependencies, runflat.sh, runprod.sh, postprocess.sh, msld_flat.inp and msld_prod.inp"),
       ("LIN", "Telling nonlinear from linearized ALF by the lmalf key, and the 8–9 substituent limit of linearized ALF")]
STDS = [
 {"id": "hayes-orientation", "name": "Hayes Group New Student Orientation (RyanHayes-Lab/Orientation)",
  "publisher": "Hayes group, University of California, Irvine", "kind": "course", "read": "full",
  "url": "https://github.com/RyanHayes-Lab/Orientation",
  "note": "All nine files read in full in Nov 2026 (repository last updated Mar 2026): README, Expectations, Startup, Cluster, Literature, Tutorial, Installation, Etcetera. This is Kevin's own group's training path, so it is the primary basis for the λ-dynamics, ALF and workflow units. Items are its documents and the tutorial's four sections, paraphrased. Lab-internal paths, accounts and contacts are not drilled; cards state a cluster path only where the task is to recognise what kind of path it is.",
  "items": [{"code": c, "title": t} for c, t in ORI]},
 {"id": "hayes-lambda-examples", "name": "RyanHayes-Lab/lambda-dynamics-examples (example run files)",
  "publisher": "Hayes group, University of California, Irvine", "kind": "reference", "read": "part",
  "url": "https://github.com/RyanHayes-Lab/lambda-dynamics-examples",
  "note": "README, the templates/charmm scripts (subsetAll.sh, runflat.sh, runprod.sh, postprocess.sh) and the p38 prep directory's alf_info.py, nsubs, nblocks, ncentral and nreps read in Nov 2026. The CHARMM input decks, topology files and per-substituent PDB and RTF files were not read line by line, so no card asks for their contents.",
  "items": [{"code": c, "title": t} for c, t in EXA]},
]
p = os.path.join(ROOT, "drills/standards.yaml")
t = open(p).read()
for s in STDS:
    if f'"id": "{s["id"]}"' not in t and f'id: {s["id"]},' not in t:
        t = t.rstrip("\n") + "\n- " + json.dumps(s, ensure_ascii=False) + "\n"
open(p, "w").write(t)

# basis: the orientation is read in full and is the group's own curriculum, so it becomes MD's primary.
p = os.path.join(ROOT, "drills/frameworks/molecular-simulation.yaml")
t = open(p).read()
if "hayes-orientation" not in t:
    old = """basis:
  primary: livecoms
  also: [livecoms-afe, alchemistry-wiki]"""
    new = """basis:
  primary: hayes-orientation
  also: [livecoms, livecoms-afe, alchemistry-wiki, hayes-lambda-examples]"""
    assert old in t, "basis block not found"
    t = t.replace(old, new)
    t = t.replace(
        "No standard exists for this subject; triangulated from best-practice papers, textbooks and the Hayes group tutorial.",
        "No accredited standard exists for this subject. Kevin's own group's orientation repository is the closest thing to a curriculum for the work he will actually do, and it was read in full, so it is primary; the best-practice papers and the alchemistry wiki fix the parts it assumes.")
    open(p, "w").write(t)
print("ok")
