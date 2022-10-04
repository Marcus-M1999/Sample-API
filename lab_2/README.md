Lab 1- W255
===============
## Documentation

##### 1.) What your application does
This application has basic functionality to say hello in response to a piece of text, and make predictions from a SVM model. Predictions are made by using the /predict endpoint and sending data in the following JSON format:
> '{"MedInc": float, "HouseAge": float, "AveRooms": float, "AveBedrms": float, "Population": float, "AveOccup": float, "Latitude": float, "Longitude": float}'

The output from this model is a float that estimates the value of a home with the above characteristics.
Additionally, this application supports the /docs endpoint which supports the "open API" documentation. Although nothing is only the default information there currently, it has the potential to clarify API arguments.

##### 2.) How to build your application
To build the application you can simply run the run.sh script under the first lab_2 folder. This will build the application and quickly show that it is working. If you desire to take a closer look at the API for an extended period you can just the docker file to build and run the container with the following commands:

> docker build -t lab2_deployed: -f lab_2/Dockerfile .

> docker run --rm --name lab_2 -d -p 8000:8000 lab1_deployed

Note: this will tag the image as "lab2_deployed" if you wish to tag the image as a different name simply change the parameter after "-t" in the docker build command. The same methodology applied to the name of the container "lab_1", simply change this parameter. Remember to change the image name (the final parameter in "docker run") so it corresponds to the tag for the image.
In the same way, you can change the ports being used by changing the "8000:8000" parameter in the "docker run" command, where the first number refers to the port on the container, and the second number refers to the port on your local machine that you wish to map to the container. Changes may also need to be made to the Dockerfile exposing the appropriate port.


#####  3.) How to run your application
To run the application you can navigate to [http://localhost:8000/docs](http://localhost:8000/docs). This will give you an overview of how the /hello method works and allow you to test it with a given URL. 
Note: If you change the port on your local machine in the docker run command, then you must also update the URL accordingly.  

#####  4.) How to test your application
A small number of sample tests are located under the test directory, in a file called "test_sample.py". Tests are integrated with poetry and pytest, so if you're running the files locally you can simple run the following command in the tests directory to run unit testing. 

> poetry run pytest

Additional tests may be added as desired, using the existing testing format from the FastAPI library.


## Questions
##### 1.) What does Pydantic handle for us?
Pydantic is an open-source library that can be used to validate incoming data as well as confirm that outgoing data matches a format. This is helpful in our case since it provides an easy-to-understand format of what the input data should be, and allows us to validate that it follows that exact format preventing errors from arising due to an unknown data format.


##### 2.) What do GitHub Actions do?
GitHub actions is a tool that automates the continuous integration and continuous delivery (CI/CD) tasks to make them easier for engineers. It accomplishes this by having a set of jobs that can include actions (such as pulling new files from your repository or setting up an environment) and scripts that can accomplish similar tasks. The automation of these monotonous steps removes the possibility of error along with any human bottlenecks (ie: someone is out to lunch and forgot to open a pull request)  since it's automated. In our case we set up GitHub Actions to create a virtual environment and run integration testing once a pull request is created. This automates a previously human-centered process, making it more efficient. 


##### 3.) In 2-3 sentences (plain language), describe what the Sequence Diagram below shows.
the sequence diagram below shows how the data flows in our system. It begins when a user pings our API with the payload and goes through steps 1 & 2 until it satisfies the pydantic validation tests. After our data flow to the model, which makes a prediction and then sends the data back to the API. In the final step, it gets output to the user (in our case as a number representing the value of a home).





