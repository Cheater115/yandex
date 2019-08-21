FROM python:3

RUN mkdir -p /opt/services/webapi
WORKDIR /opt/services/webapi

COPY requirements.txt /opt/services/webapi
RUN pip install -r requirements.txt

COPY . /opt/services/webapi

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn.py", "ya.wsgi"]
