---
mode: agent
agent: infra-mosquitto
name: infra-mosquitto-prompt
description: "Prompt for the infra-mosquitto agent. Configures Mosquitto MQTT broker listeners, bridges, authentication, ACLs, and TLS settings."
---

### Requirements

1. **Listeners:** Configure listeners for MQTT, MQTT over TLS, WebSockets, and WebSockets over TLS as requested. Each listener should have a dedicated `port`, `protocol`, and optional `bind_address`.
2. **Authentication:** Support password-file auth (`password_file`), auth_plugin, or anonymous access. Password files are managed outside the repo — reference the path only.
3. **ACLs:** Define topic-level access control using `acl_file` or inline rules. Follow least-privilege per client/topic.
4. **Bridges:** Configure remote broker bridges with `address`, `topic` mappings, `remote_clientid`, and TLS settings. Enable `try_private` and `cleansession false` for persistent bridges.
5. **TLS:** Reference certificate and key file paths. Use `cafile`, `certfile`, `keyfile`, and `tls_version` directives. Never embed cert content in config files.
6. **Logging:** Configure `log_type` and `log_dest` for debugging without filling disks.

### Constraints

- Config files in `mosquitto/config/` with per-service overrides in `conf.d/`
- Sensitive paths (passwords, keys) are references only — values must be deployed out of band
- Validate with `mosquitto -c mosquitto.conf -d` syntax check
- Use `per_listener_settings true` when listeners have different auth rules

### Success Criteria

- Config file passes `mosquitto -c` syntax check
- Listeners bind on the requested ports without conflict
- ACL rules allow/deny the specified topic patterns
- Bridges establish connection (verified with `mosquitto_sub` on remote)

### Usage Template

```
Configure the Mosquitto broker with:
- [Listener: port, protocol, TLS settings]
- Auth: [password_file path or auth_plugin]
- [Optional] Bridge to [remote host:port] for topics [topic patterns]
- [Optional] ACL rules: [topic patterns and access levels]
Show the diff and wait for my confirmation before applying.
```

### Chat Example

```
User: Add a WebSocket listener on port 9001 with TLS.
- Use certs from /etc/mosquitto/certs/
- Require client certificates
- Allow anonymous pub/sub on iot/telemetry/#
```

Agent (expected):
- Adds listener block with ws protocol, port 9001, TLS paths
- Creates conf.d/ override if appropriate
- Waits for confirmation before applying any patches
