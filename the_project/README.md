# Steps

- Create the application --> main.py
- Write the Dockerfile to build the image --> Dockerfile
- Build a docker image: `docker build -t <docker-username>/the_project:latest .`
- Push the docker image to a container registry (in this case, Docker Hub): `docker push <docker-username>/the_project:latest`
- See the image in Docker Hub (https://hub.docker.com/u/berkturetkenwartsila)
- See the image locally: docker images
- Deploy it into the Kubernetes cluster that we already have: `kubectl create deployment todo-app --image=berkturetkenwartsila/the_project`
- Check the logs of the pod and verify that it works as intended: `kubectl logs -f todo-app-76f58f58f9-rcfwg` (note that pod name might change)