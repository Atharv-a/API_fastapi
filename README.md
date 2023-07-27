# Social_Media API
- Developed a RESTful API using FastAPI, enabling users to perform CRUD operations on posts.
- Implemented PostgreSQL as the backend database with the help of SQLAlchemy as the ORM(Object Relational mapping) for handling SQL queries.
- Validated API functionality using Postman, ensuring accurate request/response handling and adherence to API specifications.
- Created a CI/CD pipeline using GitHub Actions, automating the testing, building, and deployment processes for the API.
- Hosted the API using Render hosting services, ensuring reliable and scalable deployment of the application.

## Repository Walkthrough
* **app**</br>
   Main code for the API is in app directory.
   App directory consists of
   - **router directory**
   All the operations that API support are stored in the router directory in different files on the basis of type of operation
      - **post** (all the CRUD operations that can be performed on the posts)
      - **user** (operations for sign in/log in and authenticating user)
      - **votes** (operations for casting and keeping track of votes on posts)
   - **main** (responsible to integrate all operation files in the API)
   - **auth,oauth2,utils** (they contains utility funtions used in authentication of user)
   - **schema** (defines the specifice schema that a data being send to/received by API  should follow)
   - **database,models,config**  (these files create connection to database, define table and schemas for respective table and provide session when there is a need to read/write in database)
* **tests**</br>
  tests directory contains files for testing the API. These test files are executed everytime ci/cd pipline is triggered.
  - **database** (this file contains code the creates  temporary database for test to use)
  - **confest** ( definition of the fixture functions in this file to make them accessible across multiple test files)
  - **test_posts,test_users,test_votes** (these files contains tests to check that all functions of API are working properly)
* **.github/workflow**</br>
  Contains **build-deploy** file which defines the ci/cd pipline.
* **Alembic,ALembic.ini**</br>
  ALembic provides version control for the databases.
* **DockerFile,docker_compose-dev,docker_compose-dev**</br>
  DockerFile Specifies How a image will be created and build, docker-compose files build containers according to specified steps to run applications

## Try out API
 Refer to https://social-media-api-do4q.onrender.com/docs for documentation and to try out API.
