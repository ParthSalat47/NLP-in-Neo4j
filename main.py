from neo4j import GraphDatabase
import json

driver = GraphDatabase.driver("neo4j://127.0.0.1:7687", auth=("neo4j", "1234"))
#print(driver)

with open('/home/garmadon/Projects/neo4j/data/tweets_full.json') as json_data:
    tweetArr = json.load(json_data)

#print(len(tweetArr))

import_query = '''
WITH $tweetArr AS tweets
UNWIND tweets AS tweet
MERGE (u:User {user_id: tweet.user_id})
ON CREATE SET u.screen_name = tweet.screen_name
MERGE (t:Tweet {tweet_id: tweet.tweet_id})
ON CREATE SET t.text = tweet.tweet_text,
              t.permalink = tweet.permalink
MERGE (u)-[:POSTED]->(t)

FOREACH (ht IN tweet.hashtags |
  MERGE (h:Hashtag {tag: ht.tag })
  ON CREATE SET h.archived_url = ht.archived_url
  MERGE (t)-[:HAS_TAG]->(h)
)

FOREACH (link IN tweet.links |
  MERGE (l:Link {url: link.url})
  ON CREATE SET l.archived_url = link.archived_url
  MERGE (t)-[:HAS_LINK]->(l)
)

'''

def add_tweets(tx, tweetArr):
    tx.run(import_query, tweetArr=tweetArr)

with driver.session() as session:
    session.write_transaction(add_tweets, tweetArr)

driver.close()