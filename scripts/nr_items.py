"""Write the NCLEX-RN 2026 Test Plan's 82 related-content headings (scripts/second_specs/nr3.py RC) into the
ncsbn-nclex-rn standard as items MOC.1 … PA.7, after the eight subcategory items. Idempotent."""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "scripts/second_specs"))
import nr3
p = os.path.join(ROOT, "drills/standards.yaml")
L = open(p).read().split("\n")
i = next(k for k, ln in enumerate(L) if ln.startswith("- { id: ncsbn-nclex-rn,"))
ln = L[i]
head = ln[:ln.index("items: [")]
top = re.findall(r'\{ code: "([A-Z]+)", title: "([^"]*)" \}', ln)
items = [f'{{ code: "{c}", title: "{t}" }}' for c, t in top]
items += [f'{{ code: "{c}.{n}", title: "{t}" }}' for c, ts in nr3.RC.items() for n, t in enumerate(ts, 1)]
note = ('note: "Read (Nov 2026): the eight Client Needs subcategories and their weights, the 82 related-content headings under them '
        '(items MOC.1 to PA.7, in the plan\'s order, titles lightly paraphrased), the integrated processes and the clinical judgment '
        'model\'s six steps. The activity statements under each heading were not read item by item. Weights are unchanged from the 2023 plan.", ')
head = re.sub(r'note: "[^"]*", ', note, head)
L[i] = head + "items: [" + ", ".join(items) + "] }"
open(p, "w").write("\n".join(L))
print(len(items), "items")
