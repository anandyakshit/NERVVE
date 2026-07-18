# NERVVE

### Node Based Extended Range Virtual Vigilance Ecosystem

NERVVE is a disaster-resilient emergency communication system designed to provide long-range distress messaging when conventional communication infrastructure is unavailable or compromised.

The system combines a smartphone application, Bluetooth communication, LoRa radio technology, GPS location services, and a centralized command dashboard to enable the rapid transmission and monitoring of emergency alerts across large distances.

---

## Overview

Natural disasters, network outages, and remote environments often render mobile networks unreliable or completely unavailable. NERVVE addresses this challenge by creating an independent communication pathway capable of transmitting emergency messages and GPS coordinates without relying on cellular infrastructure.

A user can send an SOS message through the NERVVE mobile application, which is transmitted via Bluetooth to a portable communication node. The node then relays the alert over LoRa radio to a receiving station, where the NERVVE Command Centre displays and logs the incident.

This approach is inspired by real-world emergency communication systems that leverage long-range, low-power radio technologies for disaster resilience and off-grid messaging.

---

## Key Features

### 📱 Mobile Emergency Client

* Live GPS location acquisition
* User-defined emergency message (up to 50 characters)
* Bluetooth communication with field node
* One-touch SOS transmission

### 📡 LoRa Communication Layer

* Long-range wireless communication
* Operates independently of cellular networks
* Optimized for emergency messaging
* Low-power operation

### 🖥️ NERVVE Command Centre

* Real-time alert monitoring
* Automatic packet counting
* Alert history logging
* GPS coordinate display
* Google Maps/OpenStreetMap integration
* Automatic device reconnect handling
* Connection status monitoring

### 🔄 Reliability Features

* Automatic receiver reconnection
* Graceful shutdown handling
* Continuous packet monitoring
* Persistent alert history during runtime

---

## System Architecture

```text
Smartphone App
       │
       │ Bluetooth (HC-05)
       ▼
Field Node
(Arduino + LoRa)
       │
       │ LoRa Radio
       ▼
Receiver Node
(Arduino + LoRa)
       │ USB Serial
       ▼
NERVVE Command Centre
(CustomTkinter Dashboard)
```

---

## Technology Stack

### Mobile Application

* MIT App Inventor
* Android Location Services
* Bluetooth Client

### Embedded Hardware

* Arduino
* HC-05 Bluetooth Module
* SX1278 LoRa Module
* GPS Location Data

### Command Centre

* Python 3
* CustomTkinter
* PySerial
* Threading
* WebBrowser API

---

## Data Packet Format

The mobile application transmits alerts in the following format:

```text
SOS: Need Medical Help | LAT: xx.xxxxx | LONG: yy.yyyyy
```

The Command Centre automatically parses the packet and extracts:

* Emergency Message
* Latitude
* Longitude
* Timestamp

---

## Command Centre Interface

### System Status

Displays:

* Receiver connection state
* Total alerts received
* Device health

### Active Alert Panel

Displays:

* Latest emergency message
* Alert priority
* GPS coordinates
* Quick map access

### Alert History

Maintains a chronological log of:

* Timestamp
* Message
* Coordinates
* Location shortcuts

---

## Intended Applications

* Disaster response
* Flood-prone regions
* Earthquake scenarios
* Rural communication
* Search and rescue operations
* Educational demonstrations
* Emergency preparedness systems

---

## Current Development Status

### Completed

* Mobile SOS application
* Bluetooth communication
* GPS integration
* Packet formatting
* Command Centre dashboard
* Real-time packet parsing
* Alert history system
* Automatic reconnect functionality
* Thread-safe shutdown handling

### Planned Enhancements

* Embedded map view
* Priority classification system
* CSV alert logging
* Multi-node support
* LoRa mesh networking
* AI-assisted emergency categorization

---

## Project Vision

NERVVE aims to demonstrate how affordable hardware and modern software can be combined to create resilient communication systems that remain functional when traditional infrastructure fails.

By integrating long-range radio communication with an intuitive user interface, NERVVE seeks to provide a foundation for future emergency communication networks capable of assisting communities during critical situations.

---

## Developed By

**Yakshit Anand**

Class XII Project

NERVVE — *Node Based Extended Range Virtual Vigilance Ecosystem*

*"Communication when it matters most."*
