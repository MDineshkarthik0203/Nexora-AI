# AgentForge Backend

Django REST backend for the AgentForge project.

## Architecture

React Frontend
    |
    | HTTP
    v
Django REST API
    |
    v
api/services.py
    |
    v
src/agentforge/graph.py
    |
    +-- Supervisor
    +-- Planner
    +-- Research
    +-- RAG
    +-- Coding
    +-- Reviewer
    +-- Human Review
    +-- Writer

## Endpoints

GET

/api/health/

POST

/api/chat/

POST

/api/human-review/

## Start

From the backend directory:

python manage.py migrate

python manage.py runserver

## Test health

Open:

http://127.0.0.1:8000/api/health/

## Test AgentForge

PowerShell:

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/chat/" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"question":"give me python code for palindrome","session_id":"agentforge-test-001"}'

## Human approval

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/human-review/" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"session_id":"agentforge-test-001","action":"approve","feedback":""}'

The session_id is used as LangGraph's thread_id so the
workflow can resume after interrupt().
