import requests
items = []
initial = "http://archive.org/wayback/available"
# iterate through list of flagged twitter screen names
with open('./data/twitter_handle_urls.csv') as f:
    for line in f:
        params = {'url': line}
        r = requests.get(initial, params=params)
        d = r.json()
        #print(d)
        items.append(d)
# write URL of any available archives to file
with open('./data/avail_urls.txt', 'w') as f:
    for item in items:
        if 'archived_snapshots' in item:
            if 'closest' in item['archived_snapshots']:
                f.write(item['archived_snapshots']['closest']['url'] + '\n')