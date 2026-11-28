"""Write a new framework from a spec in scripts/second_specs (Nov 2026): the generic form of pm_setup.py.
A spec holds FW (id, title, code, domain, track, requires, level, primary, also, note, header, subject, source),
STDS (standards to register, each a dict as in drills/standards.yaml), SKILLS, IDEAS, PRACTICES and UNITS with the
two items inside each objective. This registers the standards, skills, domain, library subject and a source file for
the skills, and writes the framework with empty drill lists. Idempotent; nothing existing is overwritten.
Then run second_types.py.   Usage: python3 scripts/fw_setup.py hp mi"""
import importlib.util, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
q = lambda s: json.dumps(s, ensure_ascii=False)
fl = lambda xs: "[" + ", ".join(q(x) for x in xs) + "]"


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "scripts/second_specs", name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


for m in [load(n) for n in sys.argv[1:]]:
    F, d = m.FW, m.FW["domain"]
    p = os.path.join(ROOT, "drills/standards.yaml"); t = open(p).read()
    for s in m.STDS:
        if f'"id": "{s["id"]}"' not in t: t = t.rstrip("\n") + "\n- " + json.dumps(s, ensure_ascii=False) + "\n"
    open(p, "w").write(t)

    p = os.path.join(ROOT, "drills/skills.yaml"); L = open(p).read().split("\n")
    if not any(f"id: {d}," in ln for ln in L):
        i = next(k for k, ln in enumerate(L) if "id: gc," in ln and "domain:" not in ln)
        L.insert(i + 1, f'  - {{ id: {d}, title: {q(F["title"])} }}')
    if not any(f"domain: {d}," in ln for ln in L):
        i = max(k for k, ln in enumerate(L) if "domain: gc," in ln)
        L[i + 1:i + 1] = [f'  - {{ id: {d}.{a}, domain: {d}, title: {q(b)}, short: {q(c)}' + (f', prereqs: [{", ".join(pr)}]' if pr else "") + " }" for a, b, c, pr in m.SKILLS]
    open(p, "w").write("\n".join(L))

    S = F["source"]; p = os.path.join(ROOT, "drills/library.yaml"); L = open(p).read().split("\n")
    if not any(ln.strip() == f'- "{F["subject"]}"' for ln in L):
        i = next(k for k, ln in enumerate(L) if ln.strip() == '- "Graduate ChemE Methods"'); L.insert(i + 1, f'  - "{F["subject"]}"')
    if not any(ln.startswith(f"  {d}:") for ln in L):
        i = next(k for k, ln in enumerate(L) if ln.startswith("  gc:")); L.insert(i + 1, f'  {d}: "{F["subject"]}"')
    if not any(ln.startswith(f"  {S['id']}:") for ln in L):
        i = next(k for k, ln in enumerate(L) if ln.startswith("  cheme-grad-methods:")); L.insert(i + 1, f'  {S["id"]}: "{F["subject"]}"')
    open(p, "w").write("\n".join(L))

    p = os.path.join(ROOT, f"drills/sources/{S['id']}.yaml")
    if not os.path.exists(p):
        out = ["# " + ln for ln in S["note"]] + [f"id: {S['id']}", f"title: {q(S['title'])}", f"short: {q(S['short'])}", "year: 2026", f"field: {S['field']}", "chapters:"]
        out += [f"  - {{ n: {n + 1}, title: {q(c)}, skills: [{d}.{a}] }}" for n, (a, b, c, pr) in enumerate(m.SKILLS)]
        open(p, "w").write("\n".join(out) + "\n")

    p = os.path.join(ROOT, f"drills/frameworks/{F['id']}.yaml")
    if os.path.exists(p): continue
    out = [f"# {F['title']} — curriculum framework (draft 1, for Kevin's markup)", "#"] + ["# " + ln for ln in F["header"]] + [
           f"id: {F['id']}", f"title: {F['title']}", f"code: {F['code']}", "draft: 1", f"track: {F['track']}", f"requires: [{', '.join(F['requires'])}]",
           f"level: {F['level']}", f"domains: [{d}]", "", "basis:", f"  primary: {F['primary']}"] + ([f"  also: [{', '.join(F['also'])}]"] if F["also"] else []) + ([f"  wanted: [{', '.join(F['wanted'])}]"] if F.get("wanted") else []) + [
           "  note: " + q(F["note"]), "", "big_ideas:"]
    for i, ti, tx in m.IDEAS: out += [f"  - id: {i}", f"    title: {q(ti)}", f"    text: {q(tx)}"]
    out += ["", "practices:"]
    for i, ti, tx in m.PRACTICES: out += [f"  - id: {i}", f"    title: {ti}", "    text: " + q(tx)]
    out += ["", "units:"]
    for n, (uid, ti, std, ideas, topics) in m.UNITS.items():
        out += [f"  - id: {uid}", f"    n: {n}", f"    title: {q(ti)}", f"    std: {fl(std)}", "    scope: core", f"    ideas: [{', '.join(ideas)}]", "    topics:"]
        for tn, (tt, los) in topics.items():
            out += [f"      - n: {tn}", f"        title: {q(tt)}", "        los:"]
            for lid, lstd, do, ek, pr, _qs in los:
                out.append(f"          - {{ id: {lid}, std: {fl(lstd)}, do: {q(do)}, ek: [{q(ek)}], p: [{pr}], drills: [] }}")
    open(p, "w").write("\n".join(out) + "\n")
print("ok")
