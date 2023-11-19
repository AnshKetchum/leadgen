from langchain.agents.tools import Tool

from langchain.tools import Tool, BaseTool
from pydantic import BaseModel, Field 
from typing import Union, Tuple, Dict
from typing import Optional, Type
import os 
from fpdf import FPDF


NAME = "create_pdf_from_content"
DESCRIPTION = """
    Tool to create a pdf 

    Parameters:
        content: content of the pdf
        pdf_file_path (str): The path to the pdf file to be created, with the base
        directory assumed to be data. So, if you specify pdf_file_path to be out.pdf, it'll be
        saved at data/out.pdf. So, DON'T SPECIFY data/ as part of the filepath. Just the filename, eg.
        user1.pdf.
"""

class PDFFromContentInput(BaseModel):
    content: str = Field()
    pdf_file_path: str = Field()

class PDFFromContentTool(BaseTool):
    name = NAME
    description = DESCRIPTION

    args_schema: Type[BaseModel] = PDFFromContentInput


    def _run(
        self, content: str, pdf_file_path: str, run_manager = None
    ) -> str:
        """Use the tool."""

        pdf = FPDF()

        pdf.add_page()
        pdf.set_font("Arial", size=15)

        pdf.cell(200, 10, txt=content, ln = 1, align='C')

        pdf.output(os.path.join('data', pdf_file_path))

        return f'Sucessfully wrote the markdown data to pdf data/{pdf_file_path}!'  

    async def _arun(
        self, content: str, pdf_file_path: str, run_manager = None
    ) -> str:
        """Use the tool asynchronously."""

        pdf = FPDF()

        pdf.add_page()
        pdf.set_font("Arial", size=15)

        pdf.cell(200, 10, txt=content, ln = 1, align='C')

        pdf.output(os.path.join('data', pdf_file_path))

        return f'Sucessfully wrote the markdown data to pdf data/{pdf_file_path}!'  