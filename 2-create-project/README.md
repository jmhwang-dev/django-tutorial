# 명령어

## 기본

```bash
django-admin startproject do_it_django_prj .
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
```

## 앱 생성

```bash
python manage.py startapp blog
python manage.py startapp single_pages
```

## 모델 생성 후 데이터베이스에 반영하기 (프로젝트 폴더에 앱이 먼저 등록되어있어야함)

```bash
python manage.py makeimgrations
```

### settings.py에 앱 등록하기

{project_name}/setting.py을 아래와 같이 추가

```python
INSTALLED_APPS = [
    ...,

    'blog',
    'single_pages'
]
```

### 이후, DB에 반영하기

```bash
# app 변경사항 등록
python manage.py makemigrations

# DB에 모델 적용
python manage.py migrate
```

### migration 폴더가 있어야 반영됨
