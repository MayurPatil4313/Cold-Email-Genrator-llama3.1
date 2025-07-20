import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

_ = load_dotenv()
API_KEY = os.getenv("API_KEY")
SENDER_NAME = os.getenv("SENDER_NAME")
SERVICE_ORG_NAME = os.getenv("SERVICE_ORG_NAME")


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama3-70b-8192", temperature=0, groq_api_key=API_KEY
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the 
        following keys: `role`, `experience`, `skills` and `description`.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):    
        """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parse = JsonOutputParser()
            json_res = json_parse.parse(res.content)
        except OutputParserException:
            raise OutputParserException(
                "Context too big. Unable to parse in =>extract_jobs"
            )

        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links, SENDER_NAME, SERVICE_ORG_NAME):
            
        prompt_email = PromptTemplate.from_template(
            """
                ### JOB DESCRIPTION:
                {job_description}
                
                ### INSTRUCTION:
                You are {SENDER_NAME}, a business development executive at {SERVICE_ORG_NAME}. {SERVICE_ORG_NAME} is an AI & Software Consulting company dedicated to facilitating
                the seamless integration of business processes through automated tools. 
                Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
                process optimization, cost reduction, and heightened overall efficiency. 
                Your job is to write a cold email to the client regarding the job mentioned above describing the capability of {SERVICE_ORG_NAME}
                in fulfilling their needs.
                Also add the most relevant ones from the following links to showcase {SERVICE_ORG_NAME}'s portfolio: {link_list}
                Remember you are Mohan, BDE at {SERVICE_ORG_NAME}. 
                Do not provide a preamble.
                ### EMAIL (NO PREAMBLE):
                
                """
        )
        chain_email = prompt_email | self.llm
        try:
            response = chain_email.invoke(
                {
                    "job_description": str(job),
                    "link_list": links,
                    "SENDER_NAME": SENDER_NAME,
                    "SERVICE_ORG_NAME": SERVICE_ORG_NAME,
                }
            )
        except Exception as e:
            print('resonse not getting in => write_mail')
            print(e)

        return response.content

if __name__ == "__main__":
    print('IN chains.py file')
    print(API_KEY)
    print(SENDER_NAME)
    print(SERVICE_ORG_NAME)
