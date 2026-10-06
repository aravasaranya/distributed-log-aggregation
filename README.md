# Distributed Log Aggregation System

A UDP-based distributed log aggregation system integrated with Mininet and SDN.

## Project Structure

- server: UDP log server and aggregation
- client: log generation and UDP clients
- sdn: Mininet topology and SDN controller

## Current Implementation

The server receives logs in the following format:

host|timestamp|severity|message

Example:

h1|2026-10-06 12:20:00|ERROR|Database connection failed

The server:
- Receives UDP logs
- Parses log fields
- Counts logs by severity
- Stores logs in logs.txt

## Technologies

- C
- UDP Sockets
- Mininet
- SDN
- OpenFlow
