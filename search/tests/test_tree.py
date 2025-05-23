import json

import pytest
import redis
from django.test import Client

from search.redis_script import REDIS_CONFIG


@pytest.mark.django_db
def test_region_tree_view_with_real_redis():
    """
    mock 데이터 없이 실제 redis에
    """
    r = redis.Redis(**REDIS_CONFIG)

    client = Client()
    url = "/api/search/region/"
    response = client.get(url)

    assert response.status_code == 200
    assert response["Content-Type"] == "application/json"

    data = json.loads(response.content)

    assert data == json.loads(r.get("region_tree"))
