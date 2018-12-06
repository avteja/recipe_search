# with open(recipe_csv_file) as f:
#     cnt = 0
#     n = 0
#     for row in f.readlines():
#         vals = row.strip().split(',')
#         # print (vals)
#         if cnt == 0:
#             # pprint (vals)
#             keyword_dict = {}
#             for k in vals:
#                 keyword_dict[k] = 0
#             keys = vals[6: ]
#             n = len(keys)
#             pprint (keys)
#         else:
#             cnt = 0
#             for i in range(len(vals)):
#                 s = re.sub('[^A-Za-z0-9]+', '', vals[i])
#                 # print (s)
#                 if s.isalnum() and s.isnumeric():
#                     break
#                 cnt += 1
#             final = vals[cnt: ]
#             m = len(final)
#             for i in range(5, m):
#                 # try:
#                 keyword_dict[keys[i-5]] += int(float(final[i]))
#                 # except:
#                 #     print (vals)
#                 #     print (vals[0])
#                 #     print (vals[i])
#                 #     exit()
#         cnt += 1
#     for i in range(n):
#         print (keys[i], keyword_dict[keys[i]])

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
index_path = '../index_facet'

with open(recipe_json_file) as f:
    recipe_data = json.load(f)

pprint (recipe_data[0])

# Setup Schema
class RecipeSchema(SchemaClass):
    title = TEXT(stored = True)
    directions = TEXT(stored = True)
    ingredients = TEXT(stored = True)
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
    # print (recipe['calories'])
    if 'calories' in recipe and recipe['calories'] is not None and float(recipe['calories']) <= 800:
        u_calories = float(recipe['calories'])
    else:
        u_calories = None
    writer.add_document(title = u_title, directions = u_directions, ingredients = u_ingredients, categories = u_categories, calories = u_calories)
    ix_cnt += 1
writer.commit()
print ('Indexed', ix_cnt, 'recipes')
