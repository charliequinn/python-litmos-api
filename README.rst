**********
Litmos API
**********

.. image:: https://readthedocs.org/projects/python-litmos-api/badge/?style=flat
    :target: https://readthedocs.org/projects/python-litmos-api
    :alt: Documentation Status

.. image:: https://travis-ci.org/charliequinn/python-litmos-api.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/charliequinn/python-litmos-api

.. image:: https://coveralls.io/repos/charliequinn/python-litmos-api/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/charliequinn/python-litmos-api

.. image:: https://landscape.io/github/charliequinn/python-litmos-api/master/landscape.svg?style=flat
    :target: https://landscape.io/github/charliequinn/python-litmos-api/master
    :alt: Code Quality Status

.. image:: https://img.shields.io/pypi/v/litmos-api.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/litmos-api

.. image:: https://img.shields.io/pypi/dm/litmos-api.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/litmos-api

.. image:: https://img.shields.io/pypi/wheel/litmos-api.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/litmos-api

.. image:: https://img.shields.io/pypi/pyversions/litmos-api.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/litmos-api

.. image:: https://img.shields.io/pypi/implementation/litmos-api.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/litmos-api


Litmos REST API client for python 3.6 and above

* Free software: BSD license

Installation
------------

::

    pip install litmos-api

Getting started
---------------

.. code-block:: python

    from litmos import Litmos


    API_KEY = 'AXXXXXXXXXX'
    LITMOS_APP_NAME = 'jins.litmos.com'
    LITMOS_SERVER_URL = 'https://api.litmos.com/v1.svc'  # https://support.litmos.com/hc/en-us/articles/227734667-Overview-Developer-API
    litmos = Litmos(API_KEY, LITMOS_APP_NAME, LITMOS_SERVER_URL)


    # --- User ---
    # retrieve users
    all_users = litmos.User.all()

    # retrieve all users (with all information populated - default /users/all API endpoint only returns a subset of user fields)
    # much longer than .all() as individual requests to /find/{user-id} for every user are made
    all_users_with_full_details = litmos.User.all(True)

    #find user by Id
    user = litmos.User.find('rnjx2WaQOa11')

    # search for user by username
    user = litmos.User.search('beelzebub@pieshop.net')

    # update JobTitle & City fields
    user.JobTitle = 'Pie eater'
    user.City = 'Pieland'

    # save user
    user.save()

    # deactivate user
    user.deactivate()

    # create user
    user = litmos.User.create({
            'UserName': 'jobaba72@pieshop.net',
            'FirstName': 'Jo',
            'LastName': 'Baba72',
            'Email': 'jobaba72@pieshop.net'
        })

    # get teams for a user
    user.teams()

    # remove all teams from user
    user.remove_teams()

    # delete user
    # with Id
    litmos.User.delete('YmrD112qlm41')

    # instance delete
    user.destroy()

    # set a user's manager
    user.set_manager('jdhaskdhlsa')

    # or pass in a user object
    manager = litmos.User.find('rnjx2WaQOa11')[0]
    user.set_manager(manager)

    # advanced custom fields
    # https://support.litmos.com/hc/en-us/articles/227735427-User-Custom-Fields
    user.update_advanced_custom_fields(
        [
            {"fieldnamex": "value1"},
            {"fieldnamey": "value2"}
        ]
    )

    # --- Team ---
    # get all teams
    all_teams = litmos.Team.all()

    # find team by Id
    team = litmos.Team.find('rnjx2WaQOa11')

    # get team members
    users = team.users()

    # get team leaders
    leaders = team.leaders()

    # get team admins
    admins = team.admins()

    # create team (at root level)
    team = litmos.Team.create({'Name': 'A-Team','Description': 'I pity the fool!'})

    # add sub-team
    sub_team = litmos.Team()
    sub_team.Name = 'B-Team'
    sub_team.Description = 'Woohoo'

    sub_team_id = team.add_sub_team(sub_team)

    # assign courses to team
    course1 = litmos.Course.find('d2cJSDvIU0c1')
    course2 = litmos.Course.find('d2cJSDvIU0c2')
    team.assign_courses([course1, course2])

    # unassign courses to team
    course1 = litmos.Course.find('d2cJSDvIU0c1')
    course2 = litmos.Course.find('d2cJSDvIU0c2')
    team.unassign_courses([course1, course2])

    # --- Team members ---

    # add users to team
    user1 = litmos.User.find('rnjx2WaQOa11')
    user2 = litmos.User.find('rnjx2WaQOa12')
    team.add_users([user1, user2])

    # remove users from team
    team.remove_user(user2)

    # --- Team leaders ---
    # promote user
    team.promote_team_leader(user1)

    # demote user
    team.demote_team_leader(user1)

    # --- Team admins ---
    # promote user
    team.promote_team_admin(user1)

    # demote user
    team.demote_team_admin(user1)

Documentation
-------------

https://python-litmos-api.readthedocs.io/

Development
-----------

To run the all tests run::

    pip install -r requirements.txt
    cd tests
    nosetests
