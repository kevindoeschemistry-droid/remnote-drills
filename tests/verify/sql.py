"""SQL drills (drills/problems/sq-*.yaml): answers are checked by running the query.

The cards are written in Oracle SQL, the dialect of the 1Z0-071 exam they follow. The verifier
runs them on an in-memory SQLite database built from the tables below, after a small translation
(MINUS -> EXCEPT, FETCH FIRST -> LIMIT, FROM DUAL dropped, DATE literals, AS before a
DML table alias) and with the Oracle
single-row functions SQLite lacks (NVL, NVL2, DECODE, MOD, TRUNC, Oracle ROUND, INSTR with four
arguments, LPAD, RPAD, INITCAP, ADD_MONTHS, LAST_DAY, MONTHS_BETWEEN, NEXT_DAY) written here in
Python. Where Oracle and SQLite would disagree (nested aggregates, ANY and ALL), a case carries the
verifier's own query `vq` written another way.

The tables are typed here a second time, apart from the figures on the cards; check_tables() in
the verifier's run compares the two.
"""
import calendar
import datetime as dt
import re
import sqlite3
from decimal import ROUND_HALF_UP, Decimal

N = None
TABLES = {
    "emp": (["id", "name", "dept", "salary", "mgr", "hired"], [
        (1, "Ana", "Sales", 5000, N, 2019),
        (2, "Ben", "Sales", 4000, 1, 2021),
        (3, "Cy", "IT", 6000, N, 2018),
        (4, "Dee", "IT", 5500, 3, 2020),
        (5, "Eli", "IT", N, 3, 2022),
        (6, "Fay", "HR", 4500, N, 2021),
    ]),
    "depts": (["dept", "city"], [("Sales", "Boston"), ("IT", "Austin"), ("Ops", "Denver")]),
    "grades": (["grade", "lo", "hi"], [("A", 0, 4499), ("B", 4500, 5499), ("C", 5500, 9999)]),
    "a": (["n"], [(1,), (2,), (2,), (3,)]),
    "b": (["n"], [(2,), (3,), (4,)]),
    "sales": (["day", "store", "product", "units"], [
        (1, "S1", "P1", 3), (1, "S2", "P1", 5), (1, "S1", "P2", 2),
        (2, "S1", "P1", 4), (2, "S2", "P2", 6), (3, "S2", "P1", 1),
    ]),
    "products": (["product", "category", "price"], [("P1", "Tea", 4), ("P2", "Cake", 10)]),
    "stores": (["store", "region"], [("S1", "West"), ("S2", "East")]),
}
DBS = {
    "emp": ["emp", "depts", "grades"],
    "sets": ["a", "b"],
    "star": ["sales", "products", "stores"],
}
SCHEMA = """
CREATE TABLE emp (id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary REAL, mgr INTEGER, hired INTEGER);
CREATE TABLE depts (dept TEXT PRIMARY KEY, city TEXT);
CREATE TABLE grades (grade TEXT, lo REAL, hi REAL);
CREATE TABLE a (n INTEGER);
CREATE TABLE b (n INTEGER);
CREATE TABLE sales (day INTEGER, store TEXT, product TEXT, units INTEGER);
CREATE TABLE products (product TEXT PRIMARY KEY, category TEXT, price REAL);
CREATE TABLE stores (store TEXT PRIMARY KEY, region TEXT);
"""


# ── Oracle single-row functions ────────────────────────────────────────────
def _round(x, d=0):
    if x is None or d is None:
        return None
    q = Decimal(1).scaleb(-int(d))
    r = Decimal(str(x)).quantize(q, rounding=ROUND_HALF_UP) if d >= 0 else \
        (Decimal(str(x)) / q).quantize(Decimal(1), rounding=ROUND_HALF_UP) * q
    return float(r)


def _trunc(x, d=0):
    if x is None:
        return None
    f = Decimal(10) ** int(d)
    v = Decimal(str(x)) * f
    return float(int(v) / f)


