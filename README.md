# Milestone 1 - project1-cle31
## Heroku app: [https://polar-lowlands-81051.herokuapp.com/]
## Libraries: 
* requests
* os
* flask
* random
* find_dotenv, load_dotenv
## APIs:

* Spotify artist
* Spotify top tracks
* Genius search
## Languages:

* Python
* HTML
* CSS/Flask

## App instruction:

1. Run the following line in terminal:
 
git clone git@github.com:csc4350-f21/project1-cle31.git

2. git install requests

3. git install Flask

4. git install python-dotenv

5. Create .env to store APIs key.

6. Sign up Spotify dev and Genius to key access token to APIs.

7. Run main.py to see the browser.

## a. What are at least 3 technical issues you encountered with your project? How did you fix them?

- I have a problem with finding the right path for fetching the data on spotify and genius APIs since they are stored in a very complocated dict and list so it took me a long time to get the things I want.
- I'm new to CSS and HTML so touching the app was the hardest part for me. I have to look up online to get familiar with padding, border, margin and how to justify block and content the way I want.
- Deploying code to heroku is super confusing and I keep getting error since I was missing the debug = True part in my main.py. Luckily the recording lecture helped me alot.
## b. What are known problems (still existing), if any, with your project?

- The was sometime the page would get error for out of range index and I still don't know why. 

##c. What would you do to improve your project in the future? 

- I would implement it to have more user-interacting such as getting user input and giving recommendations based on user's input.
- A full-list of artist's top tracks.