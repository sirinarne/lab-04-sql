import os
import logging
import mysql.connector


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def get_connection():
    """Create and return a connection to the MySQL database."""

    logging.info("Connecting to MySQL database")

    # Read database credentials from environment variables
    connection = mysql.connector.connect(
        host=os.environ["DBHOST"],
        database=os.environ["DBNAME"],
        user=os.environ["DBUSER"],
        password=os.environ["DBPASS"]
    )

    return connection


def get_data_by_group(value):
    """Return all rows from mock where the `group` column equals value."""

    logging.info("Retrieving rows where group = %s", value)

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT *
        FROM mock
        WHERE `group` = %s
    """

    cursor.execute(query, (value,))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    logging.info("Retrieved %d rows", len(rows))

    return rows


def plot_counts(groupby):
    """Count and return rows for each distinct value of the specified column."""

    logging.info("Counting rows grouped by %s", groupby)

    # Only allow columns that exist in the mock table
    allowed_columns = {
        "id",
        "group",
        "last_name",
        "email",
        "gender",
        "ip_address"
    }

    if groupby not in allowed_columns:
        raise ValueError("Invalid column name")

    connection = get_connection()
    cursor = connection.cursor()

    # Choose the query based on the requested column
    queries = {
        "id": """
            SELECT id, COUNT(*) AS count
            FROM mock
            GROUP BY id
            ORDER BY count DESC
        """,
        "group": """
            SELECT `group`, COUNT(*) AS count
            FROM mock
            GROUP BY `group`
            ORDER BY count DESC
        """,
        "last_name": """
            SELECT last_name, COUNT(*) AS count
            FROM mock
            GROUP BY last_name
            ORDER BY count DESC
        """,
        "email": """
            SELECT email, COUNT(*) AS count
            FROM mock
            GROUP BY email
            ORDER BY count DESC
        """,
        "gender": """
            SELECT gender, COUNT(*) AS count
            FROM mock
            GROUP BY gender
            ORDER BY count DESC
        """,
        "ip_address": """
            SELECT ip_address, COUNT(*) AS count
            FROM mock
            GROUP BY ip_address
            ORDER BY count DESC
        """
    }

    query = queries[groupby]

    cursor.execute(query)
    counts = cursor.fetchall()

    cursor.close()
    connection.close()

    logging.info("Finished counting rows by %s", groupby)

    return counts


def main():
    """Demonstrate the query functions using the mock table."""

    # Find all records belonging to group a
    group_data = get_data_by_group("group a")
    print("Rows in group a:")
    print(group_data)

    # Count records for each gender
    gender_counts = plot_counts("gender")
    print("\nCounts by gender:")
    print(gender_counts)


if __name__ == "__main__":
    main()