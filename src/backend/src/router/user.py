from fastapi import APIRouter, Response, status, Depends, Query, Path
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(Path(__file__).parents[1], "database_connection"))
sys.path.insert(0, os.path.join(Path(__file__).parents[1], "data_model"))
from user_model import User, UserDB
from post_model import CommentDB
from authentication import authentication
from dependencies import recursive_remove_comment
from db_connection import mongodb, client, read_concern, WriteConcern
from collections import namedtuple
from bson import ObjectId

router = APIRouter(prefix="/users", tags=["Users"])

# This is to get all information related to a specific user
@router.get("", response_model=User)
async def get_user(user_id: str = Depends(authentication)):
    # try:
    current_user = mongodb.users.find_one({"user_id": user_id})
    profile_user_model = User(**(current_user))
    # except:
    #     return Response(status_code= status.HTTP_400_BAD_REQUEST, content="Something wrong!")
    return profile_user_model


def customDecoder(studentDict):
    return namedtuple("X", studentDict.keys())(*studentDict.values())


@router.put("/upvote/{postId}")
async def upvote_User( postId: str, userID: str = Depends(authentication)):
    with client.start_session() as session:
        with session.start_transaction(read_concern=read_concern.ReadConcern("majority"),write_concern=WriteConcern("majority")):
            try:
                cmd= mongodb.users.find_one({"user_id": userID, "list_of_post_voted.id": postId},
                {
                    'upvote_downvote': '$list_of_post_voted.upvote_downvote',
                    'id': '$list_of_post_voted.id'
                },session=session)
                if cmd==0: cmd=None
                if cmd!=None:
                    if cmd['upvote_downvote']==['upvote']:
                        mongodb.posts.update_one({"_id":ObjectId(postId)},
                        {'$inc':{
                            'upvote':-1
                        }},session=session)
                        mongodb.users.update_one({"user_id": userID},
                        {'$pull':{
                            'list_of_post_voted':{
                                'id': postId,
                            }
                        }},session=session)
                        session.commit_transaction()
                        return "not upvote"
                    else:
                        mongodb.posts.update_one({"_id":ObjectId(postId)},
                        {'$inc':{
                            'upvote':1,
                            'downvote':-1
                        }},session=session)
                        mongodb.users.update_one({"user_id": userID,"list_of_post_voted.id":postId},
                        {'$set':{
                            'list_of_post_voted.0.upvote_downvote': 'upvote'
                        }},session=session)
                        session.commit_transaction()
                        return "upvote"
                else: 
                        mongodb.posts.update_one({"_id":ObjectId(postId)},{'$inc':{'upvote':1}},session=session)
                        mongodb.users.update_one({"user_id": userID},
                        {"$addToSet":{
                            'list_of_post_voted':{
                                    'id': postId,
                                    'upvote_downvote': 'upvote'
                                }
                            }
                        },session=session)
                session.commit_transaction()
            except:
                session.abort_transaction()
                return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return "upvote"

@router.put("/downvote/{postId}")
async def downvote_User(postId: str, userID: str = Depends(authentication)):
    with client.start_session() as session:
        with session.start_transaction(read_concern=read_concern.ReadConcern("majority"),write_concern=WriteConcern("majority")):
            try:
                cmd= mongodb.users.find_one({"user_id": userID, "list_of_post_voted.id": postId},
                {
                    'upvote_downvote': '$list_of_post_voted.upvote_downvote',
                    'id': '$list_of_post_voted.id'
                },session=session)
                if cmd==0: cmd=None
                if cmd!=None:
                    if (cmd['upvote_downvote']==['downvote']):
                        mongodb.posts.update_one({"_id":ObjectId(postId)},
                        {'$inc':{
                            'downvote':-1
                        }},session=session)
                        mongodb.users.update_one({"user_id": userID},
                        {'$pull':{
                            'list_of_post_voted':{
                                'id': postId
                            }
                        }},session=session)
                        session.commit_transaction()
                        return "not downvote"
                    else:
                        mongodb.posts.update_one({"_id":ObjectId(postId)},
                        {'$inc':{
                            'upvote':-1,
                            'downvote':1
                        }},session=session)
                        mongodb.users.update_one({"user_id": userID,"list_of_post_voted.id":postId},
                        {'$set':{
                            'list_of_post_voted.0.upvote_downvote': 'downvote'
                        }},session=session)
                        session.commit_transaction()
                        return "downvote"
                else: 
                        mongodb.posts.update_one({"_id":ObjectId(postId)},{'$inc':{'downvote':1}},session=session)
                        mongodb.users.update_one({"user_id": userID},
                        {"$addToSet":{
                            'list_of_post_voted':{
                                    'id': postId,
                                    'upvote_downvote': 'downvote'
                                }
                            }
                        },session=session)
                session.commit_transaction()
            except:
                session.abort_transaction()
                return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return "downvote"
            

