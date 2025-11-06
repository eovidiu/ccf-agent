# CCF Quick Security Scan

Perform a quick automated security scan of a codebase using the Adobe Common Controls Framework (CCF).

## What This Does

Runs an automated security scan that checks for:
- Hardcoded secrets and credentials
- Weak cryptography (MD5, SHA1, DES, RC4)
- Authentication and authorization issues
- Missing encryption (at rest and in transit)
- SQL injection vulnerabilities
- Input validation gaps
- Logging and monitoring deficiencies
- Configuration security issues

## Execution Steps

1. **Identify Target:**
   - Ask user for the repository path to scan
   - Ask for a system name (optional, defaults to directory name)

2. **Run Automated Scanner:**
   ```bash
   python3 code_scanner.py <repository_path> "System Name"
   ```

3. **Analyze Results:**
   - Review the generated `code_security_report.json`
   - Read the `code_security_report.md` for details

4. **Present Summary:**
   - Overall security score (0-100)
   - Number and severity of findings
   - Domain breakdown
   - Top 3-5 critical issues

5. **Provide Recommendations:**
   - Prioritized list of remediation actions
   - Quick wins vs. long-term improvements
   - Links to relevant CCF controls

## Example Output Format

```
🔍 CCF Quick Security Scan Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Overall Score: 67.5/100 (Fair)

🚨 Critical Findings: 2
⚠️  High Priority: 5
📝 Medium Priority: 8

Top Issues:
1. [CRITICAL] Hardcoded API Keys Found (3 instances)
   → Move to environment variables or secrets manager

2. [CRITICAL] Weak Cryptography Detected (MD5, SHA1 usage)
   → Upgrade to SHA-256 or higher

3. [HIGH] Missing Encryption in Transit
   → Enforce HTTPS/TLS for all communications

4. [HIGH] No Multi-Factor Authentication
   → Implement MFA for user accounts

5. [HIGH] SQL Injection Risks (2 potential vulnerabilities)
   → Use parameterized queries

📄 Full report: code_security_report.md
```

## When to Use This Skill

- Quick security assessment needed
- Code review checkpoint
- Pre-commit security check
- Initial security baseline
- Compliance pre-screening

## Follow-Up Options

After presenting results, offer to:
1. Explain specific findings in detail
2. Provide remediation code examples
3. Conduct a full interactive CCF audit
4. Create remediation tickets/tasks
5. Re-scan after fixes are applied

## Notes

- This is an automated scan - some findings may be false positives
- Results should be validated by security experts
- For comprehensive assessment, use the full `ccf-security-auditor` skill
