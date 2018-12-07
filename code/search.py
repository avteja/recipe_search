from pprint import pprint
import os.path
import sys

from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser

from whoosh import columns, fields, index, sorting

from CustomQueryParser import CustomQueryParser

index_path = '../index_test'

# Index object
ix = None
if os.path.exists(index_path):
    ix = open_dir(index_path)
else:
    print ('No index found at given path')

def parse_facets(query):
    calories = ['cal200', 'cal400', 'cal600', 'cal800']
    categories = ['breakfast', 'brunch', 'lunch', 'dinner', '22-minute meals', 'dairy free', 'peanut free', 'soy free', 'wheat/gluten-free', 'vegetarian']
    flag = -1
    for i in range(len(calories)):
        cal = calories[i]
        if query[cal][0] == 'true':
            flag = i
            break
    cals = None
    if flag != -1:
        cals = (200*i, 200*(i+1))

    facets = []
    for cat in categories:
        if query[cat][0] == 'true':
            facet = cat
            facets.append(facet)
            flag = 1

    if len(facets) == 0:
        facets = [None]

    return cals, facets, flag 

def search(query):
    query_str = query['text'][0]
    query_str = ' '.join(query_str.strip().split(','))
    parser = CustomQueryParser(ix.schema)
    with ix.searcher() as searcher:
        print (query_str)
        parsed_query = parser.parse(query_str)
        print (parsed_query)

        results = searcher.search(parsed_query)
        scores = {}

        caloriesFacet = sorting.RangeFacet("calories", 0, 800, 200)
        categoriesFacet = sorting.FieldFacet("categories", allow_overlap = True)
        # allFacets = sorting.MultiFacet([caloriesFacet, categoriesFacet])
        categories_results = searcher.search(parsed_query, groupedby = categoriesFacet)
        calories_results = searcher.search(parsed_query, groupedby = caloriesFacet)
        
        categories_groups = categories_results.groups()
        calories_groups = calories_results.groups()        

        calories_facets, categories_facets, flag = parse_facets(query)
        print (calories_facets, categories_facets, flag)
        print (len(results), len(calories_results), len(categories_results))
        
        all_res = []

        if flag != -1:
            for idx in range(len(categories_results)):
                docnum = categories_results.docnum(idx)
                score = categories_results.score(idx)
                scores[docnum] = score
                # print (idx, score)
            for idx in range(len(calories_results)):
                docnum = calories_results.docnum(idx)
                score = calories_results.score(idx)
                scores[docnum] = score
                # print (idx, score)


            res_facets = -1
            doc_set = set()
            cnt = 0
            if categories_facets[0]:
                for cat in categories_facets:
                    doclist = categories_groups[cat]
                    if cnt == 0:
                        for docnum in doclist:
                            doc_set.add(docnum)
                    else:
                        temp_set = set()
                        for docnum in doclist:
                            temp_set.add(docnum)
                        doc_set = doc_set.intersection(temp_set)
                    cnt += 1
                    # print ('{} Doclist: {}'.format(cat, doclist))

                categories_doclist = list(doc_set)
                print ('Categories doclist length:', len(categories_doclist))

            if calories_facets:
                doclist = calories_groups[calories_facets]
                temp_set = set()
                for docnum in doclist:
                    temp_set.add(docnum)
                if categories_facets[0]:
                    doc_set = doc_set.intersection(temp_set)
                else:
                    doc_set = temp_set

            doclist = list(doc_set)
            print ('Final doclist length:', len(doclist))
            print (doclist)
            
            doclist.sort(key=lambda x: scores[x], reverse=True)
            print ('Final doclist length:', len(doclist))
            print (doclist)

            if len(doclist) > 0:
                print (doclist)
                print (searcher.stored_fields(doclist[0]))
            else:
                print ('No results found')

            for docnum in doclist:
                result = searcher.stored_fields(docnum)
                dict_res = {}
                for key in result.keys():
                    dict_res[key] = result[key]
                all_res.append(dict_res)

        else:
            if len(results) == 0:
                print ('No results found')

            for result in results:
                dict_res = {}
                for key in result.keys():
                    dict_res[key] = result[key]
                all_res.append(dict_res)
        
        if len(all_res) > 5:
            all_res = all_res[: 5]

        # for res in all_res:
        #     print (res) 

    return all_res

def search_terms():
    parser = CustomQueryParser(ix.schema)
    # parser = QueryParser("directions", ix.schema)
    with ix.searcher() as searcher:
        # print (list(searcher.lexicon('directions')))
        while True:
            print ('Enter query string:', )
            query_str = input()
            parsed_query = parser.parse(query_str)
            print (parsed_query)
            results = searcher.search(parsed_query, limit = 10)
            print (len(results))
            if len(results) > 0:
                print (results[0])
                print (type(results[0]))
                print (results[0].keys())
                print (results[0]['title'])
                # print (results[1])
                # print (results[2])
            else:
                print ('No results found')
            print (results.key_terms("ingredients"))
            print (results.key_terms("directions"))
            print (results.key_terms("categories"))
            print (results.key_terms("title"))

if __name__ == "__main__":
    # query = {'breakfast': ['false'], 'brunch': ['false'], 'lunch': ['false'], 'dinner': ['false'], 'cal200': ['false'], 'cal400': ['false'], 'cal600': ['false'], 'cal800': ['false'], '22-minute meals': ['false'], 'dairy free': ['false'], 'peanut free': ['false'], 'soy free': ['false'], 'wheat/gluten-free': ['false'], 'vegetarian': ['false'], 'text': ['chicken'], 'request': ['2']}
    # search(query)
    search_terms()