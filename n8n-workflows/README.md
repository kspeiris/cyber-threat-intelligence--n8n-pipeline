# Threat Intelligence N8N Workflows

This directory contains n8n workflow definitions for the Cyber Threat Intelligence Pipeline.

## Available Workflows

### threat_intelligence_workflow.json

Automated threat collection workflow that:
- Runs every 6 hours
- Collects vulnerabilities from NVD
- Collects indicators of compromise
- Generates daily reports
- Sends Telegram notifications

## Setup

1. Import workflow into n8n:
   - Open n8n at http://localhost:5678
   - Go to Workflows → Import
   - Select the JSON file

2. Configure credentials:
   - Add Telegram Bot credentials
   - Update Telegram node with your chat ID

3. Activate workflow:
   - Click "Active" toggle to enable scheduling