# import the neo4j driver for Python

from neo4j import GraphDatabase

# Database Credentials

uri = "bolt://localhost:7687"

userName = "xxxxxx"

password = "xxxxxx"

# Connect to the neo4j database server

graphDB_Driver = GraphDatabase.driver(uri, auth=(userName, password))

# Counter
n = 1

create_works = f"CALL apoc.load.json('file:///Users/tfluhr/Desktop/json_dir/{n}.json') yield value " + "unwind value.results as r " + "unwind r.authorships as a " + "unwind a.institutions as i " + "merge (work:Work{id:r.id}) ON CREATE SET work.title = r.display_name, work.doi = r.ids.doi, work.oa = r.open_access.is_oa, work.publication_date = date(r.publication_date), work.alex_last_update = date(r.updated_date) ON MATCH SET work.title = r.display_name, work.doi = r.ids.doi, work.oa = r.open_access.is_oa, work.publication_date = date(r.publication_date), work.alex_last_update = date(r.updated_date) " + "merge (p:Person{id:a.author.display_name}) ON CREATE SET p.oa_id = a.author.id, p.orcid = a.author.orcid ON MATCH SET p.oa_id = a.author.id, p.orcid = a.author.orcid " + "merge (inst:Institution{id: coalesce(i.id, 'unknown_' ) }) " + "ON CREATE set inst.oa_id = i.id, inst.name = i.display_name, inst.country = i.country_code " + "merge(p)-[:Authored]->(work) " + "merge(p)-[:MemberOf]->(inst)"

# Execute the CQL query

while n <= 50:
    with graphDB_Driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(create_works)
#    for node in nodes:
#        print(node)
    create_works = (
        f"CALL apoc.load.json('file:///Users/tfluhr/Desktop/json_dir/{n}.json') yield value " +
        "unwind value.results as r " + "unwind r.authorships as a " +
        "unwind a.institutions as i " +
        "merge (work:Work{id:r.id}) ON CREATE SET work.title = r.display_name, work.doi = r.ids.doi, work.oa = r.open_access.is_oa, work.publication_date = date(r.publication_date), work.alex_last_update = date(r.updated_date) ON MATCH SET work.title = r.display_name, work.doi = r.ids.doi, work.oa = r.open_access.is_oa, work.publication_date = date(r.publication_date), work.alex_last_update = date(r.updated_date) " +
        "merge (p:Person{id:a.author.display_name}) ON CREATE SET p.oa_id = a.author.id, p.orcid = a.author.orcid ON MATCH SET p.oa_id = a.author.id, p.orcid = a.author.orcid " + "merge (inst:Institution{id: coalesce(i.id, 'unknown_' ) }) " +
        "ON CREATE set inst.oa_id = i.id, inst.name = i.display_name, inst.country = i.country_code " +
        "merge(p)-[:Authored]->(work) " +
        "merge(p)-[:MemberOf]->(inst)"
    )
    n += 1
    print(create_works)
