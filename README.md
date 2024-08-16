This project demonstrates how to create an Apache Beam pipeline that reads CSV files from Google Cloud Storage, transforms the data, and loads it into a BigQuery table. The pipeline is executed using Google Cloud Dataflow.

Prerequisites
Before you begin, ensure you have the following:

Google Cloud Project: You need a Google Cloud project with billing enabled.
Google Cloud SDK: Installed and authenticated on your local machine.
Python 3.7+: Ensure you have Python 3.7 or higher installed.
Virtual Environment: (Optional) Create and activate a virtual environment for your project.
Setup
1. Clone the repository
Clone this repository to your local machine:
git clone https://github.com/yourusername/pipelineboti.git
cd pipelineboti
2. Create a Virtual Environment (Optional)
Create and activate a virtual environment:
python -m venv pipeline_env
source pipeline_env/bin/activate  # On Windows: pipeline_env\Scripts\activate
3. Install Dependencies
Install the required Python packages using pip:
pip install -r requirements.txt
4. Set Up Google Cloud
Ensure your Google Cloud project is set up with the following:

BigQuery: A dataset and table where the CSV data will be loaded.
Google Cloud Storage Bucket: A bucket to store the CSV files and temporary Dataflow files.
5. Update Pipeline Configuration
Modify main.py to set your Google Cloud project, GCS bucket, and BigQuery table details:
options.view_as(GoogleCloudOptions).project = 'your-project-id'
options.view_as(GoogleCloudOptions).temp_location = 'gs://your-temp-bucket/temp/'
options.view_as(GoogleCloudOptions).staging_location = 'gs://your-staging-bucket/staging/'
options.view_as(GoogleCloudOptions).job_name = f"csv-to-bq-pipeline-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
Running the Pipeline
Once everything is set up, run the pipeline using the following command:
python main.py
The pipeline will:

Read CSV files from the specified Google Cloud Storage bucket.
Transform the data as needed.
Load the transformed data into the specified BigQuery table.
Handling Errors
If you encounter a DataflowJobAlreadyExistsError, this means a job with the same name is already running. The job name must be unique, so it's advised to append a timestamp or unique identifier to the job name (this is already handled in the code).

Monitoring the Job
You can monitor the pipeline execution in the Google Cloud Console.

Cleaning Up
To avoid incurring unnecessary charges:

Cancel any running Dataflow jobs from the Google Cloud Console.
Delete any temporary files from your Google Cloud Storage bucket.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Apache Beam for providing the unified programming model.
Google Cloud Platform for hosting and computing services.
