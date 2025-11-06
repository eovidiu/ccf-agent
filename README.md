# Adobe CCF Security Auditor

A comprehensive security assessment toolkit based on the **Adobe Common Controls Framework (CCF)**. This repository provides **Claude Code Skills** that enable organizations to systematically evaluate their security posture, identify gaps, and generate detailed security audit reports using Claude's native capabilities.

## Overview

The Adobe Common Controls Framework (CCF) is a comprehensive and rationalized set of 317 security and privacy controls across 25 domains that maps to multiple industry standards, regulations, and certifications including:

- ISO 27001
- SOC 2
- PCI-DSS
- FedRAMP
- HIPAA
- GDPR
- NIST Cybersecurity Framework
- CIS Controls
- And 20+ more frameworks

## 🎯 Quick Start: Claude Code Skills

This repository provides **three Claude Code Skills** for security assessment and remediation:

### Available Skills

1. **`ccf-security-auditor`** - Comprehensive Security Assessment
   - Full end-to-end security audit with guided questionnaire
   - Systematic review across 317 controls and 25 domains
   - Scored reports (0-100) with gap analysis
   - Multiple assessment modes: interactive, code-focused, domain-specific, compliance-focused
   - Generates detailed markdown and JSON reports

2. **`ccf-quick-scan`** - Fast Automated Code Security Scan
   - Quick security baseline in 2-5 minutes
   - Detects hardcoded secrets, weak cryptography, SQL injection risks
   - Missing encryption, input validation gaps, logging deficiencies
   - Immediate scored results with prioritized findings
   - Maps findings to specific CCF controls

3. **`ccf-remediation-helper`** - Security Issue Remediation
   - Step-by-step guidance to fix security findings
   - Working code examples and secure configurations
   - Technology-specific guidance (Python, JavaScript, Cloud, Kubernetes, Databases)
   - Testing procedures and validation checklists
   - Effort estimates and prioritization support

### Using the Skills in Claude Code

Simply invoke a skill in your Claude Code conversation:

**For a quick code security scan:**
```
Use the ccf-quick-scan skill to scan this repository for security issues
```

**For a comprehensive security assessment:**
```
Use the ccf-security-auditor skill to conduct a full security audit
```

**For help fixing a specific security issue:**
```
Use the ccf-remediation-helper skill to help me fix IAM-05: Missing MFA
```

## Architecture

```
.
├── .claude/skills/                       # Claude Code Skills
│   ├── ccf-security-auditor/
│   │   └── SKILL.md                     # Comprehensive security assessment skill
│   ├── ccf-quick-scan/
│   │   └── SKILL.md                     # Fast code security scan skill
│   └── ccf-remediation-helper/
│       └── SKILL.md                     # Security remediation guidance skill
│
├── adobe-ccf/
│   └── Open_Source_CCF.xls              # Adobe CCF v5 framework data (official)
│
├── ccf_data.json                        # Parsed CCF data (317 controls, 25 domains, 399 evidence items)
│
├── README.md                            # This file
├── VERIFICATION_REPORT.md               # CCF and Anthropic spec compliance verification
└── .gitignore                           # Ignore generated reports
```

## Features

### ccf-security-auditor

- **317 Security Controls** across **25 Control Domains**
- **4 Assessment Modes:**
  - Comprehensive Interactive Audit (2-4 hours)
  - Code-Focused Assessment (30-60 minutes)
  - Domain-Specific Assessment (30-90 minutes per domain)
  - Compliance Gap Analysis (1-3 hours)
- **Question-Based Evidence Collection** with 100+ domain-specific questions
- **Security Scoring** (0-100) overall and by domain
- **Comprehensive Reports** with executive summary, scorecard, findings, remediation roadmap
- **Compliance Framework Mapping** to ISO 27001, SOC 2, PCI-DSS, HIPAA, GDPR, FedRAMP, and more
- **Risk-Based Prioritization** (Critical, High, Medium, Low)
- **Gap Analysis** with actionable recommendations

### ccf-quick-scan

- **Fast Pattern-Based Scanning** using native Claude tools (Grep, Read, Glob)
- **Security Pattern Detection:**
  - Hardcoded secrets and credentials
  - Weak cryptography (MD5, SHA1, DES, RC4)
  - SQL injection risks
  - Missing HTTPS/TLS
  - Missing input validation
  - Inadequate logging
  - Insecure dependencies
- **Scored Results** (0-100) with severity categorization
- **CCF Control Mapping** to AM-01, IAM-05, CRY-02, CRY-04, DM-10, DM-11, SM-01
- **Immediate Findings** with file locations and line numbers

### ccf-remediation-helper

- **Step-by-Step Remediation Workflow**
- **Working Code Examples** in Python, JavaScript, and other languages
- **Technology-Specific Guidance:**
  - Cloud platforms (AWS, Azure, GCP)
  - Kubernetes
  - Databases (PostgreSQL, MySQL, etc.)
  - Web applications
