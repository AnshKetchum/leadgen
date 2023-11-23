from typing import List
from .BaseAdapter import BaseAdapter, PartialJob
from leadgen.tools.linkedin.jobs import get_linkedin_jobs, save_job_data
import pandas as pd

class MockAdapter(BaseAdapter):
    TEMP_JOBS_FILE = 'jobs.csv'

    def __init__(self, api_key = "adfjksdlfkjasdflkj") -> None:
        self.api_key = api_key
        
        #Any other API / auth related work can be done here.


    def prepopulate(self, topics):
        #Done for testing purposes.
        data = get_linkedin_jobs(topics)
        save_job_data(data)
        print('CSV populated!')

    def retrieve_jobs(self, topics, k = 1) -> List[PartialJob]:


        df = pd.read_csv(self.TEMP_JOBS_FILE)

        company = df['company'][:k]
        jobReq  = df['description'][:k]

        jobs = []
        for c, j in zip(company, jobReq):
           jobs.append({
                "company" : c,
                "jobReq" : j,
                "metadata" : {
                    "url" : "https://example.com",
                    "src" : "MockAdapter"
                }
           }) 

        return jobs
    
    def apply_to_application(self, uuid, answers, resume_fp, content_letter_fp) -> bool:
        print('Sucessfully applied to MockAdapter.com!!')
        print(resume_fp, content_letter_fp)

        import json
        with open('answers.json','w') as f:
            json.dump(answers, f)
        
        return True

    def get_complete_application(self, partial_job):
        return {
            "questions" : [
                {"type" : "select", "question" : "How much coding experience in Python do you have?" , "options" : {"A" : "5+ years", "B" : "4+ years"}},
                {"type" : "longform", "question" : "Why do you want to join flockfysh?" },
            ]
        }
    
    def poll_application_status(self, partial_job) -> str:
        return "pending"