#!/usr/bin/env python3
"""
Example Audit Script
Demonstrates programmatic usage of the CCF Security Auditor
"""
from security_auditor import (
    SecurityAuditor, SystemScope, ComplianceStatus, Priority, Finding
)


def example_web_application_audit():
    """Example: Auditing a web application"""
    print("="*80)
    print("  Example: Web Application Security Audit")
    print("="*80 + "\n")

    # Initialize auditor
    auditor = SecurityAuditor()

    # Define system scope
    scope = SystemScope(
        system_name="E-Commerce Web Application",
        primary_function="Online shopping platform with payment processing",
        data_types=["PII", "Payment Card Data", "Confidential Business Data"],
        architecture="Cloud-native microservices",
        deployment_environment="AWS (EKS, RDS, S3)",
        compliance_requirements=["PCI-DSS", "SOC 2 Type II", "GDPR"],
        user_base="External customers and internal staff",
        criticality="Critical"
    )
    auditor.set_scope(scope)

    print(f"Auditing: {scope.system_name}")
    print(f"Compliance: {', '.join(scope.compliance_requirements)}\n")

    # Asset Management
    print("Assessing Asset Management...")
    auditor.assess_control(
        "AM-01",
        ComplianceStatus.COMPLIANT,
        evidence="Comprehensive asset inventory maintained in ServiceNow CMDB, updated via automated discovery"
    )
    auditor.assess_control(
        "AM-02",
        ComplianceStatus.COMPLIANT,
        evidence="Application inventory includes all microservices, tracked in GitHub repository metadata"
    )

    # Identity and Access Management
    print("Assessing Identity and Access Management...")
    auditor.assess_control(
        "IAM-01",
        ComplianceStatus.COMPLIANT,
        evidence="Automated provisioning via Okta, role-based access control enforced"
    )
    auditor.assess_control(
        "IAM-05",
        ComplianceStatus.PARTIAL,
        evidence="MFA enforced for admin users and employees, but not for customer accounts",
        gaps=["Customer accounts do not require MFA", "Only SMS-based MFA available, no TOTP or hardware tokens"]
    )
    auditor.assess_control(
        "IAM-08",
        ComplianceStatus.COMPLIANT,
        evidence="Quarterly access reviews conducted and documented"
    )
    auditor.assess_control(
        "IAM-15",
        ComplianceStatus.COMPLIANT,
        evidence="Privileged access monitored via CloudTrail and Splunk SIEM"
    )

    # Add finding for IAM-05
    finding1 = Finding(
        finding_id="F-001",
        title="MFA Not Required for Customer Accounts",
        description="Multi-factor authentication is only enforced for administrative and employee accounts. Customer accounts rely solely on password authentication, increasing risk of account takeover.",
        affected_controls=["IAM-05"],
        priority=Priority.HIGH,
        recommendation="Implement optional MFA for customers initially, then transition to mandatory MFA with grace period. Support TOTP and WebAuthn methods.",
        risk_impact="High - Account takeover could lead to unauthorized transactions and data breach",
        remediation_effort="Medium - 2-3 sprints to implement and test"
    )
    auditor.add_finding(finding1)

    # Data Management
    print("Assessing Data Management...")
    auditor.assess_control(
        "DM-01",
        ComplianceStatus.COMPLIANT,
        evidence="Data classification policy enforced, all data assets tagged with sensitivity levels"
    )
    auditor.assess_control(
        "DM-09",
        ComplianceStatus.COMPLIANT,
        evidence="All data encrypted at rest using AES-256 (RDS encryption, S3 encryption enabled)"
    )
    auditor.assess_control(
        "DM-10",
        ComplianceStatus.COMPLIANT,
        evidence="TLS 1.2+ enforced for all communications, including microservice-to-microservice"
    )
    auditor.assess_control(
        "DM-13",
        ComplianceStatus.PARTIAL,
        evidence="Basic DLP rules configured in email gateway",
        gaps=["No DLP for web applications or API endpoints", "Cloud storage DLP not configured"]
    )

    # Add finding for DM-13
    finding2 = Finding(
        finding_id="F-002",
        title="Limited Data Loss Prevention Coverage",
        description="DLP controls are only implemented at the email gateway. No protection exists for data exfiltration via web applications, APIs, or cloud storage.",
        affected_controls=["DM-13"],
        priority=Priority.MEDIUM,
        recommendation="Extend DLP coverage to web applications (CASB solution), implement API rate limiting and anomaly detection, enable cloud storage DLP policies.",
        risk_impact="Medium - Increased risk of inadvertent or malicious data exfiltration",
        remediation_effort="High - Requires CASB procurement and configuration"
    )
    auditor.add_finding(finding2)

    # Cryptography
    print("Assessing Cryptography...")
    auditor.assess_control(
        "CRY-01",
        ComplianceStatus.COMPLIANT,
        evidence="Cryptographic standards policy published, mandates modern algorithms"
    )
    auditor.assess_control(
        "CRY-02",
        ComplianceStatus.COMPLIANT,
        evidence="AWS KMS used for key management, HSM-backed"
    )
    auditor.assess_control(
        "CRY-04",
        ComplianceStatus.COMPLIANT,
        evidence="Only approved algorithms in use: AES-256, SHA-256, RSA-2048+"
    )

    # Vulnerability Management
    print("Assessing Vulnerability Management...")
    auditor.assess_control(
        "VM-01",
        ComplianceStatus.COMPLIANT,
        evidence="Weekly vulnerability scans via Qualys, continuous scanning for containers"
    )
    auditor.assess_control(
        "VM-02",
        ComplianceStatus.PARTIAL,
        evidence="Critical OS vulnerabilities patched within 7 days",
        gaps=["Application dependency vulnerabilities not consistently patched within SLA", "No automated patching for some legacy services"]
    )
    auditor.assess_control(
        "VM-12",
        ComplianceStatus.COMPLIANT,
        evidence="Annual penetration test by third-party, last conducted 3 months ago"
    )

    # Add finding for VM-02
    finding3 = Finding(
        finding_id="F-003",
        title="Inconsistent Application Vulnerability Patching",
        description="While OS vulnerabilities are patched within 7 days, application dependencies (npm, pip packages) often exceed the 30-day SLA for high/critical vulnerabilities.",
        affected_controls=["VM-02"],
        priority=Priority.HIGH,
        recommendation="Implement automated dependency scanning in CI/CD pipeline with pull request blockers for critical vulnerabilities. Enable Dependabot or Renovate for automated updates.",
        risk_impact="High - Unpatched application vulnerabilities are frequently exploited",
        remediation_effort="Low - 1 sprint to configure and test"
    )
    auditor.add_finding(finding3)

    # Systems Monitoring
    print("Assessing Systems Monitoring...")
    auditor.assess_control(
        "SM-01",
        ComplianceStatus.COMPLIANT,
        evidence="Centralized logging via CloudWatch and Splunk, security logs retained for 1 year"
    )
    auditor.assess_control(
        "SM-04",
        ComplianceStatus.COMPLIANT,
        evidence="Splunk Enterprise SIEM with 24/7 SOC monitoring"
    )
    auditor.assess_control(
        "SM-08",
        ComplianceStatus.COMPLIANT,
        evidence="Real-time alerts configured for security events (failed auth, privilege escalation, etc.)"
    )

    # Incident Response
    print("Assessing Incident Response...")
    auditor.assess_control(
        "IR-01",
        ComplianceStatus.COMPLIANT,
        evidence="Incident response plan documented and tested quarterly via tabletop exercises"
    )
    auditor.assess_control(
        "IR-02",
        ComplianceStatus.COMPLIANT,
        evidence="24/7 incident response team via SOC outsourcing (CriticalStart)"
    )
    auditor.assess_control(
        "IR-08",
        ComplianceStatus.COMPLIANT,
        evidence="Last tabletop exercise conducted 2 months ago, full simulation annually"
    )

    # Business Continuity
    print("Assessing Business Continuity...")
    auditor.assess_control(
        "BC-01",
        ComplianceStatus.COMPLIANT,
        evidence="Business continuity plan tested annually, last test 6 months ago"
    )
    auditor.assess_control(
        "BM-03",
        ComplianceStatus.COMPLIANT,
        evidence="Database backups tested monthly, last successful restore test 3 weeks ago"
    )

    # Configuration Management
    print("Assessing Configuration Management...")
    auditor.assess_control(
        "CFM-03",
        ComplianceStatus.PARTIAL,
        evidence="CIS benchmarks applied to EC2 instances via Ansible",
        gaps=["Container images not consistently hardened", "Some third-party SaaS tools not configured per security baselines"]
    )
    auditor.assess_control(
        "CFM-04",
        ComplianceStatus.COMPLIANT,
        evidence="Infrastructure as Code (Terraform) with security scanning in CI/CD"
    )

    # Network Operations
    print("Assessing Network Operations...")
    auditor.assess_control(
        "NO-01",
        ComplianceStatus.COMPLIANT,
        evidence="AWS Security Groups configured with least privilege, deny-by-default"
    )
    auditor.assess_control(
        "NO-02",
        ComplianceStatus.COMPLIANT,
        evidence="Network segmentation via VPCs and subnets, DMZ for public-facing services"
    )

    # Third-Party Management
    print("Assessing Third-Party Management...")
    auditor.assess_control(
        "TPM-01",
        ComplianceStatus.COMPLIANT,
        evidence="Vendor security assessment process, SOC 2 reports required for critical vendors"
    )
    auditor.assess_control(
        "TPM-03",
        ComplianceStatus.COMPLIANT,
        evidence="Contracts include security requirements, SLAs, and audit rights"
    )

    # Generate report
    print("\n" + "="*80)
    print("Generating Security Audit Report...")
    print("="*80 + "\n")

    report = auditor.generate_report()

    # Display summary
    print(f"Overall Security Score: {report.overall_score:.1f}/100\n")

    print("Domain Scores:")
    for domain in sorted(report.domain_scores.keys(), key=lambda d: report.domain_scores[d], reverse=True):
        score = report.domain_scores[domain]
        if score > 0:  # Only show assessed domains
            status = "✓" if score >= 70 else "⚠" if score >= 40 else "✗"
            print(f"  {status} {domain}: {score:.1f}/100")

    print(f"\nTotal Findings: {len(report.findings)}")
    print("\nFindings by Priority:")
    for priority in [Priority.CRITICAL, Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
        count = len([f for f in report.findings if f.priority == priority])
        if count > 0:
            print(f"  {priority.value.upper()}: {count}")

    # Save reports
    auditor.export_report_json("example_audit_report.json")
    auditor.export_report_markdown("example_audit_report.md")

    print("\n✓ Reports generated:")
    print("  - example_audit_report.json")
    print("  - example_audit_report.md")

    print("\n" + "="*80)
    print("Executive Summary:")
    print("="*80)
    print(report.executive_summary)


if __name__ == "__main__":
    example_web_application_audit()
