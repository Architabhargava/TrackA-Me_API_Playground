const BACKEND_URL = "https://tracka-me-api-playground.onrender.com";



async function loadAllProfiles() {
  const output = document.getElementById("profilesOutput");
  output.textContent = "Loading profiles...";

  try {
    const res = await fetch(`${BACKEND_URL}/profiles`);
    const data = await res.json();

    if (!data || data.length === 0) {
      output.textContent = "No profiles found.";
      return;
    }

    output.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    output.textContent = "Failed to load profiles.";
  }
}


async function updateProfile() {
  const id = document.getElementById("profileId").value;
  const body = JSON.parse(
    document.getElementById("profileJson").value
  );

  await fetch(`${BACKEND_URL}/profile/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });

  alert("Profile updated successfully");
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
