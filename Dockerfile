FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app/

RUN pip install -r ./requirements.txt

EXPOSE 5000

ENV PYTHONPATH="$PYTHONPATH:/app"
CMD ["python", "/app/api/api.py"]
