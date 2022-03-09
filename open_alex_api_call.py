import urllib, requests, json, math

#DECLARE SOME STUFF
i = 1 # SIMPLE COUNTER
header = "mailto=tfluhr@iit.edu" # ADD HEADER TO API CALL IN ORDER TO GET IN POLITE POOL
uid = "I180949307" # OPENALEX INSTITUTION ID
call = ('https://api.openalex.org/works?filter=institutions.id:{}&page=1&sort=publication_date:desc&per-page=200&{}'.format(uid, header))
json_dir = r'C:\Users\tfluhr\Desktop\json_dir' # WHERE TO DUMP JSON 

# GET OBJECT COUNT

f = urllib.request.urlopen(call)
x = json.load(f)
count = x['meta']['count']
f.close()
print(count)

# GET API PAGE COUNT

api_page_count = math.ceil(count/200)
print(api_page_count)

#  Get all the JSON

while i <= api_page_count:
    call = ('https://api.openalex.org/works?filter=institutions.id:{}&page={}&sort=publication_date:desc&per-page=200&{}'.format(uid, i, header))
    response = requests.get(call)
    with open(json_dir + "\\" + str(i) + ".json" , 'wb') as file:
        file.write(response.content)
    i+=1
