import json
import requests

from conf import config
from gql import Client
from gql.transport.requests import RequestsHTTPTransport

headers = {
    'Content-Type': "application/graphql",
    'x-api-key': config.API_KEY,
    'cache-control': "no-cache",
}

sample_transport = RequestsHTTPTransport(
    url=config.API_ENDPOINT + '/graphql',
    use_json=True,
    headers=headers,
    verify=False,
    retries=3,
)
client = Client(
    transport=sample_transport,
    fetch_schema_from_transport=True,
)


