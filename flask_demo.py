from flask import Flask
from flask import request
import os
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage
)
from dotenv import load_dotenv
load_dotenv()

# NOTE: for local testing only, do NOT deploy with your key hardcoded
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

index = None

def initialize_index():
    global index
    #Check if storage already exists
    PERSIST_DIR = "./storage"
    if not os.path.exists(PERSIST_DIR):
        #load documents and create index
        documents = SimpleDirectoryReader('/Users/chitrakumarsai/Desktop/Personal/LLM documents').load_data()
        index = VectorStoreIndex.from_documents(documents=documents)
        #store it for later
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        #load existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context=storage_context)

app = Flask(__name__)

@app.route("/query", methods=["GET"])
def query_index():
    global index
    query_text = request.args.get("text", None)
    if query_text is None:
        return (
            "No text found, please include a ?text=blah parameter in the URL",
            400,
        )
    query_engine = index.as_query_engine()
    response = query_engine.query(query_text)
    return str(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5601)