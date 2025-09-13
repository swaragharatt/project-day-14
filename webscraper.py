import requests
from bs4 import BeautifulSoup
import threading
import time
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class ScraperApp:
    def __init__(self, root):
        self.root = root
        root.title(" Web Scraper ")
        root.geometry("800x600")
        bg_color = "#1e1e2f"   
        accent = "#6a0dad"     
        text_color = "#ffffff"

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=text_color)
        style.configure("TButton", background=accent, foreground=text_color, padding=6)
        style.map("TButton", background=[("active", "#8a2be2")])
        style.configure("TEntry", fieldbackground="#2e2e3e", foreground=text_color)
        style.configure("TSpinbox", fieldbackground="#2e2e3e", foreground=text_color)

        root.configure(bg=bg_color)
        control_frame = ttk.Frame(root, padding=10)
        control_frame.pack(fill='x')
        ttk.Label(control_frame, text="URL:").grid(row=0, column=0, sticky='w')
        self.url_var = tk.StringVar(value="https://quotes.toscrape.com")
        self.url_entry = ttk.Entry(control_frame, textvariable=self.url_var, width=70)
        self.url_entry.grid(row=0, column=1, columnspan=4, sticky='w')

        ttk.Label(control_frame, text="Item selector:").grid(row=1, column=0, sticky='w')
        self.item_var = tk.StringVar(value=".quote")
        self.item_entry = ttk.Entry(control_frame, textvariable=self.item_var, width=20)
        self.item_entry.grid(row=1, column=1, sticky='w')

        ttk.Label(control_frame, text="Text selector:").grid(row=1, column=2, sticky='w')
        self.text_var = tk.StringVar(value=".text")
        self.text_entry = ttk.Entry(control_frame, textvariable=self.text_var, width=20)
        self.text_entry.grid(row=1, column=3, sticky='w')

        ttk.Label(control_frame, text="Author selector:").grid(row=1, column=4, sticky='w')
        self.author_var = tk.StringVar(value=".author")
        self.author_entry = ttk.Entry(control_frame, textvariable=self.author_var, width=20)
        self.author_entry.grid(row=1, column=5, sticky='w')

        ttk.Label(control_frame, text="Pages:").grid(row=2, column=0, sticky='w')
        self.pages_var = tk.IntVar(value=1)
        self.pages_spin = ttk.Spinbox(control_frame, from_=1, to=100, textvariable=self.pages_var, width=5)
        self.pages_spin.grid(row=2, column=1, sticky='w')

        ttk.Label(control_frame, text="Delay (s):").grid(row=2, column=2, sticky='w')
        self.delay_var = tk.DoubleVar(value=1.0)
        self.delay_spin = ttk.Spinbox(control_frame, from_=0, to=10, increment=0.5, textvariable=self.delay_var, width=5)
        self.delay_spin.grid(row=2, column=3, sticky='w')

        self.start_btn = ttk.Button(control_frame, text="Start Scrape", command=self.start_scrape)
        self.start_btn.grid(row=2, column=4, sticky='w', padx=5)
        self.save_btn = ttk.Button(control_frame, text="Save CSV", command=self.save_csv)
        self.save_btn.grid(row=2, column=5, sticky='w', padx=5)

        result_frame = ttk.Frame(root, padding=(10,0,10,10))
        result_frame.pack(fill='both', expand=True)
        self.text = tk.Text(result_frame, wrap='word', bg="#2e2e3e", fg=text_color, insertbackground=text_color)
        self.text.pack(side='left', fill='both', expand=True)
        self.scroll = ttk.Scrollbar(result_frame, command=self.text.yview)
        self.scroll.pack(side='right', fill='y')
        self.text['yscrollcommand'] = self.scroll.set

        self.status_var = tk.StringVar(value="Ready")
        self.status = ttk.Label(root, textvariable=self.status_var, relief='sunken', anchor='w', background=bg_color, foreground=accent)
        self.status.pack(fill='x', side='bottom')

        self.results = []
        self._is_scraping = False

    def start_scrape(self):
        if self._is_scraping:
            messagebox.showinfo("Scraper", "Scraping in progress already.")
            return
        url = self.url_var.get().strip()
        item_sel = self.item_var.get().strip()
        text_sel = self.text_var.get().strip()
        author_sel = self.author_var.get().strip()
        pages = int(self.pages_var.get())
        delay = float(self.delay_var.get())

        if not url:
            messagebox.showerror("Error", "Please enter a URL.")
            return
        if not item_sel:
            messagebox.showerror("Error", "Please enter an item selector.")
            return
        self.results = []
        self.text.delete('1.0', tk.END)
        self.status_var.set("Starting...")
        self._is_scraping = True
        thread = threading.Thread(target=self._worker_scrape, args=(url, item_sel, text_sel, author_sel, pages, delay), daemon=True)
        thread.start()

    def _worker_scrape(self, url, item_sel, text_sel, author_sel, pages, delay):
        headers = {"User-Agent": "Mozilla/5.0 (compatible; EasyScraper/1.0)"}
        try:
            for page in range(1, pages+1):
                if '{page}' in url:
                    current_url = url.format(page=page)
                elif pages > 1:
                    current_url = f"{url.rstrip('/')}/page/{page}/"
                else:
                    current_url = url

                self._set_status(f"Fetching: {current_url}")
                try:
                    resp = requests.get(current_url, headers=headers, timeout=15)
                except Exception as e:
                    self._append_text(f"Error fetching {current_url}: {e}\n")
                    break

                if resp.status_code != 200:
                    self._append_text(f"Non-200 response for {current_url}: {resp.status_code}\n")
                    break

                soup = BeautifulSoup(resp.text, "html.parser")
                items = soup.select(item_sel)
                if not items:
                    self._append_text(f"No items found on {current_url} using selector '{item_sel}'\n")
                for it in items:
                    if text_sel:
                        t_el = it.select_one(text_sel)
                        text = t_el.get_text(strip=True) if t_el else ""
                    else:
                        text = it.get_text(strip=True)
                    author = ""
                    if author_sel:
                        a_el = it.select_one(author_sel)
                        author = a_el.get_text(strip=True) if a_el else ""
                    record = {"text": text, "author": author, "source": current_url}
                    self.results.append(record)
                    self._append_text(f"{text} — {author}\n\n")

                if page < pages:
                    time.sleep(delay)
        finally:
            self._is_scraping = False
            self._set_status("Done (or stopped).")

    def _append_text(self, msg):
        self.root.after(0, lambda: self._do_append(msg))

    def _do_append(self, msg):
        self.text.insert(tk.END, msg)
        self.text.see(tk.END)

    def _set_status(self, msg):
        self.root.after(0, lambda: self.status_var.set(msg))

    def save_csv(self):
        if not self.results:
            messagebox.showinfo("No data", "No results to save. Run a scrape first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Text", "Author", "Source"])
                for r in self.results:
                    writer.writerow([r.get("text",""), r.get("author",""), r.get("source","")])
            messagebox.showinfo("Saved", f"Saved {len(self.results)} rows to {path}")
        except Exception as e:
            messagebox.showerror("Save error", str(e))


def main():
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
