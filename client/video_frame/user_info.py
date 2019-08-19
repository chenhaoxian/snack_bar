from PyQt5.QtWidgets import QWidget,QLabel, QFormLayout, QTableWidget, QTableWidgetItem, QVBoxLayout
from utils import store_snack

class UserInfo(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        main_layout = QVBoxLayout()
        base_info_layout = QFormLayout()
        main_layout.addLayout(base_info_layout)

        self.domain_id = QLabel()
        self.weichat_name = QLabel()
        self.total_price_label = QLabel()
        self.snacks_table = QTableWidget()
        self.snacks_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.snacks_table.setColumnCount(4)
        self.snacks_table.setHorizontalHeaderLabels(('Snack', 'Unit Price', 'Quantity', 'Total Price'))
        # self.snacks_table.setItem(0, 0, QTableWidgetItem("product 1"))
        # self.snacks_table.setItem(0, 1, QTableWidgetItem("1"))
        # self.snacks_table.setItem(0, 2, QTableWidgetItem("2.5"))
        # self.snacks_table.setItem(0, 3, QTableWidgetItem("2.5"))
        #
        # self.snacks_table.setItem(1, 0, QTableWidgetItem("product 2"))
        # self.snacks_table.setItem(1, 1, QTableWidgetItem("2"))
        # self.snacks_table.setItem(1, 2, QTableWidgetItem("3"))
        # self.snacks_table.setItem(1, 3, QTableWidgetItem("6"))

        NO_INFO = 'No Info'

        self.domain_id.setText(NO_INFO)
        self.weichat_name.setText(NO_INFO)
        # self.total_price_label.setText('8.5')
        # base_info_layout.addRow(QLabel('Domain Id:'), self.domain_id)
        base_info_layout.addRow(QLabel('Name:'), self.weichat_name)
        base_info_layout.addRow(QLabel('Total Price:'), self.total_price_label)
        main_layout.addWidget(self.snacks_table)

        self.setLayout(main_layout)

    def set_domain_id(self,domain_id):
        self.domain_id.setText(domain_id)

    def set_weichat_name(self, weichat_name):
        self.weichat_name.setText(weichat_name)


    def set_snack(self, order_data):
        self.snacks_table.clearContents()
        processed_data = store_snack.process_order_for_server(order_data)

        self.snacks_table.setRowCount(len(processed_data['record']))
        for index in range(len(processed_data['record'])):
            data = processed_data['record'][index]
            name = QTableWidgetItem(str(data['snack_name']))
            quantity = QTableWidgetItem(str(data['amount']))
            unit_price = QTableWidgetItem(str(data['snack_price']))
            total_price = QTableWidgetItem(str(float(data['snack_price'])*int(data['amount'])))

            self.snacks_table.setItem(index, 0, name)
            self.snacks_table.setItem(index, 1, unit_price)
            self.snacks_table.setItem(index, 2, quantity)
            self.snacks_table.setItem(index, 3, total_price)

            # self.snacks_table.setItem(0, 0, QTableWidgetItem("product 1"))
            # self.snacks_table.setItem(0, 1, QTableWidgetItem("1"))
            # self.snacks_table.setItem(0, 2, QTableWidgetItem("2.5"))
            # self.snacks_table.setItem(0, 3, QTableWidgetItem("2.5"))

        self.total_price_label.setText(str(processed_data['total_price']))

    # def add_snack(self, data):
    #     row_position = self.snacks_table.rowCount()


