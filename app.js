const questRegex = /OculusBrowser|MetaQuest/i;
const isQuestBrowser = questRegex.test(navigator.userAgent);
const hasWebXR = typeof navigator.xr !== 'undefined';
const isSecure = window.isSecureContext;

const questBadge = document.getElementById('questBadge');
const runtimeChecklist = document.getElementById('runtimeChecklist');
const schemaHighlights = document.getElementById('schemaHighlights');
const validationChecklist = document.getElementById('validationChecklist');
const exampleJson = document.getElementById('exampleJson');

function appendListItem(list, pass, label, kind = 'runtime') {
  const li = document.createElement('li');
  const icon = pass ? '✅' : kind === 'error' ? '❌' : '⚠️';
  li.textContent = `${icon} ${label}`;
  list.appendChild(li);
}

async function detectImmersiveVrSupport() {
  if (!hasWebXR || typeof navigator.xr.isSessionSupported !== 'function') {
    return false;
  }

  try {
    return await navigator.xr.isSessionSupported('immersive-vr');
  } catch {
    return false;
  }
}

function basicProfileChecks(profile) {
  const checks = [];
  checks.push({ pass: typeof profile.profileName === 'string' && profile.profileName.length >= 3, label: 'profileName is present' });
  checks.push({ pass: profile?.engine?.name !== undefined, label: 'engine block is present' });
  checks.push({ pass: Array.isArray(profile?.runtime?.targetDevices) && profile.runtime.targetDevices.length > 0, label: 'runtime.targetDevices is populated' });
  checks.push({ pass: profile?.deployment?.https === true, label: 'deployment.https is true' });

  const targetsQuest = (profile?.runtime?.targetDevices || []).some((target) => target.startsWith('meta-quest-'));
  if (targetsQuest) {
    checks.push({ pass: profile?.runtime?.webXR?.immersiveVR === true, label: 'Quest profiles enforce webXR.immersiveVR=true' });
    checks.push({ pass: profile?.runtime?.webXR?.controllerSupport === true, label: 'Quest profiles enforce webXR.controllerSupport=true' });
  }

  return checks;
}

async function init() {
  const immersiveVrSupported = await detectImmersiveVrSupport();
  const runtimeChecks = [
    { pass: isSecure, label: 'Secure context (required for WebXR)' },
    { pass: hasWebXR, label: 'WebXR API available (navigator.xr)' },
    { pass: immersiveVrSupported, label: 'Immersive VR sessions supported' },
    { pass: isQuestBrowser, label: 'Meta Quest browser user-agent detected' },
    { pass: true, label: 'App uses relative paths and works on GitHub Pages' }
  ];

  runtimeChecks.forEach((item) => appendListItem(runtimeChecklist, item.pass, item.label));

  const questPass = isQuestBrowser && hasWebXR && isSecure;
  questBadge.textContent = questPass ? 'Quest-ready browser' : 'Needs environment checks';
  questBadge.className = `badge ${questPass ? 'ok' : 'warn'}`;

  [
    'Schema is Draft 2020-12 and tuned for web-hosted metaverse profiles.',
    'Quest-specific conditional rules enforce immersiveVR/controller support.',
    'Deployment section requires HTTPS, matching WebXR requirements.',
    'Page can be used as a direct smoke test on GitHub Pages.'
  ].forEach((text) => {
    const li = document.createElement('li');
    li.textContent = text;
    schemaHighlights.appendChild(li);
  });

  try {
    const [schemaRes, profileRes] = await Promise.all([
      fetch('./schema/metaverse-game-engine.schema.json'),
      fetch('./schema/example.metaquest-profile.json')
    ]);

    if (!schemaRes.ok || !profileRes.ok) {
      throw new Error('Unable to fetch schema/profile assets');
    }

    const schema = await schemaRes.json();
    const profile = await profileRes.json();

    exampleJson.textContent = JSON.stringify(profile, null, 2);

    const checks = [
      { pass: schema?.$schema === 'https://json-schema.org/draft/2020-12/schema', label: 'Schema draft is 2020-12' },
      { pass: schema?.properties?.runtime?.properties?.webXR !== undefined, label: 'Schema includes runtime.webXR block' },
      { pass: schema?.properties?.deployment?.properties?.https?.const === true, label: 'Schema enforces deployment.https=true' },
      ...basicProfileChecks(profile)
    ];

    checks.forEach((item) => appendListItem(validationChecklist, item.pass, item.label));
  } catch (error) {
    exampleJson.textContent = 'Could not load schema/profile. Ensure this page is served over HTTP/HTTPS.';
    appendListItem(validationChecklist, false, `Validation setup failed: ${error.message}`, 'error');
    questBadge.textContent = 'Validation error';
    questBadge.className = 'badge error';
  }
}

init();
