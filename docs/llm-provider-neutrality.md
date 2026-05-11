# LLM Provider Neutrality

`postgres-foundations` renders prompts but does not bake in a specific LLM
provider. The CLI writes Markdown prompt artifacts with structured context,
engine findings, rubrics, and expected response sections. Coaches can send those
artifacts to the model or CLI they trust.

Provider-neutrality keeps deterministic platform behavior separate from model
judgment:

- mechanical checks remain local and reproducible;
- prompts are plain Markdown files under `llm-prompts/`;
- hidden simulator notes are explicitly delimited;
- response shape is described inside each prompt; and
- LLM feedback is advisory unless a future integration records it explicitly.

Any provider response should preserve the requested Markdown sections, cite the
learner artifact or engine finding it relies on, distinguish missing evidence
from incorrect reasoning, and avoid replacing learner work with full solutions.
