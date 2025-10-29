import logging
from datetime import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure logging
LOG_FILE = "/tmp/crmreportlog.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

@shared_task
def  generatecrmreport():
    """
    Generate a weekly CRM report via GraphQL and log it to /tmp/crm_report_log.txt
    """
    # Setup GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    # GraphQL query for customers, orders, and total revenue
    query = gql("""
    query {
        totalCustomers
        totalOrders
        totalRevenue
    }
    """)

    try:
        response = client.execute(query)
        customers = response.get("totalCustomers", 0)
        orders = response.get("totalOrders", 0)
        revenue = response.get("totalRevenue", 0.0)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue"
        logging.info(log_message)
        print("CRM Report logged successfully!")

    except Exception as e:
        logging.error(f"GraphQL query failed: {e}")
        print(f"Error generating report: {e}")
