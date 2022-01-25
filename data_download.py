"""
This module collects title and abstract from dois
"""

import json
import random
import requests
import sqlite3
import time

start_time = time.time()

doi_file = "C:/Users/satan/PycharmProjects/SolarCell/dois/relevant_dois.json"
data_dir = "C:/Users/satan/PycharmProjects/SolarCell/data/"
db_file = data_dir + "abstracts.db"
elsevier_api_key = "39e4590618fd80d8b4f89edbec9673d2"
springer_api_key = "e3224f6e8aa7f7b0c3a2861d02121fa8"


def scopus_api(doi):
    url = "https://api.elsevier.com/content/abstract/doi/" + doi
    PARAMS = {"httpAccept":"application/json", "apiKey": elsevier_api_key}
    r = requests.get(url, params=PARAMS)
    if r.status_code == 200:
        data = r.json()
        return data
    return None


def scidirect_api(doi):
    """
    Search science direct api for this doi, return title,abstract, pub_date, journal if found
    :param doi:
    :return: (title, abstract, pub_date, journal) or None
    """
    url = "https://api.elsevier.com/content/article/doi/" + doi
    PARAMS = {"httpAccept":"application/json", "apiKey": elsevier_api_key}
    r = requests.get(url, params=PARAMS)
    if r.status_code == 200:
        data = r.json()
        title = data['full-text-retrieval-response']['coredata']['dc:title']
        abstract = data['full-text-retrieval-response']['coredata']['dc:description']
        pub_date = data['full-text-retrieval-response']['coredata']['prism:coverDate']
        journal = data['full-text-retrieval-response']['coredata']['prism:publicationName']
        if title:
            title = title.strip(' \n')
        if abstract:
            abstract = abstract.strip(' \n')
        if pub_date:
            pub_date = pub_date.strip(' \n')
        if journal:
            journal = journal.strip(' \n')
        return title, abstract, pub_date, journal
    return None


def springer_api(doi):
    """
    Search springer api for this doi, return title, abstract, pub_date, journal if found
    :param doi:
    :return: (title, abstract, pub_date, journal) or None
    """
    url = "http://api.springernature.com/metadata/json/doi/" + doi + "?api_key=" + springer_api_key
    r = requests.get(url)
    data = r.json()
    if data['result'][0]['total'] == '1':
        data = r.json()
        title = data['records'][0]['title']
        abstract = data['records'][0]['abstract']
        pub_date = data['records'][0]['publicationDate']
        journal = data['records'][0]['publicationName']
        if title:
            title = title.strip(' \n')
        if abstract:
            abstract = abstract.strip(' \n')
        if pub_date:
            pub_date = pub_date.strip(' \n')
        if journal:
            journal = journal.strip(' \n')
        return title, abstract, pub_date, journal
    return None


def check_coverage(n):
    # check the coverage of the three apis on the n randomly sampled dois
    i = 0
    with open(doi_file) as f:
        scidirect_dois = []
        springer_dois = []
        scopus_dois = []
        doi_list = json.load(f)
        sample_dois = random.sample(doi_list, n)
        for doi in sample_dois:
            i = i + 1
            try:
                if scidirect_api(doi):
                    scidirect_dois.append(doi)
                if springer_api(doi):
                    springer_dois.append(doi)
                if scopus_api(doi):
                    scopus_dois.append(doi)
            except:
                print(i)
                print("scopus", len(scopus_dois))
                print("scidirect", len(scidirect_dois))
                print("springer", len(springer_dois))
        print("scopus", len(scopus_dois))
        print("scidirect", len(scidirect_dois))
        print("springer", len(springer_dois))


def download_sample(n):
    # download n samples from remaining relevant dois that are not in
    # /media/kun/Storage/Research/Material_tm/relevant_abstracts/abstracts.db
    print(f"start to download {n} dois from the remaining dois")
    con = sqlite3.connect(db_file)   # connect to db
    cur = con.cursor()
    scidirect_dois = []  # a list of dois found in scidirect
    springer_dois = []   # a list of dois found in springer
    springer_limit = 5000      # springer limit 5000 per day
    with open(doi_file) as f:
        doi_list = json.load(f)    # load doi list from json file
        cur.row_factory = lambda cursor, row: row[0]    # cursor returns a list of dois rather than a list of tuples
        sql = "SELECT doi FROM tblAbstract"
        cur.execute(sql)
        existing_dois = cur.fetchall()      # fetch existing dois
        sql = "SELECT doi FROM tblMissing"
        cur.execute(sql)
        missing_dois = cur.fetchall()   # fetch known missing dois
        remaining_dois = set(doi_list) - set(existing_dois) - set(missing_dois)  # exclude existing and known missing
        # dois
        missing_dois = []        # reset missing_dois to take new ones
        sample = random.sample(remaining_dois, n)           # random sample n from remaining dois
        cur.row_factory = None   # reset cursor row_factory
        for doi in sample:
            try:
                data = scidirect_api(doi)    # try scidirect api
                if data:  # if in sci_direct
                    scidirect_dois.append(doi)
                    print(doi)
                    sql = "INSERT OR IGNORE INTO tblAbstract VALUES(?,?,?,?,?,?)"
                    cur.execute(sql, (doi, data[0], data[1], "ScienceDirect API", data[2], data[3]))
                else:  # else try springer
                    data = springer_api(doi)  # try springer api
                    time.sleep(0.4)  # pause 0.2 seconds
                    if data:  # if in springer
                        springer_dois.append(doi)
                        sql = "INSERT OR IGNORE INTO tblAbstract VALUES(?,?,?,?,?,?)"
                        cur.execute(sql, (doi, data[0], data[1], "SpringerNature API", data[2], data[3]))
                    else:  # if not in sci_direct or springer
                        missing_dois.append(doi)
                        sql = "INSERT OR IGNORE INTO tblMissing VALUES(?)"
                        cur.execute(sql, (doi,))
                    springer_limit = springer_limit - 1
                    if springer_limit == 0:  # if reach 5000 limit
                        exit(0)
            except:
                print(f"connection error happens for {doi}")
                print("scidirect so far", len(scidirect_dois))
                print("springer so far", len(springer_dois))
                print("missing so far", len(missing_dois))
                con.commit()
        print("scidirect", len(scidirect_dois))
        print("springer", len(springer_dois))
        print("missing", len(missing_dois))
        con.commit()
        con.close()


if __name__ == '__main__':
    download_sample(n=100)
    print("--- %s seconds ---" % (time.time() - start_time))


