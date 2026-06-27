#!/usr/bin/env python3
"""Generate static pages from cached Squarespace HTML snapshots."""

from __future__ import annotations

import hashlib
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FETCH_DIR = ROOT
ASSETS_IMG = ROOT / "assets" / "images"
PAGES_CSS = ROOT / "css" / "pages.css"

PAGES = [
    ("about.html", "_fetch_about.html", "about", "About — Kristina Vilyams",
     "Kristina Vilyams is a multidisciplinary artist and designer known for digital fashion, AR try-ons, and product design."),
    ("contact.html", "_fetch_contact.html", "contact", "Contact — Kristina Vilyams",
     "Get in touch with Kristina Vilyams."),
    ("press.html", "_fetch_press.html", "press", "Press — Kristina Vilyams",
     "Press coverage and features."),
    ("certifications.html", "_fetch_certifications.html", "certifications", "Certifications — Kristina Vilyams",
     "Professional certifications and courses."),
    ("central-saint-martins.html", "_fetch_central-saint-martins.html", "central-saint-martins",
     "Central Saint Martins — Kristina Vilyams", "Art Direction for Fashion coursework at Central Saint Martins."),
    ("collaborations.html", "_fetch_collaborations.html", "collaborations", "Collaborations — Kristina Vilyams",
     "Brand collaborations and creative partnerships."),
    ("editorial-features.html", "_fetch_editorial-features.html", "editorial-features",
     "Editorial Features — Kristina Vilyams", "Editorial features and articles."),
    ("moi-magazine.html", "_fetch_moi-magazine.html", "moi-magazine", "Moi Magazine — Kristina Vilyams",
     "Moi Magazine feature."),
    ("media-overview.html", "_fetch_media-overview.html", "media-overview", "Media Overview — Kristina Vilyams",
     "Media overview."),
    ("404.html", "_fetch_404.html", "", "Page Not Found — Kristina Vilyams", "Page not found."),
]

COLLAB_PAGES = [
    ("collaborations/thugpop.html", "_fetch_collaborations_thugpop.html", "collaborations/thugpop"),
    ("collaborations/susan-alexandra.html", "_fetch_collaborations_susan-alexandra.html", "collaborations/susan-alexandra"),
    ("collaborations/dollchunk.html", "_fetch_collaborations_dollchunk.html", "collaborations/dollchunk"),
    ("collaborations/gustaf-westman.html", "_fetch_collaborations_gustaf-westman.html", "collaborations/gustaf-westman"),
    ("collaborations/jiu-jie.html", "_fetch_collaborations_jiu-jie.html", "collaborations/jiu-jie"),
    ("collaborations/ouhlala-x-ioki.html", "_fetch_collaborations_ouhlala-x-ioki.html", "collaborations/ouhlala-x-ioki"),
    ("collaborations/zona-johna.html", "_fetch_collaborations_zona-johna.html", "collaborations/zona-johna"),
    ("collaborations/four.html", "_fetch_collaborations_four.html", "collaborations/four"),
]

NAV = [
    ("About", "about.html"),
    ("Collaborations", "collaborations.html"),
    ("Press", "press.html"),
    ("CSM", "central-saint-martins.html"),
    ("Contact", "contact.html"),
]

FOOTER_COLS = [
    [("About", "about.html"), ("Collaborations", "collaborations.html"), ("XR Bazaar", "https://xrbazaar.co/creators/kristinavilyams/", True)],
    [("Contact", "contact.html"), ("Virtual Try-On", "editorial-features.html"), ("CV", "https://read.cv/kristinavilyams", True)],
    [("Certifications", "certifications.html"), ("Press", "press.html"), ("Uxcel", "https://app.uxcel.com/ux/kristinavilyams", True)],
]

CONTACT_FORM_HTML = """
<div class="contact-form contact-form--page" id="contact-form">
  <form action="#" method="POST" data-form="contact">
    <div class="contact-form-field">
      <label class="contact-form-label" for="page-contact-fname">Name</label>
      <div class="contact-form-name-row">
        <div class="contact-form-subfield">
          <input id="page-contact-fname" class="contact-form-input" type="text" name="firstName" placeholder="First Name" required>
        </div>
        <div class="contact-form-subfield">
          <input id="page-contact-lname" class="contact-form-input" type="text" name="lastName" placeholder="Last Name" required>
        </div>
      </div>
    </div>
    <div class="contact-form-field">
      <label class="contact-form-label" for="page-contact-email">Email</label>
      <input id="page-contact-email" class="contact-form-input" type="email" name="email" placeholder="Email" required>
    </div>
    <div class="contact-form-field">
      <label class="contact-form-label" for="page-contact-message">Message</label>
      <textarea id="page-contact-message" class="contact-form-input contact-form-textarea" name="message" placeholder="Message" rows="6" required></textarea>
    </div>
    <button class="contact-form-submit" type="submit">Submit</button>
    <p class="contact-form-success" hidden>Thank you!</p>
  </form>
</div>
"""

