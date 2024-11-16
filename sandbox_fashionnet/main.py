import pymysql
import csv

# Database connection details
host = '127.0.0.1'
user = 'root'
password = 'kaleb'
database = 'Datathon24'

# Connect to MySQL database
connection = pymysql.connect(host=host, user=user, password=password, database=database)
cursor = connection.cursor()

# Path to your CSV file
csv_file_path = 'C:/Users/kwolf/OneDrive/Desktop/Projects/datathonFME24/archive/product_data.csv'

# Open and read the CSV file
with open(csv_file_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)  # Skip the header row (if exists)

    # Prepare SQL query for inserting data
    insert_query = "INSERT INTO product_data (cod_modelo_color, des_filename, cod_color, des_color, des_sex, des_age, des_line, des_fabric, des_product_category, des_product_aggregated_family, des_product_family, des_product_type, attribute_name, test_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # Insert each row of data into the table
    for row in csvreader:
        cursor.execute(insert_query, row)

    # Commit the changes
    connection.commit()

# Close the connection
cursor.close()
connection.close()
