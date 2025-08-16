# blog_generator.py
import os
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.schema.output_parser import StrOutputParser

# load env vars
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ Please set GROQ_API_KEY in your .env file")
    st.stop()

# Setup LLM
llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama-3.1-8b-instant", temperature=0.7)

# Prompt template
BASE_SYS = (
    "You are an expert blog writer. "
    "Write well-structured, original, and SEO-friendly blog posts with headings, subheadings, "
    "short paragraphs, and a crisp intro and conclusion."
)

PROMPT = ChatPromptTemplate.from_messages([
    ("system", BASE_SYS),
    ("human", 
        "Write a blog post about: '{topic}'.\n"
        "Tone: {tone}. Target length: ~{target_length} words.\n"
        "Keywords: {keywords}.\n"
        "Use H2/H3 headings, include meta description."
    )
])

parser = StrOutputParser()
chain = PROMPT | llm | parser

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="📝 Blog Generator", page_icon="✍️", layout="centered")

st.title("📝 Blog Generator with LangChain + Groq + LLaMA")
st.write("Enter a topic and get a blog post generated!")

topic = st.text_input("Blog Topic", "How to learn LangChain fast")
tone = st.selectbox("Tone", ["informative", "casual", "professional", "funny"], index=0)
keywords = st.text_input("Keywords (comma separated)", "langchain, groq, llama 3.1")
target_length = st.slider("Target Length (words)", 300, 2000, 800)

if st.button("Generate Blog"):
    with st.spinner("Generating blog post..."):
        result = chain.invoke({
            "topic": topic,
            "tone": tone,
            "target_length": target_length,
            "keywords": keywords
        })
        st.subheader("📄 Generated Blog Post")
        st.write(result)
