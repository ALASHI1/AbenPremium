# Aben Premium
## About the project
This is a django application that provides a premimun content to user when the user signs up , this is done with the Stripe api.
The application also has the following features:
- User can sign up for 7 days
- User can cancel the subscription
- User can see the subscription status
- User can see the current plan

## How to run the project
Download the zip file or clone the repo to a folder any where on your system then install a virtual enviroment on your terminal if you dont have one already with

```
python3 -m pip install --user virtualenv
```

Then proceed to create a virtual environment and activate it with 

```
for mac 
    python3 -m venv env('env' can be anyname)
    source env/bin/activate

for windows
    py -m venv env('env' can be anyname)
    .\env\Scripts\activate
```
To confirm if the above process has been completed you should see the 'env' like this '(env)' on your terminal/cmd

please note that you have to have python installed on your global computer to proceed 


Clone the project into your computer using

```
git clone https://github.com/ALASHI1/AbenPremium.git
```


after the above processes have been completed you wil then cd into your project(Aben_membership) with the command

```
cd challenge2/Aben_membership
```

Then proceed to install the requirements necessary for the project
using the command 

```
pip install -r requirements.txt
```

## postgres
Ensure you have postgres installed and running on you system then <br>
Create a database called ```abenbackend``` <br>
Create a user called ```abenbackenduser``` with a password of ```Aben12345``` <br>
Grant all Privileges on database ```abenbackend``` to ```abenbackenduser```

If further help is required the documentation can be found <a href='https://www.postgresql.org/docs/14/index.html'/> here </a>

After successful postgres configuration run :
```
python manage.py migrate
python manage.py runserver
```
PROCEED TO
```
http://127.0.0.1:8000/
```
to see the project running, sign up, use the test card details
```
4242 4242 4242 4242 4242
future date
123
any postal code
```
to complete the signup,
Confirm your account through the email then
login and navigate the site