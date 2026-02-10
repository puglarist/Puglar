import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.165.0/build/three.module.js";
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.13.0/firebase-app.js";
import {
  getFirestore,
  collection,
  doc,
  setDoc,
  deleteDoc,
  onSnapshot,
  serverTimestamp
} from "https://www.gstatic.com/firebasejs/10.13.0/firebase-firestore.js";
import { firebaseWebConfig, worldConfig } from "./firebase-config.js";

const canvas = document.getElementById("world");
const joinBtn = document.getElementById("joinBtn");
const statusEl = document.getElementById("status");
const playerList = document.getElementById("playerList");
const displayNameInput = document.getElementById("displayName");

let me = null;
let db = null;
let playersUnsub = null;
const cubesByPlayer = new Map();

const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
const scene = new THREE.Scene();
scene.background = new THREE.Color("#04070d");

const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 100);
camera.position.set(0, 7, 10);
camera.lookAt(0, 0, 0);

const light = new THREE.DirectionalLight("#8dc3ff", 1.25);
light.position.set(7, 12, 5);
scene.add(light);
scene.add(new THREE.AmbientLight("#7ca7ff", 0.35));

const grid = new THREE.GridHelper(30, 30, "#4ef7ff", "#17365a");
scene.add(grid);

function resize() {
  const parent = canvas.parentElement;
  const width = parent.clientWidth;
  const height = parent.clientHeight;
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}
window.addEventListener("resize", resize);
resize();

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
animate();

function upsertAvatar(player) {
  if (!cubesByPlayer.has(player.id)) {
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshStandardMaterial({ color: new THREE.Color(player.color) });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
    cubesByPlayer.set(player.id, cube);
  }

  const mesh = cubesByPlayer.get(player.id);
  mesh.position.set(player.x, 0.5, player.z);
}

function removeAvatar(id) {
  const mesh = cubesByPlayer.get(id);
  if (!mesh) {
    return;
  }
  scene.remove(mesh);
  mesh.geometry.dispose();
  mesh.material.dispose();
  cubesByPlayer.delete(id);
}

function setStatus(message) {
  statusEl.textContent = message;
}

function isFirebaseConfigured() {
  return firebaseWebConfig.apiKey && firebaseWebConfig.apiKey !== "REPLACE_ME";
}

async function joinWorld() {
  if (!isFirebaseConfigured()) {
    setStatus("Set Firebase config first");
    return;
  }

  if (!db) {
    const app = initializeApp(firebaseWebConfig);
    db = getFirestore(app);
  }

  const id = crypto.randomUUID();
  const name = (displayNameInput.value || "Explorer").trim().slice(0, 24);
  const color = `hsl(${Math.floor(Math.random() * 360)} 80% 60%)`;
  const x = Number((Math.random() * 16 - 8).toFixed(2));
  const z = Number((Math.random() * 16 - 8).toFixed(2));

  me = { id, name, color, x, z };

  const roomPlayers = collection(db, "worlds", worldConfig.roomId, "players");
  await setDoc(doc(roomPlayers, id), { ...me, joinedAt: serverTimestamp() });
  setStatus(`Connected as ${name}`);

  window.addEventListener("beforeunload", () => {
    deleteDoc(doc(roomPlayers, id));
  });

  if (playersUnsub) {
    playersUnsub();
  }

  playersUnsub = onSnapshot(roomPlayers, (snapshot) => {
    const seen = new Set();
    const listItems = [];

    snapshot.forEach((playerDoc) => {
      const player = playerDoc.data();
      seen.add(player.id);
      upsertAvatar(player);
      listItems.push(`<li>${player.name} (${player.id === me.id ? "you" : "online"})</li>`);
    });

    for (const idKey of cubesByPlayer.keys()) {
      if (!seen.has(idKey)) {
        removeAvatar(idKey);
      }
    }

    playerList.innerHTML = listItems.join("");
  });
}

joinBtn.addEventListener("click", () => {
  joinWorld().catch((error) => {
    console.error(error);
    setStatus("Connection failed - check console + Firestore rules");
  });
});

setStatus("Ready");
