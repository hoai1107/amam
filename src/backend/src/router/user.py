from fastapi import APIRouter, Response, status, FastAPI, Query, Path
import os
import sys
from pathlib import Path
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"database_connection"))
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"data_model"))
from db_connection import db
from user_model import User, UserDB
from post_model import  CommentDB
from db_connection import mongodb
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
        current_user = mongodb.users.find_one({"_id": ObjectId(user_id)})
        profile_user_model = User(**(current_user))
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
def upvote_User( postId: str, userID: str):
    cmd= mongodb.users.find_one({"_id": ObjectId(userID), "list_of_post_voted.id": postId},
    {
        'upvote_downvote': '$list_of_post_voted.upvote_downvote',
        'id': '$list_of_post_voted.id'
    })
    if cmd==0: cmd=None
    if cmd!=None:
        if cmd['upvote_downvote']==['upvote']:
            mongodb.posts.update_one({"_id":ObjectId(postId)},
            {'$inc':{
                'upvote':-1
            }})
            mongodb.users.update_one({"_id": ObjectId(userID)},
            {'$pull':{
                'list_of_post_voted':{
                    'id': postId,
                }
            }})
            return "not upvote"
        else:
            mongodb.posts.update_one({"_id":ObjectId(postId)},
            {'$inc':{
                'upvote':1,
                'downvote':-1
            }})
            mongodb.users.update_one({"_id": ObjectId(userID),"list_of_post_voted.id":postId},
            {'$set':{
                '$list_of_post_voted.0.upvote_downvote': 'upvote'
            }}) 
            return "upvote"
    else: 
            mongodb.posts.update_one({"_id":ObjectId(postId)},{'$inc':{'upvote':1}})
            mongodb.users.update_one({"_id": ObjectId(userID)},
            {"$addToSet":{
                'list_of_post_voted':{
                        'id': postId,
                        'upvote_downvote': 'upvote'
                    }
                }
            })
            return "upvote"

@router.post("/downvote/")
def downvote_User(postId: str, userID: str):
    cmd= mongodb.users.find_one({"_id": ObjectId(userID), "list_of_post_voted.id": postId},
    {
        'upvote_downvote': '$list_of_post_voted.upvote_downvote',
        'id': '$list_of_post_voted.id'
    })
    if cmd==0: cmd=None
    if cmd!=None:
        if (cmd['upvote_downvote']==['downvote']):
            mongodb.posts.update_one({"_id":ObjectId(postId)},
            {'$inc':{
                'downvote':-1
            }})
            mongodb.users.update_one({"_id": ObjectId(userID)},
            {'$pull':{
                'list_of_post_voted':{
                    'id': postId
                }
            }})
            return "not downvote"
        else:
            mongodb.posts.update_one({"_id":ObjectId(postId)},
            {'$inc':{
                'upvote':-1,
                'downvote':1
            }})
            mongodb.users.update_one({"_id": ObjectId(userID),"list_of_post_voted.id":postId},
            {'$set':{
                'list_of_post_voted.0.upvote_downvote': 'downvote'
            }}) 
            return "downvote"
    else: 
            mongodb.posts.update_one({"_id":ObjectId(postId)},{'$inc':{'downvote':1}})
            mongodb.users.update_one({"_id": ObjectId(userID)},
            {"$addToSet":{
                'list_of_post_voted':{
                        'id': postId,
                        'upvote_downvote': 'downvote'
                    }
                }
            })
            return "downvote"
            

@router.post("/comments/create")
def create_comment(userID: str,comment: CommentDB):
    cmd=mongodb.posts.find_one({"_id": ObjectId(comment.post_id)})
    if cmd==None:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        current_comment = mongodb.comments.insert_one(comment.dict())
        mongodb.users.update_one({"_id": ObjectId(userID)},{"$addToSet":{"list_of_user_comments_id": current_comment.inserted_id}})
        mongodb.posts.update_one({"_id": ObjectId(comment.post_id)},{"$inc":{"num_comments": 1}})
    return str(current_comment.inserted_id)

@router.post("/comment/change")
def change_comment(content: str,commentID: str):
    cmd=mongodb.comments.find_one({"_id": ObjectId(commentID)})
    if cmd==None:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        mongodb.comments.update_one({'_id':ObjectId(commentID)},
        {
            "$set": {
                "content": content
            }
        })
    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.post("/comment/upvote")
