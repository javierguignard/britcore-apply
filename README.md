# This is the project for Britecore Engineering Application

This project is for apply to job on Britecore enterprise.
Contains two parts, API and Frontend. 

## Restful API  
The API was created with Flask, using ORM SQLAlchemy and sqlite, 
but is factible to use another app.
I thought it was a good idea create functions for call another systems. 
These other systems respond 
with data like as list of clients, areas of the company or authentication system.  
Those functions start with the name dummy_

## Frontend
The frontend were create as one page site, using bootstrap and knockoutjs.
Is a very simple CRUD was call restful API.

## Infraestructure
I make Dockerfiles for two applications. 
For API I use python3 and run server with Flask uwsgi emmbebbed.
It's not really good, for production environments you need use a real server, 
like as gunicorn or mod_wsgi for apache.
For the frontend, I use nginx like as webserver and config this as a proxy server 
to integrate two URLS in only one domain.
 
 
 ## How to start.
 0. Install [docker](https://docs.docker.com/install/) 
 and [docker-compose](https://docs.docker.com/compose/install/)
 1. Clone this repo
 2. Call docker-compose up
 3. Go to your prefered browser and put http://localhost/ in your navigation bar.
 4. Use the system :)
 
 ## Things to keep in mind
 
 Configure your docker-compose if you need change port 
 (default is in 80, but all webservers run in this port)