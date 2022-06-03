# algorithm-2
## Heroku Deployment
Login to Heroku CLI:
`heroku login`

Add git remote:
`git remote add heroku https://git.heroku.com/algorithm-2.git`

Push to Heroku Production:
`git push heroku`

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
