const form = document.getElementById("predictForm");
const btn = document.querySelector(".btn");

function mapGender(value) {
  if (!value) return 0;
  const v = value.toString().trim().toLowerCase();
  if (v.startsWith("m")) return 0;
  if (v.startsWith("f")) return 1;
  return 0;
}

function mapDiet(value) {
  if (!value) return 0;
  const v = value.toString().trim().toLowerCase();
  if (v.includes("non")) return 1;
  if (v.startsWith("n")) return 1;
  if (v.startsWith("v")) return 0;
  return 0;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(form);

  const genderText = formData.get("gender_text");
  const dietText = formData.get("diet_type_text");

  const payload = {
    age: Number(formData.get("age")),
    gender: mapGender(genderText),
    height: Number(formData.get("height")),
    weight: Number(formData.get("weight")),
    diet_type: mapDiet(dietText),
    sunlight: Number(formData.get("sunlight")),
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
  localStorage.setItem("ndp_sunlight", formData.get("sunlight"));

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
