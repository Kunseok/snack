import json
from datetime import datetime
from elasticsearch import Elasticsearch

# host defined
es = Elasticsearch([{u'host': u'10.10.10.115', u'port': 9200}])

for i in range(1001):
    res = es.search(index="bank",q=("_id:"+str(i)))
    for x in res["hits"]["hits"]:
        print(x)
'''
result = {"mydata": mydata}
q = json.dumps(result)
print(q)
print("%d documents found" % res['hits']['total'])

for doc in res['hits']['hits']:
    print("%s) %s" % (doc['_id'], doc['_source']['content']))
print(res['result'])

res = es.get(index="test-index", doc_type='tweet', id=1)
print(res['_source'])

es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
'''
