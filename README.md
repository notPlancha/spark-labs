# Big Data Analytics on Cloud Computing Infrastructures Labs

A collection of hands-on labs for learning Apache Spark and big data analytics on cloud computing infrastructures.

## Project Structure

```
├── src/
│   ├── lab1/                         # Lab 1: Spark basics and transformations
│   │   ├── task1.ipynb               # Jupyter notebook for Task 1
│   │   ├── task2.ipynb               # Jupyter notebook for Task 2
│   │   └── report/                   # Lab report generation
│   │       └── report.typ            # Typst report source
│   ├── lab2/                         # Lab 2: Advanced data processing and testing
│   │   ├── tasks.ipynb               # Main tasks notebook
│   │   ├── testing.ipynb             # Testing and validation notebook
│   │   └── report/                   # Lab report generation
│   │       └── report.typ            # Typst report source
│   ├── lab3/                         # Lab 3: Titanic dataset analysis
│   │   ├── lab3.py                   # Python script for analysis
│   │   └── titanic.csv               # Titanic dataset
│   ├── lab4/                         # Lab 4: Databricks platform exploration
│   │   ├── task 8.md                 # Task documentation
│   │   ├── screenshots/              # Screenshots and images
│   │   │   ├── task8-1.png           # Home page
│   │   │   ├── task8-2.png           # Workspace interface
│   │   │   ├── task8-3.png           # Catalog interface
│   │   │   ├── task8-4.png           # Jobs & Pipelines interface
│   │   │   └── task8-5.png           # Compute resources interface
│   │   └── Lab4.pdf                  # Lab materials
│   └── server-docker-files/          # Docker setup for Spark server
│       ├── Dockerfile                # Spark container configuration
│       └── compose.yaml              # Docker Compose setup
├── justfile                          # Task automation with Just
├── pyproject.toml                    # Python project configuration
└── README.md                         # This file
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

### Lab 1: Apache Spark Basics and Transformations
- **Task 1**: Introduction to Apache Spark fundamentals
- **Task 2**: Advanced Spark operations and transformations
- **Report**: Comprehensive analysis and findings

### Lab 2: Advanced Data Processing and Testing
- **Tasks**: Data processing workflows and advanced transformations
- **Testing**: Validation and testing frameworks for data pipelines
- **Report**: Testing results and performance analysis

### Lab 3: Titanic Dataset Analysis
- **Analysis Script**: Python-based data exploration and analysis
- **Dataset**: Titanic passenger dataset with survival data
- **Focus**: Data cleaning, exploration, and statistical analysis with Spark

### Lab 4: Databricks Platform Exploration
- **Task 8**: Hands-on exploration of Databricks platform features
- **Topics Covered**:
  - Home page and onboarding
  - Workspace file management
  - Data catalog and discovery
  - Jobs and pipeline orchestration
  - Compute resource management

## Technologies Used

- **Apache Spark 4.0.1**: Distributed computing framework for large-scale data processing
- **PySpark**: Python API for Spark, enabling distributed data manipulation
- **Databricks**: Cloud platform for collaborative data engineering and analytics
- **Jupyter Notebooks**: Interactive computational environment for data exploration
- **Python 3.10+**: Core programming language
- **Pandas**: Data manipulation and analysis library
- **Docker**: Containerized Spark deployment and server management
- **Typst**: Modern document preparation system for report generation
- **CSV**: Data format for datasets (Titanic dataset)
