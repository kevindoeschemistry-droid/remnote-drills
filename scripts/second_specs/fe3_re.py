"""Thin wrapper so scripts/insert_objs.py can write fe3.py's RE objectives into reaction-engineering.yaml.
fe3.py spans three frameworks and insert_objs takes one at a time; the items themselves stay in fe3.py.
Usage: python3 scripts/insert_objs.py fe3_re
"""
import fe3

FRAMEWORK = "reaction-engineering"
PRACTICE = "P1"
UNITS = fe3.RE_UNITS
TOPICS = fe3.RE_TOPICS
OBJS = fe3.RE_OBJS
