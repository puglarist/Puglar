import * as THREE from 'https://unpkg.com/three@0.164.1/build/three.module.js';
import { VRButton } from 'https://unpkg.com/three@0.164.1/examples/jsm/webxr/VRButton.js';

const statusEl = document.getElementById('status');
const enterButton = document.getElementById('enter-xr');

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x070b14);
scene.fog = new THREE.Fog(0x070b14, 5, 28);

const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.01, 200);
camera.position.set(0, 1.6, 2.2);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.xr.enabled = true;
document.body.appendChild(renderer.domElement);

const hemi = new THREE.HemisphereLight(0xa5f3fc, 0x172554, 1.3);
scene.add(hemi);

const dir = new THREE.DirectionalLight(0xffffff, 0.7);
dir.position.set(2, 4, 3);
scene.add(dir);

const grid = new THREE.GridHelper(20, 40, 0x334155, 0x1e293b);
grid.position.y = 0;
scene.add(grid);

const floor = new THREE.Mesh(
  new THREE.CircleGeometry(15, 64),
  new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.1, roughness: 0.9 })
);
floor.rotation.x = -Math.PI / 2;
floor.receiveShadow = true;
scene.add(floor);

const worldAnchor = new THREE.Group();
scene.add(worldAnchor);

for (let i = 0; i < 24; i += 1) {
  const pillar = new THREE.Mesh(
    new THREE.BoxGeometry(0.25, 0.25 + Math.random() * 1.6, 0.25),
    new THREE.MeshStandardMaterial({ color: new THREE.Color(`hsl(${180 + i * 6} 72% 57%)`) })
  );
  const a = (i / 24) * Math.PI * 2;
  const r = 2.8 + Math.random() * 2.4;
  pillar.position.set(Math.cos(a) * r, 0.4 + Math.random() * 0.7, Math.sin(a) * r);
  worldAnchor.add(pillar);
}

const jointGeometry = new THREE.SphereGeometry(0.012, 10, 10);
const leftMaterial = new THREE.MeshStandardMaterial({ color: 0x22d3ee, emissive: 0x083344, emissiveIntensity: 0.45 });
const rightMaterial = new THREE.MeshStandardMaterial({ color: 0xf472b6, emissive: 0x4a044e, emissiveIntensity: 0.45 });

const handMeshes = new Map();
const controllers = [renderer.xr.getController(0), renderer.xr.getController(1)];
controllers.forEach((ctrl) => scene.add(ctrl));

function buildJointMeshes(handedness) {
  const group = new THREE.Group();
  group.visible = false;
  const material = handedness === 'left' ? leftMaterial : rightMaterial;
  for (let i = 0; i < 25; i += 1) {
    const m = new THREE.Mesh(jointGeometry, material);
    m.visible = false;
    group.add(m);
  }
  scene.add(group);
  return group;
}

function setStatus(message) {
  statusEl.textContent = message;
}

async function initXRSupport() {
  if (!navigator.xr) {
    setStatus('WebXR unavailable. Use Meta Quest Browser over HTTPS/GitHub Pages.');
    enterButton.disabled = true;
    return;
  }

  const vrSupported = await navigator.xr.isSessionSupported('immersive-vr');
  if (!vrSupported) {
    setStatus('Immersive VR not supported on this device/browser.');
    enterButton.disabled = true;
    return;
  }

  setStatus('WebXR ready. Hand tracking will appear when your hands are detected.');

  const xrButton = VRButton.createButton(renderer, {
    requiredFeatures: ['local-floor', 'hand-tracking']
  });
  xrButton.style.display = 'none';
  document.body.appendChild(xrButton);

  enterButton.disabled = false;
  enterButton.addEventListener('click', () => xrButton.click());

  renderer.xr.addEventListener('sessionstart', () => {
    setStatus('XR session started. Move hands into view to track joints.');
  });

  renderer.xr.addEventListener('sessionend', () => {
    setStatus('XR session ended. Tap Enter VR to start again.');
    handMeshes.forEach((group) => {
      group.visible = false;
      group.children.forEach((jointMesh) => {
        jointMesh.visible = false;
      });
    });
  });
}

const tempMatrix = new THREE.Matrix4();

function updateHands(frame, referenceSpace) {
  const session = renderer.xr.getSession();
  if (!session || !frame || !referenceSpace) return;

  for (const inputSource of session.inputSources) {
    if (!inputSource.hand) continue;

    const handedness = inputSource.handedness || 'unknown';
    let group = handMeshes.get(handedness);
    if (!group) {
      group = buildJointMeshes(handedness);
      handMeshes.set(handedness, group);
    }

    group.visible = true;
    let jointIndex = 0;

    for (const jointSpace of inputSource.hand.values()) {
      const pose = frame.getJointPose(jointSpace, referenceSpace);
      const jointMesh = group.children[jointIndex];
      jointIndex += 1;
      if (!jointMesh) continue;

      if (!pose) {
        jointMesh.visible = false;
        continue;
      }

      tempMatrix.fromArray(pose.transform.matrix);
      jointMesh.matrix.copy(tempMatrix);
      jointMesh.matrix.decompose(jointMesh.position, jointMesh.quaternion, jointMesh.scale);
      const radius = Math.max(0.008, pose.radius || 0.01);
      jointMesh.scale.setScalar(radius * 1.8);
      jointMesh.visible = true;
    }

    for (; jointIndex < group.children.length; jointIndex += 1) {
      group.children[jointIndex].visible = false;
    }
  }
}

renderer.setAnimationLoop((time, frame) => {
  worldAnchor.rotation.y = time * 0.00007;

  if (frame) {
    const referenceSpace = renderer.xr.getReferenceSpace();
    updateHands(frame, referenceSpace);
  }

  renderer.render(scene, camera);
});

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch((err) => {
      console.warn('Service worker registration failed:', err);
    });
  });
}

setStatus('Checking WebXR support…');
enterButton.disabled = true;
initXRSupport();
