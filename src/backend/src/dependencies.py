from fastapi.security import OAuth2PasswordBearer
from fastapi import Query
from .router.constant import shard_number
import random
from google.cloud import firestore

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "Authentication")

class Shard(object):
    """
    A shard is a distributed counter. Each shard can support being incremented
    once per second. Multiple shards are needed within a Counter to allow
    more frequent incrementing.
    """
    def __init__(self) -> None:
        self.count = 0
    
    def to_dict(self):
        return {"count": self.count}

class Counter(object):
    """
    A counter stores a collection of shards which are
    summed to return a total count. This allows for more
    frequent incrementing than a single document.
    """
    def __init__(self, count_doc) -> None:
        self.num_shards = shard_number
        self.count_doc = count_doc

    def init_counter(self):
        shard_col = self.count_doc.collection("shards")
        # Initialize each shard with count=0
        for num in range(self.num_shards):
            shard = Shard()
            shard_col.document(str(num)).set(shard.to_dict())
    
    def increment_counter(self):
        doc_shard_id = random.randint(0, self.num_shards - 1)
        shard_doc = self.count_doc.collection("shards").document(str(doc_shard_id))
        return shard_doc.update({"count": firestore.Increment(1)})
    
    def get_count(self):
        """Return a total count across all shards."""
        total = 0
        shards = self.count_doc.collection("shards").list_documents()
        for shard in shards:
            total += (shard.get()).to_dict().get("count", 0)
        return total      


async def search_query_processing(
    query_title: str = Query(title="The query for the title of the post", default="")
):
    word_arr = query_title.split(" ")
    query_title_pattern = "(.)*"
    for word in word_arr:
        query_title_pattern += word + "(.)*|"
    return query_title_pattern

