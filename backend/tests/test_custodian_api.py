import os

import pytest
import requests


BASE_URL = os.environ.get("REACT_APP_BACKEND_URL")
if not BASE_URL:
    pytest.skip("REACT_APP_BACKEND_URL is required", allow_module_level=True)
BASE_URL = BASE_URL.rstrip("/")


class TestCustodianApi:
    """Critical seeded discovery, detail, booking, and legacy API flows."""

    def test_experiences_returns_six_seeded_records(self):
        response = requests.get(f"{BASE_URL}/api/experiences", timeout=15)
        assert response.status_code == 200
        records = response.json()
        assert len(records) == 6
        assert {record["id"] for record in records} == {
            "yakshagana", "coffee", "ritual", "fishing", "coir", "kambala"
        }

    @pytest.mark.parametrize("category, expected", [("Food", 1), ("Craft", 1), ("Nature / Fishing", 2)])
    def test_category_filter(self, category, expected):
        response = requests.get(f"{BASE_URL}/api/experiences", params={"category": category}, timeout=15)
        assert response.status_code == 200
        assert len(response.json()) == expected
        assert all(record["category"] == category for record in response.json())

    def test_detail_and_missing_detail(self):
        response = requests.get(f"{BASE_URL}/api/experiences/coffee", timeout=15)
        assert response.status_code == 200
        assert response.json()["custodian"] == "Anitha Pai"
        missing = requests.get(f"{BASE_URL}/api/experiences/not-real", timeout=15)
        assert missing.status_code == 404

    def test_booking_returns_pending_confirmation(self):
        response = requests.post(
            f"{BASE_URL}/api/bookings",
            json={"experience_id": "coffee", "date": "2026-02-14", "guests": 2},
            timeout=15,
        )
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "pending_confirmation"
        assert body["guests"] == 2
        assert body["experience"] == "A proper Udupi meal on a banana leaf"

    def test_legacy_rejects_blank_and_accepts_question(self):
        blank = requests.post(f"{BASE_URL}/api/legacy", json={"experience_id": "coffee", "text": "  "}, timeout=15)
        assert blank.status_code == 400
        response = requests.post(
            f"{BASE_URL}/api/legacy",
            json={"experience_id": "coffee", "text": "What should I notice first?"},
            timeout=15,
        )
        assert response.status_code == 200
        assert response.json()["status"] == "visible_to_future_visitors"