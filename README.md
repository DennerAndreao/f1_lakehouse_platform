# F1 Lakehouse Platform

Phase 2 evolution of the original F1 Lakehouse project, focused on production-oriented cloud data platform practices.

## Current scope

This repository starts with the Infrastructure as Code foundation for the platform evolution:

- Terraform project structure
- one executable environment: `dev`
- Databricks provider configuration
- room for future reusable modules

## Planned evolution

- Infrastructure as Code
- CI/CD
- Incremental ingestion
- Data quality
- Observability
- Multi-environment deployment
- Security and governance improvements

## Relationship to Phase 1

The original analytical lakehouse remains in the separate `f1_db_medallion` repository as the Phase 1 baseline. This repository is dedicated to the platform-oriented Phase 2 evolution.
