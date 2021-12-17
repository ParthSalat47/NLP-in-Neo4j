#import polyglot
import nltk 
import json



from neo4j import GraphDatabase, basic_auth
driver = GraphDatabase.driver(
  "neo4j://localhost:7687",
  auth=basic_auth("neo4j", "hi"))
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
            parsedTweet['entities'] = []

            for sent in nltk.sent_tokenize(t['text']):
                for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                    if hasattr(chunk, 'label'):
                        print(chunk.label(), ' '.join(c[0] for c in chunk))
                        eobj = {}
                        eobj['tag'] = chunk.label()
                        eobj['entity'] = ''.join(c[0] for c in chunk)
                        parsedTweet['entities'].append(eobj)

            
            
            if len(parsedTweet['entities']) > 0:
                entityArr.append(parsedTweet)


            

        except:
            pass

    print(entityArr[:3])
    
    with open('parsed_tweets_scraped.json', 'w', encoding="utf8") as f:
     json.dump(entityArr, f, ensure_ascii=False, sort_keys=True, indent=4)
