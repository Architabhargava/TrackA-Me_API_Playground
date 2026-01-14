const BACKEND_URL = "https://tracka-me-api-playground.onrender.com";

/* ---------- AUTH ---------- */
function getAuthHeader() {
  const user = document.getElementById("authUser").value.trim();
  const pass = document.getElementById("authPass").value.trim();

  if (!user || !pass) {
    throw new Error("AuthMissing");
  }

  const token = btoa(`${user}:${pass}`);
  return {
    "Authorization": `Basic ${token}`
  };
}

/* ---------- CREATE PROFILE ---------- */
async function createProfile() {
  let authHeader;
  try {
    authHeader = getAuthHeader();
  } catch {
    alert("Please enter admin credentials before creating a profile.");
    return;
  }

  

  const body = {
    name: document.getElementById("name").value,
    email: email,
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

  const email = document.getElementById("email").value.trim();

  if (!email) {
    alert("Email is required and must be unique");
    return;
  }

  try {
    const res = await fetch(`${BACKEND_URL}/profile`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeader
      },
      body: JSON.stringify(body)
    });

   

    if (res.status === 401) {
      alert("Unauthorized: please check username and password");
      return;
    }

    if (res.status === 429) {
      alert("Rate limit exceeded: please wait 1 minute and try again");
      return;
  }

    if (!res.ok) {
      alert("Server error while creating profile");
      return;
  }
    const data = await res.json();
    document.getElementById("createStatus").textContent =
      `Profile created successfully with ID: ${data.id}`;

  } catch (err) {
    alert("Unexpected error while creating profile");
  }
}

/* ---------- UPDATE PROFILE ---------- */
async function updateProfile() {
  let authHeader;
  try {
    authHeader = getAuthHeader();
  } catch {
    alert("Please enter admin credentials before updating.");
    return;
  }

  const id = parseInt(document.getElementById("profileId").value, 10);
  if (isNaN(id)) {
    alert("Invalid Profile ID");
    return;
  }

  let body;
  try {
    body = JSON.parse(document.getElementById("profileJson").value);
  } catch {
    alert("Invalid JSON in edit box");
    return;
  }

  const res = await fetch(`${BACKEND_URL}/profile/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...authHeader
    },
    body: JSON.stringify(body)
  });

  if (res.status === 401) {
    alert("Unauthorized: Invalid credentials");
    return;
  }

  if (!res.ok) {
    alert("Update failed");
    return;
  }

  alert("Profile updated successfully");
}

/* ---------- PUBLIC READ OPS ---------- */
async function loadAllProfiles() {
  const res = await fetch(`${BACKEND_URL}/profiles`);
  const data = await res.json();
  document.getElementById("profilesOutput").textContent =
    JSON.stringify(data, null, 2);
}

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

async function searchSkill() {
  const skill = document.getElementById("skillInput").value;
  const res = await fetch(
    `${BACKEND_URL}/profiles/search?skill=${skill}`
  );
  const data = await res.json();
  document.getElementById("searchResult").textContent =
    JSON.stringify(data, null, 2);
}