def _instr(s, sub, pos=1, occ=1):
    if s is None or sub is None:
        return None
    start = pos - 1
    for _ in range(occ):
        i = s.find(sub, start)
        if i < 0:
            return 0
        start = i + 1
    return i + 1


def _pad(left):
    def f(s, n, ch=" "):
        s = str(s)
        if len(s) >= n:
            return s[:n]
        fill = (ch * n)[: n - len(s)]
        return fill + s if left else s + fill
    return f


def _date(s):
    return dt.date.fromisoformat(s)


def _add_months(s, n):
    d = _date(s)
    m = d.month - 1 + int(n)
    y, m = d.year + m // 12, m % 12 + 1
    last = calendar.monthrange(y, m)[1]
    day = last if d.day == calendar.monthrange(d.year, d.month)[1] else min(d.day, last)
    return dt.date(y, m, day).isoformat()


def _last_day(s):
    d = _date(s)
    return d.replace(day=calendar.monthrange(d.year, d.month)[1]).isoformat()


def _months_between(s1, s2):
    a, b = _date(s1), _date(s2)
    la = a.day == calendar.monthrange(a.year, a.month)[1]
    lb = b.day == calendar.monthrange(b.year, b.month)[1]
    whole = (a.year - b.year) * 12 + (a.month - b.month)
    if a.day == b.day or (la and lb):
        return float(whole)
    return whole + (a.day - b.day) / 31


def _next_day(s, name):
    d = _date(s)
    target = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"].index(name.upper())
    k = (target - d.weekday()) % 7 or 7
    return (d + dt.timedelta(days=k)).isoformat()


def _decode(*args):
    x, rest = args[0], list(args[1:])
    while len(rest) >= 2:
        s, r = rest.pop(0), rest.pop(0)
        if x == s or (x is None and s is None):
            return r
    return rest[0] if rest else None


def _translate(q):
    q = re.sub(r"\bMINUS\b", "EXCEPT", q)
    q = re.sub(r"\s+FROM\s+DUAL\b", "", q, flags=re.I)
    q = re.sub(r"OFFSET\s+(\d+)\s+ROWS?\s+FETCH\s+(?:FIRST|NEXT)\s+(\d+)\s+ROWS?\s+ONLY", r"LIMIT \2 OFFSET \1", q)
    q = re.sub(r"FETCH\s+(?:FIRST|NEXT)\s+(\d+)\s+ROWS?\s+ONLY", r"LIMIT \1", q)
    q = re.sub(r"DATE\s+'([\d-]+)'\s*-\s*DATE\s+'([\d-]+)'", r"(julianday('\1') - julianday('\2'))", q)
    q = re.sub(r"DATE\s+'([\d-]+)'\s*\+\s*(\d+)", r"date('\1', '+\2 days')", q)
    q = re.sub(r"DATE\s+'([\d-]+)'", r"'\1'", q)
    q = re.sub(r"\b(UPDATE|DELETE FROM)\s+(\w+)\s+(?!SET\b|WHERE\b)(\w+)\s+(SET|WHERE)\b", r"\1 \2 AS \3 \4", q)
    q = q.replace("||", " || ")
    return q


def connect(db):
    c = sqlite3.connect(":memory:")
    for name, n, f in [("NVL", 2, lambda a, b: b if a is None else a),
                       ("NVL2", 3, lambda a, b, d: d if a is None else b),
                       ("DECODE", -1, _decode), ("MOD", 2, lambda a, b: None if a is None or b is None else (a if b == 0 else a - b * int(a / b))),
                       ("ROUND", 1, _round), ("ROUND", 2, _round), ("TRUNC", 1, _trunc), ("TRUNC", 2, _trunc),
                       ("INSTR", 2, _instr), ("INSTR", 3, _instr), ("INSTR", 4, _instr),
                       ("LPAD", 2, _pad(True)), ("LPAD", 3, _pad(True)), ("RPAD", 2, _pad(False)), ("RPAD", 3, _pad(False)),
                       ("INITCAP", 1, lambda s: None if s is None else " ".join(w.capitalize() for w in s.split(" "))),
                       ("CONCAT", 2, lambda a, b: (a or "") + (b or "")), ("REPLACE", 2, lambda s, t: None if s is None else s.replace(t or "", "")),
                       ("ADD_MONTHS", 2, _add_months), ("LAST_DAY", 1, _last_day),
                       ("MONTHS_BETWEEN", 2, _months_between), ("NEXT_DAY", 2, _next_day)]:
        c.create_function(name, n, f, deterministic=True)
    c.execute("PRAGMA foreign_keys = ON")
    c.executescript(SCHEMA)
    for t in DBS[db]:
        cols, rows = TABLES[t]
        c.executemany(f"INSERT INTO {t} VALUES ({', '.join('?' * len(cols))})", rows)
    c.commit()
    return c


