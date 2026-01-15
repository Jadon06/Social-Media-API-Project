from app import schemas, oauth2
from app.routers import auth
from fastapi import status, HTTPException
import pytest

def test_get_all_posts(client, test_user):
    