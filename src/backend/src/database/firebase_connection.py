import collections 
import sys
if sys.version_info.major == 3 and sys.version_info.minor >= 10:

    from collections.abc import MutableMapping
else:
    from collections import MutableMapping
from firebase_admin import credentials
from firebase_admin import auth
import firebase_admin
#cred = credentials.RefreshToken('cs300-project-firebase-adminsdk-z5mzh-43da7b3a43.json')
#default_app = firebase_admin.initialize_app(cred)
#default_app = firebase_admin.initialize_app(cred)
default_app = firebase_admin.initialize_app()
print(default_app.name)