def upvote_comment(userID: str, commentID: str):
    cmd= mongodb.users.find_one({"_id": ObjectId(userID), "list_of_comment_voted.id":commentID},
    {
        'upvote_downvote': '$list_of_comment_voted.upvote_downvote',
        'id': '$list_of_comment_voted.id'
    })
    if cmd==0: cmd=None
    if cmd != None:
        if cmd['upvote_downvote']==['upvote']:
            mongodb.comments.update_one({"_id":ObjectId(commentID)},
            {'$inc':{
                'upvote':-1
            }})
            mongodb.users.update_one({"_id": ObjectId(userID)},
            {'$pull':{
                'list_of_comment_voted':{
                    'id': commentID,
                }
            }})
            return "not upvote"
        else:
            mongodb.comments.update_one({"_id":ObjectId(commentID)},
            {'$inc':{
                'upvote':1,
                'downvote':-1
            }})
            mongodb.users.update_one({"_id": ObjectId(userID),"list_of_comment_voted.id":commentID},
            {'$set':{
                'list_of_comment_voted.0.upvote_downvote': 'upvote'
            }}) 
        return "upvote"
    else:
        mongodb.comments.update_one({"_id":ObjectId(commentID)},{'$inc':{'upvote':1}})
        mongodb.users.update_one({"_id": ObjectId(userID)},
        {"$addToSet":{
            'list_of_comment_voted':{
                    'id': commentID,
                    'upvote_downvote': 'upvote'
                }
            }
        })
        return "upvote"

@router.post("/comment/downvote")
def downvote_comment(userID: str, commentID: str):
    cmd= mongodb.users.find_one({"_id": ObjectId(userID), "list_of_comment_voted.id":commentID},
    {
        'upvote_downvote': '$list_of_comment_voted.upvote_downvote',
        'id': '$list_of_comment_voted.id'
    })
    if cmd==0: cmd=None
    if cmd != None:
        if cmd['upvote_downvote']==['downvote']:
            mongodb.comments.update_one({"_id":ObjectId(commentID)},
            {'$inc':{
                'downvote':-1
            }})
            mongodb.users.update_one({"_id": ObjectId(userID)},
            {'$pull':{
                'list_of_comment_voted':{
                    'id': commentID,
                }
            }})
            return "not downvote"
        else:
            mongodb.comments.update_one({"_id":ObjectId(commentID)},
            {'$inc':{
                'upvote':-1,
                'downvote':1
            }})
            mongodb.users.update_one({"_id": ObjectId(userID),"list_of_comment_voted.id":commentID},
            {'$set':{
                'list_of_comment_voted.0.upvote_downvote': 'downvote'
            }}) 
        return "downvote"
    else:
        mongodb.comments.update_one({"_id":ObjectId(commentID)},{'$inc':{'downvote':1}})
        mongodb.users.update_one({"_id": ObjectId(userID)},
        {"$addToSet":{
            'list_of_comment_voted':{
                    'id': commentID,
                    'upvote_downvote': 'downvote'
                }
            }
        })
        return "downvote"

# Will have a meeting for the input of this endpoint
@router.post("/comments/reply")
def reply_comment(userID: str,parentCommentID: str, replyComment: CommentDB):
    cmd=mongodb.comments.find_one({"_id": ObjectId(parentCommentID)})
    if cmd is None: 
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        replyComment.is_root_comment = False
        current_comment = mongodb.comments.insert_one(replyComment.dict())
        mongodb.users.update_one({"_id": ObjectId(userID)},{"$addToSet":{"list_of_user_comments_id": current_comment.inserted_id}})
        mongodb.comments.update_one({"_id": ObjectId(parentCommentID)}, {"$addToSet": {"list_child_comment_id": current_comment.inserted_id}})
        mongodb.posts.update_one({"_id": ObjectId(replyComment.post_id)},{"$inc":{"num_comments": 1}})
    return str(current_comment.inserted_id)

@router.post('/user/update')
def user_update(user: UserDB):
    user_dict=user.dict()
    cmd=mongodb.users.find_one({'user_name':user_dict['user_name']})
    if cmd==None: return Response(status_code=status.HTTP_400_BAD_REQUEST)
    user_dict['_id']=cmd['_id']
    mongodb.users.replace_one({'_id': user_dict['_id']},
                              user_dict, upsert=False)
    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.delete("/delete/all")
async def delete_all_users():
    mongodb.users.delete_many({})

@router.delete("/delete/comments/all")
async def delete_all_comments():
    mongodb.comments.delete_many({})