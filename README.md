
# Medical Insurance Predictor

## 📝 Description
This repository contains a comprehensive Python-based application designed to **predict medical insurance costs** and **recommend suitable insurance policies** using machine learning techniques.

Built with **Tkinter** for the GUI, the app integrates **pre-trained ML models** (via `.pkl` files), uses **SQLite** for database operations, and includes advanced features such as:

- User Authentication with CAPTCHA
- Prediction History
- Policy Listings
- BMI Calculator
- Contact Form
- Admin Dashboard for user & policy management

This tool is tailored for users seeking **personalized insurance cost estimates** and **policy recommendations** based on their age, BMI, income, and lifestyle.

---

## ✨ Features

- 🔐 **User Authentication:** Secure login & registration with CAPTCHA.
- 💸 **Insurance Cost Prediction:** Regression model estimates total and monthly premiums.
- 📊 **Policy Recommendations:** Classification model suggests policy tiers and providers.
- 🕓 **Prediction History:** Tracks and displays all previous predictions.
- 📄 **Policy Listings:** View and filter available insurance policies.
- ⚖️ **BMI Calculator:** Calculate and categorize BMI with visual feedback.
- 📬 **Contact Us:** Send messages via built-in form.
- 🛠️ **Admin Dashboard:** Add/delete users and policies (admin only).

---

## ⚙️ Installation

### ✅ Prerequisites

- Python 3.6 or higher
- Required Libraries:
  - `tkinter`
  - `Pillow`
  - `pandas`
  - `pickle`
  - `sqlite3`

### 📂 Required Files

- **Models**: `regression_model.pkl`, `classification_model.pkl`, `scaler.pkl`
- **Dataset**: `dataset11.xlsx`
- **Images**: `left.jpg`, `right.jpg`, `2.jpg` (UI backgrounds)
- **Database**: `insurance_data.db` *(auto-generated on first run)*

### 📥 Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/kethavathsamba/medical-insurance-predictor.git
   cd medical-insurance-predictor
   ```

2. **Install Dependencies:**
   ```bash
   pip install Pillow pandas
   ```

   > Note: `tkinter` and `sqlite3` are usually pre-installed with Python. If not:
   ```bash
   sudo apt-get install python3-tk
   ```

3. **Add Required Files:**
   - Place all `.pkl` models, `dataset11.xlsx`, and `.jpg` images in the project directory.

4. **Run the App:**
   ```bash
   python App.py
   ```

---

## 🚀 Usage

1. **Startup:**
   - On launch, click **"Get Started"**.
2. **Register/Login:**
   - Complete CAPTCHA and register or log in.
3. **Main Navigation:**
   - **Home:** Enter data and click **Predict**.
   - **Policies:** View all insurance policies.
   - **Histories:** View past prediction records.
   - **BMI Calculator:** Get BMI and health status.
   - **Contact Us:** Send feedback or support requests.
   - **Admin Update:** Admin panel to manage data.
4. **Output:**
   - Predictions and logs are saved to `outputs`.

---

## 🤝 Contributing

We welcome contributions!  
Follow these steps:

1. **Fork the Repo**
2. **Create a Branch**
   ```bash
   git checkout -b feature/bmi-enhancement
   ```
3. **Make Changes & Commit**
   ```bash
   git commit -m "Add BMI category color coding"
   ```
4. **Push to GitHub**
   ```bash
   git push origin feature/bmi-enhancement
   ```
5. **Open a Pull Request**

For major changes, open an issue first to discuss the idea.

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Libraries: Tkinter, Pillow, Pandas
- Inspired by healthcare data analysis & ML use cases

---

