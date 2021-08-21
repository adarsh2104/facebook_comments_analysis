##                                [Facebook Comment Analyzer](https://github.com/adarsh2104/facebook_comments_analysis)  

A REST API based applications with following salient features:

### [Frontend](https://github.com/adarsh2104/facebook_comments_analysis/tree/main/frontend-app): React.JS 


1. Home Page:
  * A Form where the user can specify the keyword and start the search.
  * Previous search keywords are shown as search suggestions.

<p align="center"><img width="100%" height="700px" src="https://github.com/adarsh2104/facebook_comments_analysis/blob/main/Visuals/01.Home_page.png"></img></p>

2.Query Search:
  * Added a loader component to show processing request [react-loader](https://www.npmjs.com/package/react-loader)
<p align="center"><img width="100%" height="700px" src="https://github.com/adarsh2104/facebook_comments_analysis/blob/main/Visuals/02.Send_query_request.png"></img></p>

3.Results Page:
  * Comments arranged in tabular format with percentage of sentiment scores.
  * Cummalative sentiment is dispalayed along with the search term.
  * Conditional rendering of elements attributes based on state variables.

<p align="center"><img width="100%" height="700px" src="https://github.com/adarsh2104/facebook_comments_analysis/blob/main/Visuals/03.Results_page.png"></img></p>


### [Backend](https://github.com/adarsh2104/facebook_comments_analysis/tree/main/request_client): Python + Djnago REST + Django REST

4.[Views](https://github.com/adarsh2104/facebook_comments_analysis/blob/main/request_client/views.py):
 * Class Based API Views for GET and POST requests.
 * Used Django for Rest APIs.
 * Model Serializers for serializing/deserializing objects of PostComment and SearchKeyword Models.
 * Added logger for debugging the project.

5.[Models](https://github.com/adarsh2104/facebook_comments_analysis/blob/main/request_client/models.py):
 * Models for saving Search Keywords and PostComments
 * Implemented Foreign Key relation between the models.

6.[Utils](https://github.com/adarsh2104/facebook_comments_analysis/tree/main/request_client/utils):
 * Selenium based request client for collecting comments from Facebook posts,taking screenshots and getting matching results.
 * Saperate directory for saving Search termwise comments [screenshots](https://github.com/adarsh2104/facebook_comments_analysis/tree/main/Screenshots) 
 * Text analyzer implemented using [NTLK package](https://www.nltk.org/)

### [Database](https://github.com/adarsh2104/facebook_comments_analysis/tree/main/mysql-table-structure): SQL
 * Used MySQL database for saving [Search Keywords](https://github.com/adarsh2104/facebook_comments_analysis/blob/main/mysql-table-structure/facebook_data_tables.sql) and [Post Comments](https://github.com/adarsh2104/facebook_comments_analysis/blob/main/mysql-table-structure/facebook_data_tables.sql).
 
 <p align="center"><img width="100%" height="700px" src="https://github.com/adarsh2104/facebook_comments_analysis/blob/main/Visuals/05.Search_keyword.png"></img></p>
 <p align="center"><img width="100%" height="700px" src="https://github.com/adarsh2104/facebook_comments_analysis/blob/main/Visuals/06.PostCommenst.png"></img></p>
 
 
 ## Running the code : On Ubuntu

### Frontend: 

Navigate to the `frontend-app directory`:

```bash
cd frontend-app
```

Install the dependencies from npm:

``` bash
sudo npm install
```

Run the dev server (starts on localhost:3001/3000):

```bash
sudo npm start
```

### Backend:

To get the Django server running:

Install the requirements from pip

```bash
pip install -r requirements.txt
```

Run django's development server (starts on localhost:8000):

```bash
python manage.py runserver
```


### Stacks Used:
* Python 3.7
* Django 3.2.6
* React.JS/CSS
* MySQL


### NOTE:
Add your own Facebook login credentials in Django settings file for testing the project. :star2::star2::star2:

