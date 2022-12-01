Lab 4- W255
===============
## Documentation

##### 1.) What your application does
This application has basic functionality to say hello in response to a piece of text, and make predictions from a SVM model. Predictions are made by using the /predict endpoint and sending data in the following JSON format:
> '{"MedInc": float, "HouseAge": float, "AveRooms": float, "AveBedrms": float, "Population": float, "AveOccup": float, "Latitude": float, "Longitude": float}'

The output from this model is a float that estimates the value of a home with the above characteristics.
Additionally, this application supports the /docs endpoint which supports the "open API" documentation. Although nothing is only the default information there currently, it has the potential to clarify API arguments.

##### 2.) How to build your application
To build the application you can simply run the run.sh script. This will build the application and quickly show that it is working. If you desire to take a closer look at the API for an extended period you can just the docker file to build and run the container with the following commands:

> docker build -t lab2_deployed: -f lab_2/Dockerfile .

> docker run --rm --name lab_2 -d -p 8000:8000 lab2_deployed

Note: this will tag the image as "lab2_deployed" if you wish to tag the image as a different name simply change the parameter after "-t" in the docker build command. The same methodology applied to the name of the container "lab_1", simply change this parameter. Remember to change the image name (the final parameter in "docker run") so it corresponds to the tag for the image.
In the same way, you can change the ports being used by changing the "8000:8000" parameter in the "docker run" command, where the first number refers to the port on the container, and the second number refers to the port on your local machine that you wish to map to the container. Changes may also need to be made to the Dockerfile exposing the appropriate port.

If you desire to run the kubernetes cluster locally, you can use the following series of commands to create a local kubernetes cluster with minikube and kubectl:

> minikube start --kubernetes-version=v1.23.8
> eval $(minikube docker-env)

> docker build -t lab3_deployed:1.0 -f lab_3/Dockerfile .
> docker run --rm --name lab_3 -d -p 8000:8000 lab3_deployed:1.0

> Kubectl apply -f lab_3/infra/namespace.yaml
> Kubectl apply -f lab_3/infra/deployment-redis.yaml -n w255
> Kubectl apply -f lab_3/infra/service-redis.yaml -n w255
> Kubectl apply -f lab_3/infra/deployment-pythonapi.yaml -n w255
> Kubectl apply -f lab_3/infra/service-prediction.yaml -n w255

Note: This will create a namespace (w255), in order you test the API locally you must setup port forwarding with the following command: 
> kubectl port-forward service/prediction-service 8000:8000


#####  3.) How to run your application
To run the application you can navigate to [http://localhost:8000/docs](http://localhost:8000/docs). This will give you an overview of how the /hello and /predict methods work and allow you to test it with a given URL. 


#####  4.) How to test your application
A small number of sample tests are located under the test directory, in a file called "test_sample.py". Tests are integrated with poetry and pytest, so if you're running the files locally you can simple run the following command in the tests directory to run unit testing. 

> poetry run pytest

To run tests on the kubernetes cluster follow the above steps to setup the cluster, and then test the endpoint with your desired data similar to the following format:

curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "MedInc": [10.0, 10.0],
  "HouseAge": [10.0, 10.0],
  "AveRooms": [10.0, 10.0],
  "AveBedrms": [10.0, 10.0],
  "Population": [10.0, 10.0],
  "AveOccup": [10.0, 10.0],
  "Latitude": [10.0, 10.0],
  "Longitude": [10.0, 10.0]
}'




## Questions
##### 1.) What are the downsides of using latest as your docker image tag?
A docker tag is a series of characters (letters, numbers, slashes, etc.) that follow an image name. They are used to label the image version you plan on using, this allows someone to continuously update the docker image with different versions without interrupting the use of the image by different developers. The latest tag tells Docker to get the latest instance of the image you're using. This could potentially have problems since updates could have security flaws or be incompatible with your current environment. By using a specific docker tag you can control the exact docker image you're using cutting down on any potential security flaws or incompatibilities. 


##### 2.) What does kustomize do for us?
Kustomize is a "configuration manager" for kubectl. This means that it creates templates for your Kubernetes configuration that you can make small changes to deploy different workloads such as deployments, services, or virtual services. One use case for Kustomize is applying changes to a template relating to the docker image. In our case, we used Kustomize to make the necessary small changes to our template used in Lab 3 to deploy our API using Kubernetes to AKS.  





