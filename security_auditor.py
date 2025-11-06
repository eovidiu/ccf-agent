#!/usr/bin/env python3
"""
Adobe CCF Security Auditor
Main security auditor framework for comprehensive security reviews
"""
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum


class ComplianceStatus(Enum):
    """Compliance status for a control"""
    COMPLIANT = "compliant"
    PARTIAL = "partial"
    NON_COMPLIANT = "non_compliant"
    NOT_APPLICABLE = "not_applicable"
    NOT_ASSESSED = "not_assessed"


class Priority(Enum):
    """Priority levels for findings"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class SystemScope:
    """Represents the scope of the system being audited"""
    system_name: str
    primary_function: str
    data_types: List[str]  # PII, confidential, public, etc.
    architecture: str  # cloud-native, on-prem, hybrid
    deployment_environment: str  # AWS, Azure, GCP, on-prem, etc.
    compliance_requirements: List[str]  # ISO 27001, SOC 2, PCI-DSS, etc.
    user_base: str  # internal, external, both
    criticality: str  # critical, high, medium, low
    additional_context: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class ControlAssessment:
    """Assessment result for a single control"""
    ccf_id: str
    domain: str
    control_name: str
    status: ComplianceStatus
    evidence: str = ""
    gaps: List[str] = field(default_factory=list)
    notes: str = ""
    score: float = 0.0  # 0-100

    def to_dict(self):
        data = asdict(self)
        data['status'] = self.status.value
        return data


@dataclass
class Finding:
    """Represents a security finding or gap"""
    finding_id: str
    title: str
    description: str
    affected_controls: List[str]
    priority: Priority
    recommendation: str
    risk_impact: str
    remediation_effort: str  # high, medium, low

    def to_dict(self):
        data = asdict(self)
        data['priority'] = self.priority.value
        return data


@dataclass
class AuditReport:
    """Complete audit report"""
    scope: SystemScope
    assessment_date: str
    assessments: List[ControlAssessment]
    findings: List[Finding]
    overall_score: float
    domain_scores: Dict[str, float]
    executive_summary: str
    recommendations_summary: str

    def to_dict(self):
        return {
            'scope': self.scope.to_dict(),
            'assessment_date': self.assessment_date,
            'assessments': [a.to_dict() for a in self.assessments],
            'findings': [f.to_dict() for f in self.findings],
            'overall_score': self.overall_score,
            'domain_scores': self.domain_scores,
            'executive_summary': self.executive_summary,
            'recommendations_summary': self.recommendations_summary
        }


class SecurityAuditor:
    """Main security auditor class"""

    def __init__(self, ccf_data_path: str = "ccf_data.json"):
        """Initialize the auditor with CCF data"""
        with open(ccf_data_path, 'r', encoding='utf-8') as f:
            self.ccf_data = json.load(f)

        self.controls = self.ccf_data['controls']
        self.domains = self.ccf_data['domains']
        self.evidence_list = self.ccf_data['evidence']

        self.scope: Optional[SystemScope] = None
        self.assessments: Dict[str, ControlAssessment] = {}
        self.findings: List[Finding] = []

    def set_scope(self, scope: SystemScope):
        """Set the scope for the audit"""
        self.scope = scope

    def get_domains(self) -> List[str]:
        """Get all control domains"""
        return sorted(list(self.domains.keys()))

    def get_controls_for_domain(self, domain: str) -> List[Dict]:
        """Get all controls for a specific domain"""
        control_ids = self.domains.get(domain, [])
        return [c for c in self.controls if c['ccf_id'] in control_ids]

    def get_control_by_id(self, ccf_id: str) -> Optional[Dict]:
        """Get a specific control by ID"""
        for control in self.controls:
            if control['ccf_id'] == ccf_id:
                return control
        return None

    def assess_control(self, ccf_id: str, status: ComplianceStatus,
                      evidence: str = "", gaps: List[str] = None,
                      notes: str = "") -> ControlAssessment:
        """Assess a single control"""
        control = self.get_control_by_id(ccf_id)
        if not control:
            raise ValueError(f"Control {ccf_id} not found")

        # Calculate score based on status
        score_map = {
            ComplianceStatus.COMPLIANT: 100.0,
            ComplianceStatus.PARTIAL: 50.0,
            ComplianceStatus.NON_COMPLIANT: 0.0,
            ComplianceStatus.NOT_APPLICABLE: None,  # Don't count in scoring
            ComplianceStatus.NOT_ASSESSED: 0.0
        }

        assessment = ControlAssessment(
            ccf_id=ccf_id,
            domain=control['domain'],
            control_name=control['name'],
            status=status,
            evidence=evidence,
            gaps=gaps or [],
            notes=notes,
            score=score_map[status] if score_map[status] is not None else 0.0
        )

        self.assessments[ccf_id] = assessment
        return assessment

    def add_finding(self, finding: Finding):
        """Add a finding to the audit"""
        self.findings.append(finding)

    def calculate_domain_score(self, domain: str) -> float:
        """Calculate the overall score for a domain"""
        control_ids = self.domains.get(domain, [])
        assessed_controls = [self.assessments[cid] for cid in control_ids
                           if cid in self.assessments and
                           self.assessments[cid].status != ComplianceStatus.NOT_APPLICABLE]

        if not assessed_controls:
            return 0.0

        total_score = sum(a.score for a in assessed_controls)
        return total_score / len(assessed_controls)

    def calculate_overall_score(self) -> float:
        """Calculate the overall security score"""
        assessed_controls = [a for a in self.assessments.values()
                           if a.status != ComplianceStatus.NOT_APPLICABLE]

        if not assessed_controls:
            return 0.0

        total_score = sum(a.score for a in assessed_controls)
        return total_score / len(assessed_controls)

    def generate_report(self) -> AuditReport:
        """Generate the complete audit report"""
        # Calculate scores
        overall_score = self.calculate_overall_score()
        domain_scores = {domain: self.calculate_domain_score(domain)
                        for domain in self.domains.keys()}

        # Generate executive summary
        executive_summary = self._generate_executive_summary(overall_score, domain_scores)

        # Generate recommendations summary
        recommendations_summary = self._generate_recommendations_summary()

        report = AuditReport(
            scope=self.scope,
            assessment_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            assessments=list(self.assessments.values()),
            findings=self.findings,
            overall_score=overall_score,
            domain_scores=domain_scores,
            executive_summary=executive_summary,
            recommendations_summary=recommendations_summary
        )

        return report

    def _generate_executive_summary(self, overall_score: float,
                                    domain_scores: Dict[str, float]) -> str:
        """Generate executive summary based on scores"""
        # Determine overall posture
        if overall_score >= 90:
            posture = "Excellent"
        elif overall_score >= 75:
            posture = "Good"
        elif overall_score >= 60:
            posture = "Fair"
        elif overall_score >= 40:
            posture = "Poor"
        else:
            posture = "Critical"

        # Identify weakest domains
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1])
        weakest_domains = [d[0] for d in sorted_domains[:3] if d[1] < 60]

        # Count findings by priority
        critical_findings = len([f for f in self.findings if f.priority == Priority.CRITICAL])
        high_findings = len([f for f in self.findings if f.priority == Priority.HIGH])
        medium_findings = len([f for f in self.findings if f.priority == Priority.MEDIUM])

        summary = f"""
