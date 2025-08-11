# ToDo App

## Implement the followings
- Add request logging which is essentially a print statement so that we can monitor every todo that is sent to the backend.
- Improve the current logging so that we only get what we need

## How to run the backend and frontend applications locally?
- Run `source venv/bin/activate`.
- Run `python3 todo_app/todo_backend/backend.py` for backend when you are in the root folder of the project.
- Run `python3 todo_app/todo_frontend/frontend.py` for frontend when you are in the root folder of the project.

## How to run it in a Kubernetes cluster?
- Run `docker build -t <docker-username>/the_project:latest .` to build a docker image if there is a change in the source code.
- Run `docker push <docker-username>/the_project:latest` to push the docker image to Docker Hub.
- Run `k apply -f todo_app/todo_backend/manifests/deployment.yaml`. Assume that *Service* and *Ingress* resources are already placed in the cluster.
- Check the logs if necessary: `k logs -f <pod_name>`

## How to port forward the backend service to your local to test it easily?
- Run `k -n project port-forward svc/todo-backend-svc 8090:5678`
- `curl http://localhost:8090/todos`: See all todos.
- `curl -X POST -d "todo=add something" http://localhost:8090/todos`: Add a new todo.

## How to see logs in Grafana?
- Port forward kube-prometheus-stack with the following command: `k -n prometheus port-forward kube-prometheus-stack-1754935951-grafana-7466d6bb75-sd2vc 3000`
- Visit `http://localhost:3000/`

## How to set up logging for the application?
- Assuming that helm is installed, add the following:
    - `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`
    - `helm repo add stable https://charts.helm.sh/stable`
    - `helm repo update`
- `k create namespace prometheus`
- `helm install prometheus-community/kube-prometheus-stack --generate-name --namespace prometheus`
    - To get Grafana user password, run `k --namespace prometheus get secrets kube-prometheus-stack-1754935951-grafana -o jsonpath="{.data.admin-password}" | base64 -d ; echo`
        - Pwd: `prom-operator`
        - Username: `admin`
    - Access Grafana local instance by running
    ```bash
    export POD_NAME=$(k --namespace prometheus get pod -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=kube-prometheus-stack-1754935951" -oname)
    k --namespace prometheus port-forward $POD_NAME 3000
    ```
- `k get po -n prometheus`
- `k -n prometheus port-forward kube-prometheus-stack-1754935951-grafana-7466d6bb75-sd2vc 3000`
- Everything should be good by now and access http://localhost:3000 to see the information about the cluster.
- To see the logs of the applications that we're running (that's what we need at the end), let's continue.
- `helm repo add grafana https://grafana.github.io/helm-charts`
- `helm repo update`
- `kubectl create namespace loki-stack`
- If you would like to continue with the older version of Loki, `helm upgrade --install loki --namespace=loki-stack grafana/loki-stack --set loki.image.tag=2.9.3`
- But let's try the new one:
    - (MOST PROBABLY?) `helm upgrade --install loki --namespace=loki-stack grafana/loki --set loki.image.tag=X.X.X`. See this webpage: https://grafana.com/docs/loki/latest/setup/install/helm/install-scalable/
    - Add the line `auth_enabled: false` to the *values.yaml* file. And connection URL must be `http://loki-gateway.loki-stack.svc.cluster.local`.
    - Either install Promtail or Grafana Alloy to aggregate logs from Kubernetes to Grafana by yourself.
        - Promtail needs to be installed by yourself. The correct connection URL that needs to be changed in the *values.yaml* file is `http://loki-gateway.loki-stack.svc.cluster.local/loki/api/v1/push`.
        - Grafana Alloy: no idea how to install. Follow the official doc
- We should be good to go and see the logs of incoming todo requests in Grafana! 


## How to create/activate/deactivate a virtual environment?
- `python3 -m venv venv`: create a virtual environment called venv
- `source venv/bin/activate`: activate the virtual environment
- `deactivate`: deactivate the virtual environment
- `pip3 install -r requirements.txt`: install packages listed in the *requirements.txt* file to the environment

## (Very) initial steps I followed while I was setting up the project for the first time
- Create the application --> main.py
- Write the Dockerfile to build the image --> Dockerfile
- Build a docker image: `docker build -t <docker-username>/the_project:latest .`
- Push the docker image to a container registry (in this case, Docker Hub): `docker push <docker-username>/the_project:latest`
- See the image in Docker Hub (https://hub.docker.com/u/berkturetkenwartsila)
- See the image locally: `docker images`
- Deploy it into the Kubernetes cluster that we already have: `kubectl create deployment todo-app --image=berkturetkenwartsila/the_project`
- Check the logs of the pod and verify that it works as intended: `kubectl logs -f todo-app-76f58f58f9-rcfwg` (note that pod name changes every time there is a new deployment)