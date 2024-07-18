
# Event-Driven DAG Automation with GDACS Alerts

This project automates the triggering of Directed Acyclic Graphs (DAGs)
in response to orange or red alerts from the Global Disaster Alert
and Coordination System (GDACS).
By integrating real-time event monitoring
and automated workflow triggers,
this system ensures timely and efficient responses to critical events.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)

## Features

- **Real-Time Monitoring**: Continuously monitors the GDACS website for new alerts.
- **Automated DAG Triggers**: Triggers specific DAGs within the pipeline
based on alert.

### Prerequisites

- Python 3.8 or higher
- Poetry
- Airflow
- Docker

### Installation

```bash
git clone https://github.com/ediakatos/pipeline-event-driven-gdacs.git
```

```bash
cd pipeline-event-driven-gdacs
```

```bash
make .venv hooks
```

### Database

Run inside the Project's dir

```bash
mkdir -p data
```

and then,

```bash
make database
```

## **To run the Event-Driven Programme**

### Start-Event

```bash
make event
```

### Stop-Event

```bash
make no_event
```
