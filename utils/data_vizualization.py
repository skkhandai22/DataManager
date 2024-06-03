import matplotlib.pyplot as plt
import pandas as pd

class DataVisuals:
    def __init__(self, data, processed_data):
        self.df = data
        self.processed_df = processed_data
        
    def table_chart(self):
        creation_start_date = self.df['Case Creation Date'].min().strftime('%d-%b-%y')
        creation_end_date = self.df['Case Creation Date'].max().strftime('%d-%b-%y')
        total_cases = len(self.df)
        service_team_counts = self.df['Service Team'].value_counts().reset_index()
        service_team_counts.columns = ['Team', 'Tickets (~)']

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.axis('tight')
        ax.axis('off')

        header_color = '#40466e'
        row_colors = ['#f1f1f2', '#f8f8f9']
        header_fontsize = 8
        cell_fontsize = 6

        table_data = [
            ["Start Date", creation_start_date],
            ["End Date", creation_end_date],
            ["TOTAL", total_cases]
        ]
        main_table = ax.table(
            cellText=table_data,
            colLabels=["", ""],
            cellLoc='center',
            loc='top',
            bbox=[0, 0.8, 1, 0.2]
        )

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

        team_table = ax.table(
            cellText=service_team_counts.values,
            colLabels=service_team_counts.columns,
            cellLoc='center',
            loc='center',
            bbox=[0, 0, 1, 0.8]
        )

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

        plt.title("Service Team Tickets Summary", fontsize=8, weight='bold', color=header_color)
        plt.savefig("table_chart.png", bbox_inches='tight', pad_inches=0.1, dpi=300)    
    
    def pie_chart(self):
        aging_range_counts = self.processed_df['Aging Range'].value_counts().reset_index()
        aging_range_counts.columns = ['Aging Range', 'Count']

        def func(pct, allvals):
            absolute = int(pct / 100. * sum(allvals))
            return "{:.1f}%\n({:d})".format(pct, absolute)

        colors = plt.cm.Paired(range(len(aging_range_counts)))
        plt.rcParams.update({'font.size': 12})

        fig, ax = plt.subplots(figsize=(6, 6))
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

        plt.setp(autotexts, size=6, weight="bold")
        plt.setp(texts, size=6, weight="bold")

        plt.title('Distribution of Cases by Aging Range', fontsize=8, weight='bold')
        ax.axis('equal')
        plt.savefig("pie_chart.png", bbox_inches='tight', pad_inches=0.1, dpi=300)

    def process_visuals(self):
        self.table_chart()
        self.pie_chart()
