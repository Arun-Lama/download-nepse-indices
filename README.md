# 📈 Daily Stock Price Downloader 🚀

![GitHub Workflow Status](https://github.com/Arun-Lama/download-nepse-indices/blob/main/.github/workflows/workflow_automation.yaml)

> A Python automation tool that scrapes daily NEPSE stock prices from Sharesansar and updates a historical dataset in Google Sheets.  
> The process is fully automated and runs daily using GitHub Actions.

---

## 📊 [View Live Google Sheet](https://docs.google.com/spreadsheets/d/1VvJsBXRGZ7sKRhGeHr-DCjnESjiYWsVm-A0ZIYG6en0/edit?usp=sharing) <!-- 🔗 Replace `#` with the actual URL -->

---

## ✨ Features

- 🕒 **Automated Daily Scraping** of NEPSE indices data from Sharesansar
- 📈 **Clean Data Processing** using `pandas`
- 🔄 **Google Sheets Synchronization** via `gspread`
- 🤖 **Headless Browser Automation** with `Selenium`
- 📅 **Scheduled Execution** via GitHub Actions (⏰ Every Sunday–Thursday at 3:25 PM NPT)
- 🔐 **Secure Credential Management** using Base64-encoded environment variables
- 📋 **Comprehensive Logging** and easy debugging
- ⚙️ **Lightweight and Serverless** – no hosting or cron job required

---

## 🛠️ Installation & Setup

### ✅ Prerequisites

- Python **3.8+**
- A **Google Cloud Platform service account** with Google Sheets & Drive API access
- Access to **Sharesansar.com**
- GitHub repository with **Secrets** configured

---

### 🔁 Step 1: Clone the Repository

```bash
git clone https://github.com/Arun-Lama/download-nepse-indices/tree/main.git
cd download-nepse-indices
```

---

### 🔑 Step 2: Configure Secrets

In your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add a new **Secret** with:
   - **Name:** `GCP_SA_KEY_BASE64`
   - **Value:** Your base64-encoded Google service account JSON key

---

### 🧪 Step 3: Run Locally (Optional)

If you'd like to test the script locally:

```bash
pip install -r requirements.txt
python download_indices.py
```

Make sure to export your environment variable before running:

```bash
export GCP_SA_KEY_BASE64='your_base64_key_here'
```

---

## 🔄 Workflow Automation (GitHub Actions)

The script is automatically run via GitHub Actions on this schedule:

```
🕒 3:25 PM NPT (9:40 AM UTC) | Sunday to Thursday
```

You can also manually trigger the workflow via the **"Run Workflow"** button in GitHub Actions tab.

---

## 📁 Project Structure

```
📦 Daily-Stock-Price-Download/
├── .github/
│   └── workflows/
│       └── workflow_automation.yaml
├── download_indices.py
├── read_write_google_sheet.py
├── requirements.txt
└── README.md
└── .gitignore
```

---

## 🧾 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙋‍♂️ Author

Built by [Arun Lama](https://github.com/Arun-Lama)  
Feel free to ⭐ star the repo and suggest improvements!
