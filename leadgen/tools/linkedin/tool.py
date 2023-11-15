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
    num_jobs: Optional[int] = Field()

class ObtainLinkedInDataTool(BaseTool):
    name = "obtain_linkedin_data"

    description = """Use this tool BEFORE any data analysis on job postings companies have made, and the requirements they are looking for within a job. Without running this tool first, you won't
    Example input: data analyst

    This would get you job postings from companies looking for data analysts. You can ALSO use this tool in sucession if you want data on multiple topics. For example, you might realize that
    after getting data on data analytics, some machine learning jobs might also be relevant. Then re-run this tool, and it'll add machine learning jobs as well

    Additionally, you will have to specify the number of jobs you'll need. If no clear wording is given,
    default to 5.
    """

    args_schema: Type[BaseModel] = ObtainLinkedInData 


    def _run(
        self, keywords: str, num_jobs: int = 5, run_manager = None
    ) -> str:
        """Use the tool."""

        print("Getting", num_jobs, "for", keywords)
        data = get_linkedin_jobs(keywords, "US", 1, num_jobs)
        save_job_data(data)

        return f'Sucessfully obtained LinkedIn company postings data on {keywords}! Now, use one of the other tools available to interact with the data'

    async def _arun(
        self, keywords: str, num_jobs: int = 5, run_manager = None
    ) -> str:
        """Use the tool asynchronously."""

        print("Getting", num_jobs, "for", keywords)
        data = get_linkedin_jobs(keywords, "US", 1, num_jobs)
        save_job_data(data)

        return f'Sucessfully obtained LinkedIn company postings data on {keywords}! Now, use one of the other tools available to interact with the data'

class LinkedInJobRetrievalInput(BaseModel):
    query: str = Field()

class LinkedInJobRetrievalTool(BaseTool):
    name = "job_retrieval_search"

    description = """Ask about any jobs in the current jobs database.
    """

    args_schema: Type[BaseModel] = LinkedInJobRetrievalInput 


    def _run(
        self, query: str, run_manager = None
    ) -> str:
        """Use the tool."""

        loader = CSVLoader(file_path="jobs.csv")
        documents = loader.load()

        print('Documents loaded. Ready for QA.')
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(documents, embeddings)

        return vectorstore.as_retriever().get_relevant_documents(query)

    async def _arun(
        self, query: str, run_manager = None
    ) -> str:
        """Use the tool asynchronously."""

        loader = CSVLoader(file_path="jobs.csv")
        documents = loader.load()

        print('Documents loaded. Ready for QA.')
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(documents, embeddings)

        return vectorstore.as_retriever().get_relevant_documents(query)



