FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING UTF-8
ENV PATH /home/dashboard/.local/bin:$PATH
ENV TZ America/Mexico_City
ENV HOME /home/dashboard
ENV APP_HOME /home/dashboard
ENV LOG_LEVEL debug

WORKDIR $APP_HOME

COPY ./models ${APP_HOME}/models
COPY ./resources ${APP_HOME}/resources
COPY ./schemas ${APP_HOME}/schemas
COPY ./extensions.py ${APP_HOME}
COPY ./config.py ${APP_HOME}
COPY ./app.py ${APP_HOME}
COPY ./wsgi.py ${APP_HOME}
COPY ./requirements.txt ${APP_HOME}

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd -ms /bin/bash dashboard && \
    chown -Rf dashboard:dashboard /home/dashboard
USER dashboard

COPY ./wsgi.py ${APP_HOME}/wsgi.py

EXPOSE 8080
ENTRYPOINT ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:8080 --log-level $LOG_LEVEL wsgi:app"]