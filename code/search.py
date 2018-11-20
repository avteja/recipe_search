from pprint import pprint
import os.path
import sys

from whoosh.index import open_dir

from customQueryParser import *

index_path = '../index'

# Index object
ix = None
if os.path.exists(index_path):
    ix = open_dir(index_path)
else:
    print ('No index found at given path')

parser = CustomQueryParser(ix.schema)
with ix.searcher() as searcher:
    # print (list(searcher.lexicon('directions')))
    while True:
        print ('Enter query string:', )
        query_str = input()
        parsed_query = parser.parse(query_str)
        results = searcher.search(parsed_query, limit = 5)
        print (len(results))
        if len(results) > 0:
            print (results[0])
            # print (results[1])
            # print (results[2])
        else:
            print ('No results found')

