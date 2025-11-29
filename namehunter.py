import requests
from bs4 import BeautifulSoup
import urllib.parse

SOCIAL_PLATFORMS = {
    "Twitter": "https://twitter.com/{username}",
    "Instagram": "https://instagram.com/{username}",
    "Facebook": "https://facebook.com/{username}",
    "LinkedIn": "https://www.linkedin.com/in/{username}",
    "GitHub": "https://github.com/{username}",
    "TikTok": "https://www.tiktok.com/@{username}"
}

def check_profile(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return True
    except:
        pass
    return False

def generate_usernames(real_name):
    parts = real_name.lower().split()
    if len(parts) == 1:
        f = parts[0]
        return [f, f+"123", f+"_official"]

    f, l = parts[0], parts[-1]
    options = [
        f + l,
        f + "." + l,
        f + "_" + l,
        l + f,
        f + l + "123",
        f + "_" + l + "_official"
    ]
    return options

def search_by_name(name):
    candidates = generate_usernames(name)
    results = []

    for username in candidates:
        for platform, url in SOCIAL_PLATFORMS.items():
            profile = url.format(username=username)
            if check_profile(profile):
                results.append((platform, profile))

    return results

def google_search(name, api_key=None, cx=None):
    """Opcional: si pones tu API key de Google."""
    if not api_key or not cx:
        return []

    query = urllib.parse.quote(name)
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"

    try:
        r = requests.get(url).json()
        if "items" in r:
            return [item["link"] for item in r["items"]]
    except:
        pass

    return []


if __name__ == "__main__":
    name = input("Nombre real a buscar: ")

    print("\n🔎 Generando OSINT basado en perfiles públicos...")
    results = search_by_name(name)

    if results:
        print("\n🌐 Posibles perfiles encontrados:")
        for platform, link in results:
            print(f"- {platform}: {link}")
    else:
        print("\n❌ No se encontraron perfiles públicos para ese nombre.")

    print("\n(Opcional) Añade Google Custom Search para resultados más potentes.")
