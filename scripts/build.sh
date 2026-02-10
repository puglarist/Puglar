#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${ROOT_DIR}/dist"
PKG_DIR="${DIST_DIR}/puglar-package"

rm -rf "${PKG_DIR}"
mkdir -p "${PKG_DIR}"

mapfile -t PDF_FILES < <(find "${ROOT_DIR}" -maxdepth 1 -type f -name '*.pdf' -printf '%f\n' | sort)
mapfile -t ZIP_FILES < <(find "${ROOT_DIR}" -maxdepth 1 -type f -name '*.zip' -printf '%f\n' | sort)

if [[ ${#PDF_FILES[@]} -eq 0 && ${#ZIP_FILES[@]} -eq 0 ]]; then
  echo "No source doctrine files found (.pdf or .zip)."
  exit 1
fi

for file in "${PDF_FILES[@]}" "${ZIP_FILES[@]}"; do
  [[ -n "${file}" ]] || continue
  cp "${ROOT_DIR}/${file}" "${PKG_DIR}/${file}"
done

cp "${ROOT_DIR}/README.md" "${PKG_DIR}/README.md"

(
  cd "${PKG_DIR}"
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum * > SHA256SUMS.txt
  else
    shasum -a 256 * > SHA256SUMS.txt
  fi
)

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
ARCHIVE_PATH="${DIST_DIR}/puglar-build-${TIMESTAMP}.tar.gz"
mkdir -p "${DIST_DIR}"
tar -czf "${ARCHIVE_PATH}" -C "${DIST_DIR}" "puglar-package"

echo "Build complete: ${ARCHIVE_PATH}"
