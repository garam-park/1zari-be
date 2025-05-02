import os
import platform

from .base import *

ROOT_URLCONF = "config.urls.dev_urls"

# 로컬과 CI 환경 구분
if os.environ.get("CI") == "true":
    # CI 환경에서 사용하는 경로 (Ubuntu)
    GDAL_LIBRARY_PATH = "/usr/lib/x86_64-linux-gnu/libgdal.so"
    GEOS_LIBRARY_PATH = "/usr/lib/x86_64-linux-gnu/libgeos_c.so"
elif platform.system() == "Linux":
    # Docker, 리눅스 환경 경로
    GDAL_LIBRARY_PATH = "/usr/lib/x86_64-linux-gnu/libgdal.so"
    GEOS_LIBRARY_PATH = "/usr/lib/x86_64-linux-gnu/libgeos_c.so"
else:
    # 로컬 환경에서 사용하는 경로 (macOS)
    GDAL_LIBRARY_PATH = "/opt/homebrew/lib/libgdal.dylib"
    GEOS_LIBRARY_PATH = "/opt/homebrew/lib/libgeos_c.dylib"
