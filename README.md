# Adobe CCF Security Auditor

A comprehensive security review and assessment tool based on the **Adobe Common Controls Framework (CCF)**. This tool enables organizations to systematically evaluate their security posture, identify gaps, and generate detailed security audit reports.

## Overview

The Adobe Common Controls Framework (CCF) is a comprehensive and rationalized set of security and privacy controls that maps to multiple industry standards, regulations, and certifications including:

- ISO 27001
- SOC 2
- PCI-DSS
- FedRAMP
- HIPAA
- NIST Cybersecurity Framework
- CIS Controls
- And more...

This tool provides **two modes** of operation:

1. **Interactive Audit Mode**: Guided questionnaire-based security assessment
2. **Automated Code Scanner Mode**: Automated analysis of code repositories

## 🎯 Quick Start: Use as Claude Code Skills

This tool includes **Claude Code skills** for seamless integration with Claude Code:

### Available Skills

1. **`ccf-security-auditor`** - Comprehensive security assessment
   - Full end-to-end security audit with guided questionnaire
   - Systematic domain-by-domain control review
   - Scored reports with gap analysis

2. **`ccf-quick-scan`** - Fast automated code security scan
   - Quick security check in 2-5 minutes
   - Detects hardcoded secrets, weak crypto, vulnerabilities
   - Immediate actionable feedback

3. **`ccf-remediation-helper`** - Security issue remediation
   - Step-by-step guidance to fix security findings
   - Working code examples and configurations
   - Testing and validation support

### Using the Skills

Simply invoke a skill in your Claude Code conversation:

```
Use the ccf-quick-scan skill to scan this repository
```

or

```
Use the ccf-security-auditor skill to assess our application
```

**Skill Documentation:**
- 📖 [`.claude/skills/README.md`](.claude/skills/README.md) - Complete skill documentation
- 🚀 [`.claude/QUICK_REFERENCE.md`](.claude/QUICK_REFERENCE.md) - Quick reference card
- 📋 [`.claude/SKILLS_USAGE.md`](.claude/SKILLS_USAGE.md) - Detailed usage guide
- 📊 [`CCF_COVERAGE_ANALYSIS.md`](CCF_COVERAGE_ANALYSIS.md) - Framework coverage analysis

## Features

- **317 Security Controls** across **25 Control Domains**
- **Interactive Questionnaire** with domain-specific questions
- **Automated Code Scanning** for security issues
- **Gap Analysis** and prioritized findings
- **Security Scoring** (0-100) overall and by domain
- **Comprehensive Reports** in JSON and Markdown formats
- **Compliance Mapping** to major security frameworks
- **Risk-Based Prioritization** (Critical, High, Medium, Low)

## Architecture

```
.
├── .claude/                              # Claude Code Skills (Primary Interface)
│   ├── skills/
│   │   ├── ccf-security-auditor/
│   │   │   └── SKILL.md                 # Comprehensive security assessment skill
│   │   ├── ccf-quick-scan/
│   │   │   └── SKILL.md                 # Fast code security scan skill
│   │   ├── ccf-remediation-helper/
│   │   │   └── SKILL.md                 # Security remediation guidance skill
│   │   └── README.md                    # Skills documentation
│   ├── skills.json                      # Skills manifest and metadata
│   ├── QUICK_REFERENCE.md               # Quick reference card
│   └── SKILLS_USAGE.md                  # Detailed usage guide
│
├── adobe-ccf/
│   └── Open_Source_CCF.xls              # Adobe CCF framework data (official)
│
├── Python Tools (Skill Backend):
│   ├── ccf_parser.py                    # Parse CCF Excel into structured data
│   ├── ccf_data.json                    # Parsed CCF data (317 controls, 25 domains)
│   ├── security_auditor.py              # Core assessment engine and reporting
│   ├── questionnaire.py                 # Domain-specific questions (65 questions)
│   ├── code_scanner.py                  # Automated code security scanner
│   ├── ccf_auditor_cli.py               # Interactive CLI interface
│   └── example_audit.py                 # Example programmatic usage
│
├── Documentation:
│   ├── README.md                        # Main documentation (this file)
│   ├── QUICKSTART.md                    # 5-minute setup guide
│   └── CCF_COVERAGE_ANALYSIS.md         # Detailed coverage analysis
│
└── Configuration:
    └── .gitignore                       # Ignore reports and cache files
```

## Installation

### Prerequisites

- Python 3.7+
- pip

### Setup

```bash
# Install required dependencies
pip install xlrd openpyxl pandas

# Parse CCF data (one-time setup)
python3 ccf_parser.py

# This generates ccf_data.json which is used by the auditor
```

## Usage

### Mode 1: Interactive Audit (Recommended for Comprehensive Audits)

Run the interactive CLI to conduct a guided security assessment:

```bash
python3 ccf_auditor_cli.py
```

#### Workflow:

