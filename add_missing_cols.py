import json
import random
import requests
import sqlite3
import time

start_time = time.time()

#doi_file = "C:/Users/satan/PycharmProjects/SolarCell/dois/relevant_dois.json"
data_dir = "C:/Users/satan/PycharmProjects/SolarCell/data/"
db_file = data_dir + "abstracts.db"
elsevier_api_key = "39e4590618fd80d8b4f89edbec9673d2"
springer_api_key = "e3224f6e8aa7f7b0c3a2861d02121fa8"


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

def download(n):
    con = sqlite3.connect(db_file)  # connect to db
    cur = con.cursor()
    scidirect_dois = []  # a list of dois found in scidirect
    springer_dois = []  # a list of dois found in springer
    springer_limit = 5000  # springer limit 5000 per day

    cur.row_factory = lambda cursor, row: row[0]

    sql = "SELECT doi from tblAbstract where pub_date IS NULL AND journal IS NULL"
    #sql = "SELECT doi from tblAbstract where row[0]"
    cur.execute(sql)
    dois_missing_info = cur.fetchall()
    print(len(dois_missing_info))
    cur.row_factory = None
    for i,dois in enumerate(dois_missing_info):
        if i<n:
            print(dois)
            #print(i)
            try:
                data = scidirect_api(dois)
                if data:
                    #print("success")
                    scidirect_dois.append(data)
                    sql = "UPDATE tblAbstract SET pub_date = ?, journal = ? WHERE doi = ?"
                    cur.execute(sql, (data[2], data[3], dois))
                    #print(data[2], data[3])

                else:
                    data = springer_api(dois)  # try springer api
                    time.sleep(0.4)  # pause 0.2 seconds
                    if data:  # if in springer
                        springer_dois.append(dois)
                        sql = "UPDATE tblAbstract SET pub_date = ?, journal = ? WHERE doi = ?"
                        cur.execute(sql, (data[2], data[3], dois))

                    springer_limit = springer_limit - 1
                    if springer_limit == 0:  # if reach 5000 limit
                        exit(0)

            except Exception as e:
                print(e)
                print(dois)

    con.commit()
    con.close()

if __name__ == '__main__':
    download(n=8221)
    print("--- %s seconds ---" % (time.time() - start_time))