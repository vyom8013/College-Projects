import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox,
    QLineEdit, QMessageBox, QFrame
)
from PyQt6.QtGui import QFont

try:
    import menu_module  # Ensure menu_module.py is in the same directory
except ImportError:
    print("Error: 'menu_module' not found. Ensure 'menu_module.py' is in the same directory.")
    sys.exit(1)

class BillingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing System with Table Reservation")
        self.setGeometry(100, 100, 450, 550)
        self.setStyleSheet("background-color: #f4f4f4; border-radius: 15px;")

        # Custom Font
        title_font = QFont("Arial", 14, QFont.Weight.Bold)
        label_font = QFont("Arial", 10)

        # Title Label
        self.title_label = QLabel("🛒 Welcome to Food Billing & Reservation", self)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: black; text-align: center; padding: 10px;")

        # Menu Display
        menu_text = menu_module.display_main_menu()
        self.menu_label = QLabel(f"📜 Menu:\n{menu_text if menu_text else 'Menu loading error'}", self)
        self.menu_label.setFont(label_font)
        self.menu_label.setStyleSheet("color: black; padding: 10px; border: 1px solid #ccc;")

        # Category Selection
        self.category_label = QLabel("🔽 Select a Category:", self)
        self.category_label.setStyleSheet("color: black; padding: 5px;")
        self.category_label.setFont(label_font)
        self.category_dropdown = QComboBox(self)
        self.category_dropdown.addItems([str(i) for i in range(1, 9)])
        self.category_dropdown.setStyleSheet("background-color: white; color: black; padding: 5px; border-radius: 5px;")
        self.category_dropdown.currentIndexChanged.connect(self.update_items)

        # Item Selection
        self.item_label = QLabel("🍽 Select an Item:", self)
        self.item_label.setStyleSheet("color: black; padding: 5px;")
        self.item_label.setFont(label_font)
        self.item_dropdown = QComboBox(self)
        self.item_dropdown.setStyleSheet("background-color: white; color: black; padding: 5px; border-radius: 5px;")

        # Quantity Entry
        self.quantity_label = QLabel("✏️ Enter Quantity:", self)
        self.quantity_label.setStyleSheet("color: black; padding: 5px;")
        self.quantity_label.setFont(label_font)
        self.quantity_entry = QLineEdit(self)
        self.quantity_entry.setPlaceholderText("Enter quantity")
        self.quantity_entry.setStyleSheet("padding: 5px; border: 1px solid #888; border-radius: 5px; color: black;")

        # Name Entry
        self.name_label = QLabel("📝 Enter Your Name:", self)
        self.name_label.setStyleSheet("color: black; padding: 5px;")
        self.name_label.setFont(label_font)
        self.name_entry = QLineEdit(self)
        self.name_entry.setPlaceholderText("Your name")
        self.name_entry.setStyleSheet("padding: 5px; border: 1px solid #888; border-radius: 5px; color: black;")

        # Guests Entry (New Feature)
        self.guests_label = QLabel("👥 Number of Guests:", self)
        self.guests_label.setStyleSheet("color: black; padding: 5px;")
        self.guests_label.setFont(label_font)
        self.guests_entry = QLineEdit(self)
        self.guests_entry.setPlaceholderText("Enter guest count")
        self.guests_entry.setStyleSheet("padding: 5px; border: 1px solid #888; border-radius: 5px; color: black;")

        # Reservation Time Entry (New Feature)
        self.time_label = QLabel("⏳ Reservation Time:", self)
        self.time_label.setStyleSheet("color: black; padding: 5px;")
        self.time_label.setFont(label_font)
        self.time_entry = QLineEdit(self)
        self.time_entry.setPlaceholderText("Enter time (HH:MM AM/PM)")
        self.time_entry.setStyleSheet("padding: 5px; border: 1px solid #888; border-radius: 5px; color: black;")

        # Order Button
        self.order_button = QPushButton("💵 Place Order", self)
        self.order_button.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px; border-radius: 5px;")  
        self.order_button.setFont(title_font)
        self.order_button.setStyleSheet("background-color: #3498db; color: black; padding: 10px; border-radius: 5px;")
        self.order_button.clicked.connect(self.calculate_bill)

        # Result Label
        self.result_label = QLabel("", self)
        self.result_label.setFont(label_font)
        self.result_label.setStyleSheet("color: black; font-weight: bold; padding: 5px;")

        # Layout Setup
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(QFrame(), stretch=1)
        layout.addWidget(self.menu_label)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_dropdown)
        layout.addWidget(self.item_label)
        layout.addWidget(self.item_dropdown)
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_entry)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_entry)
        layout.addWidget(self.guests_label)
        layout.addWidget(self.guests_entry)
        layout.addWidget(self.time_label)
        layout.addWidget(self.time_entry)
        layout.addWidget(self.order_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def update_items(self):
        """Updates item dropdown based on category selection"""
        category = int(self.category_dropdown.currentText())
        menu = menu_module.display_menu(category)

        self.item_dropdown.clear()
        for i, (item, price) in enumerate(menu, start=1):
            self.item_dropdown.addItem(f"{item} - Rs.{price}", i)

    def calculate_bill(self):
        """Processes the order and displays the bill including reservation details"""
        try:
            category = int(self.category_dropdown.currentText())
            item_choice = self.item_dropdown.currentIndex()
            qty = int(self.quantity_entry.text().strip())
            user_name = self.name_entry.text().strip()
            guests = int(self.guests_entry.text().strip())
            reservation_time = self.time_entry.text().strip()

            if any(value == "" for value in [user_name, reservation_time]) or item_choice < 0 or qty <= 0 or guests <= 0:
                QMessageBox.warning(self, "Input Error", "Ensure all fields are correctly filled.")
                return

            item_name, price, total_qty = menu_module.take_order(category, item_choice + 1, qty)
            total_amount = price * total_qty
            bill = total_amount + (total_amount * 0.18)  # Adding 18% GST

            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setStyleSheet("background-color: #f4f4f4; color: black;")
            msg_box.setFont(QFont("Arial", 10))
            msg_box.setWindowTitle("Order Summary")
            msg_box.setStyleSheet("QMessageBox { background-color: #f4f4f4; color: black; }"
                                  "QPushButton { background-color: #3498db; color: white; padding: 10px; border-radius: 5px; }"
                                  "QLabel { color: black; }")
            msg_box.setText(
                f"📝 Order Details:\n"
                f"🍽 Item Ordered: {item_name}\n"
                f"💰 Price per Item: Rs.{price}\n"
                f"🔢 Quantity: {total_qty}\n"
                f"💵 GST (18%): Rs.{total_amount * 0.18}\n"
                f"💰 Total Bill: Rs.{bill}\n"
                f"👥 Guests: {guests}\n"
                f"⏳ Reservation Time: {reservation_time}\n"
                f"🙌 Thank you, {user_name}! Your table is reserved!"
            )
            msg_box.exec()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{str(e)}")

# Run the application
app = QApplication(sys.argv)
window = BillingApp()
window.show()
sys.exit(app.exec())