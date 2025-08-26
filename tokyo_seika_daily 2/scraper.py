import os, re, datetime as dt, requests
from dateutil.tz import gettz
import pdfplumber, pandas as pd, matplotlib.pyplot as plt

URLS = {
    "veg_price": "https://www.tokyo-seika.co.jp/corp/wp-content/uploads/2022/11/yasaso.pdf",
    "fruit_price": "https://www.tokyo-seika.co.jp/corp/wp-content/uploads/2022/11/kajiso.pdf",
    "veg_inbound": "https://www.tokyo-seika.co.jp/corp/wp-content/uploads/2022/01/yasanyuka.pdf",
    "fruit_inbound": "https://www.tokyo-seika.co.jp/corp/wp-content/uploads/2022/01/kajinyuka.pdf",
}

JST = gettz("Asia/Tokyo")
TODAY = dt.datetime.now(JST).date().isoformat()

os.makedirs("raw_pdfs", exist_ok=True)
os.makedirs("data", exist_ok=True)
os.makedirs(f"reports/{TODAY}", exist_ok=True)

def fetch(url, name):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    path = f"raw_pdfs/{TODAY}_{name}.pdf"
    with open(path, "wb") as f:
        f.write(r.content)
    return path

def parse_price_pdf(path, kind):
    rows = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for line in text.splitlines():
                nums = re.findall(r'\d{1,3}(?:,\d{3})*', line)
                if len(nums) >= 2:
                    item = line.split()[0]
                    hi = int(nums[0].replace(",","")) if len(nums)>=3 else None
                    mid = int(nums[1].replace(",","")) if len(nums)>=2 else None
                    lo = int(nums[2].replace(",","")) if len(nums)>=3 else None
                    rows.append({"date": TODAY, "type": kind, "item": item, "high": hi, "mid": mid, "low": lo})
    return pd.DataFrame(rows)

def parse_inbound_pdf(path, kind):
    rows = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for line in text.splitlines():
                nums = re.findall(r'\d{1,3}(?:,\d{3})*', line)
                if nums:
                    item = line.split()[0]
                    qty = int(nums[-1].replace(",",""))
                    rows.append({"date": TODAY, "type": kind, "item": item, "inbound_ton": qty})
    return pd.DataFrame(rows)

def append_csv(df, path):
    if df.empty: return
    if os.path.exists(path):
        old = pd.read_csv(path)
        df = pd.concat([old, df], ignore_index=True).drop_duplicates()
    df.to_csv(path, index=False)

def main():
    paths = {k: fetch(u,k) for k,u in URLS.items()}
    df_vp = parse_price_pdf(paths["veg_price"], "veg")
    df_fp = parse_price_pdf(paths["fruit_price"], "fruit")
    df_vi = parse_inbound_pdf(paths["veg_inbound"], "veg")
    df_fi = parse_inbound_pdf(paths["fruit_inbound"], "fruit")
    prices = pd.concat([df_vp, df_fp], ignore_index=True)
    inbound = pd.concat([df_vi, df_fi], ignore_index=True)
    append_csv(prices, "data/prices.csv")
    append_csv(inbound, "data/inbound.csv")
    # Example graph
    if not prices.empty:
        latest = prices[prices['date']==TODAY]
        latest.groupby('item')['mid'].mean().nlargest(10).plot(kind="barh", title="TOP10 mid prices")
        plt.tight_layout()
        plt.savefig(f"reports/{TODAY}/price_top10.png")

if __name__ == "__main__":
    main()
