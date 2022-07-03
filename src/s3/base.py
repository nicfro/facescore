import os
import base64

from src.settings import load_config
from src.utils.common_logger import logger
from src.utils.custom_error_handlers import ConfigError


import boto3

class S3Connector:
    def __init__(self):
        self.__check_config()
        self.session = self.get_session()
        
    def __check_config(self):
        # Load parameters from .ENV
        if os.path.isfile('ENV'):
            load_config('ENV')

        # Check required fields exist
        if None in [os.environ.get('AWS_ACCESS_KEY_ID'), 
                    os.environ.get('AWS_SECRET_ACCESS_KEY'), 
                    os.environ.get('AWS_REGION_NAME'),
                    os.environ.get('AWS_BUCKET_NAME')]:

            logger.error("Could not retrieve DB config")
            raise ConfigError("Could not retrieve DB config")

        self.AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
        self.AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME")
        self.AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")


    def get_session(self):
        return boto3.resource(
                        service_name='s3',
                        region_name=self.AWS_REGION_NAME,
                        aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY
                    )
    
    def upload_image(self, image_file, image_name):
        obj = self.session.Object(self.AWS_BUCKET_NAME, image_name)
        return obj.put(Body=image_file)
