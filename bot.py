from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings

from policy import RestaurantPolicy
from rasa_core import utils
from rasa_core.actions import Action
from rasa_core.actions.forms import EntityFormField, FormAction

from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.events import SlotSet
from rasa_core.featurizers import (
    MaxHistoryTrackerFeaturizer,
    BinarySingleStateFeaturizer)
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.policies.augmented_memoization import AugmentedMemoizationPolicy
from rasa_core.policies.fallback import FallbackPolicy

from pymongo import MongoClient

logger = logging.getLogger(__name__)

client = MongoClient()

db = client.Restaurantdb
r_collection = db.restaurant

class RestaurantAPI(object):
    def search(self, c_slot, l_slot, p_slot):

        print(c_slot)
        print(l_slot)
        print(p_slot)

        if (c_slot is not None) & (p_slot is not None) & (l_slot is not None):
            res = r_collection.find_one({"cuisine" : c_slot, "city" : l_slot, "price" : p_slot })
            if res is None:             
                res = r_collection.find_one({"cuisine" : c_slot, "city" : l_slot})
                if res is None:
                    res = r_collection.find_one({"city" : l_slot})
        elif (c_slot is not None) & (l_slot is not None):
            res = r_collection.find_one({"cuisine" : c_slot, "city" : l_slot })
        elif (c_slot is not None) & (p_slot is not None):
            res = r_collection.find_one({"cuisine" : c_slot, "price" : p_slot })
        elif (p_slot is not None) & (l_slot is not None):
            res = r_collection.find_one({"city" : l_slot, "price" : p_slot })
        else: 
            print("uno a caso")
            res = r_collection.find_one()

        if res is None:
            res = r_collection.find_one()

        return res['name']+' in '+res['city']+' offering '+res['cuisine']+' cuisine'


class ActionSearchRestaurants(FormAction):
    def name(self):
        return 'action_search_restaurants'

    @staticmethod   
    def required_fields():
        return [
            EntityFormField("cuisine", "cuisine"),
            EntityFormField("location", "location"),
            EntityFormField("price", "price")
        ]

    def submit(self, dispatcher, tracker, domain):
        dispatcher.utter_message("looking for restaurants")
        restaurant_api = RestaurantAPI()
        restaurants = restaurant_api.search(
            tracker.get_slot("cuisine"),
            tracker.get_slot("location"),
            tracker.get_slot("price")
        )

        print(restaurants)

        return [SlotSet("matches", restaurants)]
  

class ActionSuggest(Action):
    def name(self):
        return 'action_suggest'

    def run(self, dispatcher, tracker, domain):
        if tracker.get_slot("matches") is None:
            dispatcher.utter_message("I couldn't fine anything :(")
        else:
            dispatcher.utter_message("here's what I found:")
            dispatcher.utter_message(tracker.get_slot("matches"))
            dispatcher.utter_message("is it ok for you? "
                                     "hint: I'm not going to "
                                     "find anything else :)")
        return []


def train_dialogue(domain_file="restaurant_domain.yml",
                   model_path="models/dialogue",
                   training_data_file="data/babi_stories.md"):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=3),
                            RestaurantPolicy()])

    training_data = agent.load_data(training_data_file)
    agent.train(
            training_data,
            epochs=400,
            batch_size=200,
            validation_split=0.2
    )

    agent.persist(model_path)
    return agent


def train_nlu():
    from rasa_nlu.training_data import load_data
    from rasa_nlu import config
    from rasa_nlu.model import Trainer

    training_data = load_data('data/franken_data.json')
    trainer = Trainer(config.load("nlu_model_config.yml"))
    trainer.train(training_data)
    model_directory = trainer.persist('models/nlu/',
                                      fixed_model_name="current")

    return model_directory


def run(serve_forever=True):
    interpreter = RasaNLUInterpreter("models/nlu/default/current")
    agent = Agent.load("models/dialogue", interpreter=interpreter)

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
    return agent


if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")

    parser = argparse.ArgumentParser(
            description='starts the bot')

    parser.add_argument(
            'task',
            choices=["train-nlu", "train-dialogue", "run"],
            help="what the bot should do - e.g. run or train?")
    task = parser.parse_args().task

    # decide what to do based on first parameter of the script
    if task == "train-nlu":
        train_nlu()
    elif task == "train-dialogue":
        train_dialogue()
    elif task == "run":
        run()
