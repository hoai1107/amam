from fastapi import APIRouter, Response, status, Depends, Query, Path
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(Path(__file__).parents[1], "database_connection"))
sys.path.insert(0, os.path.join(Path(__file__).parents[1], "data_model"))
from user_model import User, UserDB
from post_model import CommentDB
from authentication import authentication
from db_connection import mongodb
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


@router.put("/upvote/")
def upvote_User(postId: str, userID: str = Depends(authentication)):
    cmd = mongodb.users.find_one(
        {"user_id": userID, "list_of_post_voted.id": postId},
        {
            "upvote_downvote": "$list_of_post_voted.upvote_downvote",
            "id": "$list_of_post_voted.id",
        },
    )
    if cmd == 0:
        cmd = None
    if cmd != None:
        if cmd["upvote_downvote"] == ["upvote"]:
            mongodb.posts.update_one(
                {"_id": ObjectId(postId)}, {"$inc": {"upvote": -1}}
            )
            mongodb.users.update_one(
                {"user_id": userID},
                {
                    "$pull": {
                        "list_of_post_voted": {
                            "id": postId,
                        }
                    }
                },
            )
            return "not upvote"
        else:
            mongodb.posts.update_one(
                {"_id": ObjectId(postId)}, {"$inc": {"upvote": 1, "downvote": -1}}
            )
            mongodb.users.update_one(
                {"user_id": userID, "list_of_post_voted.id": postId},
                {"$set": {"list_of_post_voted.0.upvote_downvote": "upvote"}},
            )
            return "upvote"
    else:
        mongodb.posts.update_one({"_id": ObjectId(postId)}, {"$inc": {"upvote": 1}})
        mongodb.users.update_one(
            {"user_id": userID},
            {
                "$addToSet": {
                    "list_of_post_voted": {"id": postId, "upvote_downvote": "upvote"}
                }
            },
        )
        return "upvote"


@router.put("/downvote/")
def downvote_User(postId: str, userID: str = Depends(authentication)):
    cmd = mongodb.users.find_one(
        {"user_id": userID, "list_of_post_voted.id": postId},
        {
            "upvote_downvote": "$list_of_post_voted.upvote_downvote",
            "id": "$list_of_post_voted.id",
        },
    )
    if cmd == 0:
        cmd = None
    if cmd != None:
        if cmd["upvote_downvote"] == ["downvote"]:
            mongodb.posts.update_one(
                {"_id": ObjectId(postId)}, {"$inc": {"downvote": -1}}
            )
            mongodb.users.update_one(
                {"user_id": userID}, {"$pull": {"list_of_post_voted": {"id": postId}}}
            )
            return "not downvote"
        else:
            mongodb.posts.update_one(
                {"_id": ObjectId(postId)}, {"$inc": {"upvote": -1, "downvote": 1}}
            )
            mongodb.users.update_one(
                {"user_id": userID, "list_of_post_voted.id": postId},
                {"$set": {"list_of_post_voted.0.upvote_downvote": "downvote"}},
            )
            return "downvote"
    else:
        mongodb.posts.update_one({"_id": ObjectId(postId)}, {"$inc": {"downvote": 1}})
        mongodb.users.update_one(
            {"user_id": userID},
            {
                "$addToSet": {
                    "list_of_post_voted": {"id": postId, "upvote_downvote": "downvote"}
                }
            },
        )
        return "downvote"


@router.post("/comments/create")
def create_comment(*, userID: str = Depends(authentication), comment: CommentDB):
    cmd = mongodb.posts.find_one({"_id": ObjectId(comment.post_id)})
    if cmd == None:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        comment.user_id = userID
        comment_dict = comment.dict()
        comment_dict["time_created"] = str(comment_dict["time_created"])
        current_comment = mongodb.comments.insert_one(comment_dict)
        mongodb.users.update_one(
            {"user_id": userID},
            {
                "$addToSet": {
                    "list_of_user_comments_id": str(current_comment.inserted_id)
                }
            },
        )
        mongodb.posts.update_one(
            {"_id": ObjectId(comment.post_id)}, {"$inc": {"num_comments": 1}}
        )
    return str(current_comment.inserted_id)


@router.put("/comment/{commentID}")
def change_comment(content: str, commentID: str):
    cmd = mongodb.comments.find_one({"_id": ObjectId(commentID)})
    if cmd == None:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        mongodb.comments.update_one(
            {"_id": ObjectId(commentID)}, {"$set": {"content": content}}
        )
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.delete("/comment/{commentID}")
def delete_comment(*, userID: str = Depends(authentication), commentID: str):
    pass


