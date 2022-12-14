import sys
import os
from bson import ObjectId
from pathlib import Path
from collections import namedtuple
from json import JSONEncoder,loads,dumps
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"database_connection"))
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"data_model"))
sys.path.insert(0,os.path.join(Path(__file__).parents[1],""))
from db_connection import mongodb
from user_model import User
from main import app
def customDecoder(studentDict):
    return namedtuple("X", studentDict.keys())(*studentDict.values())
@app.get('/userID/{userID}')
def getUser(userId: str) -> dict:
    c=mongodb.users.find({"_id":ObjectId(userId)})
    temp=dict()
    for i in c:
        temp=i
    temp['_id']=userId
    return temp
def getPost(questionId:str) -> dict:
    c=mongodb.posts.find({"_id":ObjectId(questionId)})
    temp=dict()
    for i in c:
        temp=i
    temp['_id']=questionId
    return temp
def getUserInfo(userId: str) -> str:
    temp=getUserInfo(userId)
    temp['_id']=userId
    temp['number_of_follows']=len(temp['list_of_follows'])
    del temp['list_of_follows']
    res=dumps(temp,indent=4)
    return res
def getPostInUserPorfile(postId: str) -> str:
    cmd=mongodb.posts.find({'_id':ObjectId(postId)},
    {
        'title':'$title',
        'tags':'$tags',
        'upvote':'$upvote',
        'downvote':'$downvote',
        'comments':'$comments'
    })
    t=0
    for i in cmd:
        t=i
        i=0
    t['number_of_comments']=len(t['comments'])
    del t['_id']
    del t['comments']
    return dumps(t,indent=4)
def upVoteUser(postId: str, userID: str, isUpVote: bool):
    cmd=mongodb.posts.find({"_id":ObjectId(postId),"list_of_user_upvote_downvote.id":{
        '$exists':userID
    }},{
        'upvote_downvote':'$list_of_user_upvote_downvote.upvote_downvote',
        'id':'$list_of_user_upvote_downvote.id'
    })
    t=0
    for i in cmd:
        t=i
        i=1
    cmd=t
    if t==0: cmd=None
    if cmd!=None:
        if (not isUpVote and cmd['upvote_downvote']==['upvote']):
            mongodb.posts.update_one({"_id":ObjectId(postId)},
            {'$inc':{
                'upvote':-1
            }})
            mongodb.posts.update_one({"_id":ObjectId(postId)},
            {'$pull':{
                'list_of_user_upvote_downvote':{
                    'id':userID
                }
            }})
    else: 
        if isUpVote:
            mongodb.posts.update_one({"_id":ObjectId(postId)},
            {
                '$inc':{
                    'upvote':1
                },
                '$addToSet':{
                    'list_of_user_upvote_downvote':{
                        'id': userID,
                        'upvote_downvote': 'upvote'
                    }
                }
            })
def downVoteUser(postId: str, userID: str, isUpVote: bool):
    cmd=mongodb.posts.find({"_id":ObjectId(postId),"list_of_user_upvote_downvote.id":{
        '$exists':userID
    }},{
        'upvote_downvote':'$list_of_user_upvote_downvote.upvote_downvote',
        'id':'$list_of_user_upvote_downvote.id'
    })
    t=0
    for i in cmd:
        t=i
        i=1
    cmd=t
    if t==0: cmd=None
    if cmd!=None:
        if (not isUpVote and cmd['upvote_downvote']==['upvote']):
            mongodb.posts.update_one({"_id":ObjectId(postId)},
            {'$inc':{
                'upvote':-1
            },'$pull':{
                'list_of_user_upvote_downvote':{
                    'id':userID
                }
            }})
    else: 
        if isUpVote:
            mongodb.posts.update_one({"_id":ObjectId(postId)},
            {
                '$inc':{
                    'upvote':1
                },
                '$addToSet':{
                    'list_of_user_upvote_downvote':{
                        'id': userID,
                        'upvote_downvote': 'upvote'
                    }
                }
            })