downloaded: dict[str, str] = {}


def rel_prefix(output_path: str) -> str:
    depth = output_path.count("/")
    return "../" * depth if depth else ""


def url_to_local(url: str) -> str:
    clean = url.split("?")[0]
    if clean in downloaded:
        return downloaded[clean]
    name_part = clean.rsplit("/", 1)[-1]
    safe = re.sub(r"[^a-zA-Z0-9._+-]", "_", name_part)[:120]
    if not safe:
        safe = hashlib.md5(clean.encode()).hexdigest()[:12]
    dest = ASSETS_IMG / safe
    if not dest.exists():
        try:
            req = urllib.request.Request(clean, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=30).read()
            dest.write_bytes(data)
            print(f"  downloaded: {safe}")
        except Exception as exc:
            print(f"  skip image {clean}: {exc}")
            return url
    downloaded[clean] = f"assets/images/{safe}"
    return downloaded[clean]


def rewrite_urls(html: str, prefix: str) -> str:
    def repl_attr(match: re.Match) -> str:
        attr, url = match.group(1), match.group(2)
        if url.startswith("https://images.squarespace-cdn.com"):
            local = url_to_local(url)
            return f'{attr}="{prefix}{local}"'
        if url.startswith("https://www.kristinavilyams.com/"):
            path = url.replace("https://www.kristinavilyams.com/", "")
            if path in ("", "home"):
                return f'{attr}="{prefix}index.html"'
            if not path.endswith(".html") and "." not in path.split("/")[-1]:
                path = path + ".html"
            return f'{attr}="{prefix}{path}"'
        if url.startswith("/"):
            path = url.lstrip("/")
            if path in ("", "home"):
                return f'{attr}="{prefix}index.html"'
            if not path.endswith(".html") and "." not in path.split("/")[-1]:
                path = path + ".html"
            return f'{attr}="{prefix}{path}"'
        return match.group(0)

    html = re.sub(r'(href|src|data-src|data-image)="([^"]+)"', repl_attr, html)
    return html


def extract_main(html: str) -> str:
    m = re.search(r'<main[^>]*id="page"[^>]*>(.*?)</main>', html, re.DOTALL)
    if not m:
        m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    if not m:
        return '<div class="page-content"><p>Content unavailable.</p></div>'
    content = m.group(1)
    content = re.sub(r"<script[^>]*>.*?</script>", "", content, flags=re.DOTALL)
    content = re.sub(r'data-controller="[^"]*"', "", content)
    content = re.sub(r'data-current-styles="[^"]*"', "", content)
    content = re.sub(r'data-current-context="[^"]*"', "", content)
    return f'<div class="sqs-page-content">{content}</div>'


def extract_title(html: str, fallback: str) -> str:
    m = re.search(r"<title>([^<]+)</title>", html)
    return m.group(1).strip() if m else fallback


def nav_link(href: str, label: str, prefix: str, active: str) -> str:
    path = f"{prefix}{href}"
    cls = ' class="is-active"' if active and href.startswith(active.split("/")[0]) and (
        active + ".html" == href or active == href.replace(".html", "")
    ) else ""
    if active == href.replace(".html", "") or (active.endswith(href.replace(".html", "")) and href in active):
        cls = ' class="is-active"'
    # simpler active match
    active_file = active.split("/")[-1] if active else ""
    href_file = href.split("/")[-1]
    if active_file and href_file == active_file + ".html":
        cls = ' class="is-active"'
    elif active == "index" and href == "index.html":
        cls = ' class="is-active"'
    return f'<li class="header-nav-item"><a href="{path}"{cls}>{label}</a></li>'


def nav_is_active(href: str, active: str) -> bool:
    href_base = href.replace(".html", "")
    if not active:
        return False
    if active == href_base or active == href.replace(".html", ""):
        return True
    if active.startswith("collaborations/") and href == "collaborations.html":
        return True
    return False


