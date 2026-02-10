const isQuestBrowser = /OculusBrowser|MetaQuest/i.test(navigator.userAgent);
const hasWebXR = typeof navigator.xr !== 'undefined';
const isSecure = window.isSecureContext;

const checklist = [
  {
    label: 'Secure context (required for WebXR)',
    pass: isSecure
  },
  {
    label: 'WebXR API available (navigator.xr)',
    pass: hasWebXR
  },
  {
    label: 'Meta Quest browser user-agent detected',
    pass: isQuestBrowser
  },
  {
    label: 'Static hosting friendly for GitHub Pages',
    pass: true
  }
];

const questBadge = document.getElementById('questBadge');
questBadge.textContent = isQuestBrowser ? 'Quest detected' : 'Non-Quest browser';
questBadge.className = `badge ${isQuestBrowser ? 'ok' : 'warn'}`;

const runtimeChecklist = document.getElementById('runtimeChecklist');
checklist.forEach((item) => {
  const li = document.createElement('li');
  li.textContent = `${item.pass ? '✅' : '⚠️'} ${item.label}`;
  runtimeChecklist.appendChild(li);
});

const highlights = [
  'Engine block supports common web-focused renderers and version pinning.',
  'Runtime block includes explicit WebXR and networking requirements.',
  'Metaverse features cover identity, avatars, world streaming, and economy.',
  'Deployment block forces HTTPS and includes GitHub Pages as a target platform.'
];

const schemaHighlights = document.getElementById('schemaHighlights');
highlights.forEach((text) => {
  const li = document.createElement('li');
  li.textContent = text;
  schemaHighlights.appendChild(li);
});

const exampleJson = document.getElementById('exampleJson');
fetch('./schema/example.metaquest-profile.json')
  .then((res) => res.json())
  .then((data) => {
    exampleJson.textContent = JSON.stringify(data, null, 2);
  })
  .catch(() => {
    exampleJson.textContent = 'Could not load example profile. Make sure the app is served over HTTP/HTTPS.';
  });
