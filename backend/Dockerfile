###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.3 as builder

# set work directory
WORKDIR /usr/src/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update
RUN apt-get install -y libpq-dev python3-dev

# nc
RUN apt-get install -y netcat

RUN pip install --upgrade pip

# install dependencies
COPY backend/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/backend/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8.3

# create directory for the app user
RUN mkdir -p /home/backend

# create the backend user
RUN addgroup --system app
RUN adduser --system --ingroup app app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update
RUN apt-get install -y libpq-dev python3-dev
RUN apt-get install -y netcat
RUN apt-get install -y ffmpeg libsm6 libxext6

COPY --from=builder /usr/src/backend/wheels /wheels
COPY --from=builder /usr/src/backend/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*
# requirements_nowheel.txt contains modules not available to be installed via copied wheels
COPY backend/requirements_nowheel.txt .
RUN pip install -r requirements_nowheel.txt

# copy entrypoint.prod.sh
COPY backend/entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# copy project
COPY backend $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
