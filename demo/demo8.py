from csv import excel
from operator import imod
from PySide2.QtWidgets import QApplication, QMessageBox, QPlainTextEdit, QLabel, QLineEdit, QPushButton
from PySide2.QtUiTools import QUiLoader


import sys
import os  
import pandas as pd 


class Stats:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('excel.ui')
        print(self.ui.__dict__)  # 可以实时了解目前的对象

        self.ui.excel2xls_button.clicked.connect(self.excel2xls)
        self.ui.xls2excel_button.clicked.connect(self.xls2excel)
        # self.ui.count_people_button.clicked.connect(self.count_people_nums)
        # self.ui.count_age_button.clicked.connect(self.count_age_sum) 


    def mkdir(self, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)


    def get_df_data(self, sheetname):
        if sheetname.endswith('xlsx'):
            return pd.read_excel(sheetname, header=None)
        else:
            return pd.read_csv(sheetname, header=None)

    
    def excel2xls(self):
        # 将excel表格基于sheet拆分为单个表
        input_dir = self.ui.input_line.text()
        output_dir = self.ui.output_line.text()
        self.mkdir(output_dir)
        info = self.ui.main_text.toPlainText()
        for line in info.splitlines():
            if not line.strip():
                continue
            excelname = line.strip('')
            excelname = os.path.join(input_dir, excelname)
            excel_reader = pd.ExcelFile(excelname) 
            sheet_names = excel_reader.sheet_names 

            for sheet in sheet_names:
                xls_name = os.path.join(output_dir, sheet + '.xlsx')
                df_data = excel_reader.parse(sheet_name=sheet)
                df_data.to_excel(xls_name, index=False)

        QMessageBox.about(self.ui,
                '拆分完成',
                f'输出目录：{output_dir}\n结果文件：{sheet_names}' )


    def xls2excel(self):
        # 将多个xls文件合并为一个excel
        input_dir = self.ui.input_line.text()
        output_dir = self.ui.output_line.text()
        self.mkdir(output_dir)
        out_excel_name = self.ui.main_text.toPlainText().strip('')
        out_excel_name = os.path.join(output_dir, out_excel_name)

        excel_writer = pd.ExcelWriter(out_excel_name)
        all_sheetnames = os.listdir(input_dir)  # 列出输入目录下面的全部表格xls
        for sheet in all_sheetnames:
            sheetname = sheet.replace('.xlsx', '')
            sheet = os.path.join(input_dir, sheet)
            df = self.get_df_data(sheet)
            # print('lll', df)
            df.to_excel(excel_writer, sheet_name=sheetname, index=False, header=False)

        excel_writer.save()
        excel_writer.close()

        QMessageBox.about(self.ui,
            '合并完成',
            f'输出结果：{out_excel_name}' )



    def test(self):
        # 测试组间功能 
        line_content = self.ui.input_line.text()
        print(line_content)

 




app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()