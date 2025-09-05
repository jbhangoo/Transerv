#
# AI training script
# WARNING: This script will train a new model from scratch!!
# Only do this once, and only if you have a lot money to pay for the training, and time to wait for the training to finish.
# Oh, and you need to have a DDL for your database schema
# OUCH!
#
# To run this script in Python:
# >>> import TRAIN_AI
# >>> train_ai()


# The import statement will vary depending on your LLM and vector database. This is an example for OpenAI + ChromaDB
import os
from vanna.openai.openai_chat import OpenAI_Chat
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore

# Set up persistent storage path
chroma_path = os.getenv('CHROMA_PATH')  # This will be your persistent storage directory

# Use Open AI
openai_api_key = os.getenv('OPENAI_API_KEY')

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

def train_vanna(testing=True):
    """
    How to train Vanna AI:
    - Before running the training script, set the OPENAI_API_KEY environment variable. You can do this in the terminal with the following command:
        export OPENAI_API_KEY=your_api_key_here
    - Open a Python command line
    - Import this module by running the following command:
        >>> from vanna_ai.TRAIN_AI import train_vanna
    - Execute this method by running the following command:
        >>> train_vanna(testing=True)
    - When satisfied, set testing=False and run the command again
    :param testing:
    :return:
    """
    vn = MyVanna(config={
        'api_key': openai_api_key,
        'model': 'gpt-4',
        'path': chroma_path  # This enables persistence
    })

    # Get the path to the root of the project
    schema_file = os.getenv('SCHEMA_FILE')
    schema_text = open(schema_file).read()
    if not testing:
        vn.train(ddl=schema_text)
        print("Vanna was configured and training was completed.")
    else:
        print("Vanna is configured to train. Training was not performed in testing mode.")
