FROM python:3.9.16

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN git clone https://github.com/LilCrocoDeal/friends_service_vk.git /fs

WORKDIR /fs/FriendsService

RUN pip install -r requirements.txt

EXPOSE 8080
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
