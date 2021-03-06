# djangoMysqlTokenProject

- 개발언어 :  Python Django
- 데이터베이스 : Mysql 5.7


## notion : 
https://yiryeong.notion.site/Django-DRF-Mysql-token-25eed24a79694781bfa47aafd672b11b


## 기능 :
1. 회원가입 (이메일과 비밀번호)
2. 로그인/로그아웃 
3. 로그인 이후 
    1. 내역 추가 
    2. 수정기능
    3. 삭제기능 
    4. 조회
4. 로그인하지 않은 고객은 접근 제한처리


## API :
1. 회원가입 : POST  /api/register/
2. 로그인 : POST /api/login/
3. 로그아웃 : POST  /api/logout/
4. 로그인 후 기능 :
    1. 가계부 리스트 조회 : GET  /api/histories/
    2. 내역 추가 : POST  /api/histories/
    3. 내역 수정 : PUT   /api/histories/id(레코드 아이디)
    4. 내역 삭제 : DELETE   /api/histories/id(레코드 아이디)
    
    

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
    
    
    
## 참고 : 
- https://django-rest-auth.readthedocs.io/en/latest/installation.html
- https://freekim.tistory.com/8](https://freekim.tistory.com/8
- https://django-rest-auth.readthedocs.io/en/latest/installation.html
