import pulumi_gcp as gcp
from utils import PROJECT_ID

ROLE_PUBSUB_PUBLISHER = "roles/pubsub.publisher"
ROLE_PUBSUB_SUBSCRIBER = "roles/pubsub.subscriber"
ROLE_RUN_INVOKER = "roles/run.invoker"

def enable_pubsub_api(project_id: str):
    """
    Enable the Pub/Sub API for the given project.
    """
    gcp.projects.Service("enable_pubsub_api", service="pubsub.googleapis.com", project=project_id)

def create_pubsub(name: str, region: str = "us-central1", project_id):
    """
    Create Pub/Sub Topic and Subscription based on provided name, region, and project_id.
    
    Parameters:
    - name: The base name for the topic and subscription.
    - region: The region for the topic and subscription (default is "us-central1").
    - project_id: The GCP project ID where the resources will be created.
    
    Returns:
    - A tuple containing the created topic and subscription.
    """

    # Create Pub/Sub topic with the provided name, region, and project_id
    topic_name = f"{name}-{region}"
    topic = gcp.pubsub.Topic(
        f"{name}_topic",
        name=topic_name,
        project=project_id  # Specify the project ID for the topic
    )

    # Create Pub/Sub subscription with the provided name, region, and project_id
    subscription_name = f"{name}-sub-{region}"
    subscription = gcp.pubsub.Subscription(
        f"{name}_subscription",
        name=subscription_name,
        topic=topic.name,
        ack_deadline_seconds=20,
        project=project_id  # Specify the project ID for the subscription
    )

    # Export the names of the topic and subscription
    pulumi.export(f"{name}_topic_name", topic.name)
    pulumi.export(f"{name}_subscription_name", subscription.name)
    
    return topic, subscription