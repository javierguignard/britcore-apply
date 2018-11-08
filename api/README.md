# REST API FOR BRITCORE PROJECT
A flask-driven restful API for FeatureRequest interactions

* #### Environment Variables
    ```
    export SECRET="some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
    export APP_SETTINGS="development"
    export DATABASE_URL="sqlite:///prod.db" #Or mysql, postgresql, etc.
    ```


* #### Install your requirements
    ```
    (venv)$ pip install -r requirements.txt
    ```

* #### Migrations
    On your psql console, create your database:
    
    ```
    (venv)$ python manage.py db init

    (venv)$ python manage.py db migrate
    ```

    And finally, migrate your migrations to persist on the DB
    ```
    (venv)$ python manage.py db upgrade
    ```
    
* #### Testing
    On your terminal, run the server using this one simple command:
    ```
    (venv)$ python manage.py test
    ```


* #### Running It
    On your terminal, run the server using this one simple command:
    ```
    (venv)$ python manage.py runserver
    ```
    You can now access the app on your local browser by using
    ```
    http://localhost:5000/api/features_requests/
    ```
    Or test creating feature_requests using Postman


* #### Use Docker
    Build docker image with Dockerfile:  
    ```  
    api/ $docker build -t frapi .  
    ```  
    Use this image like:  
    ```bash1
    docker run --name=my-container-api -d -p 5000:5000 frapi 
    ```    