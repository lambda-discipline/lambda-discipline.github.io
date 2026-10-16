# Security policy

## Supported versions

Only the live site, built from the `master` branch, is supported.

## Reporting a vulnerability

Please do not open a public issue. Report it privately through GitHub:
**Security → Report a vulnerability** on this repository
([direct link](https://github.com/lambda-discipline/lambda-discipline.github.io/security/advisories/new)).

Include the affected page or file and the steps that reproduce the problem.
You should get an acknowledgement within a week. We will agree on a
disclosure date with you once a fix is ready, and credit you in the advisory
unless you prefer otherwise.

## Scope

The site is static: plain HTML and CSS, one small inline script to filter the
builtins, no cookies, no analytics and no third-party resources. Things that
are in scope:

* Content injection or cross-site scripting through anything the build
  renders, such as an example program, its output, or a builtin's
  documentation.
* The build and deploy workflows: anything that could let a pull request,
  a change in the language repository, or a dependency publish content to the
  site or reach the workflow's credentials.
* Vulnerabilities in the Python dependencies (`requirements.txt`) or GitHub
  Actions this repository uses. Dependabot keeps them up to date.

Vulnerabilities in the language or the `lbd` interpreter belong to the
[language repository's security policy](https://github.com/lambda-discipline/lambda-discipline/blob/master/SECURITY.md).
