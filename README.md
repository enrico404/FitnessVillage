# FitnessVillage
Progetto per l'esame di intefacce utente

# Requirements
 - mysql
 - python3
 - django2

# Server installation step
 - open a mysql terminal
 - copy and paste the commands from "dbscript" file
 - open a terminal and launch the following commands:
	- python3 manage.py migrate
	- python3 manage.py createsuperuser 
	
NB: the second command create a new super user for administration purpose

# Run 
 - open a terminal inside the project root directory
 - launch the following command to run the server:
	- python3 manage.py runserver

# client 
 - inside your main browser digit the following url:
	- 127.0.0.1:8000/ 
 
 # testing
 python3 manage.py test app_name
 
 if you have problem on creation the test db you have to run the following commands: 
 - open a mysql terminal:
    - use dbFitnessVillage;
    - grant all on test_dbFitnessVillage.* to 'userFitnessVillage'@'localhost';

 
