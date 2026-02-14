import * as THREE from 'https://unpkg.com/three@0.164.1/build/three.module.js';
import { OrbitControls } from 'https://unpkg.com/three@0.164.1/examples/jsm/controls/OrbitControls.js';
import { XRButton } from 'https://unpkg.com/three@0.164.1/examples/jsm/webxr/XRButton.js';

const app = document.getElementById('app');
const metrics = {
  fps: document.getElementById('fps'),
  frametime: document.getElementById('frametime'),
  drawcalls: document.getElementById('drawcalls'),
  vrstate: document.getElementById('vrstate'),
  resScale: document.getElementById('resScale'),
  perfState: document.getElementById('perfState')
};

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.xr.enabled = true;
app.appendChild(renderer.domElement);

const vrButton = XRButton.createButton(renderer, {
  optionalFeatures: ['local-floor', 'bounded-floor', 'hand-tracking', 'layers']
});
vrButton.style.position = 'fixed';
vrButton.style.left = '12px';
vrButton.style.bottom = '12px';
vrButton.style.zIndex = '11';
app.appendChild(vrButton);

const scene = new THREE.Scene();
scene.background = new THREE.Color('#0b1322');
scene.fog = new THREE.Fog('#0b1322', 25, 90);

const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 200);
camera.position.set(0, 2.8, 7);

const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1.5, 0);
controls.enableDamping = true;
controls.maxPolarAngle = Math.PI * 0.48;

const hemi = new THREE.HemisphereLight(0xb9d4ff, 0x141d2f, 0.6);
scene.add(hemi);

const key = new THREE.DirectionalLight(0xffffff, 1.35);
key.position.set(5, 12, 4);
key.castShadow = true;
key.shadow.mapSize.set(1024, 1024);
key.shadow.camera.left = -20;
key.shadow.camera.right = 20;
key.shadow.camera.top = 20;
key.shadow.camera.bottom = -20;
scene.add(key);

const floor = new THREE.Mesh(
  new THREE.PlaneGeometry(220, 220),
  new THREE.MeshStandardMaterial({ color: '#111827', roughness: 0.92, metalness: 0.03 })
);
floor.rotation.x = -Math.PI / 2;
floor.receiveShadow = true;
scene.add(floor);

const grid = new THREE.GridHelper(120, 120, 0x3e7bff, 0x2b3348);
grid.position.y = 0.01;
scene.add(grid);

const buildPrototypeCity = () => {
  const root = new THREE.Group();
  const geo = new THREE.BoxGeometry(1, 1, 1);

  for (let x = -8; x <= 8; x++) {
    for (let z = -8; z <= 8; z++) {
      const noise = Math.abs(Math.sin(x * 0.83 + z * 0.71));
      const h = 0.8 + noise * 6.5;
      const tower = new THREE.Mesh(
        geo,
        new THREE.MeshStandardMaterial({
          color: new THREE.Color().setHSL(0.58 + noise * 0.1, 0.32, 0.25 + noise * 0.14),
          roughness: 0.43,
          metalness: 0.22
        })
      );
      tower.position.set(x * 2.2, h * 0.5, z * 2.2);
      tower.scale.set(1.25, h, 1.25);
      tower.castShadow = true;
      tower.receiveShadow = true;
      root.add(tower);
    }
  }

  const core = new THREE.Mesh(
    new THREE.TorusKnotGeometry(1.2, 0.42, 180, 22),
    new THREE.MeshStandardMaterial({ color: '#59b6ff', emissive: '#1a3b88', roughness: 0.18, metalness: 0.86 })
  );
  core.position.set(0, 6, 0);
  core.castShadow = true;
  root.add(core);

  return { root, core };
};

const { root: city, core } = buildPrototypeCity();
scene.add(city);

let resolutionScale = 1.0;
let emaFrame = 16.7;
let lastT = performance.now();
let frameCounter = 0;
let lastFpsSample = 0;

const adjustResolutionForQuest = (dt) => {
  emaFrame = THREE.MathUtils.lerp(emaFrame, dt, 0.08);

  if (emaFrame > 19 && resolutionScale > 0.72) {
    resolutionScale = Math.max(0.7, resolutionScale - 0.03);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2) * resolutionScale);
  }

  if (emaFrame < 14.5 && resolutionScale < 1.0) {
    resolutionScale = Math.min(1, resolutionScale + 0.02);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2) * resolutionScale);
  }

  metrics.resScale.textContent = resolutionScale.toFixed(2);
  metrics.perfState.textContent = emaFrame > 19 ? 'Performance mode active' : 'Profiling active';
};

renderer.xr.addEventListener('sessionstart', () => {
  metrics.vrstate.textContent = 'active';
  const session = renderer.xr.getSession();
  if (session?.updateRenderState) {
    session.updateRenderState({
      depthNear: 0.1,
      depthFar: 150
    });
  }
  if (renderer.xr.getCamera().cameras?.length) {
    renderer.xr.setFoveation?.(1);
  }
});

renderer.xr.addEventListener('sessionend', () => {
  metrics.vrstate.textContent = 'inactive';
});

const animate = (t) => {
  const dt = Math.min(60, t - lastT);
  lastT = t;

  adjustResolutionForQuest(dt);
  controls.update();

  const animTime = t * 0.001;
  core.rotation.x = animTime * 0.35;
  core.rotation.y = animTime * 0.8;
  core.position.y = 5.7 + Math.sin(animTime * 1.8) * 0.4;

  camera.position.x += (Math.sin(animTime * 0.18) * 8 - camera.position.x) * 0.002;

  renderer.render(scene, camera);

  frameCounter += 1;
  if (t - lastFpsSample > 400) {
    const fps = Math.round((frameCounter * 1000) / (t - lastFpsSample || 1));
    metrics.fps.textContent = fps.toString();
    metrics.frametime.textContent = emaFrame.toFixed(1);
    metrics.drawcalls.textContent = renderer.info.render.calls.toString();
    frameCounter = 0;
    lastFpsSample = t;
  }
};

renderer.setAnimationLoop(animate);

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => navigator.serviceWorker.register('/sw.js'));
}
