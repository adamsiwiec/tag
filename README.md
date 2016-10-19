# Tag

The Social Media of Adjectives. Create and share unique tags (similar to hastags or short phrases) with your friends and start a streak to rack up credits.

**[Currently Live here](https://tagyourit.herokuapp.com)**

[![Build Status](https://travis-ci.org/adamSiwiec/tag.svg?branch=master)](https://travis-ci.org/adamSiwiec/tag)
[![Code Climate](https://codeclimate.com/github/adamSiwiec/tag/badges/gpa.svg)](https://codeclimate.com/github/adamSiwiec/tag)
[![Test Coverage](https://codeclimate.com/github/adamSiwiec/tag/badges/coverage.svg)](https://codeclimate.com/github/adamSiwiec/tag/coverage)



### Getting Started

You will need to install a couple of things locally, plus start up a virtual environment to isolate the program.
First off you will need Python 3.5.X installed locally and will need a copy of pip.
After that run this to install your virtual environment tool:

```
pip install virtualenv
```
Next, download the zip at the top of the page, unzip it and navigate to the folder through the terminal.

```
cd /path/to/me/
```
Start up your virtualenv, using a Python 3 Interpreter:

```
virtualenv -p /path/to/python3 venv
```
Activate:

```
source venv/bin/activate
```
Install dependencies:

```
pip install -r requirements.txt
```
Run the server:

```
python manage.py runserver
```

Now check it out in your browser at [localhost:8000](http://localhost:8000)


## To do
* Create a REST API
* ~~Deploy on Heroku~~
* Add tests
* ~~Form Validation~~
* ~~Convert all Forms to crispy-forms~~
* Rework the UI
* Add the Friends and Tags page
* Use django-imagekit to optimize image quality, size, etc.
* Squash all bugs ( so close but so far )



## Authors

* **[Adam Siwiec](http://adamsiwiec.com)**  - creator - [Github Account](https://github.com/adamsiwiec)

See also the list of [contributors](https://github.com/adamsiwiec/tag/contributors) who participated in this project.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Acknowledgments

* Thanks to ZB, Jerome, and Edgar
* Also thanks to Django
