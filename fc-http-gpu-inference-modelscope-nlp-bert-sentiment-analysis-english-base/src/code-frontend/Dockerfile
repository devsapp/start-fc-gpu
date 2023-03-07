FROM python:3.9-buster

WORKDIR /usr/src/app
RUN pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install pymysql -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .

ENV MYSQL_HOST 127.0.0.1
ENV MYSQL_PORT 3306
ENV MYSQL_USER root
ENV MYSQL_PASSWORD Serverless123
ENV MYSQL_DBNAME mall_db

CMD [ "python", "-u", "/usr/src/app/app.py" ]

