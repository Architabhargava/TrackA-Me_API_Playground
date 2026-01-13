const BACKEND_URL = "https://tracka-me-api-playground.onrender.com";



async function loadProfile() {
  const id = document.getElementById("profileId").value;

  const res = await fetch(`${BACKEND_URL}/profile/${id}/edit`);
  const data = await res.json();

  document.getElementById("profileJson").value =
    JSON.stringify(data, null, 2);

  document.getElementById("editSection").style.display = "block";
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
