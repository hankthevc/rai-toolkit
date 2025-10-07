"""Generate sample assessment data for analytics dashboard demonstration."""

import argparse
import json
import random
from datetime import date, timedelta
from pathlib import Path

# Sample scenarios for realistic data
SAMPLE_SCENARIOS = [
    {
        "description": "Customer support chatbot",
        "contains_pii": True,
        "customer_facing": True,
        "high_stakes": False,
        "autonomy_level": 1,
        "sector": "General",
        "modifiers": [],
    },
    {
        "description": "Healthcare diagnosis assistant",
        "contains_pii": True,
        "customer_facing": True,
        "high_stakes": True,
        "autonomy_level": 2,
        "sector": "Healthcare",
        "modifiers": ["Cyber"],
    },
    {
        "description": "Financial fraud detection",
        "contains_pii": True,
        "customer_facing": False,
        "high_stakes": True,
        "autonomy_level": 3,
        "sector": "Finance",
        "modifiers": ["Cyber"],
    },
    {
        "description": "Internal code review assistant",
        "contains_pii": False,
        "customer_facing": False,
        "high_stakes": False,
        "autonomy_level": 0,
        "sector": "General",
        "modifiers": [],
    },
    {
        "description": "Content moderation system",
        "contains_pii": False,
        "customer_facing": True,
        "high_stakes": False,
        "autonomy_level": 2,
        "sector": "General",
        "modifiers": ["Disinformation"],
    },
    {
        "description": "Hiring assessment platform",
        "contains_pii": True,
        "customer_facing": True,
        "high_stakes": True,
        "autonomy_level": 2,
        "sector": "General",
        "modifiers": [],
    },
    {
        "description": "Educational tutoring chatbot",
        "contains_pii": True,
        "customer_facing": True,
        "high_stakes": False,
        "autonomy_level": 1,
        "sector": "General",
        "modifiers": ["Children"],
    },
    {
        "description": "Infrastructure monitoring AI",
        "contains_pii": False,
        "customer_facing": False,
        "high_stakes": True,
        "autonomy_level": 2,
        "sector": "Critical Infrastructure",
        "modifiers": ["Cyber"],
    },
]

OWNERS = [
    "Sarah Chen",
    "Marcus Rodriguez",
    "Aisha Patel",
    "David Kim",
    "Maria Santos",
    "James Wilson",
]

APPROVERS = [
    "Lisa Park (CEO)",
    "Robert Johnson (CTO)",
    "Emily Zhang (Chief Risk Officer)",
    "Michael Brown (VP Engineering)",
]


def calculate_score(scenario):
    """Replicate the risk scoring logic."""
    score = 0
    if scenario["contains_pii"]:
        score += 2
    if scenario["customer_facing"]:
        score += 2
    if scenario["high_stakes"]:
        score += 3
    score += scenario["autonomy_level"]

    sector_bumps = {
        "Healthcare": 1,
        "Finance": 1,
        "Critical Infrastructure": 1,
        "Children": 1,
    }
    score += sector_bumps.get(scenario["sector"], 0)

    modifier_weights = {"Bio": 2, "Cyber": 2, "Disinformation": 1, "Children": 1}
    for modifier in scenario.get("modifiers", []):
        score += modifier_weights.get(modifier, 0)

    return score


def determine_tier(score):
    """Convert score to tier."""
    if score <= 2:
        return "Low"
    if score <= 5:
        return "Medium"
    if score <= 8:
        return "High"
    return "Critical"


def generate_assessments(count: int):
    """Generate sample assessment records."""
    assessments = []
    start_date = date.today() - timedelta(days=180)

    for i in range(count):
        # Pick random scenario template
        scenario = random.choice(SAMPLE_SCENARIOS).copy()

        # Add some variation
        if random.random() < 0.3:
            scenario["contains_pii"] = not scenario["contains_pii"]
        if random.random() < 0.2:
            scenario["customer_facing"] = not scenario["customer_facing"]

        score = calculate_score(scenario)
        tier = determine_tier(score)

        # Random date within last 180 days
        days_ago = random.randint(0, 180)
        assessment_date = start_date + timedelta(days=days_ago)

        assessment = {
            "id": f"ASSESS-{i+1:04d}",
            "date": assessment_date.isoformat(),
            "scenario": scenario["description"],
            "owner": random.choice(OWNERS),
            "approver": random.choice(APPROVERS),
            "score": score,
            "tier": tier,
            "contains_pii": scenario["contains_pii"],
            "customer_facing": scenario["customer_facing"],
            "high_stakes": scenario["high_stakes"],
            "autonomy_level": scenario["autonomy_level"],
            "sector": scenario["sector"],
            "modifiers": scenario.get("modifiers", []),
        }

        assessments.append(assessment)

    return assessments


def main():
    parser = argparse.ArgumentParser(
        description="Generate sample assessment data for analytics"
    )
    parser.add_argument(
        "--count", type=int, default=100, help="Number of assessments to generate"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/sample_assessments.json"),
        help="Output file path",
    )

    args = parser.parse_args()

    # Create output directory if needed
    args.output.parent.mkdir(parents=True, exist_ok=True)

    assessments = generate_assessments(args.count)

    with args.output.open("w") as f:
        json.dump(assessments, f, indent=2)

    print(f"✓ Generated {args.count} sample assessments")
    print(f"✓ Saved to {args.output}")

    # Print summary stats
    tiers = [a["tier"] for a in assessments]
    print(f"\nTier distribution:")
    for tier in ["Low", "Medium", "High", "Critical"]:
        count = tiers.count(tier)
        pct = count / len(tiers) * 100
        print(f"  {tier}: {count} ({pct:.1f}%)")


if __name__ == "__main__":
    main()

