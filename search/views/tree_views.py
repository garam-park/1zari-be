from typing import Dict, List

import redis
from django.http import JsonResponse
from django.views import View

from search.schemas import RegionTreeResponse


class RegionTreeView(View):
    def get(self, request):
        r = redis.StrictRedis(
            host="localhost", port=6379, db=0, decode_responses=True
        )

        region_keys = r.keys("region:*")

        region_tree = self.build_region_tree(region_keys)

        response_model = RegionTreeResponse(__root__=region_tree)
        return JsonResponse(
            response_model.model_dump(),
            status=200,
            json_dumps_params={"ensure_ascii": False},
        )

    def build_region_tree(self, region_keys) -> Dict[str, Dict[str, List[str]]]:
        """
        Redis 키 리스트에서 계층 구조 생성
        """
        region_tree: dict = {}

        for key in region_keys:
            parts = key.split(":")
            if len(parts) < 4:
                continue

            city, district, town = parts[1], parts[2], parts[3]

            city_node = region_tree.setdefault(city, {})
            district_node = city_node.setdefault(district, set())
            district_node.add(town)

        return {
            city: {
                district: sorted(towns) for district, towns in districts.items()
            }
            for city, districts in region_tree.items()
        }
