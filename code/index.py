import json
from pprint import pprint
import os.path
import sys

from whoosh.analysis import StandardAnalyzer, StemFilter
from whoosh.fields import *
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

from CustomTokenizer import CustomTokenizer
from CustomFilter import CustomFilter

recipe_json_file = '../data/epicurious/full_format_recipes.json'
index_path = '../index'

with open(recipe_json_file) as f:
    recipe_data = json.load(f)

pprint (recipe_data[0])

# Setup Schema
class RecipeSchema(SchemaClass):
    title = TEXT(stored = True, multitoken_query = 'or', analyzer = StandardAnalyzer() | StemFilter() | CustomFilter())
    directions = TEXT(stored = True, multitoken_query = 'or', analyzer = StandardAnalyzer() | StemFilter() | CustomFilter())
    ingredients = TEXT(stored = True, multitoken_query = 'or', analyzer = StandardAnalyzer() | StemFilter() | CustomFilter())
    categories = KEYWORD(stored = True, commas = True)
    calories = NUMERIC(stored = True)

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
    if ix_cnt % 1000 == 0:
        print ('Indexed {} recipes'.format(ix_cnt))
    # print (recipe['directions'])
    u_title = recipe['title']
    u_directions = ' '.join(recipe['directions'])
    u_ingredients = ' '.join(recipe['ingredients'])
    u_categories = ','.join(recipe['categories']).lower()
    if 'calories' in recipe and recipe['calories'] is not None and float(recipe['calories']) <= 800:
        u_calories = float(recipe['calories'])
    else:
        u_calories = None
    writer.add_document(title = u_title, directions = u_directions, ingredients = u_ingredients, categories = u_categories, calories = u_calories)
    ix_cnt += 1
writer.commit()
print ('Indexed', ix_cnt, 'recipes')
