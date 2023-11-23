from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import List

class PartialJobMetadata(BaseModel):
    src: str
    postingUrl: str

class PartialJob(BaseModel):
    jobReq: str = Field()
    company: str = Field()
    metadata: PartialJobMetadata = Field()


class BaseAdapter:
    '''
    Any job platform can implement their API wrapper by 
    subclassing this base Adapter, i.e LinkedinAdapter,
    and implementing the methods as needed.
    '''

    @abstractmethod
    def retrieve_jobs(self, topics) -> List[PartialJob]:
        '''
        This method searches for and retrieves jobs given a topic, i.e "machine learning", or "software engineering"

        Returns a partial job:

        This is what a single "partial" job looks like

        {
            "jobReq": "This is a sample job requirement. Requires: \n5 years of Unix scripting.\n5+ years of Python\n1+ year of C++",
            "company": "flockfysh", 
            "metadata": {
                "src": "LinkedIn",
                "postingUrl": "https://linkedin.com/xyz"
            }
        }
        '''
        pass


    @abstractmethod
    def apply_to_application(self, uuid, answers, resume_fp, content_letter_fp) -> bool:
        '''
        Here is how a sample answer will look
        {
            "answers": [
                {'content' : "I have 5+ years of experience in the industry, and really loved the job description."},
                {'content' : "C"},
            ]
        } 

        This methods submits the data provided to the API, and returns a True/False whether the submission
        was successful.

        Returns: [True/False]
        '''
        pass

    @abstractmethod
    def get_complete_application(partial_job):
        '''
        - A public method that would retrieve a full application given a smaller job.
        
        The basic schema is shown below:
        This is what a single "partial" job looks like

        {
            "jobReq": "This is a sample job requirement. Requires: \n5 years of Unix scripting.\n5+ years of Python\n1+ year of C++",
            "company": "flockfysh", 
            "metadata": {
                "src": "LinkedIn",
                "postingUrl": "https://linkedin.com/xyz"
            }
        }
        
        Returns: List[CompleteJob], where a complete job, for now contains only a single attribute with questions:

        {
            questions: [
                {"type" : "select", "question" : "How much coding experience in Python do you have?" , "options" : {"A" : "5+ years", "B" : "4+ years"}},
                {"type" : "longform", "question" : "Why do you want to join flockfysh?" },
            ]
        }

        '''
        pass

    @abstractmethod
    def poll_application_status(self, partial_job) -> str:
        '''
        This method checks the status of a partial job

        Here's what a single "partial" job looks like

        {
            "jobReq": "This is a sample job requirement. Requires: \n5 years of Unix scripting.\n5+ years of Python\n1+ year of C++",
            "company": "flockfysh", 
            "metadata": {
                "src": "LinkedIn",
                "postingUrl": "https://linkedin.com/xyz"
            }
        }

        Returns a string, with the status description of the job. I.e "pending", "job in review", "email sent"
        '''
        pass
