---
name: infra-mosquitto-setup
description: Configure the Mosquitto MQTT broker for device messaging, including listeners, bridges, authentication, ACLs, and TLS.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Mon, 29 Jun 2026 00:00:00 GMT
---

# Mosquitto MQTT Broker Setup

## Contents
- [Configuration Layout](#configuration-layout)
- [Listeners](#listeners)
- [Authentication](#authentication)
- [ACLs](#acls)
- [Bridges](#bridges)
- [TLS](#tls)
- [Verification](#verification)

## Configuration Layout

```
mosquitto/
└── config/
    ├── mosquitto.conf          # Main config file
    ├── conf.d/
    │   ├── listeners.conf      # Listener definitions
    │   ├── auth.conf           # Auth and ACL configuration
    │   ├── bridges.conf        # Bridge definitions
    │   └── logging.conf        # Logging configuration
    ├── passwd                  # Password file (managed out of band)
    └── acl                     # ACL file (managed out of band)
```

## Listeners

Each listener is a separate port with optional protocol and TLS:

```
listener 1883
protocol mqtt

listener 8883
protocol mqtt
cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key

listener 9001
protocol websockets

listener 9002
protocol websockets
cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
```

Use `per_listener_settings true` when listeners have different auth rules.

## Authentication

### Password file

```
password_file /etc/mosquitto/passwd
allow_anonymous false
```

Create users: `mosquitto_passwd -c /etc/mosquitto/passwd <username>`

### Auth plugin

```
auth_plugin /usr/lib/mosquitto/auth_plugin.so
auth_opt_backends mysql
```

## ACLs

### File-based ACLs

```
acl_file /etc/mosquitto/acl
```

Example `acl` file:

```
# Admin access
user admin
topic readwrite #

# Device telemetry
user device-gateway
topic readwrite iot/telemetry/#

# Read-only for subscribers
pattern read iot/%u/#
```

## Bridges

Bridge config connects this broker to an upstream MQTT broker:

```
connection upstream-broker
address mqtt.example.com:1883
topic sensors/# out 2
topic commands/# in 2
cleansession false
try_private true
notifications true
notification_topic bridge/status/#
remote_clientid hub-bridge
start_type automatic
restart_timeout 10
```

## TLS

| Directive | Description |
|---|---|
| `cafile` | CA certificate file path |
| `certfile` | Server certificate file path |
| `keyfile` | Server private key file path |
| `tls_version` | Minimum TLS version (e.g., `tlsv1.2`) |
| `require_certificate` | Require client certificates (true/false) |

## Verification

1. `mosquitto -c mosquitto/config/mosquitto.conf -d` — syntax check
2. `mosquitto_sub -h localhost -p 1883 -t "test/#"` — subscribe to test topic
3. `mosquitto_pub -h localhost -p 1883 -t "test/hello" -m "world"` — publish
4. For TLS: `mosquitto_sub -h localhost -p 8883 --cafile ca.crt -t "test/#"`
