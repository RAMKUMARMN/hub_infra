---
name: discover-event-streaming
description: Trace Kafka event brokers, RabbitMQ task queues, and Mosquitto MQTT pipelines.
---

# Discover Event Streaming & Queues

Analyze the asynchronous communication and background processing infrastructure.

## Focus Areas
- Mosquitto MQTT configuration (`mosquitto/mosquitto.conf`)
- RabbitMQ queue definitions (OCR, Document, Vision, RAG tasks)
- Kafka event topics (User Events, Audit Events, Analytics)

## Goals
- Map the high-throughput asynchronous event topology.
- Verify security and persistence settings of the message brokers.

## Output
Return:
- Event streaming and messaging topology

## Workflow
1. Route the hub folder agent to plugin/skills for this specific skill folder.
2. Invoke the `discoverMessagingConfig` tool to parse broker settings.
3. Invoke `findResource` targeting "RabbitMQ" or "Kafka" connections in the compose file.
4. Return the messaging bus configuration.
