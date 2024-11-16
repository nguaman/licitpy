from licitpy.entities.tender import Tender
from licitpy.utils.threads import execute_concurrently


def test_execute_concurrently_success():
    """
    Test that execute_concurrently correctly processes all items without exceptions.
    """

    def mock_function(tender: Tender):
        return tender

    # Create mock items
    items = [Tender(code=f"T{i:04}") for i in range(16)]

    # Execute concurrently
    results = execute_concurrently(
        function=mock_function, items=items, desc="Test Success"
    )

    # Validate results
    assert len(results) == len(
        items
    ), "Expected results to match the number of input items"
    assert set(results) == set(items), "Expected all items to be processed successfully"


def test_execute_concurrently_with_exceptions():
    """
    Test that execute_concurrently handles exceptions correctly and excludes failed items.
    """

    def mock_function(tender: Tender):
        # Raise an exception for a specific item
        if tender.code == "T0005":
            raise ValueError("Mock exception")
        return tender

    # Create mock items
    items = [Tender(code=f"T{i:04}") for i in range(16)]

    # Execute concurrently
    results = execute_concurrently(
        function=mock_function, items=items, desc="Test Exceptions"
    )

    # Validate results
    assert len(results) == len(items) - 1, "Expected results to exclude the failed item"
    assert all(
        tender.code != "T0005" for tender in results
    ), "Expected failed item to be excluded from results"
