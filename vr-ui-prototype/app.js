const quickSlotData = [
  { icon: '🔫', qty: 1, tint: '#ff8a39' },
  { icon: '🧪', qty: 2, tint: '#f947d2' },
  { icon: '🩹', qty: 38, tint: '#70cfff' },
  { icon: '🔋', qty: 4, tint: '#111725' },
  { icon: '💻', qty: 1, tint: '#111725' },
  { icon: '🔪', qty: 6, tint: '#111725' },
  { icon: '💣', qty: 7, tint: '#111725' },
  { icon: '🛰️', qty: 8, tint: '#111725' },
  { icon: '⚪', qty: 9, tint: '#111725' }
];

const inventoryData = [
  ['⌚', 6, 'common'], ['📓', 2, 'common'], ['🔗', 12, 'common'], ['🧢', 1, 'common'], ['🧰', 3, 'common'],
  ['🔫', 1, 'legendary'], ['🧷', 34, 'epic'], ['💻', 1, 'common'], ['🎧', 1, 'common'], ['💊', 9, 'common'],
  ['🥾', 3, 'common'], ['🧤', 2, 'common'], ['💉', 38, 'common'], ['📦', 11, 'common'], ['🔦', 4, 'common'],
  ['🧯', 5, 'common'], ['📱', 2, 'common'], ['🔭', 1, 'epic'], ['🗂️', 5, 'common'], ['🔩', 31, 'common'],
  ['💰', 2, 'legendary'], ['🥽', 1, 'common'], ['🪫', 1, 'common'], ['🧱', 6, 'common'], ['🧠', 1, 'epic']
];

const ledgerData = [
  { name: 'Gold bars', delta: '+39000' },
  { name: 'First aid kit', delta: '-18000' },
  { name: 'Laptop', delta: '+4000' },
  { name: 'Hot dog', delta: '-340' },
  { name: 'AR platform', delta: '+1000' }
];

function renderQuickSlots() {
  const root = document.getElementById('quickSlots');
  root.innerHTML = quickSlotData
    .map(({ icon, qty, tint }) => `<div class="slot" style="background:${tint}"><span>${icon}</span><em>${qty}</em></div>`)
    .join('');
}

function renderInventory() {
  const root = document.getElementById('inventoryGrid');
  root.innerHTML = inventoryData
    .map(([icon, qty, rarity]) => `
      <article class="inv-item" data-rarity="${rarity}">
        <div class="icon">${icon}</div>
        <div class="qty">${qty}</div>
      </article>
    `)
    .join('');
}

function renderLedger() {
  const root = document.getElementById('ledger');
  root.innerHTML = ledgerData
    .map(({ name, delta }) => {
      const cls = delta.startsWith('+') ? 'pos' : 'neg';
      return `<div class="tx"><span>${name}</span><strong class="${cls}">${delta}</strong></div>`;
    })
    .join('');
}

renderQuickSlots();
renderInventory();
renderLedger();