def _rows(db, q, script=None):
    c = connect(db)
    if script:
        c.executescript(_translate(script))
    return c.execute(_translate(q)).fetchall()


def _show(v):
    if v is None:
        return "NULL"
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def sql_val(db, q):
    """first column of the first row (a number)"""
    v = _rows(db, q)[0][0]
    if v is None:
        raise ValueError(f"{q!r} returned NULL")
    return v


def sql_count(db, q):
    """number of rows the query returns"""
    return len(_rows(db, q))


def sql_pick(db, q, options):
    """index of the option equal to the query's single value, shown as text (NULL for null)"""
    got = _show(_rows(db, q)[0][0])
    hits = [i for i, o in enumerate(options) if str(o) == got]
    if len(hits) != 1:
        raise ValueError(f"{q!r} gives {got!r}, options {options}")
    return hits[0]


def sql_list(db, q, options):
    """index of the option equal to the query's first column, joined with ', ' in row order"""
    got = ", ".join(_show(r[0]) for r in _rows(db, q))
    hits = [i for i, o in enumerate(options) if str(o) == got]
    if len(hits) != 1:
        raise ValueError(f"{q!r} gives {got!r}, options {options}")
    return hits[0]


def sql_match(db, queries, target):
    """index of the only query whose result (as a multiset of rows) equals the target query's"""
    want = sorted(map(repr, _rows(db, target)))
    hits = []
    for i, q in enumerate(queries):
        try:
            if sorted(map(repr, _rows(db, q))) == want:
                hits.append(i)
        except sqlite3.Error:
            pass
    if len(hits) != 1:
        raise ValueError(f"{len(hits)} queries match {target!r}")
    return hits[0]


def sql_after(db, script, q):
    """run the statements, then the query; first column of the first row"""
    v = _rows(db, q, script)[0][0]
    if v is None:
        raise ValueError(f"{q!r} returned NULL")
    return v


def sql_fails(db, stmts):
    """index of the only statement (each run on a fresh copy) that raises an error"""
    bad = []
    for i, s in enumerate(stmts):
        try:
            c = connect(db)
            c.executescript(_translate(s))
        except sqlite3.Error:
            bad.append(i)
    if len(bad) != 1:
        raise ValueError(f"statements failing: {bad}")
    return bad[0]


def check_tables(templates):
    """every table drawn on an SQL card (a scheme panel captioned with the table's name) must show
    the rows typed here; returns the mismatches as (template, table)"""
    bad = []
    for name, t in templates.items():
        fig = t.get("figure") or {}
        for panel in fig.get("panels", []) if fig.get("type") == "scheme" else []:
            tab = panel.get("caption")
            if panel.get("type") != "table" or tab not in TABLES:
                continue
            cols, rows = TABLES[tab]
            want = [[_show(v) for v in r] for r in rows]
            if [str(h) for h in panel.get("head", [])] != cols or [[_show(v) for v in r] for r in panel.get("rows", [])] != want:
                bad.append((name, tab))
    return bad


FUNCS = {"sql_val": sql_val, "sql_count": sql_count, "sql_pick": sql_pick, "sql_list": sql_list,
         "sql_match": sql_match, "sql_after": sql_after, "sql_fails": sql_fails}


def check(p, H):
    """the SQL cards are problems as data, checked by data.py with the functions above"""
    return None
