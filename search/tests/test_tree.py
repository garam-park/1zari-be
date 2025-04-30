from unittest.mock import MagicMock, patch

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_region_tree_view_with_client():
    mock_keys = [
        "region:서울특별시:강남구:역삼동",
        "region:서울특별시:강남구:도곡동",
        "region:인천광역시:부평구:부평동",
        "region:인천광역시:부평구:부개동",
        "invalid_key",
    ]

    with patch("redis.StrictRedis") as mock_redis_cls:
        mock_redis = MagicMock()
        mock_redis.keys.return_value = mock_keys
        mock_redis_cls.return_value = mock_redis

        client = Client()
        url = "/api/search/region/"
        response = client.get(url)

    assert response.status_code == 200
    assert response["Content-Type"] == "application/json"

    data = response.json()
    assert data == {
        "서울특별시": {"강남구": ["도곡동", "역삼동"]},
        "인천광역시": {"부평구": ["부개동", "부평동"]},
    }
    assert "invalid_key" not in str(data)
