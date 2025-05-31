FROM python:3.11-slim

WORKDIR /var/www/app

RUN pip install --no-cache-dir pillow

CMD ["tail", "-f", "/dev/null"]
