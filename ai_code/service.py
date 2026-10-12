
from langchain_community.document_loaders import PyPDFLoader

from prompts import resume_prompt
from schema import ResumeAnalysis
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI

load_dotenv()

llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0,
)

def analyze_resume(
    resume_path: str,
    job_description: str,
) -> ResumeAnalysis:

    # 1. Load the uploaded PDF
    loader = PyPDFLoader(resume_path)
    documents = loader.load()

    # 2. Extract complete resume text
    resume_text = "\n".join(
        doc.page_content for doc in documents
    ).strip()

    if not resume_text:
        raise ValueError("No readable text found in the resume PDF.")

    # 3. Use structured output with your Pydantic model
    structured_llm = llm.with_structured_output(ResumeAnalysis)

    # 4. Create the chain
    chain = resume_prompt | structured_llm

    # 5. Invoke the chain
    result = chain.invoke({
        "resume_text": resume_text,
        "job_description": job_description,
    })

    print(result)

    # 6. Return the Pydantic object
    return result
