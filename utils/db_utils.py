from pymongo import MongoClient
client = MongoClient()
db = client['matches']
posts = db.posts

# for post in posts.find({'match_id': 3870838763}):
#     print(post['_id'])
#     print(post['match_id'])
