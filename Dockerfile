FROM python:3.13.2-alpine3.21
#RUN addgroup flask && useradd -r -g flask -s /usr/sbin/nologin flask
RUN addgroup flask && adduser -S -G flask flask
WORKDIR /usr/src/myapp
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN chown -R flask:flask .
USER flask
EXPOSE 5000
CMD ["gunicorn","-b","0.0.0.0:5000","app:app"]
