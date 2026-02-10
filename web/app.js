const statusEl = document.getElementById("status");
const installBtn = document.getElementById("installBtn");

let deferredPrompt = null;

if ("serviceWorker" in navigator) {
  window.addEventListener("load", async () => {
    try {
      await navigator.serviceWorker.register("./sw.js");
      statusEl.textContent = "PWA ready: service worker registered.";
    } catch (error) {
      statusEl.textContent = `Service worker failed: ${error.message}`;
    }
  });
} else {
  statusEl.textContent = "PWA unavailable: service workers are not supported.";
}

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  deferredPrompt = event;
  installBtn.hidden = false;
});

installBtn.addEventListener("click", async () => {
  if (!deferredPrompt) return;

  deferredPrompt.prompt();
  await deferredPrompt.userChoice;
  deferredPrompt = null;
  installBtn.hidden = true;
});
