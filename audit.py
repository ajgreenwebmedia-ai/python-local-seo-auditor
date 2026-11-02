import pandas as pd
import requests
from bs4 import BeautifulSoup

# List of target URLs to audit
urls = [
    "https://the1111spacce.com/",
    "https://the1111spacce.com/about-us",
    "https://the1111spacce.com/contact",
]

results = []
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

print("🔎 Starting Automated SEO Audit...\n")

for url in urls:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "MISSING"
        title_len = len(title) if title != "MISSING" else 0

        meta_desc_tag = soup.find("meta", attrs={"name": "description"})
        meta_desc = (
            meta_desc_tag["content"].strip()
            if meta_desc_tag and "content" in meta_desc_tag.attrs
            else "MISSING"
        )
        meta_len = len(meta_desc) if meta_desc != "MISSING" else 0

        h1_tags = soup.find_all("h1")
        h1_count = len(h1_tags)

        canonical_tag = soup.find("link", attrs={"rel": "canonical"})
        canonical = (
            canonical_tag["href"]
            if canonical_tag and "href" in canonical_tag.attrs
            else "MISSING"
        )

        has_schema = "YES" if "application/ld+json" in response.text else "NO"

        results.append({
            "URL": url,
            "Status Code": response.status_code,
            "Response Time (s)": round(response.elapsed.total_seconds(), 2),
            "Title Tag": title,
            "Title Length": title_len,
            "Meta Description": meta_desc,
            "Meta Desc Length": meta_len,
            "H1 Count": h1_count,
            "Canonical URL": canonical,
            "JSON-LD Schema Found": has_schema,
        })

        print(f"✅ Audited: {url} | Status: {response.status_code}")

    except Exception as e:
        print(f"❌ Failed: {url} | Error: {e}")

df = pd.DataFrame(results)
df["Title Status"] = df["Title Length"].apply(
    lambda x: (
        "OK" if 30 <= x <= 60 else ("MISSING" if x == 0 else "Needs Fix")
    )
)
df["Meta Status"] = df["Meta Desc Length"].apply(
    lambda x: (
        "OK" if 120 <= x <= 160 else ("MISSING" if x == 0 else "Needs Fix")
    )
)

df.to_csv("seo_audit_report.csv", index=False)
print("\n🎉 Audit complete! Output saved to 'seo_audit_report.csv'.")
