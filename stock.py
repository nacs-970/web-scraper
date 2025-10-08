from bs4 import BeautifulSoup
from datetime import datetime
import csv
import requests
import time
import os

def date_to_timestamp(date_str):
    """Convert YYYY-MM-DD string to Unix timestamp"""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return int(time.mktime(dt.timetuple()))

def save(table, ticker, date1, date2, save_dir="out"):

    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, f"{ticker}_{date1}_{date2}.csv")

    # Extract headers
    headers = [th.get_text(strip=True) for th in table.find_all('th')]
    headers[4] = "Close"
    headers[5] = "Adj Close"
    
    # Extract rows
    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip header row
        cols = tr.find_all(['td', 'th'])
        row = [td.get_text(strip=True) for td in cols]
        if not any("Dividend" in cell for cell in row):
            rows.append(row)
    
    # Save to CSV
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    
    print(f"CSV file '{path}' has been created.")

def scrape(tricker=None, period1=None, period2=None):

    if not tricker:
        ticker = input("Enter ticker symbol (e.g., VOO): ").strip().upper()

    if not period1:
        date1 = input("Enter start date (YYYY-MM-DD): ").strip()
        period1 = date_to_timestamp(date1)

    if not period2:
        date2 = input("Enter end date (YYYY-MM-DD): ").strip()
        period2 = date_to_timestamp(date2)

    # Yahoo Finance VOO history URL with date range
    url = f'https://finance.yahoo.com/quote/{tricker.upper()}/history/?period1={period1}&period2={period2}'

    # Headers and cookies from curl 
    # 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101',}
    # get it from f12 network
    # d=.....&......
    cookies = {
        'A1' : 'cookies',
        'A3' : 'cookies',
        'A1S': 'cookies',
    }
    
    # Send the request
    response = requests.get(url, headers=headers, cookies=cookies)
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table by class name (you can refine this if needed)
    table = soup.find('table')
    
    # Print the table if found
    if not table:
        print("Table not found!")
    else:
        print("scrapping table...")
        save(table, tricker, date1, date2)

if __name__ == "__main__":
    scrape("VOO")
