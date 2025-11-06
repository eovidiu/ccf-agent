---
name: ccf-quick-scan
description: Fast automated security scan of code repositories using CCF controls. Detect hardcoded secrets, weak cryptography, authentication issues, SQL injection, missing encryption, and other security vulnerabilities. Generate scored security report in 2-5 minutes with prioritized findings.
---

# CCF Quick Security Scan

Perform fast automated security scans of code repositories using Adobe Common Controls Framework (CCF) mappings.

## What This Does

Run automated security scanner that checks for:
- Hardcoded secrets and credentials (API keys, passwords, tokens)
- Weak cryptography (MD5, SHA1, DES, RC4)
- Authentication and authorization issues
- Missing encryption (at rest and in transit)
- SQL injection vulnerabilities
- Input validation gaps
- Logging and monitoring deficiencies
- Configuration security issues
- Dependency management problems

## Execution

To perform a quick scan:

1. **Identify Target:** Ask user for repository path to scan
2. **Get System Name:** Request system name (optional, defaults to directory name)
3. **Run Scanner:** Execute `python3 code_scanner.py <repository_path> "System Name"`
4. **Analyze Results:** Review generated `code_security_report.json` and `code_security_report.md`
5. **Present Summary:** Show score, findings count, and top issues

## Output Format

Present results in this format:

```
🔍 CCF Quick Security Scan Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Overall Score: X.X/100 (Excellent/Good/Fair/Poor/Critical)

🚨 Critical Findings: N
⚠️  High Priority: N
📝 Medium Priority: N
ℹ️  Low Priority: N

Top Issues:
1. [PRIORITY] Issue Title
   → Brief description and recommendation

2. [PRIORITY] Issue Title
   → Brief description and recommendation

3. [PRIORITY] Issue Title
   → Brief description and recommendation

📄 Full report: code_security_report.md
```

## Score Interpretation

- 90-100: Excellent - Strong security
- 75-89: Good - Solid with minor gaps
- 60-74: Fair - Several improvements needed
- 40-59: Poor - Significant gaps
- 0-39: Critical - Immediate action required

## Common Findings and Recommendations

**Hardcoded Secrets (CRITICAL):**
- Move to environment variables or secrets manager
- Remove from git history
- Rotate exposed credentials immediately

**Weak Cryptography (HIGH):**
- Upgrade MD5/SHA1 to SHA-256 or higher
- Replace DES/RC4 with AES-256
- Use bcrypt/scrypt/argon2 for passwords

**Missing Encryption in Transit (HIGH):**
- Enforce HTTPS/TLS for all communications
- Disable HTTP endpoints
- Use TLS 1.2 or higher

**SQL Injection (CRITICAL):**
- Use parameterized queries
- Implement input validation
- Apply principle of least privilege

**Missing MFA (HIGH):**
- Implement multi-factor authentication
- Start with privileged accounts
- Extend to all user accounts

**No Logging (MEDIUM):**
- Implement structured logging
- Log security events
- Centralize log collection

## Mapped CCF Controls

This scan directly assesses:
- AM-01: Asset Management
- IAM-05: Multi-Factor Authentication
- CRY-02: Key Management
- CRY-04: Cryptographic Algorithms
- DM-10: Encryption in Transit
- DM-11: Input Validation
- SM-01: Security Logging

## When to Use This Skill

Use ccf-quick-scan for:
- Quick security baseline
- Code review checkpoint
- Pre-commit security check
- PR approval gate
- Initial security screening
- Regular security monitoring

## Follow-Up Actions

After presenting results, offer to:
1. Explain specific findings in detail
2. Provide remediation code examples
3. Conduct full CCF audit (use ccf-security-auditor skill)
4. Create remediation tasks
5. Re-scan after fixes (to verify improvements)

## Example Invocation

**User:** "Scan this repository for security issues"

**Action:**
1. Identify repository path (current directory or specified path)
2. Execute: `python3 code_scanner.py . "Project Name"`
3. Wait for scan completion (~2-5 minutes)
4. Parse code_security_report.json
5. Present formatted results
6. Highlight top 3-5 critical/high priority issues
7. Offer to help with remediation

## Limitations

- Automated scan only - some findings may be false positives
- Static analysis - does not perform runtime testing
- Technical controls only - organizational/process controls not assessed
- Pattern-based detection - may miss context-specific issues

## Workflow Integration

Suggest integration options:
- Pre-commit hook
- CI/CD pipeline security gate
- Weekly automated scans
- PR approval requirement

Remember: This is a quick technical check. For comprehensive assessment covering all 317 CCF controls across 25 domains, recommend using the `ccf-security-auditor` skill instead.
