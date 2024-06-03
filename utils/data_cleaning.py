from configuration.config import Assignees

class DataClean:
    def __init__(self, data):
        self.df = data

    def process_clean(self):
        # Remove Prefixes'
        self.df['Service Team'] = self.df['Service Team'].str.replace(r'^[^_]+_', '', regex=True) 
        
        # Remove duplicates based on 'Case for SLA Result'
        self.df.drop_duplicates(subset=['Case for SLA Result'], inplace=True)

        # Filter based on 'Case Assignee'
        self.df = self.df[self.df['Case Assignee'].isin(Assignees.ASSIGNESS)]
        
        # Split 'Case for SLA Result' into 'Case#' and 'Case Subject'
        self.df[['Case#', 'Case Subject']] = self.df['Case for SLA Result'].str.split(': ', expand=True)
        subset_df = self.df[['Case#', 'Case Subject', 'Case Status', 'Service Team', 'Case Assignee', 'Case Creation Date']]
        subset_df.reset_index(drop=True, inplace=True)
        return subset_df

