from pprint import pprint
import os.path
import sys

from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser

from whoosh import columns, fields, index, sorting

from CustomQueryParser import CustomQueryParser

index_path = '../index_facet'

# Index object
ix = None
if os.path.exists(index_path):
    ix = open_dir(index_path)
else:
    print ('No index found at given path')

parser = QueryParser("directions", ix.schema)
# parser = QueryParser("directions", ix.schema)
with ix.searcher() as searcher:
    # print (list(searcher.lexicon('directions')))
    while True:
        print ('Enter query string:', )
        query_str = input()
        parsed_query = parser.parse(query_str)
        print (parsed_query)
        # results = searcher.search(parsed_query, limit = 10)

        caloriesFacet = sorting.RangeFacet("calories", 0, 1000, 200)
        categoriesFacet = sorting.FieldFacet("categories", allow_overlap = True)
        mf = sorting.MultiFacet([caloriesFacet, categoriesFacet])
        results = searcher.search(parsed_query, groupedby = mf)
        print (len(results))
        
        groups = results.groups()
        # print (groups.keys())
        
        total_num_docs = 0
        for key in groups.keys():
            total_num_docs += len(groups[key])
        print (total_num_docs)

        key = ((200, 400), 'Dinner')    
        doclist = groups[key]
        print (doclist)
        for docnum in doclist[: 5]:
            print ("  ", searcher.stored_fields(docnum))
        
        # if len(results) > 0:
            # print (results[0])
            # print (results[1])
            # print (results[2])
        # else:
        #     print ('No results found')
        # print (results.key_terms("ingredients"))

