# crm/cron_jobs/send_order_reminders.py

import os
import logging
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure logging
LOG_FILE = "/tmp/order_reminders_log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def send_order_reminders():
    # Setup GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        use_json=True,
        verify=False,  # Optional if using HTTPS locally
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    # Define GraphQL query
    query = gql("""
    query RecentOrders($startDate: Date!, $endDate: Date!) {
        allOrders(orderDate_Gte: $startDate, orderDate_Lte: $endDate) {
            edges {
                node {
                    id
                    orderDate
                    customer {
                        email
                    }
                }
            }
        }
    }
""")

    # 7 days ago
    end_date = datetime.now().date().isoformat()
    start_date = (datetime.now() - timedelta(days=7)).date().isoformat()

    try:
        # Execute query
        response = client.execute(query, variable_values={
                    "startDate": start_date,
                    "endDate": end_date
                })

        orders = response.get("allOrders", {}).get("edges", [])
        if not orders:
            logging.info("No recent orders found.")
            print("No recent orders found.")
            return

        # Log each order
        for order in orders:
            node = order.get("node", {})
            order_id = node.get("id")
            email = node.get("customer", {}).get("email")
            logging.info(f"Order ID: {order_id}, Customer Email: {email}")

        print("Order reminders processed!")

    except Exception as e:
        logging.error(f"GraphQL query failed: {e}")
        print(f"Error: {e}")

# Allow running as standalone script
if __name__ == "__main__":
    send_order_reminders()
