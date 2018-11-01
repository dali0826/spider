from mongoengine import *

class Movie(Document):
    name=StringField(max_length=512)
    star=StringField(max_length=512)
    release_time=StringField(max_length=155)
    score=StringField(max_length=32)