from PyQt5 import QtWidgets, uic,QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys
import os
from data.category import categories

dirname = os.path.dirname(QtWidgets.__file__)
plugin_path = os.path.join(dirname, 'Qt5', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

class Ui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('views/main.ui', self)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.AddSkillBtn.clicked.connect(self.add_skill)

        self.Submit.clicked.connect(self.search_jobs)

        self.init_category_combobox();

        self.show();

    def init_category_combobox(self):
        for name, slug in categories.items():
            self.CategoryComboBox.addItem(name, userData=slug)

    def add_skill(self):
        """Функція, яка бере текст з поля і додає його у список"""
        skill_text = self.SkillInput.text().strip()
        
        if skill_text:
            self.SkillList.addItem(skill_text)
            self.SkillInput.clear()
            self.SkillInput.setFocus()
    def get_search_querry(self):
        
        category = self.CategoryComboBox.currentData()
        title = self.JobTitle.text().strip()
        return f'https://remotive.com/api/remote-jobs?category={category}&search={title}&limit=10'
    
    def search_jobs(self):
        
        print(self.get_search_querry())

        jobs_list =  []
    
        if len(jobs_list) == 0:
            QtWidgets.QMessageBox.information(
                self,
                "Search Result",
                "Unfortunately, no jobs were found for your search. Try changing the category or keyword."
            )
            return
        
        self.tabWidget.setCurrentIndex(1)
    
    def get_user_skills(self):
        skills = []
        for index in range(self.SkillList.count()):
            item = self.SkillList.item(index)
            skills.append(item.text())
            
        return skills

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
