from licitpy.entities.tender import Tender
from licitpy.entities.tenders import Tenders


def test_tenders_creation_and_codes():
    """
    Test that Tenders is created correctly and the codes are retrieved in order.
    """
    # Create a Tenders collection with multiple Tender instances
    tenders = Tenders(
        [
            Tender.create("T002"),
            Tender.create("T001"),
        ]
    )

    # Assert the count of tenders
    assert tenders.count() == 2, "Expected the tenders collection to contain 2 items"

    # Assert the codes are retrieved in the correct order
    assert tenders.codes == [
        "T002",
        "T001",
    ], "Expected the codes to match ['T002', 'T001']"
