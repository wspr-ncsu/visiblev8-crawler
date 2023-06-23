-- Record of each processed log file
CREATE TABLE IF NOT EXISTS logfile (
	id SERIAL PRIMARY KEY NOT NULL,	-- PG ID for FKs from other tables
	mongo_oid BYTEA NOT NULL,	    -- Mongo vv8log OID of raw log data record
	uuid TEXT NOT NULL UNIQUE,		-- Unique UUID for this log file
	root_name TEXT NOT NULL,		-- Root name of log file as originally stored (prefix of all segment names)
	size BIGINT NOT NULL,			-- Aggregate size (bytes) of all log segments processed
	lines INT NOT NULL,				-- Aggregate size (lines) of all log segments processed
	submissionid TEXT		-- Submission ID of the log file
);

CREATE TABLE IF NOT EXISTS script_blobs (
	id SERIAL PRIMARY KEY NOT NULL,
	script_hash BYTEA NOT NULL,
	script_code TEXT NOT NULL,
	sha256sum BYTEA NOT NULL,
	size INT NOT NULL
);

CREATE TABLE IF NOT EXISTS adblock (
	id SERIAL PRIMARY KEY NOT NULL,
	url TEXT NOT NULL,
	origin TEXT NOT NULL,
	blocked BOOLEAN NOT NULL -- If the url,origin was blocked by brave adblock (using easylist and easyprivacy)
);

CREATE TABLE IF NOT EXISTS thirdpartyfirstparty (
	id SERIAL PRIMARY KEY NOT NULL,
	sha2 BYTEA NOT NULL,										-- SHA256 of script code
	root_domain TEXT NOT NULL, 									-- Root domain (the initial URL being loaded by pupeteer) of script if availiable
	url TEXT NOT NULL,											-- URL of script if availiable
	first_origin TEXT NOT NULL, 								-- First origin in which the script was loaded if availiable
	property_of_root_domain TEXT NOT NULL,						-- Tracker radar "property" (company name) of root domain if availiable, else eTLD+1 of the URL
	property_of_first_origin TEXT NOT NULL,						-- Tracker radar "property" (company name) of first origin if availiable, else eTLD+1 of the URL
	property_of_script TEXT NOT NULL,							-- Tracker radar "property" (company name) of script if availiable, else eTLD+1 of the URL
	is_script_third_party_with_root_domain BOOLEAN NOT NULL,	-- Is the script third party with respect to the root domain?
	is_script_third_party_with_first_origin BOOLEAN NOT NULL,   -- Is the script third party with respect to the first origin in which it was loaded?
	script_origin_tracking_value double precision NOT NULL      -- Tracking value as assigned by duckduckgo tracking radar
);

CREATE TABLE IF NOT EXISTS xleaks (
	id SERIAL PRIMARY KEY NOT NULL,
	isolate TEXT NOT NULL,
	visiblev8 BOOLEAN NOT NULL,
	first_origin TEXT,
	url TEXT,
	evaled_by INT -- REFERENCES script_flow (id)
);

CREATE TABLE IF NOT EXISTS js_api_features_summary (
	logfile_id INT REFERENCES logfile (id) NOT NULL,
	all_features JSON NOT NULL
);

CREATE TABLE IF NOT EXISTS script_flow (
	id SERIAL PRIMARY KEY NOT NULL,
	isolate TEXT NOT NULL, -- V8 isolate pointer
	visiblev8 BOOLEAN NOT NULL, -- Is the script loaded by the browser/injected by VisibleV8 (in most cases you want to ignore scripts if this is true)
	code TEXT NOT NULL,
	first_origin TEXT,
	url TEXT,
	apis TEXT[] NOT NULL,	-- All APIs loaded by a script in the order they were executed
	evaled_by INT -- REFERENCES script_flow (id)
);

