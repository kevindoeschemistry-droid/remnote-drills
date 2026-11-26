"""SQL (SQ) second types (Nov 2026): one more question for every objective that had one. Query answers are computed here
by running the query once through tests/verify/sql.py (SQLite with Oracle's functions) and checked again by the
verifier; tables on the cards are the existing `scheme` figures, copied from the templates that already draw them.
Concept picks are authored, on Oracle 1Z0-071 behaviour."""
import importlib.util, os
import yaml
from opl_dsl import Q

FILE, FRAMEWORK = "sq-second-types", "sql"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_spec = importlib.util.spec_from_file_location("sqlv", os.path.join(ROOT, "tests/verify/sql.py"))
SQ = importlib.util.module_from_spec(_spec)
import sys  # noqa: E402
_saved = sys.path[:]
sys.path[:] = [p for p in sys.path if "second_specs" not in p]  # second_specs/re.py would shadow the stdlib re
if getattr(sys.modules.get("re"), "__file__", "").find("second_specs") >= 0: del sys.modules["re"]
import re as _stdre  # noqa: E402,F401
_spec.loader.exec_module(SQ)
sys.path[:] = _saved
FIG = {}
for f in ("sq-query.yaml", "sq-manage.yaml"):
    for t in yaml.safe_load(open(os.path.join(ROOT, "drills/problems", f))):
        if t.get("figure"): FIG.setdefault(tuple(p.get("caption") for p in t["figure"]["panels"]), t["figure"])
EMP, EMPD, SETS, STAR = FIG[("emp",)], FIG[("emp", "depts")], FIG[("a", "b")], FIG[("sales", "products", "stores")]
SEL, FUN, AGG, JOI, SUB, DML, DDL, ADM, ANA = ("sql.select", "sql.functions", "sql.aggregate", "sql.joins", "sql.subqueries", "sql.dml",
                                               "sql.ddl", "sql.admin", "sql.analytic")


