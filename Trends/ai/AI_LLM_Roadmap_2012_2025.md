# AI & LLM Evolution Roadmap (2012-2025)
## A Comprehensive Chronological Analysis of Generative AI Development

---

## Part 1: Deep Learning Renaissance (2012-2017)

### 2012 | AlexNet & The Deep Learning Breakthrough

**Date:** 2012 (ImageNet competition)  
**Key Figure:** Krizhevsky et al., University of Toronto  
**Paper:** "ImageNet Classification with Deep Convolutional Neural Networks"  
**Impact Score:** Foundational (epoch marker)

The AlexNet architecture achieved ~70% top-1 accuracy on ImageNet, crushing traditional computer vision methods. Key innovations:
- Rectified Linear Units (ReLU) activation
- Dropout regularization to prevent overfitting
- GPU-accelerated training (NVIDIA GTX 580)
- Deep convolutional architecture (8 layers)

**Outcome:** Sparked the deep learning explosion. By 2019, algorithmic efficiency had improved such that training to AlexNet-level performance required 44x fewer FLOPs than in 2012 [web:70]—doubling every 16 months [web:70]. This efficiency gain surpassed Moore's Law (11x improvement).

---

### 2016-2017 | Transformer Revolution Preparation

**Date:** 2016-2017 (pre-publication research)  
**Key Institutions:** Google Brain, University of Toronto, Facebook AI Research  
**Status:** Theory development; practical applications not yet deployed

The transformer architecture emerged from sequence-to-sequence models, solving fundamental limitations of RNNs (vanishing gradients, poor long-range dependencies). Pre-2017 research established:
- Attention mechanisms (Bahdanau et al., 2014)
- Multi-head attention concepts
- Positional encoding strategies

---

### 2017 | "Attention Is All You Need" - The Transformer Paper

**Date:** June 2017  
**Institution:** Google Brain & University of Toronto  
**Paper:** "Attention Is All You Need" (Vaswani et al.)  
**Venue:** NeurIPS 2017  
**Citation Count:** 70,000+ (one of most-cited ML papers)  
**Available:** arXiv:1706.03762

**Core Contribution:** Introduced the Transformer architecture—a purely attention-based sequence model with no recurrence or convolution. Key components:
- Self-attention layers (allowing parallel processing)
- Multi-head attention (8-12 independent attention subspaces)
- Feed-forward networks
- Positional encoding (sine/cosine patterns)
- Layer normalization and residual connections

**Why It Mattered:**
1. **Parallelization:** Unlike RNNs, sequences could be processed in parallel, enabling scaling to massive datasets
2. **Long-range dependencies:** Attention weights directly connect distant tokens
3. **Efficient pre-training:** Foundation for modern transfer learning

**Immediate Applications:**
- Machine translation (seq2seq problems)
- Natural language understanding
- Became the basis for all modern LLMs

**Benchmark:** BLEU score improvements on English-German translation (+2.0 BLEU), English-French (+1.0 BLEU) compared to prior RNN/CNN baselines.

---

## Part 2: Pre-Trained Language Model Era (2018-2019)

### 2018 | BERT & GPT-1: Competing Paradigms Emerge

#### BERT (Google)
**Date:** October 2018  
**Institution:** Google AI Language  
**Paper:** "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"  
**Key Metrics:** Outperformed prior SOTA on 11 NLP benchmarks  
**Architecture:** 12-layer transformer (base), 24-layer (large), trained on masked language modeling

**Innovation:** Bidirectional context. Prior models (ELMo, GPT-1) only used left-to-right or right-to-left context. BERT masked 15% of tokens and trained the model to predict them using context from both directions.

**Benchmark Results (GLUE benchmark):**
- BERT-base: 78.3% (prior best: 70%)
- BERT-large: 80.4%
- Outperformed human baselines on several tasks

#### GPT-1 (OpenAI)
**Date:** June 2018  
**Institution:** OpenAI (Radford et al.)  
**Paper:** "Improving Language Understanding by Generative Pre-Training"  
**Model Size:** 117M parameters  
**Training:** Unsupervised pre-training on 40GB of text, then task-specific fine-tuning

**Innovation:** Unified approach—the same model fine-tuned on diverse tasks (sentiment, entailment, similarity, question-answering). Demonstrated that **generative pre-training** could provide better transfer learning than discriminative approaches.

**Performance:** Achieved SOTA on 9 of 12 NLP tasks despite being smaller than specialized models.

