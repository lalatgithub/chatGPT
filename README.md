##### Setup env

```
poetry update
```

OR

```
python -m venv .venv
```

```
source .venv/bin/activate
```

```
pip install -r requirements.txt
```

##### Run

copy and rename `.env_example` to `.env`

Add your openai key into `.env` from here [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

Run command from terminal

```
export $(cat .env | xargs) && poetry run jupyter notebook --ServerApp.token="" --ServerApp.password="" --notebook-dir ./src
```
