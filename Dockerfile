FROM python:3.10.13-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update -y
WORKDIR /opt/ibanking-api
COPY . /opt/ibanking-api

RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 10001
CMD ["uvicorn", "main:app", "--app-dir", "src" , "--port", "10001", "--host", "0.0.0.0"]