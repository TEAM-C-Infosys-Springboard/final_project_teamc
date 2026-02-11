# 🚀 How to Run PyKV

PyKV consists of two parts: the **Backend API** and the **Frontend Dashboard**. You need to run both in separate terminals.

## 1️⃣ Start the Backend (API)
This powers individual operations and data storage.

```bash
python -m uvicorn api.app:app --reload
```
*   **Port:** `8000`
*   **Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 2️⃣ Start the Frontend (Dashboard)
This launches the visual interface.

```bash
python -m streamlit run frontend/dashboard.py
```
*   **Port:** `8501`
*   **URL:** [http://localhost:8501](http://localhost:8501)

---

## 📦 Prerequisites
If you haven't installed dependencies yet:
```bash
pip install fastapi uvicorn streamlit requests pandas altair
```
