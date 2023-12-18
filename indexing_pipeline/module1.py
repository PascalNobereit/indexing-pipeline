from dotenv import load_dotenv
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import SQLRecordManager
from langchain.vectorstores import Pinecone
import pinecone


class IndexingPipeline:
    def __init__(self, namespace: str, connector_id: str, db_url: str):
        self.namespace = namespace
        self.connector_id = connector_id
        self.db_url = db_url
        self.pinecone_index = None
        self.vectorstore = None
        self.record_manager = None

    def setup(self):
        load_dotenv()
        pinecone.init()

        self.pinecone_index = pinecone.Index(self.connector_id)
        embeddings = OpenAIEmbeddings()

        self.vectorstore = Pinecone.from_existing_index(
            os.getenv("INDEX_NAME"), embedding=embeddings, namespace=self.namespace
        )

        record_namespace = f"pinecone/{self.connector_id}"
        self.record_manager = SQLRecordManager(record_namespace, db_url=self.db_url)
        self.record_manager.create_schema()

    def run(self, data, source_id_key="source", cleanup="full"):
        from langchain.indexes import index

        return index(
            data,
            self.record_manager,
            self.vectorstore,
            cleanup=cleanup,
            source_id_key=source_id_key,
        )
