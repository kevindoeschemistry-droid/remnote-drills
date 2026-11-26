"""Thin wrapper so scripts/insert_objs.py can write fe3.py's MT objectives into materials.yaml.
fe3.py spans three frameworks and insert_objs takes one at a time; the items themselves stay in fe3.py.
Usage: python3 scripts/insert_objs.py fe3_mt
"""
import fe3

FRAMEWORK = "materials"
PRACTICE = "P1"
UNITS = fe3.MT_UNITS
TOPICS = fe3.MT_TOPICS
OBJS = fe3.MT_OBJS
