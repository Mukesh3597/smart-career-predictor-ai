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

    def _fallback_predict(self, tenth, twelfth, grad, skill_count):
        avg = (tenth + twelfth + grad) / 3.0
        if avg >= 85:
            career = "AI / Data Science"
        elif avg >= 70:
            career = "Software Development"
        else:
            career = "IT Support / Operations"

        salary = 3.0 + (avg / 100.0) * 12.0
        return career, float(round(salary, 2))

    def _apply_city_multiplier(self, salary: float, city: str) -> float:
        city_multiplier = {
            "bangalore": 1.30,
            "hyderabad": 1.25,
            "pune": 1.20,
            "noida": 1.15,
            "delhi": 1.15,
            "kolkata": 1.00,
            "lucknow": 0.95,
            "jaipur": 0.92,
            "bhopal": 0.88,
            "patna": 0.85,
            "bijnor": 0.70
        }
        multiplier = city_multiplier.get((city or "").strip().lower(), 1.0)
        return round(salary * multiplier, 2)

    def _build_recommendation(self, career: str, interest: str, city: str, skills: list[str]) -> str:
        city = (city or "").strip()
        interest = (interest or "").strip().lower()
        skill_text = ", ".join(skills) if skills else "basic skills"

        if city.lower() == "bijnor":
            return (
                f"आपका predicted field '{career}' है। लेकिन {city} जैसे small city में direct high-paying tech roles कम हो सकते हैं। "
                f"इसलिए आपको remote jobs, internships, freelancing, और metro-city opportunities पर focus करना चाहिए. "
                f"आपकी current skills ({skill_text}) और interest '{interest}' इस field के लिए useful हैं।"
            )

        return (
            f"आपका predicted field '{career}' है। आपकी skills ({skill_text}) और interest '{interest}' इस direction के लिए अच्छे हैं। "
            f"{city or 'आपके city'} में growth के साथ remote opportunities भी explore करें।"
        )

    # ✅ FIXED roadmap (पहले गलत था)
    def _build_roadmap(self, career: str) -> list[str]:
        roadmap_map = {
            "AI / Data Science": [
                "Python मजबूत करो",
                "NumPy, Pandas, Matplotlib सीखो",
                "Machine Learning basics सीखो",
                "Projects बनाओ",
                "Internship apply करो"
            ],
            "Software Development": [
                "Programming language सीखो",
                "DSA सीखो",
                "Projects बनाओ",
                "GitHub use करो",
                "Internship apply करो"
            ]
        }
        return roadmap_map.get(career, ["Skills सीखो", "Projects बनाओ"])

    # ✅ NEW functions
    def _get_companies(self, career: str) -> list[str]:
        company_map = {
            "Software Development": ["TCS", "Infosys", "Wipro"],
            "AI / Data Science": ["Google", "Amazon", "Microsoft"]
        }
        return company_map.get(career, ["Startups"])

    def _get_job_links(self, career: str) -> list[str]:
        job_map = {
            "Software Development": [
                "https://www.naukri.com/software-developer-jobs",
                "https://www.linkedin.com/jobs/software-engineer-jobs"
            ],
            "AI / Data Science": [
                "https://www.naukri.com/data-scientist-jobs",
                "https://www.linkedin.com/jobs/data-scientist-jobs"
            ]
        }
        return job_map.get(career, ["https://www.linkedin.com/jobs"])

    def _get_internships(self) -> list[str]:
        return [
            "https://internshala.com/",
            "https://www.linkedin.com/jobs/internships/",
            "https://wellfound.com/"
        ]

    def _get_courses(self, career: str) -> list[str]:
        course_map = {
            "Software Development": [
                "https://www.freecodecamp.org/",
                "https://www.udemy.com/course/java-the-complete-java-developer-course/"
            ],
            "AI / Data Science": [
                "https://www.kaggle.com/learn",
                "https://www.coursera.org/professional-certificates/google-data-analytics"
            ]
        }
        return course_map.get(career, ["https://www.youtube.com"])

    def predict(self, tenth_pct, twelfth_pct, graduation_pct, skills, interest, city):
        skill_count = len(skills) if skills else 0
        X = np.array([[tenth_pct, twelfth_pct, graduation_pct, skill_count]])

        if self.career_model is None or self.salary_model is None or self.encoder is None:
            predicted_career, predicted_salary = self._fallback_predict(
                tenth_pct, twelfth_pct, graduation_pct, skill_count
            )
        else:
            career_pred = self.career_model.predict(X)[0]
            predicted_career = self.encoder.inverse_transform([career_pred])[0]
            predicted_salary = float(self.salary_model.predict(X)[0])
            predicted_salary = round(predicted_salary, 2)

        predicted_salary = self._apply_city_multiplier(predicted_salary, city)
        recommendation = self._build_recommendation(predicted_career, interest, city, skills or [])
        roadmap = self._build_roadmap(predicted_career)

        # ✅ FIXED
        companies = self._get_companies(predicted_career)
        job_links = self._get_job_links(predicted_career)
        internships = self._get_internships()
        courses = self._get_courses(predicted_career)

        return {
            "predicted_career": str(predicted_career),
            "predicted_salary": predicted_salary,
            "recommendation": recommendation,
            "roadmap": roadmap,
            "companies": companies,
            "job_links": job_links,
            "internships": internships,
            "courses": courses
        }


ml_service = MLService()