function loadResult() {
  const label = localStorage.getItem("ndp_prediction_label");
  const measures = localStorage.getItem("ndp_prediction_measures");
  const thankLine = localStorage.getItem("ndp_thank_line");

  const labelEl = document.getElementById("resLabel");
  const measuresEl = document.getElementById("resMeasures");
  const thankEl = document.getElementById("thankLine");

  if (label && measures) {
    labelEl.textContent = "Prediction: " + label;
    measuresEl.textContent = "Suggested Measures: " + measures;
  } else {
    labelEl.textContent = "Prediction: —";
    measuresEl.textContent =
      "Suggested Measures: Data not available. Please go back and try again.";
  }

  thankEl.textContent =
    thankLine ||
    "Thank you for using this system. Maintain a simple, balanced diet and listen to your body every day.";

  // Summary details
  document.getElementById("sumAge").textContent =
    "Age: " + (localStorage.getItem("ndp_age") || "—");

  document.getElementById("sumGender").textContent =
    "Gender: " + (localStorage.getItem("ndp_gender") || "—");

  document.getElementById("sumHeight").textContent =
    "Height: " + (localStorage.getItem("ndp_height") || "—") + " cm";

  document.getElementById("sumWeight").textContent =
    "Weight: " + (localStorage.getItem("ndp_weight") || "—") + " kg";

  document.getElementById("sumDiet").textContent =
    "Diet Type: " + (localStorage.getItem("ndp_diet") || "—");

  document.getElementById("sumSunlight").textContent =
    "Daily Sunlight: " + (localStorage.getItem("ndp_sunlight") || "—");

  document.getElementById("sumSymptoms").textContent =
    "Symptoms: " + (localStorage.getItem("ndp_symptoms") || "None");
}

function goBack() {
  // Optional: clear prediction-specific data
  localStorage.removeItem("ndp_prediction_label");
  localStorage.removeItem("ndp_prediction_measures");
  localStorage.removeItem("ndp_thank_line");
  // Keep the user input summary if you want, or clear them too:
  // localStorage.removeItem("ndp_age");
  // localStorage.removeItem("ndp_gender");
  // localStorage.removeItem("ndp_height");
  // localStorage.removeItem("ndp_weight");
  // localStorage.removeItem("ndp_diet");
  // localStorage.removeItem("ndp_sunlight");
  // localStorage.removeItem("ndp_symptoms");

  window.location.href = "index.html";
}

window.addEventListener("DOMContentLoaded", loadResult);
