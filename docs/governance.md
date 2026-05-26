# Governance

This project uses a minimal governance model appropriate for an individual development environment while still demonstrating Unity Catalog access control patterns.

## Current principal

The current `dev` grants are assigned directly to the development principal:

```text
dennermandreao@gmail.com
```

This is intentional. The project currently has one real user, so direct grants are more honest than creating decorative workspace-local groups.

## Current grants

### Catalog

```text
f1_lakehouse_dev
└── USE_CATALOG
```

### Schemas

```text
f1_lakehouse_dev.bronze
f1_lakehouse_dev.silver
f1_lakehouse_dev.gold
```

Privileges:

```text
USE_SCHEMA
CREATE_TABLE
MODIFY
```

### External location

```text
db_s3_external_databricks-s3-ingest-da803
```

Privileges:

```text
CREATE_MANAGED_STORAGE
READ_FILES
WRITE_FILES
```

## Why not groups yet?

A workspace-local `data_engineers` group was tested, but Unity Catalog grants expect principals that are valid for the relevant governance scope. For this individual project, direct user grants are cleaner.

Future evolution can introduce account-level groups using SCIM/OAuth when the platform needs multi-user access.

## Future governance evolution

Potential next steps:

- account-level `data_engineers` group
- account-level `data_analysts` group
- separate dev/prod grants
- least-privilege read-only grants for BI consumption
- service principal grants for CI/CD
