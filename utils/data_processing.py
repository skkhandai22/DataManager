from datetime import datetime
import pandas as pd
class DataProcessing:
    def __init__(self,data):
        self.data = data
    
    def process_data(self):
        current_date = pd.to_datetime(datetime.now())
        self.data['Aging (days)'] = (current_date - self.data['Case Creation Date']).dt.days

        bins = [0, 7, 14, float('inf')]
        labels = ['Less than a Week', 'More than a Week', 'More than 2 Weeks']
        self.data['Aging Range'] = pd.cut(self.data['Aging (days)'], bins=bins, labels=labels, right=False)

        return self.data
