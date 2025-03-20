import sys
import mysql.connector
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",  
        password="your_password",  
        database="BillingSystem"
    )

class BillingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Billing System")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        self.name_label = QLabel("Customer Name:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        
        self.phone_label = QLabel("Phone Number:")
        self.phone_input = QLineEdit()
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)

        
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

    
        self.amount_label = QLabel("Total Amount:")
        self.amount_input = QLineEdit()
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)


        self.submit_button = QPushButton("Generate Bill")
        self.submit_button.clicked.connect(self.store_bill)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def store_bill(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        total_amount = self.amount_input.text()

        if not name or not phone or not total_amount:
            QMessageBox.warning(self, "Error", "Please fill in all required fields.")
            return

        try:
            db = connect_db()
            cursor = db.cursor()

            
            cursor.execute("SELECT id FROM Customers WHERE phone = %s", (phone,))
            customer = cursor.fetchone()

            if not customer:
                cursor.execute("INSERT INTO Customers (name, phone, email) VALUES (%s, %s, %s)", (name, phone, email))
                db.commit()
                customer_id = cursor.lastrowid
            else:
                customer_id = customer[0]

        
            cursor.execute("INSERT INTO Bills (customer_id, total_amount) VALUES (%s, %s)", (customer_id, total_amount))
            db.commit()

            QMessageBox.information(self, "Success", "Bill stored successfully!")

        
            self.name_input.clear()
            self.phone_input.clear()
            self.email_input.clear()
            self.amount_input.clear()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", str(err))

        finally:
            if db.is_connected():
                cursor.close()
                db.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingApp()
    window.show()
    sys.exit(app.exec())
