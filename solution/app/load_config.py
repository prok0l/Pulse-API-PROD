from dotenv import load_dotenv
from dataclasses import dataclass
from os import getenv


@dataclass
class Config:
    username: str
    password: str
    host: str
    port: str
    db_name: str
    secret: str


def load() -> Config:
    load_dotenv()
    conf = Config(
        username=getenv('POSTGRES_USERNAME'),
        password=getenv('POSTGRES_PASSWORD'),
        host=getenv('POSTGRES_HOST'),
        port=getenv('POSTGRES_PORT'),
        db_name=getenv('POSTGRES_DATABASE'),
        secret=getenv('RANDOM_SECRET')
    )
    return conf