@router.put("/comment/upvote")
def upvote_comment(*, userID: str = Depends(authentication), commentID: str):
    cmd = mongodb.users.find_one(
        {"user_id": userID, "list_of_comment_voted.id": commentID},
        {
            "upvote_downvote": "$list_of_comment_voted.upvote_downvote",
            "id": "$list_of_comment_voted.id",
        },
    )
    if cmd == 0:
        cmd = None
    if cmd != None:
        if cmd["upvote_downvote"] == ["upvote"]:
            mongodb.comments.update_one(
                {"_id": ObjectId(commentID)}, {"$inc": {"upvote": -1}}
            )
            mongodb.users.update_one(
                {"user_id": userID},
                {
                    "$pull": {
                        "list_of_comment_voted": {
                            "id": commentID,
                        }
                    }
                },
            )
            return "not upvote"
        else:
            mongodb.comments.update_one(
                {"_id": ObjectId(commentID)}, {"$inc": {"upvote": 1, "downvote": -1}}
            )
            mongodb.users.update_one(
                {"user_id": userID, "list_of_comment_voted.id": commentID},
                {"$set": {"list_of_comment_voted.0.upvote_downvote": "upvote"}},
            )
        return "upvote"
    else:
        mongodb.comments.update_one(
            {"_id": ObjectId(commentID)}, {"$inc": {"upvote": 1}}
        )
        mongodb.users.update_one(
            {"user_id": userID},
            {
                "$addToSet": {
                    "list_of_comment_voted": {
                        "id": commentID,
                        "upvote_downvote": "upvote",
                    }
                }
            },
        )
        return "upvote"


@router.put("/comment/downvote")
def downvote_comment(*, userID: str = Depends(authentication), commentID: str):
    cmd = mongodb.users.find_one(
        {"user_id": userID, "list_of_comment_voted.id": commentID},
        {
            "upvote_downvote": "$list_of_comment_voted.upvote_downvote",
            "id": "$list_of_comment_voted.id",
        },
    )
    if cmd == 0:
        cmd = None
    if cmd != None:
        if cmd["upvote_downvote"] == ["downvote"]:
            mongodb.comments.update_one(
                {"_id": ObjectId(commentID)}, {"$inc": {"downvote": -1}}
            )
            mongodb.users.update_one(
                {"user_id": userID},
                {
                    "$pull": {
                        "list_of_comment_voted": {
                            "id": commentID,
                        }
                    }
                },
            )
            return "not downvote"
        else:
            mongodb.comments.update_one(
                {"_id": ObjectId(commentID)}, {"$inc": {"upvote": -1, "downvote": 1}}
            )
            mongodb.users.update_one(
                {"user_id": userID, "list_of_comment_voted.id": commentID},
                {"$set": {"list_of_comment_voted.0.upvote_downvote": "downvote"}},
            )
        return "downvote"
    else:
        mongodb.comments.update_one(
            {"_id": ObjectId(commentID)}, {"$inc": {"downvote": 1}}
        )
        mongodb.users.update_one(
            {"user_id": userID},
            {
                "$addToSet": {
                    "list_of_comment_voted": {
                        "id": commentID,
                        "upvote_downvote": "downvote",
                    }
                }
            },
        )
        return "downvote"


# Will have a meeting for the input of this endpoint
@router.post("/comments/reply")
def reply_comment(
    *,
    userID: str = Depends(authentication),
    parentCommentID: str,
    replyComment: CommentDB
):
    cmd = mongodb.comments.find_one({"_id": ObjectId(parentCommentID)})
    if cmd is None:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        root_id = parentCommentID
        if not cmd["root_comment_id"] == "root":
            root_id = cmd["root_comment_id"]
        replyComment.user_id = userID
        replyComment.root_comment_id = root_id
        comment_dict = replyComment.dict()
        comment_dict["time_created"] = str(comment_dict["time_created"])
        current_comment = mongodb.comments.insert_one(comment_dict)
        mongodb.users.update_one(
            {"user_id": userID},
            {
                "$addToSet": {
                    "list_of_user_comments_id": str(current_comment.inserted_id)
                }
            },
        )
        mongodb.comments.update_one(
            {"_id": ObjectId(root_id)},
            {"$addToSet": {"list_child_comment_id": str(current_comment.inserted_id)}},
        )
        mongodb.posts.update_one(
            {"_id": ObjectId(replyComment.post_id)}, {"$inc": {"num_comments": 1}}
        )
    return str(current_comment.inserted_id)


@router.put("/update/")
def user_update(*, userID=Depends(authentication), user: User):
    mongodb.users.update_one(
        {"user_id": userID},
        {
            "$set": {
                "avatar": user.avatar,
                "about_me": user.about_me,
                "location": user.location,
                "title": user.title,
            }
        },
    )
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.put("/bookmark/{postID}")
async def save_book_mark(*, userID=Depends(authentication), postID: str):
    try:
        bookmark = mongodb.users.find_one({"user_id": userID, "bookmark.id": postID})
        post = mongodb.posts.find_one({"_id": ObjectId(postID)})
        if bookmark == None:
            mongodb.users.update_one(
                {"user_id": userID},
                {"$addToSet": {"bookmark": {"id": postID, "title": post["title"]}}},
            )
        else:
            mongodb.users.update_one(
                {"user_id": userID}, {"$pull": {"bookmark": {"id": postID}}}
            )
    except:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.delete("/delete/all")
async def delete_all_users():
    mongodb.users.delete_many({})


@router.delete("/delete/comments/all")
async def delete_all_comments():
    mongodb.comments.delete_many({})
