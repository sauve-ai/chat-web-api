FROM python:3.10.12-slim-bullseye

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]