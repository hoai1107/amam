from fastapi.security import OAuth2PasswordBearer
from fastapi import Query
import sys
import os
from pathlib import Path
sys.path.insert(0,os.path.join(Path(__file__).parents[0],"router"))
from constant import shard_number
import random
from google.cloud import firestore

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
    query_title_pattern = "(.)*"
    for word in word_arr:
        query_title_pattern += word + "(.)*|"
    return query_title_pattern

