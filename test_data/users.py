import os
from dataclasses import dataclass


@dataclass
class User:
    email: str
    password: str = os.getenv('BASE_PASSWORD', None)


CHARLI = User(email='charlie@example.com')
CHARLI2 = User(email='charlie@example.com', password='password123')
