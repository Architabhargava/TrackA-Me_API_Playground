const BACKEND_URL = "https://tracka-me-api-playground.onrender.com";

/* ---------- AUTH HEADER ---------- */
function getAuthHeader() {
  const user = document.getElementById("authUser").value;
  const pass = document.getElementById("authPass").value;

  if (!user || !pass) return {};

  const token = btoa(`${user}:${pass}`);
  return {
    "Authorization": `Basic ${token}`
  };
}

/* ---------- CREATE PROFILE ---------- */
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
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeader()
      },
      body: JSON.stringify(body)
    });

    if (!res.ok) {
      alert("Unauthorized or rate-limited");
      return;
    }

    const data = await res.json();
    document.getElementById("createStatus").textContent =
      `Profile created with ID: ${data.id}`;

  } catch {
    alert("Create failed");
  }
}

/* ---------- LOAD ALL PROFILES (PUBLIC) ---------- */
async function loadAllProfiles() {
  const out = document.getElementById("profilesOutput");
  out.textContent = "Loading...";

  const res = await fetch(`${BACKEND_URL}/profiles`);
  const data = await res.json();

  out.textContent = JSON.stringify(data, null, 2);
}

/* ---------- LOAD PROFILE FOR EDIT ---------- */
async function loadProfile() {
  const id = parseInt(document.getElementById("profileId").value, 10);
  if (isNaN(id)) {
    alert("Invalid ID");
    return;
  }

  const res = await fetch(`${BACKEND_URL}/profile/${id}/edit`);
  if (!res.ok) {
    alert("Profile not found");
    return;
  }

  const data = await res.json();
  document.getElementById("profileJson").value =
    JSON.stringify(data, null, 2);
}

/* ---------- UPDATE PROFILE ---------- */
async function updateProfile() {
  try {
    const id = parseInt(document.getElementById("profileId").value, 10);
    const body = JSON.parse(
      document.getElementById("profileJson").value
    );

    const res = await fetch(`${BACKEND_URL}/profile/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeader()
      },
      body: JSON.stringify(body)
    });

    if (!res.ok) {
      alert("Unauthorized or failed update");
      return;
    }

    alert("Profile updated successfully");
  } catch {
    alert("Update failed");
  }
}

/* ---------- SEARCH (PUBLIC) ---------- */
async function searchSkill() {
  const skill = document.getElementById("skillInput").value;

  const res = await fetch(
    `${BACKEND_URL}/profiles/search?skill=${skill}`
  );

  const data = await res.json();
  document.getElementById("searchResult").textContent =
    JSON.stringify(data, null, 2);
}
