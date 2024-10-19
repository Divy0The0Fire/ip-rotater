FROM python:3.12

WORKDIR /code

RUN pip install flask requests

COPY . .

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "10000"]