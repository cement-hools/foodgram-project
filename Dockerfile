FROM python:3.8.5

WORKDIR /foodgram

COPY ./requirements.txt .

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN python3 manage.py collectstatic --noinput
