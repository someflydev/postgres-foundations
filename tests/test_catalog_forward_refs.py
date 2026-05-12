import json

from pgfound import paths

PROMPT_41_CORE_FEATURES = {
    "arrays",
    "constraints",
    "exclusion_constraints",
    "expression_indexes",
    "full_text_search",
    "generated_columns",
    "jsonb",
    "logical_replication",
    "materialized_views",
    "multiranges",
    "partitioning",
    "physical_replication",
    "postgres_fdw",
    "ranges",
    "row_level_security",
    "partial_indexes",
}

PROMPT_41_EXTENSIONS = {
    "citus",
    "ltree",
    "pg_partman",
    "pg_stat_statements",
    "pg_trgm",
    "pgbouncer",
    "pgcrypto",
    "pgvector",
    "postgis",
    "postgres_fdw",
    "timescaledb",
    "unaccent",
}

PROMPT_41_INDEX_PATTERNS = {
    "btree_composite_equality_then_range",
    "btree_covering_include",
    "btree_equality",
    "brin_append_only_chronological",
    "expression_index_for_normalization",
    "gin_array_membership",
    "gin_jsonb_containment",
    "gin_trgm_similarity",
    "gist_geospatial",
    "gist_range_exclusion",
    "hnsw_vector_anns",
    "ivfflat_vector_anns",
    "partial_index_for_skew",
}

PROMPT_41_TOPOLOGY_PATTERNS = {
    "blue_green_upgrade_via_logical_replication",
    "citus_distributed_cluster",
    "logical_replication_pair",
    "logical_replication_to_analytics_replica",
    "pgbouncer_in_front",
    "postgres_fdw_federation",
    "primary_with_read_replicas",
    "single_primary",
}

PROMPT_41_ANTI_PATTERNS = {
    "arrays_over_child_tables",
    "fdw_without_pushdown_verification",
    "geo_logic_without_postgis",
    "jsonb_everything",
    "naive_wall_clock_timestamp",
    "no_pooling_high_connections",
    "no_restore_drills",
    "partition_too_early",
    "redundant_indexes",
    "replica_as_performance_bandage",
    "shard_without_distribution_key",
    "unused_indexes",
    "vacuum_starvation_by_long_txn",
    "vector_before_lexical",
}

FORWARD_REFERENCE_FIELDS = {
    "core_features_that_apply": PROMPT_41_CORE_FEATURES,
    "extensions_that_apply": PROMPT_41_EXTENSIONS,
    "index_patterns_that_apply": PROMPT_41_INDEX_PATTERNS,
    "topology_patterns_that_apply": PROMPT_41_TOPOLOGY_PATTERNS,
    "anti_patterns_to_watch": PROMPT_41_ANTI_PATTERNS,
}


def _catalog(name: str) -> list[dict]:
    path = paths.DECISION_ENGINE_DIR / "catalogs" / name
    return json.loads(path.read_text(encoding="utf-8"))


def test_prompt_40_forward_references_match_prompt_41_catalog_plan() -> None:
    entries = _catalog("data_shapes.json") + _catalog("workload_patterns.json")

    for entry in entries:
        for field, planned_slugs in FORWARD_REFERENCE_FIELDS.items():
            unexpected = sorted(set(entry.get(field, [])) - planned_slugs)
            assert unexpected == [], f"{entry['id']} {field} has unplanned slugs: {unexpected}"
