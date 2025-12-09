FROM python:3.13.1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask pillow

EXPOSE 5000

ENV IN_DOCKER=1

CMD ["python", "app.py"]

