"""Tests for policy pack schema validation."""

import tempfile
from pathlib import Path
import yaml

from common.utils.policy_loader import validate_policy_packs, get_policy_validation_status


def test_valid_policy_pack_passes_validation():
    """Verify that a correctly formatted policy pack passes validation."""
    
    valid_pack = {
        "name": "Test Pack",
        "version": "1.0.0",
        "description": "Test policy pack for validation",
        "controls": [
            {
                "id": "TEST-001",
                "title": "Test Control",
                "description": "A test control",
                "authority": "Test Authority",
                "clause": "Test Clause",
                "evidence": "Test evidence",
                "tags": ["test"],
                "when": {
                    "tier": ["High", "Critical"]
                }
            }
        ]
    }
    
    # Create temp directory with valid YAML
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Write valid YAML
        yaml_path = tmpdir_path / "valid_pack.yaml"
        with open(yaml_path, 'w') as f:
            yaml.dump(valid_pack, f)
        
        # Get schema path
        repo_root = Path(__file__).resolve().parent.parent
        schema_path = repo_root / "common" / "schema" / "policy_pack.schema.json"
        
        # Validate
        result = validate_policy_packs(tmpdir_path, schema_path)
        
        assert result["total"] == 1, "Should find 1 policy pack"
        assert result["ok"] == 1, "Valid pack should pass validation"
        assert len(result["errors"]) == 0, "Should have no errors"


def test_invalid_policy_pack_fails_validation():
    """Verify that a malformed policy pack fails validation."""
    
    # Missing required "evidence" field
    invalid_pack = {
        "name": "Invalid Pack",
        "version": "1.0.0",
        "description": "Test policy pack with missing fields",
        "controls": [
            {
                "id": "TEST-002",
                "title": "Invalid Control",
                "description": "Missing required fields",
                "authority": "Test Authority",
                "clause": "Test Clause",
                # Missing "evidence" - required field
                "tags": ["test"],
                "when": {
                    "tier": ["Medium"]
                }
            }
        ]
    }
    
    # Create temp directory with invalid YAML
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Write invalid YAML
        yaml_path = tmpdir_path / "invalid_pack.yaml"
        with open(yaml_path, 'w') as f:
            yaml.dump(invalid_pack, f)
        
        # Get schema path
        repo_root = Path(__file__).resolve().parent.parent
        schema_path = repo_root / "common" / "schema" / "policy_pack.schema.json"
        
        # Validate
        result = validate_policy_packs(tmpdir_path, schema_path)
        
        assert result["total"] == 1, "Should find 1 policy pack"
        assert result["ok"] == 0, "Invalid pack should fail validation"
        assert len(result["errors"]) > 0, "Should have validation errors"
        
        # Check error details
        assert any("evidence" in err["message"].lower() for err in result["errors"]), \
            "Error should mention missing 'evidence' field"


def test_get_policy_validation_status_returns_dict():
    """Verify get_policy_validation_status returns expected structure."""
    
    status = get_policy_validation_status()
    
    # Verify structure
    assert isinstance(status, dict), "Should return a dict"
    assert "total" in status, "Should have 'total' key"
    assert "ok" in status, "Should have 'ok' key"
    assert "errors" in status, "Should have 'errors' key"
    
    # Verify types
    assert isinstance(status["total"], int), "'total' should be an int"
    assert isinstance(status["ok"], int), "'ok' should be an int"
    assert isinstance(status["errors"], list), "'errors' should be a list"
    
    # Verify all actual policy packs are validated
    assert status["total"] > 0, "Should find policy packs in repo"


def test_malformed_yaml_is_caught():
    """Verify that malformed YAML files are caught during validation."""
    
    # Create temp directory with malformed YAML
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Write malformed YAML (not even valid YAML syntax)
        yaml_path = tmpdir_path / "malformed.yaml"
        with open(yaml_path, 'w') as f:
            f.write("this is: [not: valid: yaml:")
        
        # Get schema path
        repo_root = Path(__file__).resolve().parent.parent
        schema_path = repo_root / "common" / "schema" / "policy_pack.schema.json"
        
        # Validate
        result = validate_policy_packs(tmpdir_path, schema_path)
        
        assert result["total"] == 1, "Should attempt to validate 1 file"
        assert result["ok"] == 0, "Malformed YAML should fail"
        assert len(result["errors"]) > 0, "Should report errors"
        assert any("malformed.yaml" in err["file"] for err in result["errors"]), \
            "Error should reference the malformed file"

