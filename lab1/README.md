Lab 1- W255
===============
## Documentation

##### 1.) What your application does
My application is a version of the popular entry-level program "Hello World". It takes in an argument for the /hello command and as long as something is input it will return:
> "{"name": "Hello " + name}"

Additionally, this application supports the /docs endpoint which supports the "open API" documentation. Although nothing is only the default information there currently, it has the potential to clarify API arguments.

##### 2.) How to build your application
To build the application you can simply run the run.sh script under the first lab1 folder. This will build the application and quickly show that it is working. If you desire to take a closer look at the API for an extended period you can just the docker file to build and run the container with the following commands:

> docker build -t lab1_deployed: -f lab1/Dockerfile .

> docker run --rm --name lab_1 -d -p 8000:8000 lab1_deployed

Note: this will tag the image as "lab1_deployed" if you wish to tag the image as a different name simply change the parameter after "-t" in the docker build command. The same methodology applied to the name of the container "lab_1", simply change this parameter. Remember to change the image name (the final parameter in "docker run") so it corresponds to the tag for the image.
In the same way, you can change the ports being used by changing the "8000:8000" parameter in the "docker run" command, where the first number refers to the port on the container, and the second number refers to the port on your local machine that you wish to map to the container. Changes may also need to be made to the Dockerfile exposing the appropriate port.


#####  3.) How to run your application
To run the application you can navigate to [http://localhost:8000/docs](http://localhost:8000/docs). This will give you an overview of how the /hello method works and allow you to test it with a given URL. 
Note: If you change the port on your local machine in the docker run command, then you must also update the URL accordingly.  

#####  4.) How to test your application
A small number of sample tests are located under the test directory, in a file called "test_sample.py". Tests are integrated with poetry and pytest, so if you're running the files locally you can simple run the following command in the tests directory to run unit testing. 

> poetry run pytest

Additional tests may be added as desired, using the existing testing format from the FastAPI library.


## Questions
##### 1.) What status code should be raised when a query parameter does not match our expectations?
When a query parameter does not match our expectations we raise HTML status code 422, which refers to a "request that was well-formed but unable to be followed due to semantic errors" ([source](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#client_error_responses)). Note that the API does not check for logical errors such as including numbers, or symbols that may not normally be in names.

##### 2.) What does Python Poetry handle for us?
Poetry acts as our dependency and package manager. This means that it will install and update the libraries that we specify. It does this by tracking them in the poetry.lock file, acting similar to a requirements.txt file but with superior features since it will update the libraries. We also used Poetry to create the file structure of an src directory, and tests directory inside of the lab1 directory. Poetry also tracks the configuration we use through the pyproject.toml file. Additionally, we can use poetry to create a virtual environment.


##### 3.) What advantages do multi-stage docker builds give us?
The multi-stage docker build process we went through to create this container gives us a leaner container in terms of size. It does this by removing unnecessary items from the container since we layer the container build we get rid of the unnecessary tools and can have a smaller and faster container for use in a production environment. 





