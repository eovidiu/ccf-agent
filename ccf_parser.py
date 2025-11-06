#!/usr/bin/env python3
"""
Adobe CCF Parser
Parses the Open_Source_CCF.xls file and creates structured data models
"""
import xlrd
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class CCFControl:
    """Represents a single CCF control"""
    ccf_id: str
    domain: str
    name: str
    description: str
    theme: Optional[str] = None
    control_type: Optional[str] = None
    policy_standard: Optional[str] = None
    implementation_guidance: Optional[str] = None
    testing_procedure: Optional[str] = None
    audit_artifacts: Optional[str] = None
    applicable_frameworks: Optional[Dict[str, bool]] = None

    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class Evidence:
    """Represents an evidence item"""
    reference: str
    domain: str
    title: str

    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)


class CCFParser:
    """Parser for Adobe CCF Excel file"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.workbook = xlrd.open_workbook(file_path)
        self.controls: List[CCFControl] = []
        self.evidence_list: List[Evidence] = []
        self.domains: Dict[str, List[CCFControl]] = {}

    def parse(self):
        """Parse all sheets and extract structured data"""
        self._parse_controls()
        self._parse_guidance()
        self._parse_evidence()
        self._organize_by_domain()

    def _parse_controls(self):
        """Parse CCF Open Source v5 sheet"""
        try:
            sheet = self.workbook.sheet_by_name("CCF Open Source v5")
        except:
            print("Could not find 'CCF Open Source v5' sheet")
            return

        # Row 1 contains headers
        headers = [sheet.cell(1, col).value for col in range(sheet.ncols)]

        # Find key column indices
        ccf_id_col = 0
        domain_col = 1
        name_col = 2
        desc_col = 3

        # Framework columns start at index 4
        framework_start = 4

        # Parse data rows (starting from row 2)
        for row_idx in range(2, sheet.nrows):
            ccf_id = str(sheet.cell(row_idx, ccf_id_col).value).strip()

            if not ccf_id or ccf_id == '':
                continue

            domain = str(sheet.cell(row_idx, domain_col).value).strip()
            name = str(sheet.cell(row_idx, name_col).value).strip()
            description = str(sheet.cell(row_idx, desc_col).value).strip()

            # Parse applicable frameworks
            frameworks = {}
            for col_idx in range(framework_start, min(framework_start + 20, sheet.ncols)):
                if col_idx < len(headers):
                    framework_name = headers[col_idx]
                    value = str(sheet.cell(row_idx, col_idx).value).strip()
                    frameworks[framework_name] = (value.upper() == 'X')

            control = CCFControl(
                ccf_id=ccf_id,
                domain=domain,
                name=name,
                description=description,
                applicable_frameworks=frameworks
            )

            self.controls.append(control)

    def _parse_guidance(self):
        """Parse CCF Control Guidance sheet and enrich controls"""
        try:
            sheet = self.workbook.sheet_by_name("CCF Control Guidance")
        except:
            print("Could not find 'CCF Control Guidance' sheet")
            return

        # Create a mapping of CCF ID to control index
        control_map = {c.ccf_id: i for i, c in enumerate(self.controls)}

        # Parse guidance data (starting from row 1, row 0 is header)
        for row_idx in range(1, sheet.nrows):
            ccf_id = str(sheet.cell(row_idx, 0).value).strip()

            if ccf_id not in control_map:
                continue

            control_idx = control_map[ccf_id]

            # Update control with guidance information
            self.controls[control_idx].theme = str(sheet.cell(row_idx, 4).value).strip()
            self.controls[control_idx].control_type = str(sheet.cell(row_idx, 5).value).strip()
            self.controls[control_idx].policy_standard = str(sheet.cell(row_idx, 6).value).strip()
            self.controls[control_idx].implementation_guidance = str(sheet.cell(row_idx, 7).value).strip()
            self.controls[control_idx].testing_procedure = str(sheet.cell(row_idx, 8).value).strip()
            self.controls[control_idx].audit_artifacts = str(sheet.cell(row_idx, 9).value).strip()

    def _parse_evidence(self):
        """Parse Evidence Request List (ERL) sheet"""
        try:
            sheet = self.workbook.sheet_by_name("Evidence Request List (ERL)")
        except:
            print("Could not find 'Evidence Request List (ERL)' sheet")
            return

        # Parse evidence data (starting from row 1, row 0 is header)
        for row_idx in range(1, sheet.nrows):
            reference = str(sheet.cell(row_idx, 0).value).strip()
            domain = str(sheet.cell(row_idx, 1).value).strip()
            title = str(sheet.cell(row_idx, 2).value).strip()

            if not reference:
                continue

            evidence = Evidence(
                reference=reference,
                domain=domain,
                title=title
            )

            self.evidence_list.append(evidence)

    def _organize_by_domain(self):
        """Organize controls by domain"""
        for control in self.controls:
            if control.domain not in self.domains:
                self.domains[control.domain] = []
            self.domains[control.domain].append(control)

    def get_domains(self) -> List[str]:
        """Get list of all control domains"""
        return sorted(list(self.domains.keys()))

    def get_controls_by_domain(self, domain: str) -> List[CCFControl]:
        """Get all controls for a specific domain"""
        return self.domains.get(domain, [])

    def get_control_by_id(self, ccf_id: str) -> Optional[CCFControl]:
        """Get a specific control by ID"""
        for control in self.controls:
            if control.ccf_id == ccf_id:
                return control
        return None

    def export_to_json(self, output_path: str):
        """Export parsed data to JSON"""
        data = {
            'controls': [c.to_dict() for c in self.controls],
            'evidence': [e.to_dict() for e in self.evidence_list],
            'domains': {domain: [c.ccf_id for c in controls]
                       for domain, controls in self.domains.items()}
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_statistics(self) -> Dict:
        """Get statistics about the CCF"""
        return {
            'total_controls': len(self.controls),
            'total_domains': len(self.domains),
            'total_evidence_items': len(self.evidence_list),
            'controls_by_domain': {domain: len(controls)
                                  for domain, controls in self.domains.items()}
        }


def main():
    """Main function to test the parser"""
    parser = CCFParser("adobe-ccf/Open_Source_CCF.xls")
    parser.parse()

    # Print statistics
    stats = parser.get_statistics()
    print("Adobe CCF Statistics:")
    print(f"  Total Controls: {stats['total_controls']}")
    print(f"  Total Domains: {stats['total_domains']}")
    print(f"  Total Evidence Items: {stats['total_evidence_items']}")
    print("\nControls by Domain:")
    for domain, count in sorted(stats['controls_by_domain'].items()):
        print(f"  {domain}: {count} controls")

    # Export to JSON
    parser.export_to_json("ccf_data.json")
    print("\nExported data to ccf_data.json")

    # Show sample control
    print("\nSample Control (AM-01):")
    control = parser.get_control_by_id("AM-01")
    if control:
        print(f"  ID: {control.ccf_id}")
        print(f"  Domain: {control.domain}")
        print(f"  Name: {control.name}")
        print(f"  Description: {control.description[:100]}...")
        print(f"  Theme: {control.theme}")
        print(f"  Type: {control.control_type}")


if __name__ == "__main__":
    main()
