from src.capabilities.tools import lookup_product_deadline


def test_lookup_product_found():
    result = lookup_product_deadline("LAPTOP-1000", "manufacturing")
    assert result.found is True
    assert result.deadline == "2026-12-15T17:00:00+02:00"


def test_lookup_product_loose_name():
    result = lookup_product_deadline("laptop model 1000", "manufacturing")
    assert result.found is True
    assert result.product_id == "LAPTOP-1000"


def test_lookup_product_not_found():
    result = lookup_product_deadline("PHONE-5", "manufacturing")
    assert result.found is False
    assert result.deadline is None


def test_lookup_product_rejects_invalid_stage():
    with pytest.raises(Exception):
        lookup_product_deadline("LAPTOP-1000", "marketing")