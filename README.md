<h2>Forrest Chat:</h2> is a chat room application. 
After login successfully, a user has access to chat room website. 
Main functionality is to exchange messages between logged users in real time.


<img src="screenshots\main_site_design.png" width="600" alt="login validators">


25.10.2022:

Main functionality has been achieved by using Flask_Socket_IO library.

User credentials are stored in the database and are queried by SQLAlchemy, when needed.
Login process is established by Flask_login library and WTForms.
Client site shows the history of conversation and shows active, logged users. 
Functionality has been achieved using Jinja, javascript and jquery.
Message window is always scrolled down when new message arrives.


<img src="screenshots\validators_1.png" width="600" alt="login validators">
 


26.10.2022:

Added some CSS styling.

27.10.2022:

Custom validator checking if user is already logged into the application.


<img src="screenshots\validators_2.png" width="600" alt="login validators">

CSS styling.

Application testing revealed that user is not able to send messages using "ENTER" key.
(Functionality to "ENTER" key in the chat has been added)

2.11.2022:

CSS styling on login side

For testing purposes, there are 3 users predefined ( admin : password, user1 : password1, user2: password2).
All registered users can log correctly.
Login validators work correctly.

Testing revealed live message functionality failures. Messages weren't updated in real time on the client side
(Functionality fixed: bug in updating script)

12.11.2022

User passwords has been encrypted by wergzeug.security.generate_password_hash() and password validation has been updated to use check_password_hash()

<img src="screenshots\database_1.png" width="600" alt="login validators">


Planned functionalities:

In nearest future :

	Private messages.
	Styling of login site
	Ability to create custom chat rooms
  
 
