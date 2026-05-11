from pgfound.llm import templates

BASE = {
    "allowed_concepts": ["select", "where", "primary_key", "index", "transaction"],
    "not_yet_allowed_concepts": ["window_function", "partitioning", "extension"],
}


def context_for(template_id: str) -> dict[str, object]:
    context: dict[str, object] = dict(BASE)
    context.update(
        {
            "concept_slug": "foreign_key",
            "lesson_context": "Foreign keys preserve references between tables.",
            "learner_level": "early",
            "learner_background": "backend engineer",
            "confusion_signal": "Learner thinks a join enforces relationship validity.",
            "learner_artifact": "select * from orders join customers using (customer_id);",
            "exercise_id": "first-select-write-query",
            "learner_sql": "select id from providers;",
            "reference_sql": "select id from providers;",
            "rubric_id": "query-correctness",
            "findings": [],
            "learner_schema": "create table customers (id bigint primary key);",
            "reference_schema": "create table customers (id bigint primary key);",
            "learner_index_plan": "create index on orders (customer_id);",
            "workload_description": "Lookup recent orders by customer.",
            "existing_schema": "create table orders (id bigint, customer_id bigint);",
            "query_examples": ["select * from orders where customer_id = 1;"],
            "scenario_id": "inventory-lost-update",
            "race_description": "Two sessions decrement the same row.",
            "proposed_fix": "select * from inventory where id = 1 for update;",
            "observed_trace": "both sessions read quantity 1",
            "reference_fix": "select ... for update",
            "learner_review_report": "# Review\nMissing invariant.",
            "learner_stage": "phase 3",
            "available_lessons": ["constraints-as-truth"],
            "available_exercises": ["first-select-write-query"],
            "exercise_level": "A",
            "exercise_prompt": "Write a simple SELECT.",
            "learner_attempt": "select * from providers;",
            "stuck_point": "I do not know which column to filter.",
            "common_mistake": "Using prose rules instead of constraints.",
            "domain_context": "Scheduling appointments.",
        }
    )
    return context


def test_training_templates_parse_and_render() -> None:
    loaded = templates.list_templates()

    assert {template.id for template in loaded} == templates.TRAINING_TEMPLATE_IDS
    for template in loaded:
        rendered = templates.render_template(template.id, context_for(template.id))
        assert rendered.strip()
        assert template.id.split("/", 1)[0] in {"coaching", "critique", "remediation", "shared"}
