FROM python:3.10

EXPOSE 5000

COPY . .


ENV DB_HOST=$DB_HOST
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_USER=$DB_USER
ENV DB_NAME=$DB_NAME
ENV DB_PORT=$DB_PORT
ENV DB_DRIVER=$DB_DRIVER
ENV JWT_KEY=$JWT_KEY
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_REGION_NAME=$AWS_REGION_NAME
ENV AWS_BUCKET_NAME=$AWS_BUCKET_NAME
ENV POINTS_START=$POINTS_START
ENV POINTS_UPLOAD_COST=$POINTS_UPLOAD_COST
ENV POINTS_VOTE_AWARD=$POINTS_VOTE_AWARD
ENV ENV POINTS_USER_META_DATA_AWARD=$POINTS_USER_META_DATA_AWARD

RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]