def render_shell(title: str, description: str, body: str, output_path: str, active: str, hero_header: bool = False) -> str:
    prefix = rel_prefix(output_path)
    header_cls = "header header--dynamic" if hero_header else "header header--scrolled"
    body_cls = "homepage" if hero_header else "page"

    nav_items = []
    for label, href in NAV:
        cls = ' class="is-active"' if nav_is_active(href, active) else ""
        nav_items.append(f'<li class="header-nav-item"><a href="{prefix}{href}"{cls}>{label}</a></li>')
    nav_html = "\n              ".join(nav_items)

    mobile_nav = "\n            ".join(
        f'<li><a href="{prefix}{href}">{label}</a></li>' for label, href in NAV
    )

    footer_cols = []
    for col in FOOTER_COLS:
        links = []
        for item in col:
            label, href = item[0], item[1]
            external = item[2] if len(item) > 2 else False
            target = ' target="_blank" rel="noopener noreferrer"' if external or href.startswith("http") else ""
            h = href if href.startswith("http") else f"{prefix}{href}"
            links.append(f'<a href="{h}" class="footer-link text-highlight"{target}>{label}</a>')
        footer_cols.append('<div class="footer-links-col">\n            ' + "\n            ".join(links) + "\n          </div>")
    footer_nav = "\n          ".join(footer_cols)

    canonical = f"https://www.kristinavilyams.com/{output_path.replace('.html', '').replace('index', '')}"

    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="icon" type="image/x-icon" href="{prefix}assets/images/favicon.ico">
  <link rel="canonical" href="{canonical}">
  <link rel="stylesheet" href="{prefix}css/styles.css">
  <link rel="stylesheet" href="{prefix}css/pages.css">
