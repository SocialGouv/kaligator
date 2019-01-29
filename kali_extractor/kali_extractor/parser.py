import os
import progressbar
from pymongo import MongoClient
import argparse
from documents_processor import ArticleProcessor, IDCCProcessor, \
    SectionTaProcessor, TexteStructProcessor, TexteVersionProcessor
from functools import partial
from file_utils import get_nested_file_paths
from downloader import Downloader
from dict_utils import deep_get


DOC_TYPES_MAPPING = {
    "article": {"processor": ArticleProcessor, "collection": "articles"},
    "conteneur": {"processor": IDCCProcessor, "collection": "conteneurs"},
    "section_ta": {
        "processor": SectionTaProcessor, "collection": "section_tas"
    },
    # it's important that texte/struct is before texte/version because of
    # https://github.com/SocialGouv/kali_dumps_scripts/issues/12
    "texte/struct": {
        "processor": TexteStructProcessor, "collection": "textes"
    },
    "texte/version": {
        "processor": TexteVersionProcessor, "collection": "textes"
    },
}
DOC_TYPES = list(DOC_TYPES_MAPPING.keys())


def convert_and_insert_in_mongo(mongo_db, doc_type, xml_path):
    processor = DOC_TYPES_MAPPING[doc_type]["processor"]
    collection = DOC_TYPES_MAPPING[doc_type]["collection"]
    parsed_document = processor(xml_path).process()
    kali_id, _ = next(deep_get(parsed_document, "META/META_COMMUN/ID"))
    mongo_db[collection].update_one(
        {"META.META_COMMUN.ID": kali_id},
        {"$set": parsed_document},
        upsert=True
    )


def ensure_indexes(mongo_db, doc_type):
    collection = DOC_TYPES_MAPPING[doc_type]["collection"]
    mongo_db[collection].create_index("META.META_COMMUN.ID")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Parse and import data from the KALI database dumps'
    )
    parser.add_argument(
        '--download', action="store_true",
        help="download and extract the dump if it's not already done",
    )
    parser.add_argument(
        '--mongo-uri',
        default=os.environ.get("MONGODB_URI", "mongodb://localhost"),
        help="fully qualified MongoDB uri"
    )
    parser.add_argument(
        '--mongo-db-name', default="kali",
        help="the name of the database to store documents into." +
        "only works with mongodb mode"
    )
    parser.add_argument(
        '--drop', action="store_true",
        help="drops existing database before starting." +
        "only works with mode MongoDB"
    )
    parser.add_argument(
        '--only', choices=DOC_TYPES,
        help="limits the extraction to a single document type"
    )
    parser.add_argument(
        '--dump-dir',  default="/tmp/kali_dump",
        help="path to the extracted KALI dump"
    )
    args = parser.parse_args()

    if not os.path.isdir(args.dump_dir):
        os.makedirs(args.dump_dir)

    if args.download:
        Downloader(download_dir=args.dump_dir).run()

    print(
        "will insert mongo documents into '%s' database" %
        args.mongo_db_name
    )
    mongo_client = MongoClient(args.mongo_uri)
    mongo_db = mongo_client[args.mongo_db_name]
    action = partial(convert_and_insert_in_mongo, mongo_db)

    doc_types = [args.only] if args.only else DOC_TYPES

    dump_dir_root = os.path.join(args.dump_dir, "kali", "global")
    if not os.path.isdir(dump_dir_root):
        raise Exception(
            "dump dir does not exist or doesn't contain the extracted dump."
        )

    for doc_type in doc_types:
        if args.drop:
            collection = DOC_TYPES_MAPPING[doc_type]["collection"]
            print("dropping %s " % collection)
            mongo_db[collection].drop()
        subdir_path = os.path.join(dump_dir_root, doc_type)
        ensure_indexes(mongo_db, doc_type)
        print(
            "going through %s recursively to get XML paths ..." %
            subdir_path
        )
        xml_paths = get_nested_file_paths(subdir_path)
        print("done ! got %s XML paths." % len(xml_paths))
        for i in progressbar.progressbar(range(len(xml_paths))):
            action(doc_type, xml_paths[i])
