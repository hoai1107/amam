from fastapi import APIRouter, Response, status, Depends, Query, Path
import os
import sys
from pathlib import Path
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"database_connection"))
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"data_model"))
from user_model import User, UserDB
from post_model import  CommentDB
from authentication import authentication
from db_connection import mongodb
from collections import namedtuple
from bson import ObjectId

router = APIRouter(
    prefix="/users",
    tags= ["Users"]
)

# This is to get all information related to a specific user
@router.get("", response_model= User)
async def get_user(user_id: str = Depends(authentication)):
    try:    
        current_user = mongodb.users.find_one({"user_id": user_id})
        profile_user_model = User(**(current_user))
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST, content="Something wrong!") 
    return profile_user_model

def customDecoder(studentDict):
    return namedtuple("X", studentDict.keys())(*studentDict.values())

@router.post("/upvote/")
def upvote_User( postId: str, userID: str = Depends(authentication)):
    cmd= mongodb.users.find_one({"user_id": userID, "list_of_post_voted.id": postId},
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
            mongodb.users.update_one({"user_id": userID},
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
            mongodb.users.update_one({"user_id": userID,"list_of_post_voted.id":postId},
            {'$set':{
                'list_of_post_voted.0.upvote_downvote': 'upvote'
            }}) 
            return "upvote"
    else: 
            mongodb.posts.update_one({"_id":ObjectId(postId)},{'$inc':{'upvote':1}})
            mongodb.users.update_one({"user_id": userID},
            {"$addToSet":{
                'list_of_post_voted':{
                        'id': postId,
                        'upvote_downvote': 'upvote'
                    }
                }
            })
            return "upvote"

@router.post("/downvote/")
def downvote_User(postId: str, userID: str = Depends(authentication)):
    cmd= mongodb.users.find_one({"user_id": userID, "list_of_post_voted.id": postId},
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
            mongodb.users.update_one({"user_id": userID},
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
            mongodb.users.update_one({"user_id": userID,"list_of_post_voted.id":postId},
            {'$set':{
                'list_of_post_voted.0.upvote_downvote': 'downvote'
            }}) 
            return "downvote"
    else: 
            mongodb.posts.update_one({"_id":ObjectId(postId)},{'$inc':{'downvote':1}})
            mongodb.users.update_one({"user_id": userID},
            {"$addToSet":{
                'list_of_post_voted':{
                        'id': postId,
                        'upvote_downvote': 'downvote'
                    }
                }
            })
            return "downvote"
            

@router.post("/comments/create")
def create_comment(*,userID: str = Depends(authentication),post_id: str, content: str):
    cmd=mongodb.posts.find_one({"_id": ObjectId(post_id)})
    if cmd==None:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        comment = CommentDB(post_id=post_id,content=content)
        current_comment = mongodb.comments.insert_one(comment.dict())
        mongodb.users.update_one({"user_id": userID},{"$addToSet":{"list_of_user_comments_id": current_comment.inserted_id}})
        mongodb.posts.update_one({"_id": ObjectId(post_id)},{"$inc":{"num_comments": 1}})
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
def upvote_comment(*,userID: str = Depends(authentication), commentID: str):
    cmd= mongodb.users.find_one({"user_id": userID, "list_of_comment_voted.id":commentID},
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
            mongodb.users.update_one({"user_id": userID},
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
            mongodb.users.update_one({"user_id": userID,"list_of_comment_voted.id":commentID},
            {'$set':{
                'list_of_comment_voted.0.upvote_downvote': 'upvote'
            }}) 
        return "upvote"
    else:
        mongodb.comments.update_one({"_id":ObjectId(commentID)},{'$inc':{'upvote':1}})
        mongodb.users.update_one({"user_id": userID},
        {"$addToSet":{
            'list_of_comment_voted':{
                    'id': commentID,
                    'upvote_downvote': 'upvote'
                }
            }
        })
        return "upvote"

@router.post("/comment/downvote")
def downvote_comment(*,userID: str = Depends(authentication), commentID: str):
    cmd= mongodb.users.find_one({"user_id": userID, "list_of_comment_voted.id":commentID},
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
            mongodb.users.update_one({"user_id": userID},
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
            mongodb.users.update_one({"user_id": userID,"list_of_comment_voted.id":commentID},
            {'$set':{
                'list_of_comment_voted.0.upvote_downvote': 'downvote'
            }}) 
        return "downvote"
    else:
        mongodb.comments.update_one({"_id":ObjectId(commentID)},{'$inc':{'downvote':1}})
        mongodb.users.update_one({"user_id": userID},
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
def reply_comment(*,userID: str = Depends(authentication),parentCommentID: str, post_id: str, content: str):
    cmd=mongodb.comments.find_one({"_id": ObjectId(parentCommentID)})
    if cmd is None: 
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        root_id = parentCommentID
        if not cmd['root_comment_id']== "root":
            root_id = cmd['root_comment_id']
        replyComment = CommentDB(post_id=post_id,content=content,root_comment_id=root_id)
        current_comment = mongodb.comments.insert_one(replyComment.dict())
        mongodb.users.update_one({"user_id": userID},{"$addToSet":{"list_of_user_comments_id": current_comment.inserted_id}})
        mongodb.comments.update_one({"_id": ObjectId(root_id)}, {"$addToSet": {"list_child_comment_id": current_comment.inserted_id}})
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