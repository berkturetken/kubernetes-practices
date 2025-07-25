# Kubernetes Practices

## Exercises

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