- **Common Remediation Patterns:**
  - Hardcoded secrets → Environment variables/Secrets manager
  - Weak crypto → Strong crypto
  - SQL injection → Parameterized queries
  - Missing MFA → MFA implementation
  - Missing logging → Comprehensive logging
- **Effort Estimates** and prioritization guidance
- **Testing and Validation** procedures

## How It Works

### Native Claude Integration

These skills leverage Claude's native tools instead of external scripts:

- **Read tool:** Access CCF control definitions from ccf_data.json
- **Grep tool:** Search code for security patterns and vulnerabilities
- **Glob tool:** Find configuration files, dependencies, and sensitive files
- **Read tool:** Analyze specific code files for security assessment

This native approach provides:
- **Fast execution** without external dependencies
- **Better context awareness** from Claude's understanding
- **Seamless integration** with Claude Code workflows
- **No installation required** - works out of the box

### Assessment Workflow (ccf-security-auditor)

1. **Scoping & Information Gathering**
   - System identity and criticality
   - Data classification (PII, PHI, Payment Card Data)
   - Architecture and deployment environment
   - Compliance requirements
   - User base and resources

2. **Systematic Control Review**
   - Load controls from ccf_data.json
   - Ask domain-specific questions
   - Collect evidence and documentation
   - Assess compliance status (Compliant/Partial/Non-Compliant/N/A)

3. **Evidence Collection & Gap Analysis**
   - Document current state
   - Identify gaps and deficiencies
   - Create prioritized findings
   - Map to compliance frameworks

4. **Scoring & Reporting**
   - Calculate domain and overall scores
   - Generate executive summary
   - Create domain scorecard
   - Provide remediation roadmap
   - Map compliance gaps

5. **Next Steps & Follow-Up**
   - Present findings
   - Prioritize actions
   - Offer remediation support (via ccf-remediation-helper)
   - Plan re-assessment

## Control Domains

The CCF covers 25 comprehensive security domains:

1. **Identity and Access Management** (39 controls) - MFA, RBAC, access reviews
2. **Data Management** (22 controls) - Classification, encryption, DLP
3. **Cryptography** (15 controls) - Algorithms, key management, certificates
4. **Application Security** (19 controls) - Secure SDLC, code review, testing
5. **Vulnerability Management** (23 controls) - Scanning, patching, pentesting
6. **Systems Monitoring** (32 controls) - Logging, SIEM, alerting
7. **Network Operations** (18 controls) - Firewalls, segmentation, IDS/IPS
8. **Incident Response** (8 controls) - IR plan, detection, response team
9. **Security Governance** (17 controls) - Policies, training, metrics
10. **Third-Party Management** (13 controls) - Vendor assessment, contracts
11. **Risk Management** (10 controls) - Risk assessment, tracking
12. **Business Continuity** (6 controls) - BCP/DR, backups
13. **Change Management** (4 controls) - Change control, testing
14. **Asset Management** (11 controls) - Inventory, lifecycle
15. **Configuration Management** (15 controls) - Baselines, hardening
16. And 10 more domains...

## Scoring Methodology

### Control-Level Scoring

- **Compliant** (100 points): Control fully implemented, effective, documented
- **Partial** (50 points): Control partially implemented, gaps identified
- **Non-Compliant** (0 points): Control not implemented or ineffective
- **Not Applicable** (N/A): Excluded from scoring
- **Not Assessed** (0 points): Not yet evaluated

### Domain & Overall Scoring

- **Domain Score** = Average of assessed controls in domain (excluding N/A)
- **Overall Score** = Average of all assessed controls (excluding N/A)

### Score Interpretation

- **90-100 (Excellent)**: Strong security posture, minor improvements only
- **75-89 (Good)**: Solid security, some gaps, targeted improvements needed
- **60-74 (Fair)**: Moderate security, systematic improvements required
- **40-59 (Poor)**: Significant gaps, major improvements needed
- **0-39 (Critical)**: Severe deficiencies, immediate action required

## Example Use Cases

### 1. Pre-Audit Preparation

Use `ccf-security-auditor` to prepare for SOC 2, ISO 27001, or other compliance audits:

```
Use the ccf-security-auditor skill to assess our application for SOC 2 compliance
```

Receive a gap analysis report highlighting areas needing attention before the formal audit.

### 2. Code Security Review

Quickly scan a codebase for security vulnerabilities:

```
Use the ccf-quick-scan skill to scan this repository
```

Get immediate feedback on hardcoded secrets, weak crypto, and other security issues.

### 3. Security Issue Remediation

Get detailed guidance on fixing specific security gaps:

```
Use the ccf-remediation-helper skill to help me implement encryption at rest for our database
```

