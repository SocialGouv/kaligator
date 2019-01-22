import json
import os
import progressbar
import gevent.pool
from pymongo import MongoClient
import argparse
from documents_processor import ArticleProcessor, IDCCProcessor, SectionTaProcessor, TexteProcessor
from functools import partial
from file_utils import get_nested_file_paths

PROCESSOR_MAPPING = {
    "article": ArticleProcessor,
    "conteneur": IDCCProcessor,
    "section_ta": SectionTaProcessor,
    "texte": TexteProcessor,
}

def convert_and_insert_in_mongo(mongo_db, doc_type, xml_path):
    processor = [doc_type]
    parsed_document = PROCESSOR_MAPPING[doc_type](xml_path).process()
    mongo_db[doc_type].insert_one(parsed_document)

def convert_and_write_json_file(output_dir, doc_type, xml_path):
    parsed_document = ArticleProcessor(xml_path).process()
    json_dump = json.dumps(parsed_document, indent=2, ensure_ascii=False)
    xml_file_name = os.path.splitext(os.path.basename(xml_path))[0]
    dest_json_path = os.path.join(output_dir, "%s.json" % xml_file_name)
    with open(dest_json_path, "wb") as f:
        f.write(json_dump.encode("utf-8"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Parse and import data from the KALI database dumps'
    )
    parser.add_argument(
        '--mode', choices=["json", "mongodb"], default="json",
        help="either store individual JSON files or import into a MongoDB database",
    )
    parser.add_argument(
        '--output-dir', default="./kali_json",
        help="defines where files will be stored. only works with json mode"
    )
    parser.add_argument(
        '--mongo-db-name', default="kali",
        help="the name of the database to store documents into. only works with mongodb mode"
    )
    parser.add_argument(
        '--gevent-pool', action="store_true",
        help="will use a gevent pool for faster processing"
    )
    parser.add_argument(
        '--drop', action="store_true",
        help="drops existing database before starting. only works with mode MongoDB"
    )
    parser.add_argument(
        '--only', choices=["article", "idcc", "section_ta", "texte"],
        help="limits the extraction to a single document type"
    )
    parser.add_argument('root_dir', help="path to the extracted KALI dump")
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    if args.mode == "json":
        action = partial(convert_and_write_json_file, args.output_dir)
        print("will write JSON files to %s" % args.output_dir)
    else:
        print("will insert mongo documents into '%s' database" % args.mongo_db_name)
        mongo_client = MongoClient()
        mongo_db = mongo_client[args.mongo_db_name]
        action = partial(convert_and_insert_in_mongo, mongo_db)

    if args.drop:
        mongo_client.drop_database(args.mongo_db_name)

    if args.only:
        doc_types = [args.only]
    else:
        doc_types = ["article", "conteneur", "section_ta", "texte"]

    for doc_type in doc_types:
        subdir_path = os.path.join(args.root_dir, doc_type)
        print("going through %s recursively to get XML paths ..." % subdir_path)
        xml_paths = get_nested_file_paths(subdir_path)
        print("done ! got %s XML paths." % len(xml_paths))

        if args.gevent_pool:
            print("(using a gevent Pool)")
            pool = gevent.pool.Pool(10)
            for xml_path in xml_paths:
                pool.spawn(action, doc_type, xml_path)
            pool.join()
        else:
            for i in progressbar.progressbar(range(len(xml_paths))):
                action(doc_type, xml_paths[i])

