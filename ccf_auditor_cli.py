#!/usr/bin/env python3
"""
Adobe CCF Security Auditor - Interactive CLI
Main command-line interface for conducting security audits
"""
import sys
import json
from typing import List, Optional
from security_auditor import (
    SecurityAuditor, SystemScope, ComplianceStatus,
    Priority, Finding
)
from questionnaire import QuestionnaireEngine


class CCFAuditorCLI:
    """Interactive CLI for CCF Security Auditor"""

    def __init__(self):
        self.auditor = SecurityAuditor()
        self.questionnaire = QuestionnaireEngine()
        self.scope: Optional[SystemScope] = None

    def print_header(self):
        """Print application header"""
        print("\n" + "="*80)
        print("  Adobe Common Controls Framework (CCF) Security Auditor")
        print("  Comprehensive Security Assessment Tool")
        print("="*80 + "\n")

    def print_section(self, title: str):
        """Print section header"""
        print("\n" + "-"*80)
        print(f"  {title}")
        print("-"*80 + "\n")

    def get_input(self, prompt: str, options: List[str] = None) -> str:
        """Get user input with optional validation"""
        if options:
            print(f"\n{prompt}")
            for i, option in enumerate(options, 1):
                print(f"  {i}. {option}")
            print(f"  {len(options) + 1}. Other (specify)")

            while True:
                try:
                    choice = input("\nYour choice (number or text): ").strip()

                    # Check if it's a number
                    if choice.isdigit():
                        choice_num = int(choice)
                        if 1 <= choice_num <= len(options):
                            return options[choice_num - 1]
                        elif choice_num == len(options) + 1:
                            return input("Please specify: ").strip()

                    # Check if it matches an option
                    for option in options:
                        if choice.lower() in option.lower():
                            return option

                    # Return as-is if no match
                    return choice

                except (ValueError, KeyboardInterrupt):
                    print("Invalid input. Please try again.")
        else:
            return input(f"{prompt}: ").strip()

    def conduct_scoping(self):
        """Conduct initial scoping and information gathering"""
        self.print_section("Phase 1: Scoping & Information Gathering")

        print("I'll ask you several questions to understand the scope of your system.\n")

        # System name
        system_name = self.get_input("What is the name of the system being audited?")

        # Get scoping questions
        scoping_data = {}
        for question, key, options in self.questionnaire.get_scoping_questions():
            response = self.get_input(question, options)
            scoping_data[key] = response

        # Additional context
        print("\n" + "-"*80)
        additional = self.get_input("\nAny additional context or specific concerns? (Press Enter to skip)")

        # Create scope object
        # Parse the collected data
        primary_function = scoping_data.get('scope', 'Unknown')

        # Prompt for more detailed info
        data_types_input = self.get_input(
            "\nList data types (comma-separated)",
            ["PII", "Payment data", "Health data", "Confidential", "Public"]
        )
        data_types = [d.strip() for d in data_types_input.split(',')] if data_types_input else ["Unknown"]

        architecture = self.get_input(
            "System architecture",
            ["Cloud-native", "On-premises", "Hybrid", "Multi-cloud"]
        )

        deployment = self.get_input(
            "Deployment environment",
            ["AWS", "Azure", "GCP", "On-premises", "Multiple"]
        )

        compliance_input = self.get_input(
            "Compliance requirements (comma-separated)",
            ["SOC 2", "ISO 27001", "PCI-DSS", "HIPAA", "GDPR", "FedRAMP", "None"]
        )
        compliance_reqs = [c.strip() for c in compliance_input.split(',')] if compliance_input else ["None"]

        user_base = self.get_input(
            "Primary user base",
            ["External customers", "Internal employees", "Partners", "Public", "Mixed"]
        )

        criticality = self.get_input(
            "System criticality",
            ["Critical", "High", "Medium", "Low"]
        )

        self.scope = SystemScope(
            system_name=system_name,
            primary_function=primary_function,
            data_types=data_types,
            architecture=architecture,
            deployment_environment=deployment,
            compliance_requirements=compliance_reqs,
            user_base=user_base,
            criticality=criticality,
            additional_context=additional
        )

        self.auditor.set_scope(self.scope)

        print("\n✓ Scoping completed successfully!")
        print(f"\nAuditing: {system_name}")
        print(f"Architecture: {architecture}")
        print(f"Data Types: {', '.join(data_types)}")
        print(f"Compliance: {', '.join(compliance_reqs)}")

    def conduct_systematic_review(self):
        """Conduct systematic review of CCF domains"""
        self.print_section("Phase 2: Systematic Security Review")

        print("I will now guide you through a systematic review based on CCF control domains.\n")
        print("For each domain, I'll ask targeted questions about your security controls.\n")

        domains = self.auditor.get_domains()

        # Ask which domains to review
        print("Available Control Domains:")
        for i, domain in enumerate(domains, 1):
            controls = self.auditor.get_controls_for_domain(domain)
            print(f"  {i}. {domain} ({len(controls)} controls)")

        print("\nOptions:")
        print("  1. Review all domains (comprehensive audit)")
        print("  2. Review specific domains")
        print("  3. Focus on high-priority domains")

        choice = self.get_input("\nSelect option", ["1", "2", "3"])

        if choice == "2":
            selected_input = self.get_input(
                "Enter domain numbers to review (comma-separated, e.g., 1,3,5)"
            )
            try:
                indices = [int(x.strip()) - 1 for x in selected_input.split(',')]
                domains_to_review = [domains[i] for i in indices if 0 <= i < len(domains)]
            except:
                print("Invalid input. Reviewing all domains.")
                domains_to_review = domains
        elif choice == "3":
            # High-priority domains
            high_priority = [
                "Identity and Access Management",
                "Data Management",
                "Cryptography",
                "Application Security",
                "Vulnerability Management",
                "Incident Response"
            ]
            domains_to_review = [d for d in domains if d in high_priority]
        else:
            domains_to_review = domains

        # Review each domain
        for domain_idx, domain in enumerate(domains_to_review, 1):
            self.print_section(f"Domain {domain_idx}/{len(domains_to_review)}: {domain}")

            questions = self.questionnaire.get_questions_for_domain(domain)

            if not questions:
                print(f"No predefined questions for {domain}. Skipping...\n")
                continue

            print(f"Reviewing {domain} controls...\n")

            for q_idx, (question, control_id, options) in enumerate(questions, 1):
                print(f"\nQuestion {q_idx}/{len(questions)}:")
                response = self.get_input(question, options)

                # Interpret response
                status, score = self.questionnaire.interpret_response(question, response, options)

                # Get control details
                control = self.auditor.get_control_by_id(control_id)
                if not control:
                    continue

                # Collect evidence and gaps
                gaps = []
                evidence = ""

                if status != ComplianceStatus.COMPLIANT:
                    evidence = self.get_input("  → Provide any supporting evidence or details (optional)")

                    if status == ComplianceStatus.NON_COMPLIANT:
                        gap_detail = self.get_input("  → Briefly describe the gap or issue")
                        if gap_detail:
                            gaps.append(gap_detail)

                # Assess control
                self.auditor.assess_control(
                    ccf_id=control_id,
                    status=status,
                    evidence=evidence,
                    gaps=gaps,
                    notes=f"Based on: {question}"
                )

                # Add finding if non-compliant
                if status == ComplianceStatus.NON_COMPLIANT and gaps:
                    finding_id = f"F-{domain_idx:02d}-{q_idx:02d}"
                    finding = Finding(
                        finding_id=finding_id,
                        title=f"{control['name']} - Gap Identified",
                        description=gaps[0] if gaps else "Control not implemented",
                        affected_controls=[control_id],
                        priority=self._determine_priority(domain, control_id),
                        recommendation=self._generate_recommendation(control),
                        risk_impact=self._assess_risk_impact(domain, status),
                        remediation_effort=self._estimate_effort(status)
                    )
                    self.auditor.add_finding(finding)

            print(f"\n✓ {domain} review completed!")

    def _determine_priority(self, domain: str, control_id: str) -> Priority:
        """Determine priority based on domain and control"""
        high_priority_domains = [
            "Identity and Access Management",
            "Data Management",
            "Cryptography",
            "Incident Response"
        ]

        if domain in high_priority_domains:
            return Priority.HIGH
        else:
            return Priority.MEDIUM

    def _generate_recommendation(self, control: dict) -> str:
        """Generate recommendation for a control"""
        if control.get('implementation_guidance'):
            guidance = control['implementation_guidance']
            # Take first sentence or 200 chars
            if '.' in guidance:
                return guidance.split('.')[0] + '.'
            return guidance[:200] + '...'
        return f"Implement {control['name']} according to CCF guidelines."

    def _assess_risk_impact(self, domain: str, status: ComplianceStatus) -> str:
        """Assess risk impact"""
        high_risk_domains = [
            "Identity and Access Management",
            "Data Management",
            "Cryptography"
        ]

        if domain in high_risk_domains:
            if status == ComplianceStatus.NON_COMPLIANT:
                return "High - Could lead to data breach or unauthorized access"
            else:
                return "Medium - Increased risk of security incidents"
        else:
            if status == ComplianceStatus.NON_COMPLIANT:
                return "Medium - Could impact security posture"
            else:
                return "Low - Minor security risk"

    def _estimate_effort(self, status: ComplianceStatus) -> str:
        """Estimate remediation effort"""
        if status == ComplianceStatus.NON_COMPLIANT:
            return "High - Significant implementation required"
        elif status == ComplianceStatus.PARTIAL:
            return "Medium - Enhancement of existing controls"
        else:
            return "Low - Minor adjustments needed"

    def generate_reports(self):
        """Generate and save audit reports"""
        self.print_section("Phase 3: Report Generation")

        print("Generating comprehensive security audit report...\n")

        # Generate report
        report = self.auditor.generate_report()

        # Show summary
        print(f"Overall Security Score: {report.overall_score:.1f}/100")
        print(f"\nAssessments Completed: {len(report.assessments)}")
        print(f"Findings Identified: {len(report.findings)}")

        print("\nDomain Scores:")
        for domain in sorted(report.domain_scores.keys(), key=lambda d: report.domain_scores[d]):
            score = report.domain_scores[domain]
            status = "✓" if score >= 70 else "⚠" if score >= 40 else "✗"
            print(f"  {status} {domain}: {score:.1f}/100")

        # Save reports
        print("\n" + "-"*80)
        print("Saving reports...\n")

        json_file = f"audit_report_{self.scope.system_name.replace(' ', '_')}.json"
        md_file = f"audit_report_{self.scope.system_name.replace(' ', '_')}.md"

        self.auditor.export_report_json(json_file)
        print(f"✓ JSON report saved: {json_file}")

        self.auditor.export_report_markdown(md_file)
        print(f"✓ Markdown report saved: {md_file}")

        print("\n" + "="*80)
        print("  Audit Complete!")
        print("="*80)
        print(f"\nYour security posture report is ready.")
        print(f"Review the detailed findings and recommendations in {md_file}\n")

    def run(self):
        """Run the complete audit workflow"""
        try:
            self.print_header()

            # Phase 1: Scoping
            self.conduct_scoping()

            # Phase 2: Systematic Review
            cont = self.get_input("\nProceed with systematic review?", ["Yes", "No"])
            if cont.lower().startswith('n'):
                print("Audit cancelled.")
                return

            self.conduct_systematic_review()

            # Phase 3: Report Generation
            self.generate_reports()

        except KeyboardInterrupt:
            print("\n\nAudit interrupted by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\n\nError: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """Main entry point"""
    cli = CCFAuditorCLI()
    cli.run()


if __name__ == "__main__":
    main()
