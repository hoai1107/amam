from fastapi import APIRouter, Response, status, Path, Query, Depends
import sys,os
from pathlib import Path
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"database_connection"))
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"data_model"))
sys.path.insert(0,os.path.join(Path(__file__).parents[1],""))
from db_connection import mongodb
from post_model import FullPost, PostDB, ShortPost, ObjectId, SearchFilter, OrderByOption
from constant import pagination_number
from dependencies import search_query_processing

router = APIRouter(
    prefix= "/posts",
    tags= ["Posts"]
)

# This is to get all information related to a specific post
# Remember to add the query to retrieve the avatar from the userid gotten from the db 
# This lateness is due to the lack of user model on Mongo DB
@router.get("/{post_id}/", response_model=FullPost)
async def get_post(
        post_id: str = Path(title="The ID to get the post detailed information")
    ):
    try:
        current_post = mongodb.posts.find_one({"_id":ObjectId(post_id)})
        post_info_model = FullPost(**(current_post))
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST)
    return post_info_model

@router.get("/all")
async def get_posts_on_homepage(
        page_index : int = Query(title="The page index in the homepage", default=1),
        order_by_option: OrderByOption = Query(title= "The option that users use to sort the result", default=OrderByOption.default),
        filter: list[SearchFilter] = Query(title="The tags to filter the searched posts", default= [SearchFilter.all])
    ):
    count = 0 
    if filter == ["all"]:
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
                                "$in": filter
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
        count = mongodb.posts.count_documents(filter={"tags": {"$in": filter}})
    res = list[ShortPost]()
    for doc in list_of_full_posts:
        res.append(ShortPost(**doc))
    if order_by_option.value == OrderByOption.comment:
        res.sort(key= lambda x: x.num_comments, reverse=True)
    elif order_by_option.value ==  OrderByOption.view:
        res.sort(key= lambda x: x.view, reverse= True)
    elif order_by_option.value == OrderByOption.vote:
        res.sort(key= lambda x: x.up_vote + x.down_vote, reverse= True)
    return {"data":res, "total": count}

# this is to search the post
@router.get("/search")
async def get_searched_posts(
        query_title_pattern: str = Depends(search_query_processing),
        filter: list[SearchFilter] = Query(title="The tags to filter the searched posts", default= [SearchFilter.all]),
        page_index : int = Query(title="The page index in the homepage", default=1),
        order_by_option: OrderByOption = Query(title= "The option that users use to sort the result", default=OrderByOption.default)
    ):
    count = 0
    if filter == ["all"]:
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
                            "$in": filter
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
                        "$in": filter
                    },
                "title":
                    {
                        "$regex":query_title_pattern,
                        "$options":"i"
                    }
            })
    res = list[ShortPost]()
    for doc in list_of_full_posts:
        res.append(ShortPost(**doc))
    if order_by_option.value == OrderByOption.comment:
        res.sort(key= lambda x: x.num_comments, reverse=True)
    elif order_by_option.value ==  OrderByOption.view:
        res.sort(key= lambda x: x.view, reverse= True)
    elif order_by_option.value == OrderByOption.vote:
        res.sort(key= lambda x: x.up_vote + x.down_vote, reverse= True)
    return {"data":res, "total": count}

# This is to create the a post information (and get the ID of the post)
@router.post("/create")
async def create_post(post: PostDB):
    try:
        post_dict = post.dict()
        post_dict["time_created"] = str(post_dict["time_created"])
        current_post = mongodb["posts"].insert_one(post_dict)
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST)    
    return str(current_post.inserted_id)

@router.delete("/delete/all")
async def delete_all_posts():
    mongodb.posts.delete_many({})