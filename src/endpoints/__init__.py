import os
import sys
sys.path.insert(0, os.getcwd())

from src.database.base import DBConnector
from src.s3.base import S3Connector

DBC = DBConnector()
S3 = S3Connector()