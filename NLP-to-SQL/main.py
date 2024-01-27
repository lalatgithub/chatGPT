import os
import logging

# locals
import utils
from git import Repo
from pathlib import Path
PROJECT_ROOT_DIR = Path(os.path.abspath('')).parent
REPO_PATH = os.path.join(PROJECT_ROOT_DIR, '.git')
repo = Repo(REPO_PATH)
origin = repo.remote(name='origin')
origin.push()

logging.basicConfig(
                    level=logging.INFO, 
                    format='[%(asctime)s] %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S'
                )

log = logging.getLogger(__name__)

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


if __name__ == '__main__':
    log.info(f'Loading sample data...')

    CSV_FILE_PATH = os.path.join(CURRENT_DIR, 'sales.csv')
    SQL_TABLE_NAME = 'sales'
    df = utils.csv_to_dataframe(CSV_FILE_PATH)
    db = utils.get_db_conn()

    log.info(f'Data Format: {df.shape}')

    log.info(f'Migrating DataFrame to SQL table {SQL_TABLE_NAME}')
    utils.migrate_dataframe_to_sql_table(df, SQL_TABLE_NAME, db)

    log.info('Creating table definition for Sales in OpenAI')
    openai_sql_table = utils.create_table_definition(df, SQL_TABLE_NAME)

    log.info('Waiting for user input')
    user_input = utils.prompt_input()

    log.info('Creating OpenAI prompt based on user input')
    prompt = utils.combine_prompts(openai_sql_table, user_input)

    log.info('Sending prompt to OpenAI')
    nlp_to_sql_query = utils.send_prompt_to_openai(prompt)

    response = utils.execute_nlp_query(nlp_to_sql_query, db)

    log.info(f'Response: {response}')




