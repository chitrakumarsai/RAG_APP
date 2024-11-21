import os
from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from dotenv import load_dotenv
load_dotenv()

# API key for OpenAI (DO NOT hardcode in production)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Global variables
index = None
lock = Lock()


def initialize_index():
    """
    Initializes the index using documents in the './documents' folder.
    """
    global index
    with lock:
        if os.path.exists('./data'):
            documents = SimpleDirectoryReader('./data').load_data()
            index = VectorStoreIndex.from_documents(documents)
        else:
            print("No documents found to initialize the index.")


def query_index(query_text):
    """
    Queries the index with the given text.
    :param query_text: Query string
    :return: Query response as a string
    """
    global index
    with lock:
        query_engine = index.as_query_engine()
        return str(query_engine.query(query_text))


def insert_into_index(filepath, doc_id=None):
    """
    Inserts a document into the index.
    :param filepath: Path to the document file
    :param doc_id: Optional document ID
    """
    global index
    from llama_index.core import SimpleDirectoryReader

    document = SimpleDirectoryReader(input_files=[filepath]).load_data()[0]
    if doc_id:
        document.doc_id = doc_id

    with lock:
        index.insert(document)
        # Persist changes to disk
        index.storage_context.persist()


if __name__ == "__main__":
    # Initialize the index
    print("Initializing index...")
    initialize_index()

    # Set up the BaseManager
    print("Starting index server...")
    manager = BaseManager(("127.0.0.1", 5602), b"password")
    manager.register("query_index", query_index)
    manager.register("insert_into_index", insert_into_index)
    server = manager.get_server()
    server.serve_forever()
