# Kubernetes Practices

> Releases can be found with the name `x.x` (e.g., 1.5) under chapters.

## Table of Content
- [Releases](#releases)
- [Chapters](#chapters)
    - [Chapter 1](#chapter-1)
    - [Chapter 2](#chapter-2)
    - [Chapter 3](#chapter-3)
    - [Chapter 4](#chapter-4)
- [Info about Clusters and Contexts](#info-about-clusters-and-contexts)


## Releases

- [3.1](https://github.com/berkturetken/kubernetes-practices/tree/3.1/ping_pong)

<br>

- [2.10](https://github.com/berkturetken/kubernetes-practices/tree/2.10/todo_app)
- [2.9](https://github.com/berkturetken/kubernetes-practices/tree/2.9/todo_app/todo_generator)
- [2.8](https://github.com/berkturetken/kubernetes-practices/tree/2.8/todo_app)
- [2.7](https://github.com/berkturetken/kubernetes-practices/tree/2.7/ping_pong)
- [2.6](https://github.com/berkturetken/kubernetes-practices/tree/2.6/todo_app)
- [2.5](https://github.com/berkturetken/kubernetes-practices/tree/2.5/log_output)
- [2.4](https://github.com/berkturetken/kubernetes-practices/tree/2.4/todo_app)
- [2.3](https://github.com/berkturetken/kubernetes-practices/tree/2.3/log_output)
- [2.2](https://github.com/berkturetken/kubernetes-practices/tree/2.2/todo_app)
- [2.1](https://github.com/berkturetken/kubernetes-practices/tree/2.1/log_output)

<br>

- [1.13](https://github.com/berkturetken/kubernetes-practices/tree/1.13/the_project)
- [1.12](https://github.com/berkturetken/kubernetes-practices/tree/1.12/the_project)
- [1.11](https://github.com/berkturetken/kubernetes-practices/tree/1.11)
- [1.10](https://github.com/berkturetken/kubernetes-practices/tree/1.10/log_output)
- [1.9](https://github.com/berkturetken/kubernetes-practices/tree/1.9/ping_pong)
- [1.8](https://github.com/berkturetken/kubernetes-practices/tree/1.8/the_project)
- [1.7](https://github.com/berkturetken/kubernetes-practices/tree/1.7/log_output)
- [1.6](https://github.com/berkturetken/kubernetes-practices/tree/1.6/the_project)
- [1.5](https://github.com/berkturetken/kubernetes-practices/tree/1.5/the_project)
- [1.4](https://github.com/berkturetken/kubernetes-practices/tree/1.4/the_project)
- [1.3](https://github.com/berkturetken/kubernetes-practices/tree/1.3/log_output)
- [1.2](https://github.com/berkturetken/kubernetes-practices/tree/1.2/the_project)
- [1.1](https://github.com/berkturetken/kubernetes-practices/tree/1.1/log_output)


## Chapters

### Chapter 1

Just the *Getting started* chapter.

### Chapter 2

- [1.1](https://github.com/berkturetken/kubernetes-practices/tree/1.1/log_output)
    - `k3d cluster create -a 2`: creates a Kubernetes cluster with 2 agent nodes
    - `k3d kubeconfig get k3s-default`: view the content of kubeconfig
    - `kubectl config use-context k3d-k3s-default`: set the context to the correct cluster
    - `kubectl cluster-info`: get the information about the cluster
    - `k3d cluster stop`: stop a cluster
    - `k3d cluster start`: start a cluster
    - `k3d cluster delete`: delete a cluster
    - `kubectl create deployment hashgenerator-dep --image=jakousa/dwk-app1`: deploy an application and we need a deployment object for that
    - `kubectl get pods`: list all objects of a pod
    - `kubectl get deployments`: list all objects of a deployment
    - `kubectl explain RESOURCE`: get a simple explanation of a resource
    - `kubectl logs -f RESOURCE_NAME`: get logs of a resource
- [1.2](https://github.com/berkturetken/kubernetes-practices/tree/1.2/the_project)
    - `kubectl delete deployment DEPLOYMENT_NAME`: take an existing deployment down
    - `kubectl apply -f manifests/deployment.yaml`: apply a deployment
- [1.3](https://github.com/berkturetken/kubernetes-practices/tree/1.3/log_output)
- [1.4](https://github.com/berkturetken/kubernetes-practices/tree/1.4/the_project)
    - Instead of deleting the deployment and applying it again when there is a change, utilize tags! If we come up with a new tag, we don't need to delete the deployment. Instead, just apply the deployment with the new tag. Therefore, basic workflow might look like this:
        - `docker build -t <image>:<new_tag>`
        - `docker push <image>:<new_tag>`
        - Edit the `deployment.yaml` file with the new tag
        - `kubectl apply -f manifests/deployment.yaml`
    - Tools to debug
        - `kubectl describe RESOURCE RESOURCE_NAME`: get as much as info about a resource
        - `kubectl logs`: follow the logs of (possibly) broken software
        - `kubectl delete`
    - `kubectl port-forward POD_NAME LOCAL_PORT:CONTAINER_PORT`: forward a local port to a pod. Allows you to easily access application running inside your Kubernetes cluster. Not meant for a production use but very useful for debugging and development purposes.
- [1.5](https://github.com/berkturetken/kubernetes-practices/tree/1.5/the_project)
    - `k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2`: open local 8081 to 80 in k3d-k3s-default-serverlb and local 8082 to 30080 in k3d-k3s-default-agent-0.
- [1.6](https://github.com/berkturetken/kubernetes-practices/tree/1.6/the_project)
- [1.7](https://github.com/berkturetken/kubernetes-practices/tree/1.7/log_output)
- [1.8](https://github.com/berkturetken/kubernetes-practices/tree/1.8/the_project)
- [1.9](https://github.com/berkturetken/kubernetes-practices/tree/1.9/ping_pong)
- [1.10](https://github.com/berkturetken/kubernetes-practices/tree/1.10/log_output)
    - `empytyDir volumes`: are shared filesystems inside a pod which means their lifecycle is tied to a  pod. When the pod is destroyed the data is lost.
    - `Persistent volumes`: cluster-wide resource which represents a piece of storage in the cluster that has been provisioned by the cluster administrator or is dynamically provisioned.
        - PVs have a lifecycle independent of any individual pod that uses the PV.
        - `local` PVs uses a path in a cluster node as the storage. This solution ties the volume to a particular node and if the node becomes unavailable, the storage is not usable. Therefore, local PVs are not a solution which can be used in *production*.
- [1.11](https://github.com/berkturetken/kubernetes-practices/tree/1.11)
- [1.12](https://github.com/berkturetken/kubernetes-practices/tree/1.12/the_project)
- [1.13](https://github.com/berkturetken/kubernetes-practices/tree/1.13/the_project)

### Chapter 3

- Kubernetes includes a DNS service. Containers in a pod share the network. As such, every other container inside a pod is accessible from localhost. For communication between pods, a *Service* resource is used as they expose the Pods as a network service. Alternatively, each pod has an IP created by Kubernetes.
- We can have a debugging `Pod` resource (do note that not a `Service`) which means we can go inside a pod and send a request to another pod (busybox is a good option for this purpose).
- `kubectl exec -it todo-app-7784476879-mvhd7 -- sh`: Open a shell in a pod
- `kubectl exec -it my-busybox -- wget -qO - http://todo-backend-svc:2345`: Fetch the content from the service todo-backend-svc on port 2345 and prints the result to the terminal.
- You get the same result by using the service cluster IP address. Check the address through `kubectl get svc`. And then, `kubectl exec -it my-busybox -- wget -qO - http://10.43.89.182:2345`.
- We can also access the pod directly. Get the IP address through the command `kubectl describe pod <pod_name>`. Then, `kubectl exec -it my-busybox wget -qO - http://10.42.0.63:3000`. Remember to use the targetPort from the *Service* resource here.
- Note that in contrast to the last part, we have now created a stand-alone pod in our cluster, there was no deployment object at all.
- In general, these kinds of "stand-alone" pods are good for debugging but *all application pods should be created by using a deployment*. The reason for this is that if a node where the pod resides crashes, the stand-alone pods are gone! When a pod is controlled by a deployment, Kubernetes takes care of redeployment in case of node failures.

- [2.1](https://github.com/berkturetken/kubernetes-practices/tree/2.1/log_output)
- [2.2](https://github.com/berkturetken/kubernetes-practices/tree/2.2/todo_app)

- Namespaces are used to keep resources separated. For example, A company that uses one cluster but has multiple projects can use namespaces to split the cluster into virtual clusters, one for each project. Most commonly, they would be used to separate environments such as production, testing, staging.
-  DNS entry for services includes the namespace so you can still have projects communicate with each other if needed through `service.namespace` address. For example, if there is a service called cat-pictures in a namespace ns-test, it could be reached from other namespaces via `http://cat-pictures.ns-test`.
- `k create namespace <namespace_name>`: create a namespace
- `k get all --all-namespaces`: see everything
- `k get pods -n kube-system`: see what the namespace kube-system has
- Namespaces should be kept separate - for example, we could run all of the examples and do the exercises of this course in a cluster that is shared with critical software but that would not be a smart thing to do. An administrator should set a *ResourceQuota* for that namespace, so that you can safely run anything there.
- `k config set-context --current --namespace=<name>`: set the namespace to be used by default

- [2.3](https://github.com/berkturetken/kubernetes-practices/tree/2.3/log_output)
- [2.4](https://github.com/berkturetken/kubernetes-practices/tree/2.4/todo_app)

- `Secrets` are for sensitive information that are given to containers on runtime.
- `ConfigMaps` are quite much like secrets but they may contain any kind of configurations.
    - Use case; we may have a `ConfigMap` mapped to a file with some values that the server reads during runtime.
- Both can also be used to introduce environment variables.
- `Secrets` use base64 encoding to avoid having to deal with special characters.
- `echo -n '<your_string>' | base64`: create a base64 encoded string.
- But we want more than base64 encoding because anyone can reverse the base64 version and therefore we can't save that to version control. Also, since we might want to store our configuration into a long-term storage, we need to encrypt the value.
- Possible solutions:
    - `Cloud service providers` may have their own solution such as AWS Secrets Manager
    - `SealedSecrets`, Kubernetes native solution
    - `SOPS` to encrypt the secret.yaml file
- We will use `SOPS` with the `age` encryption.
- Steps are as follows:
    - `age-keygen -o key.txt`: create a key-pair where public and private keys are stored.
    - `sops --encrypt --age <YOUR_PUBLIC_KEY> --encrypted-regex '^(data)$' secret.yaml > secret.enc.yaml`: encrypts only the data field(s) in the *secret.yaml* file using SOPS and age, and writes the encrypted result to the *secret.enc.yaml* file.
    - `export SOPS_AGE_KEY_FILE=$(pwd)/key.txt && sops --decrypt secret.enc.yaml > secret.yaml`: decrypt the encrypted file by exporting the key file in *SOPS_AGE_KEY_FILE* environment variable and run sops with the -—decrypt flag.
    - `sops --decrypt secret.enc.yaml | kubectl apply -f -`: apply a secret yaml via piping directly (this helps avoid creating a plain *secret.yaml* file)
- `ConfigMaps` are similar but the data doesn't have to be encoded and is not encrypted. ConfigMaps can be added to the container as a volume. By changing a value and applying the ConfigMap, the changes would be reflected in that volume.

- [2.5](https://github.com/berkturetken/kubernetes-practices/tree/2.5/log_output)
- [2.6](https://github.com/berkturetken/kubernetes-practices/tree/2.6/todo_app)

- `StatefulSets` are similar to `Deployments` except they make sure that if a pod dies, the replacement is *identical with the same network identity and name*.
    - If a pod is scaled, each copy have its own storage.
    - `StatefulSets` are for stateful applications and they are ideal for scaling apps that require persistent state.
    - They ensure data safety by not deleting the associated volumes when the `StatefulSet` is deleted.
    - `Deployment` creates pods using `ReplicaSet`.
    - `StatefulSet` requires a *Headless Service* to be responsible for the network identity.
        - Headless service with `clusterIp: None` instructs Kubernetes not to do proxying or load balancing but instead allows direct access to the Pods.
    - If the containers are inside the same pod, they share the network.
    - `StatefulSets` look like a `Deployment` resource but uses a `volumeClaimTemplate` to claim its own volume for each pod. `volumeClaimTemplate` also creates PVC for each replicas in the set.
    - We can dynamically provision storage by specifying `storageClassName: local-path` in which K3s takes care of that for us. No need to create a PV for the volume.
    - When we delete a `StatefulSet`, the volume will stay and bind back when we apply the `StatefulSet` again.
    - `StatefulSet` creates separate volumes for all replicas.
    - We can directly access to the pods with the headless service. Using its name would be enough since it resolves to the pod's IP address.
    - If you nslookup to the service, you will see that the service resolves to two (if we set two replicas) different IP addresses.
    - Once again, the identities of the pods are permanent. In other words, if one of the pods dies, it is guaranteed to have the same name (when it is scheduled again) and it is still attached to the same volume.
    - `k run debug-shell --rm -it --image nicolaka/netshoot -n <your_namespace> -- bash`: creates a temporary debugging pod in the Kubernetes cluster. Good for troubleshooting network connectivity issues, examining cluster DNS resolution, running diagnostic tools not available in the application containers, etc. Note that this image comes with many networking tools pre-installed. Other options might be the followings:
        - `k run debug-shell --rm -it --image ubuntu:20.04 -n <your_namespace> -- bash`: use Ubuntu's base image instead
        - `k run busybox --rm -it --image busybox -n <your_namespace> -- sh`: use Ubuntu's base image instead
        - `k debug -it <pod-name> --image ubuntu:20.04 --target=<container-name>`: use a debugging container

- [2.7](https://github.com/berkturetken/kubernetes-practices/tree/2.7/ping_pong)
- [2.8](https://github.com/berkturetken/kubernetes-practices/tree/2.8/todo_app)
- [2.9](https://github.com/berkturetken/kubernetes-practices/tree/2.9/todo_app/todo_generator)

- Monitoring
    - We utilize `Prometheus` to monitor the cluster and `Grafana` to view the data.
    - `Helm`: the package manager for Kubernetes. We can manage the applications with `Helm` more easily.
        - Uses a packaging format called *charts* to define the dependencies of an application.
        - Helm charts include information for the version of the chart, the requirements of the application, such as the Kubernetes version as well as other charts that it may depend on.
    - We can add some official charts to the repo:
        - `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`
        - `helm repo add stable https://charts.helm.sh/stable`
        - `helm repo update`
    - Install `kube-prometheus-stack`:
        - `kubectl create namespace prometheus`: By default, `kube-prometheus-stack` puts everything to the *default* namespace which we want to avoid.
        - `helm install prometheus-community/kube-prometheus-stack --generate-name --namespace prometheus`
        - This installs core components of the `kube-prometheus-stack`, a collection of Kubernetes manifests, Grafana dashboards, and Prometheus rules combined with documentation and scripts to provide easy to operate end-to-end Kubernetes cluster monitoring with Prometheus using the Prometheus operator.
    - Install `Loki` which is a log aggregiation system so that we can see the application logs.
    - `Loki` comes with `Promtail` which is a logs collector built specifically for Loki. In other words, Promtail ships the contents of local logs to private Grafana Loki instance (or Grafana Cloud). It primarily does the following three things:
        - Discovers targets.
        - Attaches labels to log streams.
        - Pushes them to the Loki instance.
    - Overall, how does Grafana Loki work?
        - Pull in any logs with Promtail.
        - Store the logs in Loki.
        - Use LogQL within Grafana (you can also utilize LogCLI) to explore.
        - Alert on your logs by sending them to a Prometheus Alertmanager.
    - Instead of Promtail, we should use Grafana Alloy since commercial support of Promtail will end on Feb 28, 2026. Subsequently, Promtail will reach its EOL on Mar 2, 2026, meaning that afterwards no future support or updates will be provided.

- [2.10](https://github.com/berkturetken/kubernetes-practices/tree/2.10/todo_app)

### Chapter 4

- Until now, we have used Kubernetes distribution K3s using Docker container via k3d. But in production environments, maintaining a Kubernetes cluster can be a burden.
- If the company/organization has the hardware, then it makes sense to manage the Kubernetes cluster.
- Set up the Google Cloud Platform:
    - Use the free 300$ credits by opening a new account.
    - Create a new project in the `Resource` page.
    - Install Google Cloud SDK by following the instructions [here](https://cloud.google.com/sdk/install).
    - Set the previously created project to be used by the `gcloud config set project <project_name>-<project_id>` command. This can also be achieved in the previous step.
    - Create a cluster: `gcloud container clusters create <cluster_name> --zone=europe-north1-b --cluster-version=1.32 --disk-size=32 --num-nodes=3 --machine-type=e2-micro` - Accept the enabling of Kubernetes Engine API so that it will be used in the project. Or use the following command: `gcloud services enable container.googleapis.com`

- [3.1](https://github.com/berkturetken/kubernetes-practices/tree/3.1/ping_pong)

## Info about Clusters and Contexts

- A *cluster* entry defines how to connect to a specific Kubernetes API server. It includes a server address (URL), CA and other connection details.
- A *context* is a named set of access parameters that tells kubectl which cluster, which user and optionally which namespace to use by default. It acts as a shortcut for switching between different clusters, users and namespaces.
- In short, *cluster* is all about where to connect and *context* is all about how to connect.
- Since I have many clusters such as k3d-edge-local, minikube, EKS clusters; it is better to list all contexts that I have: `k config get-contexts`.
- Set the context for this project's cluster which is the default one: `k config use-context k3d-k3s-default`
- Check your cluster is running: `k3d cluster list`. An example output would be:
    ```
    NAME          SERVERS   AGENTS   LOADBALANCER
    k3s-default   1/1       2/2      true
    ```
- If it is not running, start the cluster: `k3d cluster start <cluster_name>`
- Check the pods in all namespaces and verify that you're in the correct one: `k get po --all-namespaces`
