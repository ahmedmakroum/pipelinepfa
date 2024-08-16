import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions
from apache_beam.io.gcp.bigquery import WriteToBigQuery
from datetime import datetime

# Function to convert microseconds to milliseconds
def convert_time(row):
    row['time_taken_millis'] = row['time_taken_micros'] / 1000
    return row

# Function to filter out rows with non-200 status
def filter_status(row):
    return row['sc_status'] == 200

# Function to extract domain from cs_host
def extract_domain(row):
    row['domain'] = row['cs_host'].split('//')[-1].split('/')[0]
    return row

# Function to convert time_micros to a readable timestamp
def convert_timestamp(row):
    row['timestamp'] = datetime.utcfromtimestamp(row['time_micros'] / 1e6).strftime('%Y-%m-%d %H:%M:%S')
    return row

def run():
    # Define your pipeline options
    options = PipelineOptions()
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = 'arcane-boulder-429415-s1'
    google_cloud_options.region = 'us-central1'
    google_cloud_options.job_name = 'csv-to-bq-pipeline'
    google_cloud_options.staging_location = 'gs://bucketboti1/staging'
    google_cloud_options.temp_location = 'gs://bucketboti1/temp'
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    
    with beam.Pipeline(options=options) as p:
        (p
         | 'Read CSV' >> beam.io.ReadFromText('gs://bucketboti1/bucket1.csv', skip_header_lines=1)
         | 'Parse CSV' >> beam.Map(lambda line: dict(zip(
            ['time_micros', 'c_ip', 'c_ip_type', 'c_ip_region', 'cs_method', 'cs_uri', 'sc_status', 'cs_bytes',
             'sc_bytes', 'time_taken_micros', 'cs_host', 'cs_referer', 'cs_user_agent', 's_request_id', 'cs_operation',
             'cs_bucket', 'cs_object'], line.split(','))))
         | 'Filter Status 200' >> beam.Filter(filter_status)
         | 'Convert Time' >> beam.Map(convert_time)
         | 'Extract Domain' >> beam.Map(extract_domain)
         | 'Convert Timestamp' >> beam.Map(convert_timestamp)
         | 'Write to BigQuery' >> WriteToBigQuery(
                table='arcane-boulder-429415-s1:test.test',
                schema='SCHEMA_AUTODETECT',
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )

if __name__ == '__main__':
    run()