**Overall Security Posture: {posture} ({overall_score:.1f}/100)**

The security assessment of {self.scope.system_name if self.scope else 'the system'} has been completed
based on the Adobe Common Controls Framework (CCF). The system achieved an overall security score
of {overall_score:.1f} out of 100.

**Key Statistics:**
- Total Controls Assessed: {len(self.assessments)}
- Compliant Controls: {len([a for a in self.assessments.values() if a.status == ComplianceStatus.COMPLIANT])}
- Partially Compliant: {len([a for a in self.assessments.values() if a.status == ComplianceStatus.PARTIAL])}
- Non-Compliant: {len([a for a in self.assessments.values() if a.status == ComplianceStatus.NON_COMPLIANT])}

**Findings Summary:**
- Critical Priority: {critical_findings}
- High Priority: {high_findings}
- Medium Priority: {medium_findings}
"""

        if weakest_domains:
            summary += f"\n**Areas Requiring Immediate Attention:**\n"
            for domain in weakest_domains:
                summary += f"- {domain} (Score: {domain_scores[domain]:.1f}/100)\n"

        return summary.strip()

    def _generate_recommendations_summary(self) -> str:
        """Generate prioritized recommendations summary"""
        # Group findings by priority
        critical = [f for f in self.findings if f.priority == Priority.CRITICAL]
        high = [f for f in self.findings if f.priority == Priority.HIGH]
        medium = [f for f in self.findings if f.priority == Priority.MEDIUM]
        low = [f for f in self.findings if f.priority == Priority.LOW]

        summary = "**Prioritized Recommendations:**\n\n"

        if critical:
            summary += "**CRITICAL PRIORITY (Immediate Action Required):**\n"
            for i, finding in enumerate(critical, 1):
                summary += f"{i}. {finding.title}\n"
                summary += f"   - {finding.recommendation}\n\n"

        if high:
            summary += "**HIGH PRIORITY (Address within 30 days):**\n"
            for i, finding in enumerate(high, 1):
                summary += f"{i}. {finding.title}\n"
                summary += f"   - {finding.recommendation}\n\n"

        if medium:
            summary += "**MEDIUM PRIORITY (Address within 90 days):**\n"
            for i, finding in enumerate(medium, 1):
                summary += f"{i}. {finding.title}\n"
                summary += f"   - {finding.recommendation}\n\n"

        if low:
            summary += "**LOW PRIORITY (Address within 6 months):**\n"
            for i, finding in enumerate(low, 1):
                summary += f"{i}. {finding.title}\n\n"

        return summary.strip()

    def export_report_json(self, output_path: str):
        """Export report to JSON"""
        report = self.generate_report()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)

    def export_report_markdown(self, output_path: str):
        """Export report to Markdown"""
        report = self.generate_report()

        md = f"""# Security Audit Report
