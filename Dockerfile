# ubuntu:18.04의 이미지로 부터
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
RUN  apt-get update -y
RUN  apt-get install git -y
RUN apt-get update && apt-get install -y alien
RUN  apt-get install software-properties-common -y --fix-missing
RUN  add-apt-repository ppa:deadsnakes/ppa -y
RUN  apt-get update -y
RUN  apt-get install python3.9 -y
RUN  update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
RUN  update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 2

# github 에 소스코드 받기
RUN git clone https://github.com/yiryeong/djangoMysqlTokenProject.git
WORKDIR /djangoMysqlTokenProject

# 필요한 환경 설치
RUN apt-get update -y
RUN apt-get install -y python3.9-dev python3-pip libmysqlclient-dev gcc
RUN apt-get install -y python3.9-distutils
RUN pip3 install --upgrade setuptools
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade distlib
RUN pip3 install -r requirements.txt
RUN pip3 install mysqlclient

EXPOSE 7002
# container가 구동되면 실행
ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:7002"]
