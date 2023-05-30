# CS50x Final Project - Friendster

Video Demo:  https://youtu.be/5x6yIXBX53Q
Git Repo:  https://github.com/MohamedAmineSafi/cs50x-final-project

Friendster is a website that allows you to store a list of all your friends, their birthdays, hobbies, and personality types. It provides functionalities such as Register, Login, and Change Password. The "Remember Me" feature stores a cookie in the browser containing the JWT token of the user, which remains valid for 3 months. Otherwise, the cookie is valid for the duration of the session.

This project utilizes Django (class-based views) and MongoDB (in the cloud) to store user data. Below is a breakdown of some of the files:

### users/views.py

This file handles the Login, Register, Change Password, and Logout functionalities. If the user tries to access Login, Register, or Change Password pages as a GET request, the server will render the HTML page while passing "isLoggedIn" as a boolean value (which allows the website to load the Navbar links accordingly).

If any of the previously mentioned pages were accessed via a POST request, the server will grab the data, perform some checks, and then save the data to the database.

The logout page works a little differently. The user should access it through a GET request, passing the ID of the "Friend" he wants to delete from the DB. The server will make sure that the currently logged-in user "owns" (is the one who added) this "Friend". If that is the case, the server will delete the instance of the "Friend" from the DB.

### main/views.py

This file handles the home (index) and the Add Friend pages. If the user tries to access the Add Friend page with a GET request, the page renders the form. If the request was a POST request, the server makes sure that the user is logged in using the 'isLoggedIn' function (to be addressed later), then grabs the data the from form, gets the id of the logged in user, and then saves the form data to the DB (linking to his Id).

For the Home page, if the user is not logged in, the page redirects the user to the login page; otherwise, the page gets all "Friends" from the database and passes them to the home page to be shown as a table.

Delete works in the same way, except it deletes the "Friend" after making sure that the current user is the 'owner' of the "Friend".

### utils/isLoggedIn.py

To make life easier, this file stores some functions that are used often. The most important is the 'isLoggedIn' function. This function takes as arguments: the current request object, the "User" model, and the SECRET_KEY.
The function works by first trying to get the JWT Token cookie from the browser; if this fails, it returns False. Then, it looks for the user (from DB) who has the same token; if none are found, it returns False. Then it tries to decode the JWT token. The JWT token is valid for 3 months; if more than 3 months have passed, then the decoding process will fail and the function will return False. If all the above went well, the function returns True, and the user is deemed to be logged in!