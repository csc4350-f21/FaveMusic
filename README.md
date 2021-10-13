# Milestone 1 - project1-cle31
## Heroku app: [https://polar-lowlands-81051.herokuapp.com/]
## Libraries: 
* Flask
* python-dotenv
* requests
* Werkzeug
* psycopg2
* flask_login
* flask_sqlalchemy
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


## a. What are at least 2 technical issues you encountered with your project? How did you fix them? What additional features might you implement, and how?

- I implemented the password input for user, saving artist by name only and the place where user can put saved artist name to remove the artist from the saved list.

- For the passoword, when the user sign up for their account, the password they put in will convert into SHA256 to store into db for security purpose using generate_password_hash. At log in page, using check_password_hash to check if the password user put in the same with the one in db, if they are match then log the user in.

- For saving artist by name, I created a html form to get input from user and send the input data into spotify endpoint function to get the artist's ID by searching the given name and get the first artist ID return.

- For removing the artist, I created a html form for user to put in artist name from the visible saved artists list on the page. After getting input from user, use query to find the data row that match that artist name in current user db and delete that row. Therefore, delete the artist from the list.

- For technical issues, I got a KeyError bug sometimes when reloading the home page which belongs to the url_link from genius api. This happened because it always fetch the first link return from the json which is index 0 and sometimes when there isn't a lyrics page for that song, it can't return the link at that index and causing KeyError. To fix this, I catch an except case to return just https://genius.com/ when the KeyError return.

- More one issue is sometimes when I add a new artist, the page return timeout error from sqlalchemy. I went online and found a solution to config the SQLALCHEMY_POOL_SIZE to 20 and SQLALCHEMY_POOL_TIMEOUT to 300.

- The last one is the most struggle one when I didn't know how to deploy the app to heroku and kept  getting error when deploying because I put all the route pages in different file using BluePrint from flask and it run just fine using flask command but to deploy to heroku is a whole different problem than what was coverd in class. So I decided to merge all of it into main.py file and set an ip and port for heroku and it works fine again.


## b. What would you do to improve your project in the future? 

- I would implement it to have more user-interacting such as getting user input and giving recommendations based on user's input. Also more touch to the css for displaying. 

## c. How did your experience working on this milestone differ from what you pictured while working through the planning process? What was unexpectedly hard? Was anything unexpectedly easy?

- From the planning process, I only care about the logic of the page and realized that database modify and deploying are the things I should care about because it took a lot of more time to understand the concept and do it the right way. And for sure, the most annoying things for me are database,models and deploying.