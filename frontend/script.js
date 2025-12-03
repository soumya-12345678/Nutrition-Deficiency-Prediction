const form = document.getElementById("predictForm");
const btn = document.querySelector(".btn");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(form);

  // Get raw values from selects (which are already numbers in string format like "0", "1")
  const genderVal = formData.get("gender");
  const dietVal = formData.get("diet_type");
  const sunlightVal = formData.get("sunlight");

  // Get the display text for the summary page (e.g., "Male", "Vegetarian")
  const genderEl = document.getElementById("gender");
  const dietEl = document.getElementById("diet_type");
  const sunlightEl = document.getElementById("sunlight");
  
  const genderText = genderEl.options[genderEl.selectedIndex].text;
  const dietText = dietEl.options[dietEl.selectedIndex].text;
  const sunlightText = sunlightEl.options[sunlightEl.selectedIndex].text;

  const payload = {
    age: Number(formData.get("age")),
    gender: Number(genderVal),
    height: Number(formData.get("height")),
    weight: Number(formData.get("weight")),
    diet_type: Number(dietVal),
    sunlight: Number(sunlightVal),
    fatigue: formData.get("fatigue") ? 1 : 0,
    hair_fall: formData.get("hair_fall") ? 1 : 0,
    pale_skin: formData.get("pale_skin") ? 1 : 0,
    bone_pain: formData.get("bone_pain") ? 1 : 0,
    cracked_lips: formData.get("cracked_lips") ? 1 : 0,
  };

  // store details for summary
  localStorage.setItem("ndp_age", formData.get("age"));
  localStorage.setItem("ndp_gender", genderText);
  localStorage.setItem("ndp_height", formData.get("height"));
  localStorage.setItem("ndp_weight", formData.get("weight"));
  localStorage.setItem("ndp_diet", dietText);
  localStorage.setItem("ndp_sunlight", sunlightText);

  const symptoms = [];
  if (payload.fatigue) symptoms.push("Fatigue");
  if (payload.hair_fall) symptoms.push("Hair Fall");
  if (payload.pale_skin) symptoms.push("Pale Skin");
  if (payload.bone_pain) symptoms.push("Bone / Joint Pain");
  if (payload.cracked_lips) symptoms.push("Cracked Lips / Mouth Sores");
  localStorage.setItem("ndp_symptoms", symptoms.join(", "));

  btn.classList.add("loading");
  btn.disabled = true;

  try {
    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!data.success) {
      throw new Error(data.error || "Unknown error");
    }

    localStorage.setItem("ndp_prediction_label", data.label);
    localStorage.setItem("ndp_prediction_measures", data.measures);
    localStorage.setItem(
      "ndp_thank_line",
      "Thank you for using this system. Small, consistent changes in your plate today become big changes in your health tomorrow – keep your diet balanced and your body active."
    );

    window.location.href = "result.html";
  } catch (err) {
    console.error(err);
    alert("Something went wrong. Please check if the backend server is running.");
  } finally {
    btn.classList.remove("loading");
    btn.disabled = false;
  }
});