from neo4j import GraphDatabase, basic_auth
import json

tweetArr = []
with open('parsed_tweets_scraped.json', encoding="utf8") as json_data:
    tweetArr = json.load(json_data)

# pip3 install neo4j-driver
# python3 example.py


driver = GraphDatabase.driver(
  "neo4j://localhost:7687",

  auth=basic_auth("neo4j", "hi"))


# with driver.session() as session:
    # session.run('CREATE CONSTRAINT ON (p:Person) ASSERT p.name IS UNIQUE;')
    # session.run('CREATE CONSTRAINT ON (l:Location) ASSERT l.name IS UNIQUE;')
    # session.run('CREATE CONSTRAINT ON (o:Organization) ASSERT o.name IS UNIQUE;')

entity_import_query ='''
WITH ''' + f"{tweetArr}" + ''' AS parsedTweets
UNWIND parsedTweets AS parsedTweet
MATCH (t:Tweet) WHERE t.tweet_id = parsedTweet.id


FOREACH(entity IN parsedTweet.entities |
    // Person
    FOREACH(_ IN CASE WHEN entity.tag = 'PERSON' THEN [1] ELSE [] END | 
        MERGE (p:Person {name: reduce(s = "", x IN entity.entity | s + x + " ")}) //FIXME: trailing space
        MERGE (p)<-[:CONTAINS_ENTITY]-(t)
    )
    
    // Organization
    FOREACH(_ IN CASE WHEN entity.tag = 'ORGANIZATION' THEN [1] ELSE [] END | 
        MERGE (o:Organization {name: reduce(s = "", x IN entity.entity | s + x + " ")}) //FIXME: trailing space
        MERGE (o)<-[:CONTAINS_ENTITY]-(t)
    )
    
    // Location
    FOREACH(_ IN CASE WHEN entity.tag = 'GPE' THEN [1] ELSE [] END | 
        MERGE (l:Location {name: reduce(s = "", x IN entity.entity | s + x + " ")}) // FIXME: trailing space
        MERGE (l)<-[:CONTAINS_ENTITY]-(t)
    )

   
)

'''

cypher_query = '''
MATCH (u:User)-[:POSTED]->(t:Tweet)-[:HAS_TAG]->(h:Hashtag)
WHERE u.screen_name = "TEN_GOP"
OPTIONAL MATCH (t)-[:HAS_LINK]->(l:Link)
RETURN *
'''
with driver.session() as session:
    session.run(entity_import_query)