1. **Scoping & Information Gathering**
   - System name and primary function
   - Data types (PII, payment data, etc.)
   - Architecture and deployment environment
   - Compliance requirements
   - User base and criticality

2. **Systematic Security Review**
   - Choose domains to assess (all or specific)
   - Answer targeted questions for each domain
   - Provide evidence and identify gaps
   - Real-time compliance status tracking

3. **Report Generation**
   - Overall security score (0-100)
   - Domain-specific scores
   - Prioritized findings and recommendations
   - Detailed gap analysis
   - Remediation guidance

#### Example Session:

```
================================================================================
  Adobe Common Controls Framework (CCF) Security Auditor
  Comprehensive Security Assessment Tool
================================================================================

Phase 1: Scoping & Information Gathering
--------------------------------------------------------------------------------

What is the name of the system being audited?: My Web Application

What is the primary function of the system?
  1. Web application
  2. API service
  3. Mobile app
  4. Database system
  5. Other (specify)

Your choice: 1

[... continues with more questions ...]
```

### Mode 2: Automated Code Scanner (Quick Assessment)

Scan a code repository for security issues automatically:

```bash
python3 code_scanner.py <repository_path> [system_name]
```

#### Example:

```bash
python3 code_scanner.py /path/to/your/repo "My Application"
```

#### What It Scans:

- **Authentication Issues**: Hardcoded credentials, weak password checks
- **Cryptography**: Weak algorithms (MD5, SHA1, DES, RC4)
- **Secrets Management**: API keys, tokens, private keys in code
- **Data Protection**: Encryption at rest and in transit
- **Input Validation**: SQL injection risks, XSS vulnerabilities
- **Logging & Monitoring**: Audit logs, security events
- **Configuration**: Environment variables, config files
- **Dependencies**: Third-party package management
- **API Security**: CORS, rate limiting, authentication
- **Error Handling**: Exception management, error exposure

#### Output:

```
================================================================================
  Adobe CCF Security Code Scanner
================================================================================

Scanning repository: /path/to/repo
  → Scanning asset management...
  → Scanning authentication...
  → Scanning cryptography...
  → Scanning data protection...
  → Scanning for secrets...
  → Scanning logging and monitoring...
  → Scanning input validation...
  [...]

✓ Scan complete!
✓ Report saved: code_security_report.json
✓ Markdown report: code_security_report.md

Overall Score: 67.5/100
Findings: 8
```

## Report Formats

### JSON Report

Machine-readable format containing:
- Complete scope information
- All control assessments
- Findings with priorities
- Domain and overall scores
- Executive summary
- Recommendations

```json
{
  "scope": { ... },
  "assessment_date": "2024-03-01 10:30:00",
  "overall_score": 75.5,
  "domain_scores": { ... },
  "assessments": [ ... ],
  "findings": [ ... ]
}
```

### Markdown Report

Human-readable format with:
- Executive summary
- Security score dashboard
- Key findings by priority
- Detailed control assessments
- Prioritized recommendations

## Control Domains

The tool covers 25 CCF control domains:

1. **Asset Management** (13 controls) - Inventory and lifecycle management
2. **Identity and Access Management** (39 controls) - Authentication, authorization, MFA
3. **Data Management** (22 controls) - Data classification, encryption, DLP
4. **Cryptography** (15 controls) - Encryption standards, key management
5. **Application Security** (via Configuration Management) - Secure coding, testing
6. **Vulnerability Management** (23 controls) - Scanning, patching, pentesting
7. **Systems Monitoring** (32 controls) - Logging, SIEM, alerting
8. **Network Operations** (18 controls) - Firewalls, segmentation, IDS/IPS
9. **Incident Response** (8 controls) - IR plan, detection, response
10. **Business Continuity** (6 controls) - BCP, RTO/RPO, DR
11. **Configuration Management** (15 controls) - Hardening, baselines
12. **Change Management** (4 controls) - Change control, approval
13. **Third-Party Management** (13 controls) - Vendor assessment, contracts
14. **Security Governance** (17 controls) - Policies, governance body
15. **Risk Management** (10 controls) - Risk assessment, tracking
16. **Training and Awareness** (9 controls) - Security training
17. **Privacy** (10 controls) - Privacy controls and compliance
18. **Backup Management** (5 controls) - Backup procedures
19. **Mobile Device Management** (4 controls) - MDM controls
20. **Physical Security** (Site Operations - 16 controls)
21. **People Resources** (10 controls) - HR security
22. **Proactive Security** (4 controls) - Threat intelligence
23. **Service Lifecycle** (7 controls) - SDLC security
24. **System Design Documentation** (2 controls)
25. **Customer Managed Security** (4 controls)

## Scoring Methodology

### Control-Level Scoring

Each control is assessed with one of the following statuses:

- **Compliant** (100 points): Control fully implemented and effective
- **Partial** (50 points): Control partially implemented or needs improvement
- **Non-Compliant** (0 points): Control not implemented or ineffective
- **Not Applicable** (excluded from scoring): Control doesn't apply to this system
- **Not Assessed** (0 points): Control not yet evaluated

