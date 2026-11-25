"""Programming drills (drills/problems/pr-*.yaml): answers are checked by running the code.

Java snippets run as the body of main() in a class Main, with any helper methods or nested classes
(`defs`) beside it, through `java Main.java` (single-file source launch, JDK 11 or later). Python
snippets run in a fresh python3. Output is compared as printed, with lines joined by " / " so a
multi-line output can be a choice option.
"""
import hashlib
import subprocess
import tempfile
from pathlib import Path

import sympy as sp

_CACHE: dict[str, str] = {}


def _run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=60)
    return r.stdout, r.stderr, r.returncode


def java_run(body: str, defs: str = "") -> str:
    """stdout of main() running `body`; an uncaught exception prints its class name instead"""
    src = ("import java.util.*;\npublic class Main {\n" + defs + "\npublic static void main(String[] args) {\n"
           "try {\n" + body + "\n} catch (RuntimeException | StackOverflowError e) { System.out.print(e.getClass().getSimpleName()); }\n}\n}\n")
    key = "java:" + hashlib.sha1(src.encode()).hexdigest()
    if key not in _CACHE:
        with tempfile.TemporaryDirectory() as d:
            Path(d, "Main.java").write_text(src)
            out, err, rc = _run(["java", "-Xss8m", "Main.java"], d)
            if rc != 0:
                raise RuntimeError(f"java failed:\n{src}\n{err[-2000:]}")
        _CACHE[key] = out
    return _CACHE[key]


def py_run(body: str) -> str:
    key = "py:" + hashlib.sha1(body.encode()).hexdigest()
    if key not in _CACHE:
        with tempfile.TemporaryDirectory() as d:
            Path(d, "snippet.py").write_text(body)
            out, err, rc = _run(["python3", "-I", "snippet.py"], d)
            if rc != 0:
                raise RuntimeError(f"python failed:\n{body}\n{err[-2000:]}")
        _CACHE[key] = out
    return _CACHE[key]


def _show(out: str) -> str:
    return " / ".join(l.rstrip() for l in out.strip("\n").split("\n"))


def _num(out: str):
    return sp.nsimplify(out.strip(), rational=True) if "." in out.strip() else sp.Integer(out.strip())


def java_out(code, defs=""):
    """the number main() prints"""
    return _num(java_run(code, defs))


def java_ret(defs, expr):
    """the number an expression prints, with helper methods `defs` in scope"""
    return _num(java_run(f"System.out.print({expr});", defs))


def java_pick(code, options, defs=""):
    """index of the option equal to the printed output (lines joined by ' / ')"""
    got = _show(java_run(code, defs))
    hits = [i for i, o in enumerate(options) if str(o) == got]
    if len(hits) != 1:
        raise ValueError(f"java printed {got!r}, options {options}")
    return hits[0]


def py_out(code):
    return _num(py_run(code))


def py_pick(code, options):
    got = _show(py_run(code))
    hits = [i for i, o in enumerate(options) if str(o) == got]
    if len(hits) != 1:
        raise ValueError(f"python printed {got!r}, options {options}")
    return hits[0]


def js_run(body: str) -> str:
    """stdout of a JavaScript snippet run by node (the event loop drains before exit)"""
    key = "js:" + hashlib.sha1(body.encode()).hexdigest()
    if key not in _CACHE:
        with tempfile.TemporaryDirectory() as d:
            Path(d, "snippet.js").write_text(body)
            out, err, rc = _run(["node", "snippet.js"], d)
            if rc != 0:
                raise RuntimeError(f"node failed:\n{body}\n{err[-2000:]}")
        _CACHE[key] = out
    return _CACHE[key]


def js_pick(code, options):
    got = _show(js_run(code))
    hits = [i for i, o in enumerate(options) if str(o) == got]
    if len(hits) != 1:
        raise ValueError(f"node printed {got!r}, options {options}")
    return hits[0]


def sh_run(setup: str, cmds: str) -> str:
    """stdout of `cmds` run by bash in a fresh directory after `setup` (not shown) has made its files;
    git commands get a throwaway identity and no global config"""
    key = "sh:" + hashlib.sha1((setup + "\0" + cmds).encode()).hexdigest()
    if key not in _CACHE:
        with tempfile.TemporaryDirectory() as d:
            env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": d, "LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1",
                   "GIT_AUTHOR_NAME": "A", "GIT_AUTHOR_EMAIL": "a@example.com", "GIT_COMMITTER_NAME": "A",
                   "GIT_COMMITTER_EMAIL": "a@example.com"}
            Path(d, "work").mkdir()
            r = subprocess.run(["bash", "-c", "set -e\ngit config --global init.defaultBranch main\n" + setup + "\n" + cmds],
                               cwd=Path(d, "work"), capture_output=True, text=True, timeout=60, env=env)
            if r.returncode != 0:
                raise RuntimeError(f"bash failed:\n{setup}\n{cmds}\n{r.stderr[-2000:]}")
            _CACHE[key] = r.stdout
    return _CACHE[key]


def sh_out(setup, cmds):
    return _num(sh_run(setup, cmds))


def sh_pick(setup, cmds, options):
    got = _show(sh_run(setup, cmds))
    hits = [i for i, o in enumerate(options) if str(o) == got]
    if len(hits) != 1:
        raise ValueError(f"bash printed {got!r}, options {options}")
    return hits[0]


def c_lines(body: str) -> int:
    """number of lines printed by a C main() body that may fork: stdout is unbuffered (as at a
    terminal, where printf flushes at each newline) and every process waits for its children"""
    src = ("#include <stdio.h>\n#include <unistd.h>\n#include <sys/wait.h>\nint main(void) {\n"
           "setvbuf(stdout, NULL, _IONBF, 0);\n" + body + "\nwhile (wait(NULL) > 0) ;\nreturn 0;\n}\n")
    key = "c:" + hashlib.sha1(src.encode()).hexdigest()
    if key not in _CACHE:
        with tempfile.TemporaryDirectory() as d:
            Path(d, "m.c").write_text(src)
            out, err, rc = _run(["cc", "-w", "-o", "m", "m.c"], d)
            if rc != 0:
                raise RuntimeError(f"cc failed:\n{src}\n{err[-2000:]}")
            out, err, rc = _run(["./m"], d)
        _CACHE[key] = out
    return sp.Integer(len(_CACHE[key].splitlines()))


FUNCS = {"js_pick": js_pick, "c_lines": c_lines, "sh_out": sh_out, "sh_pick": sh_pick, "java_out": java_out, "java_ret": java_ret, "java_pick": java_pick, "py_out": py_out, "py_pick": py_pick}


def check(p, H):
    """the programming cards are problems as data, checked by data.py with the functions above"""
    return None
