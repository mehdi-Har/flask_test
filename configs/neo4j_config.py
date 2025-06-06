from neo4j import GraphDatabase
from urllib.parse import quote_plus

NEO4J_URI = "neo4j+s://236ac439.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = quote_plus("6HMkNw9Oh2s3xX_rH4I9DV4ZT-rSN_z8lsQ24MeZKAg")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
