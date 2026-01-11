async function createProfile() {
  const body = JSON.parse(
    document.getElementById("createJson").value
  );

  const res = await fetch(`${BACKEND_URL}/profile`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });

  const data = await res.json();
  alert("Profile created with ID: " + data.id);
}

async function loadAllProfiles() {
  const res = await fetch(`${BACKEND_URL}/profiles`);
  const data = await res.json();

  document.getElementById("profilesOutput").textContent =
    JSON.stringify(data, null, 2);
}
