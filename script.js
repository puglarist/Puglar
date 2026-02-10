const output = document.getElementById('url-output');
const button = document.getElementById('show-url');

button?.addEventListener('click', () => {
  const host = window.location.hostname;

  if (host.endsWith('github.io')) {
    output.textContent = `Opened from GitHub Pages: ${window.location.href}`;
    return;
  }

  output.textContent =
    'GitHub Pages URL format: https://<your-github-username>.github.io/<repo-name>/';
});
