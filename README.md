# Python-Selenium

## About Python-Selenium

Python-Selenium is a simplified framework from [Selenium for Python](https://selenium-python.readthedocs.io/installation.html)

## Browsers support
Browser  | Support
-------- | -------------
Chrome   | Yes
Firefox  | Yes
Safari   | No
Edge     | No

## Libraries with Python-Selenium:
In addition to Selenium, this framework works with other tools such as:
- [MySQL Connector: Connections Only With This Database](https://pypi.org/project/mysql-connector-python/)
- *[SQLAlchemy: ORM](https://www.sqlalchemy.org/)
- [Pandas: Manipule Excel](https://pandas.pydata.org/)
- [Openpyxl: Pandas motor](https://openpyxl.readthedocs.io/en/stable/)
- [PyAutoIt: Popups](https://github.com/jacexh/pyautoit)
- [Xlwings: Call Python from Excel and vice versa](https://docs.xlwings.org/en/latest/)
- [Dateutil: Simplified Dates](https://dateutil.readthedocs.io/en/stable/)

_* For use this library, you need to install the connector as PyMySQL_

## Execute the process
1. Add an folder that you require for work with this library.
2. Create an file with name _main.py_
3. Add the next code in the folder:
    `def execute_from_command_line(action:str):`
    `pass`
4. Execute the code with the next command in console:
    Markup: `python manage.py –project {project/subproject}`

_* For best suggestions, check the folder name 'project'._

## Commands that can you execute
- '--project {project/subproject}': Name of folder or subfolder
- '--type {action}': Any action that you require

## Documentation
Theren't documentation available, but work is currently being done to make it available.
In a future this page will be updated with the link to the docs. 

## Changes with V1.2
- In this version, --project command changed to --run-project or -rp
- Add --make-model and --make-project (or -mk) added.
- Add multidatabase to models (specified with __bind_key__ in model)

## License
The Python-Selenium framework is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).