# CCF Security Auditor Skills - Usage Guide

## Quick Reference

### Skill Invocation Syntax

Skills are invoked in Claude Code conversations using natural language:

```
Use the <skill-name> skill [to do something]
```

## Available Skills

### 1. ccf-security-auditor

**Purpose:** Comprehensive security assessment

**Example Invocations:**

```
Use the ccf-security-auditor skill to assess our web application
```

```
Use the ccf-security-auditor skill for a SOC 2 compliance review
```

```
Use the ccf-security-auditor skill focusing on IAM and Data Management domains
```

**What Happens:**
1. Skill activates with GRC analyst persona
2. Conducts scoping questions
3. Performs systematic domain review
4. Generates scored security report
5. Provides prioritized remediation recommendations

**Typical Duration:** 30-90 minutes (interactive)

---

### 2. ccf-quick-scan

**Purpose:** Fast automated security scan

**Example Invocations:**

```
Use the ccf-quick-scan skill to scan this repository
```

```
Use the ccf-quick-scan skill on /path/to/codebase
```

```
Run ccf-quick-scan on the current project
```

**What Happens:**
1. Runs `code_scanner.py` on specified path
2. Analyzes code for security issues
3. Generates quick security score
4. Lists prioritized findings
5. Provides immediate actionable feedback

**Typical Duration:** 2-5 minutes (automated)

---

### 3. ccf-remediation-helper

**Purpose:** Fix security issues and implement controls

**Example Invocations:**

```
Use the ccf-remediation-helper skill to fix hardcoded secrets
```

```
Use the ccf-remediation-helper skill for control IAM-05
```

```
Help me remediate the findings from the security audit
```

**What Happens:**
1. Analyzes the security issue or control
2. Explains risks and impacts
3. Provides step-by-step remediation guidance
4. Shows working code examples
5. Assists with testing and validation

**Typical Duration:** Varies by complexity

---

## Skill Workflows

### Workflow 1: Initial Assessment

```
Step 1: Quick check
> Use the ccf-quick-scan skill to scan this repository

Step 2: Comprehensive audit
> Use the ccf-security-auditor skill to assess our application

Step 3: Fix issues
> Use the ccf-remediation-helper skill to fix the critical findings
```

### Workflow 2: Compliance Preparation

```
Step 1: Scoped assessment
> Use the ccf-security-auditor skill for SOC 2 Type II compliance

Step 2: Address gaps
> Use the ccf-remediation-helper skill for the identified gaps

Step 3: Verify fixes
> Use the ccf-quick-scan skill to verify improvements
```

### Workflow 3: Continuous Security

```
Weekly: ccf-quick-scan on every PR
Monthly: ccf-remediation-helper for new findings
Quarterly: ccf-security-auditor for comprehensive review
```

---

## Skill Parameters

### Providing Context

Skills work better with context. You can provide:

**System Information:**
```
Use the ccf-security-auditor skill to assess our e-commerce platform.
It's a Node.js application deployed on AWS, handling payment card data.
```

**Specific Focus:**
```
Use the ccf-security-auditor skill focusing on cryptography and data protection controls.
```

**Compliance Requirements:**
```
Use the ccf-security-auditor skill for PCI-DSS v4.0 compliance assessment.
```

### Referencing Files

```
Use the ccf-quick-scan skill on the ./src directory
```

```
Use the ccf-remediation-helper skill to fix the issues in code_security_report.json
```

---

## Output Files

### After ccf-security-auditor:
- `audit_report_<system_name>.json` - Machine-readable report
- `audit_report_<system_name>.md` - Human-readable report

### After ccf-quick-scan:
- `code_security_report.json` - Scan results (JSON)
- `code_security_report.md` - Scan results (Markdown)

### Working with Reports:

```
Please review the findings in audit_report_MyApp.md and help me prioritize
```

```
Use the ccf-remediation-helper skill to address finding F-001 from the report
```

---

## Advanced Usage

### Chaining Skills

Skills can be chained in a single conversation:

```
First, use ccf-quick-scan on this repo, then use ccf-remediation-helper
to fix any critical issues you find, and finally run ccf-quick-scan again
to verify the fixes.
```

