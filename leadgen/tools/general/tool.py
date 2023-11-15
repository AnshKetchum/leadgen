from langchain.agents.agent_toolkits import create_retriever_tool

NAME = "user_documents_retriever"


DESCRIPTION = """
Use this tool to grab any documents the user uploads.
"""

def local_vectorstore_retrieval(store):
    """
        Return a retrieval tool to grab data from documents in a local vectorstore  
    """
    return create_retriever_tool(
        store.as_retriever(),
        NAME,
        DESCRIPTION
    )
