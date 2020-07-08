# Quick start for argocd

kubectl create namespace argocd
kubectl get namespace
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
