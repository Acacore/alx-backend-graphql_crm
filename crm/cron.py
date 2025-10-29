import logging
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"

def log_crm_heartbeat():
    """Logs a timestamped heartbeat message and optionally checks GraphQL health."""
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    # Write to /tmp/crm_heartbeat_log.txt (append mode)
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

    # Optional: GraphQL health check
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=2,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql("""{ hello }""")
        response = client.execute(query)
        hello_msg = response.get("hello", "No response")
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} GraphQL hello response: {hello_msg}\n")
    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} GraphQL query failed: {e}\n")
