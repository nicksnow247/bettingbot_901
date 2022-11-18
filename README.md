# autobets
Django/Nuxt reference application


Getting started
---------------

This setup requires Docker.
In the make file there's a list of commands for docker.
```

make start

make make_migrations
make migrate
make create_superuser

make log_all

```

Once everything is up and running open http://localhost:8000 in your browser for backend.
admin panel is on this link http://localhost:8000/admin/login/?next=/admin/

Once everything is up and running open http://localhost:3000 in your browser for frontend.


polling tasks which are used to poll matchbook.com betting exchange api use django and django celerybeat.
The crontasks are in settings.py

FYI make sure you have migrated and set up django container so the tasks work.
If you stop and start the celery containers you will have to delete the celerybeat pid file each time in order to restart.

there's three django apps for betting apis.

apimb = matchbook api.
This is what the current project frontend is using.


I need the frontend to use these api's aswell.
apibf = betfair api  Build api using betfairlightweight api wrapper on github
api sm = smarkets api No api wrapper made for smarkets. Need to buid from scratch.


All betting api credentials are listed in the env file for using these apis.
At the moment the betfair api credentials are not added to this env file. I will add them in the coming days

apibf hasn't been implemented neither has apism



The jobs I need done on this project are as follows.
Finish 1 small feature for apimb - matchbook api
1)
   At the moment I cannot select multiple sporting events to poll pricing for the trading logic to work.
   It only works with a paticular sport eg. tennis.

   I would like to load any betting market from the treeview. for Example basketball. Tennis and football into the configuration page. Then the polling task will dyamically poll the pricing of the selected markets.
   The reason for this is to cut down the api call size and only poll the betting events of interested loaded in the table instead of polling a sport.

2) I need the exact same logic done that's set up for matchbook api done on betfair api and smarkets api.
   In terms of web interface it would probably be best to have a treeview link for each api.
   e.g /matchbook/treeview /betfair/treeview /smarkets/treeview/
       /matchbook/config   /betfair/config  /smarkets/config
       
   Also fix bug refreshing the configuration page.    

3) create a dashboard that shows the profit and loss of each api in graph form and the ability to select time ranges and download to csv. 

4) small web page with current orders of each api

5) Make this project easy to deploy to aws under a purchased domain I have. I have an ec2 instance and bought a url. I would like to have it hosted on this url
   refuse-to-lose.com













