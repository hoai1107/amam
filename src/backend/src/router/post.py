from fastapi import APIRouter, Response, status, Path, Query, Depends
import sys,os
from pathlib import Path
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"database_connection"))
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"data_model"))
sys.path.insert(0,os.path.join(Path(__file__).parents[1],""))
from db_connection import mongodb
from post_model import Posts, PostDB, ObjectId, SearchFilter, OrderByOption, Comments, CommentBase
from constant import pagination_number
from dependencies import search_query_processing
from authentication import authentication

router = APIRouter(
    prefix= "/posts",
    tags= ["Posts"]
)

# This is to get all information related to a specific post
# Remember to add the query to retrieve the avatar from the userid gotten from the db 
# This lateness is due to the lack of user model on Mongo DB
@router.get("/{post_id}/")
async def get_post(
        post_id: str = Path(title="The ID to get the post detailed information")
    ):
    try:
        current_post = mongodb.posts.find_one({"_id":ObjectId(post_id)})
        post_info_model = Posts (**(current_post))
        current_comments= mongodb.comments.find({"post_id": post_id, "root_comment_id": "root"})
        comment_list = list[Comments]()
        for cmt in current_comments:
            commentbase_list = list[CommentBase]()
            for child_cmt_id in cmt["list_child_comment_id"]:
                child_comment = mongodb.comments.find_one({"_id": ObjectId(child_cmt_id)})
                child_user = mongodb.users.find_one({"user_id": child_comment["user_id"]})
                commentbase_list.append(CommentBase(**child_comment,user_name=child_user["user_name"],user_avatar=child_user["avatar"])) 
            parrent_user = mongodb.users.find_one({"user_id": cmt["user_id"]})
            comment_list.append(Comments(**cmt,user_name=parrent_user["user_name"],user_avatar=parrent_user["avatar"], list_child_comment= commentbase_list))
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST)
    return {"Post Section":post_info_model, "Comment Section": comment_list}

@router.get("/all")
async def get_posts_on_homepage(
        page_index : int = Query(title="The page index in the homepage", default=1),
        order_by_option: OrderByOption = Query(title= "The option that users use to sort the result", default=OrderByOption.default),
        category: list[SearchFilter] = Query(title="The tags to filter the searched posts", default= [SearchFilter.all])
    ):
    count = 0 
    if category == ["all"]:
        list_of_full_posts = mongodb.posts.aggregate([
            {"$sort":
                    {
                        "_id":-1
                    }
            },
            {
                "$skip": (page_index - 1)*pagination_number
            },
            {
                "$limit": pagination_number
            }
        ])
        count = mongodb.posts.count_documents(filter={})
    else:
        list_of_full_posts = mongodb.posts.aggregate([
            {"$match":
                    {
                        "tags":
                            {
                                "$in": category
                            }
                    }
            },
            {"$sort":
                    {
                        "_id":-1
                    }
            },
            {
                "$skip":(page_index - 1)*pagination_number
            },
            {
                "$limit": pagination_number
            }
        ])
        count = mongodb.posts.count_documents(filter={"tags": {"$in": category}})
    res = list[Posts]()
    for doc in list_of_full_posts:
        res.append(Posts(**doc))
    if order_by_option.value == OrderByOption.comment:
        res.sort(key= lambda x: x.num_comments, reverse=True)
    elif order_by_option.value ==  OrderByOption.view:
        res.sort(key= lambda x: x.view, reverse= True)
    elif order_by_option.value == OrderByOption.vote:
        res.sort(key= lambda x: x.upvote + x.downvote, reverse= True)
    return {"data":res, "total": count}

# this is to search the post
@router.get("/search")
async def get_searched_posts(
        query_title_pattern: str = Depends(search_query_processing),
        category: list[SearchFilter] = Query(title="The tags to filter the searched posts", default= [SearchFilter.all]),
        page_index : int = Query(title="The page index in the homepage", default=1),
        order_by_option: OrderByOption = Query(title= "The option that users use to sort the result", default=OrderByOption.default)
    ):
    count = 0
    if category == ["all"]:
        list_of_full_posts = mongodb.posts.aggregate([
            {"$match":
                {"title":
                        {
                            "$regex": query_title_pattern,
                            "$options": 'i'
                        }
                }
            },
            {"$sort":
                {
                    "_id":-1
                }
            },
            {
                "$skip": (page_index - 1)*pagination_number
            },
            {
                "$limit": pagination_number
            }
        ])
        count = mongodb.posts.count_documents(filter =
                {"title":
                    {
                        "$regex":query_title_pattern,
                        "$options":"i"
                    }
                })
    else:
        list_of_full_posts = mongodb.posts.aggregate([
            {"$match":
                {
                    "tags":
                        {
                            "$in": category
                        },
                    "title":
                        { 
                            
                            "$regex":query_title_pattern,
                            "$options":'i'
                            
                        }
                }
            },
            {"$sort":
                {
                    "_id":-1
                }
            },
            {
                "$skip":(page_index - 1)*pagination_number
            },
            {
                "$limit": pagination_number
            }
        ])
        count = mongodb.posts.count_documents(filter =
            {
                "tags":
                    {
                        "$in": category
                    },
                "title":
                    {
                        "$regex":query_title_pattern,
                        "$options":"i"
                    }
            })
    res = list[Posts]()
    for doc in list_of_full_posts:
        res.append(Posts(**doc))
    if order_by_option.value == OrderByOption.comment:
        res.sort(key= lambda x: x.num_comments, reverse=True)
    elif order_by_option.value ==  OrderByOption.view:
        res.sort(key= lambda x: x.view, reverse= True)
    elif order_by_option.value == OrderByOption.vote:
        res.sort(key= lambda x: x.upvote + x.downvote, reverse= True)
    return {"data":res, "total": count}

# This is to create the a post information (and get the ID of the post)
@router.post("/create")
async def create_post(*,userID: str = Depends(authentication),post: PostDB):
    try:
        post.user_id = userID
        post_dict = post.dict()
        post_dict["time_created"] = str(post_dict["time_created"])
        current_post = mongodb["posts"].insert_one(post_dict)
        mongodb.users.update_one({"user_id": post.user_id},{"$addToSet":{"list_of_user_question":{
                    "id": str(current_post.inserted_id),
                    "title": post.title
                }
            }
        })
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST)    
    return str(current_post.inserted_id)

@router.delete("/delete/all")
async def delete_all_posts():
    mongodb.posts.delete_many({})

@router.get("/test_performance")
async def test_performance():
    return str(mongodb.comments.find({"post_id": "63a3342822a64b9794026112", "root_comment_id": "root"}).explain())

@router.get("/test/mongo")
async def test_mongo():
    data = {"_id": 2}
    user = mongodb.users.insert_one(data)
    return user.inserted_id