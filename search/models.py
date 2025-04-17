from django.contrib.gis.db import models


class District(models.Model):
    city_no = models.CharField(verbose_name="시 고유번호", max_length=10)
    city_name = models.CharField(verbose_name="시 이름", max_length=20)
    district_no = models.CharField(
        verbose_name="구 고유번호", max_length=10, unique=True
    )
    district_name = models.CharField(verbose_name="구 이름", max_length=20)
    geometry = models.MultiPolygonField(verbose_name="구 경계", srid=5179)

    def __str__(self):
        return f"{self.city_name} {self.district_name}"
