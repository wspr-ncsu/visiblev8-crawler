-- Initialize database for tracking submissions via the backend

CREATE SCHEMA vv8_backend;

CREATE TABLE IF NOT EXISTS vv8_backend.submissions (
    id VARCHAR(36) PRIMARY KEY,
    start_time timestamp NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    end_time timestamp
        DEFAULT NULL,
    url TEXT NOT NULL,
    vv8_req_id TEXT NOT NULL,
    log_parser_req_id TEXT,
    mongo_id TEXT
);