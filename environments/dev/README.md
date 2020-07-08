Quick and dirty way to deploy eks cluster

- terraform plan
- terraform apply

configure kubectl
aws eks --region us-east-2 update-kubeconfig --name <cluser_name>

kubectl get pods
kubectl get svc