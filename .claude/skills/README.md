# Adobe CCF Security Auditor Skills

This directory contains Claude Code skills for conducting security assessments using the Adobe Common Controls Framework (CCF).

## Skill Structure

Each skill follows Anthropic's official specification:

```
.claude/skills/
├── ccf-security-auditor/
│   └── SKILL.md              # Skill definition with YAML frontmatter
├── ccf-quick-scan/
│   └── SKILL.md              # Skill definition with YAML frontmatter
└── ccf-remediation-helper/
    └── SKILL.md              # Skill definition with YAML frontmatter
```

Each `SKILL.md` file contains:
- **YAML frontmatter** with `name` and `description`
- **Instructions** in imperative form for AI consumption
- **Examples** and guidelines for usage

## Available Skills

### 1. `ccf-security-auditor` - Comprehensive Security Assessment

**Full skill name:** `ccf-security-auditor`

**Purpose:** Conduct comprehensive, end-to-end security audits using the CCF framework.

**When to use:**
- Full security posture assessment needed
- Preparing for compliance audits (SOC 2, ISO 27001, etc.)
- Initial security baseline establishment
- Annual security reviews
- Post-incident security evaluation

**What it does:**
- Guides through systematic scoping and information gathering
- Conducts domain-by-domain security control assessment
- Performs gap analysis with risk prioritization
- Generates scored security reports (0-100 scale)
- Provides actionable remediation recommendations

**Typical duration:** 30-90 minutes (depending on scope)

**Example invocation:**
```
Use the ccf-security-auditor skill to assess our web application
```

### 2. `ccf-quick-scan` - Fast Automated Code Security Scan

**Full skill name:** `ccf-quick-scan`

**Purpose:** Quickly scan a codebase for common security issues.

**When to use:**
- Quick security check needed
- Code review or PR approval
- Pre-deployment security gate
- Developer security feedback
- Initial security screening

**What it does:**
- Runs automated security scanner on code repository
- Detects hardcoded secrets, weak crypto, vulnerabilities
- Generates quick security score and findings
- Provides immediate actionable feedback

**Typical duration:** 2-5 minutes

**Example invocation:**
```
Use the ccf-quick-scan skill on the current repository
```

### 3. `ccf-remediation-helper` - Security Issue Remediation

**Full skill name:** `ccf-remediation-helper`

**Purpose:** Help fix identified security findings and implement CCF controls.

**When to use:**
- After completing an audit with findings
- When implementing specific security controls
- When fixing security vulnerabilities
- When improving existing security controls
- When you need code examples for secure implementations

**What it does:**
- Explains security findings and their risks
- Provides step-by-step remediation guidance
- Offers working code examples and configurations
- Helps with testing and validation
- Assists with documentation updates

**Typical duration:** Varies by complexity

**Example invocation:**
```
Use the ccf-remediation-helper skill to fix the hardcoded secrets issue
```

## Skill Relationships

```
┌──────────────────────────┐
│  ccf-security-auditor    │  ◄── Comprehensive audit
│   (Full Assessment)       │
└────────────┬─────────────┘
             │
             │ Identifies findings
             ▼
┌──────────────────────────┐
│  ccf-remediation-helper  │  ◄── Fix identified issues
│    (Fix Issues)           │
└──────────────────────────┘

         OR

┌──────────────────────────┐
│    ccf-quick-scan        │  ◄── Quick automated scan
│  (Fast Code Analysis)     │
└────────────┬─────────────┘
             │
             │ Identifies issues
             ▼
┌──────────────────────────┐
│  ccf-remediation-helper  │  ◄── Fix identified issues
│    (Fix Issues)           │
└──────────────────────────┘
```

## Typical Workflows

### Workflow 1: Initial Security Assessment

```
1. Invoke ccf-quick-scan
   → Get quick baseline security score

2. Invoke ccf-security-auditor
   → Conduct comprehensive assessment
   → Generate detailed report

3. Invoke ccf-remediation-helper
   → Fix critical and high priority findings

4. Re-run ccf-quick-scan
   → Verify improvements
```

### Workflow 2: Compliance Preparation

```
1. Invoke ccf-security-auditor
   → Specify compliance framework (SOC 2, ISO 27001, etc.)
   → Focus on relevant domains
   → Generate compliance gap analysis

2. Invoke ccf-remediation-helper
   → Implement required controls
   → Create compliance documentation

3. Invoke ccf-security-auditor
   → Re-assess to verify compliance readiness
```