Receive step-by-step instructions, code examples, and testing procedures.

### 4. Continuous Security Assessment

Regularly assess security posture to track improvements over time:

```
Use the ccf-security-auditor skill to conduct a quarterly security assessment
```

Compare scores and findings across quarters to measure security maturity progress.

### 5. Compliance Mapping

Identify which controls satisfy multiple compliance requirements:

```
Use the ccf-security-auditor skill for a compliance gap analysis for ISO 27001 and SOC 2
```

Get a unified view of controls that address multiple frameworks simultaneously.

## Finding Priorities

Findings are prioritized based on risk and impact:

- **CRITICAL**: Immediate action required (24-48 hours)
  - Hardcoded secrets in production
  - SQL injection vulnerabilities
  - Missing authentication
  - Active exploits

- **HIGH**: Address within 30 days
  - Weak cryptography
  - Missing encryption
  - Inadequate access controls
  - Missing MFA for privileged accounts

- **MEDIUM**: Address within 90 days
  - Policy gaps
  - Incomplete controls
  - Missing documentation
  - Partial implementations

- **LOW**: Address within 6 months
  - Process improvements
  - Enhanced monitoring
  - Training programs

## Report Formats

### Markdown Report

Human-readable format with:
- Executive summary with overall score
- Security scorecard by domain
- Critical and high priority findings
- Remediation roadmap with timelines
- Compliance framework mapping
- Detailed control assessments

### JSON Data

Machine-readable format for:
- Integration with ticketing systems
- Automated compliance tracking
- Trend analysis and dashboards
- Custom reporting

## Best Practices

1. **Be Honest and Thorough**: Accurate assessments lead to actionable improvements
2. **Collect Evidence**: Have documentation, configs, and screenshots ready
3. **Involve Cross-Functional Teams**: Include DevOps, Security, Engineering, and Compliance
4. **Regular Assessments**: Run quarterly or after major changes
5. **Track Progress**: Compare reports over time to measure improvement
6. **Prioritize Critical Findings**: Address critical and high-priority items first
7. **Document Decisions**: Record why controls are N/A or risks accepted
8. **Use All Three Skills**: quick-scan → security-auditor → remediation-helper

## Compliance Framework Coverage

The Adobe CCF maps to 20+ compliance frameworks and standards:

- ISO 27001 / ISO 27002 / ISO 27017 / ISO 27018
- SOC 2 (Trust Services Criteria)
- PCI-DSS 4.0
- HIPAA Security Rule
- GDPR / CCPA (Privacy)
- FedRAMP Moderate / FedRAMP Tailored
- NIST Cybersecurity Framework
- NIST SP 800-53
- CIS Controls v8
- Cloud Security Alliance CCM
- AICPA TSC
- BSI C5
- And more...

## Limitations

- **Static Analysis**: Code scanning is pattern-based, not runtime testing
- **No Dynamic Testing**: Does not perform penetration testing or runtime security testing
- **Manual Verification Recommended**: Automated findings should be reviewed for false positives
- **Point-in-Time Assessment**: Reflects security posture at time of audit
- **Complementary Tool**: Should complement, not replace, professional security audits

## Contributing

To update or extend the CCF data:

1. Obtain the latest Adobe CCF release from [Adobe's Trust Center](https://www.adobe.com/trust/compliance/adobe-ccf.html)
2. Replace `adobe-ccf/Open_Source_CCF.xls` with the new version
3. Parse the Excel file to regenerate `ccf_data.json` if needed
4. Update skill documentation to reflect any new controls or domains

## References

- [Adobe Common Controls Framework (CCF)](https://www.adobe.com/trust/compliance/adobe-ccf.html)
- [Adobe Trust Center](https://www.adobe.com/trust.html)
- [ISO/IEC 27001](https://www.iso.org/isoiec-27001-information-security.html)
- [SOC 2](https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report.html)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Controls](https://www.cisecurity.org/controls)
- [PCI Security Standards](https://www.pcisecuritystandards.org/)

## License

This repository uses Adobe's open-source CCF framework. Please refer to Adobe's licensing terms for the CCF data.

## Verification

This repository has been verified for:
- **100% Adobe CCF Compliance**: All 317 controls, 25 domains, 399 evidence items
- **100% Anthropic Skills Specification Compliance**: Correct structure, YAML frontmatter, imperative style

See `VERIFICATION_REPORT.md` for detailed compliance verification.

## Support

For issues, questions, or contributions:
- Open an issue in the repository
- Review skill documentation in `.claude/skills/*/SKILL.md`
- Consult `VERIFICATION_REPORT.md` for implementation details

---

**Disclaimer**: This toolkit provides preliminary security assessments and should not replace professional security audits or compliance certifications. Always consult with qualified security professionals for production systems and formal compliance requirements.
