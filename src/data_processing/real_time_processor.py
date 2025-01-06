import asyncio
from typing import Dict, Any
import pandas as pd
from datetime import datetime

class RealTimeProcessor:
    def __init__(self):
        self.data_buffer = []
        self.processing_interval = 300  # 5 minutes
        
    async def start_processing(self):
        """Start continuous data processing"""
        while True:
            try:
                if self.data_buffer:
                    await self.process_batch()
                await asyncio.sleep(self.processing_interval)
            except Exception as e:
                print(f"Processing error: {str(e)}")
    
    async def add_data(self, data: Dict[str, Any]):
        """Add new data to processing queue"""
        data['timestamp'] = datetime.now()
        self.data_buffer.append(data)
    
    async def process_batch(self):
        """Process accumulated data"""
        df = pd.DataFrame(self.data_buffer)
        
        # Basic data cleaning
        df = df.dropna()
        df = df.drop_duplicates()
        
        # Calculate moving averages
        if len(df) > 0:
            df['heart_rate_ma'] = df['heart_rate'].rolling(window=5).mean()
            df['steps_ma'] = df['steps'].rolling(window=5).mean()
            
            # Store processed data
            self.processed_data = df
            self.data_buffer = []  # Clear buffer
            
        return df 