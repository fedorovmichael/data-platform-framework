# Data Platform Framework --- Roadmap: Sprint 4 to Release

## Current Status

Sprints 1--3 are complete.

The framework currently supports an end-to-end Spark pipeline:

``` text
Source → Validation → Transformation → Sink
```

Current foundation includes:

-   Generic Source and Sink contracts
-   Validator and Transformer abstractions
-   Composite validation
-   Composite transformation
-   Registries
-   PipelineBuilder
-   PipelineExecution
-   Spark runtime integration
-   End-to-end pipeline execution
-   Unit and pipeline tests

The remaining roadmap focuses on taking the framework from a working
architecture to a production-ready Data Engineering project.

------------------------------------------------------------------------

# Sprint 4 --- Reliability & Observability

## Goal

Make pipeline execution observable, predictable, and resilient.

## 4.1 Structured Logging

Add framework-level logging around pipeline execution.

Expected lifecycle:

``` text
Pipeline started
Source read started/completed
Validation started/completed
Transformation started/completed
Sink started/completed
Pipeline succeeded/failed
```

Requirements:

-   Use Python `logging`, not `print()`
-   Include pipeline name
-   Include execution stage
-   Log failures with useful context
-   Avoid business logic inside logging code

## 4.2 Execution Status

Introduce a clear execution lifecycle.

Suggested statuses:

``` text
PENDING
RUNNING
SUCCESS
FAILED
```

Evaluate whether a `PipelineExecutionResult` abstraction is useful.

Potential execution information:

-   Pipeline name
-   Status
-   Start time
-   End time
-   Duration
-   Error information

Do not over-engineer the result contract before requirements are clear.

## 4.3 Exception Architecture

Define predictable framework-level failure behavior.

Evaluate an exception hierarchy such as:

``` text
PipelineError
├── SourceError
├── ValidationError
├── TransformationError
└── SinkError
```

Questions to resolve:

-   Which layer owns exception wrapping?
-   Which original exception information must be preserved?
-   Which errors should stop execution immediately?
-   How should validation failures differ from infrastructure failures?

## 4.4 Retry Handling

Add retry behavior at the execution/engine level.

Expected flow:

``` text
Attempt 1
   ↓
Pipeline failure
   ↓
Attempt 2
   ↓
Success / retry exhaustion
```

Requirements:

-   Configurable retry count
-   Clear retry logging
-   Preserve final failure information
-   Do not implement retry independently inside every
    transformer/source/sink
-   Test success after retry
-   Test retry exhaustion

## 4.5 Runtime and Resource Cleanup

Ensure resources are released on both successful and failed executions.

Focus especially on Spark runtime lifecycle.

Expected pattern:

``` text
Create runtime
    ↓
Execute pipeline
    ↓
Success or failure
    ↓
Cleanup
```

## 4.6 Tests

Add tests for:

-   Successful execution status
-   Failed execution status
-   Stage-specific failures
-   Retry success
-   Retry exhaustion
-   Runtime cleanup after success
-   Runtime cleanup after failure
-   Existing E2E pipeline remains green

## Sprint 4 Definition of Done

-   [ ] Structured logging implemented
-   [ ] Execution lifecycle/status implemented
-   [ ] Execution timing available
-   [ ] Exception behavior is consistent
-   [ ] Retry mechanism implemented
-   [ ] Runtime cleanup verified
-   [ ] Unit tests added
-   [ ] Existing integration/E2E tests pass

------------------------------------------------------------------------

# Sprint 5 --- Configuration & Extensibility

## Goal

Allow new pipelines to be assembled primarily through configuration
instead of framework code changes.

This sprint intentionally revisits abstractions postponed during Sprint
3.

## 5.1 Generic CompositeValidator

Refactor the current business-specific composite so it can receive
validators:

``` text
CompositeValidator
├── Validator A
├── Validator B
└── Validator C
```

The composite should execute validators and combine their results
without knowing business-specific rules.

## 5.2 Generic CompositeTransformer

Refactor transformation composition similarly:

