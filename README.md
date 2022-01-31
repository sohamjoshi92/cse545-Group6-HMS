# backend_django
To test the code. Download the whole code and paste it in a new directory. <br />
Open command prompt and locate the directory where the code is present.<br />
Install python (if you don't have in your computer).<br />
Create a virtual environment by typing this command. For windows:  <br />
>          python -m venv .\venv
For linux:
>          python -m venv ./venv
Activate the new virtual environment by typing this command. For windows (if this does not work, remove the .bat)<br />
>           .\venv\Scripts\activate.bat 
For Linux:
>           source ./venv/bin/activate           
Install django by typing this command:<br />
>           pip install Django
or<br />
>           python -m pip install Django
Replace python with python3 in linux or MAC (there might be two python versions running in linux/mac). Shouldn't take too long to install.<br />
In the project directory, to start the server, run<br />
>           python manage.py runserver
A url will be posted in the cmd, like this: "http://127.0.0.1:8000/"<br />
Copy that url and add: "hms_welcome/welcome/" to make it: "http://127.0.0.1:8000/hms_welcome/welcome/".<br />
Paste the above url in the browser and the output should be: "Welcome to the Hospital Management System. Done by Group 6. We are just getting started."<br />
