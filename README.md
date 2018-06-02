# NLU2

To run this bot you need to have Rasa NLU 0.12.3 and Rasa Core 0.9.3. Moreover, the database is managed by the MongoDB DBMS. So, before starting the bot, you need to install Rasa NLU, Rasa Core and MongoDB. 

First, the database has to be created: this can be done by 

The next step is populating the database. This can be done by running create_populate.sh bash script:
 BOH


mongoimport -d Restaurantdb -c restaurant --type csv --file /home/martina/Desktop/NLU/db.csv --headerline

Then, these are the steps necessary to train and run the bot:
- python bot.py train-nlu
- python bot.py train-dialogue
- python bot.py run