### Programmatic Integration

For automation, you can use the Python tools directly:

```python
# Quick scan
python3 code_scanner.py /path/to/repo "My App"

# Interactive audit
python3 ccf_auditor_cli.py

# Custom audit
python3 example_audit.py
```

### Skill + Direct Tool Usage

```
Use the ccf-security-auditor skill, but let me run the code scanner manually first:

$ python3 code_scanner.py . "MyApp"

Now review these results and continue with the full audit.
```

---

## Skill Behavior

### What Skills Do

✅ **Skills will:**
- Ask clarifying questions
- Request evidence and documentation
- Provide risk-based prioritization
- Generate professional reports
- Offer actionable recommendations
- Show code examples
- Explain compliance requirements

❌ **Skills will NOT:**
- Make changes to your code without permission
- Execute commands without your approval
- Make assumptions about your environment
- Store sensitive data

### Evidence Collection

Skills may request:
- Screenshots of configurations
- Policy documents
- Audit logs or reports
- Architecture diagrams
- Test results
- Compliance certificates

You can provide these inline or reference file paths.

---

## Troubleshooting

### Skill Not Responding

If a skill doesn't activate:

```
# Try explicit invocation:
Invoke the ccf-security-auditor skill

# Or reference the skill file:
Load .claude/skills/ccf-security-auditor.md and execute it
```

### Missing Dependencies

If Python tools fail:

```bash
# Install required packages:
pip install xlrd openpyxl pandas --break-system-packages

# Verify CCF data is parsed:
python3 ccf_parser.py

# Check ccf_data.json exists:
ls -l ccf_data.json
```

### Partial Results

Skills can work with partial information:

```
I don't have all the information right now. Use the ccf-security-auditor skill
and mark controls as "not assessed" where I don't have data.
```

---

## Best Practices

### 1. Start with Quick Scan

Always run `ccf-quick-scan` first for a baseline:

```
Use ccf-quick-scan to get a quick baseline before we do the full audit
```

### 2. Provide Context Up Front

Better results with context:

```
Use ccf-security-auditor to assess our healthcare app (HIPAA-compliant,
handles PHI, deployed on Azure, 50,000 users)
```

### 3. Save and Reference Reports

Keep reports for tracking progress:

```
Here's the report from last quarter: [attach audit_report_Q1.md]
Use ccf-security-auditor to assess current state and compare to Q1
```

### 4. Focus on High-Priority Domains

For time-constrained audits:

```
Use ccf-security-auditor focusing only on:
- Identity and Access Management
- Data Management
- Cryptography
- Incident Response
```

### 5. Iterate on Remediation

Use remediation helper iteratively:

```
Use ccf-remediation-helper for finding F-001

[After implementing]

Did I fix it correctly? Let's verify with ccf-quick-scan
```

---

## Integration with Development Workflow

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
python3 code_scanner.py . "Pre-commit scan"
```

### CI/CD Pipeline

```yaml
# .github/workflows/security.yml
- name: CCF Security Scan
  run: |
    python3 code_scanner.py . "${{ github.repository }}"
    # Fail if score < 70
```

### Weekly Security Review

```bash
#!/bin/bash
# weekly_security_check.sh
python3 code_scanner.py /app "Weekly-$(date +%Y-%m-%d)"
```

---

## Support

For issues with skills:
1. Check `.claude/skills/README.md` for detailed documentation
2. Review `CCF_COVERAGE_ANALYSIS.md` for coverage information
3. See `README.md` for tool documentation
4. Check `QUICKSTART.md` for setup help

---

## Skill Versions

**Current Version:** 1.0.0

**What's Included:**
- 317 CCF controls
- 25 control domains
- 65 interactive questions
- Automated code scanner
- Remediation guidance
- Multi-framework compliance mapping

**Coverage:**
- Technical controls: 70-80%
- Organizational controls: 30-40%
- Overall: 50-60% automated, 100% accessible

See `CCF_COVERAGE_ANALYSIS.md` for detailed coverage breakdown.
