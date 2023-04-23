import os
import re
import sys


removed = {
    "aiomysql",
    "aiosqlite",
    "associationproxy_toplevel",
    "asyncio_events_run_async",
    "asyncio_inspector",
    "asyncio_install",
    "asyncio_orm_avoid_lazyloads",
    "asyncio_scoped_session",
    "asyncio_toplevel",
    "asyncmy",
    "asyncpg_prepared_statement_cache",
    "asyncpg_prepared_statement_name",
    "automap_by_module",
    "automap_intercepting_columns",
    "automap_toplevel",
    "azure_synapse_ignore_no_transaction_on_rollback",
    "baked_in",
    "baked_toplevel",
    "baked_with_before_compile",
    "change_3907",
    "change_3953",
    "change_4109",
    "composite_association_proxy",
    "composite_operations",
    "context_default_functions",
    "core_inspection_toplevel",
    "custom_version_counter",
    "cx_oracle_setinputsizes",
    "dataclasses_pydantic",
    "declarative_inheritance",
    "declarative_many_to_many",
    "declarative_mixins",
    "declarative_relationship_eval",
    "declarative_table_args",
    "declarative_toplevel",
    "defaults_client_invoked_sql",
    "defaults_sequences",
    "dialect-postgresql-asyncpg",
    "dynamic_relationship",
    "examples_adjacencylist",
    "examples_asyncio",
    "examples_caching",
    "examples_inheritance",
    "examples_instrumentation",
    "examples_performance",
    "examples_session_orm_events",
    "examples_sharding",
    "examples_toplevel",
    "examples_versioned_history",
    "examples_versioned_rows",
    "examples_versioning",
    "feature_joins_09",
    "generic_functions",
    "horizontal_sharding_toplevel",
    "hybrid_pep484_naming",
    "hybrids_toplevel",
    "inspection_toplevel",
    "legacy_is_orphan_addition",
    "mapper_column_property_sql_expressions",
    "mapper_column_property_sql_expressions_composed",
    "mapper_composite",
    "mapper_sql_expressions",
    "mapper_version_counter",
    "mapping_columns_toplevel",
    "metadata_defaults",
    "metadata_defaults_toplevel",
    "metadata_reflection",
    "metadata_reflection_dbagnostic_types",
    "metadata_reflection_schemas",
    "metadata_reflection_toplevel",
    "migration_2992",
    "migration_3061",
    "mssql_comment_support",
    "mssql_identity",
    "mssql_indexes",
    "mssql_insert_behavior",
    "mssql_isolation_level",
    "mssql_pyodbc_access_tokens",
    "mssql_pyodbc_fastexecutemany",
    "mssql_pyodbc_setinputsizes",
    "mssql_reset_on_return",
    "mssql_toplevel",
    "mssql_triggers",
    "multipart_schema_names",
    "mutable_toplevel",
    "mypy_declarative_mixins",
    "mypy_toplevel",
    "mysql_indexes",
    "mysql_insert_on_duplicate_key_update",
    "mysql_isolation_level",
    "mysql_sql_mode",
    "mysql_storage_engines",
    "mysql_timestamp_onupdate",
    "mysql_toplevel",
    "oracledb",
    "oracle_isolation_level",
    "oracle_max_identifier_lengths",
    "oracle_toplevel",
    "orm_declarative_dataclasses",
    "orm_declarative_dataclasses_declarative_table",
    "orm_declarative_dataclasses_mixin",
    "orm_declarative_dc_mixins",
    "orm_declarative_native_dataclasses",
    "orm_declarative_native_dataclasses_non_mapped_fields",
    "orm_imperative_dataclasses",
    "postgresql_alternate_search_path",
    "postgresql_column_valued",
    "postgresql_constraint_options",
    "postgresql_indexes",
    "postgresql_insert_on_conflict",
    "postgresql_isolation_level",
    "postgresql_match",
    "postgresql_operator_classes",
    "postgresql_psycopg",
    "postgresql_readonly_deferrable",
    "postgresql_reset_on_return",
    "postgresql_simple_match",
    "postgresql_table_valued",
    "postgresql_table_valued_overview",
    "proxying_dictionaries",
    "psycopg2_executemany_mode",
    "pysqlcipher",
    "pysqlite_regexp",
    "pysqlite_serializable",
    "pysqlite_serializable                         ",
    "pysqlite_threading_pooling",
    "reflection_overriding_columns",
    "relationships_backref",
    "server_defaults",
    "server_side_version_counter",
    "session_expire",
    "session_object_states",
    "session_referencing_behavior",
    "sqlite_autoincrement",
    "sqlite_foreign_keys",
    "sqlite_include_internal",
    "sqlite_isolation_level",
    "sqlite_on_conflict_ddl",
    "sqlite_on_conflict_insert",
    "sqlite_toplevel",
    "triggered_columns",
    "unitofwork_contextual",
    "unitofwork_merging",
    "write_only_relationship",
}


def fixlink(m):
    print(f"MATCH: {m}")
    if m.group(1) in removed:
        return f"ref_{m.group(1)}"
    else:
        return m.group(0)


def fix(path):
    print(f"path: {path}")
    with open(path) as file_:
        text = file_.read()
        text = re.sub(r":ref:`.+ <(.+?)>`", fixlink, text)
        print("NEXT PASS")
        text = re.sub(r":ref:`(.*?)`", fixlink, text)

    with open(path, "w") as file_:
        file_.write(text)


for root, dir_, files in os.walk(sys.argv[1]):
    for file_ in files:
        if ".venv" in root:
            continue
        if file_.endswith(".rst") or file_.endswith(".py"):
            path = os.path.join(root, file_)
            fix(path)
