# Security Policy

## Supported Scope

Security reports are accepted for the public bluetape4k libraries and governed
workshop/example repositories maintained under the bluetape4k organization.

`ocean-workshop` and `kotlin-dev-agent` are outside the current governance
scope.

## Reporting a Vulnerability

Please report suspected vulnerabilities privately through GitHub Security
Advisories when available, or contact the repository owner directly if a
repository does not expose private vulnerability reporting.

Do not disclose exploitable details in public issues before a fix or mitigation
is available.

## Baseline Expectations

Governed repositories should maintain:

- secret scanning in CI or a scheduled security workflow,
- CodeQL or an explicit code-scanning exclusion,
- dependency visibility through Dependabot, dependency graph, or Gradle
  dependency submission,
- release-sensitive dependency updates validated through the central version
  drift and Nightly workflow policy.

The central `.github` repository owns the audit scripts and governance docs for
these expectations.
