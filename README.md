1. Follow url below to set up django environment:
	https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment  
   including: 
	- Installing Python 3 and pip3(command for ubuntu 16.04 :**sudo apt-get install python3-pip**;different OSs differ)
	- set up the virtual environment(different OSs differ;see link for details)
	- installing Django(command: **pip3 install django**)

2. Download github repo from:
	https://github.com/kent426/json-django.git 

3. Serve the website:
   - cd into the directory contains manage.py
   - run command in terminal: **python3 manage.py runserver**

	(may need to run :python3 manage.py migrate
	to remove warnings in the terminal)

4. Open the site on browser: http://127.0.0.1:8000/


----------file location-------------
threat file location:
	**json-django/threatapp/static/filesRecords/threat.txt**, where json-django is the project root directory. 
	File name has to be **threat.txt**.

------------------------------------
5. run tests:
under directory contains manage.py, run command: **python3 manage.py test**

		
