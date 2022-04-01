import urllib, requests, json, math

#DECLARE SOME STUFF
i = 1 # counter
header = "mailto=tfluhr@iit.edu"
uid = "I180949307"
cursor = "*"
#cursor = "IlstMTE5OTMxODQwMDAwMF0i"
call = ('https://api.openalex.org/works?filter=institutions.id:{}&sort=publication_date:desc&per-page=200&{}&cursor={}'.format(uid, header, cursor))
json_dir = r'C:\Users\tfluhr\Desktop\json_dir'

# GET OBJECT COUNT

f = urllib.request.urlopen(call)
x = json.load(f)
count = x['meta']['count']
cursor = x['meta']['next_cursor']
f.close()
print(count)
print(cursor)
# GET API PAGE COUNT

api_page_count = math.ceil(count/200)
print(api_page_count)

#  Get all the JSON

while cursor:
    call = ('https://api.openalex.org/works?filter=institutions.id:{}&sort=publication_date:desc&per-page=200&{}&cursor={}'.format(uid, header, cursor))
    response = requests.get(call)
    with open(json_dir + "\\" + str(i) + ".json" , 'wb') as file:
        file.write(response.content)
    i+=1
    f = urllib.request.urlopen(call)
    x = json.load(f)
    cursor = x['meta']['next_cursor']
    f.close()
    if cursor is not None:
        print(str(i) + ": " + cursor)
    else:
        print("JSON download complete.")

