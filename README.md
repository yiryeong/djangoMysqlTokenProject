# django_login_project

개발언어 :  Python Django
데이터베이스 : Mysql 5.7


notion : https://www.notion.so/73c7b8fc71f441c4bb2287fa0f0dfef9


## 기능 :
1. 회원가입 ( 이메일과 비밀번호)
2. 로그인/로그아웃 
3. 로그인 이후 
    1. 내역 추가 
    2. 수정기능
    3. 삭제기능 
    4. 삭제 후 복원 (x)
    5. 조회
4. 로그인하지 않은 고객은 접근 제한처리


## API :
회원가입 :  /api/register
로그인 : /api/login/
로그아웃 : /api/logout/
로그인 후 기능 :
   가계부 리스트 조회 : /api/history/getlist/
   내역 추가 : /api/history/insert/
   내역 수정 : /api/history/update/<id>
   내역 삭제 : /api/history/delete/<id>


## 개발환경 설치 : 
- python3.9
- `python3 -m pip install Django`
- `pip3 install djangorestframework`
- `pip3 install markdown`
- `pip3 install django-filter`
- `pip3 install mysqlclient`
- `pip3 install djangorestframework-simplejwt`

API 문서 자동화 환경 설치: 
- `pip3 install drf-yasg`