</head>
<body class="{body_cls}">
  <a href="#main-content" class="skip-link">Skip to Content</a>
  <div id="site-wrapper" class="site-wrapper">
    <header id="header" class="{header_cls}">
      <div class="header-inner header-inner--desktop">
        <div class="header-title-nav-wrapper">
          <nav class="header-nav" aria-label="Primary">
            <ul class="header-nav-list">
              {nav_html}
            </ul>
          </nav>
          <div class="header-title">
            <a id="site-title" href="{prefix}index.html">Kristina Vilyams</a>
          </div>
          <div class="header-spacer" aria-hidden="true"></div>
        </div>
      </div>
      <div class="header-inner header-inner--mobile">
        <button class="header-burger" type="button" aria-label="Open Menu" aria-expanded="false" aria-controls="mobile-menu">
          <span class="header-burger-box">
            <span class="top-bun"></span><span class="patty"></span><span class="bottom-bun"></span>
          </span>
        </button>
        <div class="header-title header-title--mobile">
          <a href="{prefix}index.html">Kristina Vilyams</a>
        </div>
      </div>
    </header>
    <div id="mobile-menu" class="mobile-menu" aria-hidden="true">
      <div class="mobile-menu-panel">
        <button class="mobile-menu-close" type="button" aria-label="Close Menu">
          <span class="top-bun"></span><span class="patty"></span><span class="bottom-bun"></span>
        </button>
        <nav aria-label="Mobile">
          <ul class="mobile-menu-list">
            {mobile_nav}
          </ul>
        </nav>
      </div>
    </div>
    <main id="main-content" class="page-main">
      {body}
    </main>
    <footer id="footer" class="footer">
      <div class="footer-grid">
        <h3 class="footer-name">Kristina Vilyams</h3>
        <p class="footer-copyright">Copyright © 2026 Kristina Vilyams. All Rights Reserved.</p>
        <nav class="footer-links" aria-label="Footer">
          {footer_nav}
        </nav>
        <div class="footer-social">
          <a href="https://www.instagram.com/kristinavilyams/" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
            <svg viewBox="0 0 64 64" aria-hidden="true"><path d="M46.91,25.816c-0.073-1.597-0.326-2.687-0.697-3.641c-0.383-0.986-0.896-1.823-1.73-2.657c-0.834-0.834-1.67-1.347-2.657-1.73c-0.954-0.371-2.045-0.624-3.641-0.697C36.585,17.017,36.074,17,32,17s-4.585,0.017-6.184,0.09c-1.597,0.073-2.687,0.326-3.641,0.697c-0.986,0.383-1.823,0.896-2.657,1.73c-0.834,0.834-1.347,1.67-1.73,2.657c-0.371,0.954-0.624,2.045-0.697,3.641C17.017,27.415,17,27.926,17,32c0,4.074,0.017,4.585,0.09,6.184c0.073,1.597,0.326,2.687,0.697,3.641c0.383,0.986,0.896,1.823,1.73,2.657c0.834,0.834,1.67,1.347,2.657,1.73c0.954,0.371,2.045,0.624,3.641,0.697C27.415,46.983,27.926,47,32,47s4.585-0.017,6.184-0.09c1.597-0.073,2.687-0.326,3.641-0.697c0.986-0.383,1.823-0.896,2.657-1.73c0.834-0.834,1.347-1.67,1.73-2.657c0.371-0.954,0.624-2.045,0.697-3.641C46.983,36.585,47,36.074,47,32S46.983,27.415,46.91,25.816z M32,24.297c-4.254,0-7.703,3.449-7.703,7.703c0,4.254,3.449,7.703,7.703,7.703c4.254,0,7.703-3.449,7.703-7.703C39.703,27.746,36.254,24.297,32,24.297z M32,37c-2.761,0-5-2.239-5-5c0-2.761,2.239-5,5-5s5,2.239,5,5C37,34.761,34.761,37,32,37z M40.007,22.193c-0.994,0-1.8,0.806-1.8,1.8c0,0.994,0.806,1.8,1.8,1.8c0.994,0,1.8-0.806,1.8-1.8C41.807,22.999,41.001,22.193,40.007,22.193z"/></svg>
          </a>
          <a href="https://www.linkedin.com/in/kristinavilyams/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
            <svg viewBox="0 0 64 64" aria-hidden="true"><path d="M20.4,44h5.4V26.6h-5.4V44z M23.1,18c-1.7,0-3.1,1.4-3.1,3.1c0,1.7,1.4,3.1,3.1,3.1 c1.7,0,3.1-1.4,3.1-3.1C26.2,19.4,24.8,18,23.1,18z M39.5,26.2c-2.6,0-4.4,1.4-5.1,2.8h-0.1v-2.4h-5.2V44h5.4v-8.6 c0-2.3,0.4-4.5,3.2-4.5c2.8,0,2.8,2.6,2.8,4.6V44H46v-9.5C46,29.8,45,26.2,39.5,26.2z"/></svg>
          </a>
        </div>
        <form class="newsletter-form" action="#" method="POST" data-form="newsletter">
          <p class="newsletter-description">Sign up with your email address to receive news and updates.</p>
          <div class="newsletter-fields">
            <label class="visually-hidden" for="newsletter-email">Email Address</label>
            <input id="newsletter-email" class="newsletter-input" type="email" name="email" placeholder="Email Address" autocomplete="email" required>
            <button class="newsletter-button" type="submit">Sign Up</button>
          </div>
          <p class="newsletter-footnote">We respect your privacy.</p>
        </form>
      </div>
    </footer>
  </div>
  <script src="{prefix}js/main.js"></script>
</body>
</html>"""


def build_page(output: str, fetch_file: str, active: str, title: str, description: str) -> None:
    src = FETCH_DIR / fetch_file
    if not src.exists():
        print(f"SKIP {output}: missing {fetch_file}")
        return
    print(f"Building {output}...")
    html = src.read_text(encoding="utf-8", errors="replace")
    title = extract_title(html, title)
    main = extract_main(html)
    prefix = rel_prefix(output)
    main = rewrite_urls(main, prefix)
    if output == "contact.html":
        main = re.sub(
            r'<div class="form-wrapper"[^>]*>\s*</div>',
            f'<div class="form-wrapper">{CONTACT_FORM_HTML}</div>',
            main,
            count=1,
        )
    page = render_shell(title, description, main, output, active)
    dest = ROOT / output
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding="utf-8")


def main() -> None:
    ASSETS_IMG.mkdir(parents=True, exist_ok=True)
    for out, fetch, active, title, desc in PAGES:
        build_page(out, fetch, active, title, desc)

    for out, fetch, active in COLLAB_PAGES:
        src = FETCH_DIR / fetch
        if not src.exists():
            continue
        html = src.read_text(encoding="utf-8", errors="replace")
        title = extract_title(html, "Collaboration — Kristina Vilyams")
        build_page(out, fetch, active, title, "Collaboration project.")

    print("Done.")


if __name__ == "__main__":
    main()
