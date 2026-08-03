# TASC Builder

> **Techfellah AI Software Company Builder**

TASC Builder is an AI-native software engineering platform for building, organizing, and orchestrating software projects through intelligent agents.

The project is designed with a modular, layered architecture that separates infrastructure, domain logic, persistence, execution, and user interfaces, making it easy to extend with new AI providers, workflows, and automation capabilities.

---

# Status

**Current Version**

```
v0.1.0-alpha.6
```

## Completed Milestones

* ✅ TASC-001 – Repository Foundation
* ✅ TASC-002 – Core
* ✅ TASC-003 – Command Line Interface
* ✅ TASC-004 – Projects
* ✅ TASC-005 – Agents

---

# Features

## Core

* Configuration loader
* YAML configuration parser
* Configuration validator
* Bootstrap engine
* Runtime context
* Registry
* Logging service
* Exception hierarchy

## Command Line Interface

* Workspace initialization
* Configuration validation
* Bootstrap
* Environment diagnostics

## Projects

* Create projects
* List projects
* Show project details
* Delete projects
* Filesystem persistence

## Agents

* Immutable agent definitions
* Provider abstraction
* Agent execution abstraction
* Filesystem persistence
* CRUD operations
* Ollama provider placeholder

---

# Architecture

```
                 CLI
                  │
     ┌────────────┴────────────┐
     ▼                         ▼
ProjectService           AgentService
     │                         │
     ▼                         ▼
ProjectRepository      AgentRepository
     │                         │
     ▼                         ▼
Filesystem            Filesystem

                          │
                          ▼
                    AgentExecutor
                          │
                          ▼
                      Core Registry
                          │
                          ▼
                    IAgentProvider
                          │
                          ▼
                    OllamaProvider
```

---

# Repository Layout

```
tasc-builder/

├── apps/
│
├── packages/
│   ├── core/
│   ├── cli/
│   ├── projects/
│   └── agents/
│
├── docs/
├── examples/
├── scripts/
└── README.md
```

---

# Packages

## tasc-core

Provides shared infrastructure.

* Configuration
* Registry
* Logging
* Bootstrap
* Runtime context
* Exceptions

---

## tasc-cli

Command-line interface.

Commands include:

* init
* validate
* bootstrap
* doctor
* project
* agent

---

## tasc-projects

Project management domain.

Includes:

* Domain models
* Repository
* Service
* Filesystem persistence

---

## tasc-agents

Agent management domain.

Includes:

* Agent models
* Services
* Repository
* Executor
* Provider abstraction

---

# CLI Commands

## Initialize a Workspace

```bash
tasc init my-company
```

---

## Validate Configuration

```bash
cd my-company

tasc validate
```

---

## Bootstrap

```bash
tasc bootstrap
```

---

## Environment Diagnostics

```bash
tasc doctor
```

---

# Project Commands

Create a project

```bash
tasc project create inventory
```

List projects

```bash
tasc project list
```

Show project details

```bash
tasc project show inventory
```

Delete a project

```bash
tasc project delete inventory
```

---

# Agent Commands

Create an agent

```bash
tasc agent create architect
```

List agents

```bash
tasc agent list
```

Show an agent

```bash
tasc agent show architect
```

Delete an agent

```bash
tasc agent delete architect
```

---

# Development

## Create a Virtual Environment

```bash
uv venv
source .venv/bin/activate
```

## Install Dependencies

```bash
uv sync
```

---

## Run Tests

```bash
python3 -m unittest discover -s packages -p "test_*.py" -v
```

---

## Compile

```bash
python3 -m compileall packages
```

---

## Check Whitespace

```bash
git diff --check
```

---

# Development Workflow

Every completed feature should satisfy the following:

* All unit tests pass
* Source compiles successfully
* `git diff --check` reports no issues
* Workspace dependencies resolve successfully
* CLI smoke tests pass

---

# Design Principles

* Interface-first architecture
* Dependency injection
* Immutable domain models
* Thin CLI orchestration
* Filesystem repositories
* Provider abstraction
* Separation of management and execution
* Modular package boundaries

---

# Technology Stack

* Python 3.12+
* Hatchling
* uv
* Typer
* PyYAML
* unittest

---

# Roadmap

## Completed

* Repository Foundation
* Core
* CLI
* Projects
* Agents

## Planned

* Real Ollama integration
* Additional model providers (OpenAI, Anthropic, Gemini)
* Workflow orchestration
* Multi-agent collaboration
* Event bus
* Plugin system
* Web portal
* Monitoring and telemetry

---

# License

This project is licensed under the MIT License.

---

# Author

**Techfellah**

Building an AI-native software engineering platform with a modular, extensible architecture focused on maintainability, testability, and long-term scalability.
