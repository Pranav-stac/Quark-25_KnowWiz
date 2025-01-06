import plotly.graph_objects as go
import pandas as pd

class NutritionVisualizer:
    @staticmethod
    def create_macros_chart(nutrition_data: dict) -> go.Figure:
        macros = {
            'Protein': nutrition_data['protein'],
            'Carbs': nutrition_data['carbs'],
            'Fat': nutrition_data['fat']
        }
        
        fig = go.Figure(data=[
            go.Pie(
                labels=list(macros.keys()),
                values=list(macros.values()),
                hole=.3
            )
        ])
        
        fig.update_layout(
            title="Macronutrient Distribution",
            height=300
        )
        
        return fig
    
    @staticmethod
    def create_nutrition_table(foods: list) -> pd.DataFrame:
        return pd.DataFrame(foods).round(2) 