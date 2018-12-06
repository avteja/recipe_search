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

        caloriesFacet = sorting.RangeFacet("calories", 0, 800, 200)
        categoriesFacet = sorting.FieldFacet("categories", allow_overlap = True)
        # mf = sorting.MultiFacet([caloriesFacet, categoriesFacet])
        # results = searcher.search(parsed_query, groupedby = mf)
        results_cats = searcher.search(parsed_query, groupedby = categoriesFacet)
        results_cals = searcher.search(parsed_query, groupedby = caloriesFacet)
        print (len(results))
        # print (results)
        
        groups_cats = results_cats.groups()
        groups_cals = results_cals.groups()
        # print (groups.keys())
        
        total_num_docs = 0
        for key in groups_cals.keys():
            # print (key)
            total_num_docs += len(groups[key])
            # print (len(groups[key]))
        print (total_num_docs)

        doc_set = set()
        cnt = 0
        for cat in ['dinner', '22-minute meals']:
            doclist = groups[cat]
            print (len(doclist))
            if cnt == 0:
                for docnum in doclist:
                    doc_set.add(docnum)
            else:
                temp_set = set()
                for docnum in doclist:
                    temp_set.add(docnum)
                # print (temp_set)
                doc_set = doc_set.intersection(temp_set)
            cnt += 1
            # print (doc_set)
            print ('{} Doclist: {}'.format(cat, doclist))
        doclist = list(doc_set)
        print ('Final doclist:', doclist)
        # for key in groups.keys():
        #     if key[1] == 'dinner':
        #         print (key)
        #         print (groups[key])
        # print (groups.keys())

        # cat = 'dinner'
        # key = (None, cat)
        # doclist = groups[key]
        # print (doclist)
        # for i in range(4):
        #     cal = (200*i, 200*(i+1))
        #     key = (cal, cat)
        #     print (key)
        #     if key in groups.keys():
        #         print (groups[key])
        #         doclist += groups[key]

        # print (len(doclist))
        # for docnum in doclist[: 5]:
            # print ("  ", searcher.stored_fields(docnum))
        
        # if len(results) > 0:
            # print (results[0])
            # print (results[1])
            # print (results[2])
        # else:
        #     print ('No results found')
        # print (results.key_terms("ingredients"))

