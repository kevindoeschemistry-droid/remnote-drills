# Programming Foundations — curriculum framework (draft 1)

Generated from `drills/frameworks/programming.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**140 learning objectives** in 9 units (136 core): 0 drilled, 0 partly, 140 with no drills. Core: 0 / 136 drilled.

## Big ideas

- **CRD · Programs are developed, tested and fixed.** Software is built iteratively — specify, write, test with chosen inputs, find the error, fix it — and its purpose, inputs and outputs are stated so others can use it.
- **DAT · Everything is stored as bits.** Numbers, text and images are finite bit patterns; that finiteness causes overflow and round-off, and data only becomes information after it is cleaned and processed.
- **AAP · Algorithms are built from sequence, selection, iteration and abstraction.** Every program is statements in order, choices, repetition, and named procedures and data structures that hide detail; the same task can be solved by algorithms of very different cost.
- **CSN · Computing runs on systems and networks.** Code runs on a machine through an operating system and shell, across networks and many processors; redundancy and parallelism decide reliability and speed.
- **IOC · Computing affects people.** Programs and data sets carry bias, privacy risk and legal obligations; who is helped or harmed is part of the design.
- **NUM · Scientific computing discretizes and vectorizes.** Continuous laws become loops over finite timesteps on arrays of numbers; the timestep, the floating-point precision and whether the work is vectorized decide whether the answer is right and arrives in time.

## Practices

- **P1 · Design.** Turn a described task into an algorithm or program design — which structures, which loops, which methods (CSA practice 1).
- **P2 · Implement.** Write the code, command or expression that carries out the design (CSA practice 2).
- **P3 · Trace.** Execute code by hand and state the exact output, variable values, iteration count or final state (CSA practice 3).
- **P4 · Debug.** Explain why code fails to compile, crashes or gives the wrong answer, and fix it (CSA practice 3, fixing errors).
- **P5 · Explain and document.** Describe what code does, its preconditions and impact, in comments, commit messages and plain words (CSA practice 4).
- **P6 · Compute and check.** Run numerical code with units and tolerances, test it against a known answer, and judge whether the output is physically plausible.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Using objects and methods | core | 15–25% | 27 | 0 | 0 | 27 |
| 2 · Selection and iteration | core | 25–35% | 21 | 0 | 0 | 21 |
| 3 · Class creation | core | 10–18% | 10 | 0 | 0 | 10 |
| 4 · Data collections | core | 30–40% | 24 | 0 | 0 | 24 |
| 5 · The Unix shell | core | — | 11 | 0 | 0 | 11 |
| 6 · Version control with Git | core | — | 9 | 0 | 0 | 9 |
| 7 · Python | core | — | 15 | 0 | 0 | 15 |
| 8 · Scientific computing with NumPy | core | — | 19 | 0 | 0 | 19 |
| 9 · Computing systems, networks and impact | extension | — | 4 | 0 | 0 | 4 |

## Unit 1 · Using objects and methods

Big ideas: CRD, DAT, AAP

### 1.1 Algorithms, programs and errors

Book: csa-ced §1.1; csp-ced §1.3, §1.4, §3.3

- ○ **PR-1.1.A** (CSA-1.1.A, AAP-2.A) Write an everyday procedure as ordered, unambiguous steps and trace it on an input.
  - EK: An algorithm is a finite sequence of precise steps; sequence, selection and iteration are enough to express any algorithm.
  - P1
- ○ **PR-1.1.B** (CSA-1.1.B) Put the steps of writing, compiling and running a Java program in order and say which step catches which problem.
  - EK: javac turns .java source into .class bytecode; the JVM runs the bytecode; the compiler checks syntax and types before anything runs.
  - P5
- ○ **PR-1.1.C** (CSA-1.1.C, CRD-2.I) Classify an error as syntax (compile-time), run-time (exception) or logic, given the code and its symptom.
  - EK: Syntax errors stop compilation; run-time errors throw during execution (int division by 0 throws ArithmeticException); logic errors run and give a wrong answer.
  - Needs: PR-1.1.B
  - P4
- ○ **PR-1.1.D** (CRD-2.J) Choose test inputs, including boundary cases, and state the output each should produce.
  - EK: Test typical, boundary (0, 1, empty, the limits) and invalid inputs; a test is useful only with a predicted answer.
  - Needs: PR-1.1.A
  - P6

### 1.2 Bits and binary numbers

Book: csp-ced §2.1

- ○ **PR-1.2.A** (DAT-1.C) Convert a non-negative integer between decimal and binary.
  - EK: Place values are powers of 2: 1011₂ = 8 + 2 + 1 = 11.
  - P3
- ○ **PR-1.2.B** (DAT-1.A) Count the distinct values n bits can represent, and the bits needed for N values.
  - EK: n bits give 2ⁿ patterns; N values need ⌈log₂ N⌉ bits.
  - Needs: PR-1.2.A
  - P3

### 1.3 Variables, types, expressions and output

Book: csa-ced §1.2, §1.3, §1.4; csp-ced §3.1, §3.3

- ○ **PR-1.3.A** (CSA-1.2.A) Choose a primitive type (int, double, boolean) or a reference type (String, an object) for a described quantity.
  - EK: A primitive variable holds the value itself; a reference variable holds the address of an object.
  - P1
- ○ **PR-1.3.B** (CSA-1.2.B, AAP-1.A) Declare and initialise variables of type int, double and boolean.
  - EK: type name = value; a variable is declared before use and keeps one type for its lifetime.
  - Needs: PR-1.3.A
  - P2
- ○ **PR-1.3.C** (CSA-1.3.C, AAP-2.C) Evaluate an arithmetic expression with int and double operands, including integer division and %.
  - EK: int / int truncates toward zero (7 / 2 = 3, −7 / 2 = −3); % keeps the sign of the dividend (−7 % 2 = −1); one double operand makes the result double; * / % bind tighter than + −.
  - Needs: PR-1.3.B
  - P3
- ○ **PR-1.3.D** (CSA-1.3.A, CSA-1.3.B) Predict exactly what print and println statements display, including string concatenation with numbers.
  - EK: + runs left to right: "1" + 2 + 3 is "123" but 1 + 2 + "3" is "33"; println ends the line, print does not.
  - Needs: PR-1.3.C
  - P3

### 1.4 Assignment and compound assignment

Book: csa-ced §1.4, §1.6; csp-ced §3.1

- ○ **PR-1.4.A** (CSA-1.4.A, AAP-1.B) Trace a sequence of assignment statements and give each variable's final value.
  - EK: = evaluates the right side first, then overwrites the variable on the left; the old value is gone, so a swap needs a temporary.
  - Needs: PR-1.3.C
  - P3
- ○ **PR-1.4.B** (CSA-1.6.A) Predict the value stored after compound assignment and ++ / −− operators.
  - EK: x += 3 means x = x + 3; x++ adds 1; for int x, x /= 2 truncates.
  - Needs: PR-1.4.A
  - P3

### 1.5 Casting, range and precision

Book: csa-ced §1.5; csp-ced §2.1

- ○ **PR-1.5.A** (CSA-1.5.A) Predict the result of casting between int and double, including rounding a positive double to the nearest int.
  - EK: (int) truncates toward zero; (int)(x + 0.5) rounds a non-negative x; the cast binds tighter than arithmetic: (double) 7 / 2 = 3.5 but (double)(7 / 2) = 3.0.
  - Needs: PR-1.3.C
  - P3
- ○ **PR-1.5.B** (CSA-1.5.B, DAT-1.B) Predict when int arithmetic overflows and the value that results.
  - EK: int is 32-bit two's complement, −2³¹ to 2³¹ − 1 (Integer.MIN_VALUE to Integer.MAX_VALUE); MAX_VALUE + 1 wraps to MIN_VALUE.
  - Needs: PR-1.2.B, PR-1.3.C
  - P3
- ○ **PR-1.5.C** (CSA-1.5.C, DAT-1.B) Explain why a double calculation is approximate, and compare doubles with a tolerance instead of ==.
  - EK: A double stores a binary fraction in 64 bits, so 0.1 is inexact and 0.1 + 0.2 == 0.3 is false; test Math.abs(a − b) < tol.
  - Needs: PR-1.2.A, PR-1.3.C
  - P6

### 1.6 APIs, method signatures and the Math class

Book: csa-ced §1.7, §1.8, §1.9, §1.10, §1.11; csp-ced §3.12, §3.14, §3.15

- ○ **PR-1.6.A** (CSA-1.7.A, CSA-1.9.A, AAP-3.D) Read API documentation to find what a class provides and which method to call.
  - EK: Documentation gives each method's signature (name, parameter types in order) and return type; a caller needs nothing more.
  - P5
- ○ **PR-1.6.B** (CSA-1.9.B, AAP-3.A) Write a call to a void or non-void method with arguments that match its signature, and pick which overload runs.
  - EK: Arguments match parameters by number, order and type; overloads share a name but differ in parameter list; a non-void result must be stored or used or it is lost.
  - Needs: PR-1.6.A, PR-1.3.B
  - P2
- ○ **PR-1.6.C** (CSA-1.10.A) Call a static (class) method as ClassName.method(...) and give the value it returns.
  - EK: Static methods belong to the class, not to an object; inside the same class the class name can be left off.
  - Needs: PR-1.6.B
  - P3
- ○ **PR-1.6.D** (CSA-1.11.A, AAP-3.E) Evaluate expressions with Math.abs, Math.pow, Math.sqrt and Math.random, including mapping Math.random to an integer range.
  - EK: Math.random() is a double in [0.0, 1.0); (int)(Math.random() * n) + a is an int from a to a + n − 1; pow and sqrt return double.
  - Needs: PR-1.6.C, PR-1.5.A
  - P3
- ○ **PR-1.6.E** (CSA-1.8.A, CRD-2.G) Write a comment stating what a method does, its preconditions and its postconditions.
  - EK: A precondition must be true before the call (the caller's job); a postcondition is what the method guarantees afterwards.
  - Needs: PR-1.6.B
  - P5

### 1.7 Objects, constructors and instance methods

Book: csa-ced §1.12, §1.13, §1.14

- ○ **PR-1.7.A** (CSA-1.12.A, CSA-1.12.B, CSA-1.13.B) Explain how a class relates to its objects, and declare a reference variable that holds an object or null.
  - EK: A class is the blueprint; each object is an instance with its own state; a reference variable holds null or the address of an object.
  - Needs: PR-1.3.A
  - P5
- ○ **PR-1.7.B** (CSA-1.13.A, CSA-1.13.C) Create an object with new, choosing the constructor from its parameter list.
  - EK: new ClassName(args) allocates the object and runs the constructor whose parameters match the arguments.
  - Needs: PR-1.7.A, PR-1.6.B
  - P2
- ○ **PR-1.7.C** (CSA-1.14.A) Call instance methods on an object, trace how its state changes, and predict a NullPointerException.
  - EK: obj.method() acts on that object's fields; calling a method through a null reference throws NullPointerException.
  - Needs: PR-1.7.B
  - P3
- ○ **PR-1.7.D** (CSA-1.12.B) Predict the effect of aliasing — two references to one object — after a change through either reference.
  - EK: b = a copies the reference, not the object; a change made through b is seen through a.
  - Needs: PR-1.7.C
  - P3

### 1.8 Strings

Book: csa-ced §1.15; csp-ced §3.4

- ○ **PR-1.8.A** (CSA-1.15.A, AAP-2.D) Create and concatenate String objects and predict the result.
  - EK: Strings are immutable: concatenation and every String method build a new String, leaving the original unchanged.
  - Needs: PR-1.3.D, PR-1.7.B
  - P3
- ○ **PR-1.8.B** (CSA-1.15.B, AAP-2.D) Evaluate length, substring, indexOf, equals and compareTo calls on strings.
  - EK: Indices run 0 to length() − 1; substring(a, b) is characters a to b − 1 (length b − a); indexOf returns −1 when absent; compareTo is negative, zero or positive in dictionary order.
  - Needs: PR-1.8.A
  - P3
- ○ **PR-1.8.C** (CSA-1.15.B) Distinguish == from equals when comparing strings and other objects.
  - EK: == asks whether two references point to the same object; equals compares contents.
  - Needs: PR-1.8.B, PR-1.7.D
  - P4

## Unit 2 · Selection and iteration

Big ideas: AAP, CRD

### 2.1 Boolean expressions and if statements

Book: csa-ced §2.1, §2.2, §2.3, §2.4; csp-ced §3.5, §3.6, §3.7

- ○ **PR-2.1.A** (CSA-2.2, AAP-2.E) Evaluate relational expressions (==, !=, <, <=, >, >=) to true or false.
  - EK: Relational operators compare two values and produce a boolean; they bind looser than arithmetic, so a + 1 < b compares the sum.
  - Needs: PR-1.3.C
  - P3
- ○ **PR-2.1.B** (CSA-2.3, AAP-2.H) Trace if, if–else and else-if chains and say which branch runs and what is printed.
  - EK: Exactly one branch of an if / else if / else chain runs — the first whose condition is true; a lone if may run zero times.
  - Needs: PR-2.1.A
  - P3
- ○ **PR-2.1.C** (CSA-2.4, AAP-2.I) Trace nested if statements, matching each else to its if.
  - EK: Without braces an else attaches to the nearest unmatched if, whatever the indentation suggests.
  - Needs: PR-2.1.B
  - P3 · P4
- ○ **PR-2.1.D** (CSA-2.1, AAP-2.G) Write a selection algorithm from a stated rule, such as grade bands or the leap-year rule.
  - EK: Order else-if conditions so no earlier condition shadows a later one; leap year: divisible by 4 and (not by 100, or by 400).
  - Needs: PR-2.1.C
  - P1 · P2

### 2.2 Compound boolean expressions

Book: csa-ced §2.5, §2.6; csp-ced §3.5

- ○ **PR-2.2.A** (CSA-2.5, AAP-2.F) Evaluate expressions with &&, || and !, including short-circuit evaluation.
  - EK: ! binds tightest, then &&, then ||; && skips its right side when the left is false, || when the left is true — so x != 0 && y / x > 1 never divides by zero.
  - Needs: PR-2.1.A
  - P3
- ○ **PR-2.2.B** (CSA-2.6) Rewrite a negated compound condition with De Morgan's laws.
  - EK: !(a && b) ≡ !a || !b; !(a || b) ≡ !a && !b; !(x < y) ≡ x >= y.
  - Needs: PR-2.2.A
  - P3
- ○ **PR-2.2.C** (CSA-2.6, AAP-2.L) Decide whether two boolean expressions are equivalent with a truth table or one counterexample.
  - EK: n boolean inputs give 2ⁿ rows; one row where they differ proves they are not equivalent.
  - Needs: PR-2.2.B
  - P3

### 2.3 while loops

Book: csa-ced §2.7; csp-ced §3.8

- ○ **PR-2.3.A** (CSA-2.7, AAP-2.K) Trace a while loop and give the number of iterations and the final value of each variable.
  - EK: The condition is checked before every pass, so the body may run zero times; something in the body must move the condition toward false.
  - Needs: PR-2.1.B, PR-1.4.B
  - P3
- ○ **PR-2.3.B** (CSA-2.7) Identify a loop that never runs or never stops, and fix its initialisation, condition or update.
  - EK: Check three things: the start value, the stopping condition, and that the update moves toward it.
  - Needs: PR-2.3.A
  - P4
- ○ **PR-2.3.C** (CSA-2.7, AAP-2.J) Write a condition-controlled loop for an unknown number of repetitions, such as peeling the digits off an int or halving until below a threshold.
  - EK: n % 10 is the last digit and n / 10 drops it; the loop ends when n reaches 0.
  - Needs: PR-2.3.A
  - P2

### 2.4 for loops

Book: csa-ced §2.8; csp-ced §3.8

- ○ **PR-2.4.A** (CSA-2.8, AAP-2.K) Count the iterations of a for loop from its header, for any start, bound and step.
  - EK: for (int i = a; i < b; i++) runs b − a times; with i <= b, b − a + 1 times; with i += k, ⌈(b − a)/k⌉ times (zero if a ≥ b).
  - Needs: PR-2.3.A
  - P3
- ○ **PR-2.4.B** (CSA-2.8) Trace a for loop and give its output or the final value of an accumulator.
  - EK: Order of one pass: test the condition, run the body, then the update; the loop variable is out of scope after the loop.
  - Needs: PR-2.4.A
  - P3
- ○ **PR-2.4.C** (CSA-2.8) Find and fix an off-by-one error in a loop's start value or bound.
  - EK: Check the first and last pass by hand: indices 0 to n − 1 need i = 0 and i < n.
  - Needs: PR-2.4.B
  - P4

### 2.5 Standard loop algorithms

Book: csa-ced §2.9; csp-ced §3.9

- ○ **PR-2.5.A** (CSA-2.9, AAP-2.M) Implement and trace the accumulator patterns: sum, average, product and count of matches.
  - EK: Initialise before the loop (0 for sums and counts, 1 for products), update inside it, use the result after it; divide by a count as a double.
  - Needs: PR-2.4.B
  - P2 · P3
- ○ **PR-2.5.B** (CSA-2.9) Implement and trace a running minimum or maximum.
  - EK: Initialise to the first value, not 0, so all-negative data still works.
  - Needs: PR-2.5.A
  - P2 · P3
- ○ **PR-2.5.C** (CSA-2.9, AAP-2.M) Implement digit and divisibility algorithms: digit sum, factor list, primality test, gcd.
  - EK: Trial division up to √n settles primality; Euclid: gcd(a, b) = gcd(b, a % b) until b = 0.
  - Needs: PR-2.3.C, PR-2.5.A
  - P2

### 2.6 String algorithms

Book: csa-ced §2.10

- ○ **PR-2.6.A** (CSA-2.10) Traverse a string with substring or charAt to count or locate characters or substrings.
  - EK: s.substring(i, i + 1) for i from 0 to s.length() − 1; a window of length k needs i <= s.length() − k.
  - Needs: PR-1.8.B, PR-2.4.C
  - P2 · P3
- ○ **PR-2.6.B** (CSA-2.10) Build a new string in a loop: reverse it, remove a character, or test for a palindrome.
  - EK: Start from an empty string and concatenate; reversing prepends each character, or appends while counting down from the end.
  - Needs: PR-2.6.A
  - P2 · P3

### 2.7 Nested iteration

Book: csa-ced §2.11

- ○ **PR-2.7.A** (CSA-2.11) Count how many times an inner-loop statement runs in nested loops, including triangular bounds.
  - EK: Independent bounds multiply (n·m); an inner j from i + 1 to n − 1 over i = 0 … n − 1 gives n(n − 1)/2.
  - Needs: PR-2.4.A
  - P3
- ○ **PR-2.7.B** (CSA-2.11) Trace nested loops that print a pattern and give the exact output.
  - EK: The inner loop runs to completion for each pass of the outer loop; println placement decides the line breaks.
  - Needs: PR-2.7.A, PR-2.4.B
  - P3

### 2.8 Informal run-time analysis

Book: csa-ced §2.12; csp-ced §3.17

- ○ **PR-2.8.A** (CSA-2.12, AAP-4.A) Compare algorithms by counting statement executions as a function of input size n.
  - EK: One loop over n ~ n; nested ~ n²; halving each pass ~ log₂ n; polynomial counts run in reasonable time, exponential ones do not.
  - Needs: PR-2.7.A
  - P3

## Unit 3 · Class creation

Big ideas: AAP, IOC

### 3.1 Abstraction, design and anatomy of a class

Book: csa-ced §3.1, §3.2, §3.3; csp-ced §3.13

- ○ **PR-3.1.A** (CSA-3.1, AAP-3.B) Decompose a described task into classes and methods, naming each class's attributes and behaviours.
  - EK: Abstraction hides how something works behind what it does; nouns in the description suggest classes and fields, verbs suggest methods.
  - Needs: PR-1.6.A, PR-1.7.A
  - P1
- ○ **PR-3.1.B** (CSA-3.3) Write a class with private instance variables and public methods, and say what code outside the class can use.
  - EK: Encapsulation: fields private, interface public; outside code reaches state only through public methods.
  - Needs: PR-3.1.A
  - P2

### 3.2 Constructors

Book: csa-ced §3.4

- ○ **PR-3.2.A** (CSA-3.4) Write a constructor that sets every instance variable from its parameters.
  - EK: A constructor has the class name and no return type; it runs once, when new creates the object.
  - Needs: PR-3.1.B, PR-1.7.B
  - P2
- ○ **PR-3.2.B** (CSA-3.4) Predict the default values of instance variables a constructor leaves unset.
  - EK: Unset fields are 0 (int), 0.0 (double), false (boolean) and null (references); a class with no constructor written gets a no-argument default.
  - Needs: PR-3.2.A
  - P3

### 3.3 Writing methods and passing references

Book: csa-ced §3.5, §3.6; csp-ced §3.13

- ○ **PR-3.3.A** (CSA-3.5, AAP-3.C) Write accessor and mutator methods with the correct return types.
  - EK: An accessor returns a value without changing state; a mutator, usually void, changes it; a non-void method must return on every path.
  - Needs: PR-3.2.A
  - P2
- ○ **PR-3.3.B** (CSA-3.6) Predict whether a method call changes the caller's variable, for primitive and for reference arguments.
  - EK: Java passes copies of values: reassigning a parameter never affects the caller, but changing the object a reference parameter points to does.
  - Needs: PR-3.3.A, PR-1.7.D
  - P3
- ○ **PR-3.3.C** (CSA-3.5, CRD-2.B) Trace a sequence of calls on objects of a user-written class and give every object's final state.
  - EK: Each object has its own copy of the instance variables; track them in a table, one column per object.
  - Needs: PR-3.3.B
  - P3

### 3.4 Class members, scope and this

Book: csa-ced §3.7, §3.8, §3.9

- ○ **PR-3.4.A** (CSA-3.7) Predict the value of a static variable shared by all instances, such as an instance counter.
  - EK: A static variable has one copy per class, shared by every object; static methods cannot use instance variables or this.
  - Needs: PR-3.2.A
  - P3
- ○ **PR-3.4.B** (CSA-3.8, CSA-3.9) Decide which variable a name refers to when a parameter or local shadows a field, and resolve it with this.
  - EK: A local exists only inside its block; the innermost declaration wins; this.x always names the field.
  - Needs: PR-3.3.A
  - P3 · P4
- ○ **PR-3.4.C** (CSA-3.2, IOC-1.F) Identify who a program's design affects and the legal or ethical constraints on it, such as licences on reused code and privacy of stored data.
  - EK: Code taken from elsewhere must be credited and used under its licence; a design decides what data is kept, and for how long.
  - Needs: PR-3.1.A
  - P5

## Unit 4 · Data collections

Big ideas: AAP, DAT, IOC

### 4.1 Data sets and their ethics

Book: csa-ced §4.1, §4.2; csp-ced §2.3, §5.3, §5.6

- ○ **PR-4.1.A** (CSA-4.2, DAT-2.A, DAT-2.B, DAT-2.C) Identify what a data set and its metadata can tell you, and what cleaning it needs (missing, invalid or inconsistent entries).
  - EK: Metadata (units, source, date) describes the data; correlation in data does not show causation; invalid entries must be removed or fixed before analysis.
  - P5
- ○ **PR-4.1.B** (CSA-4.1, IOC-1.D, IOC-2.A) Identify privacy, bias and consent risks in collecting a data set, including personally identifiable information.
  - EK: Data that under-represents a group biases every result built on it; combined fields (ZIP + birth date + sex) can identify a person.
  - Needs: PR-4.1.A
  - P5

### 4.2 Arrays

Book: csa-ced §4.3; csp-ced §3.2, §3.10

- ○ **PR-4.2.A** (CSA-4.3, AAP-1.C) Create an array, give its length and default element values, and access an element by index.
  - EK: new int[n] has indices 0 to n − 1, filled with 0 (0.0, false, null for other types); arr.length is a field, no parentheses; an initialiser list {…} fixes the length.
  - Needs: PR-1.7.B, PR-3.2.B
  - P3
- ○ **PR-4.2.B** (CSA-4.3) Predict an ArrayIndexOutOfBoundsException from an index expression.
  - EK: Valid indices satisfy 0 ≤ i < arr.length; arr[arr.length] is always out of bounds.
  - Needs: PR-4.2.A
  - P4

### 4.3 Array traversals

Book: csa-ced §4.4; csp-ced §3.10

- ○ **PR-4.3.A** (CSA-4.4, AAP-2.O) Traverse an array with an indexed for loop and with an enhanced for loop, and say which one can change the array.
  - EK: for (int x : arr) hands out copies of the elements, so assigning x leaves arr unchanged; modifying needs an index.
  - Needs: PR-4.2.A, PR-2.4.B
  - P2 · P3
- ○ **PR-4.3.B** (CSA-4.4) Trace a traversal that steps by 2, skips elements or runs backwards, and list the indices it visits.
  - EK: Backwards: for (int i = arr.length − 1; i >= 0; i−−); the first and last index visited settle off-by-one questions.
  - Needs: PR-4.3.A, PR-2.4.C
  - P3

### 4.4 Array algorithms

Book: csa-ced §4.5; csp-ced §3.10

- ○ **PR-4.4.A** (CSA-4.5, AAP-2.N) Implement sum, mean, minimum, maximum and count-matching over an array.
  - EK: The Unit 2 accumulator patterns, with arr[i] as the value at each pass.
  - Needs: PR-4.3.A, PR-2.5.B
  - P2
- ○ **PR-4.4.B** (CSA-4.5) Implement algorithms over adjacent pairs: detect a repeat, check that the array is sorted, count increases.
  - EK: Comparing arr[i] with arr[i + 1] needs i < arr.length − 1.
  - Needs: PR-4.4.A
  - P2 · P4
- ○ **PR-4.4.C** (CSA-4.5) Reverse, shift or rotate an array in place and give its contents afterwards.
  - EK: Reverse by swapping i with length − 1 − i for i < length / 2; a rotation must save the element it is about to overwrite.
  - Needs: PR-4.4.B, PR-1.4.A
  - P2 · P3

### 4.5 Text files and wrapper classes

Book: csa-ced §4.6, §4.7; csp-ced §2.4

- ○ **PR-4.5.A** (CSA-4.6, DAT-2.D) Read a text file line by line with Scanner and File, splitting each line into fields.
  - EK: while (sc.hasNextLine()) reads to the end; line.split(",") turns a CSV line into a String[]; opening a missing file throws FileNotFoundException, which must be declared or caught.
  - Needs: PR-1.3.B, PR-2.3.A, PR-4.2.A
  - P2
- ○ **PR-4.5.B** (CSA-4.7) Predict autoboxing and unboxing between int and Integer, and parse numbers from strings.
  - EK: Integer.parseInt("42") gives 42; an int is boxed to Integer automatically when stored in a collection; unboxing a null Integer throws NullPointerException.
  - Needs: PR-1.8.C
  - P3

### 4.6 ArrayList

Book: csa-ced §4.8, §4.9, §4.10; csp-ced §3.10

- ○ **PR-4.6.A** (CSA-4.8, AAP-2.N) Predict the contents and size of an ArrayList after add, add(i, x), set, remove and get.
  - EK: add(i, x) shifts later elements right; remove(i) shifts them left and returns the removed element; size(), not length.
  - Needs: PR-4.5.B
  - P3
- ○ **PR-4.6.B** (CSA-4.9) Find and fix the skipped-element bug when removing from an ArrayList inside a forward indexed loop.
  - EK: After remove(i) the next element slides into index i: don't increment that pass, or loop backwards; removing inside an enhanced for throws ConcurrentModificationException.
  - Needs: PR-4.6.A, PR-4.3.A
  - P4

### 4.7 2D arrays

Book: csa-ced §4.11, §4.12, §4.13

- ○ **PR-4.7.A** (CSA-4.11) Create a 2D array and give its number of rows, number of columns and the element at [r][c].
  - EK: int[][] g = new int[R][C]; g.length = R; g[0].length = C; g[r][c] is row r, column c (row-major).
  - Needs: PR-4.2.A
  - P3
- ○ **PR-4.7.B** (CSA-4.12) Trace row-major and column-major nested traversals and give the visiting order or output.
  - EK: Row-major: outer loop over rows, inner over columns; swap the loops for column-major.
  - Needs: PR-4.7.A, PR-2.7.B
  - P3
- ○ **PR-4.7.C** (CSA-4.13) Implement 2D algorithms: row sums, column sums, the main diagonal and in-bounds neighbours.
  - EK: The main diagonal is g[i][i]; neighbour (r + dr, c + dc) exists only if 0 ≤ r + dr < R and 0 ≤ c + dc < C.
  - Needs: PR-4.7.B, PR-4.4.A
  - P2

### 4.8 Searching

Book: csa-ced §4.14, §4.17; csp-ced §3.11

- ○ **PR-4.8.A** (CSA-4.14, AAP-2.O) Trace a linear search and count its comparisons in the best and worst case.
  - EK: Best case 1 comparison (first element), worst case n (last or absent).
  - Needs: PR-4.3.A
  - P3
- ○ **PR-4.8.B** (CSA-4.14, AAP-2.P) Trace an iterative binary search on a sorted array: list the midpoints examined and count the iterations.
  - EK: mid = (low + high) / 2, then discard the half that cannot hold the target; needs sorted data; at most ⌊log₂ n⌋ + 1 iterations.
  - Needs: PR-4.8.A, PR-2.8.A
  - P3

### 4.9 Sorting

Book: csa-ced §4.15

- ○ **PR-4.9.A** (CSA-4.15) Trace selection sort and give the array after k passes.
  - EK: Pass k swaps the smallest remaining element into index k; always n(n − 1)/2 comparisons, whatever the input.
  - Needs: PR-4.4.C, PR-2.7.A
  - P3
- ○ **PR-4.9.B** (CSA-4.15) Trace insertion sort, give the array after k passes, and count comparisons in the best and worst case.
  - EK: Pass k inserts element k into the sorted prefix; already sorted: n − 1 comparisons; reverse sorted: n(n − 1)/2.
  - Needs: PR-4.9.A
  - P3

### 4.10 Recursion, recursive search and merge sort

Book: csa-ced §4.16, §4.17

- ○ **PR-4.10.A** (CSA-4.16) Trace a recursive method and give its return value (factorial, digit sum, power).
  - EK: Each call gets its own parameters; the base case stops the descent; results combine as the calls return, last called first finished.
  - Needs: PR-3.3.A, PR-2.1.B
  - P3
- ○ **PR-4.10.B** (CSA-4.16) Count the calls a recursive method makes, including two-branch recursion such as naive Fibonacci.
  - EK: One recursive call per level: n + 1 calls; naive fib(n) with base cases 0 and 1 makes 2·fib(n + 1) − 1 calls — exponential.
  - Needs: PR-4.10.A
  - P3
- ○ **PR-4.10.C** (CSA-4.16) Find and fix a missing or unreachable base case that causes a StackOverflowError.
  - EK: Every recursive call must move the argument toward a base case that is actually tested.
  - Needs: PR-4.10.A
  - P4
- ○ **PR-4.10.D** (CSA-4.17) Trace recursive binary search and merge sort, giving the subarrays at each level of recursion.
  - EK: Merge sort halves down to single elements, then merges sorted halves: about n log₂ n comparisons, recursion depth ⌈log₂ n⌉.
  - Needs: PR-4.10.B, PR-4.8.B, PR-4.9.B
  - P3

## Unit 5 · The Unix shell

Big ideas: CSN

### 5.1 Navigating files and directories

Book: swc-sh §1, §2

- ○ **PR-5.1.A** (SWC-SH-2) Resolve an absolute or relative path (with ., .. and ~) from a given working directory to the directory or file it names.
  - EK: / is the root; a path not starting with / is relative to pwd; .. is the parent, . the current directory, ~ your home.
  - P3
- ○ **PR-5.1.B** (SWC-SH-2) Predict the output of a sequence of cd, pwd and ls (-a, -l, -F) commands.
  - EK: cd with no argument returns home; ls -a shows hidden dot-files; -F marks directories with /.
  - Needs: PR-5.1.A
  - P3

### 5.2 Working with files and wildcards

Book: swc-sh §3, §4

- ○ **PR-5.2.A** (SWC-SH-3) Predict the file tree after mkdir, touch, cp, mv and rm commands.
  - EK: mv moves or renames and silently overwrites; cp copies; rm deletes for good (no trash); cp and rm need -r for directories.
  - Needs: PR-5.1.B
  - P3
- ○ **PR-5.2.B** (SWC-SH-4) Expand a wildcard pattern (*, ?) against a directory listing.
  - EK: The shell expands *.pdb before the command runs; * matches any run of characters, ? exactly one.
  - Needs: PR-5.2.A
  - P3

### 5.3 Pipes and filters

Book: swc-sh §4

- ○ **PR-5.3.A** (SWC-SH-4) Predict the output of wc, sort (-n, -r), head, tail, cut and uniq on given text.
  - EK: sort is alphabetical unless -n (so 10 sorts before 2); uniq removes only adjacent duplicates, so sort first; wc -l counts lines.
  - Needs: PR-5.2.B
  - P3
- ○ **PR-5.3.B** (SWC-SH-4) Build a pipeline with |, > and >> that answers a question about files, and predict its output.
  - EK: > overwrites a file, >> appends; | sends one command's standard output to the next command's input.
  - Needs: PR-5.3.A
  - P2 · P3

### 5.4 Loops and shell scripts

Book: swc-sh §5, §6

- ○ **PR-5.4.A** (SWC-SH-5) Trace a shell for loop over files and list the commands it runs, including variable expansion and quoting.
  - EK: for f in *.dat; do ...; done expands $f once per file; write "$f" so a name with spaces stays one argument.
  - Needs: PR-5.3.B, PR-2.4.B
  - P3
- ○ **PR-5.4.B** (SWC-SH-6) Write a script that uses $1, $@ and $#, and predict what it does for given arguments.
  - EK: $1 is the first argument, $@ all of them, $# how many; run it with bash script.sh args.
  - Needs: PR-5.4.A
  - P2 · P3
- ○ **PR-5.4.C** (SWC-SH-6) Make a script executable and run it, and diagnose 'command not found' and 'permission denied'.
  - EK: chmod +x script.sh, then ./script.sh — the current directory is not on PATH, so a bare script.sh is not found.
  - Needs: PR-5.4.B
  - P4

### 5.5 Finding things

Book: swc-sh §7

- ○ **PR-5.5.A** (SWC-SH-7) Predict which lines grep matches with -i, -v, -w, -n, -c and -r.
  - EK: -i ignores case, -v inverts, -w matches whole words, -n numbers lines, -c counts, -r searches directories.
  - Needs: PR-5.3.A
  - P3
- ○ **PR-5.5.B** (SWC-SH-7) Predict which files find selects with -name, -type and -maxdepth, and feed its result to another command with $(...).
  - EK: Quote the pattern (find . -name '*.txt') so the shell does not expand it first; $(command) is replaced by that command's output.
  - Needs: PR-5.5.A, PR-5.2.B
  - P3

## Unit 6 · Version control with Git

Big ideas: CRD

### 6.1 Tracking changes

Book: swc-git §1, §3, §4

- ○ **PR-6.1.A** (SWC-GIT-1) Explain what a commit records and why it beats keeping copies like thesis_final_v2.
  - EK: A commit is a snapshot of the staged files with author, time, message and a link to its parent; history is the chain of commits.
  - P5
- ○ **PR-6.1.B** (SWC-GIT-3, SWC-GIT-4) Predict git status (untracked, modified, staged) after edits, git add and git commit.
  - EK: Working tree → git add → staging area → git commit → repository; only staged changes go into a commit.
  - Needs: PR-6.1.A, PR-5.2.A
  - P3

### 6.2 Exploring and undoing history

Book: swc-git §5

- ○ **PR-6.2.A** (SWC-GIT-5) Read git log and git diff output, and name a commit with HEAD, HEAD~n or a hash prefix.
  - EK: HEAD is the current commit, HEAD~1 its parent; git diff shows unstaged changes, git diff --staged staged ones; + lines added, − lines removed.
  - Needs: PR-6.1.B
  - P3
- ○ **PR-6.2.B** (SWC-GIT-5) Choose the command that undoes a change: discard a file's edits, unstage it, or revert a commit.
  - EK: git restore file discards working-tree edits; git restore --staged file unstages; git revert makes a new commit that undoes an old one without rewriting history.
  - Needs: PR-6.2.A
  - P4

### 6.3 Ignoring files and what not to commit

Book: swc-git §6, §8, §9, §10

- ○ **PR-6.3.A** (SWC-GIT-6) Predict which files a .gitignore excludes, including directory patterns and ! negation.
  - EK: *.dat ignores every .dat file; results/ ignores a directory; !keep.dat re-includes one; files already tracked are not affected.
  - Needs: PR-6.1.B, PR-5.2.B
  - P3
- ○ **PR-6.3.B** (SWC-GIT-8, SWC-GIT-9, SWC-GIT-10) Decide what stays out of a repository (secrets, large raw data, generated output) and add a licence and citation file to shared code.
  - EK: A secret pushed once stays in history; with no licence, others may not legally reuse the code; CITATION.cff tells people how to cite it.
  - Needs: PR-6.3.A
  - P5

### 6.4 Remotes and collaboration

Book: swc-git §7, §11, §12

- ○ **PR-6.4.A** (SWC-GIT-7, SWC-GIT-12) Predict the state of the local and remote repositories after clone, push and pull.
  - EK: clone copies the whole history and names the source origin; push sends local commits; pull is fetch + merge; a push is rejected if the remote has commits you lack.
  - Needs: PR-6.2.A
  - P3

### 6.5 Branches and conflicts

Book: swc-git §13, §14, §15

- ○ **PR-6.5.A** (SWC-GIT-13) Create and switch branches, and predict which commits each branch contains after new commits and a merge.
  - EK: A branch is a movable pointer to a commit; git switch -c name creates one; a fast-forward merge only moves the pointer, otherwise merge makes a two-parent commit.
  - Needs: PR-6.4.A
  - P3
- ○ **PR-6.5.B** (SWC-GIT-15) Read conflict markers and resolve a merge conflict to a stated intended result.
  - EK: <<<<<<< HEAD marks your side, ======= separates, >>>>>>> branch ends theirs; edit to the final text, delete the markers, then add and commit.
  - Needs: PR-6.5.A
  - P4

## Unit 7 · Python

Big ideas: AAP, DAT

### 7.1 From Java to Python



- ○ **PR-7.1.A** (PY-1) Translate a short Java method into Python: indentation for blocks, no type declarations, print().
  - EK: A colon plus indentation marks a block; names are bound by assignment and carry no declared type; # starts a comment.
  - Needs: PR-2.4.B, PR-3.3.A
  - P2
- ○ **PR-7.1.B** (PY-1) Evaluate Python arithmetic with /, //, %, ** and mixed int/float, and say where it differs from Java.
  - EK: 7 / 2 = 3.5 always; 7 // 2 = 3 but −7 // 2 = −4 (floor, where Java truncates to −3); −7 % 2 = 1; ints never overflow; 2 ** 10 = 1024.
  - Needs: PR-7.1.A, PR-1.3.C
  - P3
- ○ **PR-7.1.C** (PY-1) Predict the truthiness of values and the result of and, or, not and chained comparisons.
  - EK: 0, 0.0, '', [], {} and None are falsy; and / or return one of their operands, not just True or False; 1 < x < 5 chains.
  - Needs: PR-7.1.A, PR-2.2.A
  - P3

### 7.2 Loops and range



- ○ **PR-7.2.A** (PY-2) List the values range(start, stop, step) produces and count them, including negative steps.
  - EK: range stops before stop: range(2, 10, 3) → 2, 5, 8; len(range(a, b)) = b − a; range(5, 0, −1) → 5, 4, 3, 2, 1.
  - Needs: PR-2.4.A, PR-7.1.A
  - P3
- ○ **PR-7.2.B** (PY-2) Trace for loops over lists, strings, enumerate and zip, and while loops with break and continue.
  - EK: for x in seq yields elements, not indices; enumerate yields (i, x); zip stops at the shorter sequence; break leaves the loop, continue skips to the next pass.
  - Needs: PR-7.2.A
  - P3

### 7.3 Lists, slicing and comprehensions



- ○ **PR-7.3.A** (PY-3) Evaluate indexing and slicing with negative indices and steps on lists and strings.
  - EK: s[−1] is the last element; s[a:b] runs a to b − 1; s[::−1] reverses; a slice out of range is empty, never an IndexError.
  - Needs: PR-7.2.A, PR-4.2.A
  - P3
- ○ **PR-7.3.B** (PY-3) Predict a list after append, extend, insert, pop and remove, and tell sort() from sorted().
  - EK: List methods change the list in place and return None (so a = a.sort() loses it); sorted() returns a new list.
  - Needs: PR-7.3.A
  - P3
- ○ **PR-7.3.C** (PY-3) Predict the effect of aliasing versus copying lists, including lists of lists.
  - EK: b = a aliases; a[:] or list(a) is a shallow copy; [[0] * 3] * 2 repeats one inner list, so changing one row changes both.
  - Needs: PR-7.3.B, PR-1.7.D
  - P3 · P4
- ○ **PR-7.3.D** (PY-3) Write and evaluate a list comprehension with a condition.
  - EK: [f(x) for x in seq if test(x)] filters, then maps, in one expression.
  - Needs: PR-7.3.B, PR-7.2.B
  - P2 · P3

### 7.4 Dictionaries and strings



- ○ **PR-7.4.A** (PY-4) Predict a dictionary after insertions, updates and deletions, and count items with one.
  - EK: Keys are unique; d[k] raises KeyError when k is missing, d.get(k, 0) does not; d[k] = d.get(k, 0) + 1 counts occurrences.
  - Needs: PR-7.3.B
  - P3
- ○ **PR-7.4.B** (PY-4) Evaluate string methods (split, strip, join, replace) and f-string formatting with a set precision.
  - EK: f'{x:.3f}' prints 3 decimals, f'{x:.2e}' scientific notation; split() with no argument splits on any run of whitespace.
  - Needs: PR-7.3.A
  - P3

### 7.5 Functions, modules and errors



- ○ **PR-7.5.A** (PY-5) Trace a function with default and keyword arguments and give its return value, including an implicit None.
  - EK: A function that reaches its end without return gives None; a default value is evaluated once, when the function is defined.
  - Needs: PR-7.1.A, PR-3.3.A
  - P3
- ○ **PR-7.5.B** (PY-5) Import names from a module and guard script code with if __name__ == '__main__'.
  - EK: import numpy as np binds a module name; code under the guard runs when the file is executed, not when it is imported.
  - Needs: PR-7.5.A
  - P2
- ○ **PR-7.5.C** (PY-5) Read a traceback to find the failing line and the exception type, and handle an expected error with try / except.
  - EK: Read a traceback bottom up: the last line names the exception, the frame just above it the line that raised it; catch only the exception you expect.
  - Needs: PR-7.5.A, PR-1.1.C
  - P4

### 7.6 Reading and writing files



- ○ **PR-7.6.A** (PY-6) Read a text file line by line in a with-block, skip a header, split fields and convert them to numbers.
  - EK: with open(path) as f closes the file automatically; each line keeps its newline until strip(); float('1.5e-3') parses scientific notation.
  - Needs: PR-7.4.B, PR-7.5.C, PR-4.5.A
  - P2

## Unit 8 · Scientific computing with NumPy

Big ideas: NUM, DAT

### 8.1 NumPy arrays



- ○ **PR-8.1.A** (SCI-1) Create arrays with np.array, zeros, ones, arange and linspace, and give their shape, dtype and length.
  - EK: np.arange(0, 1, 0.25) excludes the end (4 values); np.linspace(0, 1, 5) includes it (5 values, spacing 0.25); all-integer input gives an int dtype.
  - Needs: PR-7.3.A, PR-7.5.B
  - P3
- ○ **PR-8.1.B** (SCI-1) Index and slice 1-D and 2-D arrays, including x[:, 0], x[1:, ::2] and boolean masks.
  - EK: x[i, j] is row i, column j; x[:, j] is column j; a slice is a view (writing to it changes x), x[mask] is a copy.
  - Needs: PR-8.1.A, PR-4.7.A
  - P3
- ○ **PR-8.1.C** (SCI-1) Reduce an array along an axis (sum, mean, max) and give the shape of the result.
  - EK: For shape (R, C), axis=0 collapses the rows and leaves C values (one per column); axis=1 leaves R; no axis gives a single number.
  - Needs: PR-8.1.B
  - P3

### 8.2 Vectorisation and broadcasting



- ○ **PR-8.2.A** (SCI-2) Replace an explicit loop with an element-wise array expression that gives the same result.
  - EK: x**2 + 3*x acts element by element in compiled code — typically 10–100× faster than the same Python loop.
  - Needs: PR-8.1.C, PR-4.4.A
  - P2
- ○ **PR-8.2.B** (SCI-2) Decide whether two shapes broadcast and give the result's shape.
  - EK: Align shapes from the right; each pair of dimensions must be equal or 1: (3, 1) with (4,) gives (3, 4); (3,) with (4,) fails.
  - Needs: PR-8.2.A
  - P3
- ○ **PR-8.2.C** (SCI-2) Tell element-wise * from the matrix product @ and give the shape of each result.
  - EK: (n, k) @ (k, m) → (n, m); * needs broadcastable shapes and multiplies matching entries.
  - Needs: PR-8.2.B
  - P3
- ○ **PR-8.2.D** (SCI-2) Compute all pairwise distances among N particles by broadcasting, giving each intermediate shape.
  - EK: r[:, None, :] − r[None, :, :] has shape (N, N, 3); the norm over the last axis gives the (N, N) distance matrix, zero on the diagonal.
  - Needs: PR-8.2.B
  - P2 · P3

### 8.3 Reading data files



- ○ **PR-8.3.A** (SCI-3) Load a numeric text file with np.loadtxt or np.genfromtxt using delimiter, skiprows and usecols, and give the shape of the result.
  - EK: Lines starting with # are skipped by default; a CSV needs delimiter=','; unpack=True returns the columns as separate arrays.
  - Needs: PR-8.1.A, PR-7.6.A
  - P2 · P3
- ○ **PR-8.3.B** (SCI-3) Compute summary statistics of a column (mean, std, min, argmax) and select the rows that meet a condition.
  - EK: np.argmax returns the index, not the value; np.std divides by N unless ddof=1 (sample standard deviation).
  - Needs: PR-8.3.A, PR-8.1.C
  - P3 · P6
- ○ **PR-8.3.C** (SCI-3) Save an array to a text or .npy file and reload it unchanged.
  - EK: np.save / np.load keep dtype and full precision; np.savetxt writes text, set fmt and header for readable columns.
  - Needs: PR-8.3.A
  - P2

### 8.4 Plotting



- ○ **PR-8.4.A** (SCI-4) Plot y against x with matplotlib, label the axes with units, add a legend and save the figure.
  - EK: plt.plot(x, y, label='…'); plt.xlabel('t (ps)'); plt.legend(); call plt.savefig('fig.png', dpi=300) before plt.show().
  - Needs: PR-8.3.A
  - P2
- ○ **PR-8.4.B** (SCI-4) Choose linear, semilog or log-log axes from the expected relationship, and read an exponent or rate from the straight line.
  - EK: y = a·e^(−kt) is straight on semilog-y with slope −k (natural log); y = a·xⁿ is straight on log-log with slope n.
  - Needs: PR-8.4.A
  - P6

### 8.5 An MD-style integration loop



- ○ **PR-8.5.A** (SCI-5) Write a forward-Euler loop for dy/dt = f(y, t), compute the number of steps, and give y after a few steps.
  - EK: y_(n+1) = y_n + Δt·f(y_n, t_n); steps = T/Δt; global error shrinks in proportion to Δt.
  - Needs: PR-8.1.A, PR-2.5.A
  - P2 · P3
- ○ **PR-8.5.B** (SCI-5) Integrate a 1-D harmonic oscillator with velocity Verlet and trace the first steps.
  - EK: v += (Δt/2)·a; x += Δt·v; a = F(x)/m; v += (Δt/2)·a — one force evaluation per step.
  - Needs: PR-8.5.A
  - P2 · P3
- ○ **PR-8.5.C** (SCI-5) Track total energy along a trajectory and diagnose a timestep that is too large.
  - EK: Velocity Verlet keeps the energy bounded, oscillating about its start; Euler's energy grows steadily; Δt should be a small fraction (≲ 1/20) of the fastest period.
  - Needs: PR-8.5.B, PR-8.4.A
  - P6
- ○ **PR-8.5.D** (SCI-5) Compute the Lennard-Jones energy and force for a pair of particles, then vectorise it over all pairs.
  - EK: U = 4ε[(σ/r)¹² − (σ/r)⁶]; F(r) = (24ε/r)[2(σ/r)¹² − (σ/r)⁶]; minimum at r = 2^(1/6)σ with U = −ε.
  - Needs: PR-8.5.C, PR-8.2.D
  - P2 · P6

### 8.6 Reproducible numerical scripts



- ○ **PR-8.6.A** (SCI-6) Seed a random number generator so a run reproduces exactly, and draw initial velocities from a normal distribution.
  - EK: rng = np.random.default_rng(seed); rng.normal(0, σ, size=(N, 3)); the same seed gives the same stream.
  - Needs: PR-8.1.A, PR-1.6.D
  - P2 · P6
- ○ **PR-8.6.B** (SCI-6) Test a numerical function against a case with a known answer, using a tolerance.
  - EK: np.isclose / np.allclose with rtol and atol; e.g. a harmonic oscillator must return to its start after one period 2π√(m/k).
  - Needs: PR-1.5.C, PR-7.5.A, PR-8.5.B
  - P6
- ○ **PR-8.6.C** (SCI-6) Organise an analysis as a script with functions and command-line arguments that writes its outputs to files, run from the shell and tracked in Git.
  - EK: Inputs from sys.argv or argparse, results to files, no hand edits between steps — so one command reruns everything.
  - Needs: PR-7.5.B, PR-5.4.B, PR-8.3.C, PR-6.1.B
  - P2 · P5

## Unit 9 · Computing systems, networks and impact (extension)

Big ideas: CSN, DAT, IOC

### 9.1 The internet and fault tolerance

Book: csp-ced §4.1, §4.2

- ○ **PR-9.1.A** (CSN-1.A, CSN-1.B, CSN-1.C) Describe how data crosses the internet in packets, and what IP, TCP, HTTP and DNS each do.
  - EK: Data is split into packets that may take different routes and arrive out of order; IP addresses and routes, TCP reassembles and resends, DNS maps names to addresses, HTTP carries web requests.
  - P5

### 9.2 Parallel and distributed computing

Book: csp-ced §4.3

- ○ **PR-9.2.A** (CSN-2.A, CSN-2.B) Compute the run time and speedup of a workload split across processors.
  - EK: Parallel time = sequential part + the longest parallel branch; speedup = sequential time / parallel time, capped by the part that cannot be split.
  - P3

### 9.3 Compression

Book: csp-ced §2.2

- ○ **PR-9.3.A** (DAT-1.D) Choose lossless or lossy compression for a kind of data, and run-length encode a short string.
  - EK: Lossless restores every bit (text, code, trajectories); lossy discards detail people won't notice (photos, audio); AAAABB → 4A2B.
  - Needs: PR-1.2.B
  - P3 · P5

### 9.4 Impact of computing

Book: csp-ced §5.1, §5.2, §5.3, §5.6

- ○ **PR-9.4.A** (IOC-1.A, IOC-1.B, IOC-1.C, IOC-1.D) Identify beneficial and harmful effects of a computing innovation, including the digital divide and bias built into its data.
  - EK: One innovation can help some groups and harm others; unequal access and unrepresentative training data both shift who benefits.
  - Needs: PR-4.1.B
  - P5
