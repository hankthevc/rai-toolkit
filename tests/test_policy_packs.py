"""Validate policy pack structure and required fields."""

from pathlib import Path

import pytest

from common.utils.policy_loader import load_policy_packs


@pytest.fixture(scope="module")
def packs():
    return load_policy_packs(Path("common/policy_packs"))


def test_policy_pack_count(packs):
    assert len(packs) >= 5, "Expected at least five illustrative policy packs"


def test_control_structure(packs):
    for pack in packs:
        assert pack.controls, f"{pack.name} should include controls"
        for control in pack.controls:
            assert control.id
            assert control.title
            assert control.description
            assert control.authority
            assert control.clause
            assert control.evidence
            assert control.tags
            assert control.when is not None
