# TASC Builder

**Techfellah AI Software Company Builder**

> Transform a business idea into a fully functioning software project through a configurable AI software company.

---

## Vision

TASC Builder is an open-source framework for building and operating an AI-driven software company.

Instead of managing individual AI agents, TASC Builder models the structure of a software company through configuration and orchestrates specialized AI workers to execute software projects with minimal manual intervention.

The long-term goal is to enable organizations to define their company, projects, teams, and workflows declaratively while the framework manages software delivery from planning to production.

---

## MVP Goal

The first MVP focuses on delivering a production-quality execution kernel that provides:

* Configuration-driven framework initialization
* Modular architecture
* Runtime context management
* Service registry
* Logging infrastructure
* Project bootstrapping
* Command-line interface
* Foundation for AI agent orchestration

---

# Project Status

Current Release

```
v0.1.0-alpha.2
```

Current Progress

| Module                | Status         |
| --------------------- | -------------- |
| Repository Foundation | ✅ Complete     |
| Core Module           | ✅ MVP Complete |
| CLI                   | 🚧 In Progress |
| Projects              | ⏳ Planned      |
| Agents                | ⏳ Planned      |
| Portal                | ⏳ Planned      |

---

# Architecture

```
                  TASC Builder

                       │
                       ▼

                 Core Execution Engine

        ┌─────────────────────────────────┐
        │                                 │
        │ Configuration Engine            │
        │ Bootstrap Engine                │
        │ Runtime Context                 │
        │ Registry                        │
        │ Logging                         │
        │ Exception Framework             │
        └─────────────────────────────────┘

                       │
                       ▼

                CLI / Portal / Projects

                       │
                       ▼

                  AI Workforce
```

---

# Repository Structure

```
tasc-builder/

├── apps/
│
├── packages/
│   ├── core/
│   ├── cli/
│   ├── projects/
│   ├── agents/
│   └── portal/
│
├── tests/
│
├── docs/
│
├── scripts/
│
├── config/
│
└── README.md
```

---

# Core Components

The Core module currently provides:

* Exception Framework
* Logging Framework
* Runtime Context
* Service Registry
* Configuration Loader
* YAML Parser
* Configuration Validator
* Configuration Provider
* Bootstrap Engine

---

# Configuration Pipeline

```
core.yaml
     │
     ▼
ConfigurationLoader
     │
     ▼
ConfigurationParser
     │
     ▼
ConfigurationValidator
     │
     ▼
ConfigurationProvider
     │
     ▼
CoreConfiguration
     │
     ▼
Bootstrap Engine
```

---

# Technology Stack

## Backend

* Python 3.12+
* Hatchling
* uv
* PyYAML

## Development

* Git
* GitHub
* Docker
* VS Code

## AI Development

The framework is designed to support multiple LLM providers through a provider abstraction.

The MVP development is performed using AI-assisted implementation while maintaining a provider-agnostic architecture.

---

# Development

Clone the repository:

```bash
git clone https://github.com/techfellah/tasc-builder.git
cd tasc-builder
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
uv sync
```

Run the test suite:

```bash
python3 -m unittest discover -s packages/core/tests -p "test_*.py" -v
```

Compile all packages:

```bash
python3 -m compileall packages
```

---

# Roadmap

## v0.1.0

* Core Execution Engine
* Command Line Interface
* Project Management
* Agent Management
* Bootstrap Process
* Initial Portal
* Yuki (Minimal AI Assistant)

---

# Design Principles

* Configuration First
* Modular Architecture
* Interface-Driven Design
* Immutable Configuration Models
* Strong Separation of Concerns
* Comprehensive Automated Testing
* Provider-Agnostic AI Integration

---

# Contributing

TASC Builder is an open-source project.

Contributions are welcome through:

* Bug reports
* Feature requests
* Documentation improvements
* Pull requests
* Architecture discussions

Please ensure all contributions:

* Follow the existing architecture
* Include appropriate unit tests
* Pass the complete validation suite
* Maintain backward compatibility where applicable

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

# Author

**Techfellah**

Building the next generation of AI-driven software engineering frameworks.

---

# Acknowledgements

TASC Builder is being developed as an open-source initiative to demonstrate how configurable AI systems can automate software engineering workflows while remaining modular, extensible, and maintainable.

The project emphasizes solid software architecture first, enabling future AI capabilities to be built on a reliable and testable foundation.
