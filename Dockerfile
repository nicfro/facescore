FROM python:3.8

EXPOSE 80

COPY . .

ENV DB_HOST=$DB_HOST
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_USER=$DB_USER
ENV DB_NAME=$DB_NAME
ENV DB_PORT=$DB_PORT

RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]