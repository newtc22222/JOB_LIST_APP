# WEB APP: TO DO LIST
- Python version: [python 3.7.9](https://www.python.org/downloads/release/python-379/)
- Web framework: [Flask](https://flask.palletsprojects.com/en/2.1.x/)
- Database: sqlite
- Tool support sqlite:
  - [DB Browser for SQLite](https://sqlitebrowser.org/)
  - [Sqlite viewer](https://sqliteviewer.app/)
- SQL toolkit: [flask_sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) (ORM - Data Mapper)
- Front-end:
  - [HTML5](https://www.w3schools.com/html/default.asp) + [jinja](https://jinja.palletsprojects.com/en/3.1.x/) (web templates)
  - static: images
  - CSS: [semantis UI 2.4.2](https://semantic-ui.com/)
- IDE: [Visual Studio Code](https://code.visualstudio.com/Download)
- Web deploy: [render](https://render.com/)
<hr>

## Setting for using (Windows)
1. Download and setting Python in your computer
2. Open Command Line (or Terminal) 
3. Download Flask: `py -m pip install flask`
4. Download Flask_SQLAlchemy: `py -m pip install flask_sqlalchemy`
5. In Visual Studio Code, use Terminal: 
    - `set FLASK_APP=app`
    - `run flask`
> <b>(another choice for step 5)</b> you can use the following command instead: `py app.py`

### Create requirements file
`pip freeze > requirements.txt`