
import os
from dotenv import load_dotenv

load_dotenv()

try:
   import streamlit as st
   GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY",None)
except Exception:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")