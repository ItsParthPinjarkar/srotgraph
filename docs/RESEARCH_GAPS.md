# SrotGraph Research Gaps

**Version:** 1.0.0  
**Status:** Draft  
**Last Updated:** 2026-10-15

---

## 1. Purpose

This document identifies areas where we lack sufficient information to make informed decisions. It distinguishes between **verified findings** (things we know), **hypotheses** (things we assume but haven't validated), and **open questions** (things we need to research).

**Important:** This document explicitly avoids claiming novelty without supporting research. If similar systems exist, we should understand them and position SrotGraph accordingly.

---

## 2. Verified Findings

### 2.1 Technology Stack

| Finding | Evidence |
|---------|----------|
| FastAPI is a mature async Python web framework | Official docs, widespread adoption, 0.115+ releases |
| PostgreSQL supports JSONB, UUID, and async drivers | Official documentation, asyncpg library exists |
| Redis Streams provides consumer group semantics | Redis documentation, well-documented pattern |
| SQLAlchemy 2.0 supports async operations | Official documentation, async session support |
| Next.js 14+ has App Router with React Server Components | Official Next.js documentation |
| Pydantic v2 supports settings management | Official pydantic-settings documentation |

### 2.2 AI Provider Landscape

| Provider | Capability | Verified |
|----------|------------|----------|
| OpenAI Whisper | Local speech-to-text | Yes — open-source, runs locally |
| OpenAI GPT-4 | Text analysis, claim extraction | Yes — API documented |
| Anthropic Claude | Text analysis, claim extraction | Yes — API documented |
| Google Gemini | Text analysis, claim extraction | Yes — API documented |
| DeepGram | Cloud speech-to-text API | Yes — API exists |
| AssemblyAI | Cloud speech-to-text API | Yes — API exists |

### 2.3 Existing Related Work

*Note: This section requires research. What follows are hypotheses that need verification.*

**Hypothesized existing approaches:**

1. **Transcription-first tools** — Otter.ai, Descript, Rev focus on transcription with some speaker identification, but limited claim extraction
2. **Fact-checking databases** — Snopes, PolitiFact maintain claim databases but don't extract from live media
3. **Research literature analysis** — Various academic tools for paper analysis, but not general media
4. **Intelligence analysis tools** — Palantir, IBM i2 analyze relationships but are enterprise-focused, expensive, and not open-source

**Research needed:** Confirm these hypotheses and identify any open-source alternatives that overlap with SrotGraph's goals.

---

## 3. Hypotheses to Validate

### 3.1 Architectural Hypotheses

| Hypothesis | Validation Method | Priority |
|------------|-------------------|----------|
| Modular monolith is sufficient for initial scale | Implement and measure; extract workers if needed | High |
| Redis Streams is sufficient for job queue | Implement, measure throughput, compare with alternatives | Medium |
| PostgreSQL can handle the expected metadata load | Load testing with realistic data volumes | Medium |
| Local Whisper is fast enough for development | Benchmark on target hardware | High |

### 3.2 AI Capabilities Hypotheses

| Hypothesis | Validation Method | Priority |
|------------|-------------------|----------|
| LLMs can reliably extract timestamped claims from transcripts | Test with sample transcripts, measure precision/recall | High |
| LLMs can identify relationships between claims | Test with known claim pairs, measure accuracy | Medium |
| Confidence scores from LLMs are calibrated | Compare confidence to actual accuracy on test set | Medium |
| Multiple providers produce comparable results | Run same inputs through different providers, compare outputs | Low |

### 3.3 User Workflow Hypotheses

| Hypothesis | Validation Method | Priority |
|------------|-------------------|----------|
| Analysts want to review claims chronologically | User research, prototype testing | Medium |
| Claim validation should be binary (valid/invalid) or on a scale | User research | Medium |
| Evidence attachment improves claim verification speed | Measure time-to-verify with/without evidence | Low |

---

## 4. Open Questions

### 4.1 Core Functionality

| Question | Impact | Research Approach |
|----------|--------|-------------------|
| What is the minimum claim granularity? (sentence? clause? paragraph?) | High — affects extraction design | Literature review, user interviews |
| How do we define "claim" operationally? | High — affects extraction prompts | Define with examples, get agreement |
| How do we handle implied claims (not directly stated)? | Medium — affects extraction scope | Literature review on implied assertion detection |
| What timestamp precision is needed? (seconds? milliseconds?) | Low — centiseconds likely sufficient | User requirements gathering |

### 4.2 Accuracy & Metrics

| Question | Impact | Research Approach |
|----------|--------|-------------------|
| How do we establish ground truth efficiently? | High — needed for metrics | Investigate active learning, sampling strategies |
| What metrics matter most to users? | High — affects dashboard design | User research |
| How do we measure "information loss"? | Medium — affects metric design | Define operationally (e.g., % of transcript not covered by claims) |
| What is acceptable accuracy for MVP? | High — affects timeline | User research, competitive analysis |

### 4.3 Technical Decisions

| Question | Impact | Research Approach |
|----------|--------|-------------------|
| SQLite vs PostgreSQL for development? | Medium — affects dev experience | Compare setup complexity, feature parity |
| Should we use S3 or similar for object storage from the start? | Medium — affects deployment | Evaluate local vs cloud storage tradeoffs |
| What's the optimal transcript chunk size for claim extraction? | Medium — affects extraction quality | Experiment with different chunk sizes |
| Should we implement vector search now or later? | Low — pgvector can be added when needed | Wait until semantic search is actually required |

### 4.4 Competitive Landscape

| Question | Impact | Research Approach |
|----------|--------|-------------------|
| Are there open-source alternatives? | Medium — affects positioning | Search GitHub, academic papers |
| What do commercial tools charge? | Low — informs pricing if we ever charge | Research pricing pages |
| What features do existing tools lack? | High — informs differentiation | Feature comparison, user reviews |

---

## 5. Research Plan

### 5.1 Immediate (Before Phase 2)

1. **Benchmark Whisper on target hardware** — Measure transcription speed for typical audio lengths
2. **Test mock provider output quality** — Ensure deterministic output is useful for development
3. **Search for existing open-source projects** — Identify any similar systems

### 5.2 Before Phase 3

1. **Test real providers with sample data** — Compare outputs across providers
2. **Evaluate prompt strategies** — Test different prompts for claim extraction quality
3. **Establish evaluation methodology** — Define how we'll measure accuracy

### 5.3 Ongoing

1. **Monitor AI provider releases** — New models, API changes, pricing
2. **User feedback collection** — As soon as users have something to try
3. **Performance measurement** — Continuous benchmarking

---

## 6. Existing Related Work to Review

### 6.1 Open-Source Projects (To Research)

- **WhisperX** — Whisper with word-level timestamps
- **faster-whisper** — Optimized Whisper implementation
- **Silero** — Voice activity detection, speech-to-text
- **Haystack** — LLM orchestration framework
- **LangChain** — LLM application framework
- **Label Studio** — Data labeling tool (relevant for ground truth)

*Action: Search GitHub and Hugging Face for relevant projects.*

### 6.2 Academic Literature (To Research)

- Claim detection in text
- Temporal relation extraction
- Argument mining
- Fact verification
- Evidence extraction

*Action: Search academic databases for relevant papers.*

### 6.3 Commercial Products (To Research)

- Otter.ai
- Descript
- Trint
- Fireflies.ai
- Grain
- Various fact-checking platforms

*Action: Review feature lists, pricing, and user reviews.*

---

## 7. Research Constraints

1. **Do not claim novelty without evidence** — If similar systems exist, acknowledge them
2. **Do not invent benchmarks** — Only report measurements we've actually taken
3. **Do not overpromise AI capabilities** — LLMs have known limitations; be honest about them
4. **Distinguish research from development** — Research questions don't block development, but inform it

---

## 8. Decisions Requiring Research Before Implementation

| Decision | Research Needed | Can Proceed Without? |
|----------|-----------------|----------------------|
| Speech recognition provider priority | Benchmark comparisons | Yes — start with mock, add Whisper first |
| Claim extraction prompt strategy | Prompt testing | Yes — iterate on prompts, mock to start |
| Database for development | SQLite vs PostgreSQL tradeoff | Yes — PostgreSQL is target, SQLite acceptable for some tests |
| Object storage solution | Local vs cloud tradeoffs | Yes — local filesystem first, migrate later |
| Authentication approach | User needs, security requirements | Yes — add when needed, simple approach first |

---

*This document should be updated as research is completed and new questions emerge.*
