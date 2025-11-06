# Quick Start Guide - Adobe CCF Security Auditor

Get started with the CCF Security Auditor in 5 minutes!

## Step 1: Install Dependencies (1 minute)

```bash
pip install xlrd openpyxl pandas --break-system-packages
```

## Step 2: Parse CCF Data (1 minute)

```bash
python3 ccf_parser.py
```

Expected output:
```
Adobe CCF Statistics:
  Total Controls: 317
  Total Domains: 25
  Total Evidence Items: 399

Exported data to ccf_data.json
```

## Step 3: Choose Your Mode

### Option A: Interactive Audit (Recommended for first-time users)

```bash
python3 ccf_auditor_cli.py
```

Follow the prompts:
1. Answer scoping questions about your system
2. Choose domains to review (start with 1-3 domains)
3. Answer targeted security questions
4. Receive your security report!

**Estimated time**: 15-45 minutes depending on domains selected

### Option B: Automated Code Scan (Quick assessment)

```bash
python3 code_scanner.py /path/to/your/code "Your App Name"
```

**Estimated time**: 1-5 minutes depending on codebase size

## Step 4: Review Your Reports

The tool generates two report formats:

1. **Markdown Report** - Human-readable, great for sharing
   - File: `audit_report_*.md` or `code_security_report.md`
   - Open with any text editor or Markdown viewer

2. **JSON Report** - Machine-readable, for automation
   - File: `audit_report_*.json` or `code_security_report.json`
   - Can be parsed by scripts or imported into other tools

## Understanding Your Score

| Score Range | Rating | Meaning |
|-------------|--------|---------|
| 90-100 | Excellent | Strong security posture |
| 75-89 | Good | Solid with minor gaps |
| 60-74 | Fair | Several improvements needed |
| 40-59 | Poor | Significant gaps |
| 0-39 | Critical | Immediate action required |

## Quick Examples

### Example 1: Scan This Repository

```bash
# Scan the CCF auditor tool itself!
python3 code_scanner.py . "CCF Auditor"
```

### Example 2: Quick 3-Domain Assessment

```bash
python3 ccf_auditor_cli.py
# When prompted for domains, choose option 3 (high-priority domains)
# This will focus on:
# - Identity and Access Management
# - Data Management
# - Cryptography
# - Application Security
# - Vulnerability Management
# - Incident Response
```

### Example 3: Programmatic Usage

Create a file `my_audit.py`:

```python
from security_auditor import SecurityAuditor, SystemScope, ComplianceStatus

# Initialize
auditor = SecurityAuditor()

# Define scope
scope = SystemScope(
    system_name="My Test App",
    primary_function="Web application",
    data_types=["PII"],
    architecture="Cloud-native",
    deployment_environment="AWS",
    compliance_requirements=["SOC 2"],
    user_base="External",
    criticality="High"
)
auditor.set_scope(scope)

# Assess some controls
auditor.assess_control("AM-01", ComplianceStatus.COMPLIANT,
                       evidence="Asset inventory maintained in CMDB")
auditor.assess_control("IAM-05", ComplianceStatus.PARTIAL,
                       evidence="MFA for privileged users only",
                       gaps=["MFA not enforced for all users"])
auditor.assess_control("DM-10", ComplianceStatus.NON_COMPLIANT,
                       gaps=["No encryption in transit for internal APIs"])

# Generate report
auditor.export_report_markdown("my_audit_report.md")
print(f"Score: {auditor.calculate_overall_score():.1f}/100")
```

Run it:
```bash
python3 my_audit.py
```

## Tips for Best Results

1. **Start Small**: Begin with 2-3 high-priority domains
2. **Be Prepared**: Have access to:
   - Security policies and procedures
   - Architecture diagrams
   - Configuration examples
   - Recent security assessments
3. **Involve Teams**: Get input from:
   - Security team
   - DevOps/Infrastructure
   - Development team
   - Compliance team
4. **Take Notes**: Document evidence as you go
5. **Set Aside Time**: Block 30-60 minutes for a thorough assessment

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'xlrd'"

**Solution**: Install dependencies
```bash
pip install xlrd openpyxl pandas --break-system-packages
```

### Issue: "FileNotFoundError: ccf_data.json"

**Solution**: Run the parser first
```bash
python3 ccf_parser.py
```

### Issue: Code scanner finds too many false positives

**Solution**: Review findings manually and adjust thresholds. The scanner is conservative by design.

## Next Steps

1. **Review Your Report**: Understand your current security posture
2. **Prioritize Findings**: Start with Critical and High priority items
3. **Create Action Plan**: Assign owners and deadlines for remediation
4. **Track Progress**: Re-run assessments quarterly
5. **Compare Over Time**: Watch your score improve!

## Sample Report Preview

After running an assessment, your report will look like:

```markdown
# Security Audit Report
**Adobe Common Controls Framework (CCF) Assessment**

## System Information
**System Name:** My Web Application
**Overall Score: 72.5/100**

## Security Score by Domain

| Domain | Score | Status |
|--------|-------|--------|
| Identity and Access Management | 65.0/100 | ⚠ Needs Attention |
| Data Management | 80.0/100 | ✓ Good |
| Cryptography | 90.0/100 | ✓ Good |
...

## Key Findings

### CRITICAL Priority
1. Hardcoded Secrets Detected
   - Found 3 potential secrets in code
   - Recommendation: Move to environment variables or secrets manager

### HIGH Priority
2. Missing MFA for All Users
   - MFA only enforced for privileged accounts
   - Recommendation: Extend MFA to all user accounts
...
```

## Getting Help

- **Questions?** Check the main [README.md](README.md)
- **Issues?** Review the console output for specific errors
- **Need More?** Examine the detailed Markdown report for guidance

---

**You're now ready to conduct your first security assessment!** 🎉

Start with: `python3 ccf_auditor_cli.py`
