from core.pubsub import create_pubsub, enable_pubsub_api

TAXI_STATUS_NAME = "taxi-status"
TAXI_EVENTS_NAME = "taxi-events"

def deploy_taxi_pubsub(region: str, project_id: str):
    """
    Deploys taxi-related Pub/Sub topics and subscriptions for a given region.
    
    :param region: Region where the resources will be deployed
    :return: Tuple of Pub/Sub topics and subscriptions
    """
    enable_pubsub_api()
    taxi_status_topic, taxi_status_subscription = create_pubsub(TAXI_STATUS_NAME, region, project_id)
    taxi_events_topic, taxi_events_subscription = create_pubsub(TAXI_EVENTS_NAME, region, project_id)
    
    return (taxi_status_topic, taxi_status_subscription), (taxi_events_topic, taxi_events_subscription)
