import urllib, requests, json, math

#DECLARE SOME STUFF
# counter to track api page 
i = 1 # counter
#API Call
call = ('https://api.openalex.org/works?filter=institutions.id:I180949307&page=%s&sort=publication_date:desc&per-page=200' % i)
#DIR TO DUMP JSON FILES
json_dir = r'C:\Users\tfluhr\Desktop\json_dir'

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
    call = ('https://api.openalex.org/works?filter=institutions.id:I180949307&page=%s&sort=publication_date:desc&per-page=200' % i)
    response = requests.get(call)
    with open(json_dir + "\\" + str(i) + ".json" , 'wb') as file:
        file.write(response.content)
    i+=1
