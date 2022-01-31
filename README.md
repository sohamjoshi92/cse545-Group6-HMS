# backend_django
To test the code. Download the whole code and paste it in a new directory.
Open command prompt and locate the directory where the code is present.
Install python (if you don't have in your computer).
Create a virtual environment by typing this command:  
          python -m venv .\venv          -- for windows (idk for other OSs, probably replacing the back slash with a forward slash should do it)
Activate the new virtual environment by typing this command:
          .\venv\Scripts\activate.bat        -- for windows (if this does not work, remove the .bat)
          source ./venv/bin/activate            -- for linux
Install django by typing this command:
          pip install Django 
          or
          python -m pip install Django          -- Replace python with python3 in linux or MAC (there might be two python versions running in linux/mac.)
          shouldn't take too long to install.
In the project directory, to start the server, run
          python manage.py runserver
          A url will be posted in the cmd, like this: "http://127.0.0.1:8000/"
          Copy that url and add: "hms_welcome/welcome/" to make it: "http://127.0.0.1:8000/hms_welcome/welcome/".
          Paste the above url in the browser and the output should be: "Welcome to the Hospital Management System. Done by Group 6. We are just getting started."
