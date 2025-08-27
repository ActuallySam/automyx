# 🍽️ Swiggy Delivery Spend Analyzer

This script (`spendings.py`) fetches and analyzes your Swiggy order history for the past year, calculating your total delivery spends. It handles paginated order data and provides a summary of your expenses.

---

## 📋 What It Does

- **Fetches Swiggy Orders:**  
  Retrieves all your Swiggy orders from the last 12 months using Swiggy's order history API, handling pagination automatically.

- **Calculates Total Spend:**  
  Sums up the total amount spent on orders, giving you a clear picture of your delivery expenses.

- **Customizable:**  
  You can adjust the script to filter by city or date range as needed.

---

## ⚙️ Usage

1. **Install Dependencies**  
   Make sure you have Python 3.7+ and required libraries installed.

2. **Run the Script**  
   Navigate to this directory and execute:
   ```bash
   python spendings.py
   ```

3. **View Results**  
   The script will output your total Swiggy delivery spend for the past year.

---

## 📝 Notes

- You may need to provide your Swiggy authentication details (such as cookies or tokens) for the script to access your order history.
- The script is intended for personal use and educational purposes only.

---