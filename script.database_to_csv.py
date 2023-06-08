import sqlite3
import csv


DATA_BASE_PATH = 'data/old.db.sqlite3'

def export_table_to_csv(table_name, file_name):
    # Connect to the database
    conn = sqlite3.connect(DATA_BASE_PATH)
    cursor = conn.cursor()

    # Execute a query to fetch data from the table
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()

    # Get the column names from the cursor description
    column_names = [description[0] for description in cursor.description]

    # Create and open the CSV file in write mode
    path = 'data/'
    with open(path+file_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write the column names as the header row
        writer.writerow(column_names)

        # Write the data rows
        writer.writerows(rows)

    # Close the cursor and connection
    cursor.close()
    conn.close()


export_table_to_csv(table_name='leads_agent',file_name='Agents.csv')
export_table_to_csv(table_name='leads_lead',file_name='Leads.csv')
export_table_to_csv(table_name='leads_transaction',file_name='Transactions.csv')
export_table_to_csv(table_name='company_expend',file_name='Expanses.csv')
