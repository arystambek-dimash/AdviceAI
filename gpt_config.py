import os
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def get_answer(text: str, lng: str = "eng") -> str:
    template: str = """Answer psychological questions, about the 
    questions asked by the user, if there is another 
    question that does not relate to the psychologist, you must 
    answer "I do not know, I'm sorry".
    
    Question: {text}
    
    Response language: {language}
    Answer: """
    prompt_template = PromptTemplate.from_template(
        template=template
    )
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    prediction = llm.predict(prompt_template.format(language=lng, text=text))
    return prediction