-- Feature usage information (for monomorphic callsites)
CREATE TABLE IF NOT EXISTS feature_usage (
	id SERIAL PRIMARY KEY NOT NULL,
	logfile_id INT REFERENCES logfile (id) NOT NULL,
	visit_domain TEXT NOT NULL,
	security_origin TEXT NOT NULL,
	script_hash BYTEA NOT NULL,
	script_offset INT NOT NULL,
	feature_name TEXT NOT NULL,
	feature_use CHAR NOT NULL,
	use_count INT NOT NULL
);

CREATE TABLE IF NOT EXISTS multi_origin_obj (
	id SERIAL PRIMARY KEY NOT NULL,
	objectid SERIAL NOT NULL,
	origins TEXT[] NOT NULL,
	num_of_origins INT NOT NULL,
	urls TEXT[] NOT NULL
);

CREATE TABLE IF NOT EXISTS multi_origin_api_names (
	id SERIAL PRIMARY KEY NOT NULL,
	objectid SERIAL NOT NULL,
	origin TEXT NOT NULL,
	api_name TEXT NOT NULL
);

-- Script creation records (only URL/eval causality included)
CREATE TABLE IF NOT EXISTS script_creation (
	id SERIAL PRIMARY KEY NOT NULL,
	isolate_ptr TEXT, -- V8 isolate pointer
	logfile_id INT REFERENCES logfile (id) NOT NULL,
	visit_domain TEXT NOT NULL,
	script_hash BYTEA NOT NULL,
	script_url TEXT,
	runtime_id INT,
	first_origin TEXT,
	eval_parent_hash BYTEA
);

-- Feature usage information (for polymorphic callsites)
CREATE TABLE IF NOT EXISTS poly_feature_usage (
	id SERIAL PRIMARY KEY NOT NULL,
	logfile_id INT REFERENCES logfile (id) NOT NULL,
	visit_domain TEXT NOT NULL,
	security_origin TEXT NOT NULL,
	script_hash BYTEA NOT NULL,
	script_offset INT NOT NULL,
	feature_name TEXT NOT NULL,
	feature_use CHAR NOT NULL,
	use_count INT NOT NULL
);

-- Script causality/provenance enum type
CREATE TYPE script_genesis AS ENUM (
	'unknown',         -- No pattern (or multiple ambiguous patterns) match genesis data
	'static',          -- No parent, URL provided (appears to be loaded in document HTML [of some frame])
	'eval',            -- Eval-parent (redundant/overlap with script_creation, but that's life)
	'include',         -- Direct HTMLScriptElement.src manipulation matches subsequent URL-load of script
	'insert',          -- Direct HTMLScriptElement.text(et al.) manipulation matches SHA256 of subsequent non-URL-load of script
	'write_include',   -- Document.write-injected <script src="..." /> that matches subsequent URL-load of script
	'write_insert');   -- Document.write-injected <script>...</script> that matches SHA256 of subsequent non-URL-load of script

-- Script causality/provenance link data
CREATE TABLE IF NOT EXISTS script_causality (
	id SERIAL PRIMARY KEY NOT NULL,
	logfile_id INT REFERENCES logfile (id) NOT NULL,
	visit_domain TEXT NOT NULL,
	child_hash BYTEA NOT NULL,
	genesis script_genesis NOT NULL DEFAULT 'unknown',
	parent_hash BYTEA,
	by_url TEXT,
	parent_cardinality INT,
	child_cardinality INT
);

-- Source/origin of document.createElement calls
CREATE TABLE IF NOT EXISTS create_elements (
	id SERIAL PRIMARY KEY NOT NULL,
	logfile_id INT REFERENCES logfile (id) NOT NULL,
	visit_domain TEXT NOT NULL,
	security_origin TEXT NOT NULL,
	script_hash BYTEA NOT NULL,
	script_offset INT NOT NULL,
	tag_name TEXT NOT NULL,
	create_count INT NOT NULL
);

-- [VPC-specific] table of page/logfile/{set-of-detected-captchas} records
CREATE TABLE IF NOT EXISTS page_captcha_systems (
	id SERIAL PRIMARY KEY NOT NULL,
	page_mongo_oid BYTEA NOT NULL,
	logfile_mongo_oid BYTEA NOT NULL,
	captcha_systems JSONB NOT NULL
);
