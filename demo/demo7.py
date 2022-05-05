#!/usr/bin/env python3
#-*- coding:utf-8 -*-


from PySide2.QtWidgets import QApplication, QMessageBox, QPlainTextEdit
from PySide2.QtUiTools import QUiLoader



class Stats:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('ui_design.ui')
        print(self.ui.__dict__)  # 可以实时了解目前的对象

        self.ui.count_people_button.clicked.connect(self.count_people_nums)
        self.ui.count_age_button.clicked.connect(self.count_age_sum)

    def count_people_nums(self):
        # 响应统计人数信号
        info = self.ui.plainTextEdit.toPlainText()
        all_numbers = 0
        for line in info.splitlines():
            if not line.strip():
                continue
            linelist = line.strip('').split('\t')
            name, salary, age = linelist
            all_numbers += 1
            print(linelist)
        
        QMessageBox.about(self.ui,
                    '结果',
                    f'{all_numbers}' )


    def count_age_sum(self):
        # 统计全部人员的年龄之和
        info = self.ui.plainTextEdit.toPlainText()
        age_numbers = 0
        for line in info.splitlines():
            if not line.strip():
                continue
            linelist = line.strip('').split('\t')
            name, salary, age = linelist
            age_numbers += int(age)
            print(linelist)
        
        QMessageBox.about(self.ui,
                    '结果',
                    f'{age_numbers}' )



app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()