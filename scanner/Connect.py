from elasticsearch import Elasticsearch

elastic = Elasticsearch(["localhost"],http_auth=("elastic","magicword"),port=9200)
