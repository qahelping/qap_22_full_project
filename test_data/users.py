import os
from dataclasses import dataclass


@dataclass
class User:
    email: str
    password: str = os.getenv('BASE_PASSWORD', None)


CHARLI = User(email='charlie@example.com')
ADMIN = User(email='admin@example.com', password='admin123')

