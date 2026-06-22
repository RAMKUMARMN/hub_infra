# SmartHub Document Summarization Workflow

## Purpose

Receives document text from the SmartHub backend, generates a summary using Ollama, sends the summary via email, and returns a success response.

## Endpoint

POST /webhook/document-summary

## Input

{
  "document_text": "string",
  "email": "user@example.com"
}

## Workflow

1. Webhook
2. Ollama Summarizer
3. Format Summary
4. Send Email
5. Respond to Webhook

## Testing

curl -X POST http://localhost:8000/api/v1/workflows/document-summary \
-H "Content-Type: application/json" \
-d '{
  "document_text":"Sample document",
  "email":"test@example.com"
}'
