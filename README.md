# Duplicate-Invoice-Solution
AI-powered duplicate invoice detection enriched with process mining to uncover root causes and prevent financial leakage.

# Process-Enriched Duplicate Invoice Detection

## 📌 Project Description
This project is an early-stage prototype that enhances traditional **duplicate invoice detection** by linking it to **process mining insights**.

Using the **Purchase-to-Pay (P2P) event logs** from the [4TU Data Centre (BPI Challenge)](https://data.4tu.nl/), we aim to:
- Detect **exact and near-duplicate invoices** using fuzzy/NLP-based matching.
- Correlate duplicates with their **end-to-end process traces** (activities, users, timestamps).
- Analyze **root causes** of duplication (manual entry, workflow deviations, master data issues).
- Lay the foundation for **risk scoring and proactive prevention** in Accounts Payable processes.

This work moves beyond simple detection and focuses on **why duplicates happen** and **how to prevent them**.

---

## 🎯 What We’re Trying to Do
- Move from **reactive detection** → **proactive prevention**.
- Provide **explainability**: clear reasons why invoices are flagged as duplicates.
- Enable **AP and compliance teams** to address upstream process gaps.

---

## ⚙️ Setup Instructions (Virtual Environment + Dependencies)

> **Prerequisites**
> - Python **3.9+** installed (`python --version`)
> - Git installed

### 1) Clone the Repository
```bash
git clone https://github.com/uppili-srinivasan/Duplicate-Invoice-Solution.git
cd Duplicate-Invoice-Solution
```

### 2) Create & Activate a Virtual Environment
- For mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
- For Windows (PowerShell):
```bash
py -3 -m venv venv
.\venv\Scripts\Activate.ps1
```
### 3) Create `requirements.txt`
Create a file named **`requirements.txt`** in the project root and copy the following into it:

```txt
pandas
numpy
pm4py
rapidfuzz
matplotlib
seaborn
jupyter
```
### 4) Upgrade pip and Install Dependencies
Make sure your `pip` is up to date, then install all required dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

