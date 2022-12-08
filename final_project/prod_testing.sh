echo "starting minikube"
minikube start --kubernetes-version=v1.23.8

echo"Logging into Azure"
az login --tenant berkeleydatasciw255.onmicrosoft.com
az account set --subscription="6baae99a-4d64-4071-bfac-c363e71984c3"
az aks get-credentials --name w255-aks --resource-group w255 --overwrite-existing
kubectl config use-context w255-aks
az acr login --name w255mids

NAMESPACE=marcusmanos

#TAG='112820220912'
TAG="$(date +'%Y-%m-%d_%H-%M')"
echo "TAG" $TAG
sed "s/\[TAG\]/$TAG/g" .k8s/overlays/prod/patch-deployment-project_copy.yaml > .k8s/overlays/prod/patch-deployment-project.yaml

#ACR
IMAGE_PREFIX=marcusmanos
echo "IMAGE_PREFIX: " $IMAGE_PREFIX

IMAGE_NAME=project
ACR_DOMAIN=w255mids.azurecr.io
IMAGE_FQDN="${ACR_DOMAIN}/${IMAGE_PREFIX}/${IMAGE_NAME}:${TAG}"
echo "IMAGE_NAME: " $IMAGE_NAME
echo "ACR_DOMAIN: " $ACR_DOMAIN
echo "IMAGE_FQDN: " $IMAGE_FQDN

az acr login --name w255mids

echo "building & running docker container"
echo "Building Container"
docker build -t ${IMAGE_NAME}:${TAG} -f mlapi/Dockerfile .
#docker build --platform linux/amd64 -t ${IMAGE_NAME}:${TAG} -f lab_4/Dockerfile . #made this change
echo "Start Container in detached mode"
docker run --rm --name project -d -p 8000:8000 ${IMAGE_NAME}:${TAG}


docker tag ${IMAGE_NAME}:${TAG} ${IMAGE_FQDN}
docker push ${IMAGE_FQDN}
docker pull ${IMAGE_FQDN}

echo "Generate & apply kustomize files"
kubectl kustomize .k8s/overlays/prod
kubectl apply -k .k8s/overlays/prod

NAMESPACE=marcusmanos
kubectl get pods --namespace=$NAMESPACE
kubectl get services --namespace=$NAMESPACE


echo "testing '/predict' endpoint"
curl -X 'POST' \
  'https://marcusmanos.mids255.com/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"text": ["I hate you.", "I love you."]}'

curl -X 'GET' \
    'https://marcusmanos.mids255.com/health' \
    -H 'accept: application/json'
