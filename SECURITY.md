# Security Policy

## Supported Scope

Security reports should focus on vulnerabilities in this repository's scoreboard application, including replay upload and parsing logic, authentication and account flows, web views, API endpoints, deployment configuration, and project-maintained client code.

The following are outside this repository's disclosure scope:

- Touhou game binaries, replay formats, or upstream game behavior.
- Third-party services, hosting providers, browsers, or package dependencies unless the report shows a scoreboard-specific impact.
- Social engineering, spam, denial-of-service load tests, or physical attacks.
- Publicly disclosed issues that do not include a reproducible impact on this project.

## Reporting a Vulnerability

Please report suspected vulnerabilities privately using GitHub's private vulnerability reporting feature if it is available for this repository. If that option is not available, open a minimal GitHub issue that asks for a private reporting channel and avoid posting exploit details publicly.

Include enough information for maintainers to reproduce and assess the issue:

- A short summary of the vulnerability and affected component.
- Step-by-step reproduction instructions or a proof of concept.
- The expected security impact and any affected accounts, data, or permissions.
- Relevant logs, screenshots, replay files, or request examples with secrets removed.
- Suggested fixes or mitigations, if known.

Do not include real user credentials, access tokens, private data, or destructive payloads in a report.

## Coordinated Disclosure

Maintainers will acknowledge reports as availability permits and may ask for additional details, a reproduction case, or help validating a fix. Please give the project a reasonable opportunity to investigate and release a fix before public disclosure.

While researching or validating an issue, please:

- Use only accounts, data, and systems that you own or are authorized to test.
- Avoid privacy violations, data destruction, service disruption, or persistence.
- Stop testing and report promptly if you encounter sensitive data.

## Rewards

This project does not currently publish a standing paid bug bounty program in this repository. Any rewards are discretionary unless a separate official bounty is explicitly posted by the maintainers.
