from urllib.parse import urlparse
from adblockparser import AdblockRules
import json
import os
import re
from paths import captured, dependencies


def label_data(curr_dir, sub_dir):

    # relative path to the uBlock log
    ublock_log_file = os.path.join(captured, curr_dir, "ublock_log.txt")
    # extracts url from uBlockLog.txt and writes urls to blocked_URLs_uBlock.txt

    def extract_urls_with_options():
        with open(ublock_log_file, "r") as log:
            content = log.read().splitlines()

        ublock_log_list = []
        blocked_urls_ublock = []
        index_list = []

        # get indexes of blocked signs "--" in uBlockLog.txt -> indicates blocked element
        for i, j in enumerate(content):
            if j == "--":
                index_list.append(i)

        for index in index_list:

            # strip url https://example.com/home?width=10 ----> example.com
            stripped_url = urlparse(content[index+4]).netloc
            blocked_urls_ublock.append(content[index+4])

            rule = content[index-1]

            # get option parameter for adblockparser from each blocked element
            domain = " "
            third_party = False
            stylesheet = False
            xmlhttprequest = False
            image = False
            script = False
            ping = False

            # uBlock uses some custom rules -> check for custom rules and change them to adblock format
            if '3p' in rule:
                rule = rule.replace("3p", "third-party")
                third_party = True

            if "image" in rule:
                image = True

            if "script" in rule:
                script = True

            if "ping" in rule:
                ping = True

            if "xmlhttprequest" in rule:
                xmlhttprequest = True

            if "stylesheet" in rule:
                stylesheet = True

            if "domain=" in rule:

                if "domain=~" in rule:
                    domain = " "
                elif "domain=~" not in rule:
                    # extract domain content
                    domain = rule.partition("domain=")[2]
                    if "," in domain:
                        domain = domain.partition(",")[0]

            # build log dict with options
            obj = {
                "stripped_url": stripped_url,
                "rule": rule,
                "options": {
                    "domain": domain,
                    "third-party": third_party,
                    "image": image,
                    "script": script,
                    "xmlhttprequest": xmlhttprequest,
                    "stylesheet": stylesheet,
                    "ping": ping
                }
            }

            # check options -> if False delete options |||| .copy() to dont change the iterated object while iterating
            for option in obj["options"].copy():
                if not obj["options"][option]:
                    del obj["options"][option]

            # push it to the ublock_log list
            ublock_log_list.append(obj)

        return ublock_log_list

    ublock_log_list = extract_urls_with_options()

    # CHECK RULES AND OPTIONS
    # print(ublock_log_list)

    # path to JSON file
    data_json = os.path.join(captured, curr_dir, sub_dir, "data.json")

    def label():
        # # option to use easyprivacy to check rules contained by that list against urls
        # with open(f"{dependencies}/easyprivacy.txt", "rb") as f:
        #     raw_rules = f.read().decode("utf8").splitlines()

        raw_rules = []

        # use rules from uBlockLog for performance upgrade -> used rules should be exactly the same
        for entry in ublock_log_list:
            raw_rules.append(entry["rule"])

        rules = AdblockRules(raw_rules)
        options = {}

        #  open json file
        with open(data_json, "r+", encoding="latin-1") as json_file:
            # Transforms json input to python objects
            data = json.load(json_file)

            # loop through packets
            for packet in data:

                packet["tracker"] = "false"
                layers = packet["_source"]["layers"]

                # add http2.header.value.url field
                if "http2" in packet['_source']['layers']:
                    if "http2.stream" in packet['_source']['layers']['http2']:
                        if "http2.header" in packet['_source']['layers']['http2']['http2.stream']:
                            http2 = packet['_source']['layers']['http2']
                            header = http2['http2.stream']['http2.header']

                            # if there is a http2.header
                            if 'http2.header.value' in header[0]:
                                # check if url starts with http or https -> if there is a url in the header.value

                                if 'http' in header[2]["http2.header.value"]:
                                    try:
                                        packet["http2.header.value.url"] = header[2]["http2.header.value"] + \
                                            "://" + header[1]['http2.header.value'] + \
                                            header[3]['http2.header.value']
                                    except IndexError:
                                        pass

                # check for every stripped url in http2.header.value.url
                if "http2.header.value.url" in packet:
                    # loop through new created ublock_log_list
                    for blocked_element in ublock_log_list:

                        # check if stripped_url is in http2.header.value.url
                        if blocked_element["stripped_url"] in packet["http2.header.value.url"]:

                            # set options according to blocked_element in ublock_log_list
                            options = blocked_element["options"]

                            # check if url in http2.header.value.url should be blocked according to adblockparser
                            if(rules.should_block(packet["http2.header.value.url"], options)):
                                packet["tracker"] = "true"

                        # check for every stripped url in http.request.full_uri
                if "http" in layers:
                    http = packet["_source"]["layers"]["http"]

                    if "http.request.full_uri" in http:
                        http_request_full_uri = packet["_source"]["layers"]["http"]["http.request.full_uri"]

                        # loop through new created ublock_log_list
                        for blocked_element in ublock_log_list:
                            # check if stripped_url is in http_request_full_uri
                            if blocked_element["stripped_url"] in http_request_full_uri:
                                # set options according to blocked_element in ublock_log_list
                                options = blocked_element["options"]

                                # check if url in http_request.full_uri should be blocked according to adblockparser
                                if(rules.should_block(http_request_full_uri, options)):
                                    packet["tracker"] = "true"

            json_file.seek(0)
            # write to file
            json.dump(data, json_file, indent=4)

    label()
