import requests, json, urllib, os, sys, math

### Author Functions

def get_author_count(uid, header):
    cursor = "*"
    apicall = ('https://api.openalex.org/authors?filter=last_known_institution.id:{}&per-page=200&{}&cursor={}'.format(uid, header, cursor))
    #print(apicall)
    author_count = (requests.get(apicall).json()['meta']['count'])
    return author_count

### Institution Functions

def get_institution(uid, header):
    my_inst = {}
    apicall = ('https://api.openalex.org/institutions?filter=openalex_id:{}{}'.format(uid, header))
    f = urllib.request.urlopen(apicall)
    x = json.load(f)
    my_inst["Institution Name"] = x['results'][0]['display_name']
    my_inst["work_count"] = x['results'][0]['works_count']
    my_inst["cited_by_count"] = x['results'][0]['cited_by_count']
    my_inst["last_update"] = x['results'][0]['updated_date']
    #return name, work_count, cited_by_count, last_update
    return my_inst

### Works Functions

def get_works_count(uid, header):
    works_dict = {}
    cursor = "*"
    apicall = ('https://api.openalex.org/works?filter=institutions.id:{}&per-page=200&{}&group_by=is_oa'.format(uid, header))
    works = requests.get(apicall)
    groups = works.json()['group_by']
    total_works = 0
    oa_works = 0
    for g in groups:
        total_works += g['count']
        if g['key'] == 'true':
            oa_works += g['count']
    works_dict["Total Works"] = total_works
    works_dict["Open Access"] = oa_works
    works_dict["Paywalled"] = total_works - oa_works
    return works_dict

def get_works_by_year(uid, header, year=None):
    my_inst = {}
    apicall = ('https://api.openalex.org/institutions?filter=openalex_id:{}{}'.format(uid, header))
    f = urllib.request.urlopen(apicall)
    x = json.load(f)
    years = x['results'][0]['counts_by_year']
    for i in years:
        if i['year'] == year:
            return i
        elif year == None:
            return i

### download json of all works affiliated with institution
def get_all_works(uid, header):
    i = 1   ## counter
    cursor = "*"
    json_dir = r'C:\tmp\json_dir'
    apicall = ('https://api.openalex.org/works?filter=institutions.id:{}&sort=publication_date:desc&per-page=200&{}&cursor=*'.format(uid, header))
    works_count = (requests.get(apicall).json()['meta']['count'])
    page_count = math.ceil(works_count/200)
    print(page_count)
    isExist = os.path.exists(json_dir)
    if not isExist:
        os.makedirs(json_dir)
        print("Created new directory for your files")
    else:
        raise SystemExit("Please select another directory!")
    while i < 125:
        apicall = ('https://api.openalex.org/works?filter=institutions.id:{}&sort=publication_date:desc&per-page=200&{}&cursor={}'.format(uid, header, cursor))
        response = requests.get(apicall)
        with open(json_dir + "\\" + str(i) + ".json", 'wb') as file:
            file.write(response.content)
        i += 1
        f = urllib.request.urlopen(apicall)
        x = json.load(f)
        cursor = x['meta']['next_cursor']
        f.close()
        if i < 125:
            print("downloading file number", str(i))
        else:
            print("JSON download complete.")
