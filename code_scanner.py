#!/usr/bin/env python3
"""
Automated Code Scanner for CCF Security Assessment
Analyzes codebases and generates security posture reports automatically
"""
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict
from security_auditor import (
    SecurityAuditor, SystemScope, ComplianceStatus,
    Priority, Finding
)


class CodeSecurityScanner:
    """Automated security scanner for code repositories"""

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.auditor = SecurityAuditor()
        self.findings: List[Dict] = []
        self.scan_results: Dict = {}

    def scan_repository(self) -> Dict:
        """Perform comprehensive security scan of repository"""
        print(f"Scanning repository: {self.repo_path}")

        results = {
            'asset_management': self._scan_asset_management(),
            'authentication': self._scan_authentication(),
            'authorization': self._scan_authorization(),
            'cryptography': self._scan_cryptography(),
            'data_protection': self._scan_data_protection(),
            'secrets_management': self._scan_secrets(),
            'logging_monitoring': self._scan_logging(),
            'input_validation': self._scan_input_validation(),
            'error_handling': self._scan_error_handling(),
            'dependencies': self._scan_dependencies(),
            'configuration': self._scan_configuration(),
            'api_security': self._scan_api_security(),
        }

        self.scan_results = results
        return results

    def _find_files(self, extensions: List[str] = None, exclude_dirs: Set[str] = None) -> List[Path]:
        """Find files in repository"""
        if exclude_dirs is None:
            exclude_dirs = {'.git', 'node_modules', 'venv', '__pycache__', 'dist', 'build', '.next'}

        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rb', '.php', '.cs']

        files = []
        for ext in extensions:
            for file_path in self.repo_path.rglob(f'*{ext}'):
                # Skip excluded directories
                if any(excluded in file_path.parts for excluded in exclude_dirs):
                    continue
                files.append(file_path)

        return files

    def _scan_file_content(self, file_path: Path, patterns: Dict[str, str]) -> List[Dict]:
        """Scan file for pattern matches"""
        matches = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')

                for pattern_name, pattern in patterns.items():
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line, re.IGNORECASE):
                            matches.append({
                                'file': str(file_path.relative_to(self.repo_path)),
                                'line': line_num,
                                'pattern': pattern_name,
                                'content': line.strip()[:100]
                            })
        except Exception as e:
            pass

        return matches

    def _scan_asset_management(self) -> Dict:
        """Scan for asset management practices (AM-*)"""
        print("  → Scanning asset management...")

        # Check for documentation
        docs = list(self.repo_path.rglob('README*')) + list(self.repo_path.rglob('ARCHITECTURE*'))
        has_documentation = len(docs) > 0

        # Check for dependency files
        dependency_files = [
            'package.json', 'requirements.txt', 'Gemfile', 'go.mod',
            'pom.xml', 'build.gradle', 'composer.json', 'Cargo.toml'
        ]
        has_dependency_management = any((self.repo_path / f).exists() for f in dependency_files)

        return {
            'has_documentation': has_documentation,
            'has_dependency_management': has_dependency_management,
            'documentation_files': [str(d.relative_to(self.repo_path)) for d in docs]
        }

    def _scan_authentication(self) -> Dict:
        """Scan for authentication controls (IAM-*)"""
        print("  → Scanning authentication...")

        files = self._find_files()

        # Patterns for authentication issues
        patterns = {
            'hardcoded_credentials': r'(password|passwd|pwd|secret|api[_-]?key|token)\s*=\s*["\'][^"\']+["\']',
            'weak_password_check': r'password.*length.*[<>]=?\s*[1-7][^0-9]',
            'basic_auth': r'Basic\s+[A-Za-z0-9+/=]+',
            'session_management': r'(session|cookie|jwt|token)',
            'mfa_indicators': r'(mfa|2fa|multi.?factor|totp|authenticator)',
        }

        auth_issues = []
        mfa_found = False

        for file_path in files:
            matches = self._scan_file_content(file_path, patterns)
            for match in matches:
                if match['pattern'] in ['hardcoded_credentials', 'weak_password_check', 'basic_auth']:
                    auth_issues.append(match)
                elif match['pattern'] == 'mfa_indicators':
                    mfa_found = True

        return {
            'mfa_implemented': mfa_found,
            'auth_issues_count': len(auth_issues),
            'auth_issues': auth_issues[:10]  # Limit to first 10
        }

    def _scan_authorization(self) -> Dict:
        """Scan for authorization controls (IAM-*)"""
        print("  → Scanning authorization...")

        files = self._find_files()

        patterns = {
            'rbac': r'(role|permission|acl|authorize|@requires|@permission)',
            'access_control': r'(canAccess|hasPermission|checkAuth|isAuthorized)',
        }

        matches = []
        for file_path in files:
            matches.extend(self._scan_file_content(file_path, patterns))

        has_rbac = len(matches) > 0

        return {
            'has_rbac': has_rbac,
            'rbac_references': len(matches)
        }

    def _scan_cryptography(self) -> Dict:
        """Scan for cryptographic controls (CR-*)"""
        print("  → Scanning cryptography...")

        files = self._find_files()

        patterns = {
            'weak_crypto': r'(md5|sha1|des|rc4)[\(\s]',
            'strong_crypto': r'(aes|sha256|sha384|sha512|bcrypt|scrypt|argon2)',
            'encryption': r'(encrypt|decrypt|cipher)',
            'tls_ssl': r'(tls|ssl|https)',
        }

        weak_crypto = []
        strong_crypto = []

        for file_path in files:
            matches = self._scan_file_content(file_path, patterns)
            for match in matches:
                if match['pattern'] == 'weak_crypto':
                    weak_crypto.append(match)
                elif match['pattern'] == 'strong_crypto':
                    strong_crypto.append(match)

        return {
            'weak_crypto_count': len(weak_crypto),
            'weak_crypto_issues': weak_crypto[:10],
            'strong_crypto_found': len(strong_crypto) > 0
        }

    def _scan_data_protection(self) -> Dict:
        """Scan for data protection controls (DM-*)"""
        print("  → Scanning data protection...")

        files = self._find_files()

        patterns = {
            'pii_data': r'(ssn|social.?security|credit.?card|passport|driver.?license|email|phone.?number)',
            'encryption_at_rest': r'(encrypt.*file|encrypt.*disk|encrypt.*storage)',
            'encryption_in_transit': r'(https|tls|ssl)',
            'data_sanitization': r'(sanitize|escape|validate.*input)',
        }

        matches = {}
        for pattern_name, pattern in patterns.items():
            pattern_matches = []
            for file_path in files:
                pattern_matches.extend(self._scan_file_content(file_path, {pattern_name: pattern}))
            matches[pattern_name] = len(pattern_matches)

        return {
            'pii_references': matches.get('pii_data', 0),
            'encryption_at_rest': matches.get('encryption_at_rest', 0) > 0,
            'encryption_in_transit': matches.get('encryption_in_transit', 0) > 0,
            'data_sanitization': matches.get('data_sanitization', 0) > 0
        }

    def _scan_secrets(self) -> Dict:
        """Scan for hardcoded secrets and credentials"""
        print("  → Scanning for secrets...")

        files = self._find_files()

        patterns = {
            'aws_keys': r'AKIA[0-9A-Z]{16}',
            'api_keys': r'api[_-]?key["\']?\s*[:=]\s*["\'][a-zA-Z0-9]{20,}',
            'passwords': r'password["\']?\s*[:=]\s*["\'][^"\']+["\']',
            'tokens': r'token["\']?\s*[:=]\s*["\'][a-zA-Z0-9_\-\.]{20,}',
            'private_keys': r'BEGIN\s+(RSA|DSA|EC)\s+PRIVATE\s+KEY',
        }

        secrets_found = []
        for file_path in files:
            matches = self._scan_file_content(file_path, patterns)
            secrets_found.extend(matches)

        return {
            'secrets_count': len(secrets_found),
            'secrets_found': secrets_found[:10]  # Limit output
        }

    def _scan_logging(self) -> Dict:
        """Scan for logging and monitoring (SM-*)"""
        print("  → Scanning logging and monitoring...")

        files = self._find_files()

        patterns = {
            'logging': r'(logger|log\.|console\.(log|error|warn)|logging\.|syslog)',
            'monitoring': r'(metric|monitor|trace|span|telemetry)',
            'audit_log': r'(audit|security.?log)',
        }

        matches = {}
        for pattern_name, pattern in patterns.items():
            pattern_matches = []
            for file_path in files:
                pattern_matches.extend(self._scan_file_content(file_path, {pattern_name: pattern}))
            matches[pattern_name] = len(pattern_matches)

        return {
            'has_logging': matches.get('logging', 0) > 0,
            'has_monitoring': matches.get('monitoring', 0) > 0,
            'has_audit_logging': matches.get('audit_log', 0) > 0,
            'logging_statements': matches.get('logging', 0)
        }

    def _scan_input_validation(self) -> Dict:
        """Scan for input validation"""
        print("  → Scanning input validation...")

        files = self._find_files()

        patterns = {
            'validation': r'(validate|sanitize|escape|clean)',
            'sql_injection': r'(execute|query|sql).*\+.*["\']',
            'xss_protection': r'(escapeHtml|sanitizeHtml|xss)',
        }

        validation_count = 0
        sql_injection_risks = []

        for file_path in files:
            matches = self._scan_file_content(file_path, patterns)
            for match in matches:
                if match['pattern'] == 'validation':
                    validation_count += 1
                elif match['pattern'] == 'sql_injection':
                    sql_injection_risks.append(match)

        return {
            'has_validation': validation_count > 0,
            'validation_count': validation_count,
            'sql_injection_risks': len(sql_injection_risks),
            'sql_injection_issues': sql_injection_risks[:5]
        }

    def _scan_error_handling(self) -> Dict:
        """Scan for error handling"""
        print("  → Scanning error handling...")

        files = self._find_files()

        patterns = {
            'try_catch': r'(try\s*{|except|catch\s*\()',
            'error_exposure': r'(printStackTrace|console\.error|print.*error)',
        }

        try_catch_count = 0
        error_exposure = []

        for file_path in files:
            matches = self._scan_file_content(file_path, patterns)
            for match in matches:
                if match['pattern'] == 'try_catch':
                    try_catch_count += 1
                elif match['pattern'] == 'error_exposure':
                    error_exposure.append(match)

        return {
            'has_error_handling': try_catch_count > 0,
            'error_handling_count': try_catch_count,
            'error_exposure_count': len(error_exposure)
        }

    def _scan_dependencies(self) -> Dict:
        """Scan dependency management (TPM-*, VM-*)"""
        print("  → Scanning dependencies...")

        dependency_files = {
            'package.json': 'Node.js',
            'requirements.txt': 'Python',
            'Gemfile': 'Ruby',
            'go.mod': 'Go',
            'pom.xml': 'Java (Maven)',
            'build.gradle': 'Java (Gradle)',
            'composer.json': 'PHP',
            'Cargo.toml': 'Rust'
        }

        found_files = []
        for dep_file, tech in dependency_files.items():
            file_path = self.repo_path / dep_file
            if file_path.exists():
                found_files.append({'file': dep_file, 'technology': tech})

        return {
            'has_dependency_management': len(found_files) > 0,
            'dependency_files': found_files
        }

    def _scan_configuration(self) -> Dict:
        """Scan configuration management (CM-*)"""
        print("  → Scanning configuration...")

        config_files = []
        for pattern in ['*.config', '*.conf', '*.ini', '*.yaml', '*.yml', '.env*']:
            config_files.extend(self.repo_path.rglob(pattern))

        # Check for environment variable usage
        files = self._find_files()
        env_var_usage = []

        for file_path in files:
            matches = self._scan_file_content(file_path, {
                'env_vars': r'(process\.env|os\.environ|ENV\[|getenv)'
            })
            env_var_usage.extend(matches)

        return {
            'config_files_count': len(config_files),
            'uses_env_vars': len(env_var_usage) > 0,
            'env_var_references': len(env_var_usage)
        }

    def _scan_api_security(self) -> Dict:
        """Scan API security practices"""
        print("  → Scanning API security...")

        files = self._find_files()

        patterns = {
            'cors': r'(cors|access-control-allow)',
            'rate_limiting': r'(rate.?limit|throttle)',
            'api_keys': r'(api.?key|x-api-key)',
            'authentication_header': r'(authorization|bearer|x-auth)',
        }

        matches = {}
        for pattern_name, pattern in patterns.items():
            pattern_matches = []
            for file_path in files:
                pattern_matches.extend(self._scan_file_content(file_path, {pattern_name: pattern}))
            matches[pattern_name] = len(pattern_matches)

        return {
            'has_cors': matches.get('cors', 0) > 0,
            'has_rate_limiting': matches.get('rate_limiting', 0) > 0,
            'has_api_authentication': matches.get('authentication_header', 0) > 0
        }

    def generate_assessment(self, system_name: str = None) -> Dict:
        """Generate security assessment based on scan results"""
        print("\nGenerating security assessment...")

        if not system_name:
            system_name = self.repo_path.name

        # Create scope
        scope = SystemScope(
            system_name=system_name,
            primary_function="Code repository analysis",
            data_types=["Source code", "Configuration"],
            architecture="Unknown",
            deployment_environment="Unknown",
            compliance_requirements=["Best practices"],
            user_base="Developers",
            criticality="Medium"
        )

        self.auditor.set_scope(scope)

        # Assess controls based on scan results
        self._assess_controls()

        # Generate report
        report = self.auditor.generate_report()

        return report.to_dict()

    def _assess_controls(self):
        """Assess CCF controls based on scan results"""
        results = self.scan_results

        # Asset Management
        if results['asset_management']['has_documentation']:
            self.auditor.assess_control('AM-01', ComplianceStatus.COMPLIANT,
                                       evidence="Documentation found")
        else:
            self.auditor.assess_control('AM-01', ComplianceStatus.NON_COMPLIANT,
                                       gaps=["No system documentation found"])
            self._add_finding("AM-01", "Missing System Documentation",
                            "No README or architecture documentation found",
                            Priority.MEDIUM)

        # Authentication
        auth_result = results['authentication']
        if auth_result['auth_issues_count'] > 0:
            self.auditor.assess_control('IAM-05', ComplianceStatus.NON_COMPLIANT,
                                       gaps=[f"Found {auth_result['auth_issues_count']} authentication issues"])
            self._add_finding("IAM-05", "Authentication Issues Detected",
                            f"Hardcoded credentials or weak authentication found",
                            Priority.CRITICAL)
        elif auth_result['mfa_implemented']:
            self.auditor.assess_control('IAM-05', ComplianceStatus.COMPLIANT,
                                       evidence="MFA implementation found")
        else:
            self.auditor.assess_control('IAM-05', ComplianceStatus.PARTIAL,
                                       evidence="Basic authentication present, MFA not detected")

        # Cryptography
        crypto_result = results['cryptography']
        if crypto_result['weak_crypto_count'] > 0:
            self.auditor.assess_control('CR-04', ComplianceStatus.NON_COMPLIANT,
                                       gaps=[f"Found {crypto_result['weak_crypto_count']} weak cryptography instances"])
            self._add_finding("CR-04", "Weak Cryptography Detected",
                            "MD5, SHA1, DES, or RC4 usage found",
                            Priority.HIGH)
        elif crypto_result['strong_crypto_found']:
            self.auditor.assess_control('CR-04', ComplianceStatus.COMPLIANT,
                                       evidence="Strong cryptography algorithms in use")

        # Data Protection
        data_result = results['data_protection']
        if data_result['encryption_in_transit']:
            self.auditor.assess_control('DM-10', ComplianceStatus.COMPLIANT,
                                       evidence="HTTPS/TLS usage detected")
        else:
            self.auditor.assess_control('DM-10', ComplianceStatus.NON_COMPLIANT,
                                       gaps=["No encryption in transit detected"])
            self._add_finding("DM-10", "Missing Encryption in Transit",
                            "HTTPS/TLS not detected in code",
                            Priority.HIGH)

        # Secrets Management
        secrets_result = results['secrets_management']
        if secrets_result['secrets_count'] > 0:
            self.auditor.assess_control('CR-02', ComplianceStatus.NON_COMPLIANT,
                                       gaps=[f"Found {secrets_result['secrets_count']} hardcoded secrets"])
            self._add_finding("CR-02", "Hardcoded Secrets Detected",
                            f"Found {secrets_result['secrets_count']} potential secrets in code",
                            Priority.CRITICAL)

        # Logging
        log_result = results['logging_monitoring']
        if log_result['has_audit_logging']:
            self.auditor.assess_control('SM-01', ComplianceStatus.COMPLIANT,
                                       evidence="Audit logging detected")
        elif log_result['has_logging']:
            self.auditor.assess_control('SM-01', ComplianceStatus.PARTIAL,
                                       evidence="Basic logging present, audit logging not detected")
        else:
            self.auditor.assess_control('SM-01', ComplianceStatus.NON_COMPLIANT,
                                       gaps=["No logging detected"])

        # Input Validation
        input_result = results['input_validation']
        if input_result['sql_injection_risks'] > 0:
            self.auditor.assess_control('DM-11', ComplianceStatus.NON_COMPLIANT,
                                       gaps=[f"SQL injection risks detected"])
            self._add_finding("DM-11", "SQL Injection Risk",
                            f"Found {input_result['sql_injection_risks']} potential SQL injection vulnerabilities",
                            Priority.CRITICAL)

    def _add_finding(self, control_id: str, title: str, description: str, priority: Priority):
        """Add a finding to the audit"""
        finding = Finding(
            finding_id=f"F-{len(self.auditor.findings) + 1:03d}",
            title=title,
            description=description,
            affected_controls=[control_id],
            priority=priority,
            recommendation=f"Review and remediate {control_id}: {title}",
            risk_impact="See control description for impact",
            remediation_effort="Medium"
        )
        self.auditor.add_finding(finding)


def main():
    """Main entry point for code scanner"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 code_scanner.py <repository_path> [system_name]")
        print("\nExample: python3 code_scanner.py /path/to/repo 'My Application'")
        sys.exit(1)

    repo_path = sys.argv[1]
    system_name = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(repo_path):
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)

    print("="*80)
    print("  Adobe CCF Security Code Scanner")
    print("="*80)

    scanner = CodeSecurityScanner(repo_path)

    # Perform scan
    print("\nScanning repository...")
    scanner.scan_repository()

    # Generate assessment
    report_dict = scanner.generate_assessment(system_name)

    # Save report
    output_file = f"code_security_report.json"
    with open(output_file, 'w') as f:
        json.dump(report_dict, f, indent=2)

    print(f"\n✓ Scan complete!")
    print(f"✓ Report saved: {output_file}")
    print(f"\nOverall Score: {report_dict['overall_score']:.1f}/100")
    print(f"Findings: {len(report_dict['findings'])}")

    # Save markdown report
    scanner.auditor.export_report_markdown("code_security_report.md")
    print(f"✓ Markdown report: code_security_report.md")


if __name__ == "__main__":
    main()
