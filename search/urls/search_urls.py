from django.urls.conf import path

from search.views.search_views import SearchView
from search.views.tree_views import RegionTreeView

app_name = "resume"


urlpatterns = [
    path("region/", RegionTreeView.as_view(), name="region_tree"),
    path("", SearchView.as_view(), name="resume_detail"),
]
