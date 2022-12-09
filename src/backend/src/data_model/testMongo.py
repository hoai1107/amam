import sys
import os
from pathlib import Path
sys.path.insert(0,os.path.join(Path(__file__).parents[1],'database_connection'))
from db_connection import mongodb
#mongodb.get_collection()
