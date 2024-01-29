FROM python:3.7
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir chatterbot
RUN pip  install --no-cache-dir flask
CMD ["python", "bot.py"]

