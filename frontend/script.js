const BACKEND_URL = "https://tracka-me-api-playground.onrender.com";

/* ---------------- CREATE PROFILE ---------------- */
async function createProfile() {
  try {
    const body = {
      name: document.getElementById("name").value,
      email: document.getElementById("email").value,
      education: document.getElementById("education").value,
      work: document.getElementById("work").value,
      links: document.getElementById("links").value,
      skills: document.getElementById("skills").value
        .split(",")
        .map(s => s.trim())
        .filter(Boolean),
      projects: [
        {
          title: document.getElementById("projectTitle").value,
          description: document.getElementById("projectDescription").value,
          tech_stack: document.getElementById("projectTech").value
        }
      ]
    };

    const res = await fetch(`${BACKEND_URL}/profile`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    const data = await res.json();

    document.getElementById("createStatus").textContent =
      `Profile created successfully with ID: ${data.id}`;
  } catch (err) {
    document.getElementById("createStatus").textContent =
      "Failed to create profile";
  }
}

/* ---------------- SHOW ALL PROFILES ---------------- */
async function loadAllProfiles() {
  const output = document.getElementById("profilesOutput");
  output.textContent = "Loading profiles...";

  try {
    const res = await fetch(`${BACKEND_URL}/profiles`);
    const data = await res.json();

    if (data.length === 0) {
      output.textContent = "No profiles found.";
      return;
    }

    output.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    output.textContent = "Failed to load profiles.";
  }
}

/* ---------------- LOAD PROFILE FOR EDIT ---------------- */
async function loadProfile() {
  const id = parseInt(document.getElementById("profileId").value, 10);

  if (isNaN(id)) {
    alert("Please enter a valid numeric Profile ID");
    return;
  }

  try {
    const res = await fetch(`${BACKEND_URL}/profile/${id}/edit`);
    if (!res.ok) throw new Error();

    const data = await res.json();

    document.getElementById("profileJson").value =
      JSON.stringify(data, null, 2);
  } catch {
    alert("Profile not found");
  }
}

/* ---------------- UPDATE PROFILE ---------------- */
async function updateProfile() {
  try {
    const id = parseInt(document.getElementById("profileId").value, 10);
    const body = JSON.parse(
      document.getElementById("profileJson").value
    );

    await fetch(`${BACKEND_URL}/profile/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    alert("Profile updated successfully");
  } catch {
    alert("Failed to update profile");
  }
}

/* ---------------- SEARCH BY SKILL ---------------- */
async function searchSkill() {
  const skill = document.getElementById("skillInput").value;

  const res = await fetch(
    `${BACKEND_URL}/profiles/search?skill=${skill}`
  );
  const data = await res.json();

  document.getElementById("searchResult").textContent =
    JSON.stringify(data, null, 2);
}