**Adobe Common Controls Framework (CCF) Assessment**

---

## System Information

**System Name:** {report.scope.system_name}
**Assessment Date:** {report.assessment_date}
**Primary Function:** {report.scope.primary_function}
**Architecture:** {report.scope.architecture}
**Deployment Environment:** {report.scope.deployment_environment}
**Data Types:** {', '.join(report.scope.data_types)}
**Compliance Requirements:** {', '.join(report.scope.compliance_requirements)}
**Criticality:** {report.scope.criticality}

---

## Executive Summary

{report.executive_summary}

---

## Security Score by Domain

| Domain | Score | Status |
|--------|-------|--------|
"""

        # Add domain scores
        for domain in sorted(report.domain_scores.keys()):
            score = report.domain_scores[domain]
            status = "✓ Good" if score >= 70 else "⚠ Needs Attention" if score >= 40 else "✗ Critical"
            md += f"| {domain} | {score:.1f}/100 | {status} |\n"

        md += f"\n**Overall Score: {report.overall_score:.1f}/100**\n\n---\n\n"

        # Add findings
        md += "## Key Findings and Gaps\n\n"

        # Group findings by priority
        for priority in [Priority.CRITICAL, Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
            priority_findings = [f for f in report.findings if f.priority == priority]
            if priority_findings:
                md += f"### {priority.value.upper()} Priority\n\n"
                for finding in priority_findings:
                    md += f"#### {finding.title}\n\n"
                    md += f"**Description:** {finding.description}\n\n"
                    md += f"**Affected Controls:** {', '.join(finding.affected_controls)}\n\n"
                    md += f"**Risk Impact:** {finding.risk_impact}\n\n"
                    md += f"**Remediation Effort:** {finding.remediation_effort}\n\n"
                    md += f"**Recommendation:** {finding.recommendation}\n\n"
                    md += "---\n\n"

        # Add recommendations
        md += f"## {report.recommendations_summary}\n\n"

        # Add detailed control assessments
        md += "---\n\n## Detailed Control Assessment\n\n"

        # Group by domain
        for domain in sorted(report.domain_scores.keys()):
            domain_assessments = [a for a in report.assessments if a.domain == domain]
            if domain_assessments:
                md += f"### {domain}\n\n"
                md += f"**Domain Score:** {report.domain_scores[domain]:.1f}/100\n\n"

                for assessment in sorted(domain_assessments, key=lambda x: x.ccf_id):
                    status_icon = {
                        ComplianceStatus.COMPLIANT: "✓",
                        ComplianceStatus.PARTIAL: "◐",
                        ComplianceStatus.NON_COMPLIANT: "✗",
                        ComplianceStatus.NOT_APPLICABLE: "—",
                        ComplianceStatus.NOT_ASSESSED: "?"
                    }
                    icon = status_icon.get(assessment.status, "?")

                    md += f"#### {icon} {assessment.ccf_id}: {assessment.control_name}\n\n"
                    md += f"**Status:** {assessment.status.value.replace('_', ' ').title()}\n\n"

                    if assessment.evidence:
                        md += f"**Evidence:** {assessment.evidence}\n\n"

                    if assessment.gaps:
                        md += "**Identified Gaps:**\n"
                        for gap in assessment.gaps:
                            md += f"- {gap}\n"
                        md += "\n"

                    if assessment.notes:
                        md += f"**Notes:** {assessment.notes}\n\n"

                    md += "---\n\n"

        # Add footer
        md += f"""
---

## Report Information

**Generated:** {report.assessment_date}
**Framework:** Adobe Common Controls Framework (CCF) v5
**Auditor:** Adobe CCF Security Auditor Tool

---

*This report provides a preliminary security assessment based on the Adobe Common Controls Framework.
It should be used as a guide for improving security posture and achieving compliance with industry standards.*
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)


def main():
    """Test the security auditor"""
    auditor = SecurityAuditor()

    # Test scope
    scope = SystemScope(
        system_name="Example Web Application",
        primary_function="Customer data management and processing",
        data_types=["PII", "Confidential", "Payment Data"],
        architecture="Cloud-native",
        deployment_environment="AWS",
        compliance_requirements=["SOC 2", "ISO 27001", "GDPR"],
        user_base="External",
        criticality="High"
    )

    auditor.set_scope(scope)

    print("Security Auditor initialized successfully")
    print(f"Total Controls: {len(auditor.controls)}")
    print(f"Total Domains: {len(auditor.domains)}")


if __name__ == "__main__":
    main()
