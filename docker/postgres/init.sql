-- Create database if not exists
CREATE DATABASE IF NOT EXISTS threat_intelligence;

-- Connect to the database
\c threat_intelligence;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create custom types
DO $$ BEGIN
    CREATE TYPE severity_level AS ENUM ('critical', 'high', 'medium', 'low');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE indicator_type AS ENUM ('ip', 'domain', 'url', 'hash');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create tables
CREATE TABLE IF NOT EXISTS threats (
    id SERIAL PRIMARY KEY,
    cve_id VARCHAR(50) UNIQUE,
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    severity severity_level NOT NULL,
    cvss_score FLOAT,
    source VARCHAR(100) NOT NULL,
    published_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS indicators (
    id SERIAL PRIMARY KEY,
    indicator_type indicator_type NOT NULL,
    indicator_value VARCHAR(500) UNIQUE NOT NULL,
    risk_score FLOAT DEFAULT 0.0,
    source VARCHAR(100) NOT NULL,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS alert_logs (
    id SERIAL PRIMARY KEY,
    threat_id INTEGER REFERENCES threats(id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    severity severity_level NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    report_type VARCHAR(20) NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    summary TEXT NOT NULL,
    metrics JSONB NOT NULL,
    recommendations TEXT
);

-- Create indexes for performance
CREATE INDEX idx_threats_cve_id ON threats(cve_id);
CREATE INDEX idx_threats_severity ON threats(severity);
CREATE INDEX idx_threats_published_date ON threats(published_date);
CREATE INDEX idx_indicators_type ON indicators(indicator_type);
CREATE INDEX idx_indicators_value ON indicators(indicator_value);
CREATE INDEX idx_indicators_risk_score ON indicators(risk_score);
CREATE INDEX idx_alerts_threat_id ON alert_logs(threat_id);
CREATE INDEX idx_alerts_created_at ON alert_logs(created_at);
CREATE INDEX idx_alerts_resolved ON alert_logs(is_resolved);
CREATE INDEX idx_reports_type ON reports(report_type);
CREATE INDEX idx_reports_generated_at ON reports(generated_at);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for threats table
CREATE TRIGGER update_threats_updated_at
    BEFORE UPDATE ON threats
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create trigger for indicators table
CREATE TRIGGER update_indicators_last_seen
    BEFORE UPDATE ON indicators
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for testing
INSERT INTO threats (cve_id, title, description, severity, cvss_score, source, published_date)
VALUES 
    ('CVE-2023-12345', 'Sample Critical Vulnerability', 'This is a sample critical vulnerability for testing purposes', 'critical', 9.8, 'NVD', CURRENT_TIMESTAMP - INTERVAL '1 day'),
    ('CVE-2023-12346', 'Sample High Vulnerability', 'This is a sample high severity vulnerability for testing', 'high', 7.5, 'NVD', CURRENT_TIMESTAMP - INTERVAL '2 days'),
    ('CVE-2023-12347', 'Sample Medium Vulnerability', 'This is a sample medium severity vulnerability for testing', 'medium', 5.5, 'NVD', CURRENT_TIMESTAMP - INTERVAL '3 days')
ON CONFLICT (cve_id) DO NOTHING;

INSERT INTO indicators (indicator_type, indicator_value, risk_score, source, metadata)
VALUES 
    ('ip', '192.168.1.100', 8.5, 'Mock Feed', '{"country": "US", "threat_type": "malware"}'),
    ('domain', 'malicious-domain.com', 7.0, 'Mock Feed', '{"category": "phishing"}'),
    ('hash', '5d41402abc4b2a76b9719d911017c592', 9.0, 'Mock Feed', '{"file_type": "exe", "malware_family": "trojan"}')
ON CONFLICT (indicator_value) DO NOTHING;