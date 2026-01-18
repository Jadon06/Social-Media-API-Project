from app import schemas, oauth2, models
from app.routers import auth
from fastapi import status, HTTPException
import pytest

# tests for 'get all posts'
def test_get_all_posts(authorized_client, test_posts): # even though test_posts is never called directly, pytest detects that the function 
                                                       # depends on the fixture injecting it's return value into the test
    res = authorized_client.get("/posts/")

    """TO-DO: Correct the test_posts values to not include password"""
    # def validate(post):
    #     return schemas.PostResponse(**post)
    # posts_map = map(validate, res.json()) # passes every element in res.json() into the function 'validate' and ensures that every element is 
    #                                       # according to the PostResponse schema
    # posts_list = list(posts_map)
    assert res.status_code == 200

def test_get_all_posts_unauthorized(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_get_all_posts_no_posts_exist(authorized_client):
    res = authorized_client.get("/posts/")
    assert res.status_code == 404


# tests for 'get one post'
def test_get_one_posts_unauthorized(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_posts_id_DNE(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/1000")
    assert res.status_code == 404

def test_get_one_posts_authorized(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostVote(**res.json()) # verify that the response model follows the provided schema 'PostVote'
    assert post.Post.User_id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title
    assert res.status_code == 200

# tests for 'create a post'
@pytest.mark.parametrize("title, content, published, status_code", [("test post 1", "content of test post 1", True, 201),
                                                                    ("test post 1", "content of test post 1", False, 201)])
def test_create_post(authorized_client, title, content, published, status_code):
    res = authorized_client.post("/posts/", json={"title": title, "content":content, "published":published})
    new_post = schemas.PostResponse(**res.json())
    assert new_post.title == title
    assert new_post.content == content
    assert new_post.published == published
    assert res.status_code == status_code

def test_create_post_PublishedIsNone(authorized_client): # verify that if no input is placed for published, published will default to false
    res = authorized_client.post("/posts/", json={"title": "some title", "content" : "some content"})
    new_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert new_post.published == False

def test_create_a_post_unauthorized(client, test_posts):
    res = client.post("/posts/", json={"title": "some title", "content" : "some content"})
    assert res.status_code == 401

# tests for 'delete a post'
def test_delete_post_unauthorized(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    assert res.json().get('detail') == "Not authenticated"

def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_id_DNE(authorized_client, test_posts):
    res = authorized_client.delete("/posts/10")
    assert res.status_code == 404

def test_delete_other_users_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
    assert res.json().get('detail') == 'Unauthorized Access!!'

# test for 'update post'

def test_update_post(authorized_client, test_posts, session):
    data = {"title":"new_title", "content":"new_content"}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    
    updated_post = schemas.PostCreate(**data)
    
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert res.status_code == 200
    
def test_update_post_unauthorized(client, test_posts, session):
    data = {"title":"new_title", "content":"new_content"}
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    
    assert res.status_code == 401

def test_update_post_DNE(authorized_client, test_posts, session):
    data = {"title":"new_title", "content":"new_content"}
    res = authorized_client.put("/posts/10", json=data)
    
    assert res.status_code == 404
