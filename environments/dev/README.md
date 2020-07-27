Quick and dirty way to deploy eks cluster

- terraform plan
- terraform apply

configure kubectl
aws eks --region us-east-2 update-kubeconfig --name <cluser_name>

kubectl get pods
kubectl get svc


kubectl proxy

kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep service-controller-token | awk '{print $1}')