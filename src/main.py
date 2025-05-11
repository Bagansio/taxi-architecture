import pulumi
from taxi.pubsub import deploy_taxi_pubsub
from taxi.dataflow import deploy_taxi_dataflow_pipeline

def main():
    """
    Main entry point for deploying taxi-related resources using Pulumi.
    
    - Deploys Pub/Sub topics for taxi status and events.
    - Creates Dataflow job.
    - Allows deployment of individual components (Pub/Sub, Dataflow) or both.
    """
    
    try:
        # Get the region, project ID, and components from Pulumi config or flags
        config = pulumi.Config()
        
        region = config.get("region") or "us-central1"  # Default to "us-central1" if not provided
        project_id = config.require("project_id")  # This is required in Pulumi config
        components = config.get("components") or ["pubsub", "dataflow"]

        print(f"Deploying resources in region: {region} for project: {project_id}")
        
        # Initialize Pulumi deployment stack
        with pulumi.Program():
            if 'pubsub' in components:
                print("Deploying Taxi Pub/Sub resources...")
                deploy_taxi_pubsub(region, project_id)
            
            if 'dataflow' in components:
                print("Deploying Taxi Dataflow pipeline...")
                deploy_taxi_dataflow_pipeline(region, project_id)

        pulumi.export("status", "Deployment completed successfully.")
    
    except Exception as e:
        print(f"Error: {e}")
        pulumi.log.error(f"Error during deployment: {e}")
        raise

if __name__ == "__main__":
    main()