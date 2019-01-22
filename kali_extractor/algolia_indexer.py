from algoliasearch import algoliasearch
from pymongo import MongoClient
from collections import defaultdict
import math
import sys


BATCH_SIZE = 1000

doc_type = "article"

algolia_client = algoliasearch.Client("WV1OH9RKZO", '6e45301bf75431b62475c613259e31df')

mongo_client = MongoClient()
mongo_db = mongo_client["kali"]

algolia_indexes = {
    "META": algolia_client.init_index('kali_%s_%ss' % (doc_type, "meta")),
    "CONTEXTE": algolia_client.init_index('kali_%s_%ss' % (doc_type, "contexte")),
    "VERSIONS": algolia_client.init_index('kali_%s_%ss' % (doc_type, "version")),
    "": algolia_client.init_index('kali_%ss' % doc_type)
}

total = mongo_db[doc_type].count_documents({})
cursor = mongo_db[doc_type].find().batch_size(BATCH_SIZE)

for i in range(math.floor(total / BATCH_SIZE)):
    print("first batch : items %s to %s" % (i * BATCH_SIZE, (i + 1) * BATCH_SIZE ))
    documents_batches = defaultdict(list)
    for y in range(BATCH_SIZE):
        parent_document = dict(cursor.next())
        # print("document json size in bytes is %s" % sys.getsizeof(parent_document))
        kali_id = parent_document["META"]["META_COMMUN"]["ID"]
        for sub_document_key in ["META", "CONTEXTE", "VERSIONS"]:
            sub_document = parent_document.pop(sub_document_key)
            sub_document["_parent_id"] = kali_id
            documents_batches[sub_document_key].append(sub_document)
        documents_batches[""].append(parent_document)

    for suffix, documents_batch in documents_batches.items():
        algolia_index = algolia_indexes[suffix]
        print("sending batch (%s MB) to algolia ..." % (sys.getsizeof(documents_batch) / 1024 / 1024))
        algolia_index.add_objects(documents_batch)
