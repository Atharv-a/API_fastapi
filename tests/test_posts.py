from app import schemas
import pytest 

def test_get_all_posts(authorized_client, test_posts):
    res=authorized_client.get('/posts/')
    # print(res.json())
    def check(post):
        return schemas.PostOut(**post)
    posts=list(map(check,res.json()))
    assert res.status_code == 200

def test_unauthorized_user_allposts(client,test_posts):
     res=client.get("/posts/")
     assert res.status_code == 401

def test_unauthorized_user_post(client,test_posts):
     res=client.get(f"/posts/{test_posts[0].id}")
     assert res.status_code == 401

def test_nonExsisting_post(authorized_client,test_posts):
     res = authorized_client.get(f"/posts/123213")
     assert res.status_code == 404 

def test_getting_post(authorized_client,test_posts):
    res=authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize('title,content,published',[
     ('t1','c1',True),
     ('t2','c2',False),
     ('t3','c3',False),
     ('t4','c5',True),
])
def test_create_posts(authorized_client,test_user,test_posts,title,content,published):
     res=authorized_client.post("/posts/",json={
          'title':title,
          'content':content,
          'published':published
     })
     post=  schemas.Post(**res.json())
     assert res.status_code == 201
     assert post.owner_id == test_user['id']
     assert post.title == title
     assert post.content == content
     assert post.published == published
     
def test_create_post_default_val_notgiven(authorized_client,test_user,test_posts):
     res=authorized_client.post("/posts/",json={
          'title':'random',
          'content':'this is random content',
     })
     post=  schemas.Post(**res.json())
     assert res.status_code == 201
     assert post.owner_id == test_user['id']
     assert post.title == 'random'
     assert post.content =='this is random content'
     assert post.published ==  True 

def test_unauthorized_user_create_posts(client,test_posts):
     res=client.post("/posts/",json={
          'title':"random",
          'content':"content"
     })

     assert res.status_code == 401