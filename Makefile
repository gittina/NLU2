help:
	@echo "- train-nlu"
	@echo "--- Train NLU module with Rasa NLU."

	@echo "- train-dialogue"
	@echo "--- Train dialogue model with Rasa core."

	@echo "- evaluate-nlu"
	@echo "--- Evaluate NLU model module"

	@echo "- evaluate-dialogue"
	@echo "--- Evaluate dialogue model"

	@echo "- run"
	@echo "--- Run the bot"
	
create-database:
	python createdb.py

train-nlu:
	python bot.py train-nlu

evaluate-nlu:
	python -m rasa_nlu.evaluate --data data/franken_data.json --config nlu_model_config.yml --mode crossvalidation --verbose

train-dialogue:
	python bot.py train-dialogue

evaluate-dialogue:
	python -m rasa_core.evaluate --stories data/test.md	--core models/dialogue 

run:
	python bot.py run

