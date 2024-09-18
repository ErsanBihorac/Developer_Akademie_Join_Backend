# Join Backend

This is the backend of my content managment system inspired by Kanban named "Join".

## Inhalt
- [quickstart](#quickstart)
- [features](#features)
- [contributor](#contributor)
- [license](#license)

## Quickstart

In this section i will show you step by step how to clone the project, install everything that is required and start the project.

1. Open your terminal
    Windows: Hold the Windows button and R, type "cmd" into the window, and hit enter.
    Mac: Press Command + Space, type "Terminal", and hit enter.
2. Navigate to your desktop
    Windows: Type "cd desktop" into your terminal and hit enter.
    Mac: Type "cd ~/Desktop" into your terminal and hit enter.
3. Clone the Git repository
    Windows: Type "git clone https://github.com/ErsanBihorac/Developer_Akademie_Join_Backend.git" and hit enter.
    Mac: Same as Windows, type "git clone https://github.com/ErsanBihorac/Developer_Akademie_Join_Backend.git" and hit enter.
4. Navigate to the project and create a virtual environment
    Windows: Type "cd Developer_Akademie_Join_Backend" and hit enter. Then, type "python -m venv venv" and hit enter.
    Mac: Type "cd Developer_Akademie_Join_Backend" and hit enter. Then, type "python3 -m venv venv" and hit enter.
5. Activate your virtual environment (venv)
    Windows: Type "venv\Scripts\activate" and hit enter.
    Mac: Type "source venv/bin/activate" and hit enter.
6. Install the requirements.txt (this step might take a while)
    Windows: Type "pip install -r requirements.txt" and hit enter.
    Mac: Type "pip3 install -r requirements.txt" and hit enter.
7. Make migrations
    Windows: Type "python manage.py migrate" and hit enter.
    Mac: Type "python3 manage.py migrate" and hit enter.
8. Create a superuser
    Windows: Type "python manage.py createsuperuser", hit enter, then choose a username, hit enter, choose an email address, hit enter, choose a password, hit enter, and type in the password again and hit enter.
    Mac: Type "python3 manage.py createsuperuser", hit enter, then follow the same steps as for Windows to create the superuser.
9. Start the server and login
    Windows: Type "python manage.py runserver" and hit enter. Then, open your browser and go to http://127.0.0.1:8000/admin and log in with the credentials from the previous step.
    Mac: Type "python3 manage.py runserver" and hit enter. Then, open your browser and go to http://127.0.0.1:8000/admin and log in with the credentials from the previous step.
10. Enjoy!
    Follow the instructions to access the admin panel and start using the project.

## Features

Feature 1: You can register a new user.

Feature 2: You can login with your registered user.

Feature 3: You can add contacts to your account.

Feature 4: You can create tasks and assign them to your contacts.

## Contributor

Ersan Bihorac

GitHub: https://github.com/ErsanBihorac.
LinkedIn: https://www.linkedin.com/in/ersan-bihorac/.

## License

This project is licensed under the MIT License