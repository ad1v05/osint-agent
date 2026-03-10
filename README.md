# OSINT Agent 🕵️

An autonomous Open Source Intelligence (OSINT) agent that investigates a target across multiple intelligence sources and generates a structured report — automatically.

## What it does

Give it a target (domain, IP, or organization name) and it autonomously:
- Geolocates IPs and identifies owning organizations
- Pulls recent news mentions from across the web
- Scans exposed infrastructure and open ports via Shodan
- Retrieves domain registration data via WHOIS
- Generates a formatted markdown intelligence report

## Tech Stack

- **Python** — core agent logic and API orchestration
- **AWS SQS** — cloud message queue for parallel task execution
- **Docker** — containerized for portable deployment
- **Shodan, NewsAPI, ipinfo, WHOIS XML API** — intelligence sources

## Architecture
```
User Input (target)
       │
       ▼
  OSINTAgent.run()
       │
  ┌────┴─────┐
  │  Tasks   │  ──→  Shodan API
  │  Fan-out │  ──→  WHOIS API
  │          │  ──→  NewsAPI
  └────┬─────┘  ──→  ipinfo API
       │
       ▼
  Report Generator
       │
       ▼
  report_target_date.md
```

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/ad1v05/osint-agent.git
cd osint-agent
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Add API keys
Create a `.env` file in the project root:
```
SHODAN_API_KEY=your_key
NEWS_API_KEY=your_key
IPINFO_TOKEN=your_key
WHOIS_API_KEY=your_key
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_key
AWS_REGION=us-east-1
SQS_QUEUE_URL=your_queue_url
```

### 4. Run locally
```bash
python3 main.py "Raytheon"
```

### 5. Run with Docker
```bash
docker build -t osint-agent .
docker run --env-file .env osint-agent python3 main.py "Raytheon"
```

### 6. Run with AWS SQS
Publish tasks to the queue:
```bash
python3 -c "
from aws.sqs_publisher import publish_task
publish_task('news', 'Raytheon')
publish_task('shodan', 'Raytheon')
publish_task('whois', 'raytheon.com')
"
```

Consume and execute tasks:
```bash
python3 -m aws.sqs_consumer
```

## Example Output
```
2026-03-10 14:27:11 [INFO] Starting OSINT sweep on: Raytheon
2026-03-10 14:27:11 [INFO] Running task: ip_info
2026-03-10 14:27:11 [INFO] Running task: news
2026-03-10 14:27:11 [INFO] Running task: shodan
2026-03-10 14:27:11 [INFO] Running task: whois
2026-03-10 14:27:11 [INFO] Sweep Complete.
Report Saved: report_Raytheon_20260310.md
```

## Future Improvements
- Flask web UI for submitting targets and viewing reports
- AWS Lambda for serverless task execution
- Additional intelligence sources (VirusTotal, threat feeds)
- Real-time streaming results to dashboard