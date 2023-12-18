from setuptools import setup, find_packages

setup(
    name="indexing_pipeline",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "openai",
        "pinecone-client",
        "psycopg2",
        "python-dotenv",
    ],
)
