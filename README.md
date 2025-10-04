# Big Data Analytics on Cloud Computing Infrastructures Labs

A collection of hands-on labs for learning Apache Spark and big data analytics on cloud computing infrastructures.

## Project Structure

```
├── src/
│   ├── lab1/                         # Lab 1 exercises and materials
│   │   ├── task1.ipynb               # Jupyter notebook for Task 1
│   │   ├── task2.ipynb               # Jupyter notebook for Task 2
│   │   ├── lab1 instructions.pdf     # Lab instructions
│   │   ├── lab1 help.pdf             # Additional help materials
│   │   └── report/                   # Lab report generation
│   │       ├── report.typ            # Typst report source
│   │       └── report.pdf            # Generated report
│   └── server-docker-files/          # Docker setup for Spark server
│       ├── Dockerfile                # Spark container configuration
│       └── compose.yaml              # Docker Compose setup
├── justfile                          # Task automation with Just
├── pyproject.toml                    # Python project configuration
```

## Prerequisites

- Python 3.10
- Access to external Spark server (Docker-based)
- [Just](https://just.systems/) command runner (optional, for convenience commands)
- [Typst](https://typst.app/) (for report generation)

## Getting Started

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 2. Configure External Spark Connection

This project uses an external Spark server running on a remote computer, connected by LAN. The Docker configuration files in `src/server-docker-files/` are provided for reference.

```bash
cd src/server-docker-files/
docker compose up -d
```

Make sure to configure your Spark connection settings in the Jupyter notebooks to point to the external Spark server.

## Available Commands (Just)

If you have [Just](https://just.systems/) installed, you can use these convenience commands:

```bash
# setup python venv with uv
just setup

# Compile lab report
just report lab1

# Watch and auto-compile report on changes
just watch lab1

# Compile and open report
just open lab1

# Create archive of all labs
just archive
```

## Lab Contents

### Lab 1
- **Task 1**: Introduction to Apache Spark basics
- **Task 2**: Advanced Spark operations and transformations
- **Report**: Comprehensive analysis and findings

## Technologies Used

- **Apache Spark 4.0.1**: Distributed computing framework
- **PySpark**: Python API for Spark
- **Jupyter**: Interactive notebook environment
- **Docker**: Containerized Spark deployment
- **Typst**: Modern document preparation system
