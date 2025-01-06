import asyncio
import streamlit as st
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.app import main

if __name__ == "__main__":
    st.set_page_config(
        page_title="Health & Environment Monitor",
        page_icon="🏥",
        layout="wide"
    )
    asyncio.run(main()) 