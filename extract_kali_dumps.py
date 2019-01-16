from xmljson import yahoo as xmljson_parser
from xml.etree import ElementTree
import json
import html
import os
import progressbar
import gevent.pool
from pymongo import MongoClient
import argparse


def get_all_xml_paths(root_dir):
    xml_paths = []
    for dir_name, _, file_list in os.walk(root_dir):
        for file_name in file_list:
            xml_paths.append(os.path.join(dir_name, file_name))
    return xml_paths

def convert_xml_to_json(xml_path):
    with open(xml_path, "r") as f:
        element = ElementTree.parse(f)
    root = element.getroot()
    sub_strings = [
        ElementTree.tostring(sub_element).decode("utf-8")
        for sub_element in root.findall(".//CONTENU")[0]
    ]
    parsed_contenu_html = html.unescape("".join(sub_strings))
    parsed = xmljson_parser.data(root)
    parsed_document = parsed["ARTICLE"]
    parsed_document["BLOC_TEXTUEL"]["CONTENU"] = parsed_contenu_html
    return parsed_document

def convert_and_insert_in_mongo(xml_path, mongo_db):
    parsed_document = convert_xml_to_json(xml_path)
    mongo_db['articles'].insert_one(parsed_document)

def convert_and_write_json_file(xml_path, output_dir):
    parsed_document = convert_xml_to_json(xml_path)
    json_dump = json.dumps(parsed_document, indent=2, ensure_ascii=False)
    xml_file_name = os.path.splitext(os.path.basename(xml_path))[0]
    dest_json_path = os.path.join(output_dir, "%s.json" % xml_file_name)
    with open(dest_json_path, "wb") as f:
        f.write(json_dump.encode("utf-8"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse and import data from the KALI database dumps')
    parser.add_argument('--mode', help="either store individual JSON files or import into a MongoDB database", choices=["json", "mongodb"], default="json")
    parser.add_argument('--output-dir', help="only works with json mode. defines where files will be stored.", default="./kali_json")
    parser.add_argument('--mongo-db-name', help="only works with mongodb mode. the name of the database to store documents into.", default="kali")
    parser.add_argument('--gevent-pool', help="will use a gevent pool for faster processing", action="store_true")
    parser.add_argument('root_dir', help="path to the extracted KALI dump")
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    print("going through %s recursively to get all XML paths ..." % args.root_dir)
    xml_paths = get_all_xml_paths(args.root_dir)
    print("done ! got %s XML paths." % len(xml_paths))

    print("now processing XML files ...")
    if args.mode == "json":
        action = convert_and_write_json_file
        second_arg = args.output_dir
        print("will write JSON files to %s" % args.output_dir)
    else:
        action = convert_and_insert_in_mongo
        mongo_client = MongoClient()
        mongo_db = mongo_client[args.mongo_db_name]
        second_arg = mongo_db
        print("will insert mongo documents into '%s' database" % args.mongo_db_name)

    if args.gevent_pool:
        print("(using a gevent Pool)")
        pool = gevent.pool.Pool(10)
        for xml_path in xml_paths:
            pool.spawn(action, xml_path, second_arg)
        pool.join()
    else:
        for i in progressbar.progressbar(range(len(xml_paths))):
            action(xml_paths[i], second_arg)

