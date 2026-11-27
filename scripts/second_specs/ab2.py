"""Second question types for the three AI Basics objectives that listed one drill (Nov 2026)."""
FILE, FRAMEWORK = "ab-second-types", "ai-basics"
from opl_dsl import Q

M = "Symbol('m')"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
ADD = []


def N(code, name, skill, prompt, value, verify, explain, tex="answer", **kw):
    ADD.append((code, Q(name, skill, prompt, value=value, tex=tex, verify=verify, explain=explain, **kw)))


def L(code, name, skill, prompt, options, rows, explain):
    ADD.append((code, Q(name, skill, prompt, pace="recall", cases=[{"q": a, "kc": k} for a, k in rows], choice=options, correct="kc", verify="authored", explain=explain)))


def F(code, name, skill, rows, explain):
    ADD.append((code, Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows], choice=MC, correct="0", verify="authored", explain=explain)))


def C(keys, rows):
    return [dict(zip(keys.split(), r)) for r in rows]


L("AB-1.1.A", "ab-field-pick", "aib.concepts", "{{q}} is best described as:", ["AI, but not machine learning", "Machine learning, but not deep learning", "Deep learning, but not generative", "Generative AI"], [
  ("A chess program that follows hand-written rules", 0), ("A decision tree trained to flag spam", 1), ("A convolutional network that labels photos", 2), ("A large language model chatbot", 3),
  ("A linear regression that predicts house prices from data", 1), ("A diffusion model that makes images from text", 3), ("An expert system built from if-then rules written by doctors", 0)],
  "Ask in turn: does it learn from data? Does it use a deep neural network? Does it produce new content rather than a label or a number?")
N("AB-4.1.D", "ab-parameters-that-fit", "aib.llms", "A device has {{kg}} GB free for model weights (1 GB = 10⁹ bytes). At {{kb}} bits per parameter, how many billion parameters fit?", "kg*8/kb",
  f"solve(Eq({M}*Rational(kb, 8), kg), {M})[0]", "Bytes per parameter = bits/8, and a billion parameters at one byte each is one GB. Halving the precision doubles what fits", tex="B",
  given={"kg": {"pick": [8, 16, 24, 48]}, "kb": {"pick": [4, 8, 16]}})
F("AB-6.1.B", "ab-prompt-fix-pick", "aib.use", [
  ("The answer is three times longer than you can use. The best fix is to:", "State the length and format you want", "Ask the same question again", "Add more background", "Switch to a different topic"),
  ("The model cites a paper that does not exist. The best fix is to:", "Give it the source text and ask it to quote only from that", "Ask it to be more confident", "Make the prompt shorter", "Ask for more citations"),
  ("The explanation is pitched at experts, and your reader is twelve. The best fix is to:", "Say who the reader is", "Ask for a longer answer", "Remove your question", "Ask it to use more technical terms"),
  ("You asked for three things and it did two. The best fix is to:", "List the requirements as numbered points", "Write the request as one long sentence", "Add praise", "Ask it to try harder")],
  "Name what is wrong with the answer, then change the one part of the prompt that controls it: length and format, source, audience, or the list of requirements")
assert len(ADD) == 3
