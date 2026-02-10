const statusEl = document.getElementById("status");
const xrButton = document.getElementById("xr-button");
const scene = document.querySelector("a-scene");

const destinations = [
  { x: -5, y: 1.6, z: -8 },
  { x: 0, y: 1.6, z: -16 },
  { x: 13, y: 1.6, z: -12 }
];

function setStatus(message) {
  statusEl.textContent = message;
}

function enterVR() {
  if (!scene?.is("vr-mode")) {
    scene.enterVR();
  }
}

function supportsXR() {
  if (!navigator.xr) {
    setStatus("WebXR not detected. The world still works in desktop mode.");
    return;
  }

  navigator.xr
    .isSessionSupported("immersive-vr")
    .then((supported) => {
      if (supported) {
        setStatus("WebXR ready. Use Enter VR to launch on Meta Quest.");
      } else {
        setStatus("Immersive VR unavailable in this browser; desktop mode is still active.");
      }
    })
    .catch(() => setStatus("Could not verify WebXR support. Try latest Meta Quest Browser."));
}

function setupTeleports() {
  const rig = document.getElementById("rig");
  document.querySelectorAll(".teleport").forEach((pad, index) => {
    pad.addEventListener("click", () => {
      const destination = destinations[index] ?? destinations[0];
      rig.setAttribute("position", destination);
      setStatus(`Teleported to ${index === 0 ? "Spawn" : index === 1 ? "Training Dome" : "Doctrine Library"}.`);
    });
  });
}

function setupDocLinks() {
  document.querySelectorAll(".doc-link").forEach((item) => {
    item.addEventListener("click", () => {
      const url = item.getAttribute("data-url");
      if (!url) return;
      window.open(url, "_blank", "noopener,noreferrer");
      setStatus(`Opened ${url} in a new tab.`);
    });
  });
}

xrButton.addEventListener("click", enterVR);
scene.addEventListener("loaded", () => {
  supportsXR();
  setupTeleports();
  setupDocLinks();
});
