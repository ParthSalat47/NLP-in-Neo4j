from neo4j import GraphDatabase, basic_auth
import json


with open('./tweets_full.json', encoding="utf8") as json_data:
    tweetArr = json.load(json_data)

# pip3 install neo4j-driver
# python3 example.py


driver = GraphDatabase.driver(
  "neo4j://localhost:7687",
  auth=basic_auth("neo4j", "hi"))

cypher_query = '''
MATCH (n)
RETURN COUNT(n) AS count
LIMIT $limit
'''

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

def add_tweets(tx):
    tx.run(import_query, tweetArr=tweetArr)

with driver.session(database="neo4j") as session:
    session.write_transaction(add_tweets)