def facts(name, skill, rows, explain, pace="quick"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def VAL(name, skill, db, qs, explain, figure, prompt="What does this return? {{q}}"):
    """one number per query, run here and again by the verifier"""
    cases = [{"q": q, "ans": float(SQ.sql_val(db, q))} for q in qs]
    return Q(name, skill, prompt, cases=cases, value="ans", tex="v", verify=f"sql_val('{db}', q)", explain=explain, figure=figure)


def CNT(name, skill, db, qs, explain, figure, prompt="How many rows does this return? {{q}}"):
    cases = [{"q": q, "ans": SQ.sql_count(db, q)} for q in qs]
    return Q(name, skill, prompt, cases=cases, value="ans", tex="n", final=True, verify=f"sql_count('{db}', q)", explain=explain, figure=figure)


def AFTER(name, skill, db, rows, explain, figure, prompt="After {{s}}, what does {{q}} return?"):
    cases = [{"s": s, "q": q, "ans": float(SQ.sql_after(db, s, q))} for s, q in rows]
    return Q(name, skill, prompt, cases=cases, value="ans", tex="v", verify=f"sql_after('{db}', s, q)", explain=explain, figure=figure)


ADD = [
    ("SQ-1.1.A", facts("sq-commit-kind", ADM, [
        ("Which statement commits the current transaction implicitly in Oracle?", "CREATE TABLE t (x NUMBER)", "UPDATE emp SET salary = 0", "SELECT * FROM emp", "SAVEPOINT s1"),
        ("TRUNCATE TABLE emp is:", "DDL: it commits and can't be rolled back", "DML: it can be rolled back", "DCL", "A query"),
        ("GRANT SELECT ON emp TO ben is:", "DCL", "DML", "DDL", "Transaction control"),
        ("MERGE INTO emp … is:", "DML", "DDL", "DCL", "Transaction control"),
        ("ROLLBACK TO SAVEPOINT s1 is:", "Transaction control", "DDL", "DCL", "DML"),
    ], "DDL and DCL commit implicitly; DML waits for COMMIT or ROLLBACK")),
    ("SQ-1.1.B", facts("sq-fk-behaviour", DDL, [
        ("A foreign key without ON DELETE options: deleting a parent row that has children:", "Fails with an integrity error", "Deletes the children", "Sets children to NULL", "Is ignored"),
        ("With ON DELETE CASCADE, deleting a parent row:", "Deletes its child rows too", "Fails", "Nulls the parent key", "Does nothing to children"),
        ("With ON DELETE SET NULL, deleting a parent row:", "Sets the children's foreign key to NULL", "Deletes the children", "Fails", "Copies the parent"),
        ("A foreign key column may hold NULL:", "Yes, unless it is also NOT NULL", "Never", "Only in the parent", "Only with CASCADE"),
        ("emp.mgr referencing emp.id is:", "A self-referencing foreign key", "A primary key", "A unique key only", "A check constraint"),
    ], "Referential actions decide what happens to children")),
    ("SQ-1.2.B", VAL("sq-count-distinct", SEL, "emp", [
        "SELECT COUNT(DISTINCT dept) FROM emp", "SELECT COUNT(dept) FROM emp", "SELECT COUNT(DISTINCT mgr) FROM emp",
        "SELECT COUNT(mgr) FROM emp", "SELECT COUNT(DISTINCT hired) FROM emp"],
        "COUNT(col) counts non-NULL values; COUNT(DISTINCT col) counts different non-NULL values", EMP)),
    ("SQ-1.3.C", facts("sq-substitution-2", SEL, [
        ("A script uses &dept twice. In SQL*Plus without DEFINE, you are prompted:", "Twice", "Once", "Never", "Three times"),
        ("&&dept the first time:", "Prompts once and defines the variable for later uses", "Never prompts", "Prompts every time", "Is an error"),
        ("SET VERIFY ON shows:", "The old and new lines after substitution", "Nothing", "The execution plan", "Only errors"),
        ("UNDEFINE dept:", "Removes the variable so the next & prompts again", "Deletes the column", "Drops the table", "Hides output"),
        ("For a text value, the substitution is usually written:", "'&name' (inside quotes)", "&name without quotes always", "\"&name\"", "&'name'"),
    ], "& prompts each time; && defines; DEFINE and UNDEFINE manage variables")),
    ("SQ-2.1.B", VAL("sq-round-trunc-2", FUN, "emp", [
        "SELECT ROUND(1234.567, -2) FROM DUAL", "SELECT TRUNC(1234.567, -2) FROM DUAL", "SELECT ROUND(-2.5) FROM DUAL",
        "SELECT MOD(-7, 3) FROM DUAL", "SELECT TRUNC(-7.9) FROM DUAL", "SELECT ROUND(15.749, 1) FROM DUAL"],
        "ROUND rounds half away from zero; TRUNC cuts toward zero; a negative place works left of the point; MOD keeps the sign of the dividend", None)),
    ("SQ-2.2.A", VAL("sq-null-fn-agg", FUN, "emp", [
        "SELECT SUM(NVL(salary, 0)) FROM emp", "SELECT COUNT(NVL(salary, 0)) FROM emp", "SELECT SUM(NVL2(mgr, 1, 0)) FROM emp",
        "SELECT SUM(COALESCE(mgr, id)) FROM emp", "SELECT COUNT(NULLIF(dept, 'IT')) FROM emp"],
        "NVL replaces NULL; NVL2 picks by NULL-ness; COALESCE takes the first non-NULL; NULLIF makes a value NULL", EMP)),
    ("SQ-2.2.B", VAL("sq-case-count", FUN, "emp", [
        "SELECT SUM(CASE WHEN salary >= 5000 THEN 1 ELSE 0 END) FROM emp", "SELECT COUNT(CASE WHEN salary >= 5000 THEN 1 END) FROM emp",
        "SELECT SUM(CASE dept WHEN 'IT' THEN 2 WHEN 'Sales' THEN 1 ELSE 0 END) FROM emp",
        "SELECT SUM(DECODE(dept, 'HR', 10, 1)) FROM emp", "SELECT COUNT(CASE WHEN salary < 5000 THEN 1 ELSE NULL END) FROM emp"],
        "A NULL salary fails every WHEN, falling to ELSE (or NULL); COUNT skips the NULLs", EMP)),
    ("SQ-3.1.A", VAL("sq-avg-nulls", AGG, "emp", [
        "SELECT AVG(salary) FROM emp", "SELECT AVG(NVL(salary, 0)) FROM emp", "SELECT SUM(salary) / COUNT(*) FROM emp",
        "SELECT MAX(salary) - MIN(salary) FROM emp", "SELECT COUNT(*) - COUNT(salary) FROM emp"],
        "Aggregates skip NULLs: AVG divides by the count of non-NULL values, unlike SUM/COUNT(*)", EMP)),
    ("SQ-4.1.C", facts("sq-plus-ansi", JOI, [
        ("WHERE e.dept = d.dept(+) is equivalent to:", "emp e LEFT OUTER JOIN depts d ON e.dept = d.dept", "RIGHT OUTER JOIN", "FULL OUTER JOIN", "An inner join"),
        ("WHERE e.dept(+) = d.dept is equivalent to:", "emp e RIGHT OUTER JOIN depts d ON e.dept = d.dept", "LEFT OUTER JOIN", "FULL OUTER JOIN", "CROSS JOIN"),
        ("Can the (+) operator express a full outer join?", "No: it can be on one side only", "Yes", "Only with DISTINCT", "Only in views"),
        ("The (+) goes on the side of the table that:", "May have no matching row (the deficient side)", "Must match", "Has the primary key", "Is listed first"),
    ], "(+) marks the side that may be missing")),
    ("SQ-4.2.A", VAL("sq-scalar-sub", SUB, "emp", [
        "SELECT MAX(salary) FROM emp WHERE salary < (SELECT MAX(salary) FROM emp)",
        "SELECT COUNT(*) FROM emp WHERE salary > (SELECT AVG(salary) FROM emp)",
        "SELECT COUNT(*) FROM emp WHERE dept IN (SELECT dept FROM depts WHERE city = 'Austin')",
        "SELECT COUNT(*) FROM depts d WHERE NOT EXISTS (SELECT 1 FROM emp e WHERE e.dept = d.dept)",
        "SELECT COUNT(*) FROM emp e WHERE salary > (SELECT AVG(salary) FROM emp WHERE dept = e.dept)"],
        "Evaluate the inner query first (or per outer row, if correlated), then the outer filter", EMPD)),
    ("SQ-4.2.B", facts("sq-subquery-rules", SUB, [
        ("WHERE salary = (SELECT salary FROM emp WHERE dept = 'IT') fails because:", "A single-row operator meets a subquery returning several rows", "IT has no rows", "= is not allowed", "It doesn't fail"),
        ("WHERE x NOT IN (SELECT mgr FROM emp), where mgr has NULLs, returns:", "No rows", "Every row", "Rows with NULL x", "An error"),
        ("A single-row subquery that returns no row makes the comparison:", "NULL, so no rows match", "An error", "True", "Zero"),
        ("> ALL (subquery) means greater than:", "The largest value returned", "The smallest", "Any one value", "The average"),
        ("> ANY (subquery) means greater than:", "The smallest value returned", "The largest", "All values", "The sum"),
    ], "Match the operator to how many rows the subquery returns, and watch NULLs")),
    ("SQ-4.2.C", AFTER("sq-correlated-after", DML, "emp", [
        ("UPDATE emp e SET salary = (SELECT MAX(salary) FROM emp WHERE dept = e.dept) WHERE salary IS NOT NULL", "SELECT SUM(salary) FROM emp"),
        ("DELETE FROM emp e WHERE salary < (SELECT AVG(salary) FROM emp WHERE dept = e.dept)", "SELECT COUNT(*) FROM emp"),
        ("UPDATE emp e SET salary = salary + 100 WHERE EXISTS (SELECT 1 FROM depts d WHERE d.dept = e.dept AND d.city = 'Boston')", "SELECT SUM(salary) FROM emp")],
        "The subquery runs once per row being changed, seeing the table as it was when the statement began", EMPD)),
    ("SQ-4.3.A", VAL("sq-set-sum", SUB, "sets", [
        "SELECT SUM(n) FROM (SELECT n FROM a UNION SELECT n FROM b)", "SELECT SUM(n) FROM (SELECT n FROM a UNION ALL SELECT n FROM b)",
        "SELECT SUM(n) FROM (SELECT n FROM a INTERSECT SELECT n FROM b)", "SELECT SUM(n) FROM (SELECT n FROM a MINUS SELECT n FROM b)"],
        "UNION and INTERSECT and MINUS remove duplicates; UNION ALL keeps them, so its sum counts the repeated 2", SETS)),
    ("SQ-4.3.B", facts("sq-set-rules-2", SUB, [
        ("In a compound query the column names of the result come from:", "The first SELECT", "The last SELECT", "Whichever has more rows", "They must be aliased"),
        ("ORDER BY in a compound query may appear:", "Only once, at the very end", "In every SELECT", "Only in the first SELECT", "Never"),
        ("SELECT n FROM a UNION SELECT name FROM emp fails because:", "Corresponding columns must have compatible types", "Names differ", "UNION needs ORDER BY", "It doesn't fail"),
        ("Oracle evaluates UNION, INTERSECT and MINUS:", "Left to right with equal precedence (use parentheses)", "INTERSECT first", "MINUS first", "Randomly"),
    ], "Same number and types of columns; names from the first query; one ORDER BY at the end")),
    ("SQ-5.1.A", AFTER("sq-dml-after-2", DML, "emp", [
        ("UPDATE emp SET salary = salary * 1.1 WHERE dept = 'Sales'", "SELECT SUM(salary) FROM emp"),
        ("DELETE FROM emp WHERE salary IS NULL", "SELECT COUNT(*) FROM emp"),
        ("INSERT INTO emp (id, name, dept) VALUES (7, 'Gus', 'Ops')", "SELECT COUNT(salary) FROM emp"),
        ("UPDATE emp SET mgr = 1 WHERE mgr IS NULL AND id <> 1", "SELECT COUNT(*) FROM emp WHERE mgr = 1")],
        "Apply the statement to the matching rows only; columns you don't insert are NULL", EMP)),
    ("SQ-5.2.A", facts("sq-transaction-2", DML, [
        ("A session inserts a row, then runs CREATE INDEX. The insert is:", "Committed by the DDL's implicit commit", "Rolled back", "Pending", "Lost"),
        ("Before COMMIT, another session querying the table sees:", "The data as of the last commit", "The uncommitted changes", "Nothing", "An error"),
        ("ROLLBACK TO SAVEPOINT s1:", "Undoes changes made after s1 and keeps the transaction open", "Ends the transaction", "Undoes everything", "Commits up to s1"),
        ("A session ends normally (EXIT in SQL*Plus) with pending DML. Usually:", "It is committed", "It is rolled back", "It is lost", "It waits"),
        ("A statement fails partway inside a transaction. Oracle:", "Rolls back that statement only", "Rolls back the whole transaction", "Commits", "Crashes"),
    ], "Transactions end at COMMIT, ROLLBACK or DDL")),
    ("SQ-8.1.A", VAL("sq-window-2", ANA, "emp", [
        "SELECT MAX(r) FROM (SELECT DENSE_RANK() OVER (ORDER BY dept) r FROM emp)",
        "SELECT MAX(r) FROM (SELECT RANK() OVER (ORDER BY dept) r FROM emp)",
        "SELECT SUM(c) FROM (SELECT COUNT(*) OVER (PARTITION BY dept) c FROM emp)",
        "SELECT MAX(t) FROM (SELECT SUM(salary) OVER (PARTITION BY dept) t FROM emp)",
        "SELECT MIN(rn) FROM (SELECT ROW_NUMBER() OVER (PARTITION BY dept ORDER BY id) rn FROM emp)"],
        "RANK leaves gaps after ties, DENSE_RANK doesn't; a partitioned COUNT repeats the group size on every row", EMP)),
    ("SQ-8.1.B", CNT("sq-top-n-2", ANA, "emp", [
        "SELECT * FROM (SELECT e.*, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY id) rn FROM emp e) WHERE rn <= 2",
        "SELECT * FROM (SELECT e.*, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY id) rn FROM emp e) WHERE rn = 1",
        "SELECT * FROM (SELECT e.*, DENSE_RANK() OVER (ORDER BY dept) dr FROM emp e) WHERE dr = 2",
        "SELECT * FROM emp ORDER BY id FETCH FIRST 3 ROWS ONLY"],
        "Number the rows within each group, then filter on the number in an outer query", EMP)),
    ("SQ-8.1.C", VAL("sq-star-2", ANA, "star", [
        "SELECT SUM(s.units * p.price) FROM sales s JOIN products p ON s.product = p.product",
        "SELECT SUM(s.units) FROM sales s JOIN stores t ON s.store = t.store WHERE t.region = 'East'",
        "SELECT SUM(s.units) FROM sales s JOIN products p ON s.product = p.product WHERE p.category = 'Cake'",
        "SELECT COUNT(DISTINCT s.day) FROM sales s JOIN stores t ON s.store = t.store WHERE t.region = 'West'"],
        "Join the fact table to the dimensions you filter or label by, then aggregate the measure", STAR)),
]
