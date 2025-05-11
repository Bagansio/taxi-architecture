import pulumi
import pulumi_gcp as gcp
from utils import PROJECT_ID, create_service_account

DATAFLOW_API = "dataflow.googleapis.com"
ROLE_DATAFLOW_WORKER = "roles/dataflow.worker"
ROLE_DATAFLOW_ADMIN = "roles/dataflow.admin"


def enable_dataflow_api(project_id):
    """
    Enable the Dataflow API for the given project.
    """
    gcp.projects.Service(
        "enable_dataflow_api",
        service=DATAFLOW_API,
        project=project_id,
    )


def create_dataflow(
    name: str,
    region: str,
    project_id: str,
    template_path: str,
    parameters: dict[str, str],
    service_account_email: str | None = None,
):
    """
    Deploy a Dataflow job using a Flex Template.

    Args:
        name (str): The base name of the Dataflow job.
        region (str): The region to deploy the Dataflow job.
        project_id (str): The GCP project ID.
        template_path (str): GCS path to the Flex template (e.g. gs://bucket/templates/my-job).
        parameters (dict[str, str]): Parameters required by the Dataflow template.
        service_account_email (str, optional): Optional service account email to run the job.

    Returns:
        gcp.dataflow.FlexTemplateJob: The deployed Dataflow job resource.
    """
    job = gcp.dataflow.FlexTemplateJob(
        f"{name}-dataflow-job",
        name=name,
        project=project_id,
        region=region,
        container_spec_gcs_path=template_path,
        parameters=parameters,
        service_account_email=service_account_email,
    )

    pulumi.export(f"{name}_dataflow_job_id", job.id)
    return job