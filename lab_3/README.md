Lab 3- W255
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
##### 1.) What are the benefits of caching?
Caching enables us to store previous queries and responses. This helps us to return the response to the client without having to run the method that corresponds to the endpoint. This ultimately speeds up the response time in our application while also eliminating calls and cost that will occur due to making predictions. In cases where we send large amounts of data, or our application is being hit more often caching will have a larger impact. 


##### 2.) What is the difference between Docker and Kubernetes?
Docker is a virtualized framework that consists of containers that can hose things such as an API, database, or caching service. This framework runs on top of an operating system and ensures that the application hosting can run as long as a compatible docker version is installed. To use these elements in tandem they must be able to communicate with each other, this happens in docker through a network. As we begin to scale the complexity in docker becomes exponentially more complicated, so Kubernetes was created to help with this problem. Kubernetes runs on top of docker and coordinates communication between the containers, services, load balancers, and other objects. It handles things such as scaling, resource allocation, and load balancing to name a few. In our case, we use docker to create the containers for our API, and Redis caching, then test them using docker networks through docker-compose. We then deploy them using Kubernetes to handle the complexities allowing us to focus on the deployment aspect instead of dealing with the minute details. In summation, Docker is normally used to create containers, and local or small-time testing while Kubernetes is used for deployment into the production enviroment.


##### 3.) What does a kubernetes deployment do?
In it's simplest form a kubernetes deployment is the blueprind for the pod that will be created. Inside of the configuration file for the deployment you can choose to specify things such as the container(s), ports, docker image, app name, etc. This means that when the replica set is created from the configuration file it will have a number of identical pods which all have the settings listed in the configuration file.


##### 3.) What does a kubernetes service do?
In it's simplest form a kubernetes service connects multiple pods to facilitate communication between them. An example would be how we had services for both our redis caching database and our api. This allowed our API to communicate with the redis container by giving it an ip address, and our API to communicate with incoming commands when testing our using our application. 




