import logging
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.request import RequestsHTTPTransport


#configure logging
LOG_FILE = "/tmp/order_reminders_log.txt"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
def main():
    #Define GraphQL endpoing
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    today = datetime.now()
    last_week = today -timedelta(days=7)
    start_date = last_week.strftime("%Y-%m-%d")

    #Define GraphQL query
    query = gql("""
        query RecentOrders($startDate: Date!, $endDate: Date!) {
            orders(orderDate_Gte: $startDate, orderDate_Lte: $endDate) {
                id
                customerEmail
            }
        }
    """)

    # Execute query
    params = {"startDate": start_date, "endDate": end_date}
    try:
        result = client.execute(query, variable_values=params)
        orders = result.get("orders", [])
        if not orders:
            logging.info("No recent orders found.")
        else:
            for order in orders:
                logging.info(f"Order ID: {order['id']}, Email: {order['customerEmail']}")
    except Exception as e:
        logging.error(f"GraphQL query failed: {e}")
        return

    print("Order reminders processed!")

if __name__ == "__main__":
    main()