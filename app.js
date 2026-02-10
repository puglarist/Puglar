(function () {
  const params = new URLSearchParams(window.location.search);
  const room = sanitize(params.get("room") || "default");

  const roomName = document.getElementById("room-name");
  const connectionState = document.getElementById("connection-state");
  const shareButton = document.getElementById("share-room");
  const shareStatus = document.getElementById("share-status");
  const landmarks = document.getElementById("landmarks");

  roomName.textContent = room;
  connectionState.textContent = "(shared room link ready)";
  seedLandmarks(room, landmarks);

  shareButton.addEventListener("click", async () => {
    const shareUrl = new URL(window.location.href);
    shareUrl.searchParams.set("room", room);

    try {
      await navigator.clipboard.writeText(shareUrl.toString());
      shareStatus.textContent = "Room link copied. Open it on your Quest Browser to join this world.";
    } catch (error) {
      shareStatus.textContent = "Copy failed. Use this URL: " + shareUrl.toString();
    }
  });

  function sanitize(value) {
    return value.toLowerCase().replace(/[^a-z0-9-]/g, "-").slice(0, 24) || "default";
  }

  function seedLandmarks(seed, parent) {
    const hue = hash(seed) % 360;
    const colorBase = `hsl(${hue} 80% 58%)`;
    const count = 12;

    for (let i = 0; i < count; i += 1) {
      const angle = (i / count) * Math.PI * 2;
      const radius = 12 + (i % 3) * 6;
      const x = Math.cos(angle) * radius;
      const z = Math.sin(angle) * radius;
      const y = 1.5 + ((i * 7) % 6) * 0.35;

      const tower = document.createElement("a-box");
      tower.setAttribute("position", `${x.toFixed(2)} ${y.toFixed(2)} ${z.toFixed(2)}`);
      tower.setAttribute("depth", "1.8");
      tower.setAttribute("width", "1.8");
      tower.setAttribute("height", (1.8 + (i % 5) * 0.75).toString());
      tower.setAttribute("color", colorBase);
      tower.setAttribute("material", "metalness: 0.15; roughness: 0.55");

      const label = document.createElement("a-text");
      label.setAttribute("value", `${seed}-node-${i + 1}`);
      label.setAttribute("position", `${x.toFixed(2)} ${(y + 1.9).toFixed(2)} ${z.toFixed(2)}`);
      label.setAttribute("align", "center");
      label.setAttribute("color", "#ffffff");
      label.setAttribute("width", "10");

      parent.appendChild(tower);
      parent.appendChild(label);
    }
  }

  function hash(input) {
    let h = 2166136261;
    for (let i = 0; i < input.length; i += 1) {
      h ^= input.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return Math.abs(h);
  }
})();
