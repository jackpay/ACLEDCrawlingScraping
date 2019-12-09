import csv,json

def get_seeds(seedsCSV,headers,white_list=None,blacklist=None):
    wanted_urls = []
    unwanted_urls = []
    if white_list:
        wanted_urls = get_white_list(white_list)
    if blacklist:
        with open(blacklist, 'r') as unwanted_file:
            unwanted_urls = [url.replace("\n","") for url in unwanted_file.readlines()]
    with open(seedsCSV, 'r', encoding='utf-8-sig') as seeds:
        reader = csv.reader(seeds)
        headersrow = next(reader)
        print(headersrow)
        indxs = [headersrow.index(header) for header in headers]
        link = headersrow.index('Link')
        seeds = {}
        seeds["seeds"] = [{"seed": {headersrow[i] : row[i] for i in indxs}} for row in reader if len(row) > 0
                          and (not white_list or (white_list and row[link] in wanted_urls))
                          and (not blacklist or (blacklist and not domain_present(row[link],unwanted_urls)))]
        seeds["seeds"] = seeds["seeds"]
        print(len(seeds['seeds']))
        return seeds

def domain_present(link, domains):
    for domain in domains:
        if domain in link:
            return True
    return False

def get_white_list(csvf):
    with open(csvf, 'r', encoding='utf-8-sig') as whitelist:
        reader = csv.reader(whitelist)
        link_indx = next(reader).index('Link')
        return set([row[link_indx] for row in reader])

def build_json(seeds,outputJSON):
    with open(outputJSON,'w') as f:
        json.dump(seeds,f)

if __name__ == "__main__":
    # headers = ["Name","Link", "Method52 Job name","Countries that use this link (separated by a semi-colon)"]
    headers = ["Source Name", "Link", "Countries"]

    # seedCSV = "/Users/jp242/Documents/Projects/ACLED/Scraper-backup/gsheet-25-11-19.csv"
    # seedCSV = "/Users/jp242/Documents/Projects/ACLED/ManualScrapers/gsheet-Scrapers.csv"
    seedCSV = "/Users/jp242/Documents/Projects/ACLED/final-url-list/All_Desks_Checklist_Sources_with_difficulty_info.csv"
    whitelist = "/Users/jp242/Documents/Projects/ACLED/final-url-list/full-source.csv"
    blacklist = "/Users/jp242/Documents/Projects/ACLED/final-url-list/black-list.txt"
    outputJSON = "/Users/jp242/Documents/Projects/ACLED/final-url-list/full-seed-list-minus-prebuilt-2.json"
    build_json(get_seeds(seedCSV,headers,white_list=whitelist,blacklist=blacklist),outputJSON)

