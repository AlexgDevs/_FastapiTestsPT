from dotenv import load_dotenv
from os import getenv

from pydantic_settings import BaseSettings
from pydantic import Field


load_dotenv()

class DBSettings:
    def __init__(self, database_url, echo_sql):
        self.database_url: str = database_url
        self.echo_sql: bool = echo_sql

db_settings = DBSettings(database_url=getenv('DB_URL'), echo_sql=True)