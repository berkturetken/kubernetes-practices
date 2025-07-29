# ToDo App

## How to run the backend and frontend applications locally?
- Run `source venv/bin/activate`.
- Run `python3 todo_app/todo_backend/backend.py` for backend when you are in the root folder of the project.
- Run `python3 todo_app/todo_frontend/frontend.py` for frontend when you are in the root folder of the project.

## How to run it in a Kubernetes cluster?
- Run `docker build -t <docker-username>/the_project:latest .` to build a docker image if there is a change in the source code.
- Run `docker push <docker-username>/the_project:latest` to push the docker image to Docker Hub.
- Run `k apply -f todo_app/todo_backend/manifests/deployment.yaml`. Assume that *Service* and *Ingress* resources are already placed in the cluster.
- Check the logs if necessary: `k logs -f <pod_name>`

## Some useful commands
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