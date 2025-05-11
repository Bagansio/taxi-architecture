from core.utils import create_service_account
from core.dataflow import enable_dataflow_api, create_dataflow
from utils import TAXI_PREFIX
from pubsub import TAXI_STATUS_NAME, TAXI_EVENTS_NAME

TAXI_DATAFLOW_TEMPLATE_PATH = "gs://my-bucket/templates/taxi-dataflow-job"
TAXI_DATAFLOW_JOB_NAME = f"{TAXI_PREFIX}-dataflow"
TAXI_DATAFLOW_SA_NAME = f"{TAXI_PREFIX}-dataflow-sa"

def create_taxi_dataflow_sa(project_id: str):
    """
    Creates a Dataflow Service Account with the necessary roles to read from Pub/Sub and write to BigQuery.

    Parameters:
    - name: The base name for the service account.
    - project_id: The GCP project ID where the Service Account will be created (default is the project_id from utils).

    Returns:
    - The created Service Account.
    """

    # Roles for Dataflow (Pub/Sub, BigQuery, Dataflow Worker)
    roles = [
        "roles/pubsub.subscriber",  # Read from Pub/Sub
        "roles/bigquery.dataEditor",  # Write to BigQuery
        "roles/dataflow.worker",  # Dataflow worker permissions
    ]

    return create_service_account(TAXI_DATAFLOW_SA_NAME, "Taxi Dataflow Service Account", roles, project_id) 


def deploy_taxi_dataflow_pipeline(region: str, project_id: str):
    """
    Deploy a Dataflow job using a Flex Template.

    Args:
        region (str): The region to deploy the Dataflow job.
        project_id (str): The GCP project ID.

    Returns:
        gcp.dataflow.FlexTemplateJob: The deployed Dataflow job resource.
    """

    enable_dataflow_api(project_id)

    dataflow_service_account = create_taxi_dataflow_sa(project_id)

    parameters = {
        "inputTopic": TAXI_STATUS_NAME,
        "outputTopic": TAXI_EVENTS_NAME,
    }

    dataflow_job = create_dataflow(TAXI_DATAFLOW_JOB_NAME, region, project_id, TAXI_DATAFLOW_TEMPLATE_PATH, parameters, dataflow_service_account.email)