**Philosophical Difference:**
- **BERT:** Masked language modeling (cloze task), bidirectional context. Excellent for understanding (classification, NER, QA)
- **GPT-1:** Causal language modeling (next-token prediction), left-to-right generation. Excellent for generation (translation, summarization, open-ended text)

#### ERNIE (Baidu)
**Date:** April 2019  
**Institution:** Baidu NLP Group  
**Paper:** "ERNIE: Enhanced Representation through Knowledge Integration"  
**Innovation:** Knowledge masking—masked entities and phrases, not just random tokens. Integrated external knowledge graphs into pre-training.

**Result:** Outperformed BERT on Chinese NLP tasks; foundation for Baidu's future models.

---

### 2019 | Scaling & Specialization

#### ERNIE 2.0 (Baidu)
**Date:** November 2019  
**Key Advance:** Continual pre-training framework; task-oriented pre-training. Multiple auxiliary objectives (semantic similarity, relation extraction, logic consistency).

**Result:** Outperformed BERT on 16 benchmarks including English GLUE tasks. Demonstrated that **diverse, task-aware pre-training** could exceed single-objective models.

#### GPT-2 (OpenAI)
**Date:** February 2019  
**Model Size:** 1.5B parameters (10x GPT-1)  
**Paper:** "Language Models are Unsupervised Multitask Learners"  
**Key Metric:** Zero-shot performance (no fine-tuning) on diverse tasks

**Breakthrough:** Demonstrated that scaling language models improved performance across diverse tasks without explicit task-specific training. Prompted concerns about misuse (text generation for disinformation) and led OpenAI to delay full model release initially.

**Scaling Law Discovery:** Larger models achieved better few-shot learning—a trend that would dominate the next decade.

---

## Part 3: Scaling Laws & The GPT-3 Era (2020-2022)

### 2020 | GPT-3: The Scaling Inflection Point

**Date:** June 2020  
**Institution:** OpenAI (Brown et al.)  
**Paper:** "Language Models are Few-Shot Learners"  
**Available:** arXiv:2005.14165  
**Model Size:** 175 billion parameters  
**Training Data:** 300 billion tokens (CommonCrawl, Wikipedia, books, code)  
**Training Time:** ~300 exaflop/s-days  
**Cost Estimate:** ~$5-10 million

**Unprecedented Capabilities:**
- Few-shot learning without gradient updates (prompt-in-context learning)
- Outperformed task-specific fine-tuned models on diverse tasks
- Arithmetic (2-digit addition): 96.3% accuracy
- Machine translation (zero-shot): Competitive with supervised models
- Code generation: Functional Python code from English descriptions

**Key Benchmark Results:**
- SuperGLUE: 87.1% (human baseline: 89.8%)
- SQuAD 2.0: 82.3% (fine-tuned models: 93%)
- LAMBADA (next-word prediction): 76% accuracy

**Scaling Laws Confirmed:** Compute, data, and model size are complementary. Doubling model size improved loss by ~0.05 nats (consistent with transformer scaling laws discovered by Kaplan et al., 2020).

**Business Impact:** OpenAI released GPT-3 via API (free trial, paid after). Sparked thousands of downstream applications (content generation, code completion, customer service).

### 2021 | Derivative & Optimization Work

#### ERNIE 3.0 (Baidu) — July 2021
**Paper:** "ERNIE 3.0: Large-scale Knowledge Enhanced Pre-training for Language Understanding and Generation"  
**Key Advance:** Unified framework fusing auto-regressive (generation) + auto-encoding (understanding) networks
**Benchmark:** Surpassed human baseline on SuperGLUE by +0.8% (90.6% vs. 89.8%) on July 3, 2021

**Deployment:** Baidu Maps integration (April 2021)—geography-and-language model for location understanding

