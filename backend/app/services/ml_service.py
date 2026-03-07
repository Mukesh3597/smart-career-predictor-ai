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

    def _build_roadmap(self, career: str) -> list[str]:
        roadmap_map = {
            "AI / Data Science": [
                "Python मजबूत करो",
                "NumPy, Pandas, Matplotlib सीखो",
                "Machine Learning basics सीखो",
                "Scikit-learn projects बनाओ",
                "SQL और data handling सीखो",
                "Deep Learning basics शुरू करो",
                "2 strong portfolio projects बनाओ",
                "Internship या freelance opportunities ढूँढो"
            ],
            "Software Development": [
                "Python/Java/C++ में से एक language मजबूत करो",
                "DSA basics सीखो",
                "OOP concept clear करो",
                "Web development basics सीखो",
                "Git और GitHub use करो",
                "2 full-stack projects बनाओ",
                "Database integration सीखो",
                "Internship apply करो"
            ],
            "Cyber Security": [
                "Networking basics सीखो",
                "Linux commands सीखो",
                "Cyber security fundamentals पढ़ो",
                "Web vulnerabilities समझो",
                "Ethical hacking basics सीखो",
                "CTF practice करो",
                "Security tools समझो",
                "Entry-level internship target करो"
            ],
            "Cloud / DevOps": [
                "Linux मजबूत करो",
                "Networking basics सीखो",
                "Git और GitHub सीखो",
                "Docker basics सीखो",
                "AWS/Azure fundamentals सीखो",
                "CI/CD concept समझो",
                "Deployment projects बनाओ",
                "DevOps internship apply करो"
            ],
            "Data Analyst": [
                "Excel मजबूत करो",
                "SQL सीखो",
                "Python basics सीखो",
                "Pandas और data cleaning सीखो",
                "Power BI/Tableau सीखो",
                "Data visualization projects बनाओ",
                "Business insight practice करो",
                "Analyst roles apply करो"
            ],
            "Web Development": [
                "HTML, CSS, JavaScript सीखो",
                "Responsive design बनाना सीखो",
                "Frontend framework basics सीखो",
                "Backend basics सीखो",
                "Database connect करना सीखो",
                "Authentication समझो",
                "2-3 website projects बनाओ",
                "Freelancing/Internship शुरू करो"
            ],
            "IT Support / Operations": [
                "Computer fundamentals मजबूत करो",
                "Networking basics सीखो",
                "Windows/Linux basics समझो",
                "Hardware-software troubleshooting सीखो",
                "Ticketing/support workflow समझो",
                "Basic cloud tools समझो",
                "Communication skill improve करो",
                "Support roles apply करो"
            ]
        }

        return roadmap_map.get(career, [
            "Basic programming सीखो",
            "Projects बनाओ",
            "Internship ढूँढो",
            "Skills improve करो"
        ])

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

        return {
            "predicted_career": str(predicted_career),
            "predicted_salary": predicted_salary,
            "recommendation": recommendation,
            "roadmap": roadmap
        }


ml_service = MLService()