``` text
CompositeTransformer
├── Transformer A
├── Transformer B
└── Transformer C
```

The composite should preserve transformer order.

## 5.3 ValidatorBuilder and TransformerBuilder

Introduce specialized builders only when nested configuration requires
them.

Expected flow:

``` text
Pipeline configuration
        ↓
PipelineBuilder
        ↓
ValidatorBuilder / TransformerBuilder
        ↓
Registry
        ↓
Concrete components
```

## 5.4 Configuration-Driven Composition

Support configurations conceptually similar to:

``` json
{
  "transformers": [
    {
      "type": "filter_rows",
      "options": {
        "condition": "id > 1"
      }
    },
    {
      "type": "upper_case_name"
    }
  ]
}
```

## 5.5 Configuration Validation

Reject invalid configurations before pipeline execution begins.

Cover:

-   Missing component type
-   Unknown component type
-   Invalid options
-   Invalid nested configuration
-   Missing required configuration
-   Unsupported combinations

## 5.6 Multiple Pipelines

Demonstrate that the same framework can build different jobs:

``` text
configs/
├── users_pipeline.json
├── orders_pipeline.json
└── products_pipeline.json
```

## Sprint 5 Definition of Done

-   [ ] CompositeValidator is reusable
-   [ ] CompositeTransformer is reusable
-   [ ] Nested validator/transformer configuration can be built
-   [ ] Invalid configuration fails early
-   [ ] At least two different pipelines run without core framework
    changes
-   [ ] Builder/configuration tests pass
-   [ ] E2E tests pass

------------------------------------------------------------------------

# Sprint 6 --- Real Data Integrations

## Goal

Move from framework demonstrations to realistic Data Engineering
workloads.

## 6.1 Sources

Implement production-style sources such as:

-   PostgreSQL source
-   S3 source
-   Parquet source where useful

## 6.2 Sinks

Implement production-style sinks such as:

-   S3 sink
-   PostgreSQL sink
-   Partitioned Parquet output

## 6.3 Real End-to-End Pipelines

Example:

``` text
PostgreSQL
    ↓
Spark
    ↓
Validation
    ↓
Transformation
    ↓
Partitioned Parquet
    ↓
S3
```

Also consider the reverse direction:

``` text
S3
 ↓
Spark
 ↓
Validation
 ↓
Transformation
 ↓
PostgreSQL
```

## 6.4 Schema Management

Cover:

-   Explicit schemas
-   Schema mismatches
-   Type handling
-   Missing columns
-   Bad records
-   Schema evolution considerations

## 6.5 Write Semantics

Study and implement appropriate behavior for:

-   Append
-   Overwrite
-   Partition overwrite
-   Duplicate prevention
-   Partial write failures

## 6.6 Idempotency

A production pipeline should be safe to rerun when possible.

Questions:

-   What happens when the same execution runs twice?
-   Can duplicate rows be produced?
-   Can partially written data be detected?
-   Where should execution identifiers/checkpoints live?

## 6.7 Full vs Incremental Loads

Design how the framework could support:

``` text
Full load
Incremental load
```

Potential mechanisms to evaluate:

-   Timestamp watermark
-   Increasing ID
-   Bookmark/checkpoint
-   Partition-based processing

CDC implementation is optional at this stage; architecture understanding
is required.

## 6.8 Credentials and Environment Configuration

Separate infrastructure configuration from code.

No credentials should be committed to Git.

## Sprint 6 Definition of Done

-   [ ] PostgreSQL integration works
-   [ ] S3 integration works
-   [ ] Real Spark E2E pipeline works
-   [ ] Schema behavior tested
-   [ ] Write modes understood/tested
-   [ ] Idempotency strategy demonstrated
-   [ ] Incremental-load design documented
-   [ ] Integration tests added

------------------------------------------------------------------------

# Sprint 7 --- Airflow & Orchestration

## Goal

Run framework pipelines through a real workflow orchestrator.

## 7.1 Airflow Environment

