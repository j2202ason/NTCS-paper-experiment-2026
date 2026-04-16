import os

from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_community.retrievers import BM25Retriever
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class clsRAG:
    def __init__(self):
        self.knowbase = ''
        self.llm = ChatDeepSeek(
            model="deepseek-chat",
            temperature=0,
            max_tokens=4096,
            timeout=120,
            max_retries=1,
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

    def setKnowbase(self, kbparam: str): self.knowbase = kbparam

    def judge_need_rag(self, questions) -> bool:
        system_template = """
        Your task is to judge whether the given question needs to be answered through external knowledge base retrieval (RAG).
        Output only JSON in the following format: {{"need_rag": true/false}}

        Judgment criteria:
        1. RAG required: The question involves technical terms and needs external knowledge to answer.
        2. RAG not required: The question can be answered with subjective suggestions, logical reasoning, or the LLM's own knowledge.
        """
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

        human_template = "Question：{question}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        judge_prompt = ChatPromptTemplate.from_messages([
            system_message_prompt,
            human_message_prompt
        ])
        judge_chain = judge_prompt | self.llm | JsonOutputParser()
        result = judge_chain.invoke({"question": questions})
        return result.get("need_rag", False)

 
    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def getinfo(self, questions):
        loader = Docx2txtLoader(self.knowbase)
        pages = loader.load_and_split()
     
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(pages)
  
        self.retriever = BM25Retriever.from_documents(
            docs,
            k1=1.5,  # BM25 
            b=0.75  # BM25 
            
        )

        template = """
        you are an AI asistant and .
       You are an AI assistant that can comprehend the relevant content from the {context} and answer users' questions. 
       Note: Several examples are provided in the {context}, which you can use to facilitate your learning and understanding. 
       Reply with no answer if you cannot sort out a valid answer; otherwise, provide the answer.      
        context：
        {context}

        question：{question}
        """

        prompt = ChatPromptTemplate.from_template(template)

        self.qa_chain = (
                {
                    "context": self.retriever | self.format_docs,
                    "question": RunnablePassthrough()
                }
                | prompt
                | self.llm
                | StrOutputParser()
        )

        return self.qa_chain.invoke(questions).strip()


class inteface_RAG:
    def __init__(self):
        self.RAG = clsRAG()

    def config(self, _configuration: dict):
        self.RAG.setKnowbase(_configuration.get("KnowBase"))
        self.questions = _configuration.get("Questions")

    def answer(self): return self.RAG.getinfo(self.questions)



