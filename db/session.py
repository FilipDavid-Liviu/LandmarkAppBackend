import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.core.config import settings
import psycopg2

def connect_ipv4_only(dsn):
    orig_getaddrinfo = socket.getaddrinfo

    def ipv4_only_getaddrinfo(*args, **kwargs):
        return [info for info in orig_getaddrinfo(*args, **kwargs) if info[0] == socket.AF_INET]

    socket.getaddrinfo = ipv4_only_getaddrinfo
    try:
        conn = psycopg2.connect(dsn)
    finally:
        socket.getaddrinfo = orig_getaddrinfo
    return conn

engine = create_engine(
    settings.DATABASE_URL,
    creator=lambda: connect_ipv4_only(settings.DATABASE_URL)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
