# CCF Skills - Quick Reference Card

## Skill Invocation Commands

### 🔍 Quick Security Scan (2-5 min)
```
Use the ccf-quick-scan skill to scan this repository
```

### 📋 Comprehensive Audit (30-90 min)
```
Use the ccf-security-auditor skill to assess our application
```

### 🔧 Fix Security Issues
```
Use the ccf-remediation-helper skill to fix [issue/control]
```

---

## Common Usage Patterns

| Task | Command |
|------|---------|
| Scan current repo | `Use ccf-quick-scan skill on this repository` |
| Full assessment | `Use ccf-security-auditor skill for comprehensive audit` |
| SOC 2 prep | `Use ccf-security-auditor skill for SOC 2 compliance` |
| Fix hardcoded secrets | `Use ccf-remediation-helper skill to fix hardcoded secrets` |
| Fix specific control | `Use ccf-remediation-helper skill for control IAM-05` |
| Re-scan after fixes | `Use ccf-quick-scan skill to verify improvements` |

---

## What You Get

### ccf-quick-scan →
- Security score (0-100)
- List of findings (Critical/High/Medium/Low)
- `code_security_report.json` + `.md`

### ccf-security-auditor →
- Comprehensive scored report
- Domain-by-domain assessment
- Gap analysis
- `audit_report_<name>.json` + `.md`

### ccf-remediation-helper →
- Step-by-step fix guidance
- Working code examples
- Testing procedures

---

## Quick Workflows

### New Project Assessment
```
1. Use ccf-quick-scan skill to scan this repository
2. Use ccf-security-auditor skill to assess our application
3. Use ccf-remediation-helper skill to fix critical findings
```

### Compliance Prep
```
1. Use ccf-security-auditor skill for [ISO 27001/SOC 2/PCI-DSS]
2. Review generated report
3. Use ccf-remediation-helper skill for each gap
4. Re-run ccf-quick-scan to verify
```

### PR Security Check
```
Use ccf-quick-scan skill on this PR's changes
```

---

## Setup (One-Time)

```bash
pip install xlrd openpyxl pandas --break-system-packages
python3 ccf_parser.py
```

---

## Coverage

- ✅ **317 CCF Controls** (100% data available)
- ✅ **25 Domains** (16 with interactive questions)
- ✅ **Technical Security:** 70-80% coverage
- ✅ **Compliance:** ISO 27001, SOC 2, PCI-DSS, HIPAA, GDPR

---

## Support Files

- `.claude/skills/README.md` - Full documentation
- `.claude/SKILLS_USAGE.md` - Detailed usage guide
- `CCF_COVERAGE_ANALYSIS.md` - Coverage details
- `README.md` - Main project docs
- `QUICKSTART.md` - Setup guide

---

**Pro Tip:** Start with `ccf-quick-scan` for instant feedback!
