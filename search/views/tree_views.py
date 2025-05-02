import json
from typing import Dict, List, cast

import redis
from django.http import JsonResponse
from django.views import View

from config.settings.base import REDIS_DB, REDIS_HOST, REDIS_PORT
from search.schemas import RegionTreeResponse


class RegionTreeView(View):
    def get(self, request) -> JsonResponse:
        r = redis.Redis(
            host=cast(str, REDIS_HOST),
            port=cast(int, REDIS_PORT),
            db=cast(int, REDIS_DB),
            decode_responses=True,
        )

        region_tree_json = r.get("region_tree")

        region_tree = json.loads(region_tree_json) if region_tree_json else {}

        response_model = RegionTreeResponse.model_validate(region_tree)
        return JsonResponse(
            response_model.model_dump(),
            status=200,
            json_dumps_params={"ensure_ascii": False},
        )
