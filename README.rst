=== 
Polls
===

Here is a app to conduct web-based polls. For each question, visitors can choose between a fixed number of answers

Detailed documentation is in the "docs" directory.

QUICK START
===

1. Add "Polls" to your INSTALLED_APPS settings like this:
        INSTALLED_APPS = [
                ....
                'polls',
        ]

2. Include the polls URLconf in your project urls.py like this:
        path('polls', include('polls.urls')),

3. Run ''python manage.py migrate'' to create the polls models

4. Start the development sever and visit you local host/admin to create polls ( REQUIRED at Admin site - I've setup almost things for you to able to do it)

5. Type your localhost/polls and check the result. 

