import pytest

from app.scoring import score

ALL = {"step_free_access": True, "tactile_signage": True, "visual_alerts": True,
       "hospital_within_10km": True, "allergen_labeling": True}


def test_fully_accessible_is_zero_risk():
    assert score({"wheelchair": 3, "medical": 3}, ALL) == {"risk": 0, "level": "low", "gaps": []}


def test_missing_feature_scales_with_severity():
    f = {**ALL, "step_free_access": False}
    assert score({"wheelchair": 1}, f)["risk"] == 12
    assert score({"wheelchair": 3}, f)["risk"] == 36


def test_risk_caps_at_100_and_is_high():
    r = score({"wheelchair": 3, "medical": 3, "low_vision": 3, "hearing": 3, "dietary": 3}, {})
    assert r["risk"] == 100 and r["level"] == "high"


@pytest.mark.parametrize("needs", [{"flying": 1}, {"wheelchair": 0}, {"wheelchair": 4}])
def test_invalid_input_rejected(needs):
    with pytest.raises(ValueError):
        score(needs, ALL)