Create a local Airflow environment suitable for development and testing.

## 7.2 DAG Integration

Architecture:

``` text
             Airflow
                │
                ▼
             Engine
                │
        PipelineExecution
                │
        Data Pipeline
```

Airflow orchestrates the framework; it does not replace it.

## 7.3 Scheduling

Implement scheduled pipeline execution.

Cover:

-   Cron/schedule configuration
-   Execution dates
-   Catchup behavior
-   Manual execution

## 7.4 Dependencies

Build a workflow containing multiple dependent jobs.

Example:

``` text
extract_users
      ↓
process_users
      ↓
publish_users
```

## 7.5 Retry Ownership

Explicitly decide when retry belongs to:

-   Framework execution
-   Airflow task
-   Infrastructure/client library

Avoid uncontrolled nested retries.

## 7.6 Parameters and Backfills

Practice:

-   DAG parameters
-   Runtime configuration
-   Historical execution
-   Backfill strategy

## 7.7 Failure Handling

Verify how pipeline failures propagate to Airflow and how operators
diagnose them.

## Sprint 7 Definition of Done

-   [ ] Airflow runs locally
-   [ ] Framework pipeline runs from an Airflow DAG
-   [ ] Scheduling works
-   [ ] Task dependencies demonstrated
-   [ ] Failure propagates correctly
-   [ ] Retry ownership documented
-   [ ] Parameterized execution demonstrated
-   [ ] Backfill behavior understood

------------------------------------------------------------------------

# Sprint 8 --- Productionization

## Goal

Prepare the framework for repeatable deployment, automated verification,
and external review.

## 8.1 Docker

Containerize the required services.

Potential stack:

``` text
Data Platform Framework
Airflow
PostgreSQL
Object storage / S3 integration
```

## 8.2 Environment Separation

Support clear environments:

``` text
local
test
production
```

Configuration and secrets must remain separate.

## 8.3 Code Quality

Introduce automated checks where appropriate:

-   `ruff`
-   `mypy`
-   `pytest`

Keep tooling useful rather than adding tools only for appearance.

## 8.4 CI/CD

Create CI for pull requests/pushes.

Expected pipeline:

``` text
Push / Pull Request
        ↓
Lint
        ↓
Type checks
        ↓
Unit tests
        ↓
Integration tests
        ↓
Build image
```

## 8.5 Metrics

Expose useful operational information such as:

-   Pipeline duration
-   Records read
-   Records written
-   Validation failures
-   Pipeline failures
-   Retry count

Evaluate which metrics belong to framework execution versus individual
components.

## 8.6 Documentation

Prepare the repository so another engineer can understand and run it.

README should cover:

-   Project purpose
-   Architecture
-   Getting started
-   Configuration
-   Creating a pipeline
-   Creating a Source
-   Creating a Validator
-   Creating a Transformer
-   Creating a Sink
-   Testing
-   Deployment

Add an architecture diagram.

## 8.7 Developer Experience

A new developer should be able to:

``` text
Clone repository
    ↓
Configure environment
    ↓
Start dependencies
    ↓
Run tests
    ↓
Run example pipeline
```

with minimal manual setup.

## Sprint 8 Definition of Done

-   [ ] Application is containerized
-   [ ] Environment configuration is clean
-   [ ] Secrets are not committed
-   [ ] Automated lint/type/test checks run
-   [ ] CI pipeline is green
-   [ ] Core operational metrics are available
-   [ ] README is complete
-   [ ] Architecture diagram exists
-   [ ] Fresh setup can run an example pipeline

------------------------------------------------------------------------

# Release --- Production Readiness

## Goal

Stop adding features and prove that the system behaves correctly under
realistic success and failure scenarios.

## Target Architecture

``` text
                  Airflow
                     │
                     ▼
                 Engine
                     │
              PipelineBuilder
                     │
              PipelineExecution
                     │
                     ▼
PostgreSQL → Spark → Validation → Transformation → S3
                     │
                     ▼
                Logs / Metrics
```

## Release Validation

