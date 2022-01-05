# ubuntu:18.04의 이미지로 부터
FROM ubuntu:18.04


RUN apt-get update -y
RUN apt-get install git -y


# github 에 소스코드 받기
RUN git clone https://github.com/yiryeong/djangoMysqlTokenProject.git
WORKDIR /djangoMysqlTokenProject


# 필요한 환경 설치
RUN apt-get update -y
RUN apt-get install -y python3-dev python3-pip libmysqlclient-dev gcc
RUN pip3 install -r requirements.txt
RUN pip3 install mysqlclient


EXPOSE 7002
# container가 구동되면 실행
ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:7002"]
