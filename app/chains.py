import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

_ = load_dotenv()
API_KEY = os.getenv("API_KEY")


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
            res = json_parse.parse(res.content)
        except OutputParserException:
            raise OutputParserException(
                "Context too big. Unable to parse in =>extract_jobs"
            )

        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links, SENDER_NAME, SERVICE_ORG_NAME, email_length):

        prompt_email = PromptTemplate.from_template(
            # """
            #     You are {SENDER_NAME}, a Business Development Executive at {SERVICE_ORG_NAME}, a Software Consulting company dedicated to facilitating the seamless integration of business processes through automated tools.
            #     Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, process optimization, cost reduction, and heightened overall efficiency.
            #     Your task is to compose a professional cold email to a potential client regarding the following job post:
            #     {job_description}
            #     Highlight how {SERVICE_ORG_NAME} can fulfill the client's needs as outlined in the job description.
            #     Include the most relevant portfolio items from the following list to showcase {SERVICE_ORG_NAME}'s capabilities:
            #     {link_list}
            #     Important Instructions:
            #     * You must write the email content only.
            #     * Do not include any preambles, explanations, or introductory text.
            #     * email lenght should by {email_length} not less than that
            #     * Begin the response directly with:
            #         “Dear Hiring Management,”
            # """
            """
            You are an expert cold email writer specializing in professional outreach. Write a compelling cold email to {organization} with the following specifications:

            **Sender Information:**
            - Name: {SENDER_NAME}
            - Target Role/Interest: {job_description}
            - Portfolio Links: {link_list}
            - Desired Email Length: {email_length}

            **Email Requirements:**
            1. **Subject Line:** Create an attention-grabbing subject line that mentions the organization name and hints at value proposition
            2. **Opening:** Start with a personalized connection to {organization} - mention recent news, achievements, or specific aspects that attracted you to them
            3. **Value Proposition:** Clearly articulate what you can offer based on the {job_description} and your background
            4. **Portfolio Integration:** Naturally incorporate the {link_list} by highlighting specific projects or achievements that align with {organization}'s needs
            5. **Call to Action:** End with a clear, low-pressure request for a brief conversation or meeting
            6. **Professional Tone:** Maintain a balance between professional and personable throughout

            **Email Structure:**
            - Subject: [Compelling subject line]
            - Greeting: Professional salutation
            - Opening paragraph: Personal connection to {organization}
            - Body paragraph(s): Value proposition and relevant experience
            - Portfolio mention: Integrate {link_list} contextually
            - Closing paragraph: Clear call to action
            - Sign-off: Professional closing with {SENDER_NAME}

            **Length Guidelines:**
            - Adjust content density and detail level based on {email_length}
            - Short: 100-150 words, focus on key points only
            - Medium: 150-250 words, include more context and details
            - Long: 250-350 words, comprehensive but still concise

            **Additional Instructions:**
            - Research {organization} briefly and include 1-2 specific details about their recent work, values, or industry position
            - Avoid generic templates - make each email feel personally crafted
            - Use active voice and confident language
            - Include social proof or quantifiable achievements when possible
            - Ensure all portfolio links from {link_list} are relevant to the role described in {job_description}
            - Proofread for grammar, spelling, and professional formatting

            """
        )
        chain_email = prompt_email | self.llm
        try:
            response = chain_email.invoke(
                {
                    "job_description": str(job),
                    "link_list": links,
                    "SENDER_NAME": SENDER_NAME,
                    "organization": SERVICE_ORG_NAME,
                    "email_length": email_length,
                }
            )
        except Exception as e:
            print("resonse not getting in => write_mail")
            print(e)

        return response.content


if __name__ == "__main__":
    print("IN chains.py file")
