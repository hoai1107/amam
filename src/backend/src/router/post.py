from fastapi import APIRouter, Response, status
from ..database_connection.test_firebase_connection import db
from ..data_model.model import Post

router = APIRouter(
    prefix= "/posts",
    tags= ["Posts"]
)

@router.get("/post_info/{post_id}", response_model=Post)
async def get_post_info(post_id: str):
    try:
        current_post = db.child("posts").child(post_id).get().val()
        post_info_model = Post(**(current_post))
        post_info_model.id = post_id
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST)
    return post_info_model
    

# put the post information and get the id of that post
@router.put("/post_info")
async def post_post_info(post: Post):
    try:
        post_dict = post.dict()
        del post_dict["id"]
        post_dict["time_create"] = str(post_dict["time_create"])
        current_post = db.child("posts").push(post_dict)
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST)
    return current_post["name"]
    