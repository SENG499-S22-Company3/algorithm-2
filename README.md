# algorithm-2

## Local Environment Setup
1. Ensure `python-3.10` and Heroku CLI tools are installed
2. Virtual environment setup: `python3.10 -m venv venv`
3. Activate venv: `source venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`
5. Run the app: `./bootstrap.sh`
## Heroku Deployment
Login to Heroku CLI:
`heroku login`

Add git remote:
`git remote add heroku https://git.heroku.com/algorithm-2.git`

Push to Heroku Production (ONLY PUSH FROM MAIN BRANCH):
`git add ...`
`git commit -m "..."`
`git push heroku main`

## Local Flask Deployment
To run the application, run:
`./bootstap.sh`

Navigate to http://localhost:5000/ to view the entire list of courses in the BSEng program.

Navigate to http://localhost:5000/seng to just view courses required for Algorithm 2.
These courses are filtered by the "Computer Science" and "Software Engineering" departments.

To issue an HTTP GET request, run:
`curl http://localhost:5000`
or
`curl http://localhost:5000/seng`

To issue an HTTP POST request, run:
```
curl -X POST -H "Content-Type: application/json" -d '{
    "name": "<COURSE NAME>"
}' http://localhost:5000/
```

The only required field is "name" (string).
Other possible fields are "department" (string), "class_size" (int), "semester" (int), "year" (int), "prereqs" (list(list(str))).

```
curl -X POST -H "Content-Type: application/json" -d '{
    { "subject": <COURSE SUBJECT>,
     "code": <COURSE CODE>,
      "seng_ratio": <RATIO OF SENG STUDENTS>,
      "semester": <SEMESTER>,
      "capacity": <CAPICITY OF COURSE>}
}' http://localhost:5000/
```

 The required fields are "subject" (string), "code" (string), "seng_ratio" (int), "semester" (string), and "capacity" (int).

 The capcity of the course must be set to 0 for the machine learning model to predict a course capcity, or else the same
 capacity value will be returned.
