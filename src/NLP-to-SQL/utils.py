import os
import logging
import pandas as pd
from openai import OpenAI
from sqlalchemy import create_engine, text

logging.basicConfig(
                    level=logging.INFO, 
                    format='[%(asctime)s] %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S'
                )

log = logging.getLogger(__name__)

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

openai = OpenAI()


def csv_to_dataframe(file_path):
    df = pd.read_csv(file_path)
    return df

def get_db_conn():
    db = create_engine('sqlite:///:memory:')
    return db


def migrate_dataframe_to_sql_table(df, table_name, db):
    df.to_sql(name=table_name, con=db)


def create_table_definition(df, sql_table_name):
    prompt = """### sqlite SQL table, with it properties:
    #
    #{}({})
    #
    """.format(sql_table_name, ','.join([str(col) for col in df.columns]))

    return prompt


def combine_prompts(openai_sql_table, prompt_query):
    query_string = f"### A query to answer: {prompt_query}\nSELECT"
    return openai_sql_table + query_string


def prompt_input():
    return input("Tell OpenAI what you want to know about the data:\t")


def send_prompt_to_openai(prompt):
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.4,
        stop=["#", ";'"]
    )


    nlp_to_query = f'SELECT {response.choices[0].message.content.strip()}'
    return nlp_to_query


def execute_nlp_query(nlp_to_query, db):
    with db.connect() as conn:
        result = conn.execute(text(nlp_to_query))

    return result.all()
