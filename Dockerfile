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

# poetry 설치
RUN pip install --upgrade pip 
RUN pip install poetry 

# 작업 디렉토리 설정
WORKDIR /app

# poetry 설정 파일 복사 및 의존성 설치
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN touch /app/README.md
RUN poetry install --no-interaction --no-ansi --only main

# 소스 복사
COPY . .

# 포트 오픈
EXPOSE 8000

# 기본 명령어는 docker-compose에서 지정
