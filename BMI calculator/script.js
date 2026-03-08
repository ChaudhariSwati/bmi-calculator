// DOM elements
const form = document.getElementById("bmi-form");
const weightInput = document.getElementById("weight");
const heightInput = document.getElementById("height");
const resultDiv = document.getElementById("result");
const historyList = document.getElementById("history-list");

// Load existing history
let history = JSON.parse(localStorage.getItem("bmiHistory")) || [];
renderHistory();

// Form Submit Handler
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

// Save BMI result in localStorage
function updateHistory(bmi, category) {
  const entry = {
    date: new Date().toLocaleDateString(),
    bmi: bmi.toFixed(2),
    category,
  };
  history.unshift(entry);
  if (history.length > 5) history.pop(); // limit to 5 entries
  localStorage.setItem("bmiHistory", JSON.stringify(history));
  renderHistory();
}

// Display saved history
function renderHistory() {
  historyList.innerHTML = "";
  history.forEach((entry) => {
    const li = document.createElement("li");
    li.textContent = `${entry.date}: BMI ${entry.bmi} (${entry.category})`;
    historyList.appendChild(li);
  });
}

// Toggle dark/light mode
function toggleTheme() {
  document.body.classList.toggle("dark");
  const icon = document.getElementById("theme-toggle");
  icon.textContent = document.body.classList.contains("dark") ? "☀️" : "🌙";
}
