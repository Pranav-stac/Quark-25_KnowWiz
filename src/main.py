import asyncio
from database.config import engine
from database.models import Base
from ui.app import HealthDashboard
import streamlit as st

# Create database tables
Base.metadata.create_all(bind=engine)

async def main():
    dashboard = HealthDashboard()
    await dashboard.update_data()
    dashboard.render()

if __name__ == "__main__":
    st.set_page_config(page_title="Health Monitor", layout="wide")
    asyncio.run(main()) 