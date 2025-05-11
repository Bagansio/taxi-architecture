# taxi-architecture

Imagine we are running a global business operating taxis in major cities of the world


### Deploy or update components

You can update individual components or the entire system by rerunning the deployment script. Pulumi will automatically determine what resources need to be updated based on changes in the configuration.

```bash
pulumi up --config <project-name>:project_id=my-project-id --config <project-name>:region=us-central1 --config <project-name>:components='["pubsub"]'
```

### Rollback to Previous Version
Pulumi provides a way to rollback changes if something goes wrong. Use the following steps to revert to a previous state:

#### Check the State History:

```bash
pulumi stack history
```
Rollback to a Previous Version:
If you want to revert to a specific version, run:

```bash
pulumi stack select <stack-name>@<version-id>
```
Apply the Rollback:
After selecting the correct stack version, apply the rollback:

```
bash
pulumi up
```

This will revert the deployed resources to their previous state.