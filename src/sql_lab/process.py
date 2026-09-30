import os
import logging
import pandas as pd
import mysql.connector


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def read_data(filename):
    """Read a CSV file and return it as a pandas DataFrame."""

    logging.info("Reading data from %s", filename)

    # Read CSV into a DataFrame
    data = pd.read_csv(filename)

    logging.info("Data successfully loaded")
    return data


def clean_data(data):
    """Remove rows containing missing values and return a cleaned DataFrame."""

    logging.info("Cleaning data")

    # Remove any rows that contain missing values
    cleaned_data = data.dropna().copy()

    # Make sure id is stored as an integer
    cleaned_data["id"] = cleaned_data["id"].astype(int)

    logging.info("Data successfully cleaned")
    return cleaned_data


def load_data(data, table):
    """Create the mock table if needed and upload the DataFrame to MySQL."""

    logging.info("Connecting to MySQL")

    connection = None
    cursor = None

    try:
        # Read database information from environment variables
        connection = mysql.connector.connect(
            host=os.environ["DBHOST"],
            database=os.environ["DBNAME"],
            user=os.environ["DBUSER"],
            password=os.environ["DBPASS"]
        )

        cursor = connection.cursor()

        # Create the mock table if it does not already exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS mock (
            id INT PRIMARY KEY,
            `group` VARCHAR(50),
            last_name VARCHAR(100),
            email VARCHAR(255),
            gender VARCHAR(20),
            ip_address VARCHAR(45)
        )
        """

        cursor.execute(create_table_query)

        logging.info("Table '%s' is ready", table)

        # Parameterized INSERT query
        insert_query = """
        INSERT INTO mock
            (id, `group`, last_name, email, gender, ip_address)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Upload each row to MySQL
        for _, row in data.iterrows():
            cursor.execute(
                insert_query,
                (
                    int(row["id"]),
                    row["group"],
                    row["last_name"],
                    row["email"],
                    row["gender"],
                    row["ip_address"]
                )
            )

        # Save changes to the database
        connection.commit()

        logging.info("Uploaded %d rows to '%s'", len(data), table)

    except Exception as error:
        logging.error("Error uploading data: %s", error)

    finally:
        # Close database resources
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def main():
    """Run the complete CSV cleaning and database upload process."""

    logging.info("Starting data processing")

    # Read the CSV
    data = read_data("MOCK_DATA.csv")

    # Clean the data
    data = clean_data(data)

    # Always upload to a table named mock
    load_data(data, "mock")

    logging.info("Processing complete")


if __name__ == "__main__":
    main()