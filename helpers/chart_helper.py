from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets

class ChartHelper:
    def __init__(self, tab_widget, tab_index):
        self.figure = Figure(figsize=(6, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        
        stat_tab = tab_widget.widget(tab_index)
        layout = stat_tab.layout()
        if not layout:
            layout = QtWidgets.QVBoxLayout(stat_tab)
            
        layout.addWidget(self.canvas)
        
        self.current_theme = 'dark'
        self.current_salary_data = None
        
        self._draw_empty_state()

    def set_theme(self, theme_name):
        self.current_theme = theme_name.lower()
        if self.current_salary_data is not None:
            self.draw_salary_chart(self.current_salary_data)
        else:
            self._draw_empty_state()

    def get_colors(self):
        if self.current_theme == 'light':
            return {
                'bg': '#ffffff',
                'text': '#1a202c',
                'sub_text': '#718096',
                'bar': '#4299e1',
                'bar_edge': '#2b6cb0',
                'value': '#2f855a'
            }
        else:
            return {
                'bg': '#202124',
                'text': 'white',
                'sub_text': 'gray',
                'bar': '#63b3ed',
                'bar_edge': '#2b6cb0',
                'value': '#68d391'
            }

    def _draw_empty_state(self):
        self.current_salary_data = None
        colors = self.get_colors()
        
        self.figure.clear()
        self.figure.patch.set_facecolor(colors['bg'])
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(colors['bg'])
        ax.axis('off')
        ax.text(0.5, 0.5, 'Search for jobs\nto see salary statistics', 
                color=colors['sub_text'], fontsize=14, ha='center', va='center')
        self.canvas.draw()

    def draw_salary_chart(self, salary_data):
        self.current_salary_data = salary_data
        colors = self.get_colors()
        
        self.figure.clear()
        self.figure.patch.set_facecolor(colors['bg'])
        
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(colors['bg'])
        
        if not salary_data:
            ax.axis('off')
            ax.text(0.5, 0.5, 'No salary data available\nfor the found jobs 😔', 
                    color=colors['sub_text'], fontsize=14, ha='center', va='center')
            self.canvas.draw()
            return
            
        labels = list(salary_data.keys())
        values = list(salary_data.values())
        
        bars = ax.barh(labels, values, color=colors['bar'], edgecolor=colors['bar_edge'], height=0.6)
        
        ax.set_xlabel('Maximum Salary', color=colors['sub_text'])
        ax.set_title('TOP jobs by salary', color=colors['text'], pad=20, fontsize=14)
        
        ax.tick_params(colors=colors['text'])
        ax.spines['bottom'].set_color(colors['sub_text'])
        ax.spines['left'].set_color(colors['sub_text'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width + (max(values)*0.02), bar.get_y() + bar.get_height()/2, 
                    f'{int(width)}', 
                    va='center', ha='left', color=colors['value'], fontweight='bold', fontsize=10)
        
        ax.invert_yaxis()
        self.figure.tight_layout()
        self.canvas.draw()