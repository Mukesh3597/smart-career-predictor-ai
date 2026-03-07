#uvicorn app.main:app --reload
import os
import numpy as np
import pandas as pd


def generate_student_career_data(n_rows: int = 1500, out_path: str = "data/student_career.csv"):
    np.random.seed(42)

    interests = ["ai", "web", "security", "data", "cloud", "govt", "mobile"]
    cities = [
        "Delhi", "Lucknow", "Noida", "Bangalore", "Pune",
        "Hyderabad", "Jaipur", "Bhopal", "Patna", "Kolkata", "Bijnor"
    ]
    skills_pool = ["python", "sql", "java", "c++", "html", "css", "js", "ml", "dl", "excel", "linux", "aws", "git"]

    city_multiplier = {
        "Bangalore": 1.30,
        "Hyderabad": 1.25,
        "Pune": 1.20,
        "Noida": 1.15,
        "Delhi": 1.15,
        "Kolkata": 1.00,
        "Lucknow": 0.95,
        "Jaipur": 0.92,
        "Bhopal": 0.88,
        "Patna": 0.85,
        "Bijnor": 0.70
    }

    rows = []

    for _ in range(n_rows):
        tenth = np.clip(np.random.normal(78, 12), 35, 99)
        twelfth = np.clip(tenth + np.random.normal(0, 8), 35, 99)
        grad = np.clip((tenth * 0.35 + twelfth * 0.35) + np.random.normal(10, 8), 35, 99)

        base_skill_count = int(np.clip(np.random.normal(3 + (grad - 60) / 20, 2), 0, 10))
        skill_count = base_skill_count

        picked_skills = list(np.random.choice(skills_pool, size=min(skill_count, len(skills_pool)), replace=False))
        skills = ",".join(picked_skills)

        interest = np.random.choice(interests)
        city = np.random.choice(cities)

        avg = (tenth + twelfth + grad) / 3.0

        # Career logic
        if ("ml" in picked_skills or "dl" in picked_skills or interest == "ai") and avg >= 72:
            career = "AI / Data Science"
        elif (("aws" in picked_skills or "linux" in picked_skills) and interest == "cloud") and avg >= 65:
            career = "Cloud / DevOps"
        elif (interest == "security" or "linux" in picked_skills) and avg >= 60 and np.random.rand() < 0.35:
            career = "Cyber Security"
        elif (interest == "data" or "excel" in picked_skills or "sql" in picked_skills) and avg >= 55 and np.random.rand() < 0.45:
            career = "Data Analyst"
        elif (interest == "web" or "html" in picked_skills or "js" in picked_skills) and avg >= 55 and np.random.rand() < 0.40:
            career = "Web Development"
        elif avg >= 58:
            career = "Software Development"
        else:
            career = "IT Support / Operations"

        base_salary_map = {
            "AI / Data Science": 7.5,
            "Software Development": 5.5,
            "Cyber Security": 6.0,
            "Data Analyst": 4.5,
            "Cloud / DevOps": 6.5,
            "Web Development": 4.8,
            "IT Support / Operations": 3.0
        }

        base = base_salary_map[career]
        marks_boost = (avg - 60) * 0.12
        skill_boost = skill_count * 0.25
        noise = np.random.normal(0, 0.8)

        salary = base + marks_boost + skill_boost + noise
        salary = salary * city_multiplier.get(city, 1.0)
        salary = float(np.clip(salary, 2.0, 35.0))

        rows.append({
            "tenth_pct": round(float(tenth), 2),
            "twelfth_pct": round(float(twelfth), 2),
            "graduation_pct": round(float(grad), 2),
            "skill_count": int(skill_count),
            "skills": skills,
            "interest": interest,
            "city": city,
            "career": career,
            "salary": round(salary, 2)
        })

    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"✅ Dataset generated: {out_path}")
    print(df.head(5))


if __name__ == "__main__":
    generate_student_career_data()