# The Master Timeline: AI Research & Engineering (2017–2025)

## 2017: The Architecture
*   **June 12:** **Google Brain** publishes *"Attention Is All You Need"*. The Transformer architecture is born.
    *   *Significance:* Replaces RNNs/LSTMs; enables parallel training on massive datasets.

## 2018–2019: Pre-training & Fine-tuning
*   **Oct 2018:** **Google** releases **BERT**.
    *   *Significance:* Introduces bidirectional training; dominates NLP benchmarks.
*   **Feb 2019:** **OpenAI** releases **GPT-2** (1.5B parameters).
    *   *Significance:* Demonstrates that "next token prediction" can generate coherent paragraphs.

## 2020: The Scale Hypothesis
*   **May 28:** **OpenAI** releases **GPT-3** paper.
    *   *Key Insight:* Scaling Laws (Kaplan et al.). 175B parameters. Emergent abilities (few-shot learning) appear without specific training.
*   **Dec 23:** **DeepMind** releases **AlphaFold 2** (CASP14).
    *   *Impact:* Solves the protein folding problem, proving AI's utility in fundamental biology.

## 2021: Multimodality & Code
*   **Jan 5:** **OpenAI** releases **DALL-E** (Images) and **CLIP** (Text-Image pairing).
*   **June:** **Microsoft/GitHub** launch **Copilot** (based on OpenAI Codex).
    *   *Impact:* First mass-market deployment of LLMs for productivity.

## 2022: The "Chinchilla" Correction & Generative Boom
*   **March 29:** **DeepMind** publishes **Chinchilla** paper.
    *   *Key Insight:* Most models (like GPT-3) are *undertrained*. Compute is better spent on *more data*, not *larger models*.
*   **April:** **Google** releases **PaLM** (540B).
*   **May:** **FlashAttention** paper published (Tri Dao).
    *   *Significance:* Hardware-aware exact attention; makes training long-context models feasible.
*   **Aug:** **Stability AI** releases **Stable Diffusion** (Open Source).
*   **Nov 30:** **OpenAI** launches **ChatGPT** (based on GPT-3.5).

## 2023: The "Chat" War & Open Source Renaissance
*   **Feb 24:** **Meta** releases **LLaMA-1** (Research only).
    *   *Significance:* Triggers the open-source fine-tuning explosion (Alpaca, Vicuna).
*   **March 14:** **OpenAI** releases **GPT-4**.
    *   *Specs:* MoE architecture (rumored), multimodal, human-level professional exam performance.
*   **March 14:** **Anthropic** releases **Claude 1**.
*   **May:** **DPO (Direct Preference Optimization)** paper published (Rafailov et al.).
    *   *Significance:* Removes the need for complex RLHF pipelines; simplifies alignment.
*   **July 18:** **Meta** releases **Llama 2** (Open Weights).
*   **Sept:** **Falcon 180B** (TII) released.
*   **Oct 10:** **Mistral AI** releases **Mistral 7B**.
    *   *Significance:* Outperforms Llama 2 13B; defines the "small but mighty" category.
*   **Nov:** **01.AI** (China) releases **Yi-34B**.
*   **Dec:** **Google** releases **Gemini 1.0**.
*   **Dec:** **Mamba** paper published (Gu & Dao).
    *   *Significance:* State Space Models (SSMs) challenge Transformers for efficiency.

## 2024: Reasoning, Long Context, & "China Speed"
*   **Jan 8:** **Mistral** releases **Mixtral 8x7B** (MoE).
*   **Feb 15:** **Google** releases **Gemini 1.5 Pro**.
    *   *Spec:* **1 Million Token Context Window** (later 2M). Kill-feature for RAG.
*   **March 4:** **Anthropic** releases **Claude 3 Family** (Opus, Sonnet, Haiku).
    *   *Milestone:* Claude 3 Opus surpasses GPT-4 on Leaderboards.
*   **April 18:** **Meta** releases **Llama 3** (8B & 70B).
*   **May:** **DeepSeek** releases **DeepSeek-V2**.
    *   *Innovation:* **MLA (Multi-head Latent Attention)** reduces KV cache by 93%. Pricing war begins ($0.14/1M tokens).
*   **June 21:** **Anthropic** releases **Claude 3.5 Sonnet**.
    *   *Status:* Widely considered the "smartest" coding model of 2024.
*   **July:** **Meta** releases **Llama 3.1** (405B).
*   **Sept 12:** **OpenAI** releases **o1-preview ("Strawberry")**.
    *   *Paradigm Shift:* **System 2 Reasoning**. Chain-of-Thought is baked into training and inference.
*   **Sept 19:** **Alibaba** releases **Qwen 2.5** (0.5B to 72B).
    *   *Status:* The strongest open-weights model to date, beating Llama 3.1 in math/coding.
*   **Dec:** **DeepSeek** releases **DeepSeek-V3** (671B MoE).
    *   *Impact:* Matches GPT-4o/Claude 3.5 performance; trained on just ~2K GPUs (vs. Nvidia's 100K clusters).

## 2025: Autonomous Agents & Self-Reasoning (Current Era)
*   **Jan:** **DeepSeek** releases **DeepSeek-R1**.
    *   *Significance:* First open-source "Reasoning" model (o1 rival). Uses pure RL (Reinforcement Learning) without SFT (Supervised Fine-Tuning) to discover thinking patterns.
*   **Jan:** **DeepSeek** paper *"The Watson to Doctors"*.
    *   *Application:* Medical diagnosis via reasoning models reaches expert parity.
*   **Feb:** **OpenAI** (implied) / Research Community explores **"Thinking Retrievers" (O1 Embedder)**.
    *   *Concept:* Models that reason *before* they search the web/database.
*   **March:** **xLSTM 7B** paper released.
    *   *Trend:* Revival of recurrent architectures (LSTM) with modern scaling to handle infinite context with constant memory.
*   **April:** **Stanford/HAI** releases **AI Index Report 2025**.
    *   *Finding:* "The price of intelligence has dropped 100x in 24 months."
*   **Aug:** **Goedel-Prover-V2** released.
    *   *Milestone:* Automated Theorem Proving. AI systems can formally verify software code at scale.
*   **Oct:** **Agentic AI in Gaming** survey published.
    *   *Trend:* AI moves from "NPCs" to "Game Masters" that generate infinite content in real-time.