Test normal operation and deliberately introduce failures.

### Infrastructure Failures

-   [ ] PostgreSQL unavailable
-   [ ] S3/object storage unavailable
-   [ ] Invalid credentials
-   [ ] Network/client failure

### Configuration Failures

-   [ ] Invalid JSON/configuration
-   [ ] Unknown source
-   [ ] Unknown validator
-   [ ] Unknown transformer
-   [ ] Unknown sink
-   [ ] Invalid component options

### Data Failures

-   [ ] Invalid schema
-   [ ] Missing required columns
-   [ ] Validation failure
-   [ ] Malformed/bad records

### Processing Failures

-   [ ] Source failure
-   [ ] Spark transformation failure
-   [ ] Sink failure
-   [ ] Retry exhaustion

### Operational Verification

-   [ ] Failure stage is clearly identifiable
-   [ ] Logs contain sufficient context
-   [ ] Runtime resources are cleaned up
-   [ ] Airflow receives correct task status
-   [ ] Reruns behave predictably
-   [ ] No duplicate/partial data is produced where idempotency is
    expected
-   [ ] Metrics reflect execution outcome

------------------------------------------------------------------------

# Final Release Checklist

## Architecture

-   [ ] Source/Validator/Transformer/Sink responsibilities are clear
-   [ ] Pipeline orchestration responsibilities are clear
-   [ ] Runtime responsibilities are clear
-   [ ] Engine responsibilities are clear
-   [ ] Airflow responsibilities are clear
-   [ ] No unnecessary abstraction remains in the critical path

## Reliability

-   [ ] Failures are predictable
-   [ ] Retries are controlled
-   [ ] Resource cleanup is guaranteed
-   [ ] Pipelines can be safely rerun where required

## Testing

-   [ ] Unit tests pass
-   [ ] Pipeline tests pass
-   [ ] Integration tests pass
-   [ ] Failure scenarios are covered
-   [ ] CI passes from a clean environment

## Operations

-   [ ] Logging is useful
-   [ ] Metrics are useful
-   [ ] Secrets are externalized
-   [ ] Deployment is reproducible
-   [ ] Example production-style pipeline works

## Documentation

-   [ ] README complete
-   [ ] Architecture diagram complete
-   [ ] Example configuration documented
-   [ ] Local setup documented
-   [ ] Testing documented
-   [ ] Deployment documented

------------------------------------------------------------------------

# Interview Preparation Track

Starting around Sprint 6, use the framework to practice architecture and
Data Engineering interview questions alongside implementation.

Topics include:

-   Why Spark instead of pandas?
-   Why are retries placed at a particular layer?
-   How does the framework support incremental loading?
-   How would the architecture change for streaming?
-   How is idempotency guaranteed?
-   What happens after a partial sink failure?
-   How should schema evolution be handled?
-   How would a 10 GB workload differ from a 5 TB workload?
-   Where should checkpoints/watermarks be stored?
-   What should Airflow own versus the framework?
-   How would the system be monitored in production?
-   How would multiple teams safely add new pipeline components?

Implementation decisions should be explainable as engineering
trade-offs, not only as code.

------------------------------------------------------------------------

# Roadmap Summary

``` text
Sprint 1  ██████████  Core abstractions          COMPLETE
Sprint 2  ██████████  Builder / runtime           COMPLETE
Sprint 3  ██████████  Spark E2E                   COMPLETE
Sprint 4  ░░░░░░░░░░  Reliability & observability NEXT
Sprint 5  ░░░░░░░░░░  Configuration/extensibility
Sprint 6  ░░░░░░░░░░  Real integrations
Sprint 7  ░░░░░░░░░░  Airflow/orchestration
Sprint 8  ░░░░░░░░░░  Productionization
Release   ░░░░░░░░░░  Production readiness
```

## Guiding Principle

Do not add abstractions simply because they may be useful later.

Each sprint should introduce complexity only when the framework has a
concrete requirement for it. Keep the architecture testable,
explainable, and focused on realistic Data Engineering problems.
