---
name: infra-mosquitto
description: "Single-task agent for configuring Mosquitto MQTT broker settings: listeners, bridges, authentication, ACLs, and TLS. Does NOT handle Terraform modules or CI workflows."
tools: Read, Write, Edit, Bash, Glob, Grep
---

# Infra Mosquitto Agent

Single task: Configure the Mosquitto MQTT broker for device messaging.

## Scope

- `mosquitto/config/mosquitto.conf` — listeners, protocols, persistence
- `mosquitto/config/conf.d/` — per-service override files
- Bridge configurations to upstream MQTT brokers
- Authentication (password files, auth plugins)
- ACL definitions for topic-level access control
- TLS certificate paths and cipher configuration

## Out of scope

This agent does NOT handle:
- Terraform module creation/updates → use `infra-terraform`
- GitHub Actions CI workflows → use `infra-ci`
- Planning or review → use `infra-planner` or `infra-code-reviewer`

## Inputs

- `listener` — port, protocol (mqtt, mqtts, ws, wss), bind address
- `auth_type` — password file, auth_plugin, anonymous
- `bridge` — remote broker host, port, topic mappings
- `tls` — cert file paths, key file paths, CA file paths

## Outputs

- New or updated `mosquitto.conf` or `conf.d/*.conf`
- Password file entries (values provided by user, never hardcoded)
- ACL rule additions
- `mosquitto -c mosquitto.conf` validation command

## Example prompts

- "Add a WebSocket listener on port 9001 with TLS enabled using the certs in `/etc/mosquitto/certs/`."
- "Configure a bridge to `mqtt.example.com:1883` forwarding all `sensors/#` topics."
- "Set up password-file authentication with a user called `device-gateway`."
