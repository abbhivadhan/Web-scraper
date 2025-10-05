import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import webbrowser

def scrape_links():
    url = url_entry.get().strip()
    output_box.config(state=tk.NORMAL)
    output_box.delete(1.0, tk.END)

    if not url.startswith("http"):
        messagebox.showwarning("Invalid URL", "Enter a URL starting with http or https.")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        messagebox.showerror("Connection Error", f"Failed to connect:\n{e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)

    if not links:
        output_box.insert(tk.END, "No links found on this page.")
        return

    for i, tag in enumerate(links, 1):
        full_url = urljoin(url, tag['href'])
        tag_name = f"link{i}"
        output_box.insert(tk.END, f"{i}. {full_url}\n", tag_name)
        output_box.tag_config(tag_name, foreground="red", underline=1)
        output_box.tag_bind(tag_name, "<Button-1>", lambda e, link=full_url: webbrowser.open_new(link))

    output_box.config(state=tk.DISABLED)


root = tk.Tk()
root.title("Web Link Scraper")
root.geometry("800x550")
root.configure(bg="#1e1e2f")

# Fonts and styles
header_font = ("Helvetica", 18, "bold")
label_font = ("Helvetica", 12)
button_font = ("Helvetica", 11, "bold")

# Title
tk.Label(root, text="🌐 Web Link Scraper", font=header_font, fg="white", bg="#1e1e2f").pack(pady=(20, 10))

# URL Input
url_frame = tk.Frame(root, bg="#1e1e2f")
url_frame.pack()
tk.Label(url_frame, text="Enter Website URL:", font=("helvetica", 16), fg="white", bg="#1e1e2f").pack(side=tk.LEFT, padx=5)
url_entry = tk.Entry(url_frame, width=60, font=("Helvetica", 14))
url_entry.insert(0, "https://")
url_entry.pack(side=tk.LEFT, padx=5)

# Scrape Button
def on_enter(e): scrape_button.config(bg="#000000")
def on_leave(e): scrape_button.config(bg="#000000")

scrape_button = tk.Button(root, text="Scrape Links", font=button_font, bg="#000000", fg="#000000",
                          width=7, height=2, command=scrape_links, relief=tk.FLAT, cursor="arrow")
scrape_button.pack(pady=15)
scrape_button.bind("<Enter>", on_enter)
scrape_button.bind("<Leave>", on_leave)

# Output Box (read-only, with clickable links)
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#000000", width=95, height=20,
                                       font=("Consolas", 16), cursor="arrow")
output_box.pack(padx=10, pady=10)
output_box.config(state=tk.DISABLED)

root.mainloop()