from app import schemas, oauth2, models
from app.routers import auth
from fastapi import status, HTTPException
import pytest

@pytest.mark.parametrize("choice, status_code", [("upvote", 201), ("downvote", 201)])
def test_vote_on_post(authorized_client, test_posts, choice, status_code):
    res = authorized_client.post("/vote/", json={"choice":choice, "post_id":test_posts[0].id})

    assert res.status_code == status_code

def test_upvote_on_post_twice(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"choice":"upvote", "post_id":test_posts[0].id})
    assert res.status_code == 403

def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"choice":"unvote", "post_id":test_posts[0].id})
    assert res.json().get('detail') == 'Vote was removed successfully!!'
    assert res.status_code == 200

def test_delete_vote_DNE(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"choice":"unvote", "post_id":100})
    assert res.status_code == 404

def test_vote_post_DNE(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"choice":"upvote", "post_id":100})
    assert res.status_code == 404
    
def test_vote_post_unauthorized(client, test_posts):
    res = client.post("/vote/", json={"choice":"upvote", "post_id":100})
    assert res.status_code == 401
    assert res.json().get('detail') == 'Not authenticated'