#### OPT (Meta/Facebook) — June 2022
**Paper:** "OPT: Open Pre-trained Transformer Language Models"  
**Model Size:** 175B (matching GPT-3)  
**Key Metric:** 1/7th of GPT-3's carbon footprint (~900 metric tons CO2 vs. ~3,000)
**Approach:** Same scale, more efficient training. Released weights publicly (addressing GPT-3's closed-source model concern).

#### LLaMA (Meta) — February 2023
**Paper:** "LLaMA: Open and Efficient Foundation Language Models"  
**Model Sizes:** 7B, 13B, 30B, 65B  
**Training:** 1-2 trillion tokens on public datasets only (no proprietary data)
**Performance:** LLaMA-13B outperformed GPT-3 (175B) on most benchmarks using significantly fewer parameters

**Paradigm Shift:** Efficiency became competitive with scale. LLaMA-13B's performance on MMLU (53.3%) exceeded GPT-3 (54.9% with more parameters). This sparked the "efficiency revolution" in open-source AI.

---

## Part 4: The ChatGPT Moment & Public Awareness (2022-2023)

### November 30, 2022 | ChatGPT Public Release

**Date:** November 30, 2022, 00:00 UTC  
**Institution:** OpenAI  
**Model:** GPT-3.5 (optimized version of GPT-3 using RLHF)  
**Base Model:** Training ended December 2021; fine-tuning + RLHF applied after
**Availability:** Free trial; paid ChatGPT Plus ($20/month) launched in early 2023

**Milestone Metrics:**
- **100 million users** reached within 2 months (fastest growing consumer application at the time)
- **1 million signups** in first 5 days
- 533+ research papers published within 6-7 months (by early June 2023) [web:139]
- Over 500 papers with "ChatGPT" in title by April 2023 [web:138]

**Why ChatGPT Exploded (vs. prior API access):**
1. **Zero setup cost** — free to try
2. **Intuitive chat interface** — no API knowledge needed
3. **Impressive few-shot reasoning** — could explain its own logic
4. **Accessible to non-technical users** — reduced technical barrier
5. **Viral social media adoption** — students, journalists, professionals experimenting publicly

**Documented Capabilities (verified in early studies):**
- Medical diagnosis (87.3% accuracy on pediatric cases, comparable to physicians) [web:96]
- Software coding (functional code generation, bug detection)
- USMLE medical board exam: scored 82nd percentile (first-year medical student level)
- Bar exam (US legal): 90th percentile

---

### March 2023 | Competing Models Launch

#### GPT-4 (OpenAI) — March 14, 2023
**Type:** Multimodal (text + images, though initially limited)  
**Performance:** Surpassed human baseline on most professional exams
- Bar exam: 88th percentile (vs. ChatGPT 40th percentile)
- USMLE: 92nd percentile (vs. ChatGPT 64th percentile)
- SAT: 93rd percentile
- GRE Quantitative: 86th percentile, Verbal: 93rd percentile

**Known Architecture:** Larger, post-training refined (exact size undisclosed; estimates: 1-1.76 trillion parameters)

#### Bard (Google) — March 21, 2023
**Date:** Public limited beta in select countries  
**Base Model:** LaMDA (Language Model for Dialogue Applications), scaled up  
**Status:** Rushed to market in response to ChatGPT; showed inferior reasoning compared to GPT-4
**Initial Problems:** Hallucinations (e.g., falsely claimed JWST took first photos of exoplanet)

**Lesson:** Speed-to-market without adequate safety testing led to media criticism.

#### Claude (Anthropic) — March 2023
**Announced:** Constitutional AI training approach (aligning models via AI feedback on principles rather than just human feedback)  
**Model Size:** Not initially disclosed; later revealed ~52B parameters (claimed superior safety)
**Differentiator:** Long context window (100K tokens in later versions), emphasis on harmlessness

**Approach:** Constitutional AI—training models to follow specific principles (helpfulness, honesty, harmlessness) via AI-generated feedback based on written constitutions.

---

### July 18, 2023 | LLaMA 2 (Meta) — Open Competition Intensifies

**Date:** July 18, 2023  
**Model Sizes:** 7B, 13B, 70B  
**Release:** Fully open-source under Llama 2 Community License  
**Training:** 2 trillion tokens; instruction-tuned with RLHF

**Benchmark Performance:**
- LLaMA 2-70B: Competitive with GPT-3.5, closing the gap with GPT-4 on some tasks
- LLaMA 2-70B-Chat surpassed Llama 2 13B-Chat on human preference benchmarks

**Market Impact:** First high-quality 70B open model available to researchers; enabled fine-tuning for specialized domains (medical, legal).

---

### September 27, 2023 | Mistral 7B — Efficiency Record

**Date:** September 27, 2023  
**Institution:** Mistral AI (French startup, founded 2023)  
**Paper:** "Mistral 7B" (arXiv:2310.06825)  
**Key Innovations:**
- Grouped Query Attention (GQA) — reduces memory during inference
- Sliding Window Attention (SWA) — handles long sequences without full quadratic attention cost
- Flash Attention optimizations

**Performance:**
- Mistral 7B exceeded LLaMA 2 13B on math, reasoning, code
- Outperformed LLaMA 34B on multiple benchmarks while using 5x fewer parameters
- Inference cost: 3-5x lower than comparable models

**Business Model:** Open weights; supported via enterprise Mistral Cloud offering. Demonstrated that startups could compete with major labs on efficiency.

**Follow-up: Mistral 8x7B (Mixtral of Experts)** — January 8, 2024  
**Architecture:** Sparse Mixture of Experts (SMoE); 8 experts per token, 2 selected per token  
**Parameter Count:** 45B total, 12.9B active per token  
**Performance:** Outperformed LLaMA 2 70B on benchmarks, with 6x fewer active parameters

---

## Part 5: The Explosion of Alternatives & Chinese Models (2023-2024)

### 2023 | Chinese Model Acceleration

#### Qwen Series (Alibaba) — September 2023
**Date:** September 28, 2023  
**Paper:** "Qwen Technical Report" (arXiv:2309.16609)  
**Model Lineup:** Qwen (7B, 14B, 72B) + Qwen-Chat variants  
**Training:** Proprietary high-quality corpus  
**Multimodal:** Qwen-VL (vision-language) released October 2023

**Benchmark Highlights:**
- Qwen-72B: Competitive with GPT-3.5 on English; superior on Chinese tasks
- Qwen-VL: State-of-the-art on Chinese image understanding
- Instruction-tuned chat versions surpassed comparable open models

**Strategic Importance:** Alibaba's cloud presence enabled rapid deployment; direct competitor to OpenAI in China.

#### Zhipu ChatGLM — 2023
**Date:** March 2023 (Beta), June 2023 (ChatGLM2)  
**Institution:** Zhipu AI (knowledge partner: Tsinghua University)  
**Model Size:** ChatGLM-6B (open), ChatGLM2-6B improved  
**Focus:** Long context (supports 4K-8K tokens), optimized for Chinese

**Community Impact:** Most-downloaded Chinese LLM on Hugging Face in 2023.

#### Tencent Hunyuan — 2023+
**Development:** Reportedly large-scale model in development; released smaller versions for specific tasks

---

### 2024 | Consolidation & Reasoning Shift

#### April 2024 | LLaMA 3 (Meta)
**Model Sizes:** 8B, 70B  
**Improvements:**
- 8B-Instruct competitive with Mistral 7B and above
- 70B-Instruct competitive with GPT-4 on many tasks (though not all)
- Extended to 8K context (from LLaMA 2's 4K)

#### January 2024 | Mixtral of Experts — 45B Total (12.9B Active)
**Details in Part 4.**

---

### October 2024 | o1 Series (OpenAI) — Reasoning Models

**Date:** October 2024  
**Institution:** OpenAI  
**Paper:** "When a language model is optimized for reasoning, does it still show embers of autoregression?" (arXiv:2410.01792)  
**System Card:** Released December 2024  
**Paradigm Shift:** Explicit reasoning via reinforcement learning

**Core Mechanism:**
- Trained with large-scale reinforcement learning on chain-of-thought
- Pause before responding; allocate "thinking tokens" internally
- Performance measured on reasoning difficulty, not just speed

**Benchmark Performance:**
- AIME (math olympiad): 83% accuracy (vs. GPT-4o: 13%)
- Physics/Chemistry: Superior to GPT-4 on calculation-heavy tasks
- Tradeoff: Slower inference (seconds of thinking tokens)

**Key Finding:** o1 demonstrates that explicit reasoning steps—not just scale—improve performance on logic-heavy tasks. However, research shows o1 still exhibits autoregressive biases; reasoning is not perfect.

---

### December 2024 | Qwen 2.5 Series (Alibaba)

**Date:** December 2024 / January 2025  
**Models:** Qwen2.5 (0.5B-72B), Qwen2.5-Coder, Qwen2.5-VL  
**Paper:** "Qwen2.5 Technical Report" (arXiv:2412.15115)  
**Performance:** Qwen2.5-72B-Instruct outperforms comparable open models; competitive with GPT-3.5  
**Latest VL:** Qwen2.5-VL-72B matches GPT-4o and Claude 3.5 Sonnet on multimodal tasks (Feb 2025)

---

## Part 6: Technology Adoption Timeline

### By Topic

#### **Public API Access & Commercialization:**
- **June 2020:** GPT-3 API (OpenAI), free tier + pay-as-you-go
- **November 2022:** ChatGPT (free)
- **March 2023:** ChatGPT Plus ($20/month)
- **March 2023:** GPT-4 via API & web interface
- **September 2023:** Claude API (Anthropic)
- **Ongoing:** Mistral Cloud, Alibaba Cloud (Qwen), Google Cloud (Bard/Gemini)

#### **Academic Adoption:**
- **By June 2023:** 533 peer-reviewed papers on ChatGPT (Scopus)
- **2023-2024:** Universities debate AI in education; some ban, others integrate
- **2024:** Most major universities have AI literacy programs

#### **Enterprise Deployment:**
- **2023:** First Fortune 500 companies integrate generative AI into workflows
- **2024:** 60%+ of enterprises piloting or deploying LLMs (McKinsey survey)
- **2025 projection:** Mainstream integration in customer service, content creation, data analysis

---

## Part 7: Safety, Alignment & Governance (Parallel Evolution)

### Key Safety Milestones

**2022-2023:**
- OpenAI, Anthropic, Google publish papers on alignment and constitutional AI
- Red-teaming practices formalized
- NIST AI Risk Management Framework development (published V1.0, 2023)

**2024:**
- IEEE P3395 standard development (AI model safeguards)
- EU AI Act enforcement begins
- Executive orders on AI governance (US, UK, others)
- Watermarking and provenance tracking research accelerates

**2025 Outlook:**
- Regulatory frameworks increasingly concrete
- "Responsible AI" becoming competitive requirement
- Alignment research remains open problem (no consensus solution)

---

## Part 8: Key Institutions & Leadership

| Institution | Key Contribution | Notable Researchers |
|-------------|-----------------|-------------------|
| **Google Brain** | Transformer architecture, BERT, LaMDA | Vaswani, Devlin, Thawani |
| **OpenAI** | GPT-1/2/3, ChatGPT, GPT-4, o1 series | Radford, Brown, Amodei |
| **Meta** | LLaMA series, LLaMA 2, open approach | Touvron, Hardt |
| **Anthropic** | Constitutional AI, Claude series | Amodei, Christiano |
| **Baidu** | ERNIE series, production deployment | Wang et al. |
| **Alibaba** | Qwen series, multimodal | DAMO Academy |
| **Mistral AI** | Efficiency innovations (GQA, SWA) | Jiang, Soulié |
| **Zhipu AI** | ChatGLM, long-context Chinese models | Zhu et al. |
| **University of Toronto** | Transformer theory, scaling laws | Hinton, Bengio, LeCun |

---

## Part 9: Critical Transitions & Lessons

### 1. **From Supervised Learning to Self-Supervised Pre-Training (2017-2020)**
Pre-2017, NLP relied on task-specific supervised learning. Transformers + self-supervised pre-training (predict next token, mask prediction) enabled transfer learning at scale.

### 2. **From Fine-Tuning to In-Context Learning (2020-2023)**
GPT-3 proved models could learn from examples in context (few-shot) without gradient updates. Eliminated need for task-specific fine-tuning for many applications.

### 3. **From Closed Models to Open Ecosystems (2023-2024)**
- Early: GPT-3 (closed, API-only)
- Transition: LLaMA leaked (April 2023), forcing Meta to open-source
- Result: Explosion of fine-tuned variants, democratized access
- Winners: Mistral, Qwen, open-source communities; losers: closed-source model advantage eroded

### 4. **Scaling Is No Longer Just About Parameters (2024)**
- Mistral 7B outperformed LLaMA 34B
- o1 showed reasoning > brute-force scaling
- Qwen2.5 matched GPT-3.5 at 72B (competitive architecture, not 10x scale)
- Lesson: Efficiency, training data quality, and post-training matter as much as size

### 5. **China's Rapid Model Iteration (2023-2025)**
- Qwen, ChatGLM, Hunyuan all reached GPT-3.5 parity within 18 months
- Technological parity achieved; competitive advantage now via **integration** (Alibaba Cloud) and **customization** (domain-specific fine-tuning)
- Regulatory differences (China's content restrictions) shaped model design choices

---

## Part 10: Timeline Summary Table

| Date | Organization | Model/Event | Size | Key Feature |
|------|--------------|------------|------|------------|
| **2012** | U Toronto | AlexNet | ~60M | CNNs win ImageNet |
| **2017.06** | Google Brain | Transformer | - | Attention-only architecture |
| **2018.06** | OpenAI | GPT-1 | 117M | Generative pre-training |
| **2018.10** | Google AI | BERT | 110M | Bidirectional context |
| **2019.02** | OpenAI | GPT-2 | 1.5B | Zero-shot multitask |
| **2019.04** | Baidu | ERNIE | - | Knowledge integration |
| **2020.06** | OpenAI | GPT-3 | 175B | Few-shot learning |
| **2023.02** | Meta | LLaMA | 13B-65B | Efficiency milestone |
| **2023.03** | OpenAI | GPT-4 | ~1T? | Multimodal, expert-level reasoning |
| **2023.03** | Google | Bard | - | Public launch |
| **2023.03** | Anthropic | Claude | ~52B | Constitutional AI |
| **2023.06** | Zhipu | ChatGLM2 | 6B-130B | Long context, Chinese |
| **2023.07** | Meta | LLaMA 2 | 70B | Fully open, RLHF |
| **2023.09** | Alibaba | Qwen | 72B | Multimodal vision |
| **2023.09** | Mistral | Mistral 7B | 7B | Efficiency leader |
| **2023.11** | OpenAI | o1 (preview) | - | Reasoning models in development |
| **2024.01** | Mistral | Mixtral 8x7B | 45B (12.9B active) | Sparse MoE |
| **2024.03** | Alibaba | Qwen-Coder | 7B-72B | Code specialization |
| **2024.04** | Meta | LLaMA 3 | 8B, 70B | Extended context |
| **2024.10** | OpenAI | o1 | - | Explicit chain-of-thought reasoning |
| **2024.12** | Alibaba | Qwen2.5 | 0.5B-72B | Multimodal, state-of-art |
| **2025.02** | Alibaba | Qwen2.5-VL | 72B | Matches GPT-4o, Claude 3.5 |

---

## Part 11: Unsolved Problems & Research Frontiers (As of Dec 2024)

1. **True Reasoning vs. Pattern Matching**: o1 improved but didn't solve. LLMs still conflate correlation with causation.

2. **Energy Efficiency**: AI datacenter demand threatens renewable targets. Nuclear options (Microsoft, Google, Amazon) signal infrastructure crisis.

3. **Long-Context Understanding**: Tokens can extend to 2M (Gemini 1.5), but understanding coherence over 1M+ tokens remains questionable.

4. **Alignment & Value Learning**: How do we scale alignment research? Constitutional AI promising but unproven at superhuman scales.

5. **Multimodal Generalization**: Vision-language models excel on benchmarks but fail on novel distributions. Real robustness unclear.

6. **Decoding Latency**: o1's reasoning comes at cost of latency (seconds to minutes). Real-time reasoning AI remains distant.

7. **Chinese/Non-English**: Parity achieved with English, but fundamental linguistic limitations (word boundaries, grammatical structures) suggest each language needs specialized research.

---

## References

### Primary Papers Cited
- Vaswani et al. (2017): "Attention is All You Need," NeurIPS 2017 [arXiv:1706.03762]
- Brown et al. (2020): "Language Models are Few-Shot Learners," NeurIPS 2020 [arXiv:2005.14165]
- Radford et al. (2018): "Improving Language Understanding by Generative Pre-Training" [OpenAI Blog]
- OpenAI (2024): "o1 System Card" [arXiv:2412.16720]
- Touvron et al. (2023): "LLaMA: Open and Efficient Foundation Language Models" [arXiv:2302.13971]
- Jiang et al. (2023): "Mistral 7B" [arXiv:2310.06825]
- Alibaba (2024): "Qwen2.5 Technical Report" [arXiv:2412.15115]

### Key Datasets & Benchmarks
- ImageNet (computer vision baseline, 2012-present)
- GLUE / SuperGLUE (NLP understanding)
- SQuAD (reading comprehension)
- MMLU (multitask language understanding)
- HumanEval (code generation)
- AIME, MATH (mathematical reasoning)

### Broader Context
- NIST AI Risk Management Framework (2023)
- IEEE P3395 (AI standards, in development)
- EU AI Act (enforcement phase, 2024-2025)
- Executive Order on AI (US, October 2023)

---

**Report Generated:** December 2025  
**Scope:** 2012-2025 AI/LLM evolution with focus on research publications, benchmarks, and deployment milestones  
**Coverage:** Western (OpenAI, Google, Meta, Anthropic, Mistral) and Chinese (Baidu, Alibaba, Zhipu, Tencent) developments  
**Note on Dates:** Where specific publication dates unavailable, announcement/deployment dates used as proxies.