@router.post("/comments/create")
async def create_comment(*,userID: str = Depends(authentication),comment: CommentDB):
    with client.start_session() as session:
        with session.start_transaction(read_concern=read_concern.ReadConcern("majority"),write_concern=WriteConcern("majority")):
            try:
                comment.user_id = userID
                comment_dict = comment.dict()
                comment_dict["time_created"] = str(comment_dict["time_created"])
                current_comment = mongodb.comments.insert_one(comment_dict,session=session)
                mongodb.users.update_one({"user_id": userID},{"$addToSet":{"list_of_user_comments_id": str(current_comment.inserted_id)}},session=session)
                mongodb.posts.update_one({"_id": ObjectId(comment.post_id)},{"$inc":{"num_comments": 1}},session=session)
                session.commit_transaction()
            except:
                session.abort_transaction()
                return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return str(current_comment.inserted_id)


@router.put("/comment/{commentID}")
async def change_comment(content: str,commentID: str):
    with client.start_session() as session:
        with session.start_transaction(write_concern=WriteConcern("majority")):
            try:
                mongodb.comments.update_one({'_id':ObjectId(commentID)},
                {
                    "$set": {
                        "content": content
                    }
                },session=session)
                session.commit_transaction()
            except:
                session.abort_transaction()
                return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.delete("/comment/{commentID}")
async def delete_comment(*,userID: str = Depends(authentication),commentID: str):
    with client.start_session() as session:
        recursive_remove_comment(commentID=commentID,session=session)
    return Response(status_code=status.HTTP_202_ACCEPTED)

"""
The reason why I use the majority for both read and write concern is that:
The conflict may happen here is when there are 2 transactions either of which involves this endpoint and the other try to delete the comment or the post
use majority means that it affects and is affected by the majority of nodes which is made consistent later on by MVCC of WiredTiger in MongoDB
If the first transaction is commited first, every thing happens as expected
If the second one is commited first, then the first transaction will be aborted by the raise of error due to not finding the entity in the database
That's is how I choose this concern, since it's ensure the consistency but with slight downgrade in the performance which is insignificant
"""
@router.put("/comment/{commentID}/upvote")
async def upvote_comment(*,userID: str = Depends(authentication), commentID: str):
    with client.start_session() as session:
        with session.start_transaction(read_concern=read_concern.ReadConcern("majority"),write_concern=WriteConcern("majority")):
            try:
                cmd= mongodb.users.find_one({"user_id": userID, "list_of_comment_voted.id":commentID},
                {
                    'upvote_downvote': '$list_of_comment_voted.upvote_downvote',
                    'id': '$list_of_comment_voted.id'
                },session=session)
                if cmd==0: cmd=None
                if cmd != None:
                    if cmd['upvote_downvote']==['upvote']:
                        mongodb.comments.update_one({"_id":ObjectId(commentID)},
                        {'$inc':{
                            'upvote':-1
                        }},session=session)
                        mongodb.users.update_one({"user_id": userID},
                        {'$pull':{
                            'list_of_comment_voted':{
                                'id': commentID,
                            }
                        }},session=session)
                        session.commit_transaction()
                        return "not upvote"
                    else:
                        mongodb.comments.update_one({"_id":ObjectId(commentID)},
                        {'$inc':{
                            'upvote':1,
                            'downvote':-1
                        }},session=session)
                        mongodb.users.update_one({"user_id": userID,"list_of_comment_voted.id":commentID},
                        {'$set':{
                            'list_of_comment_voted.0.upvote_downvote': 'upvote'
                        }},session=session)
                    session.commit_transaction()
                    return "upvote"
                else:
                    mongodb.comments.update_one({"_id":ObjectId(commentID)},{'$inc':{'upvote':1}},session=session)
                    mongodb.users.update_one({"user_id": userID},
                    {"$addToSet":{
                        'list_of_comment_voted':{
                                'id': commentID,
                                'upvote_downvote': 'upvote'
                            }
                        }
                    },session=session)
                session.commit_transaction()
            except:
                session.abort_transaction()
                return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return "upvote"

