class RNG {
  constructor(seed = 'default') {
    this.state = [...seed].reduce((acc, c) => acc + c.charCodeAt(0), 0) || 1;
  }

  next() {
    this.state = (this.state * 1664525 + 1013904223) % 4294967296;
    return this.state / 4294967296;
  }

  pick(arr) {
    return arr[Math.floor(this.next() * arr.length)];
  }
}

const state = {
  rng: new RNG('PUGLAR-TOURNEY'),
  players: [],
  round: 0,
  deckPool: [
    { name: 'Flare Cub', type: 'Fire', hp: 80, attack: 'Blaze Bite', damage: 35, energy: 2 },
    { name: 'Aqua Lynx', type: 'Water', hp: 95, attack: 'Tide Crash', damage: 30, energy: 2 },
    { name: 'Moss Toad', type: 'Grass', hp: 110, attack: 'Root Slam', damage: 28, energy: 1 },
    { name: 'Spark Drake', type: 'Electric', hp: 70, attack: 'Arc Burst', damage: 50, energy: 3 },
    { name: 'Mind Crow', type: 'Psychic', hp: 85, attack: 'Psi Slice', damage: 40, energy: 2 }
  ],
  pool: {
    entryFee: 0,
    total: 0,
    rakePct: 0,
    prizePool: 0,
    platformCut: 0
  }
};

const el = {
  entryFee: document.getElementById('entryFee'),
  playerCount: document.getElementById('playerCount'),
  rake: document.getElementById('rake'),
  seed: document.getElementById('seed'),
  poolInfo: document.getElementById('poolInfo'),
  cardName: document.getElementById('cardName'),
  cardType: document.getElementById('cardType'),
  cardHp: document.getElementById('cardHp'),
  cardAttackName: document.getElementById('cardAttackName'),
  cardDamage: document.getElementById('cardDamage'),
  cardEnergy: document.getElementById('cardEnergy'),
  customDeck: document.getElementById('customDeck'),
  battleLog: document.getElementById('battleLog'),
  canvas: document.getElementById('battleCanvas'),
  createTournament: document.getElementById('createTournament'),
  addCard: document.getElementById('addCard'),
  runRound: document.getElementById('runRound'),
  autoPlay: document.getElementById('autoPlay'),
  reset: document.getElementById('reset')
};

const ctx = el.canvas.getContext('2d');

function logLine(message) {
  const timestamp = new Date().toLocaleTimeString();
  el.battleLog.innerHTML = `[${timestamp}] ${message}<br>` + el.battleLog.innerHTML;
}

function createPlayers(count) {
  state.players = Array.from({ length: count }, (_, i) => ({
    id: i + 1,
    name: `Trainer-${i + 1}`,
    deck: buildDeck(),
    wins: 0,
    eliminated: false
  }));
}

function buildDeck() {
  const deck = [];
  for (let i = 0; i < 6; i += 1) {
    deck.push({ ...state.rng.pick(state.deckPool) });
  }
  return deck;
}

function deckPower(deck) {
  return deck.reduce((sum, card) => sum + card.hp * 0.25 + card.damage * 1.2 - card.energy * 3, 0);
}

function simulateBattle(p1, p2) {
  const p1Power = deckPower(p1.deck) * (0.9 + state.rng.next() * 0.22);
  const p2Power = deckPower(p2.deck) * (0.9 + state.rng.next() * 0.22);

  const winner = p1Power >= p2Power ? p1 : p2;
  const loser = winner === p1 ? p2 : p1;
  winner.wins += 1;
  loser.eliminated = true;

  const mvp = state.rng.pick(winner.deck);
  logLine(`${winner.name} defeats ${loser.name} using ${mvp.name} (${mvp.attack}, ${mvp.damage} dmg).`);
  drawBattle(winner, loser, mvp);

  return winner;
}

function pairActivePlayers() {
  const active = state.players.filter((p) => !p.eliminated);
  const shuffled = [...active].sort(() => state.rng.next() - 0.5);
  const pairs = [];
  for (let i = 0; i < shuffled.length - 1; i += 2) {
    pairs.push([shuffled[i], shuffled[i + 1]]);
  }
  if (shuffled.length % 2 === 1) {
    const bye = shuffled[shuffled.length - 1];
    bye.wins += 1;
    logLine(`${bye.name} receives a bye.`);
  }
  return pairs;
}

function runRound() {
  const active = state.players.filter((p) => !p.eliminated);
  if (active.length <= 1) {
    if (active.length === 1) payout(active[0]);
    return;
  }

  state.round += 1;
  logLine(`--- Round ${state.round} ---`);
  for (const [a, b] of pairActivePlayers()) {
    simulateBattle(a, b);
  }

  const survivors = state.players.filter((p) => !p.eliminated);
  if (survivors.length === 1) payout(survivors[0]);
}

