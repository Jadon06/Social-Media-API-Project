from app import schemas, oauth2
from app.routers import auth
from fastapi import status, HTTPException
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200

def test_get_all_posts_none(authorized_client):
    res = authorized_client.get("/posts/")
    assert res.status_code == 404