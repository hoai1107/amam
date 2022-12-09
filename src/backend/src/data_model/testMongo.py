import sys
import os
from bson import ObjectId
from pathlib import Path
sys.path.insert(0,os.path.join(Path(__file__).parents[1],'database_connection'))
from db_connection import mongodb
#c=mongodb.posts.find({ '_id': ObjectId("638ae63335e7efcac19700d1")})
def getUserInfo(userId: str):
    c=mongodb.users.find({'_id':ObjectId(userId)})
    temp=dict()
    for i in c:
        temp=i
    
getUserInfo('6392b4dc01fb6cbf7038c208')