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

Push to Heroku Production:
`git add ...`
`git commit -m "..."`
`git push heroku main`


