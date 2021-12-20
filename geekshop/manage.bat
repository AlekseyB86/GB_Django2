ECHO OFF
CLS
ECHO.
ECHO ...............................................
ECHO PRESS 1, 2 OR 3 or 4 or 5 to select your task.
ECHO ...............................................
ECHO.
ECHO 1 - makemigrations
ECHO 2 - migrate
ECHO 3 - makemessages
ECHO 4 - compilemessages
ECHO 5 - runserver
ECHO.

SET /P M=Type 1, 2, 3, 4, 5 then press ENTER:
IF %M%==1 GOTO MAKEMIGRATIONS
IF %M%==2 GOTO MIGRATE
IF %M%==3 GOTO MAKEMESSAGES
IF %M%==4 GOTO COMPILEMESSAGES
IF %M%==5 GOTO RUNSERVER
GOTO END

:MAKEMIGRATIONS
python manage.py makemigrations
GOTO END

:MIGRATE
python manage.py migrate
GOTO END

:MAKEMESSAGES
django-admin makemessages --locale=ru
GOTO END

:COMPILEMESSAGES
python manage.py compilemessages
GOTO END

:RUNSERVER
python manage.py runserver 0.0.0.0:8000
GOTO END

:END