from fastapi import APIRouter, Response, status, Path, Query, Depends
import sys,os
from pathlib import Path
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"database_connection"))
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"data_model"))
sys.path.insert(0,os.path.join(Path(__file__).parents[1],""))
from db_connection import mongodb, client, read_concern, WriteConcern
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
    with client.start_session() as session:
        with session.start_transaction(read_concern=read_concern.ReadConcern("majority")):
            try:
                current_post = mongodb.posts.find_one({"_id":ObjectId(post_id)},session=session)
                current_user = mongodb.users.find_one({"user_id": current_post["user_id"]})
                post_info_model = Posts(**(current_post))
                post_info_model.id = str(post_info_model.id)
                post_info_model = post_info_model.dict()
                post_info_model["user_name"] = current_user["user_name"]
                post_info_model["avatar"] = current_user["avatar"]
                current_comments= mongodb.comments.find({"post_id": post_id, "root_comment_id": "root"},session=session)
                comment_list = list[Comments]()
                for cmt in current_comments:
                    commentbase_list = list[CommentBase]()
                    for child_cmt_id in cmt["list_child_comment_id"]:
                        child_comment = mongodb.comments.find_one({"_id": ObjectId(child_cmt_id)},session=session)
                        child_user = mongodb.users.find_one({"user_id": child_comment["user_id"]},session=session)
                        commentbase_list.append(CommentBase(**child_comment,user_name=child_user["user_name"],user_avatar=child_user["avatar"])) 
                    parrent_user = mongodb.users.find_one({"user_id": cmt["user_id"]},session=session)
                    comment_list.append(Comments(**cmt,user_name=parrent_user["user_name"],user_avatar=parrent_user["avatar"], list_child_comment= commentbase_list))
            except:
                session.abort_transaction()
                return Response(status_code= status.HTTP_400_BAD_REQUEST)
    return {"Post Section":post_info_model, "Comment Section": comment_list}

@router.put("/{post_id}/view")
async def update_post_view(*,userID: str = Depends(authentication),post_id:str):
    with client.start_session() as session:
        with session.start_transaction(read_concern=read_concern.ReadConcern("majority"),write_concern=WriteConcern("majority")):
            try:
                post = mongodb.posts.find_one({"_id": ObjectId(post_id),"list_user_view_id": userID},session=session)
                if post == None:
                    mongodb.posts.update_one({"_id": ObjectId(post_id)},{"$inc":{"view":1},"$push":{"list_user_view_id": userID}},upsert=False,session=session)
                    post = mongodb.posts.find_one({"_id": ObjectId(post_id)},session=session)
                user_history_post = mongodb.users.find_one({"user_id": userID,"history_posts.id":post_id},session=session)
                if user_history_post != None:
                    mongodb.users.update_one({"user_id":userID},
                        {
                           "$pull": {"history_posts": {"id": post_id}}
                        },
                    upsert=False,
                    session=session)
                    mongodb.users.update_one({"user_id": userID},
                        {"$push":
                                {"history_posts":
                                    {
                                    "id": post_id,
                                    "title": post["title"]
                                    }
                                }
                        },
                    upsert=False,
                    session=session)
                else:
                    user_history_post = mongodb.users.find_one({"user_id":userID},session=session)
                    history_post_size = len(user_history_post["history_posts"])
                    if history_post_size == 30:
                        mongodb.users.update_one({"user_id":userID},
                            {
                                "$pop":{"history_posts": -1},
                                "$push":
                                    {
                                    "history_posts":{
                                        "id": post_id,
                                        "title": post["title"]
                                        }
                                    }
                            },
                        upsert=False,
                        session=session)
                    else:
                        mongodb.users.update_one({"user_id":userID},
                            {
                            "$push":{
                                "history_posts":{
                                    "id": post_id,
                                    "title": post["title"]
                                    }
                                }
                            },
                        session=session)
                session.commit_transaction()
            except:
                session.abort_transaction()
                return Response(status_code= status.HTTP_400_BAD_REQUEST)
    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.get("/all")
async def get_posts_on_homepage(
        page_index : int = Query(title="The page index in the homepage", default=1),
        order_by_option: OrderByOption = Query(title= "The option that users use to sort the result", default=OrderByOption.default),
        category: list[SearchFilter] = Query(title="The tags to filter the searched posts", default= [SearchFilter.all])
    ):
    count = 0 
    if category == ["All"]:
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
    if category == ["All"]:
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
    with client.start_session() as session:
        with session.start_transaction(write_concern=WriteConcern("majority")):
            try:
                post.user_id = userID
                post_dict = post.dict()
                post_dict["time_created"] = str(post_dict["time_created"])
                current_post = mongodb["posts"].insert_one(post_dict,session=session)
                mongodb.users.update_one({"user_id": post.user_id},{"$addToSet":{"list_of_user_question":{
                            "id": str(current_post.inserted_id),
                            "title": post.title
                        }
                    }
                },session=session)
                session.commit_transaction()
            except:
                session.abort_transaction()
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