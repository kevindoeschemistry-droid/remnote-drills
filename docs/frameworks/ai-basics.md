# AI Basics — curriculum framework (draft 1)

Generated from `drills/frameworks/ai-basics.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**19 learning objectives** in 10 units (19 core): 19 drilled, 0 partly, 0 with no drills. Core: 19 / 19 drilled.

## Big ideas

- **MATH · AI turns the world into numbers.** Images, words and sounds become vectors; a model is a function on those numbers with learned parameters.
- **LEARN · Models learn by shrinking a loss.** Training adjusts parameters to reduce error on data, and a model is judged on data it has not seen.
- **TOOL · A model is a tool with known limits.** It predicts likely text, knows only its training and its context, and is made useful and safe by grounding, tools and checking.

## Practices

- **P1 · Compute.** Carry a small AI calculation (a neuron, softmax, a parameter count, a cost) to a number.
- **P2 · Explain.** Name the concept or mechanism behind what a system does.
- **P3 · Judge.** Choose a model, a prompt fix or a safe response for a situation.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · What AI is | core | — | 1 | 1 | 0 | 0 |
| 2 · The world as numbers | core | — | 2 | 2 | 0 | 0 |
| 3 · Neural networks | core | — | 3 | 3 | 0 | 0 |
| 4 · Language models | core | — | 4 | 4 | 0 | 0 |
| 5 · Training | core | — | 3 | 3 | 0 | 0 |
| 6 · Using AI wisely | core | — | 2 | 2 | 0 | 0 |
| 7 · AI and tools | core | — | 1 | 1 | 0 | 0 |
| 8 · The toolbox | core | — | 1 | 1 | 0 | 0 |
| 9 · Staying safe | core | — | 1 | 1 | 0 | 0 |
| 10 · Big questions | core | — | 1 | 1 | 0 | 0 |

## Unit 1 · What AI is

Big ideas: MATH

### 1.1 AI, machine learning, deep learning, generative AI



- ● **AB-1.1.A** (harper-carroll-academy:1) Place a system in the nested fields AI ⊃ machine learning ⊃ deep learning ⊃ generative AI.
  - EK: ML learns from data; deep learning uses many-layer networks; generative AI produces new content.
  - P2 · drills: ab-ai-ml-dl

## Unit 2 · The world as numbers

Big ideas: MATH

### 2.1 Encoding and vectors



- ● **AB-2.1.A** (harper-carroll-academy:2) Say how images, text, audio and categories are encoded, and count the numbers in an image.
  - EK: Pixels × 3 channels; tokens → embeddings; one-hot for categories.
  - Needs: AB-1.1.A
  - P1 · P2 · drills: ab-represent, ab-pixels
- ● **AB-2.1.B** (harper-carroll-academy:2) Compute a dot product and a cosine similarity between vectors.
  - EK: Cosine = dot ÷ (lengths); 1 same direction, 0 unrelated.
  - Needs: AB-2.1.A
  - P1 · drills: ab-dot, ab-cosine

## Unit 3 · Neural networks

Big ideas: MATH

### 3.1 Neurons and layers



- ● **AB-3.1.B** (harper-carroll-academy:3) Name the parts of a network and say why activations must be nonlinear.
  - EK: Parameters, forward pass, backpropagation; stacked linear layers collapse to one.
  - Needs: AB-2.1.B
  - P2 · drills: ab-activation, ab-network-parts
- ● **AB-3.1.A** (harper-carroll-academy:3) Compute a neuron's output with ReLU or sigmoid.
  - EK: Weighted sum plus bias, then the activation.
  - Needs: AB-3.1.B
  - P1 · drills: ab-neuron, ab-sigmoid
- ● **AB-3.1.C** (harper-carroll-academy:3) Count the parameters of a fully connected layer or small network.
  - EK: Each neuron: one weight per input plus a bias.
  - Needs: AB-3.1.A
  - P1 · drills: ab-params-layer, ab-params-net

## Unit 4 · Language models

Big ideas: MATH, TOOL

### 4.1 Key terms and generation



- ● **AB-4.1.A** (harper-carroll-academy:4) Define token, context window, embedding, inference, attention, temperature and hallucination, and order the steps of generating text.
  - EK: Generation is repeated next-token prediction.
  - Needs: AB-3.1.C
  - P2 · drills: ab-llm-term, ab-next-token
- ● **AB-4.1.B** (harper-carroll-academy:4) Estimate token counts and how much text fits in a context window.
  - EK: About 0.75 English words per token.
  - Needs: AB-4.1.A
  - P1 · drills: ab-tokens, ab-context-pages
- ● **AB-4.1.C** (harper-carroll-academy:4) Compute next-token probabilities with softmax, with and without temperature.
  - EK: Low temperature sharpens, high flattens.
  - Needs: AB-4.1.B
  - P1 · drills: ab-softmax, ab-temperature
- ● **AB-4.1.D** (harper-carroll-academy:4) Convert a parameter count and precision to the memory the weights need.
  - EK: 16-bit = 2 bytes per parameter; a billion bytes ≈ 1 GB.
  - Needs: AB-4.1.C
  - P1 · drills: ab-weight-memory

## Unit 5 · Training

Big ideas: LEARN

### 5.1 How models learn



- ● **AB-5.1.A** (harper-carroll-academy:5) Classify a task as supervised, unsupervised, reinforcement or self-supervised learning, and name the stages of building a chat assistant.
  - EK: Pretraining, fine-tuning, feedback-based RL, then inference.
  - Needs: AB-3.1.C
  - P2 · drills: ab-learning-type, ab-train-stage
- ● **AB-5.1.B** (harper-carroll-academy:5) Take a gradient-descent step, compute a mean squared error and count training updates.
  - EK: w ← w − learning rate × gradient.
  - Needs: AB-5.1.A
  - P1 · drills: ab-gd-step, ab-mse, ab-steps
- ● **AB-5.1.C** (harper-carroll-academy:5) Diagnose overfitting and underfitting, name the data splits, and compute precision and recall.
  - EK: Judge on unseen data; precision is of what was flagged, recall of what was there.
  - Needs: AB-5.1.B
  - P1 · P2 · drills: ab-fit, ab-data-split, ab-precision, ab-recall

## Unit 6 · Using AI wisely

Big ideas: TOOL

### 6.1 Limits, trust and prompts



- ● **AB-6.1.A** (harper-carroll-academy:6) Explain hallucination, say what a model can know, and decide what to verify.
  - EK: Training data up to a cutoff, plus the context window; nothing else.
  - Needs: AB-4.1.D
  - P2 · P3 · drills: ab-hallucination, ab-what-model-knows
- ● **AB-6.1.B** (harper-carroll-academy:6) Choose the prompt change that fixes a given problem with an answer.
  - EK: Context, format, examples, steps.
  - Needs: AB-6.1.A
  - P3 · drills: ab-prompt-fix

## Unit 7 · AI and tools

Big ideas: TOOL

### 7.1 Agents and retrieval



- ● **AB-7.1.A** (harper-carroll-academy:7) Name the parts of an agent and the steps of its loop and of retrieval-augmented generation.
  - EK: Model + tools + memory + loop; embed, retrieve, answer from context.
  - Needs: AB-4.1.D
  - P2 · drills: ab-agent-part, ab-agent-loop, ab-rag-step

## Unit 8 · The toolbox

Big ideas: TOOL

### 8.1 Choosing and costing a model



- ● **AB-8.1.A** (harper-carroll-academy:8) Choose a kind of model for a job and work out what an API job costs.
  - EK: Input and output tokens are priced separately.
  - Needs: AB-7.1.A
  - P1 · P3 · drills: ab-model-choice, ab-api-cost

## Unit 9 · Staying safe

Big ideas: TOOL

### 9.1 Scams, deepfakes and privacy



- ● **AB-9.1.A** (harper-carroll-academy:9) Respond safely to a voice-clone, deepfake or phishing attempt, check where media came from, and decide what not to share with a chatbot.
  - EK: Verify through a channel you already trust; provenance beats detectors.
  - Needs: AB-6.1.B
  - P3 · drills: ab-scam-defense, ab-deepfake-check, ab-privacy

## Unit 10 · Big questions

Big ideas: LEARN

### 10.1 Scaling and alignment



- ● **AB-10.1.A** (harper-carroll-academy:10) Define scaling laws, alignment, AGI and foundation models, and estimate training compute and compute-optimal data.
  - EK: Compute ≈ 6 × parameters × tokens; about 20 tokens per parameter.
  - Needs: AB-9.1.A
  - P1 · P2 · drills: ab-big-ideas, ab-train-compute, ab-chinchilla
