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