### Workflow 3: Continuous Security

```
1. Regular ccf-quick-scan
   → Run on every PR or weekly

2. Quarterly ccf-security-auditor
   → Full assessment every quarter

3. On-demand ccf-remediation-helper
   → Fix issues as they arise
```

## Usage Tips

### For Developers

- Use `ccf-quick-scan` in your development workflow
- Run before committing security-sensitive changes
- Keep security score above 70/100
- Address critical findings immediately

### For Security Teams

- Use `ccf-security-auditor` for formal assessments
- Document all findings and evidence
- Track remediation progress
- Re-assess after major changes

### For Compliance Teams

- Use `ccf-security-auditor` with specific compliance focus
- Leverage CCF's multi-framework mapping
- Generate reports for auditors
- Maintain assessment documentation

### For DevOps/SRE

- Integrate `ccf-quick-scan` into CI/CD pipelines
- Set security score thresholds
- Automate security checks
- Monitor security posture trends

## Supporting Files

The skills use the following supporting files in the repository:

- **ccf_parser.py** - Parses Adobe CCF Excel file
- **security_auditor.py** - Core assessment framework
- **questionnaire.py** - Domain-specific questions
- **code_scanner.py** - Automated code security scanner
- **ccf_auditor_cli.py** - Interactive CLI interface
- **ccf_data.json** - Parsed CCF data (317 controls, 25 domains)
- **adobe-ccf/Open_Source_CCF.xls** - Official Adobe CCF framework

## CCF Framework Overview

The Adobe Common Controls Framework includes:

- **317 Security Controls** across **25 Domains**
- Maps to **20+ compliance frameworks**:
  - ISO 27001
  - SOC 2 (Type I & II)
  - PCI-DSS
  - HIPAA
  - GDPR
  - FedRAMP
  - NIST Cybersecurity Framework
  - CIS Controls
  - And more...

### 25 Control Domains

1. Asset Management (13)
2. Backup Management (5)
3. Business Continuity (6)
4. Change Management (4)
5. Configuration Management (15)
6. Cryptography (15)
7. Customer Managed Security (4)
8. Data Management (22)
9. Entity Management (11)
10. Identity and Access Management (39)
11. Incident Response (8)
12. Mobile Device Management (4)
13. Network Operations (18)
14. People Resources (10)
15. Privacy (10)
16. Proactive Security (4)
17. Risk Management (10)
18. Security Governance (17)
19. Service Lifecycle (7)
20. Site Operations (16)
21. System Design Documentation (2)
22. Systems Monitoring (32)
23. Third-Party Management (13)
24. Training and Awareness (9)
25. Vulnerability Management (23)

## Report Formats

All skills generate reports in two formats:

1. **JSON** (`*_report.json`) - Machine-readable, for automation
2. **Markdown** (`*_report.md`) - Human-readable, for stakeholders

## Best Practices

1. **Regular Assessments:** Run quarterly or after major changes
2. **Document Everything:** Collect evidence for all controls
3. **Prioritize Critical:** Fix critical and high findings first
4. **Track Progress:** Maintain assessment history
5. **Involve Teams:** Get input from security, dev, ops, compliance
6. **Stay Current:** Re-assess after implementing fixes
7. **Learn from Findings:** Use them to improve processes

## Customization

The skills can be customized by:

1. Editing the skill markdown files in `.claude/skills/`
2. Modifying the Python assessment tools
3. Adding custom questions to `questionnaire.py`
4. Extending the code scanner with custom checks
5. Creating additional skill variants for specific needs

## Getting Help

For issues or questions:

1. Check the main README.md in the repository root
2. Review QUICKSTART.md for setup instructions
3. Examine example_audit.py for usage examples
4. Consult the Adobe CCF documentation in adobe-ccf/

## Version Information

- **CCF Version:** v5 (Open Source)
- **Last Updated:** 2024
- **Skills Version:** 1.0
- **Python Required:** 3.7+

## License

These skills use the Adobe Common Controls Framework (CCF), which is provided by Adobe under their open-source licensing terms.

---

**Remember:** Security is a journey, not a destination. Regular assessments and continuous improvement are key to maintaining strong security posture.
