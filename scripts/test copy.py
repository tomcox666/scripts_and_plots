import tkinter as tk
from tkinter import messagebox
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#------Processing Reviews-------#

# Initialize sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Function to classify sentiment
def classify_sentiment(review):
    score = sid.polarity_scores(review)
    if score['compound'] >= 0.05:
        return 'Good'
    elif score['compound'] <= -0.05:
        return 'Bad'
    else:
        return 'Neutral'

# Function to handle review submission
def submit_review():
    name = name_entry.get().strip()
    order = order_entry.get().strip()
    review = review_text.get("1.0", tk.END).strip()

    if not name or not order or not review:
        messagebox.showerror("Error", "All fields are required.")
        return

    sentiment = classify_sentiment(review)
    
    new_row = {"Name": name, "Order": order, "Review": review, "Sentiment": sentiment}

    try:
        df = pd.read_excel("bakery_reviews.xlsx")
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([new_row])

    df.to_excel("outputs/bakery_reviews.xlsx", index=False)

    messagebox.showinfo("Success", "Review submitted successfully!")
    clear_form()

# Function to clear the form after submission
def clear_form():
    name_entry.delete(0, tk.END)
    order_entry.delete(0, tk.END)
    review_text.delete("1.0", tk.END)

#------Create the main application window-------#

root = tk.Tk()
root.title("Bakery Review App")

name_label = tk.Label(root, text="Your Name:")
name_label.grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(root, width=40)
name_entry.grid(row=0, column=1, padx=10, pady=10)

order_label = tk.Label(root, text="Your Order:")
order_label.grid(row=1, column=0, padx=10, pady=10)
order_entry = tk.Entry(root, width=40)
order_entry.grid(row=1, column=1, padx=10, pady=10)

review_label = tk.Label(root, text="Your Review:")
review_label.grid(row=2, column=0, padx=10, pady=10)
review_text = tk.Text(root, height=10, width=40)
review_text.grid(row=2, column=1, padx=10, pady=10)

submit_button = tk.Button(root, text="Submit Review", command=submit_review)
submit_button.grid(row=3, column=1, padx=10, pady=10)

root.mainloop()