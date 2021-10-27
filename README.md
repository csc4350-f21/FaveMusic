# Flask and `create-react-app`

## Requirements
1. `npm install`
2. `pip install -r requirements.txt`

## Run Application
1. Run command in terminal (in your project directory): `npm run build`. This will update anything related to your `App.js` file (so `public/index.html`, any CSS you're pulling in, etc).
2. Run command in terminal (in your project directory): `app app.py`
3. Preview web page in browser 'localhost:8080/' (or whichever port you're using)

## Deploy to Heroku
1. Create a Heroku app: `heroku create --buildpack heroku/python`
2. Add nodejs buildpack: `heroku buildpacks:add --index 1 heroku/nodejs`
3. Push to Heroku: `git push heroku main`

# Milestone 3 - project1-cle31
## Heroku app: [https://polar-lowlands-81051.herokuapp.com/]
## Libraries: 
* Flask
* python-dotenv
* requests
* Werkzeug
* psycopg2
* flask_login
* flask_sqlalchemy
* uuidv4
## APIs:

* Spotify artist
* Spotify top tracks
* Genius search
* Google Fonts

## Languages:

* Python
* HTML
* CSS/Flask

## App instruction:

1. Run the following line in terminal:
 
   git clone git@github.com:csc4350-f21/project1-cle31.git

2. cd to the directory where remuirements.txt is located.

3. run: pip3 install -r requirements.txt in your shell.

4. Create file name .env in the app directory to store APIs key.

5. Sign up Spotify dev and Genius to key access token to APIs.

6. Sign up heroku account to deploy your app.

7. In your terminal run: heroku login -i

8. Create a new Heroku app: heroku create

9. Create a new remote DB on your Heroku app: heroku addons:create heroku-postgresql:hobby-dev (If that doesn't work, add a -a {your-app-name} to the end of the command, no braces)

10. See the config vars set by Heroku for you: heroku config. Copy paste the value for DATABASE_URL

11. Set the value of DATABASE_URL as an environment variable by entering this in the terminal: export DATABASE_URL='copy-paste-value-in-here

12. In the terminal, run python3 to open up an interactive session.

13. Then type in these Python lines one by one:
>> from app import db
>> import models
>> db.create_all()

14. Add your git to heroku via Heroku CLI: heroku git:remote -a {{your-app-name}}

15. Push your code to heroku using: git push heroku main

16. After the process: heroku open

