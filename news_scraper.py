import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data():
    url = entry_url.get()
    html_tag = entry_tag.get()
    html_class = entry_class.get()
    
    if not url or not html_tag:
        messagebox.showerror("Input Error", "Please provide both URL and HTML Tag.")
        return

    try:
        # fetch webpage content
        response = requests.get(url)
        if response.status_code != 200:
            messagebox.showerror("Error", f"Failed to fetch the webpage. Status code: {response.status_code}")
            return

        # parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # find elements based on tag and class
        if html_class:
            elements = soup.find_all(html_tag, class_=html_class)
        else:
            elements = soup.find_all(html_tag)

        # extract text from elements
        data = [element.get_text(strip=True) for element in elements]

        # update results in the GUI
        text_results.delete("1.0", tk.END)
        text_results.insert(tk.END, "\n".join(data))

        # save data for later use
        global scraped_data
        scraped_data = data

        messagebox.showinfo("Success", f"Scraped {len(data)} items from the webpage.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# function to save scraped data to CSV
def save_to_csv():
    if not scraped_data:
        messagebox.showwarning("No Data", "No data to save. Please scrape data first.")
        return

    # prompt user to choose a file location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )

    if file_path:
        try:
            # Save data to CSV
            df = pd.DataFrame(scraped_data, columns=["Scraped Data"])
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", f"Data saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

root = tk.Tk()
root.title("Web Scraper")

scraped_data = []

# input fields
tk.Label(root, text="URL:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_url = tk.Entry(root, width=50)
entry_url.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="HTML Tag:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_tag = tk.Entry(root, width=20)
entry_tag.grid(row=1, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Class Name (Optional):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_class = tk.Entry(root, width=20)
entry_class.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# buttons
btn_scrape = tk.Button(root, text="Scrape", command=scrape_data)
btn_scrape.grid(row=3, column=0, columnspan=2, pady=10)

btn_save = tk.Button(root, text="Save to CSV", command=save_to_csv)
btn_save.grid(row=4, column=0, columnspan=2, pady=10)

# results display
tk.Label(root, text="Scraped Data:").grid(row=5, column=0, padx=10, pady=5, sticky="nw")
text_results = tk.Text(root, wrap="word", height=15, width=60)
text_results.grid(row=5, column=1, padx=10, pady=5)

root.mainloop()
