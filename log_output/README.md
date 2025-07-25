# Log Output

## How to run the application? (1.3)
`kubectl apply -f log_output/manifests/deployment.yaml`

## First deployment (1.1)
- Create the application --> main.py
- Write the Dockerfile to build the image --> Dockerfile
- Build a docker image: `docker build -t <docker-username>/log-output:latest .`
- Push the docker image to a container registry (in this case, Docker Hub): `docker push <docker-username>/log-output:latest`
- See the image in Docker Hub (https://hub.docker.com/u/berkturetkenwartsila)
- See the image locally: docker images
- Deploy it into the Kubernetes cluster that we already have: `kubectl create deployment log-output --image=berkturetkenwartsila/log-output`
- Check the logs of the pod and verify that it works as intended: `kubectl logs -f log-output-8557476c45-qr8l5` (note that pod name might change)