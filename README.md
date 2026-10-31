# Distributed Log Aggregation System Using UDP, Mininet and SDN

## 1. Introduction

In a network with multiple systems, each machine generates its own application logs. Monitoring these logs separately can become difficult, especially when we need to understand what is happening across different systems.

Our project aims to make this easier by collecting logs from multiple clients and sending them to a central server using UDP.

Along with log collection, we integrated the application with Mininet and Software Defined Networking (SDN). This allowed us to experiment with normal and critical traffic, configure queues and study how network performance changes under congestion.

## 2. Project Objectives

The main objectives of our project are:

- Generate application logs from multiple clients.
- Transfer logs to a central server using UDP.
- Extract and organise log details such as host, timestamp, severity and message.
- Maintain separate counts for different severity levels.
- Store received logs in a file.
- Distinguish between normal and critical traffic.
- Use SDN flow rules to manage network traffic.
- Configure queues and QoS in Open vSwitch.
- Test network performance under baseline and congestion conditions.

## 3. System Architecture

Our project consists of three main components.

**Log generation:** Client programs generate sample application logs with different severity levels, including INFO, WARNING, ERROR and CRITICAL.

**Log aggregation:** A central UDP server receives the messages, extracts their fields, updates the severity counters and stores the logs in a file.

**SDN network:** Mininet provides the virtual network, Open vSwitch forwards the packets, and the SDN controller manages traffic using OpenFlow rules.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| C | Log generation and UDP server |
| Python | Integrated UDP client and server |
| UDP sockets | Communication between clients and server |
| Mininet | Creating the virtual network |
| Open vSwitch | Connecting and forwarding traffic |
| OS-Ken | SDN controller |
| OpenFlow 1.3 | Installing traffic flow rules |
| iperf3 | Generating traffic and measuring performance |

## 5. UDP Log Generation and Aggregation

We first implemented and tested the log generation and receiving components independently.

The log messages follow this format:

`host|timestamp|severity|message`

Example:

`h1|2026-10-30 12:20:00|ERROR|Database connection failed`

The standalone UDP server listens on port 9000.

When a log message is received, the server:

- Extracts the host name, timestamp, severity and message.
- Checks the severity level.
- Updates the corresponding counter.
- Increases the total log count.
- Saves the received log in `logs.txt`.
- Displays the received information and severity-wise counts.

We tested the server by sending sample messages from multiple clients.

## 6. Mininet and SDN Integration

After testing the logging components, we integrated the application with our Mininet network.

Our topology consists of four hosts connected through one Open vSwitch.

- **h1, h2 and h3:** Network hosts.
- **h4:** Central server.
- **s1:** Open vSwitch.
- **OS-Ken:** SDN controller.

In the integrated logging application, we use separate UDP ports for normal and critical traffic.

| Traffic type | UDP port |
|---|---:|
| Normal | 10000 |
| Critical | 10001 |

The SDN controller installs flow rules that identify these traffic classes using their destination ports.

The integrated client and server also use acknowledgements to verify message delivery and measure round-trip time (RTT).

## 7. Queue Configuration and QoS

We then worked on traffic management using Open vSwitch queues.

Two queues were configured:

- Queue 0
- Queue 1

Different minimum and maximum rate settings were assigned to the queues.

We attached the QoS configuration to the switch port and used OpenFlow rules with `set_queue` actions to direct matching packets into the selected queues.

This allowed us to experiment with traffic allocation and prioritisation.

## 8. Network Performance Testing

We used iperf3 to generate UDP traffic between h1 and h4.

Two separate traffic streams were tested using UDP ports 5201 and 5202. Each test used a target sending rate of 8 Mbps for 20 seconds.

We performed two types of experiments.

### 8.1 Baseline Testing

Baseline testing was performed to observe network performance before introducing the congestion scenario.

We recorded the throughput, packet loss and jitter for both traffic streams.

### 8.2 Congestion Testing

For congestion testing, competing UDP traffic was generated through the network.

We observed how the traffic behaved when network resources were shared.

The results were collected using iperf3 and saved for comparison.

### Metrics Observed

- **Throughput:** Amount of data transferred per second.
- **Packet loss:** Number or percentage of datagrams not received.
- **Jitter:** Variation in packet arrival times.
- **Transfer:** Total amount of data transferred.

We also inspected the OpenFlow flow table to verify packet counts and queue assignments.

## 9. Testing and Verification

The following tests were performed during the project:

1. Tested UDP communication between clients and the server.
2. Verified that the server received and processed logs.
3. Checked log storage and severity-wise counters.
4. Tested connectivity between Mininet hosts.
5. Verified the SDN controller connection.
6. Inspected OpenFlow rules and packet counters.
7. Checked queue and QoS configurations in Open vSwitch.
8. Performed baseline UDP traffic tests using iperf3.
9. Generated competing traffic for congestion testing.
10. Observed throughput, packet loss and jitter during the experiments.

## 10. Team Contributions

**Person 1: UDP Log Generation**

Worked on generating application logs with timestamps and severity levels and sending them through UDP clients.

**Person 2: UDP Server and Log Aggregation**

Worked on implementing the UDP server, receiving and parsing log messages, maintaining severity-wise counters and storing the logs.

**Person 3: SDN and Network Integration**

Worked on the Mininet topology, SDN controller, OpenFlow rules, queue configuration and network integration.

## 11. Conclusion

Through this project, we developed a system that collects application logs from multiple clients and stores them at a central server.

We also integrated the application with a virtual SDN network and experimented with traffic classification, queue configuration and congestion testing.

Working on this project helped us understand how UDP communication, log aggregation and SDN-based traffic management can be combined in a single system.
