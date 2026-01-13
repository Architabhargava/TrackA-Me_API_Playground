const BACKEND_URL = "https://tracka-me-api-playground.onrender.com";



async function loadProfile() {
  const idRaw = document.getElementById("profileId").value;

  // 🔒 sanitize input
  const id = parseInt(idRaw, 10);

  if (isNaN(id)) {
    alert("Please enter a valid numeric Profile ID");
    return;
  }

  try {
    const res = await fetch(`${BACKEND_URL}/profile/${id}/edit`);

    if (!res.ok) {
      throw new Error("Profile not found");
    }

    const data = await res.json();

    document.getElementById("profileJson").value =
      JSON.stringify(data, null, 2);

  } catch (err) {
    alert("Failed to load profile. Check Profile ID.");
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
