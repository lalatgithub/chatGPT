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

Copy and rename `.env_example` to `.env`

Add your openai key from here [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

Run command from terminal

```
export $(cat .env | xargs) && poetry run jupyter notebook --ServerApp.token="" --ServerApp.password="" --notebook-dir ./src
```
