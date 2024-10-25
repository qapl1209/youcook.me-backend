Python version: 3.12.6

Spinning up mongo docker container:
```
docker run -d --name my_mongodb --network my_network -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME= <mongo_user> -e MONGO_INITDB_ROOT_PASSWORD= <mongo_password> mongo

```

To run locally (first cd to src folder):
```
uvicorn main:app --host 127.0.0.1 --port 8000
```

Sources:

Project Structure\
```https://github.com/JakubPluta/gymhero/ ```

MongoDB Integration w/ FastAPI\
```https://github.com/mongodb-developer/mongodb-with-fastapi/tree/master?tab=readme-ov-file```
