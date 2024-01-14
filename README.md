#### OpenAI bootcamp

This repo includes some practice examples using openAI [ChatGPT-3, DALL-E], Python, Jupyter Notebook, Poetry etc

The repository includes both Python raw scripts and Jupyter Notebooks to visualize the data in browser.

#### Tech Stack
* Python 3.11
* ChatGPT-3.5
* DALL-E
* SQLAlchemy
* SQLite
* Jupyter

#### Setup and Run project

If you are a poetry guy
```
poetry update
```

OR

If you are a pip/venv guy
```
python -m venv .venv
```

```
source .venv/bin/activate
```

```
pip install -r requirements.txt
```

#### Run

copy and rename `.env_example` to `.env`

Add your openai key into `.env` from here [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

Run command from terminal

If you love terminal and `__name__ == "__main__"`
```
export $(cat .env | xargs) && poetry run python ./NLP-to-SQL/main.py
```

If you love Jupyter Notebook
```
export $(cat .env | xargs) && poetry run jupyter notebook --ServerApp.token="" --ServerApp.password=""
```
