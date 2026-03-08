import zipfile
import os

# Define file contents
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Enhanced BMI Calculator</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <div class="container">
    <header>
      <h1>BMI Calculator</h1>
      <button id="theme-toggle" onclick="toggleTheme()">🌙</button>
    </header>

    <form id="bmi-form">
      <label for="weight">Weight (kg):</label>
      <input type="number" id="weight" placeholder="e.g. 70" required />

      <label for="height">Height (cm):</label>
      <input type="number" id="height" placeholder="e.g. 170" required />

      <button type="submit">Calculate BMI</button>
    </form>

    <div id="result" class="result"></div>

    <div class="chart">
      <h3>BMI Categories</h3>
      <ul>
        <li><strong>&lt; 18.5:</strong> Underweight</li>
        <li><strong>18.5 – 24.9:</strong> Normal weight</li>
        <li><strong>25 – 29.9:</strong> Overweight</li>
        <li><strong>30+:</strong> Obese</li>
      </ul>
    </div>

    <div id="history">
      <h3>BMI History</h3>
      <ul id="history-list"></ul>
    </div>
  </div>

  <script src="script.js"></script>
</body>
</html>
"""

style_css = """
* {
  box-sizing: border-box;
  font-family: Arial, sans-serif;
}

body {
  background-color: #f2f2f2;
  color: #333;
  margin: 0;
  padding: 20px;
  transition: background-color 0.3s, color 0.3s;
}

.container {
  max-width: 500px;
  margin: auto;
  background: #fff;
  padding: 20px 30px;
  border-radius: 12px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h1 {
  margin: 0;
  font-size: 1.8em;
}

#theme-toggle {
  font-size: 1.2em;
  background: transparent;
  border: none;
  cursor: pointer;
}

form {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
}

label {
  margin-top: 10px;
}

input {
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

button {
  margin-top: 15px;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.result {
  margin-top: 20px;
  padding: 10px;
  background-color: #e7f3ff;
  border-left: 5px solid #007bff;
  border-radius: 6px;
}

.chart {
  margin-top: 20px;
}

.chart ul {
  padding-left: 20px;
}

#history {
  margin-top: 20px;
}

#history-list li {
  margin-bottom: 5px;
}

/* Dark Mode */
.dark {
  background-color: #121212;
  color: #f1f1f1;
}

.dark .container {
  background-color: #1e1e1e;
}

.dark input,
.dark button {
  background-color: #333;
  color: white;
  border: 1px solid #555;
}

.dark .result {
  background-color: #2c3e50;
  border-left: 5px solid #1abc9c;
}
"""

script_js = """
const form = document.getElementById("bmi-form");
const weightInput = document.getElementById("weight");
const heightInput = document.getElementById("height");
const resultDiv = document.getElementById("result");
const historyList = document.getElementById("history-list");

let history = JSON.parse(localStorage.getItem("bmiHistory")) || [];
renderHistory();

form.addEventListener("submit", function (e) {
  e.preventDefault();

  const weight = parseFloat(weightInput.value);
  const heightCm = parseFloat(heightInput.value);
  const heightM = heightCm / 100;

  if (weight > 0 && heightM > 0) {
    const bmi = weight / (heightM * heightM);
    let category = "";
    let tips = "";

    if (bmi < 18.5) {
      category = "Underweight";
      tips = "Consider a nutritious diet with more calories.";
    } else if (bmi < 24.9) {
      category = "Normal weight";
      tips = "Great! Keep maintaining your healthy habits.";
    } else if (bmi < 29.9) {
      category = "Overweight";
      tips = "Exercise regularly and watch your portion sizes.";
    } else {
      category = "Obese";
      tips = "Consult a doctor for a personalized health plan.";
    }

    resultDiv.innerHTML = `
      <strong>BMI:</strong> ${bmi.toFixed(2)}<br>
      <strong>Category:</strong> ${category}<br>
      <em>${tips}</em>
    `;

    updateHistory(bmi, category);
  } else {
    resultDiv.textContent = "Please enter valid inputs.";
  }
});

function updateHistory(bmi, category) {
  const entry = {
    date: new Date().toLocaleDateString(),
    bmi: bmi.toFixed(2),
    category,
  };
  history.unshift(entry);
  if (history.length > 5) history.pop();
  localStorage.setItem("bmiHistory", JSON.stringify(history));
  renderHistory();
}

function renderHistory() {
  historyList.innerHTML = "";
  history.forEach((entry) => {
    const li = document.createElement("li");
    li.textContent = `${entry.date}: BMI ${entry.bmi} (${entry.category})`;
    historyList.appendChild(li);
  });
}

function toggleTheme() {
  document.body.classList.toggle("dark");
  const icon = document.getElementById("theme-toggle");
  icon.textContent = document.body.classList.contains("dark") ? "☀️" : "🌙";
}
"""

# Save files and create ZIP
zip_path = "/mnt/data/bmi_calculator.zip"
with zipfile.ZipFile(zip_path, 'w') as zipf:
    zipf.writestr("index.html", index_html)
    zipf.writestr("style.css", style_css)
    zipf.writestr("script.js", script_js)

zip_path  # Return the path to the ZIP file for download

