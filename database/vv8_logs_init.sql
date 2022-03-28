-- This file will initialize the database for Visible V8 log storage and
-- all of the tables required to run it. Ideally this file will be run
-- every time a VV8 container is initiated via DockerCompose.

-- Create global entity id sequence
CREATE SEQUENCE IF NOT EXISTS vv8_logs_entity_seq
    AS bigint;

-- Create submissions table
CREATE TABLE IF NOT EXISTS submissions (
    submission_id bigint PRIMARY KEY,
    start_time timestamp NOT NULL,
    end_time timestamp,
    url_scheme varchar(126) NOT NULL,
    url_domain varchar NOT NULL,
    url_path varchar NOT NULL,
    url_query_params varchar NOT NULL,
    url_fragment varchar NOT NULL
);
CREATE INDEX IF NOT EXISTS submissions_url_domain_index
    ON submissions (url_domain);

-- Create relationship table
CREATE TABLE IF NOT EXISTS relationships (
    relationship_id bigint PRIMARY KEY,
    relationship_type varchar(250) NOT NULL,
    from_entity bigint NOT NULL,
    to_entity bigint NOT NULL,
    submission_id bigint NOT NULL
        REFERENCES submissions(submission_id)
);
CREATE INDEX IF NOT EXISTS relationships_from_entity_index
    ON relationships (from_entity);
CREATE INDEX IF NOT EXISTS relationships_to_entity_index
    ON relationships (to_entity);

-- Create isolates table
CREATE TABLE IF NOT EXISTS isolates (
    isolate_id bigint PRIMARY KEY
        DEFAULT nextval('vv8_logs_entity_seq'),
    isolate_value bigint,
    submission_id bigint NOT NULL
        REFERENCES submissions(submission_id)
);

-- Creates window_origins table
CREATE TABLE IF NOT EXISTS window_origins (
    window_origin_id bigint PRIMARY KEY
        DEFAULT nextval('vv8_logs_entity_seq'),
    isolate_id bigint NOT NULL,
    url text,
    submission_id bigint NOT NULL
        REFERENCES submissions(submission_id)
);

-- Create execution_contexts table
CREATE TABLE IF NOT EXISTS execution_contexts (
    context_id bigint PRIMARY KEY
        DEFAULT nextval('vv8_logs_entity_seq'),
    window_id bigint
        REFERENCES window_origins(window_origin_id),
    isolate_id bigint
        REFERENCES isolates(isolate_id),
    sort_index integer NOT NULL,
    url text,
    script_id varchar(250),
    src text,
    submission_id bigint NOT NULL
        REFERENCES submissions(submission_id)
);

-- Create log_entries table
CREATE TABLE IF NOT EXISTS log_entries (
    log_entry_id bigint PRIMARY KEY
        DEFAULT nextval('vv8_logs_entity_seq'),
    sort_index integer NOT NULL,
    log_type varchar(250) NOT NULL,
    src_offset integer NOT NULL,
    context_id bigint
        REFERENCES execution_contexts(context_id),
    function varchar(250),
    arguments text,
    property varchar(250),
    object varchar(250),
    submission_id bigint NOT NULL
        REFERENCES submissions(submission_id)
);
CREATE INDEX IF NOT EXISTS log_entries_log_type
    ON log_entries (log_type);
