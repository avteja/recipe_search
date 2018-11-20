import json
from pprint import pprint
import os.path
import sys

from whoosh import qparser

# Assumes 4 indices are present:
# directions, title, ingredients, categories
class CustomQueryParser(object):
    def __init__(self, schema):
        self.schema = schema
        self.field_names = ["ingredients", "directions", "title", "categories"]
        self.field_boosts = {"ingredients": 1.0, "directions": 1.0, "title": 2.0, "categories": 1.0}
        self.parser = qparser.MultifieldParser(self.field_names, self.schema, self.field_boosts)

    def parse(self, query):
        return self.parser.parse(query)
