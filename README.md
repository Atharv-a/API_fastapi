# Social_Media API
- Developed a RESTful API using FastAPI, enabling users to perform CRUD operations on posts.
- Implemented PostgreSQL as the backend database with the help of SQLAlchemy as the ORM(Object Relational mapping) for handling SQL queries.
- Validated API functionality using Postman, ensuring accurate request/response handling and adherence to API specifications.
- Created a CI/CD pipeline using GitHub Actions, automating the testing, building, and deployment processes for the API.
- Hosted the API using Render hosting services, ensuring reliable and scalable deployment of the application.

Documentation for API https://social-media-api-do4q.onrender.com/docs

## Repository Walkthrough
* **app**</br>
   Main code for the API is in app directory.
   App directory consists of
   **router directory**
   All the operations that API support are stored in the router directory in different files in on the basis of type of operation
   - post (All the CRUD operations the can be performed on the posts)
   - user (Operations for sign in/log in and authenticating user)
   - votes (operations for casting and keeping track of votes on posts)
   - main (Responsible to integrate all operation files in the API)
   - auth,oauth2,utils (It contains utility funtions used in authentication of user)
   - schema (defines the specifice schema that a data being send to/received by API  should follow)
   - database,models,config  (these files create connection to database, define table and schemas for respective table and provide session when need read/write in database)
* **tests**</br>
  tests directory contains files for testing the API. These test case are executed everytime ci/cd pipline is triggered.
  - **database** (this file contains code the creates  temporary database for test to use)
  - **confest** ( definition of the fixture functions in this file to make them accessible across multiple test files)
  - **test_posts,test_users,test_votes** (these files contains tests to check that all functions of API are working properly)

