import * as THREE from 'https://unpkg.com/three@0.161.0/build/three.module.js';
import { VRButton } from 'https://unpkg.com/three@0.161.0/examples/jsm/webxr/VRButton.js';
import { XRHandModelFactory } from 'https://unpkg.com/three@0.161.0/examples/jsm/webxr/XRHandModelFactory.js';

const statusEl = document.querySelector('#status');
const enterButton = document.querySelector('#enter-xr');

const setStatus = (message) => {
  statusEl.textContent = message;
};

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.xr.enabled = true;
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x070c18);

const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.01, 100);
camera.position.set(0, 1.6, 2);

scene.add(new THREE.HemisphereLight(0xffffff, 0x223355, 1.2));
const keyLight = new THREE.DirectionalLight(0xffffff, 1.2);
keyLight.position.set(2, 4, 1);
scene.add(keyLight);

const grid = new THREE.GridHelper(8, 24, 0x4d83ff, 0x28418a);
grid.position.y = 0;
scene.add(grid);

const floor = new THREE.Mesh(
  new THREE.CircleGeometry(4, 64),
  new THREE.MeshStandardMaterial({ color: 0x101f42, roughness: 0.9, metalness: 0.05 }),
);
floor.rotation.x = -Math.PI / 2;
scene.add(floor);

const orb = new THREE.Mesh(
  new THREE.IcosahedronGeometry(0.2, 3),
  new THREE.MeshStandardMaterial({ color: 0x66ddff, emissive: 0x145574, emissiveIntensity: 0.7 }),
);
orb.position.set(0, 1.4, -1.1);
scene.add(orb);

const handFactory = new XRHandModelFactory();
const handAnchors = [
  { hand: renderer.xr.getHand(0), color: 0x68ffa1 },
  { hand: renderer.xr.getHand(1), color: 0xff89c2 },
];

for (const { hand, color } of handAnchors) {
  const model = handFactory.createHandModel(hand, 'mesh');
  hand.add(model);

  const fingertipMarker = new THREE.Mesh(
    new THREE.SphereGeometry(0.02, 18, 18),
    new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: 0.5 }),
  );
  fingertipMarker.visible = false;
  hand.add(fingertipMarker);
  hand.userData.fingertipMarker = fingertipMarker;

  scene.add(hand);
}

const TEMP = new THREE.Vector3();
let pinchDetected = false;

function handleHands() {
  let anyTracked = false;
  pinchDetected = false;

  for (const { hand } of handAnchors) {
    const indexTip = hand.joints['index-finger-tip'];
    const thumbTip = hand.joints['thumb-tip'];
    const marker = hand.userData.fingertipMarker;

    if (!indexTip || !thumbTip || !indexTip.visible || !thumbTip.visible) {
      if (marker) marker.visible = false;
      continue;
    }

    anyTracked = true;

    if (marker) {
      marker.visible = true;
      marker.position.copy(indexTip.position);
    }

    const pinchDistance = indexTip.position.distanceTo(thumbTip.position);
    if (pinchDistance < 0.03) {
      pinchDetected = true;
      TEMP.copy(indexTip.position);
      TEMP.z -= 0.3;
      orb.position.lerp(TEMP, 0.35);
    }
  }

  if (!anyTracked) {
    setStatus('Waiting for hands… move hands into view.');
    return;
  }

  if (pinchDetected) {
    setStatus('Pinch detected ✅ Orb follows your fingertips.');
  } else {
    setStatus('Hands tracked ✅ Try pinching index + thumb.');
  }
}

function animate(timeMs) {
  const t = timeMs * 0.001;
  orb.rotation.x = t * 0.7;
  orb.rotation.y = t * 1.2;
  orb.position.y = 1.4 + Math.sin(t * 1.3) * 0.06;

  handleHands();
  renderer.render(scene, camera);
}
renderer.setAnimationLoop(animate);

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

const enableXRButton = () => {
  const vrButton = VRButton.createButton(renderer, {
    optionalFeatures: ['local-floor', 'bounded-floor', 'hand-tracking'],
  });
  vrButton.style.display = 'none';
  document.body.appendChild(vrButton);

  enterButton.disabled = false;
  setStatus('Ready. Press Enter VR on Quest Browser.');

  enterButton.addEventListener('click', () => vrButton.click());
};

if (!navigator.xr) {
  enterButton.disabled = true;
  setStatus('WebXR not available. Open this page in Meta Quest Browser.');
} else {
  navigator.xr
    .isSessionSupported('immersive-vr')
    .then((supported) => {
      if (!supported) {
        enterButton.disabled = true;
        setStatus('Immersive VR session not supported on this device/browser.');
        return;
      }
      enableXRButton();
    })
    .catch((error) => {
      enterButton.disabled = true;
      setStatus(`WebXR check failed: ${error.message}`);
    });
}
