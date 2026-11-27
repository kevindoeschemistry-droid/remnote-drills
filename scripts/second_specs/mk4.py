"""Second question types for the three kindergarten objectives that still had one drill (Nov 2026)."""
from opl_dsl import Q

FILE, FRAMEWORK = "mk-second-types-4", "math-k8"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
ADD = [
 ("MK-1.4.A", Q("k2-attribute-tool", "k8.measurement", "Which would you use to find out {{q}}?", pace="recall",
    cases=[{"q": "how long a table is", "kc": 0}, {"q": "how heavy a pumpkin is", "kc": 1}, {"q": "how much milk is in a jug", "kc": 2}, {"q": "how tall you are", "kc": 0},
           {"q": "which of two apples is heavier", "kc": 1}, {"q": "how much water a bucket holds", "kc": 2}],
    choice=["A ruler or tape measure", "A scale or balance", "A measuring cup"], correct="kc", verify="authored",
    explain="Length is measured along a line, weight on a scale, and how much something holds by filling it")),
 ("MK-1.5.A", Q("k2-position-pick", "k8.geometry", "{{q}}", pace="recall",
    cases=[{"q": "A bird sits on top of a fence. The bird is ___ the fence.", "o1": "above", "o2": "below", "o3": "beside", "o4": "behind"},
           {"q": "A shoe is under the bed. The shoe is ___ the bed.", "o1": "below", "o2": "above", "o3": "in front of", "o4": "next to"},
           {"q": "Two children stand side by side. One is ___ the other.", "o1": "next to", "o2": "above", "o3": "below", "o4": "behind"},
           {"q": "In a line for lunch, Sam can see the back of Mia's head. Sam is ___ Mia.", "o1": "behind", "o2": "in front of", "o3": "above", "o4": "below"},
           {"q": "A round clock hangs over a square window. The shape above is a ___.", "o1": "circle", "o2": "square", "o3": "triangle", "o4": "rectangle"}],
    choice=MC, correct="0", verify="authored", explain="Position words say where one thing is compared with another: above, below, beside, in front of, behind, next to")),
 ("MK-1.5.E", Q("k2-solid-corners", "k8.geometry", "You build a {{s}} from sticks and clay balls, one ball at each corner. It uses {{ke}} sticks. How many clay balls do you need?", pace="quick",
    cases=[{"s": "cube", "ke": 12, "kf": 6}, {"s": "pyramid with a triangle base", "ke": 6, "kf": 4}, {"s": "pyramid with a square base", "ke": 8, "kf": 5}, {"s": "prism with triangle ends", "ke": 9, "kf": 5}],
    value="ke - kf + 2", tex="balls", verify="solve(Eq(x - ke + kf, 2), x)[0]", final=True,
    explain="Count the corners: a cube has 8, a triangle-base pyramid 4, a square-base pyramid 5, a triangle-end prism 6")),
]
