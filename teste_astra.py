from astrapy import DataAPIClient

# Initialize the client
client = DataAPIClient("AstraCS:ilQehQeSTBxiCRepglElcUso:d40a28189a7819139734572534f3822ace543b3c37352c8355ffa479b29ac0a9")
db = client.get_database_by_api_endpoint(
  "https://987b5868-c001-4dd5-93c8-c955d5cb27f5-us-east-2.apps.astra.datastax.com"
)

print(f"Connected to Astra DB: {db.list_collection_names()}")