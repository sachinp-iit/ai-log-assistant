# AI Log Assistant

## Overview

AI Log Assistant is an Agentic AI platform for infrastructure log
analysis. It combines RAG, LLMs, vector search, and ML-based anomaly
detection to help DevOps, SRE, and Cloud teams investigate incidents.

## Objectives

-   Conversational AI chatbot for infrastructure logs
-   Semantic log search using Qdrant
-   ML-based anomaly detection
-   Root cause analysis
-   Incident summarization
-   Trend analysis and reporting
-   Similar incident retrieval
-   Alert recommendations

## Dataset

The project uses an infrastructure/cloud anomaly dataset containing
operational metrics and anomaly labels.

Typical fields include: - Timestamp - CPU Usage - Memory Usage - Network
Traffic - Power Consumption - Execution Time - Energy Efficiency - Task
Metadata - Anomaly Status

## Architecture

``` text
Infrastructure Logs / CSV
          │
          ▼
   Data Ingestion
          │
          ▼
 Preprocessing & Chunking
          │
 ┌────────┴────────┐
 ▼                 ▼
Qdrant          ML Models
(RAG)      (Anomaly Detection)
 └────────┬────────┘
          ▼
      AI Agents
          ▼
 FastAPI REST APIs
          ▼
   Chat UI / Dashboard
```

## AI Agents

-   Chat Agent
-   Retrieval Agent
-   Anomaly Detection Agent
-   Root Cause Analysis Agent
-   Incident Summary Agent
-   Alert Recommendation Agent

## Features

### RAG

-   Semantic search
-   Context-aware responses
-   Similar incident search

### AI Chatbot

-   Natural language log queries
-   Infrastructure troubleshooting
-   Log explanation

### Anomaly Detection

-   Detect abnormal infrastructure behavior
-   Predict anomaly probability
-   Explain detected anomalies

### Root Cause Analysis

-   Identify contributing metrics
-   Correlate system events
-   Explain failures

### Analytics

-   Resource utilization
-   Trend analysis
-   Incident reports
-   Historical comparisons

## Project Structure

``` text
agents/
api/
config/
core/
database/
dependencies/
infra_logs/
models/
prompts/
schemas/
services/
storage/
utils/
vector_db/
main.py
requirements.txt
```

## API Modules

-   Log Ingestion
-   Chat
-   Retrieval
-   Anomaly Detection
-   Root Cause Analysis
-   Health Check

## Tech Stack

-   FastAPI
-   LangChain
-   LangGraph
-   OpenRouter
-   Qdrant
-   Sentence Transformers
-   BGE Embeddings
-   Python

## Future Enhancements

-   Streaming log ingestion
-   Grafana integration
-   Prometheus integration
-   Kubernetes support
-   Multi-agent orchestration
-   Real-time alerting
-   Fine-tuned anomaly models

## Goal

Build a production-ready AI platform capable of understanding
infrastructure logs, detecting anomalies, explaining failures, and
assisting engineers through natural language.
