from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import sys
import os
import qasync
import asyncio
import webbrowser
import qdarktheme

from data.category import categories
from Services.job_manager import get_table_data
from Services.statistics_service import calculate_salary_statistics
from helpers.chart_helper import ChartHelper

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
        self.tabWidget.setCurrentIndex(0)

        self.AddSkillBtn.clicked.connect(self.add_skill)
        self.Submit.clicked.connect(self.on_find_job_clicked)
        self.SkillList.itemDoubleClicked.connect(self.remove_skill)

        self.init_category_combobox()
        
        self.chart_helper = ChartHelper(self.tabWidget, 1)

        self.showMaximized()

    def init_category_combobox(self):
        for name, slug in categories.items():
            self.CategoryComboBox.addItem(name, userData=slug)

    def add_skill(self):
        skill_text = self.SkillInput.text().strip()
        if skill_text:
            self.SkillList.addItem(skill_text)
            self.SkillInput.clear()
            self.SkillInput.setFocus()

    def remove_skill(self, item):
        row = self.SkillList.row(item)
        self.SkillList.takeItem(row)
        
    def get_user_skills(self):
        skills = []
        for index in range(self.SkillList.count()):
            item = self.SkillList.item(index)
            skills.append(item.text())
        return skills

    @qasync.asyncSlot()
    async def on_find_job_clicked(self):
        category_slug = self.CategoryComboBox.currentData()
        job_title = self.JobTitle.text()
        user_skills = self.get_user_skills()

        if not user_skills:
            QtWidgets.QMessageBox.warning(self, "Alert", "Add at least one skill")
            return

        self.Submit.setEnabled(False)
        self.Submit.setText("Searching")

        try:
            jobs_result = await get_table_data(category_slug, job_title, user_skills)

            if not jobs_result:
                QtWidgets.QMessageBox.information(self, "Result", "Jobs not found! Try to change job title or category")
            else:
                self.populate_table(jobs_result)

                salary_stats = calculate_salary_statistics(jobs_result)
                
                self.chart_helper.draw_salary_chart(salary_stats)

        finally:
            self.Submit.setEnabled(True)
            self.Submit.setText("Find Job")
    
    def populate_table(self, jobs):
        self.tableWidget.setRowCount(0)
        
        for row_index, job in enumerate(jobs):
            self.tableWidget.insertRow(row_index)
            
            self.tableWidget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(job.get('position', 'N/A'))))
            self.tableWidget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(job.get('company', 'N/A'))))
            
            salary = job.get('salary')
            salary_str = str(salary) if salary else "Not specified"
            self.tableWidget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(salary_str))
            
            self.tableWidget.setItem(row_index, 3, QtWidgets.QTableWidgetItem(str(job.get('match_rate', 'N/A'))))

            btn_email = QtWidgets.QPushButton("Send")
            btn_email.setCursor(Qt.PointingHandCursor)
            btn_email.clicked.connect(lambda checked, j=job: self.on_send_email_clicked(j))
            self.tableWidget.setCellWidget(row_index, 4, btn_email)

            btn_browser = QtWidgets.QPushButton("🌐 Open")
            btn_browser.setCursor(Qt.PointingHandCursor)
            job_url = job.get('url', '')
            btn_browser.clicked.connect(lambda checked, u=job_url: self.on_open_browser_clicked(u))
            self.tableWidget.setCellWidget(row_index, 5, btn_browser)

    def on_open_browser_clicked(self, url):
        if url:
            webbrowser.open(url)
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "There is no link for this vacancy")

    def on_send_email_clicked(self, job_data):
        job_title = job_data.get('title', 'Unknown')
        company = job_data.get('company_name', 'Unknown')
        QtWidgets.QMessageBox.information(
            self, 
            "Email Simulation", 
            f"Тут буде логіка відправки email!\n\nГотуємо лист про вакансію:\n{job_title} в компанії {company}"
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    window = Ui()
    
    with loop:
        loop.run_forever()