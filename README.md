# Smart Career Predictor AI 🚀

A full-stack Machine Learning web application that predicts a user's **Job Title** and **Expected Salary (LPA)** based on academic performance and skills.

Built with **FastAPI**, **Scikit-learn**, and **SQL Database** with a modern web UI.

---

## ✨ Features

- ✅ Predict **Job Title** (Career)
- ✅ Predict **Expected Salary (LPA)**
- ✅ Modern Website UI (Header + Sections + Footer)
- ✅ Stores prediction history in database
- ✅ Swagger API Docs available at `/docs`
- ✅ Docker-ready (optional)

---

## 🧠 Tech Stack

**Backend**
- FastAPI (Python)
- SQLAlchemy
- SQLite (Local) / PostgreSQL (Deploy)

**Machine Learning**
- Scikit-learn (RandomForest Classifier + Regressor)
- Joblib for model persistence

**Frontend**
- HTML, CSS, JavaScript (served by FastAPI)

---

## 📁 Project Structure


career-predictor-ai/
backend/
app/
ml/
static/
index.html
style.css
script.js
requirements.txt
Dockerfile


---

## ⚙️ Setup & Run (Local)

### 1 Create & Activate Virtual Environment
```bash
cd backend
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
2) Install Requirements
pip install -r requirements.txt
3) Generate Dataset (Synthetic)
cd ml
python generate_data.py
4) Train ML Models
python train_model.py
5) Run FastAPI Server
cd ..
uvicorn app.main:app --reload

Open:

Website: http://127.0.0.1:8000/

API Docs: http://127.0.0.1:8000/docs

🔥 API Usage (Example)
POST /predict/

Request body:

{
  "full_name": "Mukesh",
  "email": "mukesh@test.com",
  "tenth_pct": 88,
  "twelfth_pct": 82,
  "graduation_pct": 79,
  "skills": ["python", "sql", "ml"],
  "interest": "ai",
  "city": "Delhi"
}

Response:

{
  "predicted_career": "AI / Data Science",
  "predicted_salary": 10.3,
  "saved_prediction_id": 1
}
🧪 Notes

Salary is estimated in LPA and depends on model training data.

Models are stored in backend/ml/artifacts/.

📌 Author

Mukesh
GitHub: https://github.com/Mukesh3597