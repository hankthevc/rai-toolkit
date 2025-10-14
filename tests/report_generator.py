"""HTML report generator for RAI Toolkit stress tests.

Produces a comprehensive, visually-appealing report categorizing issues by severity
and providing actionable recommendations for governance professionals.
"""

from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Template


class Issue:
    """Represents a single test finding."""

    def __init__(
        self,
        severity: str,  # "Critical", "High", "Medium", "Low"
        category: str,  # "Functional", "UX", "Performance", "Governance", "Polish"
        title: str,
        description: str,
        screenshot_path: Path | None = None,
        reproduction_steps: list[str] | None = None,
        recommendation: str = "",
        governance_impact: str = "",
    ):
        self.severity = severity
        self.category = category
        self.title = title
        self.description = description
        self.screenshot_path = screenshot_path
        self.reproduction_steps = reproduction_steps or []
        self.recommendation = recommendation
        self.governance_impact = governance_impact


class StressTestReport:
    """Aggregates test results and generates HTML reports."""

    def __init__(self):
        self.issues: list[Issue] = []
        self.metrics: dict[str, Any] = {}
        self.test_summary: dict[str, int] = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
        }

    def add_issue(self, issue: Issue):
        """Add a finding to the report."""
        self.issues.append(issue)

    def add_metric(self, name: str, value: Any):
        """Record a performance or quality metric."""
        self.metrics[name] = value

    def update_test_summary(self, passed: int, failed: int, skipped: int):
        """Update overall test counts."""
        self.test_summary["passed"] = passed
        self.test_summary["failed"] = failed
        self.test_summary["skipped"] = skipped
        self.test_summary["total"] = passed + failed + skipped

    def _calculate_health_score(self) -> int:
        """Calculate overall health score (0-100)."""
        if not self.issues:
            return 100

        # Deduct points based on severity
        severity_weights = {"Critical": 25, "High": 10, "Medium": 3, "Low": 1}
        total_deduction = sum(severity_weights.get(issue.severity, 0) for issue in self.issues)

        # Cap at 0
        score = max(0, 100 - total_deduction)
        return score

    def _group_issues_by_severity(self) -> dict[str, list[Issue]]:
        """Group issues by severity level."""
        grouped = {"Critical": [], "High": [], "Medium": [], "Low": []}
        for issue in self.issues:
            if issue.severity in grouped:
                grouped[issue.severity].append(issue)
        return grouped

    def _embed_screenshot(self, screenshot_path: Path) -> str:
        """Convert screenshot to base64 data URI."""
        if not screenshot_path or not screenshot_path.exists():
            return ""

        with open(screenshot_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{img_data}"

    def generate_html(self, output_path: Path):
        """Generate comprehensive HTML report."""
        health_score = self._calculate_health_score()
        grouped_issues = self._group_issues_by_severity()

        # Count issues by severity
        severity_counts = {
            severity: len(issues) for severity, issues in grouped_issues.items()
        }

        # HTML template
        template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAI Toolkit Stress Test Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.1em; opacity: 0.9; }
        .timestamp { font-size: 0.9em; margin-top: 10px; opacity: 0.8; }
        
        .executive-summary {
            background: #f8f9fa;
            padding: 30px 40px;
            border-bottom: 3px solid #e9ecef;
        }
        .health-score {
            text-align: center;
            margin: 20px 0;
        }
        .score-circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            margin: 0 auto 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3em;
            font-weight: bold;
            color: white;
        }
        .score-excellent { background: #28a745; }
        .score-good { background: #ffc107; }
        .score-fair { background: #fd7e14; }
        .score-poor { background: #dc3545; }
        
        .summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            text-align: center;
        }
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .stat-label {
            color: #6c757d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .critical { color: #dc3545; }
        .high { color: #fd7e14; }
        .medium { color: #ffc107; }
        .low { color: #17a2b8; }
        
        .content {
            padding: 40px;
        }
        .section {
            margin-bottom: 40px;
        }
        .section h2 {
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e9ecef;
        }
        
        .issue {
            background: #fff;
            border: 1px solid #dee2e6;
            border-left: 4px solid;
            border-radius: 4px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .issue.critical { border-left-color: #dc3545; }
        .issue.high { border-left-color: #fd7e14; }
        .issue.medium { border-left-color: #ffc107; }
        .issue.low { border-left-color: #17a2b8; }
        
        .issue-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
        }
        .issue-title {
            font-size: 1.3em;
            font-weight: 600;
        }
        .severity-badge {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
            color: white;
        }
        .severity-badge.critical { background: #dc3545; }
        .severity-badge.high { background: #fd7e14; }
        .severity-badge.medium { background: #ffc107; color: #333; }
        .severity-badge.low { background: #17a2b8; }
        
        .issue-description {
            margin: 15px 0;
            line-height: 1.8;
        }
        .issue-screenshot {
            margin: 15px 0;
            text-align: center;
        }
        .issue-screenshot img {
            max-width: 100%;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .reproduction-steps {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin: 15px 0;
        }
        .reproduction-steps h4 {
            margin-bottom: 10px;
            color: #495057;
        }
        .reproduction-steps ol {
            margin-left: 20px;
        }
        .reproduction-steps li {
            margin: 5px 0;
        }
        .recommendation {
            background: #e7f3ff;
            border-left: 3px solid #0066cc;
            padding: 15px;
            margin-top: 15px;
            border-radius: 4px;
        }
        .recommendation strong {
            color: #0066cc;
        }
        .governance-impact {
            background: #fff3cd;
            border-left: 3px solid #ffc107;
            padding: 15px;
            margin-top: 10px;
            border-radius: 4px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        .metric-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            border-left: 3px solid #667eea;
        }
        .metric-name {
            font-weight: 600;
            color: #495057;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 1.5em;
            color: #667eea;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px 40px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
        }
        
        .no-issues {
            text-align: center;
            padding: 40px;
            color: #28a745;
            font-size: 1.2em;
        }
        .no-issues::before {
            content: "✓";
            display: block;
            font-size: 4em;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>RAI Toolkit Stress Test Report</h1>
            <p>Comprehensive evaluation for senior governance professionals</p>
            <div class="timestamp">Generated: {{ timestamp }}</div>
        </div>
        
        <div class="executive-summary">
            <h2 style="text-align: center; margin-bottom: 20px;">Executive Summary</h2>
            
            <div class="health-score">
                <div class="score-circle {% if health_score >= 90 %}score-excellent{% elif health_score >= 70 %}score-good{% elif health_score >= 50 %}score-fair{% else %}score-poor{% endif %}">
                    {{ health_score }}
                </div>
                <div style="font-size: 1.1em; color: #6c757d;">Overall Health Score</div>
            </div>
            
            <div class="summary-stats">
                <div class="stat-card">
                    <div class="stat-number">{{ test_summary.total }}</div>
                    <div class="stat-label">Total Tests</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" style="color: #28a745;">{{ test_summary.passed }}</div>
                    <div class="stat-label">Passed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" style="color: #dc3545;">{{ test_summary.failed }}</div>
                    <div class="stat-label">Failed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number critical">{{ severity_counts.Critical }}</div>
                    <div class="stat-label">Critical Issues</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number high">{{ severity_counts.High }}</div>
                    <div class="stat-label">High Priority</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number medium">{{ severity_counts.Medium }}</div>
                    <div class="stat-label">Medium Priority</div>
                </div>
            </div>
        </div>
        
        <div class="content">
            {% if not issues %}
            <div class="no-issues">
                All tests passed! No issues detected.
            </div>
            {% else %}
            
            {% for severity in ['Critical', 'High', 'Medium', 'Low'] %}
            {% if grouped_issues[severity] %}
            <div class="section">
                <h2><span class="{{ severity.lower() }}">{{ severity }} Issues</span> ({{ grouped_issues[severity]|length }})</h2>
                
                {% for issue in grouped_issues[severity] %}
                <div class="issue {{ severity.lower() }}">
                    <div class="issue-header">
                        <div class="issue-title">{{ issue.title }}</div>
                        <div class="severity-badge {{ severity.lower() }}">{{ severity }}</div>
                    </div>
                    
                    <div style="color: #6c757d; font-size: 0.9em; margin-bottom: 10px;">
                        Category: {{ issue.category }}
                    </div>
                    
                    <div class="issue-description">
                        {{ issue.description }}
                    </div>
                    
                    {% if issue.screenshot_path %}
                    <div class="issue-screenshot">
                        <img src="{{ embed_screenshot(issue.screenshot_path) }}" alt="Screenshot">
                    </div>
                    {% endif %}
                    
                    {% if issue.reproduction_steps %}
                    <div class="reproduction-steps">
                        <h4>Reproduction Steps:</h4>
                        <ol>
                        {% for step in issue.reproduction_steps %}
                            <li>{{ step }}</li>
                        {% endfor %}
                        </ol>
                    </div>
                    {% endif %}
                    
                    {% if issue.recommendation %}
                    <div class="recommendation">
                        <strong>Recommendation:</strong> {{ issue.recommendation }}
                    </div>
                    {% endif %}
                    
                    {% if issue.governance_impact %}
                    <div class="governance-impact">
                        <strong>Governance Impact:</strong> {{ issue.governance_impact }}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            {% endif %}
            {% endfor %}
            
            {% endif %}
            
            {% if metrics %}
            <div class="section">
                <h2>Performance Metrics</h2>
                <div class="metrics-grid">
                    {% for name, value in metrics.items() %}
                    <div class="metric-card">
                        <div class="metric-name">{{ name }}</div>
                        <div class="metric-value">{{ value }}</div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
        </div>
        
        <div class="footer">
            <p>This report evaluates the RAI Toolkit as a demonstration/portfolio project.</p>
            <p>Focus areas: Governance rigor, technical depth, professional polish, and transparency.</p>
        </div>
    </div>
</body>
</html>
        """

        template = Template(template_str)

        html = template.render(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            health_score=health_score,
            test_summary=self.test_summary,
            severity_counts=severity_counts,
            issues=self.issues,
            grouped_issues=grouped_issues,
            metrics=self.metrics,
            embed_screenshot=self._embed_screenshot,
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")

        print(f"\n📊 Report generated: {output_path}")
        print(f"   Health Score: {health_score}/100")
        print(f"   Critical Issues: {severity_counts['Critical']}")
        print(f"   High Issues: {severity_counts['High']}")
        print(f"   Medium Issues: {severity_counts['Medium']}")
        print(f"   Low Issues: {severity_counts['Low']}")

