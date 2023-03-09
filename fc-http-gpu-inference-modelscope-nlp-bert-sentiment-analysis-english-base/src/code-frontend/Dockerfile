FROM python:3.9-buster

WORKDIR /usr/src/app
RUN pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install pymysql -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install tablestore -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .

CMD [ "python", "-u", "/usr/src/app/app.py" ]

