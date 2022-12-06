from fastapi import APIRouter, Response, status, Path, Query, Depends
from ..database_connection.test_firebase_connection import mongodb
from ..data_model.post_model import Post, ShortPost, ObjectId, SearchFilter, OrderByOption
from .constant import pagination_number
from ..dependencies import search_query_processing

router = APIRouter(
    prefix= "/posts",
    tags= ["Posts"]
)

# This is to get all information related to a specific post
@router.get("/post_detail/{post_id}", response_model=Post)
async def get_post(
        post_id: str = Path(title="The ID to get the post detailed information")
    ):
    try:
        current_post = mongodb.posts.find_one({"_id":ObjectId(post_id)})
        post_info_model = Post(**(current_post))
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST)
    return post_info_model

# This is to get the number of documents available in the database
@router.get("/post_all/number_of_post")
async def number_of_post_homepage(
        filter: list[SearchFilter] = Query(title="The tags to filter the searched posts", default= [SearchFilter.all])
    ):
    if filter == ["all"]:
        return mongodb.posts.count_documents(filter={})
    else:
        return mongodb.posts.count_documents(filter={"tags": {"$in": filter}})

@router.get("/post_all/")
async def get_posts_on_homepage(
        page_index : int = Query(title="The page index in the homepage", default=1),
        order_by_option: OrderByOption = Query(title= "The option that users use to sort the result", default=OrderByOption.default),
        filter: list[SearchFilter] = Query(title="The tags to filter the searched posts", default= [SearchFilter.all])
    ):
    if filter == ["all"]:
        list_of_full_posts = mongodb.posts.aggregate([
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
    res = list[ShortPost]()
    for doc in list_of_full_posts:
        res.append(ShortPost(num_comments=len(doc["comments"]),**doc))
    if order_by_option.value == OrderByOption.comment:
        res.sort(key= lambda x: x.num_comments, reverse=True)
    elif order_by_option.value ==  OrderByOption.view:
        res.sort(key= lambda x: x.view, reverse= True)
    elif order_by_option.value == OrderByOption.vote:
        res.sort(key= lambda x: x.up_vote + x.down_vote, reverse= True)
    return res

@router.get("/search_post/number_of_post")
async def number_of_posts_queried(
    query_title_pattern: str = Depends(search_query_processing),
    filter: list[SearchFilter] = Query(title="The tags to filter the searched posts", default= [SearchFilter.all])
):
    if filter == ["all"]:
        return mongodb.posts.count_documents(filter={"title":{"$regex":query_title_pattern,"$options":"i"}})
    else:
        return mongodb.posts.count_documents(filter={"tags":{"$in": filter},"title":{"$regex":query_title_pattern,"$options":"i"}})

# this is to search the post
@router.put("/search_post/")
async def get_searched_posts(
        query_title_pattern: str = Depends(search_query_processing),
        filter: list[SearchFilter] = Query(title="The tags to filter the searched posts", default= [SearchFilter.all]),
        page_index : int = Query(title="The page index in the homepage", default=1),
        order_by_option: OrderByOption = Query(title= "The option that users use to sort the result", default=OrderByOption.default)
    ):
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
    res = list[ShortPost]()
    for doc in list_of_full_posts:
        res.append(ShortPost(num_comments=len(doc["comments"]),**doc))
    if order_by_option.value == OrderByOption.comment:
        res.sort(key= lambda x: x.num_comments, reverse=True)
    elif order_by_option.value ==  OrderByOption.view:
        res.sort(key= lambda x: x.view, reverse= True)
    elif order_by_option.value == OrderByOption.vote:
        res.sort(key= lambda x: x.up_vote + x.down_vote, reverse= True)
    return res

# This is to create the a post information (and get the ID of the post)
# Due to the possibility that adding a new pyndantic class (whose id field is gone) just to create
# a record in the database can tangle the code -> this class will kept Post class instance as the query para
# This won't affect anything (when frontend communicate with the backend, remember to exclude the ID field)
@router.put("/create_post")
async def create_post(post: Post):
        post_dict = post.dict()
        del post_dict["id"]
        post_dict["time_created"] = str(post_dict["time_created"])
        current_post = mongodb["posts"].insert_one(post_dict)
        return str(current_post.inserted_id)


    
    
    
    