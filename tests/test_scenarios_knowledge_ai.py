from scenario_industry_helpers import (
    assert_industry_scenarios_valid,
    load_report,
    slugs_by_class,
)


def test_knowledge_ai_industry_scenarios_validate_and_match_goldens() -> None:
    assert_industry_scenarios_valid("knowledge-ai")


def test_knowledge_ai_retrieval_posture_moves_from_lexical_to_hybrid() -> None:
    internal = load_report("knowledge-ai", "01-internal-eng-knowledge-search")
    assert {"full_text_search", "pg_trgm"} <= (
        slugs_by_class(internal, "recommend_now") | slugs_by_class(internal, "candidate_later")
    )
    assert "pgvector" in slugs_by_class(internal, "not_enough_evidence")

    support = load_report("knowledge-ai", "02-customer-support-ai-assistant-backend")
    assert {"full_text_search", "pgvector"} <= slugs_by_class(support, "recommend_now")

    research = load_report("knowledge-ai", "03-research-corpus-with-hybrid-retrieval")
    assert {"full_text_search", "pg_trgm", "pgvector", "row_level_security"} <= slugs_by_class(
        research, "recommend_now"
    )
