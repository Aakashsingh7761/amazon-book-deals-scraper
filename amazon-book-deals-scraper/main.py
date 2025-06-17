import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36'
}

url = "https://www.amazon.in/s?k=python+books&rh=p_36%3A-50000"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

books = []
results = soup.find_all("div", {"data-component-type": "s-search-result"})

for item in results:
    title = item.h2.text.strip()
    link = "https://www.amazon.in" + item.h2.a["href"]
    try:
        price = item.find("span", "a-price-whole").text.strip()
    except:
        price = "N/A"
    try:
        rating = item.find("span", "a-icon-alt").text.strip()
    except:
        rating = "No rating"
    
    books.append({
        "Title": title,
        "Price (INR)": price,
        "Rating": rating,
        "Link": link
    })

df = pd.DataFrame(books)
df.to_csv("amazon_books.csv", index=False)
print("Scraped", len(df), "books under ₹500. Saved to amazon_books.csv")
