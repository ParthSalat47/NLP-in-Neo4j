#import polyglot
from text import Text

from neo4j import GraphDatabase
driver = GraphDatabase.driver("neo4j://127.0.0.1:7687", auth=("neo4j", "1234"))  
#neo4j://127.0.0.1:7687
#driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "1234"))  #this is working

with driver.session() as session:
    results = session.run("MATCH (t:Tweet) RETURN t.text AS text, t.tweet_id AS tweet_id")

#print(results)

tweetObjArr = []

for r in results:
    tweetObj = {}
    tweetObj['id'] = r['tweet_id']
    tweetObj['text'] = r['text']
    tweetObjArr.append(tweetObj)

print(len(tweetObjArr))

entityArr = []

for t in tweetObjArr:
    try:
        parsedTweet = {}
        parsedTweet['id'] = t['id']
        parsedTweet['text'] = t['text']
        blob = Text(t['text'])
        entities = blob.entities
        parsedTweet['entities'] = []
        for e in entities:
            eobj = {}
            eobj['tag'] = e.tag
            eobj['entity'] = e
            parsedTweet['entities'].append(eobj)
        if len(parsedTweet['entities']) > 0:
            entityArr.append(parsedTweet)
    except:
        pass
