#!/usr/bin/env python3
"""
Security Assessment Questionnaire
Provides domain-specific questions for systematic CCF security reviews
"""
from typing import Dict, List, Tuple
from security_auditor import ComplianceStatus, Priority


class QuestionnaireEngine:
    """Generates targeted questions for each CCF control domain"""

    # Domain-specific question templates
    DOMAIN_QUESTIONS = {
        "Asset Management": [
            ("Do you maintain a comprehensive inventory of all information systems, applications, and network devices?",
             "AM-01", ["Yes, comprehensive and automated", "Yes, but manual/incomplete", "No inventory exists"]),
            ("How frequently is your asset inventory reconciled and updated?",
             "AM-01", ["Automated/Real-time", "Monthly", "Quarterly", "Annually", "Never/Rarely"]),
            ("Are all assets classified by their criticality and data sensitivity?",
             "AM-05", ["Yes, all assets classified", "Partial classification", "No classification"]),
            ("Do you track and manage the lifecycle of your assets (from acquisition to disposal)?",
             "AM-06", ["Yes, formal process", "Informal process", "No process"]),
        ],

        "Identity and Access Management": [
            ("Do you enforce multi-factor authentication (MFA) for all users accessing sensitive systems?",
             "IAM-05", ["Yes, for all users", "Yes, for privileged users only", "No MFA implemented"]),
            ("How are user access rights provisioned and managed?",
             "IAM-01", ["Automated role-based access control", "Manual approval process", "Ad-hoc/No formal process"]),
            ("Is there a formal process for regular access reviews and recertification?",
             "IAM-08", ["Yes, quarterly or more frequent", "Yes, annually", "No formal review process"]),
            ("Are privileged accounts monitored and their activities logged?",
             "IAM-15", ["Yes, comprehensive monitoring", "Partial monitoring", "No monitoring"]),
            ("How quickly are access rights revoked when employees leave or change roles?",
             "IAM-09", ["Immediately/Same day", "Within 24 hours", "Within a week", "No formal process"]),
        ],

        "Data Management": [
            ("Is sensitive data encrypted at rest?",
             "DM-09", ["Yes, all sensitive data", "Partial encryption", "No encryption"]),
            ("Is data encrypted in transit (e.g., TLS/SSL for all communications)?",
             "DM-10", ["Yes, all transmissions", "Most transmissions", "Limited/No encryption"]),
            ("Do you have a data classification scheme in place?",
             "DM-01", ["Yes, comprehensive", "Partial/Informal", "No classification"]),
            ("Are data retention and disposal policies defined and enforced?",
             "DM-04", ["Yes, automated enforcement", "Yes, manual enforcement", "No formal policy"]),
            ("Do you implement data loss prevention (DLP) controls?",
             "DM-13", ["Yes, comprehensive DLP", "Basic DLP", "No DLP"]),
        ],

        "Application Security": [
            ("Do you follow secure coding practices and standards?",
             "CM-01", ["Yes, mandatory with enforcement", "Yes, guidelines exist", "No formal practices"]),
            ("Is security testing (SAST/DAST) integrated into your development pipeline?",
             "VM-11", ["Yes, automated in CI/CD", "Yes, manual/periodic", "No security testing"]),
            ("Do you conduct regular vulnerability assessments of applications?",
             "VM-01", ["Yes, continuously", "Yes, monthly/quarterly", "Annually or less", "Never"]),
            ("Is there a process for secure code review before deployment?",
             "CM-02", ["Yes, all code reviewed", "Critical code only", "No formal review"]),
            ("How do you manage third-party dependencies and libraries?",
             "VM-14", ["Automated scanning and updates", "Manual tracking", "No formal process"]),
        ],

        "Network Operations": [
            ("Is network segmentation implemented to separate sensitive systems?",
             "NO-02", ["Yes, comprehensive segmentation", "Basic segmentation", "No segmentation"]),
            ("Are firewalls configured following the principle of least privilege?",
             "NO-01", ["Yes, deny-by-default", "Partially configured", "Minimal restrictions"]),
            ("Do you monitor network traffic for anomalies and threats?",
             "SM-01", ["Yes, 24/7 monitoring", "Business hours only", "No monitoring"]),
            ("Are intrusion detection/prevention systems (IDS/IPS) deployed?",
             "NO-11", ["Yes, comprehensive", "Limited deployment", "Not deployed"]),
            ("Is wireless network access properly secured (WPA3, certificate-based auth)?",
             "NO-09", ["Yes, enterprise-grade security", "Basic security (WPA2)", "Weak/No security"]),
        ],

        "Systems Monitoring": [
            ("Are security logs collected from all critical systems?",
             "SM-01", ["Yes, comprehensive collection", "Partial collection", "Minimal/No collection"]),
            ("How long are security logs retained?",
             "SM-03", ["1+ years", "6-12 months", "1-6 months", "Less than 1 month"]),
            ("Is there a Security Information and Event Management (SIEM) system in place?",
             "SM-04", ["Yes, with active monitoring", "Yes, but limited use", "No SIEM"]),
            ("Are logs reviewed regularly for security incidents?",
             "SM-05", ["Yes, automated analysis", "Yes, manual review", "Rarely/Never reviewed"]),
            ("Do you have alerting configured for critical security events?",
             "SM-08", ["Yes, comprehensive alerts", "Basic alerts", "No alerting"]),
        ],

        "Vulnerability Management": [
            ("How frequently are systems scanned for vulnerabilities?",
             "VM-01", ["Continuously", "Weekly", "Monthly", "Quarterly", "Annually or less"]),
            ("What is your target timeframe for patching critical vulnerabilities?",
             "VM-02", ["Within 24 hours", "Within 1 week", "Within 1 month", "No defined timeframe"]),
            ("Is there a formal vulnerability management program?",
             "VM-01", ["Yes, comprehensive program", "Basic program", "No formal program"]),
            ("Are penetration tests conducted regularly?",
             "VM-12", ["Yes, quarterly or more", "Yes, annually", "Never conducted"]),
            ("Do you track and manage vulnerabilities to closure?",
             "VM-03", ["Yes, formal tracking system", "Informal tracking", "No tracking"]),
        ],

        "Cryptography": [
            ("Are cryptographic standards defined and enforced organization-wide?",
             "CR-01", ["Yes, comprehensive policy", "Basic guidelines", "No standards"]),
            ("How are cryptographic keys managed?",
             "CR-02", ["Hardware Security Module (HSM)", "Key management service", "No formal management"]),
            ("Are encryption algorithms up-to-date and comply with industry standards?",
             "CR-04", ["Yes, modern algorithms only", "Mix of old and new", "Outdated algorithms in use"]),
            ("Is there a key rotation policy?",
             "CR-03", ["Yes, automated rotation", "Yes, manual rotation", "No rotation policy"]),
        ],

        "Incident Response": [
            ("Do you have a documented incident response plan?",
             "IR-01", ["Yes, tested regularly", "Yes, but not tested", "No formal plan"]),
            ("Is there a dedicated incident response team?",
             "IR-02", ["Yes, 24/7 team", "Yes, business hours", "No dedicated team"]),
            ("How are security incidents detected?",
             "IR-03", ["Automated detection systems", "Manual monitoring", "Reactive/reported by users"]),
            ("What is your average time to detect a security incident?",
             "IR-04", ["< 1 hour", "< 24 hours", "< 1 week", "> 1 week"]),
            ("Are incident response procedures tested through tabletop exercises or simulations?",
             "IR-09", ["Yes, quarterly or more", "Yes, annually", "Never tested"]),
        ],

        "Business Continuity": [
            ("Do you have a business continuity plan (BCP)?",
             "BC-01", ["Yes, tested regularly", "Yes, but not tested", "No BCP"]),
            ("What is your Recovery Time Objective (RTO) for critical systems?",
             "BC-03", ["< 4 hours", "< 24 hours", "< 1 week", "Not defined"]),
            ("What is your Recovery Point Objective (RPO) for critical data?",
             "BC-03", ["< 1 hour", "< 24 hours", "< 1 week", "Not defined"]),
            ("Are backups tested regularly for restoration?",
             "BM-03", ["Yes, monthly or more", "Yes, quarterly", "Annually or less", "Never tested"]),
        ],

        "Access Control": [
            ("Is the principle of least privilege enforced for all accounts?",
             "IAM-03", ["Yes, strictly enforced", "Partially enforced", "Not enforced"]),
            ("Are administrative privileges separated from regular user accounts?",
             "IAM-14", ["Yes, separate admin accounts", "Same accounts with elevation", "No separation"]),
            ("Is there session timeout configured for inactive sessions?",
             "IAM-19", ["Yes, < 15 minutes", "Yes, < 30 minutes", "Yes, > 30 minutes", "No timeout"]),
        ],

        "Configuration Management": [
            ("Are system configurations hardened according to security benchmarks (CIS, STIG)?",
             "CM-04", ["Yes, fully hardened", "Partially hardened", "No hardening"]),
            ("Is there a baseline configuration standard for all systems?",
             "CM-03", ["Yes, enforced", "Yes, but not enforced", "No baseline"]),
            ("Are configuration changes tracked and audited?",
             "CHM-01", ["Yes, automatically", "Yes, manually", "Not tracked"]),
        ],

        "Change Management": [
            ("Is there a formal change management process?",
             "CHM-01", ["Yes, comprehensive", "Basic process", "No formal process"]),
            ("Are all changes reviewed and approved before implementation?",
             "CHM-02", ["Yes, all changes", "Critical changes only", "No review process"]),
            ("Is there a rollback procedure for failed changes?",
             "CHM-04", ["Yes, tested", "Yes, but not tested", "No rollback procedure"]),
        ],

        "Third-Party Management": [
            ("Are third-party vendors assessed for security before engagement?",
             "TPM-01", ["Yes, comprehensive assessment", "Basic assessment", "No assessment"]),
            ("Do you have contracts with security and privacy requirements for vendors?",
             "TPM-03", ["Yes, all vendors", "Critical vendors only", "No security requirements"]),
            ("Is third-party access monitored and restricted?",
             "TPM-05", ["Yes, strictly controlled", "Basic controls", "No restrictions"]),
        ],

        "Security Governance": [
            ("Is there an executive-level security governance body?",
             "SG-01", ["Yes, active board/committee", "Informal governance", "No governance"]),
            ("Are security policies reviewed and updated regularly?",
             "SG-02", ["Yes, annually or more", "Every 2-3 years", "Rarely/Never"]),
            ("Is there a security awareness program?",
             "TA-01", ["Yes, comprehensive program", "Basic training", "No formal program"]),
        ],

        "Risk Management": [
            ("Do you conduct regular risk assessments?",
             "RM-01", ["Yes, quarterly or more", "Yes, annually", "Never"]),
            ("Are risks formally tracked and managed?",
             "RM-02", ["Yes, risk register maintained", "Informal tracking", "Not tracked"]),
            ("Is there a risk acceptance process for residual risks?",
             "RM-04", ["Yes, formal approval", "Informal process", "No process"]),
        ],
    }

    @staticmethod
    def get_questions_for_domain(domain: str) -> List[Tuple[str, str, List[str]]]:
        """Get questions for a specific domain"""
        return QuestionnaireEngine.DOMAIN_QUESTIONS.get(domain, [])

    @staticmethod
    def interpret_response(question: str, response: str, options: List[str]) -> Tuple[ComplianceStatus, float]:
        """
        Interpret a response and determine compliance status and score
        Returns: (ComplianceStatus, score_0_to_100)
        """
        # Normalize response
        response_lower = response.lower().strip()

        # Find which option was selected
        option_index = -1
        for i, option in enumerate(options):
            if response_lower in option.lower() or option.lower() in response_lower:
                option_index = i
                break

        # If exact match not found, try to infer
        if option_index == -1:
            if "yes" in response_lower or "comprehensive" in response_lower or "all" in response_lower:
                option_index = 0
            elif "partial" in response_lower or "basic" in response_lower or "some" in response_lower:
                option_index = min(1, len(options) - 1)
            elif "no" in response_lower or "never" in response_lower or "none" in response_lower:
                option_index = len(options) - 1

        # Determine status based on position in options
        # First option is usually best, last is usually worst
        if option_index == 0:
            return ComplianceStatus.COMPLIANT, 100.0
        elif option_index == len(options) - 1:
            return ComplianceStatus.NON_COMPLIANT, 0.0
        else:
            # Partial compliance for middle options
            score = 100.0 - (option_index / (len(options) - 1)) * 100.0
            if score > 60:
                return ComplianceStatus.PARTIAL, score
            else:
                return ComplianceStatus.NON_COMPLIANT, score

    @staticmethod
    def generate_finding_from_gap(domain: str, control_id: str, control_name: str,
                                  gap_description: str) -> Dict:
        """Generate a finding based on identified gap"""
        # Determine priority based on domain and gap severity
        high_priority_domains = ["Identity and Access Management", "Data Management",
                                "Cryptography", "Incident Response"]

        if domain in high_priority_domains:
            if "no" in gap_description.lower() or "never" in gap_description.lower():
                priority = Priority.CRITICAL
            else:
                priority = Priority.HIGH
        else:
            if "no" in gap_description.lower() or "never" in gap_description.lower():
                priority = Priority.HIGH
            else:
                priority = Priority.MEDIUM

        # Generate recommendation based on control
        recommendation = f"Implement {control_name} controls to address the identified gap. {gap_description}"

        return {
            'domain': domain,
            'control_id': control_id,
            'control_name': control_name,
            'priority': priority,
            'gap_description': gap_description,
            'recommendation': recommendation
        }

    @staticmethod
    def get_scoping_questions() -> List[Tuple[str, str, List[str]]]:
        """Get initial scoping questions"""
        return [
            ("What is the primary function of the system?",
             "scope",
             ["Web application", "API service", "Mobile app", "Desktop application",
              "Database system", "Infrastructure", "Other"]),

            ("What types of data does the system process or store?",
             "scope",
             ["Personally Identifiable Information (PII)", "Payment card data (PCI)",
              "Health information (PHI)", "Confidential business data",
              "Public data only", "Multiple types"]),

            ("What is the system architecture?",
             "scope",
             ["Cloud-native (AWS/Azure/GCP)", "On-premises", "Hybrid cloud",
              "Multi-cloud", "SaaS"]),

            ("What is the system criticality?",
             "scope",
             ["Critical (business-essential)", "High (important)", "Medium (supporting)",
              "Low (non-essential)"]),

            ("Who are the primary users?",
             "scope",
             ["External customers", "Internal employees", "Partners/vendors",
              "Public users", "Mixed"]),

            ("What compliance requirements apply?",
             "scope",
             ["SOC 2", "ISO 27001", "PCI-DSS", "HIPAA", "GDPR", "FedRAMP",
              "None specific", "Multiple"]),
        ]


def main():
    """Test the questionnaire engine"""
    engine = QuestionnaireEngine()

    print("Scoping Questions:")
    for q, _, options in engine.get_scoping_questions():
        print(f"\n{q}")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")

    print("\n" + "="*80)
    print("Sample Domain Questions (Identity and Access Management):")
    for q, control_id, options in engine.get_questions_for_domain("Identity and Access Management"):
        print(f"\n[{control_id}] {q}")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")


if __name__ == "__main__":
    main()
