from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets

class ChartHelper:
    def __init__(self, tab_widget, tab_index):
        self.figure = Figure(figsize=(6, 6), dpi=100)
        self.figure.patch.set_facecolor('#202124')
        self.canvas = FigureCanvas(self.figure)
        
        stat_tab = tab_widget.widget(tab_index)
        layout = stat_tab.layout()
        if not layout:
            layout = QtWidgets.QVBoxLayout(stat_tab)
            
        layout.addWidget(self.canvas)
        
        self._draw_empty_state()

    def _draw_empty_state(self):
        self.figure.clear()
        self.figure.patch.set_facecolor('#202124')
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#202124')
        ax.axis('off')
        ax.text(0.5, 0.5, 'Search for jobs\nto see salary statistics', 
                color='gray', fontsize=14, ha='center', va='center')
        self.canvas.draw()

    def draw_salary_chart(self, salary_data):
        self.figure.clear()
        self.figure.patch.set_facecolor('#202124')
        
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#202124')
        
        if not salary_data:
            ax.axis('off')
            ax.text(0.5, 0.5, 'No salary data available\nfor the found jobs 😔', 
                    color='gray', fontsize=14, ha='center', va='center')
            self.canvas.draw()
            return
            
        labels = list(salary_data.keys())
        values = list(salary_data.values())
        
        bars = ax.barh(labels, values, color='#63b3ed', edgecolor='#2b6cb0', height=0.6)
        
        ax.set_xlabel('Maximum Salary', color='gray')
        ax.set_title('TOP jobs by salary', color='white', pad=20, fontsize=14)
        
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('gray')
        ax.spines['left'].set_color('gray')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width + (max(values)*0.02), bar.get_y() + bar.get_height()/2, 
                    f'{int(width)}', 
                    va='center', ha='left', color='#68d391', fontweight='bold', fontsize=10)
        
        ax.invert_yaxis()
        self.figure.tight_layout()
        self.canvas.draw()