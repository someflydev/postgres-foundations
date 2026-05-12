# Internal AI Knowledge Platform

A 500-person engineering organization has 80,000 documents and weekly growth. Engineers need exact keyword search, typo-tolerant discovery, semantic retrieval for conceptual questions, and hybrid ranking for mixed queries.

The system should run on plain managed PostgreSQL with pgvector available. It should not assume TimescaleDB, Citus, or a specialized search service. Your job is to design the relational model, search indexes, retrieval queries, and operational posture that make this realistic.
