"""Utilities for loading and matching governance-as-code policy packs."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Sequence

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator


class WhenClause(BaseModel):
    """Conditional metadata describing when to recommend a control."""

    tier: Sequence[str] | None = None
    contains_pii: bool | None = None
    customer_facing: bool | None = None
    high_stakes: bool | None = None
    autonomy_at_least: int | None = Field(default=None, ge=0)
    sector: Sequence[str] | None = None
    modifiers: Sequence[str] | None = None

    model_config = ConfigDict(extra="forbid")


class PolicyControl(BaseModel):
    """Structure for a single governance control."""

    id: str
    title: str
    description: str
    authority: str
    clause: str
    evidence: str
    tags: List[str]
    mappings: Dict[str, List[str]] | None = None
    when: WhenClause

    @field_validator("tags", mode="before")
    @classmethod
    def _ensure_tags(cls, value: Iterable[str]) -> List[str]:
        if value is None:
            return []
        return list(value)


class PolicyPack(BaseModel):
    """A validated policy pack sourced from YAML."""

    name: str
    version: str
    description: str
    controls: List[PolicyControl]

    model_config = ConfigDict(extra="forbid")


class ScenarioContext(BaseModel):
    """Scenario attributes used to evaluate policy controls."""

    # Core risk assessment
    tier: str
    contains_pii: bool = False
    customer_facing: bool = False
    high_stakes: bool = False
    autonomy_level: int = Field(default=0, ge=0)
    sector: str = "General"
    modifiers: List[str] = Field(default_factory=list)
    
    # Extended risk factors (for policy matching)
    model_type: str = "Traditional ML"
    data_source: str = "Proprietary/Internal"
    learns_in_production: bool = False
    international_data: bool = False
    explainability_level: str = "Post-hoc Explainable"
    uses_foundation_model: str = "No Third-Party"
    generates_synthetic_content: bool = False
    dual_use_risk: str = "None"
    decision_reversible: str = "Fully Reversible"
    protected_populations: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid", protected_namespaces=())


def load_policy_pack(path: Path) -> PolicyPack:
    """Read a single YAML policy pack and return a validated model."""

    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return PolicyPack(**data)


def load_policy_packs(directory: Path) -> List[PolicyPack]:
    """Load and validate all policy packs in a directory."""

    packs: List[PolicyPack] = []
    for path in sorted(directory.glob("*.yaml")):
        packs.append(load_policy_pack(path))
    if not packs:
        raise FileNotFoundError(f"No policy packs discovered in {directory}")
    return packs


def control_matches(control: PolicyControl, scenario: ScenarioContext) -> bool:
    """Return True when a control's conditions align with the scenario."""

    conditions = control.when

    if conditions.tier and scenario.tier not in conditions.tier:
        return False

    if conditions.contains_pii is not None and scenario.contains_pii != conditions.contains_pii:
        return False

    if conditions.customer_facing is not None and scenario.customer_facing != conditions.customer_facing:
        return False

    if conditions.high_stakes is not None and scenario.high_stakes != conditions.high_stakes:
        return False

    if conditions.autonomy_at_least is not None and scenario.autonomy_level < conditions.autonomy_at_least:
        return False

    if conditions.sector and scenario.sector not in conditions.sector:
        return False

    if conditions.modifiers:
        scenario_modifiers = set(scenario.modifiers)
        if not scenario_modifiers.intersection(set(conditions.modifiers)):
            return False

    return True


def select_applicable_controls(
    packs: Sequence[PolicyPack], scenario: ScenarioContext
) -> List[PolicyControl]:
    """Filter controls across packs for a given scenario."""

    matched: List[PolicyControl] = []
    for pack in packs:
        for control in pack.controls:
            if control_matches(control, scenario):
                matched.append(control)
    return matched
