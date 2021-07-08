FROM python:3.9

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

#VOLUME C:/Users/Администратор/Desktop/autotest2/resurses /usr/src/app/resourses




ENV TZ Europe/Moscow

CMD ["python", "app.py"]
