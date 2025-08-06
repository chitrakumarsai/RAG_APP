
import os
from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

# API key for OpenAI (DO NOT hardcode in production)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") # type: ignore

# Global variables
PERSIST_DIR = "./backend/storage"
index = None
lock = Lock()


def initialize_index():
    """
    Initializes the index using documents in the './data' folder or loads a persisted index.
    """
    global index
    with lock:
        if not os.path.exists(PERSIST_DIR):
            print("Creating a new index...")
            if os.path.exists('./backend/data'):
                documents = SimpleDirectoryReader('./data').load_data()
                index = VectorStoreIndex.from_documents(documents)
                # Persist the index for later use
                index.storage_context.persist(persist_dir=PERSIST_DIR)
            else:
                print("No documents found in './data' to initialize the index.")
        else:
            print("Loading existing index from storage...")
            storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
            index = load_index_from_storage(storage_context=storage_context)


def query_index(query_text):
    """
    Queries the index with the given text.
    :param query_text: Query string
    :return: Query response as a string
    """
    global index
    with lock:
        if index is None:
            print("Index is not initialized. Please initialize it first.")
            return None
        query_engine = index.as_query_engine()
        response = query_engine.query(query_text)
        return str(response)


def insert_into_index(filepath, doc_id=None):
    """
    Inserts a document into the index.
    :param filepath: Path to the document file
    :param doc_id: Optional document ID
    """
    global index
    document = SimpleDirectoryReader(input_files=[filepath]).load_data()[0]
    if doc_id:
        document.doc_id = doc_id # type: ignore

    with lock:
        if index is None:
            print("Index is not initialized. Initializing a new one...")
            documents = [document]
            index = VectorStoreIndex.from_documents(documents)
        else:
            index.insert(document)
        # Persist changes to disk
        index.storage_context.persist()


if __name__ == "__main__":
    # Initialize the index
    print("Initializing index...")
    initialize_index()

    # # Example query
    # example_query = "What is a transformer?"
    # print(f"Querying index: {example_query}")
    # response = query_index(example_query)
    # pprint(response)

    # Set up the BaseManager
    print("Starting index server...")
    manager = BaseManager(("127.0.0.1", 5602), b"password")
    manager.register("query_index", query_index)
    manager.register("insert_into_index", insert_into_index)
    server = manager.get_server()
    server.serve_forever()

