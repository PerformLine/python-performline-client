from performline.client import Client
from performline.products.common.models import RemediationStatus


class TestRemediationStatus:

    def test_instantiation(self):
        expected_statuses = [
            "Not reviewed",
            "Opened",
            "In progress",
            "Escalated",
            "Closed no action required",
            "Closed resolved",
        ]
        api_key = "976794ca6e5897e27d1b439064691bb1c3eb0420"
        rs = RemediationStatus(api_key)
        statuses = rs.remediation_statuses
        assert expected_statuses == statuses
