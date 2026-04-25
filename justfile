setup:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	. .venv/bin/activate && streamlit run app.py

freeze:
	. .venv/bin/activate && pip freeze > requirements.lock.txt

clean:
	rm -rf .venv __pycache__ agents/__pycache__ tools/__pycache__