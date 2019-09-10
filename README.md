## Tool , Technologies and Version
Python 3.6.8<br />
Django 1.11<br />
psycopg2-binary==2.8.3<br />
djangorestframework==3.9.4<br />
djangorestframework-jwt==1.11.0<br />



## Installation

Inside your root directory create VIRTUAL ENVIRONMENT :

virtualenv env --python=python3 (If your Current version of Python is Python2)

virtual env (If your Current default version of Python is Python3)


After creating Virtual Environment you need to Activate that environment so that all the installed package will only available for this Specific Project not for the rest if any.

source env/bin/activate

After activating an environment we need to install all the required packages.

pip install -r requirements.txt

## Requirements.txt (Required Packages)
certifi==2019.6.16 <br />
cloudinary==1.15.0 <br />
Django==1.11 <br />
django-cors-headers==3.0.2 <br />
django-material==1.1.1 <br />
django-richtextfield==1.2.2 <br />
djangorestframework==3.9.4 <br />
djangorestframework-jwt==1.11.0 <br />
mock==3.0.5 <br />
psycopg2-binary==2.8.3 <br />
PyJWT==1.7.1 <br />
pyotp==2.2.7 <br />
pytz==2019.1 <br />
six==1.12.0 <br />
urllib3==1.25.3 <br />




## Usage

To start the Server:

python manage.py runserver