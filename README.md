<p align="center">
  <h3 align="center">Simplicar API</h3>

  <p align="center">
    API for SimpliCar
  </p>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
The company has developed a platform where you can manage High, Low, Modification of libraries, books and authors.
Among the services provided, one is the generation of a public site where users can discover these products
and buy them. The platform has an API implemented which will provide all the necessary information
for the rendering of products, transactions and lead generation.

### Requirements

Create a model called "Leads" with the following fields:
    ● email
    ● Full name
    ● Phone
    ● Library (Existing Model Reference)

Build REST API with the following endpoints and actions:

    Library (ABM)
    Model: Library
    Path: domain / api / library / {id}
    Permitted Actions: GET | POST | PUT
    Response format: JSON

    Library (Filter)
    Model: Library
    Path: domain / api / library / {id} / books / {id}
    Allowed Actions: GET
    Response format: JSON

    Books
    Model: Book
    Path: domain / api / book / {id}
    Permitted Actions: GET | POST | PUT
    Response format: JSON

    Books (Search)
    Model: Book
    Path: domain / api / book / search? Text = ”book title”
    Allowed Actions: GET
    Response format: JSON

    Authors
    Model: Book
    Path: domain / api / author / {id}
    Permitted Actions: GET | POST | PUT
    Response format: JSON

    Leads
    Model: Lead
    Path: domain / api / lead
    Allowed Actions: POST
    Response format: JSON

### Built With

●	Python 3
●	Django
●	Django REST framework
●	JWT ó API KEY
●	Unit test
●	Docker
●	Automatic email sending

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites for Local Development
* Python Programming Language
* Django Framework
* Django Rest Framework

### Installation 

1. Clone the repo
   ```sh
   git clone https://github.com/josebrz/SimpliCar.git
   ```
2. Change directory to SimpliCar
   ```sh
   cd SimpliCar
   ```
3. Install python module dependencies
   ```sh
   pip install -r requirements.txt
   ```
4. Run migrations and api server
   ```sh
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
   ```

### Using Docker Compose
1. Clone the repo
   ```sh
   git clone https://github.com/josebrz/SimpliCar.git
   ```
2. Change directory to SimpliCar
   ```sh
   cd SimpliCar
   ```
3. Build and start containers with docker-compose
   ```sh
   docker-compose up
   ```

<!-- USAGE EXAMPLES -->
## Usage

* Open http://127.0.0.1:8000/api/auth/register and register your user
* Open http://127.0.0.1:8000/api-token-auth/ and crate your token with your username and password and copy the token(ctrl + c)
* Using Postman and import file colection_postman.json and set Authorization with type "Bearer Token" and past your token in
  and paste your token in the Token box, here you can test the different end points
* In the post endpoint you can change the request to GET and get all the records from the table
* When creating a Lead an email will be sent to the message box of "simplicartestapp@gmail.com",
  you can check it by entering that box with the password "simpli12345"
* In the code you can test the different TEST that I have created by running the command "python manage.py test"

###NOTE
The port set is 0.0.0.0:8000 but the port that must be used in the browser is 127.0.0.1:8000,
 in postman the requests are well configured and you should not modify them


<!-- CONTACT -->
## Contact

José Brizuela - jose.brizuela9512@gmail.com