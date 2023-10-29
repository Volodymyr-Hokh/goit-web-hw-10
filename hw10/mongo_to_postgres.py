import configparser
import os
import re
import urllib.parse

import django
from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw10.settings")
django.setup()

from quotes.models import Author, Quote, Tag


config = configparser.ConfigParser()
r = config.read('mongo_config.ini')

mongo_user = urllib.parse.quote_plus(config.get('DB', 'user'))
mongodb_pass = urllib.parse.quote_plus(config.get('DB', 'pass'))
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

client = MongoClient(
    f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""")
db = client['quotes']

 
def seed_data():
    for author_data in db['author'].find():
        Author.objects.get_or_create(
            fullname=author_data['fullname'],
            born_date=author_data.get('born_date'),
            born_location=author_data.get('born_location'),
            description=author_data.get('description'),
            )

    for quote_data in db['quote'].find():
        tags = []
        for tag in quote_data['tags']:
            t = Tag.objects.get_or_create(name=tag)[0]
            tags.append(t)



        exist_quote = bool(len(Quote.objects.filter(quote=quote_data["quote"])))

        if not exist_quote:
            author_from_mongo = db['author'].find_one({"_id": quote_data['author']})
            author_fullname = author_from_mongo["fullname"]
            author = Author.objects.get(fullname=author_fullname)
            quote = Quote.objects.create(author=author, quote=quote_data['quote'])
            for tag in tags:
                quote.tags.add(tag)


if __name__ == "__main__":
    seed_data()

