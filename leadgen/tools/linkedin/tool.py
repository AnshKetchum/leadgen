from .jobs import get_linkedin_jobs, save_job_data
from langchain.tools import Tool, BaseTool
from pydantic import BaseModel, Field 
from typing import Union, Tuple, Dict
from typing import Optional, Type

from langchain.agents.agent_toolkits.conversational_retrieval.tool import create_retriever_tool
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings

class ObtainLinkedInData(BaseModel):
    keywords: str = Field()

class ObtainLinkedInDataTool(BaseTool):
    name = "obtain_linkedin_data"

    description = """Use this tool BEFORE any data analysis on job postings companies have made, and the requirements they are looking for within a job. Without running this tool first, you won't
    Example input: data analyst

    This would get you job postings from companies looking for data analysts. You can ALSO use this tool in sucession if you want data on multiple topics. For example, you might realize that
    after getting data on data analytics, some machine learning jobs might also be relevant. Then re-run this tool, and it'll add machine learning jobs as well
    """

    args_schema: Type[BaseModel] = ObtainLinkedInData 


    def _run(
        self, keywords: str,run_manager = None
    ) -> str:
        """Use the tool."""

        #data = get_linkedin_jobs(keywords, "US", 1)
        #save_job_data(data)

        return f'Sucessfully obtained LinkedIn company postings data on {keywords}! Now, use one of the other tools available to interact with the data'

    async def _arun(
        self, keywords: str,run_manager = None
    ) -> str:
        """Use the tool asynchronously."""

        #data = get_linkedin_jobs(keywords, "US", 1)
        #save_job_data(data)

        return f'Sucessfully obtained LinkedIn company postings data on {keywords}! Now, use one of the other tools available to interact with the data'

def create_qa_retriever_tool(llm, fp = "jobs.csv"):
    """
    Creates a retriever tool to perform Q & A over the job postings data
    """ 
    NAME = "job_retrieval_search"
    DESCRIPTION = "Ask about any jobs in the current jobs database."

    loader = CSVLoader(file_path=fp)
    documents = loader.load()

    print('Documents loaded. Ready for QA.')
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    retriever_tool = create_retriever_tool(vectorstore.as_retriever(), NAME, DESCRIPTION)
    return retriever_tool

