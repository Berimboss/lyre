## Lyre

Lyre is a simple application for sharing music. It has an overly
minimal UI and fits into one little python file.

Some configuration is required for Lyre to run.

## Running Locally

You can run Lyre easily with Vagrant, so go [install](http://downloads.vagrantup.com) that now.

Vagrant also requires [Virtualbox](https://www.virtualbox.org/wiki/Downloads).

Once Vagrant is installed, clone the repo and boot the VM.

    $ git clone https://github.com/pearkes/lyre.git
    ...
    $ vagrant up
    ...

You'll need to create an `.env` file in the root of your project.

Inside of it, you should have something like this:

    BUCKET_URL=s3://ag32g23g2:vabnebiesesbs@s3.amazonaws.com/bucket-4j842n82o4iv2
    CACHE_TYPE=simple
    DATABASE_URL=sqlite:////tmp/test.db
    PRETTY_SERVER_NAME=33.33.33.16
    SERVER_NAME=33.33.33.16
    UPLOAD_FOLDER=files/

Now you can ssh into the VM (if it's done provisiong from the `vagrant up`.

    vagrant ssh
    ...
    cd site/

You're now in a shared file system with your host computer. You can run
lyre locally now!

    make setup
    ...

Now visit http://33.33.33.16:5000 and you should see the homepage.

To see all of the commands you can run, checkout the Makefile in the
root of the project.

## Deploying to Heroku

Music sharing is only fun if you can do it with your friends.

Grab the [Heroku Toolbelt](https://toolbelt.heroku.com/) and install it
on your computer. You may have to go sign up for a Heroku account and run:

    $ heroku login
    ...

Now you can create an app! Replace `lyre-2` to whatever you'd like the name
of your application to be on the web.

    $ heroku create lyre-2

Cool. Now you can add the necessary addons:

    $ heroku addons:add heroku-postgresql:dev
    ...
    $ heroku addons:add newrelic:standard
    ...
    $ heroku addons:add bucket:test

Then we need to configure Heroku much like we did our local environemnt.

Heroku makes this easy.

*Be sure to change the values to whatever yours are.*

    $ heroku config:add CACHE_TYPE=simple PRETTY_SERVER_NAME=lyre-2.herokuapp.com SERVER_NAME=lyre-2.herokuapp.com UPLOAD_FOLDER=files/
    ...

One last trick as we have to make sure the application knows where the database
you added earlier is.

    $ heroku config
    === lyre Config Vars
    ...
    HEROKU_POSTGRESQL_COLOR_URL:         postgres://jgeiajg8eahgea:-fawfagaga-2tasPsDDfTzT@ec2-23-23-25-187.compute-1.amazonaws.com/resource45912
    ...

You'll need to copy the database url (i.e `postgres://...`) and make another
configuration variable called `DATABASE_URL`.

    $ heroku config:add DATABASE_URL=postgres://jgeiajg8eahgea:-fawfagaga-2tasPsDDfTzT@ec2-23-23-25-187.compute-1.amazonaws.com/resource45912
    ...

Now all you need to do is push.

    $ git push heroku master
    ...

You should be able to visit the website and upload songs!

    $ heroku open
    ...
