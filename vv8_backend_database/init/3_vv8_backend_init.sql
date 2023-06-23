-- Initialize database for tracking submissions via the backend

CREATE TABLE IF NOT EXISTS submissions (
    id VARCHAR(36) PRIMARY KEY,
    start_time timestamp NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    end_time timestamp
        DEFAULT NULL,
    url TEXT NOT NULL,
    vv8_req_id TEXT NOT NULL,
    log_parser_req_id TEXT,
    postprocessor_used TEXT,
    postprocessor_output_format TEXT,
    postprocessor_delete_log_after_parsing BOOLEAN,
    crawler_args TEXT[],
    mongo_id TEXT
);