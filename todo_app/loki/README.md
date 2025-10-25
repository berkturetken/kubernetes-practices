# Loki

## How to install Loki?

- Add Grafana's chart repository to Helm:
  - `helm repo add grafana https://grafana.github.io/helm-charts`
- Update the chart repository:
  - `helm repo update`
- Create configuration file like `values.yaml`.
- Install or upgrade the Loki deployment
  - `helm install loki grafana/loki --values values.yaml -n loki-stack`
  - `helm upgrade loki grafana/loki --values values.yaml -n loki-stack`
