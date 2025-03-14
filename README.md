# BPMN Workflow Engine by `python-sage-bpmn`

![Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Pylint](https://img.shields.io/badge/pylint-9-brightgreen)

![PyPI release](https://img.shields.io/pypi/v/python-sage-bpmn "python-sage-bpmn")
![Supported Python versions](https://img.shields.io/pypi/pyversions/python-sage-bpmn "python-sage-bpmn")
![Documentation](https://img.shields.io/readthedocs/python-sage-bpmn "python-sage-bpmn")
![License](https://img.shields.io/badge/license-MIT-red)
![GitHub last commit](https://img.shields.io/github/last-commit/sageteamorg/python-sage-bpmn)

## Table of Contents
- [BPMN Workflow Engine by `python-sage-bpmn`](#bpmn-workflow-engine-by-python-sage-bpmn)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Step 1: Setting Up the BPMN Repository](#step-1-setting-up-the-bpmn-repository)
    - [Step 2: Parsing a BPMN File](#step-2-parsing-a-bpmn-file)
    - [Step 3: Querying BPMN Elements](#step-3-querying-bpmn-elements)
    - [Step 4: Extracting and Managing BPMN Processes](#step-4-extracting-and-managing-bpmn-processes)
  - [Error Handling](#error-handling)
  - [Contributing](#contributing)
  - [License](#license)

---

## Introduction
The **BPMN Workflow Engine** is an open-source Python library for managing and executing Business Process Model and Notation (BPMN) workflows. It provides functionality for defining tasks, events, and gateways, managing workflow sequences, and parsing BPMN XML files.

This package is designed for developers working with BPMN-based process automation, allowing seamless integration into existing applications.

## Features
- Define and manage BPMN tasks, events, and gateways.
- Query BPMN elements using a structured repository.
- Parse BPMN XML files and extract process definitions.
- Handle errors efficiently with custom BPMN exceptions.

## Installation
Install the package via pip:
```bash
pip install python-sage-bpmn
```

## Usage

### Step 1: Setting Up the BPMN Repository
To manage BPMN elements, you need to create a repository instance:
```python
from sage_bpmn import InMemoryBPMNRepository

repo = InMemoryBPMNRepository()
```
This repository will store all BPMN elements extracted from sage_bpmn files.

### Step 2: Parsing a BPMN File
To extract BPMN elements from an XML file:
```python
from sage_bpmn import BPMNParser

parser = BPMNParser("example.bpmn", repository=repo)
parser.extract_all()
```
After parsing, the repository will contain tasks, gateways, processes, and sequence flows.

### Step 3: Querying BPMN Elements
You can now query stored BPMN elements using the query engine:
```python
from sage_bpmn import BPMNQueryEngine, TaskType, GatewayType

query_engine = BPMNQueryEngine(repository=repo)

# Retrieve all tasks
print("All Tasks:", query_engine.repository.get_tasks())

# Get a task by ID
task = query_engine.get_task_by_id("task1")
print("Task with ID 'task1':", task)

# Retrieve user tasks
print("User Tasks:", query_engine.get_tasks_by_type(TaskType.USER))

# Search tasks by name
print("Search Tasks Containing 'Approval':", query_engine.search_tasks_by_name("Approval"))
```

### Step 4: Extracting and Managing BPMN Processes
Once extracted, processes and subprocesses can be analyzed:
```python
# Get extracted processes
processes = repo.get_processes()
print("Extracted Processes:")
for process in processes.values():
    print(f"- {process.name} (ID: {process.process_id})")

# Retrieve subprocesses of a specific process
parent_process_id = next(iter(processes.keys()))  # First process
subprocesses = query_engine.get_subprocesses(parent_process_id)
print(f"\nSubprocesses under {parent_process_id}:")
for subprocess in subprocesses:
    print(f"- {subprocess.name} (ID: {subprocess.process_id})")
```

## Error Handling
Custom exceptions allow handling BPMN-related issues gracefully:
```python
from sage_bpmn import BPMNValidationError

try:
    raise BPMNValidationError("Missing start event")
except BPMNValidationError as e:
    print(f"Validation error: {e.message}")
```

## Contributing
Contributions are welcome! Please fork the repository, make changes, and submit a pull request.

## License
This project is licensed under the MIT License.