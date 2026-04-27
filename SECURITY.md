# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.7   | :white_check_mark: |
| 1.0.5   | :white_check_mark: |
| < 1.0.5 | :x:                |

## Reporting a Vulnerability

We take the security of nabla-hooks seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **alban.andrieu@free.fr**

Include the following information:

1. **Type of issue** (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
2. **Full paths** of source file(s) related to the manifestation of the issue
3. **Location** of the affected source code (tag/branch/commit or direct URL)
4. **Step-by-step instructions** to reproduce the issue
5. **Proof-of-concept or exploit code** (if possible)
6. **Impact** of the issue, including how an attacker might exploit it

This information will help us triage your report more quickly.

### What to Expect

- **Acknowledgment**: You should receive an acknowledgment within 48 hours
- **Initial Assessment**: We will provide an initial assessment within 5 business days
- **Progress Updates**: We will keep you informed of our progress
- **Disclosure**: We will work with you to understand the issue and develop a fix
- **Credit**: You will be credited for the discovery (unless you prefer to remain anonymous)

### Security Update Process

1. **Validation**: We validate the reported vulnerability
2. **Development**: We develop a fix in a private repository
3. **Testing**: We thoroughly test the fix
4. **Release**: We release a security update
5. **Announcement**: We announce the vulnerability and fix (after the fix is deployed)

## Security Best Practices

### For Users

When using nabla-hooks, follow these security best practices:

1. **Keep Updated**: Always use the latest version
2. **Review Configuration**: Regularly review your configuration files
3. **Secure Credentials**: Never commit JIRA credentials or tokens to version control
4. **Use Environment Variables**: Store sensitive data in environment variables
5. **Validate Inputs**: Be cautious with user-provided commit messages

### Credential Management

When using JIRA integration:

```bash
# ✅ Good - Use environment variables
export JIRA_USER=your-email@example.com
export JIRA_PASSWORD=your-api-token
export JIRA_URL=https://your-domain.atlassian.net

# ❌ Bad - Don't hardcode credentials
JIRA_USER="user@example.com"  # In script files
```

### Certificate Validation

When using custom certificates:

```bash
# Always use proper certificate paths
export JIRA_CERT_PATH=/etc/ssl/certs/ca-certificates.crt

# Don't disable SSL verification in production
```

## Known Security Considerations

### 1. Dependency Security

This project uses several dependencies. We:
- Regularly update dependencies
- Monitor security advisories
- Use tools like Dependabot, Bandit, and Checkov

### 2. Code Execution

Git hooks execute code on your system. Be aware:
- Hooks run with your user permissions
- Review hooks before installation
- Only install hooks from trusted sources

### 3. Sensitive Data

Be careful not to expose sensitive data:
- JIRA credentials
- API tokens
- Internal URLs
- Private repository information

## Security Tools in Use

We use several security tools to maintain code quality:

- **Bandit**: Python security linter
- **Checkov**: Infrastructure as code security scanning
- **Gitleaks**: Secret detection
- **Grype**: Vulnerability scanning
- **Semgrep**: Static analysis security testing
- **Dependabot**: Automated dependency updates

## Security Scanning

Run security scans locally:

```bash
# Run Bandit
bandit -r hooks/ pre_commit_hooks/

# Run Checkov
checkov --directory .

# Run Gitleaks
gitleaks detect --source . --verbose

# Run Grype
grype .
```

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine affected versions
2. Audit code to find any similar problems
3. Prepare fixes for all supported versions
4. Release new versions as soon as possible

We aim to:
- Acknowledge reports within 48 hours
- Provide fixes within 30 days for critical vulnerabilities
- Provide fixes within 90 days for non-critical vulnerabilities

## Past Security Advisories

No security advisories have been published for this project yet.

## Security Hall of Fame

We would like to thank the following individuals for responsibly disclosing security vulnerabilities:

*(No entries yet)*

## Additional Resources

- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [GitHub Security Advisories](https://github.com/AlbanAndrieu/nabla-hooks/security/advisories)

## Contact

For security-related questions or concerns, please contact:
- **Email**: alban.andrieu@free.fr
- **Gitter**: [nabla-hooks/Lobby](https://gitter.im/nabla-hooks/Lobby)

---

Thank you for helping keep nabla-hooks and its users safe!
