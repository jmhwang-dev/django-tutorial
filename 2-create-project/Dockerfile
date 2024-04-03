# 파이썬 이미지 불러오기
FROM python:3.12.1-slim-bullseye

# 프로젝트 작업 폴더
WORKDIR /usr/src/app

# 소스 코드를 컴파일해서 확장자가 .pyc인 파일을 생성하는데 이를 생성하지 않도록 설정
ENV PYTHONDONTWRITERBYTECODE 1

# 파이썬 로그가 버퍼링 없이 즉각적으로 출력
ENV PYTHONUNBUFFERED 1

# Dockerfile이 있는 위치(.)에 파일을 모두 작업 폴더(/usr/src/app)로 복사
COPY . /usr/src/app/

# install dependencies
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt