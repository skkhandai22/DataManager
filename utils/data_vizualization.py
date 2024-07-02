import matplotlib.pyplot as plt
from utils.data_processing import DataProcessing
import pandas as pd

class DataVisuals:
    def __init__(self, data, processed_data):
        self.df = data
        self.processed_df = processed_data
        
    def table_chart(self):
        # Process the data
        processor = DataProcessing(self.df)
        df = processor.process_data()

        # Get the creation start date, end date, and total cases
        creation_start_date = df['Case Creation Date'].min().strftime('%d-%b-%y')
        creation_end_date = df['Case Creation Date'].max().strftime('%d-%b-%y')
        total_cases = len(df)

        # Calculate the count of rows for each service team
        service_team_counts = df['Service Team'].value_counts().reset_index()
        service_team_counts.columns = ['Team', 'Tickets (~)']

        # Calculate the average aging days for each service team
        average_aging = df.groupby('Service Team')['Aging (days)'].mean().reset_index()
        average_aging.columns = ['Team', 'Average Aging']

        average_aging['Average Aging'] = average_aging['Average Aging'].round()

        # Merge the counts and average aging dataframes
        service_team_summary = pd.merge(service_team_counts, average_aging, on='Team')

        # Create table chart
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('tight')
        ax.axis('off')

        # Define colors and styles
        header_color = '#0F6936'
        row_colors = ['#f1f1f2', '#f8f8f9']
        header_fontsize = 12
        cell_fontsize = 10

        # Main information table
        table_data = [
            ["Creation Start Date", creation_start_date],
            ["Creation End Date", creation_end_date],
            ["TOTAL", total_cases]
        ]
        main_table = ax.table(
            cellText=table_data,
            colLabels=["", ""],
            cellLoc='center',
            loc='top',
            bbox=[0, 0.8, 1, 0.2]
        )

        # Apply styles to main table
        main_table.auto_set_font_size(False)
        main_table.set_fontsize(header_fontsize)
        main_table.scale(1.2, 1.2)
        for key, cell in main_table.get_celld().items():
            cell.set_edgecolor('w')
            if key[0] == 0:
                cell.set_facecolor(header_color)
                cell.set_text_props(color='w', weight='bold')
            else:
                cell.set_facecolor(row_colors[key[0] % len(row_colors)])

        # Service team summary table
        team_table = ax.table(
            cellText=service_team_summary.values,
            colLabels=service_team_summary.columns,
            cellLoc='center',
            loc='center',
            bbox=[0, 0, 1, 0.8]
        )

        # Apply styles to service team summary table
        team_table.auto_set_font_size(False)
        team_table.set_fontsize(cell_fontsize)
        team_table.scale(1.2, 1.2)
        for key, cell in team_table.get_celld().items():
            cell.set_edgecolor('w')
            if key[0] == 0:
                cell.set_facecolor(header_color)
                cell.set_text_props(color='w', weight='bold')
            else:
                cell.set_facecolor(row_colors[key[0] % len(row_colors)])

        plt.title("Service Team Tickets Summary", fontsize=16, weight='bold', color=header_color)
        plt.savefig("table_chart.png", bbox_inches='tight', pad_inches=0.1, dpi=300)
        plt.show()
    def pie_chart(self):
        aging_range_counts = self.processed_df['Aging Range'].value_counts().reset_index()
        aging_range_counts.columns = ['Aging Range', 'Count']

        def func(pct, allvals):
            absolute = int(pct / 100. * sum(allvals))
            return "{:.1f}%\n({:d})".format(pct, absolute) if absolute != 0 else ""

        colors = plt.cm.Paired(range(len(aging_range_counts)))
        plt.rcParams.update({'font.size': 12})

        fig, ax = plt.subplots(figsize=(8, 6))  # Adjusted figure size to fit the details box
        wedges, texts, autotexts = ax.pie(
            aging_range_counts['Count'],
            labels=aging_range_counts['Aging Range'],
            autopct=lambda pct: func(pct, aging_range_counts['Count']),
            startangle=90,
            colors=colors,
            textprops=dict(color="w"),
            wedgeprops=dict(edgecolor='w')
        )

        ax.legend(wedges, aging_range_counts['Aging Range'],
                title="Aging Range",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))

        # Increase font size for the percentages and absolute values inside the pie chart
        plt.setp(autotexts, size=10, weight="bold")
        plt.setp(texts, size=12, weight="bold")

        plt.title('Distribution of Cases by Aging Range', fontsize=14, weight='bold')
        ax.axis('equal')

        # Create the details box below the legend
        details_text = "\n".join([f"{ar}: {cnt} ({pct:.1f}%)" for ar, cnt, pct in zip(
            aging_range_counts['Aging Range'], 
            aging_range_counts['Count'], 
            100 * aging_range_counts['Count'] / aging_range_counts['Count'].sum()
        )])
        plt.figtext(0.5, -0.05, details_text, ha="center", fontsize=10, bbox={"facecolor":"white", "alpha":0.5, "pad":5})

        plt.savefig("pie_chart.png", bbox_inches='tight', pad_inches=0.1, dpi=300)

    def process_visuals(self):
        self.table_chart()
        self.pie_chart()
