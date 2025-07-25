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
    - `kubectl logs -f RESOURCE`: get logs of a resource
- [1.2](https://github.com/berkturetken/kubernetes-practices/tree/1.2/the_project)
    - `kubectl delete deployment RESOURCE`: take an existing deployment down
    - `kubectl apply -f manifests/deployment.yaml`: apply a deployment
- [1.3](https://github.com/berkturetken/kubernetes-practices/tree/1.3/log_output)
- [1.4](https://github.com/berkturetken/kubernetes-practices/tree/1.4/the_project)