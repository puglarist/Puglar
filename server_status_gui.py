"""Simple GUI dashboard for Fortnite and Warzone service health.

Data sources:
- Epic Games public status summary API for Fortnite/Epic Online Services components.
- Activision Online Services page scraped for Call of Duty: Warzone row.
"""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

import requests
from bs4 import BeautifulSoup

EPIC_SUMMARY_URL = "https://status.epicgames.com/api/v2/summary.json"
ACTIVISION_SERVICES_URL = "https://support.activision.com/onlineservices"
USER_AGENT = "PuglarServerStatus/1.0 (+https://example.local)"
TIMEOUT_SECONDS = 12


@dataclass
class ServiceStatus:
    game: str
    source: str
    status: str
    details: str


class StatusScraper:
    """Scrapes Fortnite and Warzone status from public sources."""

    def _request(self, url: str) -> requests.Response:
        return requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT_SECONDS,
        )

    def fetch_fortnite_status(self) -> ServiceStatus:
        response = self._request(EPIC_SUMMARY_URL)
        response.raise_for_status()

        summary = response.json()
        components = summary.get("components", [])

        fortnite_components = [
            c
            for c in components
            if "fortnite" in c.get("name", "").lower()
            or "epic online services" in c.get("name", "").lower()
        ]

        if not fortnite_components:
            return ServiceStatus(
                game="Fortnite",
                source=EPIC_SUMMARY_URL,
                status="Unknown",
                details="No Fortnite components were found in Epic status summary.",
            )

        degraded = [
            c for c in fortnite_components if c.get("status", "") != "operational"
        ]

        if degraded:
            detail = "; ".join(
                f"{c.get('name', 'component')}: {c.get('status', 'unknown')}"
                for c in degraded
            )
            return ServiceStatus(
                game="Fortnite",
                source=EPIC_SUMMARY_URL,
                status="Degraded",
                details=detail,
            )

        return ServiceStatus(
            game="Fortnite",
            source=EPIC_SUMMARY_URL,
            status="Operational",
            details=f"Checked {len(fortnite_components)} Epic/Fortnite components.",
        )

    def fetch_warzone_status(self) -> ServiceStatus:
        response = self._request(ACTIVISION_SERVICES_URL)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        row = None
        for tr in soup.select("tr"):
            text = " ".join(tr.stripped_strings).lower()
            if "warzone" in text:
                row = tr
                break

        if row is None:
            return ServiceStatus(
                game="Warzone",
                source=ACTIVISION_SERVICES_URL,
                status="Unknown",
                details="Could not find a Warzone row on Activision Online Services page.",
            )

        text = " ".join(row.stripped_strings)
        lower = text.lower()

        if "online" in lower and "offline" not in lower:
            state = "Operational"
        elif "offline" in lower:
            state = "Outage"
        else:
            state = "Unknown"

        return ServiceStatus(
            game="Warzone",
            source=ACTIVISION_SERVICES_URL,
            status=state,
            details=text,
        )

    def fetch_all(self) -> Iterable[ServiceStatus]:
        return [self.fetch_fortnite_status(), self.fetch_warzone_status()]


class ServerStatusGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Fortnite + Warzone World Server Status")
        self.root.geometry("880x320")

        self.scraper = StatusScraper()

        frame = ttk.Frame(root, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            frame,
            columns=("game", "status", "details", "source"),
            show="headings",
            height=8,
        )
        self.tree.heading("game", text="Game")
        self.tree.heading("status", text="Status")
        self.tree.heading("details", text="Details")
        self.tree.heading("source", text="Source")

        self.tree.column("game", width=110, anchor=tk.W)
        self.tree.column("status", width=110, anchor=tk.W)
        self.tree.column("details", width=370, anchor=tk.W)
        self.tree.column("source", width=260, anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True)

        controls = ttk.Frame(frame)
        controls.pack(fill=tk.X, pady=(8, 0))

        self.refresh_button = ttk.Button(controls, text="Refresh", command=self.refresh)
        self.refresh_button.pack(side=tk.LEFT)

        self.status_label = ttk.Label(controls, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=(12, 0))

        self.refresh()

    def refresh(self):
        self.refresh_button.configure(state=tk.DISABLED)
        self.status_label.configure(text="Refreshing...")

        def worker():
            try:
                statuses = list(self.scraper.fetch_all())
                self.root.after(0, lambda: self._update_table(statuses, None))
            except Exception as exc:  # noqa: BLE001
                self.root.after(0, lambda: self._update_table([], str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def _update_table(self, statuses: list[ServiceStatus], error: str | None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if error:
            self.tree.insert("", tk.END, values=("Error", "Failed", error, ""))
            self.status_label.configure(text="Refresh failed")
        else:
            for service in statuses:
                self.tree.insert(
                    "",
                    tk.END,
                    values=(service.game, service.status, service.details, service.source),
                )
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.status_label.configure(text=f"Updated {now}")

        self.refresh_button.configure(state=tk.NORMAL)


def main():
    root = tk.Tk()
    ServerStatusGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
