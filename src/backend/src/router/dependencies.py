from fastapi.security import OAuth2PasswordBearer
from fastapi import Query, Response, status
import sys
import os
from pathlib import Path
from db_connection import mongodb, client_session, read_concern, WriteConcern
from bson import ObjectId
sys.path.insert(0,os.path.join(Path(__file__).parents[0],"router"))

"""
In fact, tokenUrl merely does have a meaning for the fastapi documentation
For example you have async def test_authentication(token: str = Depends(oauth2_scheme)):
pass
@router.get("/test_authentication")
async def test(token: str = Depends(test_authentication)):
    return token 
In the documentation, that we have to click to authorize button. That authorize button use this url to create token for the whole
endpoints in that documentation
In fact, we just need to input the token for this and that's it.
oauth2_scheme is an instance of OAuth2PasswordBearer. Therefore, the above endpoint follows the bearer way for the authentication. 
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "authentication/sign-in")

async def search_query_processing(
    query_title: str = Query(title="The query for the title of the post", default="")
):
    word_arr = query_title.split(" ")
    query_title_pattern = ""
    for word in word_arr:
        query_title_pattern += " " + word + " " + "(.)*|"
        query_title_pattern += " " + word.capitalize() + " " + "(.)*|"
    return query_title_pattern[:-1]

"""
This is to recursively delete the comments... This process is wrapped into transactions during iterations within the recursion
About the isolation level, read uses serializable and write will use majority
majority ensure the consistency for the write thanks to the mechanism of MVCC in the WiredTiger storage engine of the current version of MongoDB
serializable for the read to avoid the case that transactions for deleting a comment and a replying comment happen concurrently
If it is, the num_comments in the post will decrease in the unexpected amount due to the effect of the majority write concern 
-> use serializable to ensure that the comment want to be deleted is available in this case.  
"""

async def recursive_remove_comment(commentID:str, session: client_session.ClientSession):
    with session.start_transaction(read_concern=read_concern.ReadConcern("serializable"),write_concern=WriteConcern("majority")):
        try:
            deleted_comment = mongodb.comments.find_one({"_id":commentID},session=session)
            mongodb.users.update_one({"user_id": deleted_comment["user_id"]},{"$pull": {"list_of_user_comments_id": commentID}},session=session)
            mongodb.posts.update_one({"_id": ObjectId(deleted_comment["post_id"])},{"$inc":{"num_comments":-1}},session=session)
            mongodb.comments.delete_one({"_id":commentID},session=session)
            session.commit_transaction()
            list_of_child_comment_id = deleted_comment["list"]
            for child_comment_id in list_of_child_comment_id:
                recursive_remove_comment(commentID=child_comment_id,session= session)
        except:
            session.abort_transaction()
            return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return Response(status_code=status.HTTP_202_ACCEPTED)