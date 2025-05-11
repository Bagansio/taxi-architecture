import pulumi
import pulumi_gcp as gcp


PROJECT_ID = pulumi.Config().require("gcp:project")

def create_service_account(name: str, display_name: str, roles: list[str], project_id: str = PROJECT_ID):
    """
    Creates a service account and assigns the given roles to it.
    
    Parameters:
    - name: The base name for the service account.
    - display_name: The display name of the service account.
    - roles: List of roles to assign to the service account.
    - project_id: The GCP project ID
    
    Returns:
    - The created service account.
    """
    sa = gcp.serviceaccount.Account(
        f"{name}-sa",
        account_id=name,
        display_name=display_name,
        project=project_id,
    )

    for i, role in enumerate(roles):
        gcp.projects.IAMMember(
            f"{name}-iam-{i}",
            project=project_id,
            role=role,
            member=sa.email.apply(lambda email: f"serviceAccount:{email}"),
        )

    pulumi.export(f"{name}_sa_email", sa.email)
    return sa
