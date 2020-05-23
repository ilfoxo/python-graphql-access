import json
import requests

from conf import config
from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from graphql import build_ast_schema, parse

headers = {
    'Content-Type': "application/graphql",
    'x-api-key': config.API_KEY,
    'cache-control': "no-cache",
}

with open('conf/schema.graphql') as source:
    document = parse(source.read())
schema = build_ast_schema(document)

sample_transport = RequestsHTTPTransport(
    url=config.API_ENDPOINT + '/graphql',
    use_json=True,
    headers=headers,
    verify=False,
    retries=3,
)
client = Client(
    transport=sample_transport, schema=schema
)


