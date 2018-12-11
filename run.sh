source ../venv/bin/activate && pip install -r requorements.txt &&(uwsgi -s 127.0.0.1:8008 -w ssweb &)
