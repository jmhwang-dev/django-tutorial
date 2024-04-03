FROM nginx:latest
# 도커가 제공하는 기본 Nginx의 기본 설정 값을 삭제
RUN rm /etc/nginx/conf.d/default.conf
# 로컬에 새로 만든 Nginx 설정 정보를 Nginx 이미지에 복사
COPY nginx.conf /etc/nginx/conf.d