# backend_django
To test the code. Download the whole code and paste it in a new directory. <br />
Open command prompt and locate the directory where the code is present.<br />
Install python (if you don't have in your computer).<br />
Create a virtual environment by typing this command:  <br />
          python -m venv .\venv          -- for windows (idk for other OSs, probably replacing the back slash with a forward slash should do it)<br />
Activate the new virtual environment by typing this command:<br />
          .\venv\Scripts\activate.bat        -- for windows (if this does not work, remove the .bat)<br />
          source ./venv/bin/activate            -- for linux<br />
Install django by typing this command:<br />
          pip install Django <br />
          or<br />
          python -m pip install Django          -- Replace python with python3 in linux or MAC (there might be two python versions running in linux/mac.)<br />
          shouldn't take too long to install.<br />
In the project directory, to start the server, run<br />
          python manage.py runserver<br />
          A url will be posted in the cmd, like this: "http://127.0.0.1:8000/"<br />
          Copy that url and add: "hms_welcome/welcome/" to make it: "http://127.0.0.1:8000/hms_welcome/welcome/".<br />
          Paste the above url in the browser and the output should be: "Welcome to the Hospital Management System. Done by Group 6. We are just getting started."<br />