@router.put("/comment/{commentID}/downvote")
async def downvote_comment(*,userID: str = Depends(authentication), commentID: str):
    with client.start_session() as session:
        with session.start_transaction(read_concern=read_concern.ReadConcern("majority"),write_concern=WriteConcern("majority")):
            try:
                cmd= mongodb.users.find_one({"user_id": userID, "list_of_comment_voted.id":commentID},
                {
                    'upvote_downvote': '$list_of_comment_voted.upvote_downvote',
                    'id': '$list_of_comment_voted.id'
                },session=session)
                if cmd==0: cmd=None
                if cmd != None:
                    if cmd['upvote_downvote']==['downvote']:
                        mongodb.comments.update_one({"_id":ObjectId(commentID)},
                        {'$inc':{
                            'downvote':-1
                        }},session=session)
                        mongodb.users.update_one({"user_id": userID},
                        {'$pull':{
                            'list_of_comment_voted':{
                                'id': commentID,
                            }
                        }},session=session)
                        session.commit_transaction()
                        return "not downvote"
                    else:
                        mongodb.comments.update_one({"_id":ObjectId(commentID)},
                        {'$inc':{
                            'upvote':-1,
                            'downvote':1
                        }},session=session)
                        mongodb.users.update_one({"user_id": userID,"list_of_comment_voted.id":commentID},
                        {'$set':{
                            'list_of_comment_voted.0.upvote_downvote': 'downvote'
                        }},session=session)
                    session.commit_transaction()
                    return "downvote"
                else:
                    mongodb.comments.update_one({"_id":ObjectId(commentID)},{'$inc':{'downvote':1}},session=session)
                    mongodb.users.update_one({"user_id": userID},
                    {"$addToSet":{
                        'list_of_comment_voted':{
                                'id': commentID,
                                'upvote_downvote': 'downvote'
                            }
                        }
                    },session=session)
                session.commit_transaction()
            except:
                session.abort_transaction()
                return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return "downvote"


# Will have a meeting for the input of this endpoint
@router.post("/comments/reply")
async def reply_comment(*,userID: str = Depends(authentication),parentCommentID: str,replyComment:CommentDB):
    with client.start_session() as session:
        
        with session.start_transaction(read_concern=read_concern.ReadConcern("majority"),write_concern=WriteConcern("majority")):
            try:
                cmd=mongodb.comments.find_one({"_id": ObjectId(parentCommentID)},session=session)
                root_id = parentCommentID
                if not cmd['root_comment_id']== "root":
                    root_id = cmd['root_comment_id']
                replyComment.user_id = userID
                replyComment.root_comment_id = root_id
                comment_dict = replyComment.dict()
                comment_dict["time_created"] = str(comment_dict["time_created"])
                current_comment = mongodb.comments.insert_one(comment_dict,session=session)
                mongodb.users.update_one({"user_id": userID},{"$addToSet":{"list_of_user_comments_id": str(current_comment.inserted_id)}},session=session)
                mongodb.comments.update_one({"_id": ObjectId(root_id)}, {"$addToSet": {"list_child_comment_id": str(current_comment.inserted_id)}},session=session)
                mongodb.posts.update_one({"_id": ObjectId(replyComment.post_id)},{"$inc":{"num_comments": 1}},session=session)
                session.commit_transaction()
            except:
                session.abort_transaction()
                return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return str(current_comment.inserted_id)

@router.put('/user/update/')
async def user_update(*,userID= Depends(authentication),user: User):
    try:
        mongodb.users.update_one({"user_id":userID},{
            "$set":{
                "avatar": user.avatar,
                "about_me": user.about_me,
                "location":user.location,
                "title": user.title
            }})
    except:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.put("/user/bookmark/{postID}")
async def save_book_mark(*,userID=Depends(authentication),postID:str):
    with client.start_session() as session:
        with session.start_transaction(read_concern=read_concern.ReadConcern("majority"),write_concern=WriteConcern("majority")):
            try:
                bookmark = mongodb.users.find_one({"user_id": userID, "bookmark.id":postID},session=session)
                if bookmark == None:
                    post = mongodb.posts.find_one({"_id": ObjectId(postID)},session=session)
                    mongodb.users.update_one({"user_id": userID},
                    {"$addToSet":
                        {
                            "bookmark":{
                                "id": postID,
                                "title": post["title"]
                            }
                        }
                    },session=session)
                else:
                    mongodb.users.update_one({"user_id": userID},
                    {"$pull":
                        {
                            "bookmark":{
                                "id": postID
                            }
                        }
                    },session=session)
                session.commit_transaction()
            except:
                session.abort_transaction()
                return Response(status_code= status.HTTP_400_BAD_REQUEST)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.delete("/delete/all")
async def delete_all_users():
    mongodb.users.delete_many({})


@router.delete("/delete/comments/all")
async def delete_all_comments():
    mongodb.comments.delete_many({})
