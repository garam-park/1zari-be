# syntax=docker/dockerfile:1
FROM python:3.13-slim

# 시스템 패키지 설치 및 환경설정
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  build-essential \
  libpq-dev \
  gdal-bin \
  libgdal-dev \
  libgeos-dev \
  && rm -rf /var/lib/apt/lists/*

# GDAL 심볼릭 링크가 없으면 생성 (여러 위치 대응)
RUN set -eux; \
  GDAL_SO=$(find /usr/lib /usr/lib/x86_64-linux-gnu /usr/lib/aarch64-linux-gnu -name "libgdal.so*" | head -n 1); \
    if [ -n "$GDAL_SO" ]; then \
      ln -sf "$GDAL_SO" /usr/lib/libgdal.so; \
    fi
# GEOS 심볼릭 링크가 없으면 생성 (여러 위치 대응)
RUN set -eux; \
  GEOS_SO=$(find /usr/lib /usr/lib/x86_64-linux-gnu /usr/lib/aarch64-linux-gnu -name "libgeos_c.so*" | head -n 1); \
  if [ -n "$GEOS_SO" ]; then \
  ln -sf "$GEOS_SO" /usr/lib/libgeos_c.so; \
  fi

# poetry 설치
RUN pip install --upgrade pip 
RUN pip install poetry 

# 작업 디렉토리 설정
WORKDIR /app

# poetry 설정 파일 복사 및 의존성 설치
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN touch /app/README.md
RUN poetry install --no-interaction --no-ansi --only main --no-root

# 소스 복사
COPY . .

# 포트 오픈
EXPOSE 8000

# 기본 명령어는 docker-compose에서 지정
