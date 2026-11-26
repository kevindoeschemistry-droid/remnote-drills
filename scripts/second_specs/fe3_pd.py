"""Thin wrapper so scripts/insert_objs.py can write fe3.py's PD objectives into process-design.yaml.
fe3.py spans three frameworks and insert_objs takes one at a time; the items themselves stay in fe3.py.
Usage: python3 scripts/insert_objs.py fe3_pd
"""
import fe3

FRAMEWORK = "process-design"
PRACTICE = "P1"
UNITS = fe3.PD_UNITS
TOPICS = fe3.PD_TOPICS
OBJS = fe3.PD_OBJS
