# Multi-Environment Deployment Setup

This repository now supports automatic deployment to separate environments based on Git branches.

## Environment Strategy

| Branch Pattern | Namespace       | Environment | Use Case                 |
| -------------- | --------------- | ----------- | ------------------------ |
| `main`         | `project`       | PROD        | Production deployment    |
| `dev`          | `env-dev`       | DEV         | Any development activity |
| `feature/*`    | `env-feature-*` | DEV         | Feature testing          |

For example:

- **main branch** → deploys to `project` namespace (production)
- **dev branch** → deploys to `env-dev` namespace
- **feature/auth** → deploys to `env-feature-auth` namespace
- **feature/new-ui** → deploys to `env-feature-new-ui` namespace

## How It Works

### Automatic Deployments

When you push code to any tracked branch that is defined above:

1. **Docker images** are built and tagged with `branch-sha`.
2. **Namespace** is created automatically if it doesn't exist.
3. **All resources** (deployments, services, ingress, etc.) are deployed to the branch-specific namespace.
4. **Rollout status** is monitored to ensure successful deployment.

### Environment Isolation

Each branch, which follows the strategy explained above, gets:

- Its own Kubernetes namespace
- Separate deployments, services, and ingress
- Isolated database (StatefulSet)
- No interference with other environments

## GitHub Environments

Currently, we have two GitHub Environments:

### 1. PROD

- Used for: `main` branch deployments
- Secrets required:
  - `GKE_SA_KEY`: Service account key for GKE
  - `GKE_PROJECT`: GCP project ID

### 2. DEV

- Used for: `dev` and `feature/*` branches
- Secrets required:
  - `GKE_SA_KEY`: Same service account key as mentioned above.
  - `GKE_PROJECT`: Same GCP project ID as mentioned above.

## Usage

### Deploy a Feature Branch

```bash
git checkout -b feature/my-feature
# Make your changes
git add .
git commit -m "Add new feature"
git push origin feature/my-feature
```

This automatically:

1. Triggers the workflow.
2. Creates `env-feature-my-feature` namespace.
3. Deploys your feature to that namespace.

### Manual Deployment

You can manually trigger deployment via GitHub Actions UI:

1. Go to **Actions** tab.
2. Select **Release application** workflow.
3. Click **Run workflow** button on the right side.
4. Put the branch name to be deployed to the `Branch to deploy` field.

### Check Your Deployment

```bash
# List all namespaces
kubectl get namespaces

# Check pods in your feature namespace
kubectl get pods -n <correct_namespace>

# Check services
kubectl get services -n <correct_namespace>

# Check ingress
kubectl get ingress -n <correct_namespace>
```

### Cleanup

When you're done with a feature branch and want to delete it, the automatic clean-up workflow is triggered after running the following commands:

```bash
git branch -D <branch_name>             # delete the branch locally
git push origin --delete <branch_name>  # delete the branch in the remote which triggers the workflow
```

## Workflow Files

- `.github/workflows/main.yaml` - Main deployment workflow
- `.github/workflows/cleanup.yaml` - Environment cleanup workflow

## Configuration

### Modifying Tracked Branches

Edit the `on.push.branches` field in `.github/workflows/main.yaml`:

```yaml
on:
  push:
    branches:
      - main
      - dev
      - "feature/**" # Track all feature branches
      - "hotfix/**" # EXAMPLE: Add this to also track hotfix branches
```

### Changing Namespace Naming

Edit the following line in `.github/workflows/main.yaml`:

```bash
echo "NAMESPACE=env-$BRANCH_SAFE" >> $GITHUB_ENV
```

## Best Practices

1. **Delete feature branches** after merging to cleanup resources.
2. **Use meaningful branch names** since they become part of the namespace,
3. **Monitor namespaces** periodically and cleanup unused ones.
4. **Use DEV environment** for non-production branches to save costs.
5. **Test in feature branch** before merging to main.
