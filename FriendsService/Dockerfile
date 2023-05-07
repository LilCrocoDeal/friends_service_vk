FROM python:3.9.16

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/fs

COPY .requirments.txt /usr/src/requirments.txt
RUN pip install -r /usr/src/requirments.txt

COPY . /usr/src/fs

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]