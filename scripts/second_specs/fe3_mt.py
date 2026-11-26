"""Thin wrapper so scripts/insert_objs.py can write fe3.py's MT objectives into materials.yaml.
fe3.py spans three frameworks and insert_objs takes one at a time; the items themselves stay in fe3.py.
Usage: python3 scripts/insert_objs.py fe3_mt
"""
import importlib.util as _il, pathlib as _p

# Imported by path, not by name: scripts/second_specs cannot go on sys.path, because its own re.py shadows the
# standard library's (the mistake recorded in CLAUDE.md). scripts/opl_fill.py loads every file in this folder,
# so a bare "import fe3" here breaks that script as well as this one.
_s = _il.spec_from_file_location("fe3_items", _p.Path(__file__).with_name("fe3.py"))
fe3 = _il.module_from_spec(_s); _s.loader.exec_module(fe3)

FRAMEWORK = "materials"
PRACTICE = "P1"
UNITS = fe3.MT_UNITS
TOPICS = fe3.MT_TOPICS
OBJS = fe3.MT_OBJS
