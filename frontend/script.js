const BACKEND_URL = "http://127.0.0.1:8000";

/* ---------- DEFAULT CREATE JSON ---------- */
document.getElementById("createJson").value = JSON.stringify({
  name: "Your Name",
  email: "your@email.com",
  education: "",
  work: "",
  links: "",
  skills: ["AI", "Python"],
  projects: []
}, null, 2);

/* ---------- CREATE PROFILE ---------- */
async function createProfile() {
  try {
    const body = JSON.parse(
      document.getElementById("createJson").value
    );

    const res = await fetch(`${BACKEND_URL}/profile`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    const data = await res.json();
    document.getElementById("createStatus").textContent =
      "Profile created with ID: " + data.id;
  } catch (err) {
    document.getElementById("createStatus").textContent =
      "Invalid JSON or server error";
  }
}

/* ---------- LOAD ALL PROFILES ---------- */
async function loadAllProfiles() {
  const res = await fetch(`${BACKEND_URL}/profiles`);
  const data = await res.json();

  document.getElementById("profilesOutput").textContent =
    JSON.stringify(data, null, 2);
}

/* ---------- LOAD PROFILE FOR EDIT ---------- */
async function loadProfile() {
  const id = document.getElementById("profileId").value;
  if (!id) return;

  const res = await fetch(`${BACKEND_URL}/profile/${id}/edit`);
  const data = await res.json();

  document.getElementById("profileJson").value =
    JSON.stringify(data, null, 2);
}

/* ---------- UPDATE PROFILE ---------- */
async function updateProfile() {
  try {
    const id = document.getElementById("profileId").value;
    const body = JSON.parse(
      document.getElementById("profileJson").value
    );

    await fetch(`${BACKEND_URL}/profile/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    document.getElementById("updateStatus").textContent =
      "Profile updated successfully";
  } catch (err) {
    document.getElementById("updateStatus").textContent =
      "Invalid JSON or update failed";
  }
}

/* ---------- SEARCH ---------- */
async function searchSkill() {
  const skill = document.getElementById("skillInput").value;
  const res = await fetch(
    `${BACKEND_URL}/profiles/search?skill=${skill}`
  );
  const data = await res.json();

  document.getElementById("searchResult").textContent =
    JSON.stringify(data, null, 2);
}
