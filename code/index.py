import json
from pprint import pprint
import os.path
import sys

from whoosh.fields import *
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

recipe_json_file = '../data/epicurious/full_format_recipes.json'
index_path = '../index'

with open(recipe_json_file) as f:
    recipe_data = json.load(f)

pprint (recipe_data[0])

# Setup Schema
class RecipeSchema(SchemaClass):
    title = TEXT(stored = True)
    directions = TEXT(stored = True)
    ingredients = TEXT(stored = True)
    categories = KEYWORD(stored = True, commas = True)

# print ('Found', len(recipe_data), 'recipes')

ix = None
if not os.path.exists(index_path):
    os.mkdir(index_path)
else:
    ix = open_dir(index_path)

ix = create_in(index_path, RecipeSchema)
ix_cnt = 0
print ('Indexing....')
writer = ix.writer()
for recipe in recipe_data:
    if not recipe:
        continue
    # print (recipe['directions'])
    u_title = recipe['title']
    u_directions = ' '.join(recipe['directions'])
    u_ingredients = ' '.join(recipe['ingredients'])
    u_categories = ','.join(recipe['categories'])
    writer.add_document(title = u_title, directions = u_directions, ingredients = u_ingredients, categories = u_categories)
    ix_cnt += 1
writer.commit()
print ('Indexed', ix_cnt, 'recipes')
