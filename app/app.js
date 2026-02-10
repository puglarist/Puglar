class RollSDKAdapter {
  constructor(config = {}) {
    this.config = config;
    this.initialized = false;
  }

  async initialize() {
    await new Promise((resolve) => setTimeout(resolve, 300));
    this.initialized = true;
    return {
      status: "connected",
      network: this.config.network ?? "roll-mainnet",
      wallet: this.config.wallet ?? "metaverse-uploader",
    };
  }

  async uploadVideo(file, metadata) {
    if (!this.initialized) {
      throw new Error("ROLL SDK is not initialized");
    }

    await new Promise((resolve) => setTimeout(resolve, 450));
    return {
      assetId: `roll_${crypto.randomUUID().slice(0, 8)}`,
      fileName: file.name,
      title: metadata.title,
      channel: metadata.channel,
      size: file.size,
      createdAt: new Date().toISOString(),
    };
  }
}

class MTVMovieChannel {
  constructor() {
    this.nowPlaying = [
      "Retro Pulse: Midnight Beat",
      "Street Frame: Neon Rush",
      "The Last Tape",
    ];
    this.trending = [
      "Viral Stage Vol. 7",
      "Bytewave Documentary",
      "Meta Skaters: City Drift",
    ];
    this.genreRails = {
      Action: ["Metro Outrun", "Silent Orbit"],
      Music: ["Turntable Planet", "Live After Dark"],
      Family: ["Star Pals", "Dream Arcade"],
    };
  }

  getProgrammingSnapshot() {
    return {
      nowPlaying: this.nowPlaying,
      trending: this.trending,
      rails: this.genreRails,
    };
  }

  addUploadedTitle(title, channel) {
    this.nowPlaying.unshift(`${title} (${channel})`);
    this.trending.unshift(title);
  }
}

class MetaverseStreamingHub {
  constructor({ sdk, channel }) {
    this.sdk = sdk;
    this.channel = channel;
    this.library = [];
    this.providers = ["MTV", "Hulu", "Netflix", "Disney+"];
  }

  async upload(file, metadata) {
    const asset = await this.sdk.uploadVideo(file, metadata);
    this.library.unshift(asset);
    this.channel.addUploadedTitle(metadata.title, metadata.channel);
    return asset;
  }
}

const sdk = new RollSDKAdapter({
  network: "roll-mainnet",
  wallet: "puglar-channel-vault",
});
const channel = new MTVMovieChannel();
const hub = new MetaverseStreamingHub({ sdk, channel });

const sdkConnectionElement = document.getElementById("sdk-connection");
const sdkNetworkElement = document.getElementById("sdk-network");
const nowPlayingElement = document.getElementById("now-playing");
const trendingElement = document.getElementById("trending-list");
const railsElement = document.getElementById("genre-rails");
const uploadForm = document.getElementById("upload-form");
const uploadFeedback = document.getElementById("upload-feedback");
const uploadedVideosElement = document.getElementById("uploaded-videos");

const renderProgramming = () => {
  const snapshot = channel.getProgrammingSnapshot();

  nowPlayingElement.innerHTML = snapshot.nowPlaying.map((title) => `<li>${title}</li>`).join("");
  trendingElement.innerHTML = snapshot.trending.map((title) => `<li>${title}</li>`).join("");
  railsElement.innerHTML = Object.entries(snapshot.rails)
    .map(([genre, titles]) => `<li><strong>${genre}</strong>: ${titles.join(", ")}</li>`)
    .join("");
};

const renderUploads = () => {
  uploadedVideosElement.innerHTML = hub.library
    .map(
      (asset) =>
        `<li><strong>${asset.title}</strong> · ${asset.channel} · ${Math.round(asset.size / 1024)} KB · ${asset.assetId}</li>`,
    )
    .join("");
};

const initialize = async () => {
  try {
    const connection = await sdk.initialize();
    sdkConnectionElement.textContent = `ROLL SDK ${connection.status}`;
    sdkNetworkElement.textContent = `Network: ${connection.network} · Wallet: ${connection.wallet}`;
  } catch (error) {
    sdkConnectionElement.textContent = "ROLL SDK connection failed";
    sdkNetworkElement.textContent = error.message;
  }

  renderProgramming();

  if (window.adsbygoogle) {
    document.querySelectorAll(".adsbygoogle").forEach(() => {
      window.adsbygoogle.push({});
    });
  }
};

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  uploadFeedback.className = "";

  const title = document.getElementById("video-title").value.trim();
  const channelName = document.getElementById("video-channel").value;
  const file = document.getElementById("video-file").files[0];

  if (!title || !file) {
    uploadFeedback.textContent = "Please provide a title and video file.";
    uploadFeedback.classList.add("error");
    return;
  }

  try {
    const asset = await hub.upload(file, { title, channel: channelName });
    uploadFeedback.textContent = `Uploaded ${asset.fileName} as ${asset.assetId}.`;
    uploadFeedback.classList.add("success");
    renderProgramming();
    renderUploads();
    uploadForm.reset();
  } catch (error) {
    uploadFeedback.textContent = `Upload failed: ${error.message}`;
    uploadFeedback.classList.add("error");
  }
});

initialize();
