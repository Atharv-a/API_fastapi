import pytest
from app import models


@pytest.fixture()
def test_vote(test_posts,session,test_user):
   vote=models.Vote(post_id=test_posts[2].id,user_id=test_user['id'])
   session.add(vote)
   session.commit()


def test_vote_on_post(authorized_client,test_posts):
   res = authorized_client.post(
      '/votes/',json={"post_id": test_posts[0].id,'vote_type':1})
   assert res.status_code == 201


def test_voteOnPost_AlreadyVotedOn(authorized_client,test_posts,test_vote):
   res=authorized_client.post(
      '/votes/',json={'post_id':test_posts[2].id,'vote_type':1})
   assert res.status_code == 409


def test_delete_vote(authorized_client,test_posts,test_vote):
   res = authorized_client.post(
      '/votes/',json={'post_id':test_posts[2].id,'vote_type':0}
   )
   assert res.status_code == 201


def test_delete_vote_not_voted_on(authorized_client,test_posts):
   res = authorized_client.post(
      '/votes/',json={'post_id':test_posts[2].id,'vote_type':0}
   )
   assert res.status_code == 404


def test_vote_post_not_indb(authorized_client,test_posts):
   res = authorized_client.post(
      '/votes/',json={'post_id':728,'vote_type':1}
   )
   assert res.status_code == 404


def test_vote_by_unauthorized_user(client,test_posts):
   res = client.post(
      '/votes/',json={'post_id':test_posts[2].id,'vote_type':1}
   )
   assert res.status_code == 401

