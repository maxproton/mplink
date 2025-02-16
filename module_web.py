import csv

import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

COMMON_SITEMAP_LOCATIONS = [
    "sitemap.xml",
    "sitemap_index.xml",
    "sitemap1.xml",
    "sitemap/sitemap.xml",
    "sitemap/sitemap-index.xml",
    "sitemap-list.xml",
    "sitemap-index.xml",
    "sitemap/sitemap1.xml",
    "sitemaps.xml",
]


def check_link(domain):
    if "https://" not in domain:
        domain = "https://" + domain
    try:
        response = requests.get(domain, timeout=5)
        return response.status_code
    except requests.RequestException as e:
        return 0

def is_same_domain(link, base_domain):
    return urlparse(link).netloc == urlparse(base_domain).netloc

def is_valid_xml(content):
    """Check if content is valid XML and not an HTML page"""
    try:
        if b"<html" in content.lower():  # If it's an HTML page, return False
            return False
        ET.fromstring(content)  # Try parsing as XML
        return True
    except ET.ParseError:
        return False

def get_sitemap_and_robot_links(domain, verbose):
    urls = set()  # Using a set to avoid duplicates

    # Ensure the domain has a trailing slash
    if not domain.endswith("/"):
        domain += "/"

    robots_url = urljoin(domain, "robots.txt")

    try:
        response = requests.get(robots_url, timeout=5)
        response.raise_for_status()

        # Extract Sitemap URLs from robots.txt
        sitemap_links = re.findall(r"Sitemap:\s*(.+)", response.text)
        urls.update(link.strip() for link in sitemap_links)

        # Extract "Allow" and "Disallow" rules (could contain additional links)
        other_links = re.findall(r"(Allow|Disallow):\s*(.+)", response.text)
        for _, link in other_links:
            full_url = urljoin(domain, link.strip())
            urls.add(full_url)

    except requests.RequestException as e:
        print(f"Error fetching robots.txt: {e}")

    # If no sitemaps were found in robots.txt, try common sitemap locations
    if not any("sitemap" in url for url in urls):
        if verbose:
            print("[Info] No sitemaps found in robots.txt, trying common sitemap locations...")
        for sitemap_path in COMMON_SITEMAP_LOCATIONS:
            sitemap_url = urljoin(domain, sitemap_path)
            if verbose:
                print(f"[Info] Trying sitemap {sitemap_url}")
            try:
                response = requests.get(sitemap_url, timeout=5)
                if response.status_code == 200 and "xml" in response.headers.get("Content-Type", "").lower():
                    if is_valid_xml(response.content):
                        urls.add(sitemap_url)
                        if verbose:
                            print(f"[Info] Found sitemap URL {sitemap_url}")
            except requests.RequestException:
                if verbose:
                    print(f"[Info] Nothing found at {sitemap_url} moving on..")
                pass  # Ignore errors and continue checking

    return list(urls)  # Convert back to a list

def extract_links(url, verbose, timeout=5):
    """
    Extracts <a href> and <img src> links from a webpage and checks their HTTP status.
    Returns a dictionary with 'alive' and 'dead' links.
    """
    links = set()

    try:
        # Fetch the page content
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        if verbose:
            print(f"[Info] Fetched main url content. Analysing.")
        # Extract links from <a href> and <img src>
        for tag in soup.find_all(['a', 'img']):
            link = tag.get('href') if tag.name == 'a' else tag.get('src')
            if link:
                full_url = urljoin(url, link.strip())  # Make absolute URL
                links.add(full_url)
                if verbose:
                    print(f"[Info] Adding {full_url} to collection")

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return list(links)

def generate_csv_summary(data, domain, title):
    domain = domain.replace("https://", "")
    with (open(f"report-{domain}-{title}.csv", "w", newline="") as file):
        writer = csv.DictWriter(file, fieldnames=["BASE-ADDRESS", "URL", "STATUS"])
        writer.writeheader()  # Write column headers
        for url, base in data.items():
            if base != None:
                row = {
                    "BASE-ADDRESS": base,
                    "URL": url
                }
                writer.writerow(row)
    return f"CSV {title} created"
