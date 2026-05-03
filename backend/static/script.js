function getVal(id) {
  return document.getElementById(id).value.trim();
}

function fillSample() {
  document.getElementById("name").value = "Mukesh";
  document.getElementById("email").value = "mukeshk07341@gmail.com";
  document.getElementById("tenth").value = 80;
  document.getElementById("twelfth").value = 84;
  document.getElementById("grad").value = 54;
  document.getElementById("skills").value = "python";
  document.getElementById("interest").value = "ai";
  document.getElementById("city").value = "Bijnor";
  document.getElementById("stream").value = "BCA";
}

function clearForm() {
  ["name", "email", "tenth", "twelfth", "grad", "skills", "interest", "city", "stream"].forEach(id => {
    document.getElementById(id).value = "";
  });

  const resBox = document.getElementById("result");
  resBox.classList.add("hide");
  resBox.innerHTML = "";
}

async function predictCareer() {
  const btn = document.getElementById("btnPredict");
  btn.disabled = true;
  btn.textContent = "Predicting...";

  const full_name = getVal("name");
  const email = getVal("email");
  const tenth_pct = parseFloat(getVal("tenth"));
  const twelfth_pct = parseFloat(getVal("twelfth"));
  const graduation_pct = parseFloat(getVal("grad"));
  const skillsRaw = getVal("skills");

  const skills = skillsRaw
    ? skillsRaw.split(",").map(s => s.trim()).filter(Boolean)
    : [];

  const interest = getVal("interest");
  const city = getVal("city");

  const payload = { tenth_pct, twelfth_pct, graduation_pct, skills, interest, city };
  if (full_name) payload.full_name = full_name;
  if (email) payload.email = email;

  const resBox = document.getElementById("result");
  resBox.classList.remove("hide");
  resBox.innerHTML = "⏳ Please wait... predicting your career";

  try {
    const API_URL = "https://smart-career-predictor-ai.onrender.com";

    const res = await fetch(`${API_URL}/predict/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      resBox.style.background = "rgba(239,68,68,.12)";
      resBox.innerHTML = "❌ Error: " + JSON.stringify(data);
      return;
    }

    // Roadmap
    const roadmapHtml = (data.roadmap || [])
      .map((step, index) => `<li><b>Step ${index + 1}:</b> ${step}</li>`)
      .join("");

    // Companies
    const companiesHtml = (data.companies || [])
      .map(c => `<li>${c}</li>`)
      .join("");

    // Jobs
    const jobsHtml = (data.job_links || [])
      .map(link => `<li><a href="${link}" target="_blank">${link}</a></li>`)
      .join("");

    // Internships
    const internshipsHtml = (data.internships || [])
      .map(link => `<li><a href="${link}" target="_blank">${link}</a></li>`)
      .join("");

    // Courses
    const coursesHtml = (data.courses || [])
      .map(link => `<li><a href="${link}" target="_blank">${link}</a></li>`)
      .join("");

    resBox.style.background = "rgba(34,197,94,.10)";
    resBox.innerHTML = `
      <div style="line-height:1.8">

        <div><b>✅ Job Title:</b> ${data.predicted_career}</div>
        <div><b>💰 Expected Salary (LPA):</b> ${data.predicted_salary}</div>

        <div style="margin-top:10px;"><b>🧠 Recommendation:</b></div>
        <div>${data.recommendation || "No recommendation available"}</div>

        <div style="margin-top:12px;"><b>🗺 Roadmap:</b></div>
        <ol style="padding-left:20px;">
          ${roadmapHtml || "<li>No roadmap available</li>"}
        </ol>

        <div style="margin-top:12px;"><b>🏢 Companies:</b></div>
        <ul>${companiesHtml}</ul>

        <div style="margin-top:12px;"><b>💼 Job Links:</b></div>
        <ul>${jobsHtml}</ul>

        <div style="margin-top:12px;"><b>🎯 Internships:</b></div>
        <ul>${internshipsHtml}</ul>

        <div style="margin-top:12px;"><b>📚 Courses:</b></div>
        <ul>${coursesHtml}</ul>

        <div style="margin-top:10px;">
          <small>Prediction ID: ${data.saved_prediction_id}</small>
        </div>

      </div>
    `;
  } catch (e) {
    resBox.style.background = "rgba(239,68,68,.12)";
    resBox.innerHTML = "❌ Backend connect नहीं हो पाया। Server चल रहा है क्या?";
  } finally {
    btn.disabled = false;
    btn.textContent = "Predict";
  }
}