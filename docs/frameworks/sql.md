# SQL — curriculum framework (draft 1)

Generated from `drills/frameworks/sql.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**40 learning objectives** in 8 units (37 core): 40 drilled, 0 partly, 0 with no drills. Core: 37 / 37 drilled.

## Big ideas

- **SETS · A query describes a result, not a procedure.** Each clause transforms a set of rows in a fixed logical order (FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY), and that order explains what each clause can see.
- **null · NULL is unknown, not zero.** Arithmetic and comparisons with NULL give NULL or unknown; group functions skip it; NOT IN against a NULL returns nothing.
- **STATE · Changes are transactions on objects with rules.** DML is undone until COMMIT, DDL commits, and constraints, privileges and the dictionary govern what any statement may do.

## Practices

- **P1 · Predict.** Say what a statement returns or leaves behind, on tables you can see.
- **P2 · Choose.** Pick the clause, join, function or object that does what is asked.
- **P3 · Recall the rule.** State the Oracle rule that decides whether a statement runs.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Querying one table | core | — | 8 | 8 | 0 | 0 |
| 2 · Functions | core | — | 6 | 6 | 0 | 0 |
| 3 · Aggregation | core | — | 3 | 3 | 0 | 0 |
| 4 · Multiple tables | core | — | 8 | 8 | 0 | 0 |
| 5 · Changing data | core | — | 3 | 3 | 0 | 0 |
| 6 · Schema objects | core | — | 5 | 5 | 0 | 0 |
| 7 · Access, the dictionary and time | core | — | 4 | 4 | 0 | 0 |
| 8 · Analytic SQL (beyond the exam) | extension | — | 3 | 3 | 0 | 0 |

## Unit 1 · Querying one table

Big ideas: SETS, 

### 1.1 Relational concepts



- ● **SQ-1.1.A** (oracle-1z0-071:1) Classify a statement as DML, DDL, DCL or transaction control.
  - EK: TRUNCATE, RENAME and COMMENT are DDL; MERGE is DML.
  - P3 · drills: sq-statement-kind, sq-commit-kind
- ● **SQ-1.1.B** (oracle-1z0-071:1) Identify primary keys, foreign keys and self-references in a schema.
  - EK: A foreign key may be null and may point into its own table.
  - Needs: SQ-1.1.A
  - P2 · drills: sq-keys, sq-fk-behaviour

### 1.2 SELECT



- ● **SQ-1.2.A** (oracle-1z0-071:2) Evaluate an arithmetic expression in the select list, including one with NULL.
  - EK: Usual precedence; anything combined with NULL is NULL.
  - Needs: SQ-1.1.B
  - P1 · drills: sq-select-expr, sq-null-arith
- ● **SQ-1.2.B** (oracle-1z0-071:2) Count the rows DISTINCT returns over one or more columns.
  - EK: DISTINCT covers the whole select list; all NULLs are one value.
  - Needs: SQ-1.2.A
  - P1 · drills: sq-distinct-rows, sq-count-distinct
- ● **SQ-1.2.C** (oracle-1z0-071:2) Use aliases, concatenation and the q-quote correctly, including Oracle's treatment of empty strings.
  - EK: Aliases exist only from SELECT onward; '' is NULL; || ignores NULL.
  - Needs: SQ-1.2.B
  - P1 · P3 · drills: sq-alias-legal, sq-concat, sq-oracle-empty-string

### 1.3 Restricting and sorting



- ● **SQ-1.3.A** (oracle-1z0-071:3) Count the rows a WHERE clause keeps, with AND/OR precedence, BETWEEN, IN, LIKE and IS NULL.
  - EK: AND before OR; a comparison with NULL is never true.
  - Needs: SQ-1.2.C
  - P1 · drills: sq-where-count, sq-null-trap
- ● **SQ-1.3.B** (oracle-1z0-071:3) Predict the order of rows from ORDER BY, including where Oracle puts NULLs, and which rows FETCH and OFFSET keep.
  - EK: NULLs sort high: last ascending, first descending.
  - Needs: SQ-1.3.A
  - P1 · drills: sq-order-first, sq-fetch-rows
- ● **SQ-1.3.C** (oracle-1z0-071:3) Say how &, &&, DEFINE and VERIFY behave.
  - EK: && prompts once and defines the variable for the session.
  - Needs: SQ-1.3.B
  - P3 · drills: sq-substitution, sq-substitution-2

## Unit 2 · Functions

Big ideas: 

### 2.1 Single-row functions



- ● **SQ-2.1.A** (oracle-1z0-071:4) Evaluate character functions: SUBSTR, INSTR, LENGTH, LPAD, RPAD, TRIM, REPLACE, INITCAP.
  - EK: Positions count from 1; a negative SUBSTR start counts from the end.
  - Needs: SQ-1.3.C
  - P1 · drills: sq-char-number, sq-char-text
- ● **SQ-2.1.B** (oracle-1z0-071:4) Evaluate ROUND, TRUNC and MOD, including negative places and negative numbers.
  - EK: ROUND halves away from zero; MOD takes the dividend's sign.
  - Needs: SQ-2.1.A
  - P1 · drills: sq-number-fn, sq-round-trunc-2
- ● **SQ-2.1.C** (oracle-1z0-071:4) Do date arithmetic and evaluate MONTHS_BETWEEN, ADD_MONTHS, LAST_DAY and NEXT_DAY.
  - EK: DATE − DATE is days; month-ends stay month-ends.
  - Needs: SQ-2.1.B
  - P1 · drills: sq-date-number, sq-date-text

### 2.2 Conversion and conditional expressions



- ● **SQ-2.2.A** (oracle-1z0-071:5) Evaluate NVL, NVL2, NULLIF and COALESCE.
  - EK: COALESCE returns its first non-null argument.
  - Needs: SQ-2.1.C
  - P1 · drills: sq-null-fn, sq-null-fn-agg
- ● **SQ-2.2.B** (oracle-1z0-071:5) Evaluate CASE and DECODE.
  - EK: DECODE matches NULL to NULL; CASE with no ELSE gives NULL.
  - Needs: SQ-2.2.A
  - P1 · drills: sq-case-decode, sq-case-count
- ● **SQ-2.2.C** (oracle-1z0-071:5) Read TO_CHAR and TO_NUMBER format models and say when Oracle converts implicitly.
  - EK: Too-narrow models print #; strings compared with dates use NLS_DATE_FORMAT.
  - Needs: SQ-2.2.B
  - P1 · P3 · drills: sq-to-char, sq-implicit

## Unit 3 · Aggregation

Big ideas: SETS, 

### 3.1 Group functions, GROUP BY and HAVING



- ● **SQ-3.1.A** (oracle-1z0-071:6) Evaluate COUNT, SUM, AVG, MIN and MAX on a column with NULLs.
  - EK: COUNT(*) counts rows; everything else skips NULLs.
  - Needs: SQ-2.2.C
  - P1 · drills: sq-aggregate, sq-avg-nulls
- ● **SQ-3.1.B** (oracle-1z0-071:6) Count the groups a GROUP BY … HAVING query returns and evaluate a nested group function.
  - EK: WHERE filters rows before grouping, HAVING groups after.
  - Needs: SQ-3.1.A
  - P1 · drills: sq-group-rows, sq-group-nested
- ● **SQ-3.1.C** (oracle-1z0-071:6) Spot the grouping error in a query and state the logical order of the clauses.
  - EK: Ungrouped columns and group functions in WHERE are errors.
  - Needs: SQ-3.1.B
  - P3 · drills: sq-group-error, sq-clause-order

## Unit 4 · Multiple tables

Big ideas: SETS, 

### 4.1 Joins



- ● **SQ-4.1.A** (oracle-1z0-071:7) Count the rows of an inner, outer, cross, natural or USING join, and choose the join that keeps the rows asked for.
  - EK: Outer joins keep unmatched rows with NULLs; CROSS multiplies.
  - Needs: SQ-3.1.C
  - P1 · P2 · drills: sq-join-count, sq-join-pick
- ● **SQ-4.1.B** (oracle-1z0-071:7) Evaluate a self-join and a non-equijoin.
  - EK: Two aliases of one table; a range condition instead of =.
  - Needs: SQ-4.1.A
  - P1 · drills: sq-self-join, sq-nonequi
- ● **SQ-4.1.C** (oracle-1z0-071:7) Translate Oracle's (+) outer-join notation to ANSI syntax.
  - EK: (+) marks the side that may be missing.
  - Needs: SQ-4.1.B
  - P3 · drills: sq-oracle-plus, sq-plus-ansi

### 4.2 Subqueries



- ● **SQ-4.2.A** (oracle-1z0-071:8) Count the rows of a query with a single-row, multiple-row (IN, ANY, ALL), correlated or EXISTS subquery.
  - EK: > ALL is above the maximum; a correlated subquery reruns per row.
  - Needs: SQ-4.1.C
  - P1 · drills: sq-subquery-count, sq-scalar-sub
- ● **SQ-4.2.B** (oracle-1z0-071:8) Say whether a subquery comparison runs, returns nothing or fails.
  - EK: = with a multi-row subquery raises ORA-01427.
  - Needs: SQ-4.2.A
  - P3 · drills: sq-subquery-error, sq-subquery-rules
- ● **SQ-4.2.C** (oracle-1z0-071:8) Predict the result of a correlated UPDATE or DELETE.
  - EK: The subquery sees the table as the statement began.
  - Needs: SQ-4.2.B
  - P1 · drills: sq-correlated-dml, sq-correlated-after

### 4.3 Set operators



- ● **SQ-4.3.A** (oracle-1z0-071:9) Count the rows of UNION, UNION ALL, INTERSECT and MINUS.
  - EK: Only UNION ALL keeps duplicates.
  - Needs: SQ-4.2.C
  - P1 · drills: sq-set-count, sq-set-sum
- ● **SQ-4.3.B** (oracle-1z0-071:9) State the rules for compound queries: matching columns, names, ORDER BY and precedence.
  - EK: Names from the first query; ORDER BY once at the end; equal precedence.
  - Needs: SQ-4.3.A
  - P3 · drills: sq-set-rules, sq-set-rules-2

## Unit 5 · Changing data

Big ideas: STATE

### 5.1 DML



- ● **SQ-5.1.A** (oracle-1z0-071:10) Predict a table after INSERT, UPDATE or DELETE.
  - EK: No WHERE means every row; omitted columns get their default.
  - Needs: SQ-1.3.C
  - P1 · drills: sq-dml-after, sq-dml-after-2
- ● **SQ-5.1.B** (oracle-1z0-071:10) Predict the result of MERGE and of a multitable INSERT ALL or INSERT FIRST.
  - EK: INSERT FIRST stops at the first true WHEN.
  - Needs: SQ-5.1.A
  - P1 · drills: sq-merge, sq-multi-insert

### 5.2 Transactions



- ● **SQ-5.2.A** (oracle-1z0-071:10) Trace COMMIT, ROLLBACK, SAVEPOINT and implicit commits through a session.
  - EK: ROLLBACK TO keeps the transaction open; DDL commits.
  - Needs: SQ-5.1.B
  - P1 · drills: sq-transaction, sq-transaction-2

## Unit 6 · Schema objects

Big ideas: STATE

### 6.1 Indexes, synonyms and sequences



- ● **SQ-6.1.A** (oracle-1z0-071:11) Compute the values a sequence hands out, with and without CYCLE.
  - EK: First NEXTVAL is START WITH; CURRVAL repeats the session's last.
  - Needs: SQ-5.2.A
  - P1 · drills: sq-sequence, sq-sequence-cycle
- ● **SQ-6.1.B** (oracle-1z0-071:11) Say whether an index can serve a condition, and how indexes and synonyms relate to their tables.
  - EK: Functions and leading wildcards defeat a plain index; synonyms grant nothing.
  - Needs: SQ-6.1.A
  - P3 · drills: sq-index-use, sq-objects

### 6.2 Tables and constraints



- ● **SQ-6.2.A** (oracle-1z0-071:12) Find the INSERT that violates a PRIMARY KEY, UNIQUE, CHECK or FOREIGN KEY constraint, and name constraint types by their dictionary code.
  - EK: UNIQUE allows many NULLs; a CHECK passes on NULL.
  - Needs: SQ-6.1.B
  - P1 · P3 · drills: sq-constraint-fail, sq-constraint-type
- ● **SQ-6.2.B** (oracle-1z0-071:12) Choose between DELETE, TRUNCATE and DROP, and state the rules for data types, temporary and external tables and unused columns.
  - EK: TRUNCATE is DDL; NUMBER(p,s) rounds extra decimals.
  - Needs: SQ-6.2.A
  - P2 · P3 · drills: sq-ddl-facts, sq-datatypes, sq-temp-external

### 6.3 Views



- ● **SQ-6.3.A** (oracle-1z0-071:13) Say whether DML works through a view and what OR REPLACE, FORCE and dropping do.
  - EK: GROUP BY, DISTINCT and READ ONLY block DML; CHECK OPTION keeps rows visible.
  - Needs: SQ-6.2.B
  - P3 · drills: sq-view-dml, sq-view-facts

## Unit 7 · Access, the dictionary and time

Big ideas: STATE

### 7.1 User access



- ● **SQ-7.1.A** (oracle-1z0-071:14) Classify privileges as system or object and predict what REVOKE takes from others.
  - EK: Object grants cascade on revoke; ADMIN OPTION grants do not.
  - Needs: SQ-6.3.A
  - P3 · drills: sq-privilege-kind, sq-revoke-cascade, sq-grant-facts

### 7.2 Data dictionary



- ● **SQ-7.2.A** (oracle-1z0-071:15) Name the dictionary view that answers a question and the scope of its prefix.
  - EK: USER_ ⊂ ALL_ ⊂ DBA_.
  - Needs: SQ-7.1.A
  - P3 · drills: sq-dictionary, sq-dictionary-prefix

### 7.3 Time zones and intervals



- ● **SQ-7.3.A** (oracle-1z0-071:16) Say what CURRENT_DATE, CURRENT_TIMESTAMP, LOCALTIMESTAMP, SYSDATE and the TIMESTAMP types hold.
  - EK: CURRENT_ follow the session; SYS follow the server.
  - Needs: SQ-7.2.A
  - P3 · drills: sq-timezone-fn, sq-tz-types
- ● **SQ-7.3.B** (oracle-1z0-071:16) Convert and add INTERVAL YEAR TO MONTH and DAY TO SECOND values.
  - EK: Adding a month interval to the 31st can fail.
  - Needs: SQ-7.3.A
  - P1 · drills: sq-interval-ym, sq-interval-ds, sq-interval-add

## Unit 8 · Analytic SQL (beyond the exam) (extension)

Big ideas: SETS

### 8.1 Window functions and reporting



- ● **SQ-8.1.A** Evaluate ROW_NUMBER, RANK, DENSE_RANK, LAG and running or partitioned aggregates.
  - EK: PARTITION BY restarts; RANK leaves gaps after ties.
  - Needs: SQ-3.1.A, SQ-3.1.C, SQ-4.3.B
  - P1 · drills: sq-window, sq-window-2
- ● **SQ-8.1.B** Predict the rows of a top-n-per-group or paging query built on a window function.
  - EK: Number in an inline view, filter outside it.
  - Needs: SQ-8.1.A
  - P1 · drills: sq-top-per-group, sq-top-n-2
- ● **SQ-8.1.C** Evaluate an aggregation over a star schema: fact joined to dimensions, filtered and grouped.
  - EK: Compute the measure per fact row, then sum.
  - Needs: SQ-8.1.B
  - P1 · drills: sq-star-agg, sq-star-2