function payout(champion) {
  const finalPool = state.pool.prizePool;
  const secondPlace = state.players.filter((p) => p.eliminated).sort((a, b) => b.wins - a.wins)[0];
  const firstShare = finalPool * 0.7;
  const secondShare = finalPool * 0.3;

  logLine(`🏆 Champion: ${champion.name} wins ${firstShare.toFixed(4)} ETH.`);
  if (secondPlace) {
    logLine(`🥈 Runner-up: ${secondPlace.name} wins ${secondShare.toFixed(4)} ETH.`);
  }
  logLine(`Platform cut retained: ${state.pool.platformCut.toFixed(4)} ETH.`);
}

function updatePoolInfo() {
  state.pool.entryFee = Number(el.entryFee.value);
  state.pool.rakePct = Number(el.rake.value);
  const playerCount = Number(el.playerCount.value);

  state.pool.total = state.pool.entryFee * playerCount;
  state.pool.platformCut = state.pool.total * (state.pool.rakePct / 100);
  state.pool.prizePool = state.pool.total - state.pool.platformCut;

  el.poolInfo.textContent = `Total: ${state.pool.total.toFixed(4)} ETH | Prize Pool: ${state.pool.prizePool.toFixed(4)} ETH | Platform: ${state.pool.platformCut.toFixed(4)} ETH`;
}

function drawBattle(winner, loser, mvp) {
  ctx.clearRect(0, 0, el.canvas.width, el.canvas.height);

  const grad = ctx.createLinearGradient(0, 0, 0, el.canvas.height);
  grad.addColorStop(0, '#252d58');
  grad.addColorStop(1, '#111629');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, el.canvas.width, el.canvas.height);

  drawCard(120, 60, winner, '#64f0a7');
  drawCard(540, 60, loser, '#ff7ea1');

  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 28px Inter, sans-serif';
  ctx.fillText('Battle Snapshot', 335, 36);
  ctx.font = '18px Inter, sans-serif';
  ctx.fillText(`MVP: ${mvp.name} • ${mvp.attack} • ${mvp.damage} DMG`, 280, 322);
}

function drawCard(x, y, player, glow) {
  ctx.save();
  ctx.shadowColor = glow;
  ctx.shadowBlur = 18;
  ctx.fillStyle = '#13172b';
  ctx.fillRect(x, y, 240, 240);
  ctx.shadowBlur = 0;
  ctx.strokeStyle = glow;
  ctx.lineWidth = 3;
  ctx.strokeRect(x, y, 240, 240);

  ctx.fillStyle = '#f4f7ff';
  ctx.font = 'bold 22px Inter, sans-serif';
  ctx.fillText(player.name, x + 16, y + 36);

  ctx.font = '16px Inter, sans-serif';
  const deckSummary = player.deck.slice(0, 3).map((c) => `${c.name} (${c.damage})`);
  ctx.fillText(`Wins: ${player.wins}`, x + 16, y + 66);
  ctx.fillText('Core cards:', x + 16, y + 96);

  deckSummary.forEach((line, i) => {
    ctx.fillText(`• ${line}`, x + 16, y + 124 + i * 26);
  });

  ctx.restore();
}

function createTournament() {
  state.rng = new RNG(el.seed.value.trim() || 'PUGLAR');
  state.round = 0;
  updatePoolInfo();
  createPlayers(Number(el.playerCount.value));
  el.battleLog.innerHTML = '';
  logLine(`Tournament created with ${state.players.length} players.`);
  logLine(`Entry ${state.pool.entryFee.toFixed(4)} ETH, prize pool ${state.pool.prizePool.toFixed(4)} ETH.`);
  ctx.clearRect(0, 0, el.canvas.width, el.canvas.height);
}

function addCustomCard() {
  const card = {
    name: el.cardName.value.trim() || 'Unknown',
    type: el.cardType.value,
    hp: Number(el.cardHp.value),
    attack: el.cardAttackName.value.trim() || 'Strike',
    damage: Number(el.cardDamage.value),
    energy: Number(el.cardEnergy.value)
  };
  state.deckPool.push(card);

  const li = document.createElement('li');
  li.textContent = `${card.name} [${card.type}] HP ${card.hp} | ${card.attack} (${card.damage}) cost ${card.energy}`;
  el.customDeck.prepend(li);
  logLine(`Custom card added: ${card.name}`);
}

el.createTournament.addEventListener('click', createTournament);
el.addCard.addEventListener('click', addCustomCard);
el.runRound.addEventListener('click', runRound);
el.autoPlay.addEventListener('click', () => {
  while (state.players.filter((p) => !p.eliminated).length > 1) {
    runRound();
  }
});
el.reset.addEventListener('click', () => {
  state.players = [];
  state.round = 0;
  el.battleLog.innerHTML = '';
  el.customDeck.innerHTML = '';
  ctx.clearRect(0, 0, el.canvas.width, el.canvas.height);
  logLine('State reset. Build a new tournament.');
});

updatePoolInfo();
createTournament();
