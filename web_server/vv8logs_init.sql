-- This file will initialize the database for Visible V8 log storage and
-- all of the tables required to run it. Ideally this file will be run
-- every time a VV8 container is initiated via DockerCompose.

-- JFAGAN
-- Create Database
CREATE DATABASE vv8_logs;

-- Create global entity id sequence
CREATE SEQUENCE IF NOT EXISTS vv8_logs_sequence
    AS bigint;

-- Create submissions table
CREATE TABLE IF NOT EXISTS submissions (
    submission_id biginteger PRIMARY KEY,
    start_time timestamp,
    end_time timestamp,
    url_scheme varchar(126) NOT NULL,
    url_domain varchar NOT NULL,
    url_path varchar NOT NULL,
    url_query_params NOT NULL,
    url_fragment NOT NULL
);

-- Create relationship table
CREATE TABLE IF NOT EXISTS relationship (
    relationship_id biginteger PRIMARY KEY,
    relationship_type varchar(250),
    from_entity biginteger NOT NULL,
    to_entity biginteger NOT NULL,
    submission_id biginteger NOT NULL,
        FOREIGN KEY REFERENCES submissions(submission_id),
);

-- SUBRNET
-- Create isolates table
CREATE TABLE IF NOT EXISTS isolates (
    isolate_id biginteger NOT NULL PRIMARY KEY,
    isolate_id_value biginteger,
    request_id big_integer NOT NULL,
        FOREIGN KEY REFERENCES submissions(submission_id),
);

-- Creates window_origins table
CREATE TABLE IF NOT EXISTS window_origins (
    window_origin_id biginteger NOT NULL PRIMARY KEY,
    isolate_id biginteger NOT NULL,
    url text,
    request_id big_integer NOT NULL
);

-- Create execution_contexts table
CREATE TABLE IF NOT EXISTS execution_contexts (
    contect_id biginteger NOT NULL PRIMARY KEY,
    window_id biginteger,
        FOREIGN KEY REFERENCES window_origins(window_origin_id),
    isolate_id biginteger,
        FOREIGN KEY REFERENCES isolates(isolate_id),
    sort_index integer NOT NULL,
    url text,
    script_id varchar(250),
    src text,
    request_id bitinteger NOT NULL,
        FOREIGN KEY REFERENCES submissions(submission_id),
);

-- Create log_entries table
CREATE TABLE IF NOT EXISTS log_entries (
    log_entry_id biginteger NOT NULL PRIMARY KEY,
    sort_index integer NOT NULL,
    log_type varchar(250) NOT NULL,
    src_offset integer NOT NULL,
    context_id biginteger,
        FOREIGN KEY REFERENCES execution_contexts(context_id),
    function varchar(250),
    arguments text,
    property varchar(250),
    object varchar(250),
    request_id biginteger NOT NULL,
        FOREIGN KEY REFERENCES submissions(submission_id),
);