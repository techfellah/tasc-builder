# TASC Core

## Purpose

This package provides the foundational package boundary for the core runtime and shared structural elements of the TASC architecture.

## Package structure

The package is organized into a set of Python namespaces that separate bootstrap, configuration, context, events, exceptions, interfaces, logging, models, registry, services, and utilities responsibilities.

## Responsibilities

The package owns the architectural foundation for core runtime composition, shared metadata, and package-level boundaries. It is intentionally limited to structural organization and package-level separation, including the package-level exception hierarchy for common core failure semantics.

## Package boundaries

This package is the core package boundary and is not responsible for business implementation, service behavior, or runtime logic details.
