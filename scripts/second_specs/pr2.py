"""Programming Foundations (PR) depth (Nov 2026): two question types for every objective. Code cards are run here once
to fill the right option (tests/verify/progcode.py runs them again in the verifier), so the hand-written part of
each card is its distractors; concept picks are authored. NumPy cards need numpy (installed in CI)."""
import os, sys
from opl_dsl import Q

import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("progcode", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "tests/verify/progcode.py"))
PC = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(PC)
import shelve  # noqa: E402
PC._CACHE = shelve.open("/tmp/pr2-run-cache")  # spec-time only: snippets rerun quickly while editing

FILE, FRAMEWORK = "pr-depth", "programming"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
JB, JO, JC, JL, JA, PY, SHL, GIT = ("prog.java-basics", "prog.java-objects", "prog.java-control", "prog.java-collections",
                                   "prog.java-algorithms", "prog.python", "prog.shell", "prog.git")
CODE = {"type": "code", "src": "code"}
SHOW = {"type": "code", "src": "show"}
CMDS = {"type": "code", "src": "cmds"}


def facts(name, skill, rows, explain, pace="quick"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def _opts(got, wrong, name):
    assert got not in wrong and len(set(wrong)) == 3, (name, got, wrong)
    return {"o1": got, "o2": wrong[0], "o3": wrong[1], "o4": wrong[2]}


def J(name, skill, rows, explain, defs="", prompt="What does this print?"):
    cases = []
    for code, wrong in rows:
        c = {"code": code, **_opts(PC._show(PC.java_run(code, defs)), wrong, name)}
        if defs: c.update({"defs": defs, "show": defs + "\n\n" + code})
        cases.append(c)
    fn = "java_pick(code, [o1, o2, o3, o4], defs)" if defs else "java_pick(code, [o1, o2, o3, o4])"
    return Q(name, skill, prompt, cases=cases, choice=MC, correct="0", verify=fn, explain=explain, figure=SHOW if defs else CODE)


def JN(name, skill, codes, explain, defs="", prompt="What does this print?"):
    cases = []
    for code in codes:
        c = {"code": code, "ans": float(PC.java_out(code, defs))}
        if defs: c.update({"defs": defs, "show": defs + "\n\n" + code})
        cases.append(c)
    fn = "java_out(code, defs)" if defs else "java_out(code)"
    return Q(name, skill, prompt, cases=cases, value="ans", tex="v", final=True, verify=fn, explain=explain, figure=SHOW if defs else CODE)


def P(name, skill, rows, explain, prompt="What does this print?"):
    cases = [{"code": code, **_opts(PC._show(PC.py_run(code)), wrong, name)} for code, wrong in rows]
    return Q(name, skill, prompt, cases=cases, choice=MC, correct="0", verify="py_pick(code, [o1, o2, o3, o4])", explain=explain, figure=CODE)


def PN(name, skill, codes, explain, prompt="What does this print?", final=True):
    cases = [{"code": code, "ans": float(PC.py_out(code))} for code in codes]
    return Q(name, skill, prompt, cases=cases, value="ans", tex="v", final=final, verify="py_out(code)", explain=explain, figure=CODE)


def SH(name, skill, prompt, rows, explain):
    cases = [{"setup": su, "cmds": cm, **_opts(PC._show(PC.sh_run(su, cm)), wrong, name)} for su, cm, wrong in rows]
    return Q(name, skill, prompt, cases=cases, choice=MC, correct="0", verify="sh_pick(setup, cmds, [o1, o2, o3, o4])", explain=explain, figure=CMDS)


def SHN(name, skill, prompt, rows, explain):
    cases = [{"setup": su, "cmds": cm, "ans": float(PC.sh_out(su, cm))} for su, cm in rows]
    return Q(name, skill, prompt, cases=cases, value="ans", tex="v", final=True, verify="sh_out(setup, cmds)", explain=explain, figure=CMDS)


GIT1 = "git init -q .; echo a > a.txt; git add a.txt; git commit -qm one"
NP = "import numpy as np\n"

ADD = [
    # ── 1 objects and methods ─────────────────────────────────────────────────────────────────────────────────────
    ("PR-1.1.A", PN("pr-collatz-steps", JB, [f"n = {n}\nsteps = 0\nwhile n != 1:\n    n = n // 2 if n % 2 == 0 else 3 * n + 1\n    steps += 1\nprint(steps)" for n in (6, 7, 12, 19, 27)],
        "Follow the steps exactly, one at a time, keeping a table of n and steps", prompt="Trace this procedure. What does it print?")),
    ("PR-1.1.A", facts("pr-algorithm-steps", JB, [
        ("'Add salt to taste' is a poor algorithm step because it is:", "Ambiguous: it doesn't say how much or when to stop", "Too short", "Out of order", "Too precise"),
        ("An algorithm must finish. A step 'repeat until the dough is ready' needs:", "A testable stopping condition", "More salt", "A loop counter only", "Nothing"),
        ("Which is the sequencing, selection and iteration of 'for each test, if score ≥ 90 add 1 to count'?", "Iteration contains a selection; the add is a sequence step", "Only selection", "Only sequencing", "Recursion"),
        ("Two cooks following the same written recipe get different dishes. The recipe is not:", "Unambiguous", "Long enough", "Iterative", "Recursive"),
    ], "Each step must be exact, ordered and finite")),
    ("PR-1.1.B", facts("pr-compile-run", JB, [
        ("The order of steps for a Java program:", "Write source → compile (javac) → run bytecode on the JVM (java)", "Compile → write → run", "Run → compile → write", "Write → run → compile"),
        ("A missing semicolon is caught:", "By the compiler", "At run time", "By the operating system", "Never"),
        ("Dividing an int by zero is caught:", "At run time (ArithmeticException)", "By the compiler", "By the editor", "Never"),
        ("javac Hello.java produces:", "Hello.class (bytecode)", "Hello.exe", "Hello.py", "Nothing"),
        ("A wrong formula that gives wrong answers is caught by:", "Testing with known answers", "The compiler", "The JVM", "Nothing ever"),
    ], "The compiler catches syntax and types; the JVM catches run-time faults; tests catch logic")),
    ("PR-1.1.B", facts("pr-compile-run-2", JB, [
        ("Why can the same .class file run on Windows and Linux?", "The JVM interprets or compiles the bytecode for each machine", "Java is a scripting language", "It can't", "Bytecode is machine code"),
        ("An IDE's red underline while typing usually shows:", "A compile-time error found by checking as you type", "A run-time crash", "A logic error", "A warning about style only"),
        ("Python, unlike Java, usually reports a misspelled variable name:", "Only when that line runs", "At compile time", "Never", "In the editor only"),
    ], "When each error shows up depends on the toolchain")),
    ("PR-1.1.C", facts("pr-error-kind-code", JB, [
        ("int x = 5 / 0; compiles and then:", "Throws ArithmeticException at run time", "Fails to compile", "Prints Infinity", "Prints 0"),
        ("String s = 5; is:", "A compile-time (type) error", "A run-time error", "A logic error", "Fine"),
        ("double avg = (a + b) / 2; with ints a = 3, b = 4 gives 3.0. This is:", "A logic error (integer division)", "A syntax error", "A run-time error", "Fine"),
        ("int[] a = new int[3]; a[3] = 1; is:", "A run-time error (ArrayIndexOutOfBoundsException)", "A compile error", "A logic error only", "Fine"),
        ("System.out.println(\"hi\") with the closing ; missing is:", "A syntax error", "A run-time error", "A logic error", "Fine"),
    ], "Compile-time: syntax and types; run-time: exceptions; logic: wrong results")),
    ("PR-1.1.D", facts("pr-test-inputs", JB, [
        ("A method returns the larger of two ints. A good boundary test is:", "Two equal values", "Two different positive values only", "No test", "Random values only"),
        ("A method computes a discount for orders of 100 dollars or more. Boundary tests are:", "99.99, 100 and 100.01", "50 and 500", "0 only", "Any value"),
        ("A method averages an array. An edge case to test is:", "An empty array", "An array of 5 numbers", "A sorted array", "An array of positives"),
        ("Before running a test you should write down:", "The expected output", "The run time", "The line count", "Nothing"),
        ("isEven(n) should be tested with:", "A negative odd, 0, and positive even and odd values", "Only 2", "Only 1", "Only large numbers"),
    ], "Test the edges and state the expected result first")),
    ("PR-1.1.D", PN("pr-test-expected", JB, [
        "def grade(s):\n    if s >= 90: return 4\n    if s >= 80: return 3\n    return 0\nprint(grade(90) + grade(89) + grade(80))",
        "def clamp(v, lo, hi):\n    return max(lo, min(v, hi))\nprint(clamp(-5, 0, 10) + clamp(15, 0, 10) + clamp(10, 0, 10))",
        "def fee(age):\n    return 0 if age < 5 or age >= 65 else 10\nprint(fee(4) + fee(5) + fee(64) + fee(65))"],
        "Run each boundary input through the rule by hand; the sum checks every one", prompt="These boundary tests are run together. What does it print?")),
    ("PR-1.2.A", P("pr-to-binary", JB, [(f"print(bin({n})[2:])", w) for n, w in [(45, ["101011", "110101", "10110"]), (100, ["1100010", "1010010", "110100"]),
        (13, ["1011", "1110", "1001"]), (64, ["100000", "1111111", "10000000"]), (255, ["11111110", "111111111", "10000000"])]],
        "Divide by 2 repeatedly and read the remainders bottom to top, or subtract the largest powers of 2",
        prompt="What is the decimal number in the code written in binary? (The code prints it.)")),
    ("PR-1.2.B", Q("pr-max-unsigned", JB, "What is the largest unsigned value that {{n}} bits can hold?", given={"n": {"pick": [4, 8, 10, 16]}},
        value="2^n - 1", tex="v", final=True, verify="summation(2**Symbol('j'), (Symbol('j'), 0, n - 1))",
        explain="n bits make 2ⁿ patterns, 0 to 2ⁿ − 1; signed two's complement shifts the range to −2ⁿ⁻¹ … 2ⁿ⁻¹ − 1")),
    ("PR-1.3.A", facts("pr-type-choice", JB, [
        ("The number of students in a class:", "int", "double", "boolean", "String"),
        ("A bank balance with cents, for a quick estimate:", "double (BigDecimal for real money)", "int", "boolean", "char"),
        ("Whether a light is on:", "boolean", "int", "String", "double"),
        ("A student's name:", "String (a reference type)", "char", "int", "boolean"),
        ("The average of test scores:", "double", "int", "boolean", "String"),
    ], "Pick the type whose values match the quantity")),
    ("PR-1.3.A", facts("pr-primitive-reference", JB, [
        ("int differs from String in that int is:", "A primitive holding the value itself", "A reference to an object", "Always null", "Mutable"),
        ("A String variable that has not been given an object holds:", "null (as a field)", "0", "\"\"", "false"),
        ("Which can call methods with a dot, like x.length()?", "A reference type such as String", "int", "double", "boolean"),
    ], "Primitives hold values; references point to objects")),
    ("PR-1.3.B", J("pr-declare-init", JB, [
        ("double d = 7 / 2;\nSystem.out.print(d);", ["3.5", "3", "4.0"]),
        ("int n = (int) 9.99;\nSystem.out.print(n);", ["10", "9.99", "9.0"]),
        ("boolean b = 3 > 2;\nSystem.out.print(b);", ["1", "3 > 2", "false"]),
        ("double d = 1 + 1 / 2;\nSystem.out.print(d);", ["1.5", "1", "2.0"])],
        "The right side is evaluated first, with its own types; only then is it stored (and widened) into the variable")),
    ("PR-1.3.B", facts("pr-declare-legal", JB, [
        ("Which compiles?", "double x = 5;", "int x = 5.0;", "boolean b = 1;", "int x = \"5\";"),
        ("Which compiles?", "int count = 0;", "int count = 0.5;", "boolean b = \"true\";", "double d = true;"),
        ("Which declares a constant?", "final double TAX = 0.08;", "const double TAX = 0.08;", "double TAX == 0.08;", "static TAX = 0.08;"),
        ("Using a local variable before assigning it:", "Fails to compile", "Gives 0", "Gives null", "Throws at run time"),
    ], "Widening is automatic; narrowing needs a cast")),
    ("PR-1.3.C", J("pr-int-average", JB, [
        ("int a = 3, b = 4;\nSystem.out.print((a + b) / 2);", ["3.5", "4", "3.0"]),
        ("int a = 3, b = 4;\nSystem.out.print((a + b) / 2.0);", ["3", "3.0", "4"]),
        ("int a = 3, b = 4;\nSystem.out.print((double) (a + b) / 2);", ["3.0", "3", "4.0"]),
        ("int a = 3, b = 4;\nSystem.out.print((double) ((a + b) / 2));", ["3.5", "3", "4.0"])],
        "If both operands are int, / truncates; one double operand makes the whole division double. Where the cast sits matters")),
    ("PR-1.3.D", J("pr-println-lines", JB, [
        ("System.out.print(\"a\");\nSystem.out.println(\"b\");\nSystem.out.print(\"c\");", ["a / b / c", "abc", "a / bc"]),
        ("System.out.println(\"a\");\nSystem.out.print(\"b\");\nSystem.out.print(\"c\");", ["ab / c", "abc", "a / b / c"]),
        ("System.out.println(1 + 2);\nSystem.out.println(\"1\" + 2);", ["3 / 3", "12 / 12", "3 / 3.0"]),
        ("System.out.print(\"x\\ty\");", ["x\\ty", "xy", "x\\ny"])],
        "println ends the line after printing; print does not. Lines on the card are joined by ' / '")),
    ("PR-1.4.A", J("pr-swap-trace", JB, [
        ("int a = 1, b = 2;\na = b;\nb = a;\nSystem.out.print(a + \" \" + b);", ["2 1", "1 2", "1 1"]),
        ("int a = 1, b = 2;\nint t = a;\na = b;\nb = t;\nSystem.out.print(a + \" \" + b);", ["1 2", "2 2", "1 1"]),
        ("int a = 5, b = 3;\na = a + b;\nb = a - b;\na = a - b;\nSystem.out.print(a + \" \" + b);", ["5 3", "8 5", "8 3"])],
        "Each assignment overwrites: a swap without a temporary loses the first value")),
    ("PR-1.4.B", JN("pr-incr-prefix", JB, [
        "int x = 5;\nint y = x++ + 2;\nSystem.out.print(y * 10 + x);",
        "int x = 5;\nint y = ++x + 2;\nSystem.out.print(y * 10 + x);",
        "int x = 10;\nx -= 3;\nx *= 2;\nSystem.out.print(x);",
        "int x = 7;\nx %= 4;\nx += x++;\nSystem.out.print(x);",
        "int x = 3;\nint y = x-- - --x;\nSystem.out.print(y * 10 + x);"],
        "x++ uses the old value then adds one; ++x adds first. Compound operators apply the operation and store")),
    ("PR-1.5.A", JN("pr-round-cast", JB, [
        "System.out.print((int) (2.7 + 0.5));", "System.out.print((int) (2.4 + 0.5));", "System.out.print(Math.round(2.5));",
        "System.out.print((int) -2.7);", "System.out.print((int) 7.99 + (int) 0.99);"],
        "(int) truncates toward zero; adding 0.5 first rounds a positive number to the nearest integer")),
    ("PR-1.5.B", JN("pr-overflow-long", JB, [
        "long n = 100000 * 100000;\nSystem.out.print(n);", "long n = 100000L * 100000;\nSystem.out.print(n);",
        "int n = Integer.MAX_VALUE;\nn++;\nSystem.out.print(n);", "int n = Integer.MIN_VALUE;\nSystem.out.print(-n);"],
        "int arithmetic wraps at 2³¹; the result is computed in int before it is widened to long unless an operand is long")),
    ("PR-1.5.C", J("pr-double-eq", JB, [
        ("System.out.print(0.1 + 0.2 == 0.3);", ["true", "0.3", "An error"]),
        ("System.out.print(Math.abs(0.1 + 0.2 - 0.3) < 1e-9);", ["false", "0.0", "An error"]),
        ("System.out.print(0.5 + 0.25 == 0.75);", ["false", "0.75", "An error"]),
        ("double s = 0;\nfor (int k = 0; k < 10; k++) s += 0.1;\nSystem.out.print(s == 1.0);", ["true", "1.0", "0.9999999999999999"])],
        "Most decimal fractions have no exact binary form; sums of halves and quarters are exact, sums of tenths are not")),
    ("PR-1.6.A", facts("pr-api-docs", JO, [
        ("The docs list String substring(int beginIndex). It returns:", "A String", "void", "An int", "A char"),
        ("The docs say indexOf returns −1 if the substring is not found. This is its:", "Postcondition for the not-found case", "Precondition", "Parameter", "Exception"),
        ("To find a method that tells whether a list contains an element, look in the docs for:", "boolean contains(Object o)", "void add(E e)", "int size()", "E get(int i)"),
        ("Math.sqrt is listed as static double sqrt(double a). You call it as:", "Math.sqrt(x)", "new Math().sqrt(x)", "x.sqrt()", "sqrt Math(x)"),
        ("charAt(int index) 'Throws IndexOutOfBoundsException if index is out of range' tells you:", "The precondition 0 ≤ index < length()", "It returns −1", "It never fails", "It returns null"),
    ], "Read return type, parameters, pre- and postconditions")),
    ("PR-1.6.A", facts("pr-api-docs-2", JO, [
        ("ArrayList's remove(int index) returns:", "The element removed", "void", "A boolean always", "The new size"),
        ("A method documented as void:", "Returns nothing, so it can't be used in an expression", "Returns 0", "Returns null", "Returns a boolean"),
        ("The docs mark a method 'deprecated'. You should:", "Prefer the replacement the docs name", "Always use it", "It's an error", "Ignore the docs"),
    ], "The signature and the description together say how to call it")),
    ("PR-1.6.B", J("pr-overload-pick", JB, [
        ("f(3);", ["d", "s", "An error"]), ("f(3.0);", ["i", "s", "An error"]), ("f(\"3\");", ["i", "d", "An error"]), ("f('a');", ["d", "s", "An error"]),
        ("f(3L);", ["i", "s", "An error"])],
        "Java picks the most specific overload the argument fits: exact match first, then widening (char → int, long → double)",
        defs="static void f(int x) { System.out.print(\"i\"); }\nstatic void f(double x) { System.out.print(\"d\"); }\nstatic void f(String x) { System.out.print(\"s\"); }")),
    ("PR-1.6.B", facts("pr-call-signature", JB, [
        ("double area(double r) is called as:", "double a = area(2.5);", "area(double 2.5);", "double a = area();", "area = 2.5;"),
        ("void greet(String name) can't be used as:", "String s = greet(\"Ann\");", "greet(\"Ann\");", "greet(name);", "greet(\"\" + 5);"),
        ("Overloaded methods must differ in:", "Their parameter lists", "Their return types only", "Their names", "Their comments"),
        ("int max(int a, int b) called as max(3) is:", "A compile error: wrong number of arguments", "Fine", "A run-time error", "Returns 3"),
    ], "Arguments must match the parameter list in number, order and type")),
    ("PR-1.6.C", JN("pr-static-calls", JB, [
        "System.out.print(Integer.parseInt(\"42\") + 1);", "System.out.print(Math.max(3, Math.min(10, 7)));",
        "System.out.print(Math.abs(-8) + Math.floorMod(-7, 3));", "System.out.print((int) Math.pow(2, 10));",
        "System.out.print(Integer.MAX_VALUE / 1000000);"],
        "Static methods belong to the class: ClassName.method(args), no object needed")),
    ("PR-1.6.C", facts("pr-static-facts", JB, [
        ("Math.sqrt(16) is called on:", "The Math class, no object", "An object made with new Math()", "The number 16", "System"),
        ("A static method can't directly use:", "Instance variables (there is no this)", "Its parameters", "Local variables", "Other static methods"),
        ("Why is main static?", "The JVM calls it before any object exists", "For speed", "It needn't be", "To make it private"),
    ], "Static means 'of the class'")),
    ("PR-1.6.E", facts("pr-pre-post", JO, [
        ("For double sqrtOf(double x), a sensible precondition is:", "x ≥ 0", "The result ≥ 0", "x is an int", "None"),
        ("A postcondition for sort(int[] a) is:", "a is in non-decreasing order and holds the same values", "a is not null", "a has length ≥ 1", "It runs fast"),
        ("If a caller breaks a method's precondition:", "The method promises nothing", "The method must fix it", "Java throws automatically", "It's a compile error"),
        ("A Javadoc @return tag documents:", "What the method returns", "The parameters", "The author", "Exceptions"),
    ], "Preconditions bind the caller; postconditions bind the method")),
    ("PR-1.6.E", facts("pr-pre-post-2", JO, [
        ("int indexOf(int[] a, int t) returns the first index of t, or −1. Its postcondition for 'not found' is:", "Returns −1", "Throws an exception", "Returns 0", "Returns a.length"),
        ("A good method comment says:", "What it does, not line by line how", "Every variable's name", "The author's mood", "Nothing"),
        ("'@param n must be positive' states:", "A precondition", "A postcondition", "A return value", "An exception"),
    ], "Contracts make methods usable without reading their code")),
    ("PR-1.7.A", facts("pr-class-object", JO, [
        ("A class is to an object as:", "A blueprint is to a house built from it", "A house is to a blueprint", "A method is to a variable", "A loop is to an if"),
        ("Dog d; declares:", "A reference that can hold a Dog object (or null)", "A Dog object", "A class", "A method"),
        ("Two objects of the same class share:", "Their methods, but each has its own instance variables", "All variable values", "Nothing", "Their references"),
        ("d.bark() on d == null throws:", "NullPointerException", "ClassCastException", "Nothing", "A compile error"),
    ], "Objects are instances of a class; references point to them")),
    ("PR-1.7.A", facts("pr-class-object-2", JO, [
        ("How many objects does 'Dog a = new Dog(); Dog b = a;' create?", "One", "Two", "Zero", "Three"),
        ("A reference variable holds:", "The address of an object (or null)", "The object's fields copied", "The class", "A primitive value"),
        ("An object with no references left is:", "Eligible for garbage collection", "Deleted immediately", "Saved to disk", "Still usable"),
    ], "new makes objects; = copies references")),
    ("PR-1.7.B", J("pr-ctor-pick", JO, [
        ("new Box();", ["B1", "B2", "An error"]), ("new Box(3);", ["B0", "B2", "An error"]), ("new Box(3, 4);", ["B0", "B1", "An error"]),
        ("new Box(3.5);", ["B0", "B1", "B2"])],
        "The constructor is chosen by the argument list, like an overloaded method",
        defs="static class Box {\n  Box() { System.out.print(\"B0\"); }\n  Box(int w) { System.out.print(\"B1\"); }\n  Box(int w, int h) { System.out.print(\"B2\"); }\n  Box(double w) { System.out.print(\"Bd\"); }\n}")),
    ("PR-1.7.B", facts("pr-new-facts", JO, [
        ("If a class declares only Box(int w), then new Box() is:", "A compile error: no no-argument constructor", "Fine", "A run-time error", "Gives w = 0"),
        ("A constructor has:", "The class's name and no return type", "A void return type", "Any name", "A static modifier"),
        ("new Box(5) returns:", "A reference to a new Box object", "void", "The int 5", "null"),
    ], "Constructors build and initialise objects")),
    ("PR-1.7.C", J("pr-object-state", JO, [
        ("Counter c = new Counter();\nc.inc(); c.inc(); c.reset(); c.inc();\nSystem.out.print(c.get());", ["3", "0", "2"]),
        ("Counter c = new Counter();\nCounter d = new Counter();\nc.inc(); d.inc(); d.inc();\nSystem.out.print(c.get() + \" \" + d.get());", ["3 3", "2 1", "1 1"]),
        ("Counter c = null;\nc.inc();\nSystem.out.print(\"ok\");", ["ok", "0", "1"])],
        "Each object keeps its own state; calling a method on null throws NullPointerException",
        defs="static class Counter {\n  private int n;\n  void inc() { n++; }\n  void reset() { n = 0; }\n  int get() { return n; }\n}")),
    ("PR-1.7.D", J("pr-alias-array", JO, [
        ("int[] a = {1, 2, 3};\nint[] b = a;\nb[0] = 9;\nSystem.out.print(a[0]);", ["1", "0", "An error"]),
        ("int[] a = {1, 2, 3};\nint[] b = a.clone();\nb[0] = 9;\nSystem.out.print(a[0]);", ["9", "0", "An error"]),
        ("int[] a = {1, 2, 3};\nint[] b = a;\nb = new int[]{7, 8};\nSystem.out.print(a[0]);", ["7", "0", "An error"]),
        ("StringBuilder s = new StringBuilder(\"hi\");\nStringBuilder t = s;\nt.append(\"!\");\nSystem.out.print(s);", ["hi", "!", "An error"])],
        "Assigning a reference shares the object; reassigning one reference later doesn't move the other")),
    ("PR-1.8.A", J("pr-concat-loop", JO, [
        ("String s = \"\";\nfor (int k = 1; k <= 3; k++) s += k;\nSystem.out.print(s);", ["6", "321", "1 2 3"]),
        ("String s = \"x\";\ns = s + 1 + 2;\nSystem.out.print(s);", ["x3", "3x", "12x"]),
        ("String s = 1 + 2 + \"\";\ns += 1 + 2;\nSystem.out.print(s);", ["123", "312", "6"]),
        ("String s = \"ab\";\ns.concat(\"cd\");\nSystem.out.print(s);", ["abcd", "cd", "An error"])],
        "+ with a String concatenates left to right; Strings are immutable, so concat returns a new String you must keep")),
    ("PR-1.8.B", JN("pr-compareto", JO, [
        "System.out.print(\"apple\".compareTo(\"banana\"));", "System.out.print(\"cat\".compareTo(\"car\"));",
        "System.out.print(\"Zoo\".compareTo(\"apple\"));", "System.out.print(\"ab\".compareTo(\"abcd\"));", "System.out.print(\"same\".compareTo(\"same\"));"],
        "compareTo returns the difference of the first differing chars (Unicode), or of lengths if one is a prefix; negative means 'comes first'")),
    ("PR-1.8.C", J("pr-integer-cache", JO, [
        ("Integer a = 127, b = 127;\nSystem.out.print(a == b);", ["false", "127", "An error"]),
        ("Integer a = 128, b = 128;\nSystem.out.print(a == b);", ["true", "128", "An error"]),
        ("Integer a = 128, b = 128;\nSystem.out.print(a.equals(b));", ["false", "128", "An error"]),
        ("String a = \"hi\";\nString b = new String(\"hi\");\nSystem.out.print(a == b);", ["true", "hi", "An error"])],
        "== compares references; small Integers (−128…127) are cached so == happens to work there. Use equals for values")),
    # ── 2 selection and iteration ─────────────────────────────────────────────────────────────────────────────────
    ("PR-2.1.A", J("pr-relational", JC, [
        ("System.out.print(7 != 7.0);", ["true", "An error", "7"]), ("System.out.print('a' < 'b');", ["false", "An error", "97"]),
        ("int x = 5;\nSystem.out.print(x >= 5 == true);", ["false", "An error", "5"]), ("System.out.print(10 / 4 == 2.5);", ["true", "An error", "2.5"])],
        "Numbers are compared after promotion (7 == 7.0); chars compare by code; integer division happens before ==")),
    ("PR-2.1.A", facts("pr-relational-facts", JC, [
        ("x = 5 inside an if condition in Java:", "Is a compile error (an int is not a boolean)", "Compares x with 5", "Is always true", "Is always false"),
        ("To test 0 < x < 10 in Java, write:", "0 < x && x < 10", "0 < x < 10", "x in (0, 10)", "0 < x || x < 10"),
        ("!(x > 3) is the same as:", "x <= 3", "x < 3", "x >= 3", "x != 3"),
    ], "Relational operators give booleans; chain them with &&")),
    ("PR-2.1.B", J("pr-elseif-order", JC, [
        ("int s = 85;\nif (s >= 60) System.out.print(\"D\");\nelse if (s >= 80) System.out.print(\"B\");\nelse System.out.print(\"F\");", ["B", "DB", "F"]),
        ("int s = 85;\nif (s >= 80) System.out.print(\"B\");\nif (s >= 60) System.out.print(\"D\");", ["B", "D", "Nothing"]),
        ("int s = 55;\nif (s >= 80) System.out.print(\"B\");\nelse if (s >= 60) System.out.print(\"D\");\nelse System.out.print(\"F\");", ["D", "B", "DF"])],
        "An else-if chain runs only the first true branch, so order matters; separate ifs can each run")),
    ("PR-2.1.C", J("pr-dangling-else", JC, [
        ("int x = 5;\nif (x > 10)\n  if (x > 20) System.out.print(\"a\");\nelse System.out.print(\"b\");\nSystem.out.print(\"c\");", ["bc", "ac", "b"]),
        ("int x = 15;\nif (x > 10)\n  if (x > 20) System.out.print(\"a\");\nelse System.out.print(\"b\");\nSystem.out.print(\"c\");", ["c", "ac", "b"]),
        ("int x = 5;\nif (x > 10) {\n  if (x > 20) System.out.print(\"a\");\n} else System.out.print(\"b\");\nSystem.out.print(\"c\");", ["c", "ac", "b"])],
        "An else belongs to the nearest unmatched if, whatever the indentation; braces change that")),
    ("PR-2.1.D", Q("pr-leap-year", JC, "Is {{yr}} a leap year (divisible by 4, except century years not divisible by 400)?",
        cases=[{"yr": y, "lc": f"import calendar\nprint(int(calendar.isleap({y})))", "kd": 0 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 1}
               for y in (1900, 2000, 2024, 2100, 2023, 2400)],
        choice=["Leap year", "Not a leap year"], correct="kd", verify="1 - py_out(lc)",
        explain="if (y % 400 == 0) leap; else if (y % 100 == 0) not; else if (y % 4 == 0) leap; else not")),
    ("PR-2.1.D", J("pr-grade-band", JC, [(f"int s = {s};\nString g;\nif (s >= 90) g = \"A\";\nelse if (s >= 80) g = \"B\";\nelse if (s >= 70) g = \"C\";\nelse g = \"F\";\nSystem.out.print(g);", w)
        for s, w in [(90, ["B", "C", "F"]), (89, ["A", "C", "F"]), (70, ["B", "F", "A"]), (69, ["C", "B", "A"])]],
        "Check the highest band first so each later test can assume the earlier ones failed")),
    ("PR-2.2.A", J("pr-short-circuit-side", JC, [
        ("int n = 0;\nif (n != 0 && 10 / n > 1) System.out.print(\"a\");\nSystem.out.print(\"b\");", ["ab", "ArithmeticException", "a"]),
        ("int n = 0;\nif (n == 0 || 10 / n > 1) System.out.print(\"a\");\nSystem.out.print(\"b\");", ["b", "ArithmeticException", "a"]),
        ("int n = 0;\nif (n != 0 & 10 / n > 1) System.out.print(\"a\");\nSystem.out.print(\"b\");", ["b", "ab", "a"])],
        "&& stops at a false left side and || at a true one, so the right side may never run; & and | always evaluate both")),
    ("PR-2.2.B", facts("pr-demorgan-pick", JC, [
        ("!(a && b) is equivalent to:", "!a || !b", "!a && !b", "a || b", "!a && b"),
        ("!(x > 0 || y > 0) is equivalent to:", "x <= 0 && y <= 0", "x <= 0 || y <= 0", "x < 0 && y < 0", "x > 0 && y > 0"),
        ("!(age >= 13 && age <= 19) is equivalent to:", "age < 13 || age > 19", "age < 13 && age > 19", "age <= 13 || age >= 19", "age > 13 && age < 19"),
        ("!(!a || b) is equivalent to:", "a && !b", "!a && b", "a || !b", "!a || !b"),
    ], "Negate each part and swap && with ||")),
    ("PR-2.2.C", Q("pr-equiv-check", JC, "Are {{fs}} and {{gs}} equivalent for all booleans a, b, c?",
        cases=[{"fs": "a && (b || c)", "gs": "(a && b) || (a && c)", "f": "a and (b or c)", "g": "(a and b) or (a and c)", "kd": 0},
               {"fs": "a || (b && c)", "gs": "(a || b) && c", "f": "a or (b and c)", "g": "(a or b) and c", "kd": 1},
               {"fs": "!(a && b)", "gs": "!a && !b", "f": "not (a and b)", "g": "(not a) and (not b)", "kd": 1},
               {"fs": "a || (a && b)", "gs": "a", "f": "a or (a and b)", "g": "a", "kd": 0},
               {"fs": "(a || b) && !(a && b)", "gs": "a != b", "f": "(a or b) and not (a and b)", "g": "a != b", "kd": 0}],
        choice=["Equivalent", "Not equivalent"], correct="kd", verify="1 - cs_equiv(f, g, 'a b c')",
        explain="Fill a truth table, or find one assignment where they differ")),
    ("PR-2.2.C", facts("pr-counterexample", JC, [
        ("A counterexample showing a || (b && c) differs from (a || b) && c:", "a = true, c = false", "a = false, b = false", "all true", "all false"),
        ("A counterexample showing !(a && b) differs from !a && !b:", "a = true, b = false", "a = b = true", "a = b = false", "None exists"),
        ("To prove two expressions equivalent with a truth table for 3 variables, check:", "All 8 rows", "1 row", "3 rows", "4 rows"),
    ], "One differing row disproves; all rows prove")),
    ("PR-2.3.A", JN("pr-while-iter", JC, [
        "int n = 100, k = 0;\nwhile (n > 1) { n /= 2; k++; }\nSystem.out.print(k);", "int n = 1, k = 0;\nwhile (n < 1000) { n *= 3; k++; }\nSystem.out.print(k);",
        "int n = 50, k = 0;\nwhile (n > 0) { n -= 7; k++; }\nSystem.out.print(k);", "int n = 10, k = 0;\nwhile (n != 0) { n = n / 3; k++; }\nSystem.out.print(k);"],
        "Count the passes with a trace table: check the condition, run the body, repeat")),
    ("PR-2.3.B", facts("pr-infinite-loop", JC, [
        ("int k = 0; while (k < 10) { System.out.print(k); } never stops because:", "k is never updated", "The condition is false", "print is slow", "k is an int"),
        ("for (int k = 10; k > 0; k++) runs:", "Until k overflows (practically forever)", "10 times", "Never", "Once"),
        ("int k = 10; while (k < 10) k++; runs the body:", "Zero times", "Once", "Ten times", "Forever"),
        ("while (x != 0) x -= 2; with x = 5:", "Never stops (skips 0)", "Stops after 2 passes", "Stops after 3", "Never runs"),
        ("A fix for while (x != 0) x -= 2; with odd x is:", "Use while (x > 0)", "Use x -= 1 only when even", "Add a print", "Use do-while"),
    ], "Check initialisation, condition and update together")),
    ("PR-2.3.B", facts("pr-loop-fix", JC, [
        ("A loop meant to read until input is 0 ends after one pass. Likely cause:", "The condition was tested on the wrong variable or reset inside", "Too many variables", "A missing semicolon", "Nothing"),
        ("for (int k = 0; k < n; k--) should be:", "for (int k = 0; k < n; k++)", "for (int k = 0; k > n; k--)", "for (int k = n; k < n; k++)", "It is correct"),
        ("A do-while loop's body runs:", "At least once", "Zero or more times", "Never", "Exactly once"),
    ], "Every loop needs progress toward its exit")),
    ("PR-2.3.C", JN("pr-reverse-digits", JC, [f"int n = {n}, r = 0;\nwhile (n > 0) {{\n  r = r * 10 + n % 10;\n  n /= 10;\n}}\nSystem.out.print(r);" for n in (1234, 907, 5500, 12321)],
        "n % 10 peels the last digit; n / 10 drops it; r * 10 + d appends it. Trailing zeros vanish")),
    ("PR-2.4.A", JN("pr-for-step", JC, [
        "int c = 0;\nfor (int k = 3; k <= 30; k += 3) c++;\nSystem.out.print(c);", "int c = 0;\nfor (int k = 100; k > 0; k -= 7) c++;\nSystem.out.print(c);",
        "int c = 0;\nfor (int k = 1; k < 1000; k *= 2) c++;\nSystem.out.print(c);", "int c = 0;\nfor (int k = -5; k < 5; k += 2) c++;\nSystem.out.print(c);"],
        "Count the values the loop variable takes: ⌊(end − start)/step⌋ + 1 when the bound is inclusive and reachable")),
    ("PR-2.4.B", JN("pr-for-accum", JC, [
        "int s = 0;\nfor (int k = 1; k <= 5; k++) s += k * k;\nSystem.out.print(s);", "int p = 1;\nfor (int k = 2; k <= 6; k += 2) p *= k;\nSystem.out.print(p);",
        "int s = 0;\nfor (int k = 10; k >= 0; k -= 3) s += k;\nSystem.out.print(s);", "int s = 0;\nfor (int k = 0; k < 20; k++) if (k % 3 == 0) s++;\nSystem.out.print(s);"],
        "Keep a trace table of k and the accumulator")),
    ("PR-2.4.B", J("pr-for-print", JC, [
        ("for (int k = 0; k < 4; k++) System.out.print(k * 2 + \" \");", ["0 2 4 6 8", "2 4 6 8", "0 1 2 3"]),
        ("for (int k = 5; k > 0; k -= 2) System.out.print(k);", ["5310", "531-1", "54321"]),
        ("for (int k = 1; k <= 10; k *= 3) System.out.print(k + \",\");", ["1,3,9,27,", "3,9,", "1,4,7,10,"])],
        "List the values of k first, then apply the body to each")),
    ("PR-2.4.C", facts("pr-off-by-one-fix", JC, [
        ("Summing a[0..n−1] with for (k = 1; k <= n; k++) s += a[k]; has two bugs. The fix:", "for (k = 0; k < n; k++)", "for (k = 1; k < n; k++)", "for (k = 0; k <= n; k++)", "for (k = 1; k <= n − 1; k++)"),
        ("Printing 1 to 10 with for (k = 1; k < 10; k++):", "Misses 10: use k <= 10", "Is correct", "Prints 0", "Misses 1"),
        ("A loop over pairs a[k], a[k + 1] should stop at:", "k < a.length − 1", "k < a.length", "k <= a.length", "k < a.length + 1"),
        ("Fence-post rule: 10 posts with 1 m between neighbours span:", "9 m", "10 m", "11 m", "1 m"),
    ], "Check the first and last iterations")),
    ("PR-2.5.A", J("pr-average-bug", JC, [
        ("int[] a = {1, 2, 2};\nint s = 0;\nfor (int v : a) s += v;\nSystem.out.print(s / a.length);", ["1.67", "2", "1.6666666666666667"]),
        ("int[] a = {1, 2, 2};\nint s = 0;\nfor (int v : a) s += v;\nSystem.out.print((double) s / a.length);", ["1", "1.67", "2.0"]),
        ("int[] a = {3, 8, 5, 8};\nint c = 0;\nfor (int v : a) if (v == 8) c++;\nSystem.out.print(c);", ["1", "8", "16"])],
        "Average = sum / count, with at least one double operand to avoid truncation")),
    ("PR-2.5.B", JN("pr-min-init", JC, [
        "int[] a = {5, 3, 9};\nint m = 0;\nfor (int v : a) if (v < m) m = v;\nSystem.out.print(m);",
        "int[] a = {5, 3, 9};\nint m = a[0];\nfor (int v : a) if (v < m) m = v;\nSystem.out.print(m);",
        "int[] a = {-5, -3, -9};\nint m = 0;\nfor (int v : a) if (v > m) m = v;\nSystem.out.print(m);",
        "int[] a = {-5, -3, -9};\nint m = Integer.MIN_VALUE;\nfor (int v : a) if (v > m) m = v;\nSystem.out.print(m);"],
        "Start a running min or max at the first element (or ±∞), never at 0: 0 may be better than every real value")),
    ("PR-2.5.C", Q("pr-gcd-steps", JC, "Euclid's algorithm: while b ≠ 0, (a, b) ← (b, a mod b). What is gcd({{a}}, {{b}})?",
        given={"a": {"pick": [84, 252, 1071]}, "b": {"pick": [36, 105, 462]}}, value="gcd(a, b)", tex="g", final=True,
        verify="gcd(a, b)",
        explain="Each step keeps the gcd while shrinking the numbers; it ends when the remainder is 0")),
    ("PR-2.6.A", JN("pr-count-sub", JC, [
        "String s = \"banana\";\nint c = 0;\nfor (int k = 0; k + 2 <= s.length(); k++)\n  if (s.substring(k, k + 2).equals(\"an\")) c++;\nSystem.out.print(c);",
        "String s = \"aaaa\";\nint c = 0;\nfor (int k = 0; k + 2 <= s.length(); k++)\n  if (s.substring(k, k + 2).equals(\"aa\")) c++;\nSystem.out.print(c);",
        "String s = \"mississippi\";\nint c = 0;\nfor (int k = 0; k < s.length(); k++)\n  if (s.charAt(k) == 's') c++;\nSystem.out.print(c);",
        "String s = \"hello world\";\nSystem.out.print(s.indexOf(\"o\", 5));"],
        "Slide a window of the pattern's length; overlapping matches all count")),
    ("PR-2.6.B", J("pr-build-string", JC, [
        ("String s = \"level\", r = \"\";\nfor (int k = s.length() - 1; k >= 0; k--) r += s.charAt(k);\nSystem.out.print(r.equals(s));", ["false", "level", "levle"]),
        ("String s = \"stats!\", r = \"\";\nfor (int k = s.length() - 1; k >= 0; k--) r += s.charAt(k);\nSystem.out.print(r);", ["stats!", "stat", "!stat"]),
        ("String s = \"banana\", r = \"\";\nfor (int k = 0; k < s.length(); k++)\n  if (s.charAt(k) != 'a') r += s.charAt(k);\nSystem.out.print(r);", ["banana", "aaa", "bnna"])],
        "Walk the string and append the characters you keep, in the order you want them")),
    ("PR-2.7.A", Q("pr-triangle-count", JC, "for (int i = 0; i < {{n}}; i++) for (int j = 0; j < i; j++) count++; What is count?",
        given={"n": {"pick": [5, 10, 20, 100]}}, value="n*(n - 1)/2", tex="c", final=True,
        verify="summation(Symbol('k'), (Symbol('k'), 0, n - 1))", explain="The inner loop runs 0, 1, …, n − 1 times: n(n − 1)/2")),
    ("PR-2.7.B", J("pr-pattern", JC, [
        ("for (int i = 1; i <= 3; i++) {\n  for (int j = 1; j <= i; j++) System.out.print(j);\n  System.out.println();\n}", ["1 / 11 / 111", "123 / 12 / 1", "1 / 2 / 3"]),
        ("for (int i = 3; i >= 1; i--) {\n  for (int j = 0; j < i; j++) System.out.print(\"*\");\n  System.out.println();\n}", ["* / ** / ***", "*** / *** / ***", "*** / ** / *** "]),
        ("for (int i = 1; i <= 3; i++) {\n  for (int j = 1; j <= 3; j++) System.out.print(i * j + \" \");\n  System.out.println();\n}", ["1 2 3 / 1 2 3 / 1 2 3", "1 4 9", "1 2 3 4 6 9"])],
        "The outer loop chooses the row; the inner loop prints that row's items")),
    ("PR-2.8.A", Q("pr-stmt-count", JA, "How many times does the innermost statement run, for n = {{n}}? {{loops}}",
        cases=[{"loops": "for i in 0..n−1: for j in 0..n−1: s", "kk": 0}, {"loops": "for i in 0..n−1: s; for j in 0..n−1: s", "kk": 1},
               {"loops": "for (i = 1; i < n; i *= 2): s", "kk": 2}],
        given={"n": {"pick": [16, 64]}},
        value="kk == 0 ? n^2 : (kk == 1 ? 2*n : log2(n))", tex="c", final=True,
        verify="n**2 if kk == 0 else (2*n if kk == 1 else log(n, 2))", explain="Nested full loops multiply (n²), loops in sequence add (2n), doubling takes log₂ n steps")),
    ("PR-2.8.A", facts("pr-growth-compare", JA, [
        ("Algorithm A does 100n steps, B does n². For large n:", "A is faster", "B is faster", "They are equal", "It depends only on hardware"),
        ("Doubling n for a quadratic algorithm multiplies its time by about:", "4", "2", "8", "1"),
        ("Linear search versus binary search on a sorted array of 10⁶ items, worst case:", "About 10⁶ versus about 20 comparisons", "Equal", "20 versus 10⁶", "10⁶ versus 10³"),
    ], "Count how steps grow with n, not the exact number")),
    # ── 3 classes ─────────────────────────────────────────────────────────────────────────────────────────────────
    ("PR-3.1.A", facts("pr-decompose", JO, [
        ("A library system tracks books and members who borrow them. Good classes are:", "Book, Member and Loan", "Library only", "One class per method", "Borrow and Return"),
        ("A bank Account class's attributes are:", "Balance and owner", "deposit and withdraw", "Bank and teller", "Interest rate formula"),
        ("A behaviour (method) of a Thermostat:", "setTarget(temp)", "target", "Room", "Celsius"),
        ("Nouns in a problem statement usually become:", "Classes or attributes", "Methods", "Loops", "Exceptions"),
    ], "Nouns suggest classes and fields; verbs suggest methods")),
    ("PR-3.1.A", facts("pr-decompose-2", JO, [
        ("A class that parses files, computes taxes and draws charts should be:", "Split so each class has one job", "Kept as one", "Made static", "Renamed"),
        ("Where should 'compute the total of an order' live?", "In Order, which holds the items", "In Customer", "In main only", "In a global variable"),
        ("Verbs such as 'enrol', 'pay', 'ship' usually become:", "Methods", "Classes", "Fields", "Packages"),
    ], "Put behaviour next to the data it uses")),
    ("PR-3.1.B", facts("pr-private-access", JO, [
        ("Outside class Account, with private double balance, acct.balance = 0; is:", "A compile error", "Allowed", "A run-time error", "Allowed in main"),
        ("Why make instance variables private?", "So the class controls every change and keeps its invariants", "For speed", "Java requires it", "To hide methods"),
        ("Code outside the class can use:", "Public methods and constructors", "Private fields", "Private methods", "Nothing"),
        ("A private helper method can be called:", "Only from inside its class", "From anywhere", "From subclasses only", "Never"),
    ], "Encapsulation: private data, public behaviour")),
    ("PR-3.1.B", facts("pr-private-access-2", JO, [
        ("Inside class Account, another Account's private balance:", "Is accessible (privacy is per class, not per object)", "Is not accessible", "Is null", "Needs a getter"),
        ("A public field that any code can set to a negative balance breaks:", "The class invariant", "Compilation", "Nothing", "The JVM"),
        ("The keyword with no modifier (package-private) allows access from:", "The same package", "Everywhere", "Nowhere", "Subclasses only"),
    ], "Access is decided by where the code is written")),
    ("PR-3.2.A", J("pr-ctor-shadow", JO, [
        ("System.out.print(new P(5).x);", ["5", "null", "An error"]), ("System.out.print(new Q(5).x);", ["0", "null", "An error"]),
        ("System.out.print(new P(5).x + new Q(5).x);", ["10", "0", "An error"])],
        "x = x assigns the parameter to itself; this.x = x sets the field",
        defs="static class P { int x; P(int x) { x = x; } }\nstatic class Q { int x; Q(int x) { this.x = x; } }")),
    ("PR-3.2.A", facts("pr-ctor-facts", JO, [
        ("A constructor should:", "Set every instance variable to a valid starting value", "Print the object", "Return the object", "Be static"),
        ("this(…) as the first line of a constructor:", "Calls another constructor of the same class", "Creates a new object", "Is illegal", "Calls the superclass only"),
        ("If you write no constructor at all, Java supplies:", "A no-argument constructor that leaves default values", "Nothing", "A constructor for every field", "An error"),
    ], "Constructors establish the object's invariant")),
    ("PR-3.2.B", J("pr-default-null", JO, [
        ("Pet p = new Pet();\nSystem.out.print(\"Hi \" + p.name);", ["Hi ", "NullPointerException", "Hi name"]),
        ("Pet p = new Pet();\nSystem.out.print(p.age + \" \" + p.cute);", ["null null", "0 true", "An error"]),
        ("Pet p = new Pet();\nSystem.out.print(p.name.length());", ["0", "null", "4"])],
        "Unset fields get defaults: 0, 0.0, false, null. Concatenating null prints 'null'; calling a method on it throws",
        defs="static class Pet { String name; int age; boolean cute; }")),
    ("PR-3.3.A", facts("pr-accessor", JO, [
        ("An accessor for private double price is:", "public double getPrice() { return price; }", "public void getPrice() { return price; }", "public double getPrice(double p)", "private double getPrice()"),
        ("A mutator for price is:", "public void setPrice(double p) { price = p; }", "public double setPrice()", "public void setPrice() { return price; }", "private setPrice"),
        ("A mutator can protect the invariant by:", "Rejecting invalid values (e.g. negative prices)", "Returning the field", "Being static", "Nothing"),
        ("A getter that returns a private array directly lets callers:", "Change the object's internal state", "Only read it", "Nothing", "Crash it"),
    ], "Getters return a copy or value; setters validate")),
    ("PR-3.3.A", facts("pr-accessor-2", JO, [
        ("Return type of a method that returns nothing:", "void", "null", "int", "Object"),
        ("boolean isEmpty() is an example of:", "An accessor", "A mutator", "A constructor", "A static method"),
        ("An immutable class has:", "No mutators, and final private fields", "Only setters", "Public fields", "No constructor"),
    ], "Name, return type and side effects tell accessors from mutators")),
    ("PR-3.3.B", J("pr-swap-method", JO, [
        ("int a = 1, b = 2;\nswap(a, b);\nSystem.out.print(a + \" \" + b);", ["2 1", "1 1", "2 2"]),
        ("int[] v = {1, 2};\nswapIn(v);\nSystem.out.print(v[0] + \" \" + v[1]);", ["1 2", "1 1", "2 2"]),
        ("int[] v = {1, 2};\nreplace(v);\nSystem.out.print(v[0]);", ["9", "0", "2"])],
        "Java passes copies: a copy of an int, or a copy of a reference. Changing the object through the copy shows; reassigning it does not",
        defs="static void swap(int x, int y) { int t = x; x = y; y = t; }\nstatic void swapIn(int[] a) { int t = a[0]; a[0] = a[1]; a[1] = t; }\nstatic void replace(int[] a) { a = new int[]{9, 9}; }")),
    ("PR-3.3.C", J("pr-two-objects", JO, [
        ("Acct a = new Acct(100), b = new Acct(50);\na.pay(b, 30);\nSystem.out.print(a.bal + \" \" + b.bal);", ["100 50", "70 20", "130 80"]),
        ("Acct a = new Acct(100), b = a;\nb.pay(a, 30);\nSystem.out.print(a.bal);", ["70", "130", "40"]),
        ("Acct a = new Acct(10), b = new Acct(0);\na.pay(b, 30);\nSystem.out.print(a.bal + \" \" + b.bal);", ["-20 30", "10 30", "0 0"])],
        "Trace each object's fields; two names for one object see the same changes",
        defs="static class Acct {\n  int bal;\n  Acct(int b) { bal = b; }\n  void pay(Acct o, int x) {\n    if (x <= bal) { bal -= x; o.bal += x; }\n  }\n}")),
    ("PR-3.4.A", JN("pr-static-counter", JO, [
        "new T(); new T(); T t = new T();\nSystem.out.print(T.made);", "T a = new T();\nT b = a;\nSystem.out.print(T.made);",
        "for (int k = 0; k < 5; k++) new T();\nSystem.out.print(T.made * 10 + new T().id);"],
        "A static field has one copy for the class; every constructor call increments the same counter",
        defs="static class T {\n  static int made = 0;\n  int id;\n  T() { made++; id = made; }\n}")),
    ("PR-3.4.B", JN("pr-shadow-this", JO, [
        "System.out.print(new S().f(5));", "System.out.print(new S().g(5));", "S s = new S();\ns.h(7);\nSystem.out.print(s.x);"],
        "Inside a method, a parameter or local named x hides the field x; this.x names the field",
        defs="static class S {\n  int x = 1;\n  int f(int x) { return x; }\n  int g(int x) { return this.x + x; }\n  void h(int x) { this.x = x * 2; }\n}")),
    ("PR-3.4.C", facts("pr-impact", JO, [
        ("Copying code from a GPL project into your closed-source app you sell:", "Requires releasing your app's source under the GPL", "Is always fine", "Needs only a comment", "Is fine if you rename it"),
        ("An app that predicts loan approval should first consider:", "Who could be harmed by errors or bias", "Font choices", "Code style", "Only speed"),
        ("Collecting users' location by default without telling them raises:", "Privacy and consent problems", "Only performance problems", "Nothing", "Licensing only"),
        ("Using a library under the MIT licence requires:", "Keeping its copyright notice", "Releasing your code", "Paying a fee", "Nothing at all"),
    ], "Software affects people beyond its users")),
    ("PR-3.4.C", facts("pr-impact-2", JO, [
        ("A school app stores student grades. Stakeholders include:", "Students, parents, teachers and the school", "Only the developer", "Only the server", "Nobody"),
        ("Accessibility in design means:", "People with disabilities can use the program", "It loads quickly", "It is cheap", "It is open source"),
        ("Scraping a website against its terms of use can be:", "A legal and ethical problem even if technically easy", "Always fine", "Required", "Encrypted"),
    ], "Name who is affected and what rules apply")),
    # ── 4 collections ─────────────────────────────────────────────────────────────────────────────────────────────
    ("PR-4.1.A", facts("pr-data-clean", JL, [
        ("A survey's age column has entries 'twenty', -3 and 250. Cleaning means:", "Converting or flagging invalid values", "Deleting the column", "Averaging as is", "Nothing"),
        ("Metadata for a sensor data set tells you:", "Units, collection times and how it was measured", "Only the values", "The averages", "Nothing useful"),
        ("Missing values coded as 0 in a temperature column will:", "Bias the mean downward", "Not matter", "Raise the mean", "Crash the program"),
        ("Duplicate rows from merging two files should be:", "Found and removed (or explained)", "Kept", "Summed", "Ignored"),
    ], "Know what each field means before trusting it")),
    ("PR-4.1.A", facts("pr-data-clean-2", JL, [
        ("Dates written as 03/04/2025 in one file and 2025-04-03 in another need:", "A single consistent format", "Nothing", "Sorting", "Deleting"),
        ("A data set can't tell you:", "Why its patterns happen, without more evidence", "Its means", "Its counts", "Its range"),
        ("Before analysis, record:", "Each cleaning step, so it can be repeated", "Nothing", "Only the result", "The plot colours"),
    ], "Cleaning is part of the analysis: document it")),
    ("PR-4.1.B", facts("pr-data-privacy", JL, [
        ("Name, home address and birth date together are:", "Personally identifiable information", "Anonymous data", "Metadata only", "Public by default"),
        ("A face-recognition model trained mostly on one group may:", "Err more often on other groups (bias)", "Work equally for all", "Be faster", "Be cheaper"),
        ("Informed consent means people:", "Understand and agree to how their data is used", "Clicked once", "Were not asked", "Paid a fee"),
        ("Removing names alone may not anonymise data because:", "Other fields can re-identify people when combined", "Names are needed", "It always works", "Of encryption"),
    ], "Collect only what you need, with consent, and check who is missing")),
    ("PR-4.1.B", facts("pr-data-privacy-2", JL, [
        ("A survey only reachable online misses:", "People without internet access (sampling bias)", "Nobody", "Only experts", "Only children"),
        ("Storing data you don't need increases:", "Harm if it leaks", "Accuracy", "Speed", "Nothing"),
        ("Aggregated counts (how many students per class) are usually:", "Lower privacy risk than individual rows", "More private than nothing", "Personally identifying", "Illegal"),
    ], "Data carries risks for the people in it")),
    ("PR-4.2.A", J("pr-array-defaults", JL, [
        ("double[] a = new double[3];\nSystem.out.print(a[1]);", ["0", "null", "An error"]), ("boolean[] a = new boolean[2];\nSystem.out.print(a[0]);", ["true", "0", "null"]),
        ("String[] a = new String[2];\nSystem.out.print(a[0]);", ["\"\"", "0", "NullPointerException"]), ("int[] a = {4, 5, 6};\nSystem.out.print(a.length + a[a.length - 1]);", ["3", "6", "ArrayIndexOutOfBoundsException"])],
        "new fills elements with 0, 0.0, false or null; length is a field, and the last index is length − 1")),
    ("PR-4.2.B", J("pr-index-ok", JL, [
        ("int[] a = new int[5];\nint k = 5;\nSystem.out.print(a[k - 1]);", ["ArrayIndexOutOfBoundsException", "5", "null"]),
        ("int[] a = new int[5];\nSystem.out.print(a[a.length]);", ["0", "5", "null"]),
        ("int[] a = {1, 2, 3};\nint k = -1;\nSystem.out.print(a[k + 1]);", ["ArrayIndexOutOfBoundsException", "3", "0"]),
        ("int[] a = {1, 2, 3};\nfor (int k = 0; k <= a.length; k++) System.out.print(a[k]);", ["123", "12", "1230"])],
        "Valid indices are 0 to length − 1; anything else throws at the moment it is used, after earlier output has printed")),
    ("PR-4.3.A", J("pr-foreach-change", JL, [
        ("int[] a = {1, 2, 3};\nfor (int v : a) v *= 2;\nSystem.out.print(a[0] + a[1] + a[2]);", ["12", "2", "An error"]),
        ("int[] a = {1, 2, 3};\nfor (int k = 0; k < a.length; k++) a[k] *= 2;\nSystem.out.print(a[0] + a[1] + a[2]);", ["6", "3", "An error"]),
        ("StringBuilder[] a = {new StringBuilder(\"a\"), new StringBuilder(\"b\")};\nfor (StringBuilder s : a) s.append(\"!\");\nSystem.out.print(a[0]);", ["a", "!", "An error"])],
        "The enhanced-for variable is a copy of each element: reassigning it changes nothing, but it can mutate the object it refers to")),
    ("PR-4.3.B", JN("pr-visit-indices", JL, [
        "int c = 0;\nfor (int k = 0; k < 10; k += 2) c++;\nSystem.out.print(c);", "int c = 0;\nfor (int k = 9; k >= 0; k -= 3) c++;\nSystem.out.print(c);",
        "int s = 0;\nint[] a = {5, 6, 7, 8, 9};\nfor (int k = 1; k < a.length; k += 2) s += a[k];\nSystem.out.print(s);",
        "int s = 0;\nint[] a = {5, 6, 7, 8, 9};\nfor (int k = a.length - 1; k > 0; k--) s += a[k];\nSystem.out.print(s);"],
        "List the indices first; a traversal that starts at 1 or stops at 0 exclusive skips an end")),
    ("PR-4.4.A", JN("pr-array-max", JL, [
        "int[] a = {-4, -9, -2, -7};\nint m = a[0];\nfor (int v : a) m = Math.max(m, v);\nSystem.out.print(m);",
        "int[] a = {3, 8, 1, 8, 2};\nint at = 0;\nfor (int k = 1; k < a.length; k++) if (a[k] > a[at]) at = k;\nSystem.out.print(at);",
        "int[] a = {3, 8, 1, 8, 2};\nint at = 0;\nfor (int k = 1; k < a.length; k++) if (a[k] >= a[at]) at = k;\nSystem.out.print(at);"],
        "> keeps the first maximum, >= the last")),
    ("PR-4.4.A", JN("pr-array-count", JL, [
        "int[] a = {12, 7, 30, 15, 8};\nint c = 0;\nfor (int v : a) if (v % 3 == 0) c++;\nSystem.out.print(c);",
        "int[] a = {2, 4, 6, 8};\ndouble s = 0;\nfor (int v : a) s += v;\nSystem.out.print(s / a.length);",
        "int[] a = {5, -1, 3, -4, 0};\nint s = 0;\nfor (int v : a) if (v > 0) s += v;\nSystem.out.print(s);"],
        "Sum, count and mean follow one pattern: initialise, update for each element, use after the loop")),
    ("PR-4.4.B", JN("pr-adjacent-count", JL, [
        "int[] a = {1, 3, 2, 5, 6, 4};\nint c = 0;\nfor (int k = 0; k < a.length - 1; k++) if (a[k + 1] > a[k]) c++;\nSystem.out.print(c);",
        "int[] a = {2, 2, 3, 3, 3, 1};\nint c = 0;\nfor (int k = 1; k < a.length; k++) if (a[k] == a[k - 1]) c++;\nSystem.out.print(c);",
        "int[] a = {1, 4, 9, 16};\nint m = 0;\nfor (int k = 1; k < a.length; k++) m = Math.max(m, a[k] - a[k - 1]);\nSystem.out.print(m);"],
        "Pairs run from (0, 1) to (n − 2, n − 1): n − 1 comparisons")),
    ("PR-4.4.C", J("pr-rotate", JL, [
        ("int[] a = {1, 2, 3, 4};\nint t = a[0];\nfor (int k = 0; k < a.length - 1; k++) a[k] = a[k + 1];\na[a.length - 1] = t;\nSystem.out.print(Arrays.toString(a));", ["[4, 1, 2, 3]", "[2, 3, 4, 4]", "[1, 2, 3, 4]"]),
        ("int[] a = {1, 2, 3, 4};\nfor (int k = 0; k < a.length - 1; k++) a[k + 1] = a[k];\nSystem.out.print(Arrays.toString(a));", ["[1, 1, 2, 3]", "[2, 3, 4, 4]", "[4, 1, 2, 3]"]),
        ("int[] a = {1, 2, 3, 4, 5};\nfor (int k = 0; k < a.length / 2; k++) {\n  int t = a[k]; a[k] = a[a.length - 1 - k]; a[a.length - 1 - k] = t;\n}\nSystem.out.print(Arrays.toString(a));", ["[1, 2, 3, 4, 5]", "[5, 4, 3, 4, 5]", "[5, 2, 3, 4, 1]"])],
        "Shifting forward in place overwrites before it reads: copy from the far end, or save the element you'll lose")),
    ("PR-4.5.A", facts("pr-scanner-file", JL, [
        ("To read a text file line by line in Java:", "Scanner in = new Scanner(new File(\"data.txt\")); while (in.hasNextLine()) …", "System.in.read()", "new File(\"data.txt\").read()", "Math.read(\"data.txt\")"),
        ("new Scanner(new File(…)) can throw:", "FileNotFoundException, a checked exception you must handle or declare", "Nothing", "ArithmeticException", "NullPointerException always"),
        ("line.split(\",\") on \"Ann,12,3.5\" gives:", "An array {\"Ann\", \"12\", \"3.5\"}", "A list of ints", "One String", "\"Ann12 3.5\""),
        ("To turn the field \"12\" into a number:", "Integer.parseInt(fields[1])", "(int) fields[1]", "fields[1].toInt()", "Math.int(fields[1])"),
    ], "Open, loop while there is input, split, convert, close")),
    ("PR-4.5.A", facts("pr-scanner-file-2", JL, [
        ("Mixing nextInt() and nextLine() often skips a line because:", "nextInt leaves the newline unread", "Files are binary", "nextLine is slow", "Of encoding"),
        ("A CSV header line should be:", "Read and skipped before the data loop", "Parsed as numbers", "Ignored by split", "Deleted from the file"),
        ("try (Scanner in = new Scanner(f)) { … } ensures:", "The file is closed even if an exception occurs", "Faster reading", "No exceptions", "The file is created"),
    ], "Handle headers, newlines and closing")),
    ("PR-4.5.B", J("pr-autobox", JL, [
        ("ArrayList<Integer> v = new ArrayList<>(List.of(10, 20, 30));\nv.remove(1);\nSystem.out.print(v);", ["[20, 30]", "[10, 20, 30]", "[10, 30, 20]"]),
        ("ArrayList<Integer> v = new ArrayList<>(List.of(10, 20, 30));\nv.remove(Integer.valueOf(10));\nSystem.out.print(v);", ["[10, 30]", "[10, 20]", "[10, 20, 30]"]),
        ("Integer n = null;\nint m = n;\nSystem.out.print(m);", ["0", "null", "An error"]),
        ("System.out.print(Integer.parseInt(\"12\") + \"3\");", ["15", "123.0", "NumberFormatException"])],
        "remove(int) removes by index; remove(Object) by value. Unboxing null throws NullPointerException")),
    ("PR-4.5.B", JN("pr-parse", JL, [
        "System.out.print(Integer.parseInt(\"7\") + Integer.parseInt(\"35\"));", "System.out.print(Double.parseDouble(\"2.5\") * 4);",
        "Integer a = 5;\nint b = a + 2;\nSystem.out.print(b * a);", "String s = \"40\";\nSystem.out.print(Integer.valueOf(s) / 3);"],
        "Parse text to numbers before arithmetic; autoboxing converts int ↔ Integer automatically")),
    ("PR-4.6.A", J("pr-arraylist-ops", JL, [
        ("ArrayList<String> v = new ArrayList<>();\nv.add(\"a\"); v.add(\"b\"); v.add(0, \"c\");\nv.set(1, \"d\");\nSystem.out.print(v);", ["[c, a, b]", "[a, d, b]", "[d, a, b]"]),
        ("ArrayList<String> v = new ArrayList<>(List.of(\"x\", \"y\", \"z\"));\nv.remove(0);\nv.add(\"w\");\nSystem.out.print(v + \" \" + v.size());", ["[x, y, w] 3", "[y, z, w] 4", "[w, y, z] 3"]),
        ("ArrayList<Integer> v = new ArrayList<>(List.of(4, 5, 6));\nv.add(1, v.get(2));\nSystem.out.print(v);", ["[4, 5, 6, 6]", "[4, 2, 5, 6]", "[6, 4, 5, 6]"])],
        "add(i, x) shifts later elements right; set replaces; remove shifts left; size changes with add and remove only")),
    ("PR-4.6.B", J("pr-remove-skip", JL, [
        ("ArrayList<Integer> v = new ArrayList<>(List.of(2, 4, 5, 6));\nfor (int k = 0; k < v.size(); k++) if (v.get(k) % 2 == 0) v.remove(k);\nSystem.out.print(v);", ["[5]", "[2, 4, 5, 6]", "[5, 6, 4]"]),
        ("ArrayList<Integer> v = new ArrayList<>(List.of(2, 4, 5, 6));\nfor (int k = v.size() - 1; k >= 0; k--) if (v.get(k) % 2 == 0) v.remove(k);\nSystem.out.print(v);", ["[4, 5]", "[2, 4, 5, 6]", "[5, 6]"]),
        ("ArrayList<Integer> v = new ArrayList<>(List.of(1, 1, 1));\nfor (int k = 0; k < v.size(); k++) if (v.get(k) == 1) v.remove(k);\nSystem.out.print(v);", ["[]", "[1, 1]", "[1, 1, 1]"])],
        "Removing at k shifts the next element into k, and k++ skips it. Loop backwards, or only advance when nothing was removed")),
    ("PR-4.7.A", JN("pr-jagged", JL, [
        "int[][] g = new int[3][5];\nSystem.out.print(g.length * 10 + g[0].length);", "int[][] g = {{1, 2}, {3, 4, 5}, {6}};\nSystem.out.print(g[1].length * 10 + g[1][2]);",
        "int[][] g = {{1, 2, 3}, {4, 5, 6}};\nSystem.out.print(g[1][0] + g[0][2]);", "int[][] g = new int[4][];\ng[2] = new int[7];\nSystem.out.print(g[2].length + g.length);"],
        "g.length counts rows; g[r].length counts the columns of row r, which may differ")),
    ("PR-4.7.B", J("pr-column-major", JL, [
        ("int[][] g = {{1, 2, 3}, {4, 5, 6}};\nfor (int c = 0; c < 3; c++)\n  for (int r = 0; r < 2; r++) System.out.print(g[r][c]);", ["123456", "321654", "654321"]),
        ("int[][] g = {{1, 2}, {3, 4}, {5, 6}};\nfor (int r = g.length - 1; r >= 0; r--)\n  for (int c = 0; c < 2; c++) System.out.print(g[r][c]);", ["123456", "654321", "135246"]),
        ("int[][] g = {{1, 2}, {3, 4}};\nfor (int[] row : g)\n  for (int v : row) System.out.print(v * 2);", ["1234", "2468 ", "4826"])],
        "The outer loop chooses what changes slowly: rows for row-major, columns for column-major")),
    ("PR-4.7.C", JN("pr-diag-sum", JL, [
        "int[][] g = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};\nint s = 0;\nfor (int k = 0; k < 3; k++) s += g[k][k];\nSystem.out.print(s);",
        "int[][] g = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};\nint s = 0;\nfor (int k = 0; k < 3; k++) s += g[k][2 - k];\nSystem.out.print(s);",
        "int[][] g = {{1, 2, 3}, {4, 5, 6}};\nint s = 0;\nfor (int r = 0; r < 2; r++) s += g[r][1];\nSystem.out.print(s);",
        "int[][] g = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};\nint r = 0, c = 2, n = 0;\nfor (int dr = -1; dr <= 1; dr++) for (int dc = -1; dc <= 1; dc++) {\n  int rr = r + dr, cc = c + dc;\n  if ((dr != 0 || dc != 0) && rr >= 0 && rr < 3 && cc >= 0 && cc < 3) n += g[rr][cc];\n}\nSystem.out.print(n);"],
        "Main diagonal g[k][k]; anti-diagonal g[k][n − 1 − k]; a column fixes c; neighbours need bounds checks")),
    ("PR-4.8.A", Q("pr-linear-compares", JA, "Linear search for {{t}} in [{{arr}}] compares from the left. How many comparisons does it make?",
        cases=[{"arr": "4, 8, 15, 16, 23, 42", "t": t, "code": f"a = [4, 8, 15, 16, 23, 42]\nc = 0\nfor v in a:\n    c += 1\n    if v == {t}: break\nprint(c)"} for t in (4, 16, 42, 99)],
        value="ans", tex="c", final=True, verify="py_out(code)", explain="Best case 1 (first element); worst case n (last element or absent)")),
    ("PR-4.8.A", facts("pr-linear-facts", JA, [
        ("Linear search on an unsorted array of n items, worst case:", "n comparisons", "log₂ n", "1", "n²"),
        ("Average comparisons for a present key at a uniformly random position:", "About n/2", "n", "1", "log n"),
        ("Linear search works on:", "Any array, sorted or not", "Sorted arrays only", "Arrays of numbers only", "Linked lists only"),
    ], "Check one by one until found or done")),
    ("PR-4.8.B", Q("pr-bsearch-max", JA, "At most how many iterations does binary search take on a sorted array of n = {{n}} elements?",
        given={"n": {"pick": [8, 100, 1000, 1000000]}}, value="floor(log2(n)) + 1", tex="k", final=True, verify="floor(log(n, 2)) + 1",
        explain="Each iteration halves the range: ⌊log₂ n⌋ + 1 iterations in the worst case")),
    ("PR-4.9.A", JN("pr-selection-swaps", JA, [
        "int[] a = {5, 1, 4, 2, 3};\nint sw = 0;\nfor (int i = 0; i < a.length - 1; i++) {\n  int m = i;\n  for (int k = i + 1; k < a.length; k++) if (a[k] < a[m]) m = k;\n  if (m != i) { int t = a[i]; a[i] = a[m]; a[m] = t; sw++; }\n}\nSystem.out.print(sw);",
        "int[] a = {4, 3, 2, 1};\nint sw = 0;\nfor (int i = 0; i < a.length - 1; i++) {\n  int m = i;\n  for (int k = i + 1; k < a.length; k++) if (a[k] < a[m]) m = k;\n  if (m != i) { int t = a[i]; a[i] = a[m]; a[m] = t; sw++; }\n}\nSystem.out.print(sw);",
        "int[] a = {2, 1, 4, 3};\nint sw = 0;\nfor (int i = 0; i < a.length - 1; i++) {\n  int m = i;\n  for (int k = i + 1; k < a.length; k++) if (a[k] < a[m]) m = k;\n  if (m != i) { int t = a[i]; a[i] = a[m]; a[m] = t; sw++; }\n}\nSystem.out.print(sw);"],
        "Selection sort makes at most n − 1 swaps, one per pass, skipping passes whose minimum is already in place")),
    ("PR-4.9.B", Q("pr-insertion-worst", JA, "How many comparisons does insertion sort make on a {{kind}} array of {{n}} distinct elements?",
        cases=[{"kind": "reverse-sorted", "kk": 1, "n": n} for n in (5, 10, 20)] + [{"kind": "already sorted", "kk": 0, "n": n} for n in (5, 20)],
        value="kk == 1 ? n*(n - 1)/2 : n - 1", tex="c", final=True, verify="binomial(n, 2) if kk == 1 else n - 1",
        explain="Sorted input: one comparison per element. Reverse: each element walks all the way back")),
    ("PR-4.10.A", J("pr-recursion-order", JA, [
        ("f(3);", ["123", "3", "321123"]), ("g(3);", ["321", "3", "123321"]), ("h(3);", ["123321", "333", "321"])],
        "Work before the recursive call happens on the way down; work after it happens on the way back up",
        defs="static void f(int n) { if (n == 0) return; System.out.print(n); f(n - 1); }\nstatic void g(int n) { if (n == 0) return; g(n - 1); System.out.print(n); }\nstatic void h(int n) { if (n == 0) return; System.out.print(n); h(n - 1); System.out.print(n); }")),
    ("PR-4.10.B", JN("pr-pow-calls", JA, ["calls = 0;\npow(2, 8);\nSystem.out.print(calls);", "calls = 0;\npow(2, 16);\nSystem.out.print(calls);",
        "calls = 0;\nslow(2, 8);\nSystem.out.print(calls);", "calls = 0;\npow(3, 5);\nSystem.out.print(calls);"],
        "Halving the exponent gives about log₂ n calls; subtracting one gives n calls",
        defs="static int calls = 0;\nstatic long pow(long b, int n) {\n  calls++;\n  if (n == 0) return 1;\n  long h = pow(b, n / 2);\n  return n % 2 == 0 ? h * h : h * h * b;\n}\nstatic long slow(long b, int n) {\n  calls++;\n  return n == 0 ? 1 : b * slow(b, n - 1);\n}")),
    ("PR-4.10.C", J("pr-base-case", JA, [
        ("System.out.print(sumTo(3));", ["6", "3", "0"]), ("System.out.print(down(3));", ["StackOverflowError", "0", "3"]), ("System.out.print(odd(4));", ["true", "false", "0"])],
        "Every path must reach a base case: sumTo has none, odd(4) skips n == 1 by stepping by 2, down(3) is fine",
        defs="static int sumTo(int n) { return n + sumTo(n - 1); }\nstatic int down(int n) { return n == 0 ? 0 : n + down(n - 1); }\nstatic boolean odd(int n) { return n == 1 ? true : odd(n - 2); }")),
    ("PR-4.10.C", facts("pr-base-case-facts", JA, [
        ("A StackOverflowError from recursion usually means:", "A base case is missing or never reached", "The array is too small", "Integer overflow", "A syntax error"),
        ("fact(n) = n * fact(n − 1) with base case n == 0, called as fact(−1):", "Never reaches the base case", "Returns 1", "Returns −1", "Returns 0"),
        ("A safe base case for a method that counts down by 2 is:", "n <= 0", "n == 0", "n == 1", "n == −1"),
    ], "Base cases must catch every input the recursion can produce")),
    ("PR-4.10.D", Q("pr-merge-levels", JA, "Merge sort on n = {{n}} elements (n a power of 2) splits down to single elements. How many levels of splitting are there?",
        given={"n": {"pick": [8, 16, 64, 1024]}}, value="log2(n)", tex="L", final=True, verify="log(n, 2)",
        explain="Each level halves the subarrays; each level's merges do Θ(n) work, so Θ(n log n) in all")),
    ("PR-4.10.D", facts("pr-merge-trace", JA, [
        ("Merge sort on [8, 3, 5, 1] first splits into:", "[8, 3] and [5, 1]", "[8] and [3, 5, 1]", "[1, 3] and [5, 8]", "[8, 5] and [3, 1]"),
        ("After merging [8, 3] and [5, 1] at the bottom level, the halves are:", "[3, 8] and [1, 5]", "[8, 3] and [5, 1]", "[1, 3] and [5, 8]", "[3, 5] and [1, 8]"),
        ("Recursive binary search for 7 in [1, 3, 5, 7, 9, 11] (mid = (lo + hi)/2) first looks at index:", "2 (value 5)", "3 (value 7)", "0", "5"),
        ("Merging [1, 5] and [3, 8] makes how many comparisons?", "3", "4", "2", "1"),
    ], "Split until size 1, then merge back up")),
    # ── 5 shell ───────────────────────────────────────────────────────────────────────────────────────────────────
    ("PR-5.1.A", SH("pr-sh-relpath", SHL, "Starting in your home directory (~), which holds data/raw, data/clean and code, what does this print?", [
        ("mkdir -p data/raw data/clean code", "cd code\nls ../data", ["raw", "clean raw", "code"]),
        ("mkdir -p data/raw data/clean code", "cd data/raw\nls -d ../../c*", ["code", "../clean", "../../clean"]),
        ("mkdir -p data/raw data/clean code; touch data/raw/a.csv", "cd data/clean\nls ../raw", ["raw", "../raw/a.csv", "clean"])],
        ".. is the parent; relative paths start from the current directory")),
    ("PR-5.1.B", SH("pr-sh-ls-flags", SHL, "A directory holds a.txt, .hidden and a subdirectory d. What does this print?", [
        ("touch a.txt .hidden; mkdir d", "ls", ["a.txt d .hidden", "a.txt", ". .. .hidden a.txt d"]),
        ("touch a.txt .hidden; mkdir d", "ls -a", ["a.txt d", ".hidden a.txt d", "a.txt d .hidden"]),
        ("touch a.txt .hidden; mkdir d", "ls -F", ["a.txt d", "a.txt d/ .hidden", "a.txt* d/"])],
        "ls hides dot files; -a shows them (with . and ..); -F marks directories with /")),
    ("PR-5.2.A", SHN("pr-sh-count-files", SHL, "Starting in an empty directory, how many entries does the last command print?", [
        ("", "mkdir a b\ntouch a/x b/y\ncp a/x b/\nls b | wc -l"), ("", "touch x y z\nmv x y\nls | wc -l"),
        ("", "mkdir d\ntouch d/f1 d/f2\nrm d/f1\nls d | wc -l"), ("", "touch a\ncp a b\nmv b c\nls | wc -l")],
        "mv onto an existing file replaces it; cp keeps the original; rm deletes")),
    ("PR-5.2.B", SHN("pr-sh-glob-count", SHL, "The directory holds a1.txt a2.txt b1.txt b10.txt notes.md. How many names does the pattern match?", [
        ("touch a1.txt a2.txt b1.txt b10.txt notes.md", "ls b?.txt | wc -l"), ("touch a1.txt a2.txt b1.txt b10.txt notes.md", "ls *1*.txt | wc -l"),
        ("touch a1.txt a2.txt b1.txt b10.txt notes.md", "ls *.* | wc -l"), ("touch a1.txt a2.txt b1.txt b10.txt notes.md", "ls [ab]?.txt | wc -l")],
        "* matches any run of characters, ? exactly one, [ab] one of the set")),
    ("PR-5.3.A", SHN("pr-sh-filter-num", SHL, "lengths.txt holds the lines 21 methane, 9 ethane, 30 propane, 12 cubane, 21 methane. What does this print?", [
        ("printf '21 methane\\n9 ethane\\n30 propane\\n12 cubane\\n21 methane\\n' > lengths.txt", "sort -n lengths.txt | head -1 | cut -d ' ' -f 1"),
        ("printf '21 methane\\n9 ethane\\n30 propane\\n12 cubane\\n21 methane\\n' > lengths.txt", "sort lengths.txt | uniq | wc -l"),
        ("printf '21 methane\\n9 ethane\\n30 propane\\n12 cubane\\n21 methane\\n' > lengths.txt", "sort lengths.txt | head -1 | cut -d ' ' -f 1"),
        ("printf '21 methane\\n9 ethane\\n30 propane\\n12 cubane\\n21 methane\\n' > lengths.txt", "sort -rn lengths.txt | head -2 | tail -1 | cut -d ' ' -f 1")],
        "sort is alphabetical unless -n; uniq only merges adjacent duplicates, so sort first")),
    ("PR-5.3.B", SHN("pr-sh-redirect-count", SHL, "Starting in an empty directory, what does the last command print?", [
        ("", "echo a > f\necho b > f\nwc -l < f"), ("", "echo a > f\necho b >> f\nwc -l < f"), ("", "echo a >> f\necho b >> f\necho c > f\nwc -l < f"),
        ("", "printf 'x\\ny\\nz\\n' > f\ngrep -v y f > g\nwc -l < g")],
        "> truncates then writes; >> appends; < feeds a file to standard input")),
    ("PR-5.4.A", SH("pr-sh-for-loop", SHL, "The directory holds a.csv and b.csv. What does this print?", [
        ("touch a.csv b.csv", "for f in *.csv; do echo $f; done", ["*.csv", "a.csv b.csv", "f / f"]),
        ("touch a.csv b.csv", "for f in *.csv; do echo ${f%.csv}.txt; done", ["a.csv.txt / b.csv.txt", "a.txt b.txt", "*.txt"]),
        ("touch a.csv b.csv", "for f in *.csv; do echo f; done", ["a.csv / b.csv", "f", "*.csv"]),
        ("touch a.csv b.csv", "n=0; for f in *.csv; do n=$((n+1)); done; echo $n", ["0", "1", "a.csv b.csv"])],
        "The glob expands before the loop; the variable needs its dollar sign (plain f is just the letter); the %-form of expansion strips a suffix")),
    ("PR-5.4.A", facts("pr-sh-quoting", SHL, [
        ("A loop runs wc -l on each .csv file, passing the loop variable unquoted. A file named 'my data.csv' fails because:", "The unquoted variable splits into two words", "wc can't read CSV", "The loop is wrong", "It doesn't fail"),
        ("The fix is to:", "Put the variable in double quotes", "Put it in single quotes", "Remove the dollar sign", "Use a semicolon"),
        ("A variable inside single quotes is:", "Printed literally, not expanded", "Expanded", "An error", "Deleted"),
        ("A variable inside double quotes is:", "Expanded, with its spaces kept as one word", "Printed literally", "Split on spaces", "An error"),
    ], "Double quotes expand variables but keep spaces; single quotes expand nothing")),
    ("PR-5.4.B", Q("pr-sh-args", SHL, "script.sh holds the one line shown first. What does the command print?",
        cases=[{"setup": "printf 'echo \"$# $1\"\\n' > script.sh", "cmds": cm, "show": "# script.sh\necho \"$# $1\"\n\n" + cm,
                **_opts(PC._show(PC.sh_run("printf 'echo \"$# $1\"\\n' > script.sh", cm)), w, "pr-sh-args")}
               for cm, w in [("bash script.sh a b c", ["3 a b c", "a 3", "1 a"]), ("bash script.sh \"a b\" c", ["3 a", "2 a", "1 a b"]), ("bash script.sh", ["1", "0 script.sh", "a"])]],
        choice=MC, correct="0", verify="sh_pick(setup, cmds, [o1, o2, o3, o4])", figure=SHOW,
        explain="The script prints the argument count and then the first argument; quotes group words into one argument")),
    ("PR-5.4.B", facts("pr-sh-args-facts", SHL, [
        ("Looping over the quoted all-arguments parameter (dollar-at in quotes) visits:", "Each argument, keeping spaces inside arguments", "Each word of all arguments joined", "Only the first argument", "Files in the directory"),
        ("Inside a script, parameter 0 (dollar-zero) holds:", "The script's name", "The first argument", "The argument count", "The exit status"),
        ("The dollar-question-mark parameter holds:", "The exit status of the last command", "The argument count", "The PID", "The first argument"),
    ], "Positional parameters carry arguments")),
    ("PR-5.4.C", facts("pr-sh-exec", SHL, [
        ("./run.sh gives 'Permission denied'. Fix:", "chmod +x run.sh", "sudo rm run.sh", "Rename it run.txt", "Add a comment"),
        ("run.sh gives 'command not found' but ./run.sh works because:", "The current directory isn't on PATH", "The file is empty", "chmod is missing", "Bash is broken"),
        ("The first line #!/bin/bash in a script:", "Names the interpreter to run it with", "Is a comment with no effect", "Makes it executable", "Is required by ls"),
        ("bash run.sh runs a script even without execute permission because:", "bash reads the file itself as input", "It changes permissions", "It is root", "It can't"),
    ], "Executable bit, shebang, and PATH decide how a script runs")),
    ("PR-5.4.C", SHN("pr-sh-exec-check", SHL, "In a fresh directory, what does this print (1 if the file is executable, else 0)?", [
        ("printf 'echo hi\\n' > run.sh", "[ -x run.sh ] && echo 1 || echo 0"), ("printf 'echo hi\\n' > run.sh", "chmod +x run.sh\n[ -x run.sh ] && echo 1 || echo 0"),
        ("printf 'echo hi\\n' > run.sh", "chmod 644 run.sh\n[ -x run.sh ] && echo 1 || echo 0"), ("printf 'echo hi\\n' > run.sh", "chmod 755 run.sh\n[ -x run.sh ] && echo 1 || echo 0")],
        "New files are not executable; chmod +x or a mode with x for the user adds it")),
    ("PR-5.5.A", SHN("pr-sh-grep-count", SHL, "notes.txt holds: Error one / warning / error two / ERRORS / ok. What does this print?", [
        ("printf 'Error one\\nwarning\\nerror two\\nERRORS\\nok\\n' > notes.txt", "grep -c error notes.txt"),
        ("printf 'Error one\\nwarning\\nerror two\\nERRORS\\nok\\n' > notes.txt", "grep -ic error notes.txt"),
        ("printf 'Error one\\nwarning\\nerror two\\nERRORS\\nok\\n' > notes.txt", "grep -iwc error notes.txt"),
        ("printf 'Error one\\nwarning\\nerror two\\nERRORS\\nok\\n' > notes.txt", "grep -vc error notes.txt")],
        "-i ignores case, -w needs a whole word, -v inverts, -c counts matching lines")),
    ("PR-5.5.B", SHN("pr-sh-find-count", SHL, "The tree holds a.txt, data/one.txt, data/two.csv, data/old/three.txt. What does this print?", [
        ("mkdir -p data/old; touch a.txt data/one.txt data/two.csv data/old/three.txt", "find . -name '*.txt' | wc -l"),
        ("mkdir -p data/old; touch a.txt data/one.txt data/two.csv data/old/three.txt", "find . -maxdepth 2 -name '*.txt' | wc -l"),
        ("mkdir -p data/old; touch a.txt data/one.txt data/two.csv data/old/three.txt", "find . -type d | wc -l"),
        ("mkdir -p data/old; touch a.txt data/one.txt data/two.csv data/old/three.txt", "find data -type f | wc -l")],
        "find walks the whole tree; -maxdepth limits it; -type d counts directories including the start")),
    # ── 6 git ─────────────────────────────────────────────────────────────────────────────────────────────────────
    ("PR-6.1.A", facts("pr-git-why", GIT, [
        ("A commit records:", "A snapshot of the tracked files, with author, time, message and parent", "Only the changed lines, with no history", "A zip of the folder", "Nothing until pushed"),
        ("Compared with thesis_final_v2.docx copies, Git gives:", "A history you can compare, annotate and restore precisely", "Bigger files", "Nothing", "Automatic writing"),
        ("A good commit message says:", "What changed and why, in a short summary line", "'stuff'", "The date only", "Nothing"),
        ("A commit's hash:", "Identifies it uniquely from its content and history", "Is random", "Is its date", "Is the author"),
    ], "Commits are labelled snapshots")),
    ("PR-6.1.A", facts("pr-git-why-2", GIT, [
        ("Small, focused commits make it easier to:", "Find and revert the change that broke something", "Hide work", "Push faster", "Avoid branches"),
        ("git commit with no staged changes:", "Does nothing (nothing to commit)", "Commits everything", "Deletes files", "Pushes"),
        ("The staging area lets you:", "Choose which changes go into the next commit", "Undo commits", "Merge branches", "Share code"),
    ], "Stage deliberately, commit often")),
    ("PR-6.1.B", SH("pr-git-status-2", GIT, "A repository tracks a.txt, committed and unchanged. After these commands, what does git status --short print?", [
        (GIT1, "rm a.txt\ngit status --short", [" M a.txt", "D  a.txt", "?? a.txt"]),
        (GIT1, "git rm -q a.txt\ngit status --short", [" D a.txt", "?? a.txt", " M a.txt"]),
        (GIT1, "git mv a.txt b.txt\ngit status --short", ["?? b.txt", " D a.txt", "A  b.txt"]),
        (GIT1, "echo x >> a.txt\ngit add a.txt\ngit restore --staged a.txt\ngit status --short", ["M  a.txt", "MM a.txt", "?? a.txt"])],
        "Column 1 is staged, column 2 unstaged: D deleted, R renamed, M modified")),
    ("PR-6.2.A", SHN("pr-git-log-count", GIT, "After these commands, what does the last command print?", [
        (GIT1, "echo b > b; git add b; git commit -qm two\necho c > c; git add c; git commit -qm three\ngit log --oneline | wc -l"),
        (GIT1, "echo b > b; git add b; git commit -qm two\necho c > c; git add c; git commit -qm three\ngit log --oneline HEAD~1 | wc -l"),
        (GIT1, "echo b > b; git add b; git commit -qm two\necho c > c; git add c; git commit -qm three\ngit diff --name-only HEAD~2 HEAD | wc -l"),
        (GIT1, "echo b > b; git add b; git commit -qm two\necho more >> a.txt\ngit diff --name-only | wc -l")],
        "HEAD~n is n commits back; git diff with no arguments shows unstaged changes; diff A B lists what changed between commits")),
    ("PR-6.2.A", facts("pr-git-names", GIT, [
        ("HEAD~1 names:", "The parent of the current commit", "The first commit", "The next commit", "The remote"),
        ("A commit can be named by:", "A unique prefix of its hash, e.g. 3f2a9c1", "Its message only", "Its date only", "Its size"),
        ("git diff --staged shows:", "Changes staged for the next commit", "Unstaged changes", "All history", "Remote changes"),
        ("git log --oneline shows:", "One line per commit: short hash and subject", "Only the latest commit", "File contents", "Branches only"),
    ], "Name commits by relation or hash")),
    ("PR-6.2.B", facts("pr-git-undo-pick", GIT, [
        ("Discard uncommitted edits to a.txt in the working tree:", "git restore a.txt", "git revert a.txt", "git reset --hard HEAD~5", "git rm a.txt"),
        ("Unstage a.txt but keep the edits:", "git restore --staged a.txt", "git restore a.txt", "git rm a.txt", "git commit --amend"),
        ("Undo a pushed commit safely:", "git revert <hash>", "git reset --hard", "Delete .git", "git rebase -i on main"),
        ("Fix the message of the last commit, not yet pushed:", "git commit --amend", "git revert", "git restore", "git rm"),
    ], "Match the command to where the change lives: working tree, staging area, or history")),
    ("PR-6.3.A", SH("pr-git-ignore-2", GIT, "A repository holds data.csv, run.py and results/out.csv. With this .gitignore, what does git status --short --untracked-files=all list?", [
        ("git init -q .; mkdir results; touch data.csv run.py results/out.csv", "printf '*.csv\\n' > .gitignore\ngit status --short --untracked-files=all | grep -v gitignore", ["?? data.csv / ?? run.py", "?? results/out.csv / ?? run.py", "?? run.py / ?? results/out.csv / ?? data.csv"]),
        ("git init -q .; mkdir results; touch data.csv run.py results/out.csv", "printf 'results/\\n' > .gitignore\ngit status --short --untracked-files=all | grep -v gitignore", ["?? run.py", "?? data.csv", "?? results/out.csv / ?? run.py"]),
        ("git init -q .; mkdir results; touch data.csv run.py results/out.csv", "printf '*.csv\\n!data.csv\\n' > .gitignore\ngit status --short --untracked-files=all | grep -v gitignore", ["?? run.py", "?? data.csv / ?? results/out.csv / ?? run.py", "?? results/out.csv / ?? run.py"])],
        "Patterns apply at any depth; a trailing / matches a directory; ! re-includes a file a later pattern excluded")),
    ("PR-6.3.B", facts("pr-repo-hygiene", GIT, [
        ("An API key committed by mistake should be:", "Revoked and rotated (deleting it in a later commit isn't enough)", "Left alone", "Renamed", "Commented out"),
        ("A 5 GB raw instrument file belongs:", "Outside the repo (archive or LFS), with a pointer and checksum", "In the repo", "In the commit message", "In .gitignore only, then lost"),
        ("Generated outputs (figures, compiled code) should usually be:", "Ignored and regenerated from the code", "Committed every time", "Emailed", "Deleted"),
        ("A LICENSE file tells others:", "What they may do with the code", "Who wrote each line", "How to install", "Nothing"),
        ("A CITATION.cff file:", "Tells others how to cite the software", "Licenses it", "Ignores files", "Builds it"),
    ], "Commit sources, not secrets or bulk data")),
    ("PR-6.3.B", facts("pr-repo-hygiene-2", GIT, [
        ("A README should explain:", "What the project does and how to run it", "Only the author", "The git history", "Nothing"),
        ("Without a licence, others may:", "Not legally reuse your code (all rights reserved)", "Do anything", "Only read it once", "Sell it"),
        (".env files with passwords should be:", "In .gitignore, with a template (.env.example) committed", "Committed", "Printed in the README", "Encrypted in the message"),
    ], "A repository is a publication")),
    ("PR-6.4.A", SHN("pr-git-remote-count", GIT, "A bare repository 'origin' and two clones are set up. How many commits does the last command count?", [
        ("git init -q --bare origin.git; git clone -q origin.git a 2>/dev/null; cd a; echo x > x; git add x; git commit -qm one; git push -q origin HEAD:main 2>/dev/null; cd ..",
         "git clone -q -b main origin.git b 2>/dev/null\ncd a\necho y > y; git add y; git commit -qm two\ncd ../b\ngit rev-list --count HEAD"),
        ("git init -q --bare origin.git; git clone -q origin.git a 2>/dev/null; cd a; echo x > x; git add x; git commit -qm one; git push -q origin HEAD:main 2>/dev/null; cd ..",
         "git clone -q -b main origin.git b 2>/dev/null\ncd a\necho y > y; git add y; git commit -qm two\ngit push -q origin HEAD:main 2>/dev/null\ncd ../b\ngit pull -q origin main 2>/dev/null\ngit rev-list --count HEAD"),
        ("git init -q --bare origin.git; git clone -q origin.git a 2>/dev/null; cd a; echo x > x; git add x; git commit -qm one; git push -q origin HEAD:main 2>/dev/null; cd ..",
         "cd a\necho y > y; git add y; git commit -qm two\necho z > z; git add z; git commit -qm three\ncd ..\ngit --git-dir=origin.git rev-list --count main")],
        "Commits stay local until pushed; another clone sees them only after it pulls")),
    ("PR-6.4.A", facts("pr-git-remote", GIT, [
        ("git push is rejected as non-fast-forward. Usually you should:", "Pull (fetch and merge or rebase), then push", "Force-push to main", "Delete the remote", "Re-clone"),
        ("git fetch:", "Downloads remote commits without changing your branch", "Merges them", "Pushes", "Deletes local work"),
        ("git clone gives you:", "The full history and a remote named origin", "Only the latest files", "Only one branch's last commit", "Nothing until pull"),
    ], "Local and remote repositories sync only on push, fetch and pull")),
    ("PR-6.5.A", SHN("pr-git-branch-count", GIT, "After these commands, what does the last command print?", [
        (GIT1, "git switch -q -c feat\necho f > f; git add f; git commit -qm f\ngit switch -q -\ngit rev-list --count HEAD"),
        (GIT1, "git switch -q -c feat\necho f > f; git add f; git commit -qm f\ngit rev-list --count HEAD"),
        (GIT1, "git switch -q -c feat\necho f > f; git add f; git commit -qm f\ngit switch -q -\ngit merge -q feat\ngit rev-list --count HEAD"),
        (GIT1, "git switch -q -c feat\necho f > f; git add f; git commit -qm f\ngit switch -q -\necho m > m; git add m; git commit -qm m\ngit merge -q --no-edit feat\ngit rev-list --count HEAD")],
        "A branch is a pointer; commits made on it don't appear on main until merged. A fast-forward adds no merge commit")),
    ("PR-6.5.B", facts("pr-conflict", GIT, [
        ("Between <<<<<<< HEAD and ======= you see:", "Your current branch's version", "The incoming branch's version", "The common ancestor", "Nothing"),
        ("Between ======= and >>>>>>> feat you see:", "The incoming branch's version", "Your version", "The ancestor", "Git's suggestion"),
        ("To finish resolving a conflict in a.txt:", "Edit the file to the intended text, remove the markers, git add a.txt, then commit", "Delete the file", "git push", "git reset --hard"),
        ("Git reports a conflict when:", "Both branches changed the same lines differently", "Any file changed", "Branches have different names", "Files are large"),
    ], "Markers show both sides; you decide the result")),
    ("PR-6.5.B", facts("pr-conflict-2", GIT, [
        ("The intended result keeps both added lines. You should:", "Keep both lines in the right order and delete all markers", "Keep only HEAD", "Keep only the incoming side", "Leave the markers"),
        ("git merge --abort:", "Returns to the state before the merge started", "Commits the conflict", "Deletes the branch", "Pushes"),
        ("Committing a file that still contains <<<<<<< markers:", "Is allowed by git but breaks the file", "Is impossible", "Resolves it", "Deletes the markers"),
    ], "Resolve, test, then commit")),
    # ── 7 python ──────────────────────────────────────────────────────────────────────────────────────────────────
    ("PR-7.1.A", PN("pr-java-to-py", PY, [
        "def total(xs):\n    s = 0\n    for x in xs:\n        if x > 0:\n            s += x\n    return s\nprint(total([3, -1, 4, -1, 5]))",
        "def count_even(n):\n    c = 0\n    for k in range(1, n + 1):\n        if k % 2 == 0:\n            c += 1\n    return c\nprint(count_even(9))",
        "def fact(n):\n    r = 1\n    while n > 1:\n        r *= n\n        n -= 1\n    return r\nprint(fact(5))"],
        "Blocks are indentation; no types or semicolons; for k in range(a, b) runs a … b − 1",
        prompt="This Python is a translation of a short Java method. What does it print?")),
    ("PR-7.1.A", facts("pr-java-py", PY, [
        ("Java's for (int k = 0; k < n; k++) in Python is:", "for k in range(n):", "for k = 0 to n:", "for (k in n):", "while k < n: k++"),
        ("Java's && and || in Python are:", "and, or", "&&, ||", "&, |", "both, either"),
        ("Java's System.out.println(x) in Python is:", "print(x)", "echo(x)", "System.print(x)", "printf(x)"),
        ("A Python block ends:", "When the indentation returns to the outer level", "At a }", "At end", "At a semicolon"),
        ("Java's x++ in Python is:", "x += 1", "x++", "++x", "inc(x)"),
    ], "Same ideas, different syntax")),
    ("PR-7.1.B", PN("pr-py-mixed", PY, ["print(7 // 2 * 2.0)", "print(2 ** -1)", "print(-7 // 2 + -7 % 2)", "print(10 / 5)", "print(round(2.5) + round(3.5))"],
        "/ always gives a float; // floors toward −∞ (Java truncates toward 0); round() rounds halves to even", final=False)),
    ("PR-7.1.C", P("pr-py-chain", PY, [
        ("print(1 < 2 < 3, 3 > 2 > 2)", ["True True", "False False", "An error"]), ("print(not 0, not '')", ["False False", "0 ''", "An error"]),
        ("print([] or None)", ["[]", "False", "An error"]), ("print(5 > 3 == True)", ["True", "An error", "1"])],
        "Chained comparisons mean a < b and b < c; and/or return an operand, not necessarily a bool")),
    ("PR-7.2.A", PN("pr-py-range-len", PY, ["print(len(range(3, 20, 4)))", "print(len(range(10, 0, -3)))", "print(sum(range(1, 11, 2)))", "print(len(range(5, 5)))"],
        "range(start, stop, step) stops before stop; the count is ⌈(stop − start)/step⌉, or 0")),
    ("PR-7.2.B", P("pr-py-zip", PY, [
        ("for k, c in enumerate('ab', 1):\n    print(k, c, end=' ')", ["0 a 1 b", "a 1 b 2", "1 2"]),
        ("print(list(zip([1, 2, 3], 'xy')))", ["[(1, 'x'), (2, 'y'), (3, None)]", "[1, 'x', 2, 'y']", "An error"]),
        ("for v in [1, 2, 3, 4]:\n    if v == 3:\n        continue\n    print(v, end='')", ["1234", "12", "4"]),
        ("for v in [1, 2, 3]:\n    if v == 2:\n        break\nelse:\n    print('done', end='')\nprint(v)", ["done3", "done2", "3"])],
        "enumerate pairs indices with items; zip stops at the shortest; a loop's else runs only if no break happened")),
    ("PR-7.3.A", P("pr-py-slice-str", PY, [
        ("print('chemistry'[2:5])", ["hemi", "che", "mis"]), ("print('chemistry'[::-1][:3])", ["che", "rts", "yrtsimehc"]),
        ("print('chemistry'[-3:])", ["che", "try ", "ist"]), ("print([1, 2, 3, 4, 5][1::2])", ["[1, 3, 5]", "[2, 3]", "[4, 2]"])],
        "s[a:b] takes a up to b − 1; negative indices count from the end; a step of −1 reverses")),
    ("PR-7.3.B", P("pr-py-sort-none", PY, [
        ("xs = [3, 1, 2]\nys = xs.sort()\nprint(ys)", ["[1, 2, 3]", "[3, 1, 2]", "An error"]),
        ("xs = [3, 1, 2]\nys = sorted(xs)\nprint(xs, ys)", ["[1, 2, 3] [1, 2, 3]", "[3, 1, 2] None", "None [1, 2, 3]"]),
        ("xs = [1, 2]\nxs.append([3, 4])\nprint(len(xs))", ["4", "2", "An error"]),
        ("xs = [5, 6, 7]\nv = xs.pop(0)\nxs.remove(7)\nprint(v, xs)", ["7 [5, 6]", "5 [6, 7]", "0 [6]"])],
        "list.sort() sorts in place and returns None; sorted() returns a new list. append adds one item; extend adds each")),
    ("PR-7.3.C", P("pr-py-grid-alias", PY, [
        ("g = [[0] * 2] * 2\ng[0][0] = 1\nprint(g)", ["[[1, 0], [0, 0]]", "[[1, 1], [1, 1]]", "An error"]),
        ("g = [[0] * 2 for _ in range(2)]\ng[0][0] = 1\nprint(g)", ["[[1, 0], [1, 0]]", "[[1, 1], [0, 0]]", "An error"]),
        ("a = [[1], [2]]\nb = a[:]\nb[0].append(9)\nprint(a)", ["[[1], [2]]", "[[1], [2], [9]]", "An error"]),
        ("import copy\na = [[1], [2]]\nb = copy.deepcopy(a)\nb[0].append(9)\nprint(a)", ["[[1, 9], [2]]", "[[1], [2], 9]", "An error"])],
        "[row] * n repeats one reference; a slice copies the outer list only; deepcopy copies all levels")),
    ("PR-7.3.D", PN("pr-py-comp-sum", PY, ["print(sum([k * k for k in range(5) if k % 2 == 0]))", "print(len([c for c in 'banana' if c in 'an']))",
        "print(sum(len(w) for w in 'to be or not'.split() if len(w) > 2))", "print(max([x - y for x in [1, 5] for y in [2, 3]]))"],
        "[expr for v in seq if cond]: filter first, then transform; two for clauses nest left to right")),
    ("PR-7.4.A", PN("pr-py-dict-count", PY, [
        "d = {}\nfor w in 'a b a c b a'.split():\n    d[w] = d.get(w, 0) + 1\nprint(d['a'])", "d = {'x': 1, 'y': 2}\nd['x'] = 5\nd['z'] = 3\ndel d['y']\nprint(sum(d.values()))",
        "d = {k: k * k for k in range(4)}\nprint(d[3] + len(d))", "d = {'a': 1}\nprint(d.get('b', 10) + d.get('a', 10))"],
        "d.get(k, default) avoids a KeyError; assigning to an existing key replaces its value")),
    ("PR-7.4.B", P("pr-py-fstring", PY, [
        ("print(f'{3.14159:.2f}')", ["3.14159", "3.1", "3.142"]), ("print(f'{7:03d}|{2/3:.1%}')", ["7|0.67", "007|0.67%", "7|66.7%"]),
        ("print(' a,b '.strip().split(','))", ["[' a', 'b ']", "['a,b']", "['a', 'b', '']"]), ("print('-'.join('abc').upper())", ["ABC", "a-b-c", "-A-B-C-"])],
        "Format specs: .2f fixed decimals, 03d zero-padding, .1% percent; strip trims ends; join puts the separator between items")),
    ("PR-7.5.A", P("pr-py-default-mutable", PY, [
        ("def add(v, xs=[]):\n    xs.append(v)\n    return xs\nadd(1)\nprint(add(2))", ["[2]", "[1]", "An error"]),
        ("def add(v, xs=None):\n    xs = [] if xs is None else xs\n    xs.append(v)\n    return xs\nadd(1)\nprint(add(2))", ["[1, 2]", "None", "An error"]),
        ("def f(a, b=2, *, c=3):\n    return a + b * c\nprint(f(1, c=10))", ["9", "7", "An error"]),
        ("def f(x):\n    if x > 0:\n        return x\nprint(f(-1))", ["0", "-1", "An error"])],
        "Default values are evaluated once, so a mutable default is shared between calls; a function that falls off the end returns None")),
    ("PR-7.5.B", P("pr-py-main-guard", PY, [
        ("print(__name__)", ["main", "snippet", "None"]), ("def f():\n    return 'f ran'\nif __name__ == '__main__':\n    print(f())", ["Nothing", "f", "An error"]),
        ("import math as m\nprint(m.floor(2.7))", ["2.7", "3", "An error"]), ("from math import sqrt\nprint(int(sqrt(49)))", ["7.0", "49", "An error"])],
        "A file run directly has __name__ == '__main__'; imported, it has its module name, so the guard skips script code")),
    ("PR-7.5.B", facts("pr-py-import", PY, [
        ("Why guard code with if __name__ == '__main__':?", "So importing the file doesn't run its script code", "For speed", "It's required", "To hide functions"),
        ("from stats import mean lets you call:", "mean(xs)", "stats.mean(xs) only", "import.mean(xs)", "Nothing"),
        ("import numpy as np then calls functions as:", "np.mean(x)", "numpy.np.mean(x)", "mean(x)", "as.mean(x)"),
    ], "Modules organise code; the guard separates library from script")),
    ("PR-7.5.C", P("pr-py-try", PY, [
        ("try:\n    x = int('4a')\nexcept ValueError:\n    x = -1\nfinally:\n    print('f', end=' ')\nprint(x)", ["-1", "f 4", "ValueError"]),
        ("try:\n    print(1 / 0)\nexcept ZeroDivisionError as e:\n    print(type(e).__name__)", ["0", "inf", "Error"]),
        ("try:\n    v = [1, 2][5]\nexcept LookupError:\n    v = 0\nprint(v)", ["IndexError", "5", "None"]),
        ("def f():\n    try:\n        return 'try'\n    finally:\n        print('cleanup', end=' ')\nprint(f())", ["try", "cleanup", "try cleanup"])],
        "except catches the named type and its subclasses (IndexError is a LookupError); finally always runs, even after return")),
    ("PR-7.6.A", PN("pr-py-read-file", PY, [
        "import io\nf = io.StringIO('name,mass\\nA,1.5\\nB,2.5\\nC,4.0\\n')\nnext(f)\ntotal = 0\nfor line in f:\n    name, mass = line.strip().split(',')\n    total += float(mass)\nprint(total)",
        "import io\nf = io.StringIO('t,T\\n0,300\\n1,310\\n2,330\\n')\nrows = f.read().splitlines()[1:]\nprint(max(int(r.split(',')[1]) for r in rows))",
        "import io\nf = io.StringIO('# header\\n1 2\\n3 4\\n')\nn = 0\nfor line in f:\n    if line.startswith('#'):\n        continue\n    n += sum(int(t) for t in line.split())\nprint(n)"],
        "Skip the header, strip the newline, split on the delimiter, convert each field. (io.StringIO stands in for open(...) here)", final=False)),
    ("PR-7.6.A", facts("pr-py-with", PY, [
        ("with open('data.csv') as f: … guarantees:", "The file is closed when the block ends, even after an error", "Faster reading", "The file exists", "Write access"),
        ("for line in f: gives each line:", "Including its trailing newline", "Without the newline", "As a list", "As numbers"),
        ("float('2.5\\n') gives:", "2.5 (whitespace is ignored)", "An error", "'2.5'", "2"),
        ("To skip a one-line header:", "next(f) before the loop", "f.skip()", "for line in f[1:]", "del f[0]"),
    ], "Open in a with-block, iterate lines, convert fields")),
    # ── 8 numpy ───────────────────────────────────────────────────────────────────────────────────────────────────
    ("PR-8.1.A", P("pr-np-create", PY, [
        (NP + "x = np.linspace(0, 1, 5)\nprint(x.shape, x[1])", ["(4,) 0.2", "(5,) 0.2", "(5,) 0.2,"]),
        (NP + "x = np.arange(0, 1, 0.25)\nprint(len(x), x[-1])", ["5 1.0", "4 1.0", "3 0.75"]),
        (NP + "x = np.zeros((2, 3))\nprint(x.shape, x.dtype)", ["(3, 2) float64", "(2, 3) int64", "6 float64"]),
        (NP + "x = np.array([1, 2, 3])\nprint(x.dtype, (x / 2).dtype)", ["float64 float64", "int64 int64", "int float"])],
        "linspace includes both ends (n points); arange excludes the stop; zeros and ones default to float64")),
    ("PR-8.1.A", facts("pr-np-create-facts", PY, [
        ("np.linspace(0, 10, 11) has spacing:", "1", "10/11", "0.1", "11"),
        ("np.arange(0, 10, 2) gives:", "[0, 2, 4, 6, 8]", "[0, 2, 4, 6, 8, 10]", "[2, 4, 6, 8, 10]", "5 points from 0 to 10"),
        ("x.shape for a 3 × 4 array is:", "(3, 4)", "12", "(4, 3)", "[3, 4]"),
        ("To make 100 evenly spaced times from 0 to 2 s inclusive:", "np.linspace(0, 2, 100)", "np.arange(0, 2, 100)", "np.arange(0, 2)", "range(0, 2, 0.02)"),
    ], "Shapes and dtypes before values")),
    ("PR-8.1.B", PN("pr-np-index", PY, [NP + "x = np.arange(12).reshape(3, 4)\nprint(x[:, 0].sum())", NP + "x = np.arange(12).reshape(3, 4)\nprint(x[1:, ::2].sum())",
        NP + "x = np.array([3, -1, 4, -1, 5])\nprint(x[x > 0].sum())", NP + "x = np.arange(12).reshape(3, 4)\nprint(x[-1, -1] + x[0, 1])"],
        "x[r, c]; ':' takes all; a:b:s slices with a step; a boolean mask keeps the True positions")),
    ("PR-8.1.B", P("pr-np-shape-index", PY, [
        (NP + "x = np.zeros((5, 3))\nprint(x[:, 0].shape)", ["(5, 1)", "(3,)", "(1, 5)"]), (NP + "x = np.zeros((5, 3))\nprint(x[1:3].shape)", ["(3, 3)", "(2,)", "(5, 2)"]),
        (NP + "x = np.zeros((5, 3))\nprint(x[:, :1].shape)", ["(5,)", "(1, 5)", "(3, 1)"]), (NP + "x = np.arange(6)\nprint(x[x % 2 == 0].shape)", ["(6,)", "(2,)", "(3, 1)"])],
        "An integer index removes that axis; a slice keeps it")),
    ("PR-8.1.C", P("pr-np-axis-shape", PY, [
        (NP + "x = np.ones((4, 3))\nprint(x.sum(axis=0).shape)", ["(4,)", "(1, 3)", "()"]), (NP + "x = np.ones((4, 3))\nprint(x.mean(axis=1).shape)", ["(3,)", "(4, 1)", "()"]),
        (NP + "x = np.ones((4, 3))\nprint(x.max().shape)", ["(4,)", "(3,)", "(1,)"]), (NP + "x = np.ones((2, 4, 3))\nprint(x.sum(axis=1).shape)", ["(2, 4)", "(4, 3)", "(2, 1, 3)"])],
        "Reducing along an axis removes that axis from the shape; no axis reduces everything to a scalar")),
    ("PR-8.1.C", PN("pr-np-axis-value", PY, [NP + "x = np.array([[1, 2, 3], [4, 5, 6]])\nprint(x.sum(axis=0)[1])", NP + "x = np.array([[1, 2, 3], [4, 5, 6]])\nprint(x.mean(axis=1)[1])",
        NP + "x = np.array([[1, 9, 3], [4, 5, 6]])\nprint(x.max(axis=0).sum())", NP + "x = np.array([[1, 9, 3], [4, 5, 6]])\nprint(x.argmax(axis=1).sum())"],
        "axis=0 collapses rows (one result per column); axis=1 collapses columns (one per row)", final=False)),
    ("PR-8.2.A", PN("pr-np-vectorise", PY, [NP + "x = np.arange(1, 6)\nprint((x ** 2).sum())", NP + "x = np.array([1.0, 2.0, 4.0])\nprint((x / x.sum()).max())",
        NP + "t = np.arange(4)\ny = 3 * t + 1\nprint(y[-1])", NP + "x = np.array([2, 5, 1, 7])\nprint(np.where(x > 3, x, 0).sum())"],
        "Array expressions act element by element, replacing an explicit loop; np.where is a vectorised if", final=False)),
    ("PR-8.2.A", facts("pr-np-vectorise-facts", PY, [
        ("A loop 'for k in range(n): y[k] = 2 * x[k] + 1' becomes:", "y = 2 * x + 1", "y = np.loop(x)", "y = [2 * x + 1]", "y = x.apply(2, 1)"),
        ("Why are vectorised NumPy expressions faster than Python loops?", "The loop runs in compiled code over contiguous memory", "They use fewer numbers", "They skip elements", "They aren't"),
        ("'if x[k] > 0: y[k] = x[k] else 0' for every k becomes:", "np.where(x > 0, x, 0)", "if x > 0: y = x", "max(x, 0)", "x > 0"),
    ], "Think in whole arrays")),
    ("PR-8.2.B", P("pr-np-broadcast", PY, [
        (NP + "print((np.ones((3, 1)) + np.ones(4)).shape)", ["(3, 1)", "(4,)", "An error"]), (NP + "print((np.ones((2, 3)) * np.ones(3)).shape)", ["(2,)", "(3, 3)", "An error"]),
        (NP + "print((np.ones((5, 1, 3)) - np.ones((4, 1))).shape)", ["(5, 1, 3)", "(4, 5, 3)", "An error"]),
        (NP + "try:\n    np.ones((2, 3)) + np.ones(2)\nexcept ValueError:\n    print('error')", ["(2, 3)", "(2, 2)", "(3, 2)"])],
        "Align shapes from the right; each pair of sizes must be equal or 1; size-1 axes stretch")),
    ("PR-8.2.B", facts("pr-np-broadcast-facts", PY, [
        ("Do shapes (4, 3) and (3,) broadcast?", "Yes, to (4, 3)", "No", "Yes, to (3, 4)", "Only with reshape"),
        ("Do shapes (4, 3) and (4,) broadcast?", "No: trailing sizes 3 and 4 differ", "Yes, to (4, 3)", "Yes, to (4, 4)", "Yes, to (4,)"),
        ("To subtract each row's mean from a (100, 3) array x:", "x - x.mean(axis=1, keepdims=True)", "x - x.mean(axis=1)", "x - x.mean()", "x.mean(axis=0) - x"),
    ], "Right-align and compare")),
    ("PR-8.2.C", P("pr-np-matmul", PY, [
        (NP + "a = np.ones((2, 3)); b = np.ones((3, 4))\nprint((a @ b).shape)", ["(2, 3)", "(3, 4)", "An error"]),
        (NP + "a = np.array([[1, 2], [3, 4]])\nprint((a * a)[0, 1], (a @ a)[0, 1])", ["4 4", "10 4", "2 10"]),
        (NP + "v = np.array([1, 2, 3])\nprint(v @ v, (v * v).shape)", ["(3,) 14", "14 14", "6 (3,)"]),
        (NP + "a = np.ones((3, 2))\ntry:\n    a @ a\nexcept ValueError:\n    print('error')", ["(3, 3)", "(2, 2)", "(3, 2)"])],
        "* multiplies element by element (shapes broadcast); @ is the matrix product, (m, k) @ (k, n) → (m, n)")),
    ("PR-8.2.C", facts("pr-np-matmul-facts", PY, [
        ("(5, 3) @ (3, 2) has shape:", "(5, 2)", "(3, 3)", "(5, 3)", "An error"),
        ("(5, 3) * (5, 3) has shape:", "(5, 3)", "(5, 5)", "(3, 3)", "An error"),
        ("(5, 3) @ (5, 3) gives:", "An error (inner sizes 3 and 5 differ)", "(5, 5)", "(3, 3)", "(5, 3)"),
        ("For 1-D vectors u @ v gives:", "Their dot product (a scalar)", "An outer product", "Element-wise product", "An error"),
    ], "Inner dimensions must match for @")),
    ("PR-8.2.D", P("pr-np-pairwise", PY, [
        (NP + "r = np.zeros((10, 3))\nd = r[:, None, :] - r[None, :, :]\nprint(d.shape)", ["(10, 3)", "(10, 10)", "(3, 10, 10)"]),
        (NP + "r = np.zeros((10, 3))\nd = r[:, None, :] - r[None, :, :]\nprint(np.sqrt((d ** 2).sum(-1)).shape)", ["(10, 10, 3)", "(10,)", "(3,)"]),
        (NP + "r = np.array([[0, 0], [3, 4], [6, 8]])\nd = r[:, None, :] - r[None, :, :]\nprint(np.sqrt((d ** 2).sum(-1)).max())", ["5.0", "14.0", "100.0"])],
        "r[:, None, :] − r[None, :, :] broadcasts (N, 1, 3) and (1, N, 3) to (N, N, 3); summing squares over the last axis gives the N × N distances")),
    ("PR-8.2.D", Q("pr-np-pair-count", PY, "N = {{N}} particles: how many floats does the (N, N, 3) displacement array hold, and how many distinct pairs are there? (Give the number of distinct pairs.)",
        given={"N": {"pick": [10, 100, 1000]}}, value="N*(N - 1)/2", tex="P", final=True, verify="binomial(N, 2)",
        explain="The full array holds 3N² floats though only N(N − 1)/2 pairs are distinct: memory grows as N², so large N needs neighbour lists")),
    ("PR-8.3.A", PN("pr-np-loadtxt", PY, [
        NP + "import io\ntxt = io.StringIO('t,x,y\\n0,1,2\\n1,3,4\\n2,5,6\\n')\nd = np.loadtxt(txt, delimiter=',', skiprows=1)\nprint(d.shape[0] * 10 + d.shape[1])",
        NP + "import io\ntxt = io.StringIO('t,x,y\\n0,1,2\\n1,3,4\\n2,5,6\\n')\nd = np.loadtxt(txt, delimiter=',', skiprows=1, usecols=(0, 2))\nprint(d[:, 1].sum())",
        NP + "import io\ntxt = io.StringIO('a b\\n1 2\\n3 nan\\n')\nd = np.genfromtxt(txt, skip_header=1)\nprint(np.isnan(d).sum())"],
        "skiprows skips header lines; usecols picks columns; genfromtxt tolerates missing values as nan", final=False)),
    ("PR-8.3.A", facts("pr-np-loadtxt-facts", PY, [
        ("np.loadtxt('d.csv', delimiter=',') on a file with a text header:", "Fails unless skiprows=1", "Skips it automatically", "Loads it as nan", "Returns strings"),
        ("A 100-row, 4-column file loaded with usecols=(1, 3) has shape:", "(100, 2)", "(100, 4)", "(2, 100)", "(4,)"),
        ("Missing entries are best handled by:", "np.genfromtxt, which fills them with nan", "np.loadtxt", "Deleting the file", "int()"),
    ], "Tell the loader about headers, delimiters and columns")),
    ("PR-8.3.B", PN("pr-np-stats", PY, [NP + "x = np.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])\nprint(x.std())", NP + "x = np.array([3, 9, 2, 9])\nprint(x.argmax())",
        NP + "d = np.array([[1, 10], [2, 30], [3, 20]])\nprint(d[d[:, 1] > 15, 0].sum())", NP + "x = np.array([2.0, 4.0, 6.0])\nprint(x.std(ddof=1))"],
        "std uses ddof=0 (population) by default; argmax gives the first index of the maximum; a mask on one column selects rows", final=False)),
    ("PR-8.3.B", facts("pr-np-stats-facts", PY, [
        ("x.std() divides by:", "n (ddof=0)", "n − 1", "n + 1", "√n"),
        ("For a sample standard deviation use:", "x.std(ddof=1)", "x.std()", "x.var()", "np.mean(x)"),
        ("d[d[:, 2] > 0] selects:", "Rows whose third column is positive", "Columns", "The third column", "Nothing"),
    ], "Population versus sample, and masks over rows")),
    ("PR-8.3.C", P("pr-np-save", PY, [
        (NP + "import io\nb = io.BytesIO()\nx = np.arange(6).reshape(2, 3)\nnp.save(b, x)\nb.seek(0)\ny = np.load(b)\nprint(y.shape, (x == y).all())", ["(6,) True", "(2, 3) False", "(3, 2) True"]),
        (NP + "import io\ns = io.StringIO()\nnp.savetxt(s, np.array([[1.5, 2.0]]), delimiter=',')\nprint(s.getvalue().count(','))", ["2", "0", "1.5"]),
        (NP + "import io\nb = io.BytesIO()\nnp.save(b, np.array([1, 2], dtype=np.int32))\nb.seek(0)\nprint(np.load(b).dtype)", ["int64", "float64", "object"])],
        ".npy keeps shape and dtype exactly; savetxt writes text (floats by default), which loses dtype and needs a shape on reload")),
    ("PR-8.3.C", facts("pr-np-save-facts", PY, [
        ("To save an array and reload it with the same shape and dtype:", "np.save / np.load (.npy)", "np.savetxt / loadtxt always", "print and copy", "json.dump"),
        ("To share a table with a spreadsheet user:", "np.savetxt(..., delimiter=',') as CSV", "np.save", "pickle", "A screenshot"),
        ("Several arrays in one file:", "np.savez", "np.save twice to one name", "np.loadtxt", "Impossible"),
    ], "Binary for exactness, text for people")),
    ("PR-8.4.A", facts("pr-plot", PY, [
        ("plt.plot(t, T, label='run 1') then plt.legend() shows:", "A legend entry 'run 1'", "Nothing", "A title", "Axis labels"),
        ("Axis labels should include:", "The quantity and its units, e.g. 'Time (s)'", "Only the variable letter", "Nothing", "The file name"),
        ("plt.savefig('fig.png', dpi=300) should be called:", "Before plt.show(), which may clear the figure", "After plt.close()", "Never", "Before plotting"),
        ("Plotting two series on one axes needs:", "Two plot calls (or one with both), then legend", "Two figures", "subplot(3)", "Nothing special"),
        ("fig, ax = plt.subplots() then ax.set_xlabel('x (m)') labels:", "That axes' x axis", "All figures", "The title", "The legend"),
    ], "Label, legend, then save")),
    ("PR-8.4.A", PN("pr-plot-data", PY, [NP + "t = np.linspace(0, 10, 11)\nT = 300 + 5 * t\nprint(T[np.argmin(np.abs(t - 4))])", NP + "x = np.linspace(0, 2, 5)\nprint(len(x) - 1)",
        NP + "t = np.arange(0, 1, 0.1)\nprint(round(t[1] - t[0], 3))"],
        "Know what arrays you're plotting: points, spacing and the value at a given x", final=False)),
    ("PR-8.4.B", facts("pr-log-axes", PY, [
        ("y = A·e^(−kt) appears as a straight line on:", "Semilog-y axes (log y against t)", "Log-log axes", "Linear axes", "Polar axes"),
        ("y = C·x^p appears straight on:", "Log-log axes, with slope p", "Semilog-y", "Linear axes", "Semilog-x"),
        ("On semilog-y with natural log, the slope of ln y against t is:", "−k, the rate constant", "A", "p", "1/k"),
        ("Data spanning 10⁻³ to 10³ is best shown on:", "A log axis", "A linear axis", "A pie chart", "No axis"),
    ], "Choose axes that make the expected model straight")),
    ("PR-8.4.B", Q("pr-loglog-slope", PY, "On a log-log plot, the line passes through (x, y) = ({{x1}}, {{y1}}) and ({{x2}}, {{y2}}). What exponent p does y = Cxᵖ have?",
        cases=[{"x1": 1, "y1": 2, "x2": 100, "y2": 20000}, {"x1": 10, "y1": 1000, "x2": 1000, "y2": 10}, {"x1": 2, "y1": 3, "x2": 32, "y2": 12}, {"x1": 1, "y1": 5, "x2": 1000, "y2": 5000000}],
        value="log(y2/y1)/log(x2/x1)", tex="p", verify="solve(Eq(Symbol('pp')*log(Rational(x2, x1)), log(Rational(y2, y1))), Symbol('pp'))[0]",
        explain="p = Δlog y / Δlog x")),
    ("PR-8.5.A", Q("pr-euler-step", PY, "Forward Euler on dy/dt = −{{k}}y with y(0) = {{y0}} and Δt = {{h}}. What is y after {{n}} steps?",
        given={"k": {"pick": [0.5, 1, 2]}, "y0": {"pick": [1, 10]}, "h": {"pick": [0.1, 0.2]}, "n": {"pick": [2, 3, 5]}},
        value="y0*(1 - k*h)^n", tex="y_n", verify="nsimplify(y0)*(1 - nsimplify(k)*nsimplify(h))**n",
        explain="Each step multiplies by (1 − kΔt); it is stable only while |1 − kΔt| < 1")),
    ("PR-8.5.A", Q("pr-euler-nsteps", PY, "To integrate from t = 0 to t = {{T}} with Δt = {{h}}, how many Euler steps are needed?",
        given={"T": {"pick": [1, 5, 10]}, "h": {"pick": [0.01, 0.05, 0.1]}}, value="round(T/h)", tex="n", final=True, verify="Rational(T)/nsimplify(h)",
        explain="n = T/Δt; compute it with round(), since T/Δt in floating point may land just below an integer")),
    ("PR-8.5.B", Q("pr-verlet-step", PY, "Velocity Verlet for a unit-mass spring (a = −x), Δt = {{h}}, x₀ = {{x0}}, v₀ = 0. What is x after one step (x₁ = x₀ + v₀Δt + ½a₀Δt²)?",
        given={"h": {"pick": [0.1, 0.2, 0.5]}, "x0": {"pick": [1, 2]}}, value="x0 - 0.5*x0*h^2", tex="x_1", verify="nsimplify(x0)*(1 - nsimplify(h)**2/2)",
        explain="Then a₁ = −x₁ and v₁ = v₀ + ½(a₀ + a₁)Δt")),
    ("PR-8.5.B", Q("pr-verlet-v", PY, "Same oscillator (a = −x), Δt = {{h}}, x₀ = {{x0}}, v₀ = 0. What is v₁ = v₀ + ½(a₀ + a₁)Δt?",
        given={"h": {"pick": [0.1, 0.2]}, "x0": {"pick": [1, 2]}}, value="0.5*(-x0 - x0*(1 - h^2/2))*h", tex="v_1",
        verify="Rational(1, 2)*(-nsimplify(x0) - nsimplify(x0)*(1 - nsimplify(h)**2/2))*nsimplify(h)",
        explain="Verlet averages the old and new accelerations: time-reversible and energy-conserving on average")),
    ("PR-8.5.C", facts("pr-energy-drift", PY, [
        ("Total energy in an NVE run rises steadily. The likely cause:", "The timestep is too large", "The system is too small", "Too many output frames", "The seed"),
        ("With velocity Verlet and a good timestep, total energy:", "Fluctuates slightly around a constant", "Rises linearly", "Falls to zero", "Is exactly constant at every step"),
        ("For bonds to hydrogen at about 10 fs period, a usual timestep is:", "1 fs (2 fs with constraints)", "10 fs", "100 fs", "1 ps"),
        ("Forward Euler on an oscillator:", "Gains energy every step", "Conserves energy", "Loses all energy", "Is exact"),
    ], "Energy drift is the first check on an integrator")),
    ("PR-8.5.C", Q("pr-euler-energy", PY, "Forward Euler on a unit oscillator (x′ = v, v′ = −x) multiplies the energy x² + v² by (1 + Δt²) each step. With Δt = {{h}}, by what factor does energy grow over {{n}} steps?",
        given={"h": {"pick": [0.01, 0.05, 0.1]}, "n": {"pick": [100, 1000]}}, value="(1 + h^2)^n", tex="g",
        verify="((1 + nsimplify(h)**2))**n", explain="(x + vΔt)² + (v − xΔt)² = (1 + Δt²)(x² + v²): a steady drift upward")),
    ("PR-8.5.D", Q("pr-lj-energy", PY, "Lennard-Jones with ε = 1, σ = 1: U(r) = 4(r⁻¹² − r⁻⁶). What is U at r = {{r}}?",
        given={"r": {"pick": [1, 1.1, 1.2, 1.5, 2]}}, value="4*(r^(-12) - r^(-6))", tex="U", verify="4*(nsimplify(r)**-12 - nsimplify(r)**-6)",
        explain="Zero at r = σ, minimum −ε at r = 2^(1/6)σ ≈ 1.122")),
    ("PR-8.5.D", Q("pr-lj-force", PY, "With ε = σ = 1, the LJ force F(r) = −dU/dr. What is F at r = {{r}} (positive means repulsive)?",
        given={"r": {"pick": [1, 1.1, 1.5, 2]}}, value="24*(2*r^(-13) - r^(-7))", tex="F",
        verify="-diff(4*(Symbol('rr')**-12 - Symbol('rr')**-6), Symbol('rr')).subs(Symbol('rr'), nsimplify(r))",
        explain="F = 24(2r⁻¹³ − r⁻⁷): repulsive inside the minimum, attractive outside, zero at 2^(1/6)")),
    ("PR-8.6.A", P("pr-np-seed", PY, [
        (NP + "a = np.random.default_rng(42).normal(size=3)\nb = np.random.default_rng(42).normal(size=3)\nprint((a == b).all())", ["False", "None", "An error"]),
        (NP + "g = np.random.default_rng(0)\na = g.random()\nb = g.random()\nprint(a == b)", ["True", "None", "0"]),
        (NP + "v = np.random.default_rng(1).normal(0, 2, size=100000)\nprint(round(v.std(), 1))", ["1.0", "4.0", "0.0"])],
        "The same seed gives the same stream; successive draws from one generator differ. normal(mean, sd) has the sd you pass")),
    ("PR-8.6.A", Q("pr-mb-sd", PY, "Initial velocities per component are drawn from a normal with σ = √(k_BT/m). In reduced units (k_B = m = 1) at T = {{T}}, what σ do you pass?",
        given={"T": {"pick": [0.5, 1, 1.5, 2]}}, value="sqrt(T)", tex="\\sigma", verify="sqrt(nsimplify(T))",
        explain="Maxwell–Boltzmann: each component has variance k_BT/m; seed the generator so the run reproduces")),
    ("PR-8.6.B", P("pr-np-isclose", PY, [
        (NP + "print(np.isclose(0.1 + 0.2, 0.3))", ["False", "0.3", "An error"]), (NP + "print(0.1 + 0.2 == 0.3)", ["True", "0.3", "An error"]),
        (NP + "print(np.allclose([1.0, 2.0], [1.0, 2.0 + 1e-12]))", ["False", "None", "An error"]), (NP + "print(np.isclose(1e-10, 0))", ["False", "0", "An error"])],
        "Compare floats with a tolerance; isclose has an absolute tolerance of 1e-8, so tiny numbers near 0 count as close")),
    ("PR-8.6.B", facts("pr-test-numeric", PY, [
        ("A good test for a numerical integrator:", "A case with a known exact answer (e.g. the integral of x² from 0 to 1, which is 1/3)", "Running it once and looking", "Checking it doesn't crash", "Timing it"),
        ("Halving the step of a second-order method should cut the error by about:", "4", "2", "8", "1"),
        ("assert abs(f(x) - expected) < 1e-9 is better than ==, because:", "Rounding makes exact equality unreliable", "It's faster", "== fails to compile", "It isn't"),
    ], "Test against known answers and convergence rates")),
    ("PR-8.6.C", P("pr-argparse", PY, [
        ("import argparse\np = argparse.ArgumentParser()\np.add_argument('--steps', type=int, default=100)\na = p.parse_args(['--steps', '50'])\nprint(a.steps * 2)", ["5050", "200", "'50'"]),
        ("import argparse\np = argparse.ArgumentParser()\np.add_argument('--steps', type=int, default=100)\na = p.parse_args([])\nprint(a.steps)", ["None", "0", "An error"]),
        ("import argparse\np = argparse.ArgumentParser()\np.add_argument('infile')\na = p.parse_args(['run.csv'])\nprint(a.infile)", ["infile", "None", "['run.csv']"])],
        "argparse turns command-line words into typed attributes with defaults")),
    ("PR-8.6.C", facts("pr-script-organise", PY, [
        ("A reproducible analysis script should:", "Take inputs as arguments, write outputs to files, and fix seeds", "Use hard-coded paths and print results", "Need manual edits each run", "Run only in a notebook"),
        ("Putting the analysis in functions and calling them from main():", "Makes pieces testable and reusable", "Slows it", "Is required by Python", "Hides bugs"),
        ("Outputs should be written:", "To files named from the inputs or parameters", "Only to the screen", "Over the input data", "Nowhere"),
    ], "Scripts, not copy-paste")),
    # ── 9 systems and impact ──────────────────────────────────────────────────────────────────────────────────────
    ("PR-9.1.A", facts("pr-internet", JB, [
        ("DNS turns:", "A name like example.com into an IP address", "Packets into files", "HTML into pixels", "IP into MAC"),
        ("TCP provides:", "Reliable, ordered delivery over unreliable IP", "Names for hosts", "Web pages", "Routing"),
        ("IP is responsible for:", "Addressing and routing packets between networks", "Reliability", "Encryption", "Naming"),
        ("HTTP is:", "The request–response protocol for the web, on top of TCP", "A routing protocol", "A naming system", "A cable"),
        ("Data is split into packets so that:", "Links can be shared and lost pieces resent", "It is encrypted", "It is smaller in total", "It needs no addresses"),
    ], "Layers: HTTP over TCP over IP, with DNS for names")),
    ("PR-9.1.A", facts("pr-internet-2", JB, [
        ("Packets of one file can arrive out of order because:", "They may take different routes", "TCP reorders them deliberately", "DNS shuffles them", "They can't"),
        ("Redundant routes make the internet:", "Fault tolerant: traffic reroutes around failures", "Slower always", "Less secure", "Centralised"),
        ("HTTPS adds to HTTP:", "TLS encryption and server authentication", "Faster routing", "Compression only", "Nothing"),
    ], "The internet is a network of networks that routes around damage")),
    ("PR-9.2.A", Q("pr-parallel-time", JB, "A workload has {{s}} s of sequential work and {{p}} s of perfectly parallel work. How long does it take on {{n}} processors, and what is the speedup? (Give the speedup.)",
        given={"s": {"pick": [10, 20]}, "p": {"pick": [80, 180]}, "n": {"pick": [2, 4, 10]}}, value="(s + p)/(s + p/n)", tex="S",
        verify="Rational(s + p, 1)/(s + Rational(p, n))", explain="Time = sequential + parallel/n; the sequential part caps the speedup")),
    ("PR-9.2.A", Q("pr-parallel-limit", JB, "With {{s}} s sequential and {{p}} s parallelisable, what is the largest speedup any number of processors can give?",
        given={"s": {"pick": [10, 20, 25]}, "p": {"pick": [90, 180, 75]}}, value="(s + p)/s", tex="S", verify="limit((s + p)/(s + p/Symbol('nn')), Symbol('nn'), oo)",
        explain="As n grows the parallel part vanishes, leaving the sequential time")),
    ("PR-9.3.A", P("pr-rle", JB, [
        ("from itertools import groupby\ns = 'AAABBC'\nprint(''.join(f'{len(list(g))}{k}' for k, g in groupby(s)))", ["A3B2C1", "3A2BC", "AAABBC"]),
        ("from itertools import groupby\ns = 'WWWWBWW'\nprint(''.join(f'{len(list(g))}{k}' for k, g in groupby(s)))", ["6W1B", "4WB2W", "W4B1W2"]),
        ("from itertools import groupby\ns = 'ABAB'\nprint(len(''.join(f'{len(list(g))}{k}' for k, g in groupby(s))))", ["4", "2", "6"])],
        "Run-length encoding writes count + symbol per run: great for long runs, worse than nothing when runs are short")),
    ("PR-9.3.A", facts("pr-compression", JB, [
        ("A program's source code should be compressed:", "Losslessly (zip): every bit must come back", "Lossily (JPEG)", "Either", "Never"),
        ("A photo for a website:", "Lossy (JPEG/WebP) is usually fine", "Must be lossless", "Can't be compressed", "Should be text"),
        ("A medical scan for diagnosis:", "Lossless, to keep every detail", "Lossy", "Either", "Text"),
        ("Lossless compression works by:", "Removing redundancy, so it can be undone exactly", "Dropping detail", "Encrypting", "Lowering resolution"),
    ], "Lossless when every bit matters; lossy when people won't notice")),
    ("PR-9.4.A", facts("pr-impact-innovation", JB, [
        ("Students without home internet can't do online homework. This is:", "The digital divide", "Bias in data", "Phishing", "Overfitting"),
        ("A hiring model trained on past hires that favoured one group may:", "Reproduce that bias", "Remove it automatically", "Be neutral", "Hire randomly"),
        ("A beneficial effect of GPS navigation:", "Efficient routes and emergency response", "No effects", "More traffic always", "None"),
        ("A harmful effect of the same innovation can be:", "Tracking people's movements without consent", "Shorter trips", "Better maps", "Saved fuel"),
    ], "Innovations help and harm; ask for whom")),
    ("PR-9.4.A", facts("pr-impact-innovation-2", JB, [
        ("Crowdsourcing (e.g. citizen science) lets projects:", "Gather data and effort from many people", "Avoid all errors", "Skip consent", "Work offline only"),
        ("An effect nobody intended when an innovation was designed is:", "An unintended consequence", "A feature", "A bug report", "A protocol"),
        ("Open data can help research but risks:", "Re-identification of people in it", "Nothing", "Slower science", "Less access"),
    ], "Weigh effects on different groups")),
]

# a few answers are built here rather than written by hand
for code, q in ADD:
    if q.name == "pr-linear-compares":
        for c in q.cases: c["ans"] = float(PC.py_out(c["code"]))
    if q.name == "pr-gcd-steps":
        q.value = "gcd(a, b)"
