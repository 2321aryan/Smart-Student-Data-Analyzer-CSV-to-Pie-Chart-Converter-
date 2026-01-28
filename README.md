# 📊 Smart Student Data Analyzer (CSV to Pie Chart Converter)

A **Streamlit-based data analysis application** that intelligently analyzes student performance data from CSV files and generates **interactive pie charts**, rankings, and pass/fail insights automatically.

---

## 🚀 Project Overview

The **Smart Student Data Analyzer** allows users to upload one or multiple CSV files containing student marks. The application automatically:

* Detects student name and subject columns
* Calculates total marks, percentage, and rank
* Generates smart pie charts (Top N + Others)
* Displays pass vs fail distribution
* Provides downloadable chart images

This project is ideal for **teachers, institutions, and students** who want quick visual insights from academic datasets.

---

## ✨ Key Features

* 📂 Upload **multiple CSV files** (auto-merged)
* 🧠 **Smart column detection** (names & subjects)
* 🥧 Dynamic **Top-N student pie charts**
* 📊 Subject-wise or total marks analysis
* ✅ **Pass vs Fail** visualization
* 🏆 Automatic **ranking & top 10 students table**
* ⬇️ Download charts as PNG
* 🌐 Simple, clean **Streamlit UI**

---

## 🛠️ Tech Stack

* **Python 3**
* **Streamlit** – UI framework
* **Pandas** – Data processing
* **Matplotlib** – Chart generation

---

## 📁 Project Structure

```text
csv-to-pie-chart-converter/
│
├── app.py
├── *.png                # Sample generated pie charts
└── README.md
```

---

## ▶️ How to Run the Project

### 1️⃣ Install Dependencies

```bash
pip install streamlit pandas matplotlib
```

### 2️⃣ Run the Application

```bash
streamlit run app.py
```

### 3️⃣ Open in Browser

```text
http://localhost:8501
```

---

## 📄 CSV File Requirements

Your CSV file should contain:

* One column for **student names**
* Multiple **numeric subject columns**

✅ The app automatically detects:

* Student name column (e.g., Name, Student, Candidate)
* Subject columns (numeric values only)

Example:

```csv
Name,Maths,Physics,Chemistry
Aryan,85,78,90
Rahul,72,80,68
```

---

## 📊 Analysis Performed

* **Total Marks** = Sum of subject marks
* **Percentage** = (Total / Maximum Marks) × 100
* **Rank** = Based on percentage (dense ranking)
* **Result**:

  * Pass → Percentage ≥ 40
  * Fail → Percentage < 40

---

## 📥 Outputs Generated

* 🎯 Top-N Students Pie Chart
* 📈 Subject-wise Performance Pie Chart
* ✅ Pass vs ❌ Fail Distribution
* 🏆 Top 10 Students Table
* 🖼️ Downloadable PNG charts

---

## ⚠️ Notes & Limitations

* CSV must contain numeric subject columns
* Marks assumed to be out of **100 per subject**
* Designed for **educational datasets**
* Not intended for real-time database usage

---

## 🎓 Use Cases

* School & college result analysis
* Academic performance visualization
* Student ranking systems
* Data visualization projects
* Mini-projects / Final-year projects

---

## 📜 License

This project is open-source and intended for **educational and learning purposes**.
