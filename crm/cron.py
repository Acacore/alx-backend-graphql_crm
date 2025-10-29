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
            retries=3,
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



LOG_FILE = "/tmp/low_stock_updates_log.txt"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)



def update_low_stock():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    # GraphQL mutation
    mutation = gql("""
        mutation {
            updateLowStockProducts {
                message
                updatedProducts {
                    id
                    name
                    stock
                }
            }
        }
    """)

    try:
        result = client.execute(mutation)
        data = result.get("updateLowStockProducts", {})
        message = data.get("message", "No message returned.")
        updated_products = data.get("updatedProducts", [])

        if updated_products:
            logging.info(message)
            for p in updated_products:
                logging.info(f"Product: {p['name']} → New stock: {p['stock']}")
        else:
            logging.info(message)

    except Exception as e:
        logging.error(f"GraphQL mutation failed: {e}")
        return

    print("Low-stock products update completed.")
