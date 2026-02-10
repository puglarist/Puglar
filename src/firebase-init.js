import { initializeApp } from 'https://www.gstatic.com/firebasejs/12.9.0/firebase-app.js';
import { getAnalytics, isSupported } from 'https://www.gstatic.com/firebasejs/12.9.0/firebase-analytics.js';

const firebaseConfig = {
  apiKey: 'AIzaSyDs8KCpHJDQPNPAsw5zxV2kUaCqJhTeoBQ',
  authDomain: 'metaverse-e158a.firebaseapp.com',
  projectId: 'metaverse-e158a',
  storageBucket: 'metaverse-e158a.firebasestorage.app',
  messagingSenderId: '872537493763',
  appId: '1:872537493763:web:c7815b55128ec9b6129936',
  measurementId: 'G-6F1S80ZN1P'
};

const app = initializeApp(firebaseConfig);
const statusEl = document.getElementById('status');

isSupported()
  .then((supported) => {
    if (!supported) {
      statusEl.textContent = 'Firebase initialized, but Analytics is not supported in this environment.';
      return;
    }

    getAnalytics(app);
    statusEl.textContent = 'Firebase app and Analytics initialized successfully.';
  })
  .catch((error) => {
    statusEl.textContent = `Firebase initialized, but Analytics setup failed: ${error.message}`;
  });
