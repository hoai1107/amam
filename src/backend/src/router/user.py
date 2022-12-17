from fastapi import APIRouter, Response, status, FastAPI, Query, Path
import os
import sys
from pathlib import Path
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"database_connection"))
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"data_model"))
from db_connection import db
from user_model import User, VotingUser, UserDB
from post_model import Comments, CommentDB
from db_connection import mongodb
from json import JSONEncoder,loads,dumps
from collections import namedtuple
from bson import ObjectId
router = APIRouter(
    prefix="/users",
    tags= ["Users"]
)

# This is to get all information related to a specific user
@router.get("/{user_id}", response_model= User)
async def get_user(user_id: str):
    try:    
        current_user = db.child("users").child(user_id).get().val()
        profile_user_model = User(**(current_user))
        profile_user_model.id = user_id
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST, content="Something wrong!") 
    return profile_user_model

# This is to create the a user information (and get the ID of the user)
@router.post("/create")
async def create_user(user: UserDB):
    try:
        user_dict = user.dict()
        current_user = mongodb["users"].insert_one(user_dict)
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST, content="Something wrong!")
    # the Id of the user
    return str(current_user.inserted_id)

def customDecoder(studentDict):
    return namedtuple("X", studentDict.keys())(*studentDict.values())

@router.post("/upvote/")
def upvote_User( postId: str, userID: str, isUpVote: bool):
    cmd=mongodb.posts.find_one({"_id":ObjectId(postId),"list_of_user_upvote_downvote.id":{
        '$exists':userID
    }},{
        'upvote_downvote':'$list_of_user_upvote_downvote.upvote_downvote',
        'id':'$list_of_user_upvote_downvote.id'
    })
    if cmd==0: cmd=None
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
            return "not upvote"
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
            return "upvote"

@router.post("/downvote/")
def downvote_User(postId: str, userID: str, isDownVote: bool):
    cmd=mongodb.posts.find_one({"_id":ObjectId(postId),"list_of_user_upvote_downvote.id":{
        '$exists':userID
    }},{
        'upvote_downvote':'$list_of_user_upvote_downvote.upvote_downvote',
        'id':'$list_of_user_upvote_downvote.id'
    })
    if cmd==0: cmd=None
    if cmd!=None:
        if (not isDownVote and cmd['upvote_downvote']==['downvote']):
            mongodb.posts.update_one({"_id":ObjectId(postId)},
            {'$inc':{
                'downvote':-1
            },'$pull':{
                'list_of_user_upvote_downvote':{
                    'id':userID
                }
            }})
    else: 
        if isDownVote:
            mongodb.posts.update_one({"_id":ObjectId(postId)},
            {
                '$inc':{
                    'downvote':1
                },
                '$addToSet':{
                    'list_of_user_upvote_downvote':{
                        'id': userID,
                        'upvote_downvote': 'downvote'
                    }
                }
            })

@router.post("/comments/{postID}")
def create_comment(comment: CommentDB, postID: str):
    cmd=mongodb.posts.find_one({"_id": ObjectId(postID)})
    if cmd==None:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        cnt=mongodb.posts.find_one({"_id": ObjectId(postID)},{"comments":"$comments"})
        if len(cnt)>0: return Response(status_code=status.HTTP_208_ALREADY_REPORTED)
        mongodb.posts.update_one({'_id':ObjectId(postID)},
        {
            "$push": {"comments": comment.dict()}
        })
    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.post("/comment/change")
def change_comment(comment: CommentDB, postID: str):
    cmt_dict=comment.dict()
    cmd=mongodb.posts.find_one({"_id": ObjectId(postID)})
    if cmd==None:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        mongodb.posts.update_one({'_id':ObjectId(postID), 'comments.user_id':
        {
            '$exists': cmt_dict['user_id']
        }},
        {
            "$set": {
                "comments.$.content_of_comment":cmt_dict['content_of_comment']
            }
        })
    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.post("/comment/upvote")
def upvote_comment(userID: str, postID: str, isUpVote: bool, user: VotingUser| None):
    user_dict=user.dict()
    cmd=mongodb.posts.find_one({'_id': ObjectId(postID), 'comments.user_id': {"$exists": userID}})
    if cmd==None: Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        #cmd=mongodb.posts.find_one({'_id': ObjectId(postID), 'comments.user_id': {"$exists":userID}, 'comments.list_of_user_upvote_downvote_cmt.id': {"$exists":user_dict['id']}})
        if not isUpVote:
            mongodb.posts.update_one({'_id': ObjectId(postID),'comments.user_id': {"$exists":userID}}, 
            {
                '$pull': {'comments.list_of_user_upvote_downvote_cmt': {'id' :{
                    "$exists": user_dict['id']
                }}},
                '$inc': {'comments.up_vote',-1}
            })
        elif isUpVote:
                user_dict['upvote_downvote']='upvote'
                mongodb.posts.update_one({'_id': ObjectId(postID),'comments.user_id':userID}, 
            {
                    '$push': {'comments.$.list_of_user_upvote_downvote_cmt':user_dict},
                    '$inc':{'comments.$.up_vote':1}
            })
    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.post("/comment/downvote")
def downvote_comment(userID: str, postID: str, isDownvote: bool, user: VotingUser| None):
    user_dict=user.dict()
    cmd=mongodb.posts.find_one({'_id': ObjectId(postID), 'comments.user_id': {"$exists": userID}})
    if cmd==None: Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        #cmd=mongodb.posts.find_one({'_id': ObjectId(postID), 'comments.user_id': {"$exists":userID}, 'comments.list_of_user_upvote_downvote_cmt.id': {"$exists":user_dict['id']}})
        if not isDownvote:
            mongodb.posts.update_one({'_id': ObjectId(postID),'comments.user_id': {"$exists":userID}}, 
            {
                '$pull': {'comments.list_of_user_upvote_downvote_cmt': {'id' :{
                    "$exists": user_dict['id']
                }}},
                '$inc': {'comments.downvote',-1}
            })
        elif isDownvote:
                user_dict['upvote_downvote']='downvote'
                mongodb.posts.update_one({'_id': ObjectId(postID),'comments.user_id':userID}, 
            {
                    '$push': {'comments.$.list_of_user_upvote_downvote_cmt':user_dict},
                    '$inc':{'comments.$.down_vote':1}
            })
    return Response(status_code=status.HTTP_202_ACCEPTED)

# Will have a meeting for the input of this endpoint
@router.post("/comments/reply")
def reply_comment(parentCommentID: str, replyComment: CommentDB):
    cmd=mongodb.comments.find_one({"_id": ObjectId(parentCommentID)})
    if cmd is None: 
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        replyComment.is_root_comment = False
        current_comment = mongodb.comments.insert_one(replyComment)
        mongodb.comments.update_one({"_id": ObjectId(parentCommentID)}, {"$addToSet": {"list_child_comment_id": current_comment.inserted_id}})
    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.post('/user/update')
def user_update(user: UserDB):
    user_dict=user.dict()
    cmd=mongodb.users.find_one({'user_name':user_dict['user_name']})
    if cmd==None: return Response(status_code=status.HTTP_400_BAD_REQUEST)
    user_dict['_id']=cmd['_id']
    mongodb.users.replace_one({'_id': user_dict['_id']},
                              user_dict, upsert=False)
    return Response(status_code=status.HTTP_202_ACCEPTED)