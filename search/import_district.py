from django.contrib.gis.utils import LayerMapping

from config.settings.base import BASE_DIR
from search.models import District

district_mapping = {
    "district_no": "DISTRICT_N",
    "district_name": "DISTRICT_1",
    "city_no": "CITY_NO",
    "city_name": "CITY_NAME",
    "geometry": "POLYGON",  # 또는 'geometry'
}

shp_file = str(BASE_DIR / "search/data/new_new_city_district.shp")


def run(verbose=True):
    District.objects.all().delete()
    lm = LayerMapping(
        District,
        shp_file,
        district_mapping,
        transform=True,
        source_srs="ESRI:102080",
        encoding="utf-8",
        # geom_field 파라미터는 빼세요!
    )
    lm.save(strict=True, verbose=verbose)
