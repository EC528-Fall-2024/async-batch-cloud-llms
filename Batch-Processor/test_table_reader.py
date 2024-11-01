from google.cloud import bigquery

client = bigquery.Client()

# Perform a query.
QUERY = ('SELECT plain_text FROM `elated-scope-437703-h9.test_dataset.test_table_with_rows'
    'WHERE row_number = 3')

query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print(row.name)