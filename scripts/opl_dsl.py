"""DSL for the WeBWorK OPL gap-fill specs (scripts/opl_specs/*.py), used by scripts/opl_fill.py."""


class Q:
    """one template (one question)"""
    def __init__(self, name, skill, prompt, value=None, ask="Answer", tex="x", tol=0.0001, explain="", verify=None,
                 given=None, cases=None, let=None, require=None, pace="quick", choice=None, correct=None,
                 final=False, label="v", figure=None):
        self.__dict__.update(locals()); del self.__dict__["self"]

    def to_yaml(self):
        t = {"template": self.name, "skill": self.skill, "pace": self.pace}
        if self.given: t["given"] = self.given
        if self.cases: t["cases"] = self.cases
        if self.require: t["require"] = [self.require] if isinstance(self.require, str) else self.require
        if self.let: t["let"] = self.let
        if self.figure: t["figure"] = self.figure
        t["prompt"] = self.prompt
        fields = set(self.given or {}) | {k for c in (self.cases or []) for k in c} | set(self.let or {})
        if self.label in fields:
            self.label = next(l for l in ("v", "r", "y", "w", "ans_") if l not in fields)
        part = {"ask": self.ask, "label": self.label}
        if self.choice is not None:
            part["choice"] = self.choice
            part["correct"] = self.correct
        else:
            part["tex"] = self.tex
            part["value"] = self.value
            if self.final: part["final"] = True
            # cards print data to 4 significant figures and people answer to 3: accept 0.5% unless the
            # arithmetic itself is the skill (final). The verifier still checks the key to 1e-6.
            part["tol"] = self.tol if self.final else max(self.tol, 0.005)
        part["explain"] = self.explain
        t["parts"] = [part]
        v = self.verify
        if v == "authored": t["verify"] = {"authored": True}
        elif self.choice is not None: t["verify"] = {"choices": {self.label: v}}
        else: t["verify"] = {"expect": {self.label: v}}
        return t


class L:
    def __init__(self, id, do, ek, opl, qs, p="P1", std=None, drills=None, needs=None):
        self.id, self.do, self.ek, self.opl, self.qs, self.p, self.std = id, do, ek, opl, qs, p, std or []
        self.drills, self.needs = drills or [], needs or []  # existing templates and objectives to point at


class U:
    def __init__(self, n, uid, title, topics, std=None):
        self.n, self.uid, self.title, self.topics, self.std = n, uid, title, topics, std or []




class QP(Q):
    """one template with several chained parts (an exam-length problem). parts: list of dicts with
    label, ask, tex, value, verify, explain and optional tol/final. Pace defaults to workout."""
    def __init__(self, name, skill, prompt, parts, given=None, cases=None, let=None, require=None, pace="workout"):
        Q.__init__(self, name, skill, prompt, given=given, cases=cases, let=let, require=require, pace=pace)
        self.parts = parts

    def to_yaml(self):
        t = {"template": self.name, "skill": self.skill, "pace": self.pace}
        if self.given: t["given"] = self.given
        if self.cases: t["cases"] = self.cases
        if self.require: t["require"] = [self.require] if isinstance(self.require, str) else self.require
        if self.let: t["let"] = self.let
        t["prompt"] = self.prompt
        fields = set(self.given or {}) | {k for c in (self.cases or []) for k in c} | set(self.let or {})
        parts, expect = [], {}
        for p in self.parts:
            if p["label"] in fields: raise SystemExit(f"{self.name}: part label {p['label']} collides with a field")
            q = {"ask": p["ask"], "label": p["label"], "tex": p.get("tex", p["label"]), "value": p["value"]}
            if p.get("final"): q["final"] = True
            q["tol"] = p.get("tol", 0.0001) if p.get("final") else max(p.get("tol", 0.0001), 0.005)
            q["explain"] = p.get("explain", "")
            parts.append(q); expect[p["label"]] = p["verify"]
        t["parts"] = parts
        t["verify"] = {"expect": expect}
        return t
