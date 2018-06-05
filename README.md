# NLU2

To run this bot you need to have Rasa NLU 0.12.3 and Rasa Core 0.9.3. Moreover, the database is managed by the MongoDB DBMS. So, before starting the bot, you need to install Rasa NLU, Rasa Core and MongoDB. 

- First, the database has to be created and populated by data contained in data/db.csv file. This can be done by running the command:

``` make create-database ```

- Then, these are the steps necessary to train and run the bot:
``` make train-nlu ```
``` make train-dialogue ```
``` make run ```

