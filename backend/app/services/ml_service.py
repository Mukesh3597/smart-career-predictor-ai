# ✅ File: backend/app/services/ml_service.py

import os
import joblib
import numpy as np
from app.config import ARTIFACT_DIR


class MLService:
    def __init__(self):
        self.career_model = None
        self.salary_model = None
        self.encoder = None
        self._load_artifacts()

    def _load_artifacts(self):
        career_path = os.path.join(ARTIFACT_DIR, "career_model.pkl")
        salary_path = os.path.join(ARTIFACT_DIR, "salary_model.pkl")
        enc_path = os.path.join(ARTIFACT_DIR, "encoder.pkl")

        if os.path.exists(career_path):
            self.career_model = joblib.load(career_path)

        if os.path.exists(salary_path):
            self.salary_model = joblib.load(salary_path)

        if os.path.exists(enc_path):
            self.encoder = joblib.load(enc_path)

    def _fallback_predict(self, tenth, twelfth, grad, skill_count, interest, city):
        avg = (tenth + twelfth + grad) / 3.0

        if avg >= 85:
            career = "AI / Data Science"
        elif avg >= 70:
            career = "Software Development"
        else:
            career = "IT Support / Operations"

        salary = 3.0 + (avg / 100.0) * 12.0
        return career, float(round(salary, 2))

    def predict(self, tenth_pct, twelfth_pct, graduation_pct, skills, interest, city):
        skill_count = len(skills) if skills else 0
        interest = (interest or "").strip().lower()
        city = (city or "").strip().lower()

        # Model features (must match training)
        X = np.array([[tenth_pct, twelfth_pct, graduation_pct, skill_count]])

        # If models missing, use fallback
        if self.career_model is None or self.salary_model is None or self.encoder is None:
            return self._fallback_predict(tenth_pct, twelfth_pct, graduation_pct, skill_count, interest, city)

        # ✅ Career prediction (decode label)
        career_pred = self.career_model.predict(X)[0]
        career_label = self.encoder.inverse_transform([career_pred])[0]

        # ✅ Salary prediction
        salary_pred = float(self.salary_model.predict(X)[0])
        salary_pred = round(salary_pred, 2)

        return str(career_label), salary_pred


ml_service = MLService()