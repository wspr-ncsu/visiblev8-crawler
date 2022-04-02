-- This file will initialize the database for Visible V8 log storage and
-- all of the tables required to run it. Ideally this file will be run
-- every time a VV8 container is initiated via DockerCompose.

-- Create schema
CREATE SCHEMA vv8_logs

-- Create global entity id sequence
CREATE SEQUENCE IF NOT EXISTS vv8_logs.vv8_logs_entity_seq
    AS bigint;

-- Create submissions table
CREATE TABLE IF NOT EXISTS vv8_logs.submissions (
    submission_id bigserial PRIMARY KEY,
    start_time timestamp NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    end_time timestamp,
    url_scheme varchar(126) NOT NULL,
    url_domain varchar NOT NULL,
    url_path varchar NOT NULL,
    url_query_params varchar NOT NULL,
    url_fragment varchar NOT NULL
);
CREATE INDEX IF NOT EXISTS submissions_url_domain_index
    ON vv8_logs.submissions (url_domain);

-- Create relationship table
CREATE TABLE IF NOT EXISTS vv8_logs.relationships (
    relationship_id bigserial PRIMARY KEY,
    relationship_type varchar(250) NOT NULL,
    from_entity bigint NOT NULL,
    to_entity bigint NOT NULL,
    submission_id bigint NOT NULL
        REFERENCES vv8_logs.submissions(submission_id)
);
CREATE INDEX IF NOT EXISTS relationships_from_entity_index
    ON vv8_logs.relationships (from_entity);
CREATE INDEX IF NOT EXISTS relationships_to_entity_index
    ON vv8_logs.relationships (to_entity);

-- Create isolates table
CREATE TABLE IF NOT EXISTS vv8_logs.isolates (
    isolate_id bigint PRIMARY KEY
        DEFAULT nextval('vv8_logs.vv8_logs_entity_seq'),
    isolate_value bigint,
    submission_id bigint NOT NULL
        REFERENCES vv8_logs.submissions(submission_id)
);
CREATE INDEX IF NOT EXISTS isolates_submission_id_index
    ON vv8_logs.isolates (submission_id)

-- Creates window_origins table
CREATE TABLE IF NOT EXISTS vv8_logs.window_origins (
    window_origin_id bigint PRIMARY KEY
        DEFAULT nextval('vv8_logs.vv8_logs_entity_seq'),
    isolate_id bigint NOT NULL,
    url text,
    submission_id bigint NOT NULL
        REFERENCES vv8_logs.submissions (submission_id)
);
CREATE INDEX IF NOT EXISTS window_origins_submission_id_index
    ON vv8_logs.window_origins (submission_id)

-- Create execution_contexts table
CREATE TABLE IF NOT EXISTS vv8_logs.execution_contexts (
    context_id bigint PRIMARY KEY
        DEFAULT nextval('vv8_logs.vv8_logs_entity_seq'),
    window_id bigint
        REFERENCES vv8_logs.window_origins(window_origin_id),
    isolate_id bigint
        REFERENCES vv8_logs.isolates(isolate_id),
    sort_index integer NOT NULL,
    url text,
    script_id varchar(250),
    src text,
    submission_id bigint NOT NULL
        REFERENCES vv8_logs.submissions(submission_id)
);
CREATE INDEX IF NOT EXISTS execution_contexts_submission_id_index
    ON vv8_logs.execution_contexts (submission_id)

-- Create log_entries table
CREATE TABLE IF NOT EXISTS vv8_logs.log_entries (
    log_entry_id bigint PRIMARY KEY
        DEFAULT nextval('vv8_logs.vv8_logs_entity_seq'),
    sort_index integer NOT NULL,
    log_type varchar(250) NOT NULL,
    src_offset integer NOT NULL,
    context_id bigint
        REFERENCES vv8_logs.execution_contexts(context_id),
    function varchar(250),
    arguments text,
    property varchar(250),
    object varchar(250),
    submission_id bigint NOT NULL
        REFERENCES vv8_logs.submissions(submission_id)
);
CREATE INDEX IF NOT EXISTS log_entries_log_type
    ON vv8_logs.log_entries (log_type);
CREATE INDEX IF NOT EXISTS log_entries_submission_id_index
    ON vv8_logs.log_entries (submission_id)