### Domain Scoring

Domain score = Average of all assessed controls in that domain (excluding N/A controls)

### Overall Security Score

Overall score = Average of all assessed controls across all domains (excluding N/A controls)

### Score Interpretation

- **90-100**: Excellent - Strong security posture
- **75-89**: Good - Solid security with minor gaps
- **60-74**: Fair - Moderate security, several improvements needed
- **40-59**: Poor - Significant security gaps
- **0-39**: Critical - Immediate action required

## Finding Priorities

Findings are prioritized based on risk and impact:

- **CRITICAL**: Immediate action required (e.g., hardcoded secrets, SQL injection)
- **HIGH**: Address within 30 days (e.g., missing encryption, weak crypto)
- **MEDIUM**: Address within 90 days (e.g., missing documentation, partial controls)
- **LOW**: Address within 6 months (e.g., policy updates, minor improvements)

## Example Use Cases

### 1. Pre-Audit Preparation

Use the interactive audit mode to prepare for SOC 2, ISO 27001, or other compliance audits:

```bash
python3 ccf_auditor_cli.py
```

Select compliance requirements during scoping, answer questions honestly, and receive a gap analysis report highlighting areas needing attention before the formal audit.

### 2. Continuous Security Assessment

Integrate the code scanner into your CI/CD pipeline:

```bash
# In your CI/CD script
python3 code_scanner.py . "MyApp-${BUILD_NUMBER}"

# Check the score and fail the build if below threshold
# Parse code_security_report.json for automation
```

### 3. Third-Party Security Review

Evaluate the security posture of vendors or acquired codebases:

```bash
python3 code_scanner.py /path/to/vendor/code "Vendor Name"
```

### 4. Security Program Maturity Assessment

Track your organization's security maturity over time by running periodic audits and comparing scores across domains.

### 5. Compliance Mapping

Identify which controls satisfy multiple compliance requirements simultaneously using the CCF's built-in mappings to ISO 27001, SOC 2, NIST, etc.

## Advanced Usage

### Custom Assessments

You can programmatically use the security auditor:

```python
from security_auditor import SecurityAuditor, SystemScope, ComplianceStatus

# Initialize auditor
auditor = SecurityAuditor()

# Set scope
scope = SystemScope(
    system_name="My App",
    primary_function="Web application",
    data_types=["PII"],
    architecture="Cloud-native",
    deployment_environment="AWS",
    compliance_requirements=["SOC 2"],
    user_base="External",
    criticality="High"
)
auditor.set_scope(scope)

# Assess controls
auditor.assess_control(
    ccf_id="IAM-05",
    status=ComplianceStatus.COMPLIANT,
    evidence="MFA enabled for all users"
)

# Generate report
report = auditor.generate_report()
print(f"Overall Score: {report.overall_score}")
```

### Extending the Code Scanner

Add custom security checks:

```python
from code_scanner import CodeSecurityScanner

class CustomScanner(CodeSecurityScanner):
    def _scan_custom_check(self):
        # Your custom security check
        pass
```

## Best Practices

1. **Be Honest**: Accurate answers lead to actionable recommendations
2. **Collect Evidence**: Have documentation ready (policies, configs, screenshots)
3. **Involve Teams**: Get input from DevOps, Security, and Engineering
4. **Regular Assessments**: Run quarterly or after major changes
5. **Track Progress**: Compare reports over time to measure improvement
6. **Prioritize Critical**: Address critical and high-priority findings first
7. **Document Decisions**: Record why certain controls are N/A or have risks accepted

## Limitations

- **Code Scanner**: Static analysis only, may have false positives/negatives
- **No Dynamic Testing**: Does not perform runtime security testing
- **Manual Verification**: Automated findings should be manually verified
- **Framework Coverage**: Focuses on CCF; may not cover all framework-specific nuances
- **Point-in-Time**: Assessment reflects security posture at time of audit

## Contributing

This tool is based on Adobe's open-source CCF v5. To update or extend:

1. Update `adobe-ccf/Open_Source_CCF.xls` with new CCF versions
2. Run `python3 ccf_parser.py` to regenerate `ccf_data.json`
3. Add new questions to `questionnaire.py` for new control domains
4. Extend scanner checks in `code_scanner.py` for new security patterns

## References

- [Adobe Common Controls Framework (CCF)](https://www.adobe.com/trust/compliance/adobe-ccf.html)
- [ISO/IEC 27001](https://www.iso.org/isoiec-27001-information-security.html)
- [SOC 2](https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report.html)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Controls](https://www.cisecurity.org/controls)

## License

This tool uses Adobe's open-source CCF framework. Please refer to Adobe's licensing terms for the CCF data.

## Support

For issues, questions, or contributions, please open an issue in the repository.

---

**Disclaimer**: This tool provides a preliminary security assessment and should not replace professional security audits or compliance certifications. Always consult with qualified security professionals for production systems.
