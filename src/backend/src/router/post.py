from fastapi import APIRouter, Response, status, Path, Query
from ..database_connection.test_firebase_connection import db, storage
from ..data_model.post_model import Post, ShortPost
from .constant import pagination_number

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
        current_post = db.child("posts").child(post_id).get().val()
        post_info_model = Post(**(current_post))
        post_info_model.id = post_id
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST)
    return post_info_model

# this is to get the list of all posts on homepage
@router.get("/post_all/{page_index}", response_model= list[ShortPost])
async def get_posts_on_homepage(
        page_index : int = Path(title="The page index in the homepage", default=1)
    ):
    list_of_full_posts = db.child("posts").order_by_key().limit_to_last(page_index*pagination_number).get().val()
    list_of_short_posts = list[ShortPost]()
    list_of_full_posts = list(list_of_full_posts.items())
    for i in range((page_index-1)*pagination_number,len(list_of_full_posts)):
        key = list_of_full_posts[i][0]
        value = list_of_full_posts[i][1]
        value["num_comments"] = len(value["comments"])
        list_of_short_posts.append(ShortPost(id= key,**(value)))
    return list_of_short_posts

# this is to search the post
@router.put("/search_post/{query_title}/{page_index}")
async def get_searched_posts(
        query_title: str = Path(title="The query for the title of the post", default=""),
        filter: list[str] = Query(title="The tags to filter the searched posts", default= ["all"]),
        page_index : int = Path(title="The page index in the homepage", default=1)
    ):
    list_of_full_matched_posts = db.child("posts").order_by_child("title",).equal_to(query_title).get().val()
    list_of_short_posts = list[ShortPost]()
    for key, value in list_of_full_matched_posts.items():
        if set(value["tags"]) == set(filter):
            value["num_comments"] = len(value["comments"])
            list_of_short_posts.append(ShortPost(id= key,**(value)))
    return list_of_short_posts[(page_index-1)*pagination_number:page_index*pagination_number]

# This is to create the a post information (and get the ID of the post)
@router.put("/create_post")
async def create_post(post: Post):
    post_dict = post.dict()
    del post_dict["id"]
    post_dict["time_created"] = str(post_dict["time_created"])
    current_post = db.child("posts").push(post_dict)
    return current_post["name"]

