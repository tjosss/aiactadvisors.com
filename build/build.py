#!/usr/bin/env python3
"""AI Act Advisors — Static Site Generator
Reads consultants.json and generates all HTML pages."""

import json, os, re, shutil
from datetime import datetime, timedelta
from html import escape

BASE = '/sessions/kind-vigilant-meitner/mnt/aiactadvisors.com'
BUILD = os.path.join(BASE, 'build')
STATIC = os.path.join(BASE, 'static')
DATA = os.path.join(BASE, 'consultants.json')

with open(DATA) as f:
    consultants = json.load(f)

# ── Deadline countdown ──
deadline = datetime(2026, 8, 2)
days_left = (deadline - datetime.now()).days

# ── Helpers ──
FLAGS = {
    'United Kingdom': '🇬🇧', 'Germany': '🇩🇪', 'France': '🇫🇷',
    'Spain': '🇪🇸', 'Netherlands': '🇳🇱', 'United States': '🇺🇸',
    'Switzerland': '🇨🇭', 'Belgium': '🇧🇪', 'Poland': '🇵🇱',
    'Finland': '🇫🇮', 'Sweden': '🇸🇪', 'Ireland': '🇮🇪',
    'Norway': '🇳🇴', 'Luxembourg': '🇱🇺', 'Greece': '🇬🇷',
    'Italy': '🇮🇹', 'Austria': '🇦🇹', 'Denmark': '🇩🇰',
    'Portugal': '🇵🇹', 'Czech Republic': '🇨🇿',
}

def flag(country):
    return FLAGS.get(country, '🇪🇺')

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def country_counts():
    cc = {}
    for c in consultants:
        cc[c['country']] = cc.get(c['country'], 0) + 1
    return dict(sorted(cc.items(), key=lambda x: -x[1]))

def sector_counts():
    sc = {}
    for c in consultants:
        for s in c['sectors']:
            if s != 'All Sectors':
                sc[s] = sc.get(s, 0) + 1
    return dict(sorted(sc.items(), key=lambda x: -x[1]))

def city_counts():
    cc = {}
    for c in consultants:
        key = (c['city'], c['country'])
        cc[key] = cc.get(key, 0) + 1
    return dict(sorted(cc.items(), key=lambda x: -x[1]))

def svg_pin():
    return '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>'

def svg_globe():
    return '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'

def svg_link():
    return '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'

def svg_check():
    return '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>'

# ── Layout ──
def header():
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RRHZE8N0GW"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-RRHZE8N0GW');
</script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="google-site-verification" content="lz-CmQYG7LZE-G7RL7IPztnLW2yL4FKL-g5lXHoplgA" />
<meta name="description" content="{{meta_desc}}">
<title>{{title}} | AI Act Advisors</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{css_path}}static/css/style.css">
<link rel="icon" href="{{css_path}}static/images/favicon.svg" type="image/svg+xml">
</head>
<body>
<div class="urgency-bar">
  <strong><span id="countdown"></span> days</strong> until EU AI Act high-risk deadline (August 2026) — Find your compliance consultant now
</div>
<script>document.getElementById('countdown').textContent=Math.max(0,Math.ceil((new Date('2026-08-02T00:00:00')-new Date())/(1000*60*60*24)));</script>
<header class="site-header">
  <div class="header-inner">
    <a href="{{css_path}}index.html" class="site-logo">AI Act <span>Advisors</span></a>
    <button class="mobile-toggle" onclick="document.querySelector('.main-nav').classList.toggle('open')" aria-label="Menu">&#9776;</button>
    <nav class="main-nav">
      <a href="{{css_path}}consultants.html">All Consultants</a>
      <a href="{{css_path}}countries.html">By Country</a>
      <a href="{{css_path}}sectors.html">By Sector</a>
      <a href="{{css_path}}blog.html">Resources</a>
      <a href="{{css_path}}products.html">Free Tools</a>
      <a href="{{css_path}}list-your-practice.html" class="nav-cta">List Your Practice</a>
    </nav>
  </div>
</header>'''

def footer():
    return '''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <h4>AI Act Advisors</h4>
        <p class="footer-about">Europe\'s directory for EU AI Act compliance consultants, ethics advisors, and governance experts. Find, compare, and contact the right expert for your organisation.</p>
      </div>
      <div>
        <h4>Directory</h4>
        <a href="{css_path}consultants.html">All Consultants</a>
        <a href="{css_path}countries.html">Browse by Country</a>
        <a href="{css_path}sectors.html">Browse by Sector</a>
      </div>
      <div>
        <h4>Resources</h4>
        <a href="{css_path}blog.html">Blog</a>
        <a href="{css_path}about.html">About Us</a>
        <a href="{css_path}list-your-practice.html">List Your Practice</a>
      </div>
      <div>
        <h4>Legal</h4>
        <a href="{css_path}privacy.html">Privacy Policy</a>
        <a href="{css_path}terms.html">Terms of Use</a>
        <a href="{css_path}disclaimer.html">Disclaimer</a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 AI Act Advisors. All rights reserved.</p>
      <p class="footer-disclaimer">AI Act Advisors is an independent directory service. Listings are informational only and do not constitute endorsement. Verify consultant qualifications independently. This site does not provide legal advice. For legal guidance, consult a qualified professional.</p>
    </div>
  </div>
</footer>
<div id="cookie-banner" style="display:none;position:fixed;bottom:0;left:0;right:0;background:#1f2937;color:#e5e7eb;padding:1rem 1.5rem;z-index:999;font-size:0.85rem;box-shadow:0 -2px 10px rgba(0,0,0,0.15)">
  <div style="max-width:1140px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem">
    <p style="margin:0;flex:1">We use cookies for analytics only (Google Analytics 4 with anonymised IPs). No marketing cookies. <a href="{css_path}privacy.html" style="color:#D79922">Privacy Policy</a></p>
    <div style="display:flex;gap:0.5rem">
      <button onclick="acceptCookies()" style="background:#4056A1;color:#fff;border:none;padding:0.4rem 1rem;border-radius:8px;font-weight:600;cursor:pointer;font-size:0.85rem">Accept</button>
      <button onclick="declineCookies()" style="background:transparent;color:#9ca3af;border:1px solid #4b5563;padding:0.4rem 1rem;border-radius:8px;cursor:pointer;font-size:0.85rem">Decline</button>
    </div>
  </div>
</div>
<script>
if(!localStorage.getItem('cookie-consent')){document.getElementById('cookie-banner').style.display='block'}
function acceptCookies(){localStorage.setItem('cookie-consent','accepted');document.getElementById('cookie-banner').style.display='none'}
function declineCookies(){localStorage.setItem('cookie-consent','declined');document.getElementById('cookie-banner').style.display='none'}
</script>
<script src="{css_path}static/js/main.js"></script>
<script>
document.addEventListener('DOMContentLoaded',function(){
  document.querySelectorAll('.listing-card a, a[href*="consultant/"]').forEach(function(a){
    a.addEventListener('click',function(){
      var name=this.textContent.trim();
      var href=this.getAttribute('href')||'';
      var id=href.split('/').pop().replace('.html','');
      if(typeof gtag==='function'){
        gtag('event','consultant_click',{consultant_name:name,consultant_id:id,page_location:window.location.pathname});
      }
    });
  });
  document.querySelectorAll('.country-card').forEach(function(a){
    a.addEventListener('click',function(){
      var name=this.querySelector('.name');
      if(name&&typeof gtag==='function'){
        gtag('event','country_click',{country_name:name.textContent.trim(),page_location:window.location.pathname});
      }
    });
  });
  document.querySelectorAll('a[href*="list-your-practice"]').forEach(function(a){
    a.addEventListener('click',function(){
      if(typeof gtag==='function'){
        gtag('event','cta_click',{cta_type:'list_practice',page_location:window.location.pathname});
      }
    });
  });
});
</script>
</body>
</html>'''

def page(title, meta_desc, body_html, css_path=''):
    h = header().replace('{title}', escape(title)).replace('{meta_desc}', escape(meta_desc)).replace('{css_path}', css_path).replace('{{title}}', escape(title)).replace('{{meta_desc}}', escape(meta_desc)).replace('{{css_path}}', css_path)
    f = footer().replace('{css_path}', css_path)
    return h + body_html + f

def write_page(path, content):
    full = os.path.join(BUILD, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content)

def consultant_card(c, css_path=''):
    badge = ''
    if c['verificationLevel'] == 'basic-verified':
        badge = f'<span class="badge badge-verified">{svg_check()} Verified</span>'
    elif c['verificationLevel'] == 'premium':
        badge = '<span class="badge badge-premium">★ Premium</span>'

    size_badge = ''
    if c['companySize'] == 'enterprise':
        size_badge = '<span class="badge badge-enterprise">Enterprise</span>'
    elif c['companySize'] == 'boutique':
        size_badge = '<span class="badge badge-boutique">Boutique</span>'

    tags = ''.join(f'<span class="card-tag">{escape(s)}</span>' for s in c['services'][:4])

    return f'''<div class="listing-card" data-country="{escape(c['country'])}" data-city="{escape(c['city'])}" data-size="{c['companySize']}" data-services="{','.join(c['services'])}" data-sectors="{','.join(c['sectors'])}">
  <div class="card-header">
    <h3><a href="{css_path}consultant/{c['id']}.html">{escape(c['name'])}</a></h3>
    <div>{badge} {size_badge}</div>
  </div>
  <div class="card-location">{svg_pin()} {escape(c['city'])}, {escape(c['country'])}</div>
  <p class="card-desc">{escape(c['description'])}</p>
  <div class="card-tags">{tags}</div>
  <div class="card-footer">
    <a href="{css_path}consultant/{c['id']}.html">View Profile →</a>
    <a href="{escape(c['website'])}" target="_blank" rel="noopener">{svg_link()} Website</a>
  </div>
</div>'''

# ── Schema markup ──
def schema_consultant(c):
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "{escape(c['name'])}",
  "description": "{escape(c['description'])}",
  "url": "{escape(c['website'])}",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "{escape(c['city'])}",
    "addressCountry": "{escape(c['country'])}"
  }},
  "areaServed": "Europe",
  "serviceType": {json.dumps(c['services'])}
}}
</script>'''

# ═══════════════════════════════════════════════
# BUILD PAGES
# ═══════════════════════════════════════════════

if os.path.exists(BUILD):
    shutil.rmtree(BUILD)
os.makedirs(BUILD)

# Copy static assets
if os.path.exists(STATIC):
    shutil.copytree(STATIC, os.path.join(BUILD, 'static'))

# ── Homepage ──
cc = country_counts()
sc = sector_counts()
top_consultants = consultants[:12]

country_cards = ''
for country, count in list(cc.items())[:8]:
    country_cards += f'<a href="country/{slug(country)}.html" class="country-card"><span class="flag">{flag(country)}</span><div class="count">{count}</div><div class="name">{escape(country)}</div></a>'

featured_cards = ''.join(consultant_card(c) for c in top_consultants)

homepage_body = f'''
<section class="hero">
  <div class="container">
    <h1>Find Your <em>EU AI Act</em><br>Compliance Consultant</h1>
    <p>Europe's directory of verified AI Act compliance consultants, ethics advisors, and governance experts. Compare specialists and get the help you need before the deadline.</p>
    <div class="hero-stats">
      <div class="hero-stat"><span class="num">{len(consultants)}</span><span class="label">Consultants Listed</span></div>
      <div class="hero-stat"><span class="num">{len(cc)}</span><span class="label">Countries Covered</span></div>
      <div class="hero-stat"><span class="num">{days_left}</span><span class="label">Days to Deadline</span></div>
    </div>
  </div>
</section>

<section class="search-section">
  <div class="container">
    <div class="filter-bar">
      <select id="filter-country"><option value="">All Countries</option>{''.join(f'<option value="{escape(c)}">{escape(c)} ({n})</option>' for c,n in cc.items())}</select>
      <select id="filter-sector"><option value="">All Sectors</option>{''.join(f'<option value="{escape(s)}">{escape(s)} ({n})</option>' for s,n in sc.items())}</select>
      <select id="filter-size"><option value="">All Sizes</option><option value="boutique">Boutique</option><option value="mid-size">Mid-size</option><option value="enterprise">Enterprise</option></select>
      <button class="btn btn-primary" onclick="applyFilters()">Search</button>
    </div>
  </div>
</section>

<section class="container">
  <div class="section-heading">
    <h2>Browse by Country</h2>
    <p>Find AI Act compliance consultants across Europe</p>
  </div>
  <div class="country-grid">{country_cards}</div>
</section>

<section class="container">
  <div class="section-heading">
    <h2>Featured Consultants</h2>
    <p>Verified EU AI Act compliance experts</p>
  </div>
  <div class="results-info">Showing <strong>{len(top_consultants)}</strong> of {len(consultants)} consultants</div>
  <div class="listings-grid" id="listings">{featured_cards}</div>
  <div style="text-align:center;padding:1.5rem 0"><a href="consultants.html" class="btn btn-primary">View All {len(consultants)} Consultants →</a></div>
</section>
'''

write_page('index.html', page('Find EU AI Act Compliance Consultants', f'Europe\'s directory of {len(consultants)} verified EU AI Act compliance consultants across {len(cc)} countries. Compare and contact AI governance experts before the August 2026 deadline.', homepage_body))

# ── All Consultants Page ──
all_cards = ''.join(consultant_card(c) for c in consultants)
consultants_body = f'''
<section class="landing-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="index.html">Home</a> <span>›</span> All Consultants</div>
    <h1>All EU AI Act Consultants</h1>
    <p>{len(consultants)} verified compliance consultants across {len(cc)} countries</p>
  </div>
</section>
<section class="search-section">
  <div class="container">
    <div class="filter-bar">
      <input type="text" id="search-text" placeholder="Search by name or keyword...">
      <select id="filter-country"><option value="">All Countries</option>{''.join(f'<option value="{escape(c)}">{escape(c)} ({n})</option>' for c,n in cc.items())}</select>
      <select id="filter-sector"><option value="">All Sectors</option>{''.join(f'<option value="{escape(s)}">{escape(s)} ({n})</option>' for s,n in sc.items())}</select>
      <select id="filter-size"><option value="">All Sizes</option><option value="boutique">Boutique</option><option value="mid-size">Mid-size</option><option value="enterprise">Enterprise</option></select>
      <button class="btn btn-primary" onclick="applyFilters()">Search</button>
      <button class="btn btn-secondary" onclick="clearFilters()">Clear</button>
    </div>
  </div>
</section>
<section class="container">
  <div class="results-info">Showing <strong id="results-count">{len(consultants)}</strong> consultants</div>
  <div class="listings-grid" id="listings">{all_cards}</div>
  <div class="no-results" id="no-results" style="display:none">
    <h3>No consultants found</h3>
    <p>Try adjusting your filters or <a href="list-your-practice.html">suggest a consultant</a>.</p>
  </div>
</section>
'''
write_page('consultants.html', page('All EU AI Act Consultants', f'Browse {len(consultants)} verified EU AI Act compliance consultants. Filter by country, sector, and company size.', consultants_body))

# ── Individual Consultant Profiles ──
for c in consultants:
    services_html = ''.join(f'<li>{escape(s)}</li>' for s in c['services'])
    sectors_html = ''.join(f'<li>{escape(s)}</li>' for s in c['sectors'])
    langs_html = ', '.join(c['languages'])

    badge = ''
    if c['verificationLevel'] == 'basic-verified':
        badge = f'<span class="badge badge-verified">{svg_check()} Verified</span>'

    links = f'<div class="sidebar-item">{svg_globe()} <a href="{escape(c["website"])}" target="_blank" rel="noopener">{escape(c["website"])}</a></div>'
    if c.get('linkedin'):
        links += f'<div class="sidebar-item">{svg_link()} <a href="{escape(c["linkedin"])}" target="_blank" rel="noopener">LinkedIn</a></div>'

    profile_body = f'''
{schema_consultant(c)}
<section class="profile-hero">
  <div class="container">
    <div class="breadcrumbs" style="color:rgba(255,255,255,0.5)"><a href="../index.html" style="color:rgba(255,255,255,0.6)">Home</a> <span>›</span> <a href="../consultants.html" style="color:rgba(255,255,255,0.6)">Consultants</a> <span>›</span> {escape(c['name'])}</div>
    <h1>{escape(c['name'])} {badge}</h1>
    <div class="profile-meta">
      <span>{svg_pin()} {escape(c['city'])}, {escape(c['country'])}</span>
      <span>{escape(c['companySize'].title())}</span>
      <span>{escape(c['priceRange'])}</span>
    </div>
  </div>
</section>
<section class="profile-content">
  <div class="container">
    <div class="profile-grid">
      <div class="profile-main">
        <h2>About {escape(c['name'])}</h2>
        <p>{escape(c['description'])}</p>

        <h2>Services</h2>
        <ul class="service-list">{services_html}</ul>

        <h2>Sectors Served</h2>
        <ul class="service-list">{sectors_html}</ul>

        <h2>Languages</h2>
        <p>{escape(langs_html)}</p>

        <p style="margin-top:2rem;font-size:0.82rem;color:var(--gray-400)">This listing is based on publicly available information. If you represent this company and wish to update or remove this listing, contact info@aiactadvisors.com.</p>
      </div>
      <div class="profile-sidebar">
        <div class="sidebar-card">
          <h3>Contact Details</h3>
          {links}
        </div>
        <div class="sidebar-card">
          <h3>Request a Consultation</h3>
          <form class="contact-form" name="inquiry-{c['id']}" method="POST" data-netlify="true" netlify-honeypot="bot-field">
            <input type="hidden" name="consultant" value="{escape(c['name'])}">
            <p style="display:none"><label>Don't fill this out: <input name="bot-field"></label></p>
            <label>Your Name</label><input type="text" name="name" required>
            <label>Your Email</label><input type="email" name="email" required>
            <label>Company</label><input type="text" name="company">
            <label>Message</label><textarea name="message" placeholder="Describe your AI Act compliance needs..."></textarea>
            <label class="consent-label"><input type="checkbox" required> I consent to my inquiry being forwarded to {escape(c['name'])}. See our <a href="../privacy.html">Privacy Policy</a>.</label>
            <button type="submit" class="btn btn-primary" style="width:100%">Send Inquiry</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</section>
'''
    write_page(f'consultant/{c["id"]}.html', page(f'{c["name"]} — EU AI Act Consultant', f'{c["name"]} provides EU AI Act compliance consulting in {c["city"]}, {c["country"]}. {c["description"][:150]}', profile_body, css_path='../'))

# ── Country Pages ──
for country, count in cc.items():
    country_consultants = [c for c in consultants if c['country'] == country]
    cards = ''.join(consultant_card(c, '../') for c in country_consultants)

    body = f'''
<section class="landing-hero">
  <div class="container">
    <div class="breadcrumbs" style="color:rgba(255,255,255,0.5)"><a href="../index.html" style="color:rgba(255,255,255,0.6)">Home</a> <span>›</span> <a href="../countries.html" style="color:rgba(255,255,255,0.6)">Countries</a> <span>›</span> {escape(country)}</div>
    <h1>AI Act Consultants in {escape(country)}</h1>
    <p>{count} verified EU AI Act compliance consultants based in {escape(country)}. Find the right expert for your organisation.</p>
  </div>
</section>
<section class="container">
  <div class="results-info">Showing <strong>{count}</strong> consultants in {escape(country)}</div>
  <div class="listings-grid">{cards}</div>
</section>
'''
    write_page(f'country/{slug(country)}.html', page(f'AI Act Consultants in {country}', f'Find {count} verified EU AI Act compliance consultants in {country}. Compare AI governance experts and request consultations.', body, '../'))

# ── Countries Index ──
all_country_cards = ''
for country, count in cc.items():
    all_country_cards += f'<a href="country/{slug(country)}.html" class="country-card"><span class="flag">{flag(country)}</span><div class="count">{count}</div><div class="name">{escape(country)}</div></a>'

countries_index = f'''
<section class="landing-hero">
  <div class="container">
    <div class="breadcrumbs" style="color:rgba(255,255,255,0.5)"><a href="index.html" style="color:rgba(255,255,255,0.6)">Home</a> <span>›</span> Countries</div>
    <h1>AI Act Consultants by Country</h1>
    <p>Browse {len(consultants)} consultants across {len(cc)} countries</p>
  </div>
</section>
<section class="container">
  <div class="country-grid" style="padding:2rem 0">{all_country_cards}</div>
</section>
'''
write_page('countries.html', page('AI Act Consultants by Country', f'Find EU AI Act compliance consultants in {len(cc)} European countries. Browse by location to find local experts.', countries_index))

# ── Sector Pages ──
for sector, count in sc.items():
    sector_consultants = [c for c in consultants if sector in c['sectors']]
    cards = ''.join(consultant_card(c, '../') for c in sector_consultants)

    body = f'''
<section class="landing-hero">
  <div class="container">
    <div class="breadcrumbs" style="color:rgba(255,255,255,0.5)"><a href="../index.html" style="color:rgba(255,255,255,0.6)">Home</a> <span>›</span> <a href="../sectors.html" style="color:rgba(255,255,255,0.6)">Sectors</a> <span>›</span> {escape(sector)}</div>
    <h1>AI Act Compliance for {escape(sector)}</h1>
    <p>{len(sector_consultants)} consultants specialising in EU AI Act compliance for the {escape(sector.lower())} sector.</p>
  </div>
</section>
<section class="container">
  <div class="results-info">Showing <strong>{len(sector_consultants)}</strong> consultants for {escape(sector)}</div>
  <div class="listings-grid">{cards}</div>
</section>
'''
    write_page(f'sector/{slug(sector)}.html', page(f'AI Act Compliance for {sector}', f'Find EU AI Act compliance consultants specialising in {sector}. {len(sector_consultants)} verified experts for your sector.', body, '../'))

# ── Sectors Index ──
sector_cards = ''
for sector, count in sc.items():
    sector_cards += f'<a href="sector/{slug(sector)}.html" class="country-card"><div class="count">{count}</div><div class="name">{escape(sector)}</div></a>'

sectors_index = f'''
<section class="landing-hero">
  <div class="container">
    <div class="breadcrumbs" style="color:rgba(255,255,255,0.5)"><a href="index.html" style="color:rgba(255,255,255,0.6)">Home</a> <span>›</span> Sectors</div>
    <h1>AI Act Compliance by Sector</h1>
    <p>Find consultants specialising in your industry</p>
  </div>
</section>
<section class="container">
  <div class="country-grid" style="padding:2rem 0">{sector_cards}</div>
</section>
'''
write_page('sectors.html', page('AI Act Compliance by Sector', 'Find EU AI Act compliance consultants by industry sector. Healthcare, financial services, manufacturing, and more.', sectors_index))

# ── City Pages ──
for (city, country), count in city_counts().items():
    city_consultants = [c for c in consultants if c['city'] == city and c['country'] == country]
    cards = ''.join(consultant_card(c, '../') for c in city_consultants)
    body = f'''
<section class="landing-hero">
  <div class="container">
    <div class="breadcrumbs" style="color:rgba(255,255,255,0.5)"><a href="../index.html" style="color:rgba(255,255,255,0.6)">Home</a> <span>›</span> <a href="../country/{slug(country)}.html" style="color:rgba(255,255,255,0.6)">{escape(country)}</a> <span>›</span> {escape(city)}</div>
    <h1>AI Act Consultants in {escape(city)}</h1>
    <p>{count} EU AI Act compliance consultants based in {escape(city)}, {escape(country)}.</p>
  </div>
</section>
<section class="container">
  <div class="listings-grid">{cards}</div>
</section>
'''
    write_page(f'city/{slug(city)}.html', page(f'AI Act Consultants in {city}', f'Find {count} EU AI Act compliance consultants in {city}, {country}.', body, '../'))

# ── Static Pages ──
# About
about_body = '''
<div class="static-page">
  <h1>About AI Act Advisors</h1>
  <p>AI Act Advisors is Europe's dedicated directory for finding EU AI Act compliance consultants, ethics advisors, and governance experts.</p>
  <h2>Why We Exist</h2>
  <p>The EU AI Act introduces sweeping compliance requirements for businesses deploying AI systems across Europe. With the high-risk systems deadline approaching in August 2026, thousands of companies need expert help — but finding the right consultant means clicking through dozens of individual firm websites with no way to compare.</p>
  <p>AI Act Advisors solves this by aggregating verified consultants into one searchable, filterable directory. Think of us as the comparison platform that connects businesses with the compliance expertise they need.</p>
  <h2>How Listings Work</h2>
  <p>We research and verify consultants from publicly available sources including firm websites, professional directories, and EU Commission expert groups. Every listing is checked to confirm the firm actively offers AI Act compliance services.</p>
  <p>Consultants can claim and enhance their free listing at any time. We also offer premium placement for firms seeking greater visibility.</p>
  <h2>Contact</h2>
  <p>For questions, corrections, or partnership inquiries: <strong>info@aiactadvisors.com</strong></p>
</div>
'''
write_page('about.html', page('About AI Act Advisors', 'About AI Act Advisors — Europe\'s directory for EU AI Act compliance consultants.', about_body))

# Privacy Policy
privacy_body = '''
<div class="static-page">
  <h1>Privacy Policy</h1>
  <p><em>Last updated: February 2026</em></p>
  <h2>Who We Are</h2>
  <p>AI Act Advisors ("we", "us") operates aiactadvisors.com, a directory of EU AI Act compliance consultants.</p>
  <h2>Data We Collect</h2>
  <p><strong>Visitor data:</strong> We use Google Analytics 4 with anonymised IP addresses to understand how visitors use our site. Analytics only run after you consent via our cookie banner.</p>
  <p><strong>Inquiry form data:</strong> When you submit a consultation request, we collect your name, email, company name, and message. This data is shared only with the consultant(s) you select.</p>
  <p><strong>Consultant data:</strong> We publish business information about compliance consultants based on publicly available data (legitimate interest) or information they submit directly (consent).</p>
  <h2>Lawful Basis</h2>
  <p>Visitor analytics: consent. Inquiry forms: consent (checkbox required). Consultant listings: legitimate interest for publicly available business data; consent for self-submitted data.</p>
  <h2>Your Rights</h2>
  <p>Under GDPR, you have the right to access, correct, delete, restrict, or port your data. Contact us at info@aiactadvisors.com and we will respond within 30 days.</p>
  <h2>Right to Be Forgotten</h2>
  <p>If a consultant requests removal of their listing, we will delete it within 72 hours.</p>
  <h2>Cookies</h2>
  <p>We use a cookie consent banner. Analytics cookies are only set after you accept. No marketing or third-party tracking cookies are used.</p>
  <h2>Contact</h2>
  <p>For data requests: <strong>info@aiactadvisors.com</strong></p>
</div>
'''
write_page('privacy.html', page('Privacy Policy', 'AI Act Advisors privacy policy. How we collect, use, and protect your data under GDPR.', privacy_body))

# Terms
terms_body = '''
<div class="static-page">
  <h1>Terms of Use</h1>
  <p><em>Last updated: February 2026</em></p>
  <h2>Acceptance</h2>
  <p>By using aiactadvisors.com, you agree to these terms.</p>
  <h2>Directory Purpose</h2>
  <p>AI Act Advisors is an informational directory. We aggregate publicly available information about EU AI Act compliance consultants to help businesses find appropriate expertise.</p>
  <h2>No Legal Advice</h2>
  <p>Nothing on this site constitutes legal advice. The directory is for informational purposes only. For legal guidance on AI Act compliance, consult a qualified professional.</p>
  <h2>No Endorsement</h2>
  <p>Listing a consultant on our directory does not constitute endorsement of their services, qualifications, or competence. Users are responsible for independently verifying consultant credentials before engagement.</p>
  <h2>Accuracy</h2>
  <p>We make reasonable efforts to ensure listing accuracy but cannot guarantee all information is current or complete. Listings are based on publicly available information and self-reported data.</p>
  <h2>Limitation of Liability</h2>
  <p>AI Act Advisors shall not be liable for any damages arising from the use of this directory, reliance on listing information, or engagement with listed consultants.</p>
  <h2>Contact</h2>
  <p>Questions about these terms: <strong>info@aiactadvisors.com</strong></p>
</div>
'''
write_page('terms.html', page('Terms of Use', 'AI Act Advisors terms of use.', terms_body))

# Disclaimer
disclaimer_body = '''
<div class="static-page">
  <h1>Disclaimer</h1>
  <p>AI Act Advisors is an independent directory service. Listings are informational only and do not constitute endorsement of any consultant, firm, or service.</p>
  <p>Verify consultant qualifications independently before making any engagement decisions. This site does not provide legal advice. For legal guidance on EU AI Act compliance, consult a qualified professional.</p>
  <p>Listing information is based on publicly available sources and self-reported data. We make reasonable efforts to verify accuracy but cannot guarantee completeness or currency of all information.</p>
  <p>If you represent a listed company and wish to update or remove your listing, contact <strong>info@aiactadvisors.com</strong>.</p>
</div>
'''
write_page('disclaimer.html', page('Disclaimer', 'AI Act Advisors disclaimer. Listings are informational only.', disclaimer_body))

# List Your Practice
list_body = '''
<div class="static-page">
  <h1>List Your Practice</h1>
  <p>Are you an EU AI Act compliance consultant, ethics advisor, or governance expert? Get listed in Europe's dedicated AI Act consultant directory — <strong>free</strong>.</p>
  <h2>Why List With Us</h2>
  <p>Businesses across Europe are searching for AI Act compliance help. Our directory connects them directly with qualified consultants like you. Listings are free and include your company profile, services, sectors, and contact information.</p>
  <h2>Submit Your Listing</h2>
  <form class="contact-form" name="listing-submission" method="POST" action="/list-your-practice.html" data-netlify="true" netlify-honeypot="bot-field" style="max-width:600px">
    <input type="hidden" name="form-name" value="listing-submission">
    <p style="display:none"><label>Don't fill this out: <input name="bot-field"></label></p>
    <label>Company Name *</label><input type="text" name="company" required>
    <label>Website URL *</label><input type="url" name="website" required placeholder="https://">
    <label>Country *</label><input type="text" name="country" required>
    <label>City *</label><input type="text" name="city" required>
    <label>Contact Email *</label><input type="email" name="email" required>
    <label>Primary Services (select all that apply)</label>
    <textarea name="services" placeholder="AI Act Compliance, Risk Assessment, AI Governance, ISO 42001, etc."></textarea>
    <label>Sectors Served</label>
    <textarea name="sectors" placeholder="Healthcare, Financial Services, Manufacturing, etc."></textarea>
    <label>Languages</label><input type="text" name="languages" placeholder="English, German, French...">
    <label>Company Size</label>
    <select name="company_size"><option value="">Select...</option><option>Solo</option><option>Boutique (2-20)</option><option>Mid-size (21-200)</option><option>Enterprise (200+)</option></select>
    <label>Description of AI Act Services (100-500 words) *</label>
    <textarea name="description" required style="min-height:150px" placeholder="Describe your EU AI Act compliance services, approach, and key differentiators..."></textarea>
    <label>LinkedIn URL</label><input type="url" name="linkedin" placeholder="https://linkedin.com/company/...">
    <label class="consent-label"><input type="checkbox" required> I confirm this information is accurate and I authorise AI Act Advisors to publish this listing.</label>
    <button type="submit" class="btn btn-primary" style="width:100%">Submit Listing for Review</button>
  </form>
  <p style="margin-top:1rem;font-size:0.85rem;color:var(--gray-500)">Submissions are reviewed within 48 hours. We verify that your website is active and explicitly mentions AI Act services.</p>
</div>
'''
write_page('list-your-practice.html', page('List Your Practice — Free Consultant Listing', 'Get your AI Act compliance practice listed in Europe\'s dedicated consultant directory. Free listings available.', list_body))

# Blog index
blog_body = '''
<div class="static-page">
  <h1>AI Act Resources</h1>
  <p>Guides, analysis, and updates on EU AI Act compliance.</p>
  <div class="blog-list">
    <div class="blog-card">
      <h2><a href="blog/eu-ai-act-compliance-guide-smes.html">EU AI Act Compliance Guide for SMEs</a></h2>
      <p class="meta">February 2026</p>
      <p>A practical guide for small and medium enterprises navigating EU AI Act compliance requirements, risk classification, and next steps.</p>
    </div>
  </div>
</div>
'''
write_page('blog.html', page('AI Act Resources & Blog', 'Guides and analysis on EU AI Act compliance. Practical resources for businesses navigating AI regulation.', blog_body))

# Sample blog post
blog_post = '''
<article class="blog-post">
  <div class="breadcrumbs"><a href="../index.html">Home</a> <span>›</span> <a href="../blog.html">Blog</a> <span>›</span> Compliance Guide for SMEs</div>
  <h1>EU AI Act Compliance Guide for SMEs</h1>
  <p class="meta">February 2026 · 8 min read</p>

  <p>The EU AI Act is the world's first comprehensive AI regulation, and its requirements are rapidly coming into force. For small and medium enterprises, understanding your obligations is critical — penalties can reach up to €35 million or 7% of global annual turnover.</p>

  <h2>Key Deadlines You Need to Know</h2>
  <p>The AI Act follows a phased rollout. Prohibited AI practices have been enforceable since February 2025. GPAI model transparency requirements became mandatory in August 2025. The most significant deadline — full compliance for high-risk AI systems — arrives in <strong>August 2026</strong>.</p>
  <p>Given that compliance typically takes 8-14 months, companies starting now are already working against a tight timeline.</p>

  <h2>Is Your AI System High-Risk?</h2>
  <p>The AI Act classifies AI systems into risk tiers. High-risk systems — those used in areas like employment decisions, credit scoring, healthcare diagnostics, or biometric identification — face the strictest requirements including conformity assessments, risk management systems, and ongoing monitoring.</p>
  <p>If your product or service uses AI in any of the areas listed in Annex III of the regulation, you likely need to prepare for high-risk compliance.</p>

  <h2>What Compliance Looks Like</h2>
  <p>For high-risk systems, compliance involves establishing a risk management system, implementing data governance practices, maintaining technical documentation, enabling human oversight, and ensuring accuracy and robustness. You will also need to register your system in the EU database.</p>

  <h2>Getting Expert Help</h2>
  <p>Most SMEs do not have in-house expertise for AI Act compliance. Working with a qualified consultant can help you classify your systems, identify gaps, and build a compliance roadmap within your budget.</p>
  <p><a href="../consultants.html" class="btn btn-primary">Find an AI Act Consultant →</a></p>
</article>
'''
write_page('blog/eu-ai-act-compliance-guide-smes.html', page('EU AI Act Compliance Guide for SMEs', 'Practical guide for SMEs navigating EU AI Act compliance. Key deadlines, risk classification, and how to get expert help.', blog_post, '../'))

# Blog post 2: Penalties
blog_post_2 = '''
<article class="blog-post">
  <div class="breadcrumbs"><a href="../index.html">Home</a> <span>›</span> <a href="../blog.html">Blog</a> <span>›</span> AI Act Penalties</div>
  <h1>EU AI Act Penalties: What Your Company Faces in 2026</h1>
  <p class="meta">February 2026 · 6 min read</p>

  <p>The EU AI Act introduces some of the most severe penalties in European regulatory history. Understanding the fine structure is essential for any organisation deploying AI systems that interact with EU markets.</p>

  <h2>Three Tiers of Penalties</h2>
  <p>The AI Act establishes a tiered penalty structure based on the severity of the violation. The highest fines apply to prohibited AI practices — systems that manipulate human behaviour, exploit vulnerabilities, or conduct untargeted facial recognition in public spaces. These carry penalties of up to <strong>€35 million or 7% of global annual turnover</strong>, whichever is higher.</p>
  <p>The second tier covers violations of high-risk AI system requirements, including failure to comply with risk management, data governance, transparency, or human oversight obligations. These attract fines of up to <strong>€15 million or 3% of global annual turnover</strong>.</p>
  <p>The third tier addresses providing incorrect or misleading information to authorities, with penalties of up to <strong>€7.5 million or 1% of global annual turnover</strong>.</p>

  <h2>Real Enforcement Is Already Happening</h2>
  <p>Enforcement is not theoretical. Italy fined OpenAI €15 million in early 2025 under existing data protection rules related to AI, and Finland became the first EU member state to activate full national AI Act supervision in January 2026. National authorities across all 27 member states must be operational by August 2025.</p>

  <h2>SME Considerations</h2>
  <p>The AI Act includes proportionality provisions for small and medium enterprises. Fines for SMEs are calculated on a sliding scale, and regulatory sandboxes allow smaller organisations to test compliance approaches. However, SME status does not exempt companies from compliance — it only affects the penalty calculation.</p>

  <h2>The Cost of Non-Compliance vs. Compliance</h2>
  <p>Compliance costs for SMEs typically range from €500K to €2M, while mid-size companies budget €2-5M and large enterprises €8-15M. These figures are substantial, but they pale in comparison to potential penalties of tens of millions of euros — not to mention reputational damage and loss of market access.</p>

  <h2>Next Steps</h2>
  <p>The most effective way to manage regulatory risk is to engage a qualified compliance consultant who understands your specific sector and risk profile. Early engagement reduces costs and provides time to implement changes before enforcement deadlines.</p>
  <p><a href="../consultants.html" class="btn btn-primary">Find an AI Act Consultant →</a></p>
</article>
'''
write_page('blog/eu-ai-act-penalties-2026.html', page('EU AI Act Penalties: What Your Company Faces in 2026', 'Understanding EU AI Act penalties and fines. Three tiers from €7.5M to €35M. What your company needs to know before 2026.', blog_post_2, '../'))

# Blog post 3: Hairdressers & Beauty Salons
blog_post_3 = '''
<article class="blog-post">
  <div class="breadcrumbs"><a href="../index.html">Home</a> <span>›</span> <a href="../blog.html">Blog</a> <span>›</span> AI Act for Hairdressers</div>
  <h1>Does the EU AI Act Apply to My Hair Salon?</h1>
  <p class="meta">February 2026 · 10 min read · <span style="background:var(--gold-light);color:var(--gray-800);padding:0.15rem 0.5rem;border-radius:4px;font-size:0.8rem;font-weight:600">Industry Use Case</span></p>

  <p>You run a hair salon. You cut hair, mix colour, and keep clients coming back. You are not a tech company. So why would EU artificial intelligence regulation have anything to do with you?</p>
  <p>The short answer: if you use modern booking software, a virtual receptionist, or any tool that makes automated decisions about your clients, you are already using AI. And the EU AI Act, which comes fully into force in August 2026, applies to businesses that <strong>deploy</strong> AI systems — not just those that build them.</p>
  <p>Here is what you actually need to know.</p>

  <h2>The AI You Are Probably Already Using</h2>
  <p>Most salon owners do not think of their booking software as "artificial intelligence." But the tools that power modern salons are increasingly AI-driven. Here are the most common ones:</p>

  <h3>Booking and Scheduling Software</h3>
  <p><strong>Fresha</strong>, used by over 100,000 salons worldwide, now includes AI-powered <a href="https://www.fresha.com/blog/Up-Next-2026" target="_blank">"smart bookings"</a> that automatically optimise your calendar by shortening gaps between appointments. Their <a href="https://www.prnewswire.com/news-releases/freshas-ai-powered-defense-reduces-fraud-by-99-302377652.html" target="_blank">AI fraud detection system</a> uses machine learning to reduce fraudulent bookings by 99 percent. In 2026, Fresha is rolling out an <a href="https://www.fresha.com/blog/Up-Next-2026" target="_blank">AI receptionist</a> that answers client questions and handles bookings outside your working hours.</p>
  <p><strong>Booksy</strong> was one of the first beauty platforms to integrate with <a href="https://biz.booksy.com/en-us/blog/booksy-google-ai-mode-integration" target="_blank">Google AI Mode</a>, allowing clients to say "find me a hair salon for highlights this Saturday afternoon" and have Google's AI automatically match them with your real-time availability and complete the booking. Booksy also uses <a href="https://getzowie.com/testimonials/booksy" target="_blank">Zowie AI to handle 70 percent of customer service enquiries</a> automatically.</p>
  <p>Other popular platforms like <strong>Vagaro</strong>, <strong>GlossGenius</strong>, <strong>Boulevard</strong>, and <strong>Zenoti</strong> all incorporate some form of AI for scheduling optimisation, client recommendations, or automated communications.</p>

  <h3>AI Receptionists and Phone Handling</h3>
  <p>A growing number of salons use AI phone answering services. Tools like <strong>BookingBee</strong>, <strong>My AI Front Desk</strong>, <strong>GoodCall</strong>, and <strong>Qlient.ai</strong> answer calls 24/7, understand service-specific questions, book appointments, and handle cancellations — without a human picking up the phone.</p>

  <h3>AI Hair Colour Technology</h3>
  <p>Fresha recently <a href="https://theindustry.beauty/fresha-invests-in-ai-powered-hair-colour-technology-company-yuv/" target="_blank">invested in Yuv</a>, an AI-powered hair colour technology company. Yuv allows salons to save personalised hair colour formulas in client profiles, ensuring consistency across visits. Other companies offer virtual try-on tools where clients can see how a colour or style would look before committing.</p>

  <h3>AI Marketing and Client Retention</h3>
  <p>Many salon platforms now include AI-powered marketing: automated email campaigns with personalised product recommendations, smart segmentation that targets clients who have not visited recently, and dynamic messaging that adjusts based on client behaviour.</p>

  <h2>What Risk Level Does This Put You In?</h2>
  <p>The EU AI Act uses a <a href="https://eur-lex.europa.eu/EN/legal-content/summary/rules-for-trustworthy-artificial-intelligence-in-the-eu.html" target="_blank">four-tier risk classification</a>: prohibited, high-risk, limited risk, and minimal risk. The classification depends on the intended purpose of the AI system and the potential impact on people's fundamental rights. Here is where typical salon AI falls:</p>

  <table style="width:100%;border-collapse:collapse;margin:1.5rem 0">
    <thead>
      <tr style="background:var(--blue);color:white">
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">AI Tool</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Risk Level</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Why</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Booking optimisation (Fresha smart bookings, Booksy scheduling)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Internal operational tool. Does not affect fundamental rights.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI receptionist / chatbot (BookingBee, GoodCall, Fresha AI receptionist)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Interacts directly with clients. Must disclose that they are communicating with AI.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI fraud detection (Fresha ML-based fraud prevention)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Internal security tool. No direct impact on individuals' rights.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI marketing personalisation (automated emails, client segmentation)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Product recommendations and marketing. Not profiling in the Annex III sense.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Virtual try-on / AI colour matching</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Cosmetic tool. No decision-making that affects rights.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Google AI Mode booking (via Booksy/Fresha)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI interacts with clients on your behalf. Transparency obligations apply.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI-powered staff scheduling or HR tools</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Potentially High</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">If AI makes decisions about staff work allocation, performance, or dismissal, it could fall under Annex III (employment).</td>
      </tr>
    </tbody>
  </table>

  <p><strong>The good news:</strong> most salon AI falls into the minimal or limited risk categories. You are not facing the same compliance burden as a bank using AI for credit scoring or a hospital using AI for diagnostics.</p>
  <p><strong>The important caveat:</strong> if you use any AI tool that interacts directly with clients — an AI receptionist, a chatbot, Google AI Mode booking — you have a transparency obligation. Your clients must know they are talking to AI, not a person.</p>

  <h2>What You Actually Need to Do</h2>

  <h3>1. Know What AI You Use</h3>
  <p>Make a simple list of every software tool in your salon. Check if it uses AI features (most will mention it in their marketing or settings). Common ones: Fresha, Booksy, Vagaro, GlossGenius, Boulevard, Zenoti, BookingBee, GoodCall, Timely.</p>

  <h3>2. Ensure AI Literacy (Required Since February 2025)</h3>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4 of the AI Act</a> requires that all staff and operators of AI systems have a sufficient level of AI literacy. For a salon, this means you and your team should understand the basics of how your AI tools work, what decisions they make, and what data they collect. This does not require a certification — a documented briefing or training session is sufficient.</p>

  <h3>3. Disclose AI Interactions to Clients</h3>
  <p>If your salon uses an AI receptionist, chatbot, or any AI that interacts with clients, you must clearly inform clients that they are communicating with an AI system. This can be as simple as:</p>
  <ul>
    <li>A message at the start of a chatbot conversation: "You are chatting with our AI assistant"</li>
    <li>A note on your website: "Phone calls may be answered by an AI receptionist"</li>
    <li>A disclosure in your booking confirmation: "This booking was processed by AI"</li>
  </ul>

  <h3>4. Review Your Data Practices</h3>
  <p>AI tools that personalise marketing or store client preferences (like hair colour formulas) use personal data. Ensure your privacy policy covers AI processing and that you have a lawful basis under GDPR. Most salon software providers handle this through their own terms, but you should check.</p>

  <h3>5. Check Your Software Providers</h3>
  <p>The heaviest compliance obligations under the AI Act fall on the <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-16" target="_blank">providers</a> (developers) of AI systems, not the <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26" target="_blank">deployers</a> (users like you). Fresha, Booksy, and similar platforms are responsible for conformity assessments and technical documentation. But you should confirm your providers are aware of and preparing for AI Act compliance — ask them directly.</p>

  <h2>Can You Handle This Yourself?</h2>
  <p>For most hair salons, <strong>yes</strong>. The steps above are straightforward and do not require a consultant. If your salon only uses booking software and basic marketing tools, your compliance burden is light: know what you use, train your team, disclose AI to clients, and keep your privacy policy updated.</p>
  <p>You would need professional help if:</p>
  <ul>
    <li>You use AI to make decisions about staff (scheduling based on performance, automated roster changes)</li>
    <li>You use biometric AI (facial recognition for client check-in)</li>
    <li>You develop your own AI tools (custom recommendation engines, bespoke apps)</li>
    <li>You are unsure whether your AI tools fall into a higher risk category</li>
  </ul>

  <h2>What "Compliant" Looks Like for a Salon</h2>
  <p>Picture this: you run a 6-chair salon using Fresha for bookings and BookingBee for after-hours phone handling. Here is what compliance looks like:</p>
  <ul>
    <li>You have a one-page document listing all AI tools you use, their purpose, and their risk level</li>
    <li>Your staff have had a 30-minute briefing on what AI the salon uses and how it works</li>
    <li>Your website has a note that phone calls may be handled by AI</li>
    <li>Your BookingBee greeting includes "Hi, you have reached [salon name]'s AI assistant"</li>
    <li>Your privacy policy mentions AI-powered booking and marketing</li>
    <li>You have emailed Fresha and BookingBee asking for confirmation of their AI Act compliance readiness</li>
  </ul>
  <p>For most salons, that covers it. You are not being asked to hire a compliance team or register in an EU database. The obligations for minimal and limited risk AI are proportionate — they are designed to be manageable for businesses of any size.</p>

  <h2>The Bottom Line</h2>
  <p>The EU AI Act does apply to your salon, but the requirements for the kind of AI most salons use are not onerous. The regulation is designed to be proportionate — a hair salon using Fresha is not treated the same as a hospital deploying diagnostic AI.</p>
  <p>What matters is awareness. Know what tools you use, understand what they do with your clients' data, make sure your team has a basic understanding, and be upfront with clients when AI is involved in their experience. That is a reasonable standard, and it is achievable without outside help for most salons.</p>
  <p>If you are unsure about any of it, or if your situation is more complex than what we have described here, it is worth speaking to someone who specialises in this area.</p>

  <div style="margin-top:2rem;padding:1.5rem;background:var(--blue-lighter);border-radius:8px;font-size:0.9rem;line-height:1.8">
    <p style="margin:0 0 0.75rem 0"><strong>Sources and further reading:</strong></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.fresha.com/blog/Up-Next-2026" target="_blank">Fresha 2026 feature roadmap</a> — AI receptionist, smart bookings, marketing AI</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.prnewswire.com/news-releases/freshas-ai-powered-defense-reduces-fraud-by-99-302377652.html" target="_blank">Fresha AI fraud prevention</a> — 99% fraud reduction claim (PR Newswire)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://theindustry.beauty/fresha-invests-in-ai-powered-hair-colour-technology-company-yuv/" target="_blank">Fresha invests in Yuv</a> — AI hair colour technology (TheIndustry.beauty)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://biz.booksy.com/en-us/blog/booksy-google-ai-mode-integration" target="_blank">Booksy Google AI Mode integration</a> — agentic booking (Booksy blog)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://getzowie.com/testimonials/booksy" target="_blank">Booksy + Zowie AI</a> — 70% automated customer service (Zowie case study)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://bookingbee.ai/10-best-ai-receptionist-for-salons-in-2025/" target="_blank">AI receptionists for salons</a> — BookingBee, GoodCall, Qlient.ai comparison</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://eur-lex.europa.eu/EN/legal-content/summary/rules-for-trustworthy-artificial-intelligence-in-the-eu.html" target="_blank">EU AI Act summary (EUR-Lex)</a> — official risk classification overview</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4: AI Literacy (Official EU text)</a> — obligations for deployers</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-16" target="_blank">Article 16: Provider obligations</a> | <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26" target="_blank">Article 26: Deployer obligations</a></p>
    <p style="margin:0"><a href="https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2" target="_blank">Eurostat: 20% of EU enterprises use AI (2025)</a></p>
  </div>

  <p style="margin-top:2rem"><a href="../consultants.html" class="btn btn-primary">Find an AI Act Consultant →</a></p>
</article>
'''
write_page('blog/ai-act-hairdressers-beauty-salons.html', page('Does the EU AI Act Apply to My Hair Salon?', 'AI Act compliance for hairdressers and beauty salons. What AI tools like Fresha and Booksy mean for your salon under EU regulation.', blog_post_3, '../'))

# Blog post 4: Recruitment Agencies
blog_post_4 = '''
<article class="blog-post">
  <div class="breadcrumbs"><a href="../index.html">Home</a> <span>›</span> <a href="../blog.html">Blog</a> <span>›</span> AI Act for Recruitment</div>
  <h1>Recruitment Agencies: Why Your AI Hiring Tools Are High-Risk Under the EU AI Act</h1>
  <p class="meta">February 2026 · 12 min read · <span style="background:var(--red-light);color:var(--red);padding:0.15rem 0.5rem;border-radius:4px;font-size:0.8rem;font-weight:600">HIGH-RISK · Industry Use Case</span></p>

  <p>If you run a recruitment agency and use any form of AI to screen CVs, score candidates, or automate parts of your hiring process, this article is important. Unlike most industries where the EU AI Act imposes light-touch obligations, recruitment AI is <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">explicitly listed as high-risk in Annex III</a> of the regulation.</p>
  <p>This is not a grey area. AI systems used to recruit, select, or evaluate candidates are specifically named. The compliance requirements are substantial, and the deadline — August 2, 2026 — is approaching quickly.</p>

  <h2>What the AI Act Actually Says About Recruitment</h2>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III, Category 4</a> of the AI Act classifies the following as high-risk:</p>
  <ul>
    <li>AI systems intended to be used for the <strong>recruitment or selection of natural persons</strong>, in particular to place targeted job advertisements, to analyse and filter job applications, and to evaluate candidates</li>
    <li>AI systems intended to make <strong>decisions affecting terms of work-related relationships</strong>, promotion, termination, task allocation based on individual behaviour or personal traits, or to monitor and evaluate performance</li>
  </ul>
  <p>This covers a very wide range of tools that recruitment agencies use every day. If your software ranks candidates, filters applications, or makes any form of automated recommendation about who to progress, it almost certainly falls under this category.</p>
  <p>There is a narrow exception under <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6" target="_blank">Article 6(3)</a>: AI systems that perform only "narrow procedural tasks" — for example, a tool that simply extracts contact details or graduation dates from a CV without ranking or recommending. But the moment that tool starts scoring, matching, or shortlisting, it crosses into high-risk territory.</p>

  <h2>The AI Tools Recruitment Agencies Actually Use</h2>
  <p>Most recruitment agencies are already using AI, whether they realise it or not. Here are the most common platforms and what their AI does:</p>

  <h3>CV Screening and Candidate Matching</h3>
  <p><strong><a href="https://www.manatal.com" target="_blank">Manatal</a></strong> (from $15/user/month) uses AI to parse CVs, score candidates against job requirements, enrich profiles with data from LinkedIn and other social platforms, and generate ranked shortlists. Their <a href="https://www.manatal.com/blog/ai-resume-screening" target="_blank">AI Recommendations feature</a> scans your entire database and produces scorecards of the most suitable candidates for each role. Manatal also offers an AI Interviewer that conducts automated screening around the clock.</p>
  <p><strong><a href="https://help.workable.com/hc/en-us/articles/23685011706775-Using-the-Screening-Assistant-AI-powered" target="_blank">Workable</a></strong> includes a Screening Assistant that uses semantic analysis to match candidates to job requirements. It generates profile summaries with a checklist showing how each candidate matches against the hard requirements, and ranks candidates based on AI evaluation. Workable also offers anonymised resume screening to reduce unconscious bias.</p>
  <p><strong><a href="https://www.zoho.com/recruit/ai-recruitment.html" target="_blank">Zoho Recruit</a></strong> uses Zia, Zoho's proprietary AI, to find best-suited candidates based on job requirements and skill sets, and provides AI-generated skill scores. Zia can also generate job descriptions, source candidates, and roll out offer letters.</p>

  <h3>Video Interviewing and Assessment</h3>
  <p><strong><a href="https://www.hirevue.com/ai-in-hiring" target="_blank">HireVue</a></strong> is one of the largest AI hiring platforms, offering AI-powered video assessments with detailed candidate scoring. HireVue uses generative AI with proprietary models for job matching and candidate assessment. The platform conducts regular third-party bias audits and has an AI ethics board overseeing development. Enterprise pricing starts at around $35,000 per year.</p>
  <p>It is worth noting that HireVue previously used facial analysis in video interviews — a practice that attracted significant scrutiny and was eventually discontinued. The EU AI Act now <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5" target="_blank">explicitly prohibits</a> emotion recognition in workplace and recruitment contexts.</p>

  <h3>Other Common Tools</h3>
  <p>Platforms like <strong>Recruiterflow</strong>, <strong>Eightfold AI</strong>, <strong>Paradox</strong>, <strong>Phenom</strong>, and <strong>GoodTime (Orchestra)</strong> all use AI for candidate matching, automated outreach, interview scheduling, and sentiment analysis. Even widely used tools like <strong>LinkedIn Recruiter</strong> now incorporate AI-powered candidate recommendations and, as of early 2025, an <a href="https://www.linkedin.com/business/talent/blog/product-tips/linkedin-hiring-assistant" target="_blank">AI recruitment agent</a> for small businesses.</p>

  <h2>Risk Classification for Common Recruitment AI</h2>

  <table style="width:100%;border-collapse:collapse;margin:1.5rem 0">
    <thead>
      <tr style="background:var(--red);color:white">
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">AI Tool / Function</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Risk Level</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Why</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI CV screening / candidate scoring (Manatal, Workable, Zoho Recruit)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Explicitly listed in Annex III, Category 4(a): AI used to analyse, filter, and evaluate candidates.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI video interviewing / assessment (HireVue)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Evaluates candidates using AI. Falls under Annex III, Category 4(a).</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI candidate matching / recommendation (LinkedIn AI Recruiter, Eightfold)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Recommends who to progress. Falls under selection and evaluation.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Automated job ad targeting</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Explicitly named in Annex III: "to place targeted job advertisements."</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI interview scheduling (GoodTime, Calendly AI)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Administrative task. No evaluation of candidates.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI chatbot for candidate enquiries</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Interacts with candidates. Transparency obligation applies (must disclose AI).</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Emotion recognition in interviews</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>PROHIBITED</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5" target="_blank">Article 5</a> bans emotion recognition in the workplace. Already in force since Feb 2025.</td>
      </tr>
    </tbody>
  </table>

  <h2>What You Are Required to Do</h2>
  <p>As a recruitment agency deploying high-risk AI, your obligations under <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26" target="_blank">Article 26</a> are more significant than those of a business using minimal-risk AI. Here is what is expected of you:</p>

  <h3>1. Inform Candidates</h3>
  <p>You must tell candidates that AI is being used in the recruitment process, explain how the AI system functions, and clarify what role it plays in decision-making. Under both the AI Act and <a href="https://gdpr-info.eu/art-22-gdpr/" target="_blank">GDPR Article 22</a>, candidates have the right to request an explanation of automated decisions that significantly affect them.</p>

  <h3>2. Ensure Human Oversight</h3>
  <p>High-risk AI systems must operate under meaningful human oversight. This means a qualified person must review AI-generated shortlists, scores, and recommendations before they become hiring decisions. The AI should assist your recruiters, not replace their judgement.</p>

  <h3>3. Monitor the AI System</h3>
  <p>You are required to continuously monitor the operation of your AI tools following the instructions provided by the software provider. This includes watching for unexpected outputs, discriminatory patterns, or inaccurate results, and reporting any serious incidents.</p>

  <h3>4. Conduct a Data Protection Impact Assessment</h3>
  <p>Under <a href="https://gdpr-info.eu/art-35-gdpr/" target="_blank">GDPR Article 35</a>, deploying high-risk AI that processes personal data requires a Data Protection Impact Assessment (DPIA). This evaluates the potential impact on candidates' rights and freedoms and proposes mitigation measures. If you do not already have a DPIA for your AI hiring tools, you need one.</p>

  <h3>5. Ensure AI Literacy</h3>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4</a> requires that all staff involved in operating AI systems have sufficient AI literacy. Your recruiters need to understand how the AI tools work, what data they use, and where their limitations are. This has been mandatory since February 2025.</p>

  <h3>6. Work With Your Software Providers</h3>
  <p>The heaviest technical obligations — risk management systems, data governance, technical documentation, conformity assessments, CE marking, and EU database registration — fall on the <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-16" target="_blank">providers</a> (the companies that build the AI). But you need to confirm that your providers are preparing for compliance. Ask them directly: are they conducting conformity assessments? Do they have technical documentation? Will they be ready by August 2026?</p>
  <p>Platforms like Manatal, Workable, and Zoho Recruit already advertise <a href="https://www.manatal.com/features/compliance" target="_blank">GDPR compliance features</a> and SOC 2 certification. But GDPR compliance alone does not satisfy AI Act requirements. The AI Act adds obligations around risk management, bias testing, and transparency that go beyond data protection.</p>

  <h2>Can You Handle This Yourself?</h2>
  <p>Partially. Some of the deployer obligations — informing candidates, ensuring human oversight, training your team — are things you can implement internally. But given that recruitment AI is explicitly high-risk, there are areas where professional guidance is advisable:</p>
  <ul>
    <li>Conducting a proper DPIA if you have not done one before</li>
    <li>Assessing whether your specific AI tools meet the Article 6(3) exemption criteria</li>
    <li>Reviewing your contracts with AI providers to ensure they are meeting their provider obligations</li>
    <li>Preparing documentation that demonstrates your compliance as a deployer</li>
  </ul>
  <p>For a small recruitment agency using one or two AI tools, the compliance effort is manageable with some guidance. For larger agencies using multiple AI platforms across different jurisdictions, a specialist consultant is strongly recommended.</p>

  <h2>What "Compliant" Looks Like for a Recruitment Agency</h2>
  <p>Consider a mid-sized recruitment agency with 15 consultants, using Manatal for candidate screening and LinkedIn Recruiter for sourcing. Here is what compliance looks like by August 2026:</p>
  <ul>
    <li>You have documented which AI tools you use, their purpose, and confirmed they fall under Annex III Category 4</li>
    <li>Your candidate-facing communications clearly state that AI is used in the screening process, and explain how</li>
    <li>Every AI-generated shortlist and candidate score is reviewed by a human recruiter before any decision is made</li>
    <li>Your team has completed AI literacy training covering how Manatal's scoring works, what data it uses, and its known limitations</li>
    <li>You have completed a DPIA for your AI hiring tools, or engaged a data protection specialist to do so</li>
    <li>You have written to Manatal and LinkedIn confirming their AI Act compliance roadmap, and have their responses on file</li>
    <li>You have a process for candidates to request an explanation of how AI was used in their application</li>
    <li>You are monitoring the AI system's outputs for patterns of bias or inaccuracy, and documenting any issues</li>
  </ul>
  <p>This is more work than what a hair salon or restaurant needs to do, and that is proportionate — AI that affects people's employment prospects carries real consequences, and the regulation reflects that.</p>

  <h2>The Penalties</h2>
  <p>Non-compliance with high-risk AI obligations can result in fines of up to <strong>&#x20AC;15 million or 3% of global annual turnover</strong>, whichever is higher. Separately, GDPR violations (such as failing to conduct a DPIA) can add fines of up to &#x20AC;20 million or 4% of turnover. These penalties can compound.</p>
  <p>But beyond fines, there is a reputational risk. Recruitment agencies operate on trust. If candidates or clients discover you are using AI without transparency or proper safeguards, the commercial damage may exceed any regulatory penalty.</p>

  <h2>The Deadline</h2>
  <p>The core obligations for high-risk AI systems under Annex III take effect on <strong>August 2, 2026</strong>. Compliance typically takes 8 to 14 months, which means agencies starting now are already working on a tight timeline. The AI literacy requirement under Article 4 has been in force since February 2025.</p>

  <div style="margin-top:2rem;padding:1.5rem;background:var(--red-light);border-radius:8px;font-size:0.9rem;line-height:1.8">
    <p style="margin:0 0 0.75rem 0"><strong>Sources and further reading:</strong></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III: High-Risk AI Systems</a> — Category 4 covers employment and recruitment</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6" target="_blank">Article 6: Classification rules for high-risk AI</a> — how systems are classified</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26" target="_blank">Article 26: Deployer obligations</a> — what employers and agencies must do</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5" target="_blank">Article 5: Prohibited AI practices</a> — includes emotion recognition at work</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4: AI Literacy</a> — mandatory since February 2025</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.herohunt.ai/blog/recruiting-under-the-eu-ai-act-impact-on-hiring" target="_blank">Recruiting under the EU AI Act: Full Guide</a> (HeroHunt.ai)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.hunton.com/insights/legal/the-impact-of-the-eu-ai-act-on-human-resources-activities" target="_blank">The Impact of the EU AI Act on Human Resources</a> (Hunton Andrews Kurth LLP)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.gtlaw.com/en/insights/2025/5/use-of-ai-in-recruitment-and-hiring-considerations-for-eu-and-us-companies" target="_blank">AI in Recruitment: Considerations for EU and US Companies</a> (Greenberg Traurig)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.manatal.com/features/compliance" target="_blank">Manatal compliance features</a> | <a href="https://resources.workable.com/tutorial/compliance-in-ai-for-recruitment" target="_blank">Workable compliance in AI</a> | <a href="https://www.zoho.com/recruit/ai-recruitment.html" target="_blank">Zoho Recruit AI</a></p>
    <p style="margin:0"><a href="https://gdpr-info.eu/art-35-gdpr/" target="_blank">GDPR Article 35: Data Protection Impact Assessment</a> | <a href="https://gdpr-info.eu/art-22-gdpr/" target="_blank">GDPR Article 22: Automated decision-making</a></p>
  </div>

  <p style="margin-top:2rem"><a href="../consultants.html" class="btn btn-primary">Find an AI Act Consultant →</a></p>
</article>
'''
write_page('blog/ai-act-recruitment-agencies.html', page('Recruitment Agencies: Why Your AI Hiring Tools Are High-Risk Under the EU AI Act', 'AI Act compliance for recruitment agencies. CV screening, candidate scoring, and video interviewing tools are high-risk under Annex III.', blog_post_4, '../'))

# Blog post 5: Restaurants & Cafes
blog_post_5 = '''
<article class="blog-post">
  <div class="breadcrumbs"><a href="../index.html">Home</a> <span>›</span> <a href="../blog.html">Blog</a> <span>›</span> AI Act for Restaurants</div>
  <h1>Restaurant Owners: Is Your AI Ordering System Compliant With the EU AI Act?</h1>
  <p class="meta">February 2026 · 11 min read · <span style="background:var(--gold-light);color:var(--gray-800);padding:0.15rem 0.5rem;border-radius:4px;font-size:0.8rem;font-weight:600">Industry Use Case</span></p>

  <p>You run a restaurant. You focus on food, service, and keeping customers happy. But if you use a modern point-of-sale system, an AI phone answering service, or dynamic pricing on your menu, you are already using AI — and the EU AI Act has something to say about it.</p>
  <p>The regulation, which comes fully into force in August 2026, applies to all businesses that <strong>deploy</strong> AI systems, not just those that develop them. That includes restaurants.</p>
  <p>Here is what you need to know.</p>

  <h2>The AI Tools Restaurants Actually Use</h2>
  <p>Restaurant technology has changed significantly in the past few years. Many of the platforms that restaurants rely on daily now include AI features — sometimes prominently marketed, sometimes quietly running in the background.</p>

  <h3>Point-of-Sale and Operations</h3>
  <p><strong><a href="https://pos.toasttab.com/products/toast-iq" target="_blank">Toast</a></strong> is one of the largest restaurant technology platforms, used by over <a href="https://investors.toasttab.com/news/news-details/2025/Toast-Reports-Fourth-Quarter-and-Full-Year-2024-Results/default.aspx" target="_blank">127,000 locations</a> as of late 2024. Their <a href="https://pos.toasttab.com/products/toast-iq" target="_blank">Toast IQ</a> platform uses AI to analyse sales data, identify trends, and provide actionable recommendations. Toast also offers AI-powered menu engineering that analyses item performance and suggests pricing changes, and predictive analytics for demand forecasting.</p>
  <p><strong><a href="https://get.popmenu.com/ai-answering" target="_blank">Popmenu</a></strong>, used by over 10,000 restaurants, offers an <a href="https://get.popmenu.com/ai-answering" target="_blank">AI Answering</a> feature that handles phone calls, answers questions about the menu, takes reservations, and processes orders — all without a human picking up the phone. Popmenu also uses AI for personalised marketing and dynamic menu recommendations.</p>

  <h3>Reservations and Guest Management</h3>
  <p><strong><a href="https://sevenrooms.com" target="_blank">SevenRooms</a></strong> uses AI to build detailed guest profiles, predict dining preferences, and automate personalised marketing based on visit history. Their platform segments guests automatically and triggers targeted campaigns. <strong>OpenTable</strong> and <strong>Resy</strong> also use AI for table management optimisation and demand prediction.</p>

  <h3>Labour and Inventory Forecasting</h3>
  <p><strong><a href="https://www.lineup.ai" target="_blank">Lineup.ai</a></strong> uses AI specifically for restaurant sales forecasting and labour scheduling. The platform analyses historical sales data, weather, local events, and other variables to predict how busy you will be and how many staff you need. <strong><a href="https://www.fourth.com" target="_blank">Fourth</a></strong> offers similar AI-powered workforce management and inventory forecasting for hospitality businesses.</p>

  <h3>Dynamic Pricing</h3>
  <p>Some restaurants have begun using AI-powered dynamic pricing — adjusting menu prices based on demand, time of day, or ingredient costs. This is more common in quick-service and delivery platforms, but it is spreading. Companies like <strong>Juicer</strong> (now part of Uber) and various delivery platforms use algorithmic pricing that changes in real time.</p>

  <h3>AI Phone Answering and Ordering</h3>
  <p>Beyond Popmenu, a growing number of services offer AI phone systems specifically for restaurants. <strong>Slang.ai</strong>, <strong>Maitre-D AI</strong>, and <strong>Presto</strong> (used by several large US chains) answer phones, handle takeaway orders, upsell, and manage reservations. These systems use natural language processing to understand callers and respond conversationally.</p>

  <h3>Kitchen and Food Safety AI</h3>
  <p>Tools like <strong>Apicbase</strong> and <strong>Winnow</strong> use AI for food waste tracking and recipe management. Winnow's AI-powered camera system identifies food waste in commercial kitchens and provides data to reduce costs. <strong>CookRight by Picadeli</strong> and similar systems use computer vision to monitor food preparation for safety and consistency.</p>

  <h2>Risk Classification for Common Restaurant AI</h2>

  <table style="width:100%;border-collapse:collapse;margin:1.5rem 0">
    <thead>
      <tr style="background:var(--blue);color:white">
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">AI Tool / Function</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Risk Level</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Why</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Sales analytics / menu engineering (Toast IQ)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Internal business intelligence tool. No impact on individuals' rights.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI phone answering / ordering (Popmenu AI Answering, Slang.ai)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Interacts directly with customers. Must disclose that the caller is speaking with AI.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Guest profiling and personalised marketing (SevenRooms)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Marketing personalisation. Not profiling in the Annex III sense.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI demand forecasting / labour scheduling (Lineup.ai, Fourth)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal to Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Forecasting demand is minimal. If AI determines individual staff schedules or affects working conditions, it could edge toward higher risk.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Dynamic pricing (algorithmic menu pricing)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Pricing decisions. Not individually targeted in a way that affects fundamental rights.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Food waste AI / kitchen monitoring (Winnow, CookRight)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Operational efficiency tool. Monitors food, not people.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Reservation chatbot (website or app)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI interacting with customers. Transparency obligation applies.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI staff performance monitoring</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>Potentially HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">If AI monitors and evaluates individual staff performance, it falls under <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III Category 4</a> (employment).</td>
      </tr>
    </tbody>
  </table>

  <h2>What You Actually Need to Do</h2>

  <h3>1. Know What AI You Use</h3>
  <p>Go through your technology stack. Your POS system, reservation platform, phone system, marketing tools, scheduling software, and any delivery platform integrations. Check which ones use AI features. Most will mention it on their website or in their settings. Common restaurant platforms with AI: Toast, Popmenu, SevenRooms, OpenTable, Resy, Lineup.ai, Fourth, Square, Lightspeed.</p>

  <h3>2. Ensure AI Literacy (Required Since February 2025)</h3>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4 of the AI Act</a> requires that staff involved in operating AI systems understand the basics. For a restaurant, this means your managers and anyone handling the AI phone system, reservation platform, or scheduling tool should know what the AI does, what data it uses, and where its limitations are. A 30-minute documented briefing is sufficient.</p>

  <h3>3. Disclose AI Interactions to Customers</h3>
  <p>If your restaurant uses an AI phone system, chatbot, or any AI that interacts directly with customers, you must disclose this. Examples:</p>
  <ul>
    <li>Your AI phone greeting: "Thank you for calling [restaurant]. You are speaking with our AI assistant."</li>
    <li>A note on your website: "Our phone line uses AI to handle reservations and orders"</li>
    <li>Your chatbot's opening message: "I am an AI assistant for [restaurant]. How can I help?"</li>
  </ul>
  <p>This is a transparency obligation under the AI Act. It applies to all AI systems that interact directly with people.</p>

  <h3>4. Be Careful With Staff Scheduling AI</h3>
  <p>This is where restaurants need to pay closer attention. If your scheduling tool simply forecasts demand and suggests how many staff you need, that is minimal risk. But if the AI is making decisions about <em>which</em> specific staff members work which shifts based on performance data, attendance patterns, or individual characteristics, it could cross into <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III Category 4</a> — the same high-risk category as recruitment AI.</p>
  <p>The distinction matters. Predicting "you need 4 servers on Friday" is different from "assign Maria to Friday because her performance score is highest." The second scenario involves AI making decisions about individual employment terms.</p>

  <h3>5. Review Your Data Practices</h3>
  <p>Guest profiling platforms like SevenRooms collect and process personal data. Ensure your privacy policy covers AI-powered processing, and that you have a lawful basis under GDPR. If you use loyalty programmes with AI personalisation, make sure customers can opt out.</p>

  <h3>6. Check Your Software Providers</h3>
  <p>As with any industry, the heaviest compliance burden falls on the <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-16" target="_blank">providers</a> (the companies that build the AI), not the <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26" target="_blank">deployers</a> (you). But you should ask your technology providers whether they are preparing for AI Act compliance. A simple email asking "What is your EU AI Act compliance roadmap?" is a good start.</p>

  <h2>Can You Handle This Yourself?</h2>
  <p>For most restaurants, yes. The majority of restaurant AI falls into the minimal or limited risk categories. The steps outlined above — identifying your AI tools, briefing your team, disclosing AI interactions, and checking with providers — are things you can do without a consultant.</p>
  <p>You would need professional guidance if:</p>
  <ul>
    <li>You use AI that makes decisions about individual staff members (scheduling, performance evaluation, task allocation)</li>
    <li>You use customer-facing AI that collects biometric data (facial recognition for loyalty, for example)</li>
    <li>You develop your own AI tools (custom ordering systems, proprietary recommendation engines)</li>
    <li>You operate across multiple EU jurisdictions and need to navigate different national implementations</li>
  </ul>

  <h2>What "Compliant" Looks Like for a Restaurant</h2>
  <p>Consider a busy city restaurant with 25 covers, using Toast for POS, Popmenu for AI phone answering, SevenRooms for reservations, and Lineup.ai for staff scheduling. Here is what compliance looks like:</p>
  <ul>
    <li>You have a simple document listing all AI tools, their purpose, and their risk classification</li>
    <li>Your managers have had a 30-minute briefing on the AI tools the restaurant uses</li>
    <li>Your Popmenu AI phone greeting clearly states the caller is speaking with an AI assistant</li>
    <li>Your website mentions that phone calls and online ordering may be handled by AI</li>
    <li>Your privacy policy covers AI-powered guest profiling and marketing</li>
    <li>You have confirmed with your scheduling platform that AI only forecasts demand, not individual staff assignments based on performance</li>
    <li>You have emailed Toast, Popmenu, SevenRooms, and Lineup.ai asking about their AI Act compliance plans</li>
  </ul>
  <p>For most restaurants, that covers your obligations. The compliance effort is proportionate — a restaurant using AI for phone answering and demand forecasting is not held to the same standard as a hospital using AI for diagnostics or a bank using AI for credit decisions.</p>

  <h2>The Bottom Line</h2>
  <p>Restaurant AI is growing fast. AI phone answering, demand forecasting, dynamic pricing, and guest personalisation are becoming standard features in restaurant technology platforms. The EU AI Act applies to all of these, but for most restaurants, the obligations are manageable.</p>
  <p>The key actions are straightforward: know what AI you use, make sure your team understands the basics, tell customers when they are interacting with AI, and confirm your software providers are preparing for compliance. If your situation is more complex — particularly around staff management AI — it is worth getting advice from someone who specialises in this area.</p>

  <div style="margin-top:2rem;padding:1.5rem;background:var(--blue-lighter);border-radius:8px;font-size:0.9rem;line-height:1.8">
    <p style="margin:0 0 0.75rem 0"><strong>Sources and further reading:</strong></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://pos.toasttab.com/products/toast-iq" target="_blank">Toast IQ platform</a> — AI analytics and menu engineering for restaurants</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://investors.toasttab.com/news/news-details/2025/Toast-Reports-Fourth-Quarter-and-Full-Year-2024-Results/default.aspx" target="_blank">Toast Q4 2024 results</a> — 127,000+ restaurant locations</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://get.popmenu.com/ai-answering" target="_blank">Popmenu AI Answering</a> — AI phone system for restaurants</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://sevenrooms.com" target="_blank">SevenRooms</a> — AI-powered guest management and marketing</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.lineup.ai" target="_blank">Lineup.ai</a> — AI sales forecasting and labour scheduling</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.fourth.com" target="_blank">Fourth</a> — AI workforce management for hospitality</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://eur-lex.europa.eu/EN/legal-content/summary/rules-for-trustworthy-artificial-intelligence-in-the-eu.html" target="_blank">EU AI Act summary (EUR-Lex)</a> — official risk classification overview</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III: High-Risk AI Systems</a> — Category 4 covers employment</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4: AI Literacy</a> — mandatory since February 2025</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-16" target="_blank">Article 16: Provider obligations</a> | <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26" target="_blank">Article 26: Deployer obligations</a></p>
  </div>

  <p style="margin-top:2rem"><a href="../consultants.html" class="btn btn-primary">Find an AI Act Consultant →</a></p>
</article>
'''
write_page('blog/ai-act-restaurants-cafes.html', page('Restaurant Owners: Is Your AI Ordering System Compliant With the EU AI Act?', 'AI Act compliance for restaurants and cafes. Toast, Popmenu, SevenRooms, and other restaurant AI tools under EU regulation.', blog_post_5, '../'))

# Blog post 6: Estate Agents
blog_post_6 = '''
<article class="blog-post">
  <div class="breadcrumbs"><a href="../index.html">Home</a> <span>›</span> <a href="../blog.html">Blog</a> <span>›</span> AI Act for Estate Agents</div>
  <h1>Estate Agents: Your AI Valuation Tools Could Be High-Risk Under the EU AI Act</h1>
  <p class="meta">February 2026 · 12 min read · <span style="background:var(--gold-light);color:var(--gray-800);padding:0.15rem 0.5rem;border-radius:4px;font-size:0.8rem;font-weight:600">Potentially HIGH-RISK · Industry Use Case</span></p>

  <p>Estate agency has changed. Automated valuations, AI-powered property search, virtual staging, and AI receptionists are now standard tools of the trade. If you run an estate agency in the UK or EU, you are almost certainly using AI already — and the EU AI Act, which comes fully into force in August 2026, has specific implications for this industry.</p>
  <p>The interesting part: property valuation AI is not explicitly named as high-risk, but it may well qualify through its connection to mortgage access and housing decisions. Here is what that means for you.</p>

  <h2>The AI Tools Estate Agents Actually Use</h2>

  <h3>Automated Valuation Models (AVMs)</h3>
  <p><strong><a href="https://www.hometrack.com/" target="_blank">Hometrack</a></strong> is the dominant AVM provider in the UK, used by over 80 percent of top UK lenders to generate property valuations. The system processes around 50 million valuations per year using 200+ million data points including pricing structures, supply and demand metrics, and mortgage survey data. If a mortgage lender has valued a property using an automated system, there is a good chance Hometrack was involved.</p>
  <p><strong><a href="https://www.pricehubble.com/" target="_blank">PriceHubble</a></strong> operates across 11 European countries, serving over 800 companies with AI-driven property valuations, market forecasts, and portfolio analysis. Their models combine listing data, transaction records, and building characteristics to generate real-time valuations for agents and brokerages.</p>
  <p><strong><a href="https://www.realyse.com/" target="_blank">REalyse</a></strong> provides AI-powered property valuations and market analytics in the UK, drawing on 20+ data sources including Land Registry records and EPC data. Their Pulse platform gives brokers and agents access to price trends, capital growth predictions, and rental yield analysis.</p>

  <h3>AI Property Search and Matching</h3>
  <p><strong>Rightmove</strong> has rolled out a <a href="https://www.rightmove.co.uk/" target="_blank">conversational AI property search</a> built with Google Gemini. Buyers describe what they want in plain language — "three-bed under &pound;400K, ten minutes from a train station, low council tax" — and the AI returns matching properties from live listings. Rightmove has also launched AI-powered online valuations for vendors, with an 83 percent click-through rate to agent pages during early trials.</p>
  <p><strong>OnTheMarket</strong> (now owned by CoStar) is investing in over 100 AI initiatives including lead filtering, improved AVMs, machine vision for property images, and natural language search.</p>
  <p><strong>Zoopla</strong> has introduced an AI redesign tool that lets buyers virtually redecorate property interiors, reporting an 80 percent increase in listing views during testing.</p>

  <h3>AI CRM and Lead Scoring</h3>
  <p><strong><a href="https://www.reapit.com/" target="_blank">Reapit</a></strong>, the market-leading CRM for UK estate agencies, is launching <strong>Reapit AI (RAI)</strong> in early 2026. Features include predictive lead scoring that identifies high-probability leads, automated follow-up sequences, and a listing concierge that collects data and imagery from vendors.</p>
  <p><strong><a href="https://www.altosoftware.co.uk/" target="_blank">Alto</a></strong>, used by over 6,000 agencies and 25,000 users, includes AI-generated property descriptions and automated task management. <strong><a href="https://www.street.co.uk/" target="_blank">Street CRM</a></strong> offers similar AI features as a modern alternative.</p>

  <h3>AI Voice and Chatbots</h3>
  <p><strong><a href="https://nurtur.tech/" target="_blank">Nurtur</a></strong> provides an AI voice system specifically for estate agents. It answers live property enquiries by phone, searches the agent's stock in real time, and handles sophisticated queries like "three-bed near good schools." The system has already handled over 16,000 calls with an average duration of 1 minute 35 seconds.</p>

  <h3>Virtual Tours and AI Staging</h3>
  <p><strong><a href="https://matterport.com/" target="_blank">Matterport</a></strong> creates 3D virtual tours and digital twins of properties, with a recent AI "defurnishing" feature that removes furniture from scans to show empty spaces. AI virtual staging tools like <strong>StageVirtually</strong> and <strong>REimagineHome</strong> generate photorealistic furnished images of empty properties in seconds.</p>

  <h2>Risk Classification for Common Estate Agent AI</h2>

  <table style="width:100%;border-collapse:collapse;margin:1.5rem 0">
    <thead>
      <tr style="background:var(--blue);color:white">
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">AI Tool / Function</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Risk Level</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Why</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Automated property valuation (Hometrack, PriceHubble, REalyse)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>Potentially HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Valuations directly affect mortgage access. <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III, Section 5</a> covers AI used for access to essential private services, including creditworthiness assessment.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI property search and matching (Rightmove AI, OnTheMarket)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Helps buyers find properties. No decision-making that restricts access to housing.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI lead scoring and prioritisation (Reapit AI)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Internal business tool. Prioritises leads for agents, does not affect buyers' access to services.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI voice assistant / chatbot (Nurtur, website chatbots)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Interacts directly with clients. Must disclose AI interaction.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI-generated property descriptions (Alto, Street CRM)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Content generation. No impact on individuals' rights.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Virtual staging and 3D tours (Matterport, StageVirtually)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Visual presentation tool. No decision-making involved.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI tenant screening / referencing</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI that assesses tenants for rental eligibility affects access to housing. Falls under Annex III, Section 5.</td>
      </tr>
    </tbody>
  </table>

  <h2>Why Property Valuation AI Deserves Attention</h2>
  <p>Property valuation is not explicitly named as high-risk in <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III</a>. However, the regulation covers AI systems used for "access to and enjoyment of essential private services," which includes creditworthiness assessment and credit scoring. Property valuations are a direct input to mortgage decisions — a lender will not approve a mortgage if the AVM returns a low valuation. In practice, this means:</p>
  <ul>
    <li>An automated valuation that undervalues a property can prevent a buyer from getting a mortgage</li>
    <li>Systematic undervaluation in certain areas could have discriminatory effects on specific communities</li>
    <li>The financial impact of an inaccurate valuation is significant — it can make or break a property transaction</li>
  </ul>
  <p>Whether regulators will treat property valuation AVMs as high-risk remains to be confirmed as national enforcement bodies finalise their guidance. But the connection to mortgage access makes it an area where estate agents and valuation providers should be prepared.</p>

  <h2>What You Actually Need to Do</h2>

  <h3>1. Know What AI You Use</h3>
  <p>Make a list of every technology tool in your agency. Check which ones include AI features. Common platforms: Reapit, Alto, Street, Rightmove, Zoopla, OnTheMarket, Hometrack (if you provide valuations), Nurtur, Matterport.</p>

  <h3>2. Ensure AI Literacy (Required Since February 2025)</h3>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4 of the AI Act</a> requires that staff operating AI systems have sufficient understanding of how those systems work. For an estate agency, this means your negotiators and administrators should know which tools use AI, what decisions the AI makes, and what data it processes. A documented team briefing covers this.</p>

  <h3>3. Disclose AI Interactions to Clients</h3>
  <p>If you use Nurtur or any AI voice system to handle enquiries, a website chatbot for property questions, or Rightmove's AI search on your behalf, clients must know they are interacting with AI. This can be as simple as the AI announcing itself at the start of a call or conversation.</p>

  <h3>4. If You Provide Automated Valuations</h3>
  <p>This is where the compliance picture becomes more involved. If your agency uses AVM technology to provide valuations — particularly for mortgage purposes — you should:</p>
  <ul>
    <li>Document which AVM tool you use and how it generates valuations</li>
    <li>Ensure a qualified human reviews AI-generated valuations before they are relied upon for mortgage decisions</li>
    <li>Understand the data sources your AVM uses and whether they could introduce bias</li>
    <li>Contact your AVM provider (Hometrack, PriceHubble, etc.) and ask about their AI Act compliance plans</li>
  </ul>

  <h3>5. If You Use AI for Tenant Referencing</h3>
  <p>AI systems that assess whether a tenant qualifies for a rental property are making decisions about access to housing. This is a clearer high-risk use case under the AI Act. If your lettings arm uses automated tenant screening, ensure there is meaningful human oversight, that tenants are informed AI is being used, and that you have a process for tenants to challenge automated decisions.</p>

  <h3>6. Check Your Software Providers</h3>
  <p>The heaviest technical obligations fall on the <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-16" target="_blank">providers</a> (Hometrack, Reapit, Alto, etc.), not on you as a <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26" target="_blank">deployer</a>. But you should confirm your providers are preparing. Ask them: "What is your EU AI Act compliance roadmap?"</p>

  <h2>Can You Handle This Yourself?</h2>
  <p>For most estate agencies, the core obligations — AI literacy, transparency with clients, checking your providers — are manageable without outside help. However, you would benefit from professional guidance if:</p>
  <ul>
    <li>You provide automated valuations used in mortgage decisions</li>
    <li>You use AI for tenant screening or referencing</li>
    <li>You develop proprietary AI tools (custom matching algorithms, bespoke valuation models)</li>
    <li>You operate across multiple EU jurisdictions</li>
  </ul>

  <h2>What "Compliant" Looks Like for an Estate Agency</h2>
  <p>Consider a high-street estate and lettings agency with 8 negotiators, using Reapit for CRM, Rightmove and Zoopla for listings, Nurtur for after-hours calls, and Matterport for virtual tours. Here is what compliance looks like:</p>
  <ul>
    <li>You have a document listing all AI tools, their purpose, and risk classification</li>
    <li>Your team has had a briefing on the AI tools the agency uses</li>
    <li>Nurtur's phone greeting discloses it is an AI assistant</li>
    <li>Your website notes that enquiries may be handled by AI</li>
    <li>You have written to Reapit, Rightmove, and any valuation providers asking about their AI Act compliance plans</li>
    <li>If you use AI tenant referencing, tenants are informed and a human reviews the AI's recommendation</li>
    <li>Your privacy policy mentions AI-powered tools and data processing</li>
  </ul>

  <h2>The Bottom Line</h2>
  <p>Estate agency AI is largely minimal or limited risk, with two notable exceptions: automated property valuations (which connect to mortgage access) and AI tenant screening (which affects access to housing). For most agencies, the compliance effort is straightforward — know your tools, train your team, be transparent with clients, and check with your providers.</p>
  <p>If your agency is involved in valuations or tenant referencing that rely on AI, it is worth keeping a closer eye on how national regulators interpret Annex III in the property context. The guidance is still evolving, and being ahead of it is better than being caught out.</p>

  <div style="margin-top:2rem;padding:1.5rem;background:var(--blue-lighter);border-radius:8px;font-size:0.9rem;line-height:1.8">
    <p style="margin:0 0 0.75rem 0"><strong>Sources and further reading:</strong></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.hometrack.com/" target="_blank">Hometrack</a> — UK's leading automated valuation model provider (50M+ valuations/year)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.pricehubble.com/" target="_blank">PriceHubble</a> — AI property valuations across 11 European countries</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.realyse.com/" target="_blank">REalyse</a> — UK property data analytics and AI valuations</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.reapit.com/" target="_blank">Reapit</a> — market-leading CRM launching Reapit AI (RAI) in 2026</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.altosoftware.co.uk/" target="_blank">Alto Software</a> — 6,000+ agencies, 25,000 users, AI-generated descriptions</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://nurtur.tech/" target="_blank">Nurtur</a> — AI voice system for estate agents (16,000+ calls handled)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://matterport.com/" target="_blank">Matterport</a> — 3D virtual tours with AI defurnishing</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III: High-Risk AI Systems (Official EU text)</a> — Section 5 covers access to essential services</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4: AI Literacy (Official EU text)</a> — mandatory since February 2025</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-16" target="_blank">Article 16: Provider obligations</a> | <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26" target="_blank">Article 26: Deployer obligations</a></p>
  </div>

  <p style="margin-top:2rem"><a href="../consultants.html" class="btn btn-primary">Find an AI Act Consultant →</a></p>
</article>
'''
write_page('blog/ai-act-estate-agents.html', page('Estate Agents: Your AI Valuation Tools Could Be High-Risk Under the EU AI Act', 'AI Act compliance for estate agents. Automated valuations, AI property search, and tenant screening under EU regulation.', blog_post_6, '../'))

# Blog post 7: E-Commerce Shops
blog_post_7 = '''
<article class="blog-post">
  <div class="breadcrumbs"><a href="../index.html">Home</a> <span>›</span> <a href="../blog.html">Blog</a> <span>›</span> AI Act for E-Commerce</div>
  <h1>E-Commerce Shops: What the EU AI Act Means for Your Online Store</h1>
  <p class="meta">February 2026 · 12 min read · <span style="background:var(--gold-light);color:var(--gray-800);padding:0.15rem 0.5rem;border-radius:4px;font-size:0.8rem;font-weight:600">Industry Use Case</span></p>

  <p>If you sell online, you use AI. Product recommendations, chatbots, fraud detection, dynamic pricing, personalised emails — these are standard features in modern e-commerce platforms. The EU AI Act, which comes fully into force in August 2026, applies to businesses that deploy AI systems. That includes your online shop.</p>
  <p>The good news is that most e-commerce AI falls into the minimal or limited risk categories. But there is one area where the regulation bites hard: if your shop offers buy now, pay later services like Klarna or Afterpay, the AI credit scoring behind those payments is explicitly high-risk.</p>
  <p>Here is what you need to know.</p>

  <h2>The AI Tools E-Commerce Businesses Actually Use</h2>

  <h3>Product Recommendations</h3>
  <p><strong><a href="https://www.nosto.com/" target="_blank">Nosto</a></strong> uses behavioural and predictive AI to deliver personalised product suggestions in real time. Their platform runs 20+ self-learning algorithms for cross-sells, upsells, and "visually similar" product recommendations. Nosto integrates with Shopify, Magento, BigCommerce, and Shopware.</p>
  <p><strong><a href="https://www.clerk.io/" target="_blank">Clerk.io</a></strong>, founded in Copenhagen, provides an all-in-one AI personalisation platform with 20+ recommendation logics. Customers report a 22 percent increase in average basket size from their recommendations. <strong><a href="https://www.mastercard.com/europe/en/business/consumer-acquisition-and-engagement/personalization/how-it-works.html" target="_blank">Dynamic Yield</a></strong> (now owned by Mastercard) powers personalisation for 350+ global brands.</p>

  <h3>AI Chatbots and Customer Service</h3>
  <p><strong><a href="https://www.gorgias.com/" target="_blank">Gorgias</a></strong>, used by 15,000 e-commerce brands, offers an AI Agent that resolves 60 percent of support enquiries automatically. Their 2026 update includes a Shopping Assistant that proactively engages customers with personalised recommendations and intent-based discounting.</p>
  <p><strong><a href="https://www.tidio.com/" target="_blank">Tidio</a></strong> serves over 300,000 businesses with live chat and its Lyro AI chatbot that automates common questions, order status checks, and ticket creation. Both platforms integrate deeply with Shopify and other major e-commerce systems.</p>

  <h3>Dynamic Pricing</h3>
  <p><strong><a href="https://prisync.com/" target="_blank">Prisync</a></strong> monitors competitor prices in real time and generates AI-driven SmartPrice suggestions based on competitor pricing and your product costs. <strong><a href="https://competera.ai/" target="_blank">Competera</a></strong> handles AI pricing for large retailers including Sephora, MediaMarkt, and Ocado, updating thousands of SKUs multiple times daily.</p>

  <h3>Inventory and Demand Forecasting</h3>
  <p><strong><a href="https://www.prediko.io/" target="_blank">Prediko</a></strong>, used by 1,000+ Shopify merchants, trains its AI on 25 million+ SKUs across 15 industries. It analyses seasonality, past sales, and growth trends to predict demand, flag low stock, and generate purchase orders automatically.</p>

  <h3>Fraud Detection</h3>
  <p><strong><a href="https://www.signifyd.com/" target="_blank">Signifyd</a></strong> provides AI-powered fraud decisions with a financial guarantee against chargebacks on approved orders. Their system analyses transaction patterns to make instant checkout decisions, claiming a 5-9 percent conversion increase. <strong><a href="https://www.riskified.com/" target="_blank">Riskified</a></strong> offers similar AI fraud protection for high-volume retailers.</p>
  <p>Shopify includes built-in machine learning fraud analysis that flags unusual orders based on IP address, payment method, and order patterns, though many merchants supplement this with dedicated tools.</p>

  <h3>AI Email Marketing and Personalisation</h3>
  <p><strong><a href="https://www.klaviyo.com/" target="_blank">Klaviyo</a></strong>, used by 117,000+ brands with Shopify, includes 40+ AI-powered features: optimised send times based on subscriber engagement, AI-generated subject lines, churn prediction, and next-purchase-date forecasting. It personalises product recommendations across email, SMS, and WhatsApp.</p>

  <h3>AI-Generated Product Descriptions</h3>
  <p>Tools like <strong><a href="https://describely.ai/" target="_blank">Describely</a></strong> generate SEO-optimised product descriptions in bulk, syncing with Shopify, Wix, and Salsify. This is increasingly common as merchants scale their catalogues faster than they can write descriptions manually.</p>

  <h2>Risk Classification for Common E-Commerce AI</h2>

  <table style="width:100%;border-collapse:collapse;margin:1.5rem 0">
    <thead>
      <tr style="background:var(--blue);color:white">
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">AI Tool / Function</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Risk Level</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Why</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Product recommendations (Nosto, Clerk.io, Dynamic Yield)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Suggestions based on browsing behaviour. No impact on fundamental rights.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI chatbot / customer service (Gorgias, Tidio)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Interacts directly with customers. Must disclose AI interaction.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Dynamic pricing (Prisync, Competera)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Pricing decisions based on market data. Not individually targeted in a rights-affecting way.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Inventory / demand forecasting (Prediko)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Internal supply chain tool. No direct consumer impact.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Fraud detection (Signifyd, Riskified, Shopify)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Fraud detection is explicitly exempted from the credit-scoring high-risk category in Annex III.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI email personalisation (Klaviyo)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Marketing personalisation. Standard commercial practice.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI-generated product descriptions (Describely)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Content generation tool. Article 50 transparency may apply if descriptions are not reviewed by a human.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Buy now, pay later credit scoring (Klarna, Afterpay)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III, Section 5</a> explicitly covers AI used for creditworthiness assessment and credit scoring.</td>
      </tr>
    </tbody>
  </table>

  <h2>The Buy Now, Pay Later Question</h2>
  <p>This is the part of e-commerce AI that crosses into high-risk territory. If your shop offers Klarna, Afterpay, Clearpay, or similar buy now, pay later (BNPL) services, the AI credit scoring that decides whether a customer is approved happens in the background — but it is explicitly covered by <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III, Section 5</a> of the AI Act, which classifies AI for "evaluating the creditworthiness of natural persons or establishing their credit score" as high-risk.</p>
  <p>The compliance burden here falls primarily on the BNPL providers (Klarna, Afterpay, etc.), not on you as the merchant. They are the <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-16" target="_blank">providers</a> of the AI system. However, as a <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26" target="_blank">deployer</a>, you should:</p>
  <ul>
    <li>Inform customers that BNPL decisions involve AI credit assessment</li>
    <li>Ensure your BNPL providers are preparing for AI Act compliance</li>
    <li>Provide a process for customers to query BNPL decisions (most providers already handle this)</li>
  </ul>

  <h2>What You Actually Need to Do</h2>

  <h3>1. Know What AI You Use</h3>
  <p>Go through your technology stack: your e-commerce platform (Shopify, WooCommerce, Magento), recommendation engine, chatbot, email marketing, fraud detection, pricing tools, and payment providers. List which ones use AI features. Most will mention it in their marketing or settings.</p>

  <h3>2. Ensure AI Literacy (Required Since February 2025)</h3>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4</a> requires that staff operating AI systems understand the basics of how they work. If you run the shop yourself, that means you. If you have a team, ensure they understand which customer interactions are AI-powered and what data the AI processes.</p>

  <h3>3. Disclose AI Interactions to Customers</h3>
  <p>If you use an AI chatbot for customer service, customers must know they are talking to AI. This is straightforward — most chatbot platforms already include an option to display an "AI assistant" label. For AI-generated product descriptions, consider adding a note if descriptions are not reviewed by a human.</p>

  <h3>4. Review Your Dynamic Pricing</h3>
  <p>Standard competitive pricing based on market data is minimal risk. But if your pricing AI applies different prices to different customer segments based on personal data — for example, showing higher prices to customers identified as less price-sensitive — you should review whether this could be considered discriminatory. The AI Act does not explicitly classify this as high-risk, but it intersects with existing consumer protection rules.</p>

  <h3>5. Check Your Payment Providers</h3>
  <p>If you offer BNPL, confirm that your providers (Klarna, Afterpay, Clearpay, etc.) are preparing for high-risk AI compliance. Ask them directly about their AI Act compliance roadmap.</p>

  <h3>6. Check All Your Software Providers</h3>
  <p>The heaviest obligations fall on the providers of AI systems, not on you as a deployer. But you should confirm your key providers are aware of the AI Act. A simple email asking "Are you preparing for EU AI Act compliance?" to Nosto, Clerk.io, Gorgias, Tidio, Klaviyo, or whichever tools you use is a reasonable step.</p>

  <h2>Can You Handle This Yourself?</h2>
  <p>For most small-to-medium e-commerce businesses, yes. The majority of your AI tools fall into minimal or limited risk categories. The steps above — mapping your AI, briefing yourself or your team, labelling chatbots, checking with providers — are all things you can do without a consultant.</p>
  <p>You would need professional guidance if:</p>
  <ul>
    <li>You develop your own AI tools (custom recommendation engines, proprietary pricing algorithms)</li>
    <li>You use AI to make decisions that affect individual customers' access to services (beyond standard personalisation)</li>
    <li>You process biometric data for customer identification</li>
    <li>You operate a BNPL or credit service directly (rather than through a third-party provider)</li>
    <li>You sell across multiple EU jurisdictions and need to navigate different national implementations</li>
  </ul>

  <h2>What "Compliant" Looks Like for an Online Shop</h2>
  <p>Consider a Shopify store with 500 orders per month, using Nosto for recommendations, Tidio for chat, Klaviyo for email, Shopify's built-in fraud analysis, and Klarna for BNPL. Here is what compliance looks like:</p>
  <ul>
    <li>You have a simple document listing all AI tools, their purpose, and risk level</li>
    <li>You understand how each tool uses customer data</li>
    <li>Your Tidio chatbot displays "AI assistant" in the chat window</li>
    <li>Your privacy policy mentions AI-powered recommendations, chatbot, and email personalisation</li>
    <li>Your checkout page notes that Klarna decisions involve AI credit assessment</li>
    <li>You have confirmed with Klarna that they are preparing for AI Act compliance</li>
    <li>You have emailed Nosto, Tidio, and Klaviyo about their AI Act compliance plans</li>
  </ul>
  <p>For most online shops, that is the extent of it. The regulation is designed to be proportionate — a Shopify store using product recommendations is not treated the same as a bank using AI for loan decisions.</p>

  <h2>The Bottom Line</h2>
  <p>E-commerce AI is largely low-risk under the EU AI Act. Product recommendations, email personalisation, inventory forecasting, and fraud detection are all minimal risk. Chatbots require transparency (tell customers it is AI). The one area that crosses into high-risk is BNPL credit scoring, but the compliance burden there sits primarily with the payment providers, not with you as the merchant.</p>
  <p>The key actions: know what AI you use, tell customers when they are interacting with AI, check that your BNPL providers are preparing for compliance, and keep your privacy policy updated. If your setup is more complex, speak to a specialist.</p>

  <div style="margin-top:2rem;padding:1.5rem;background:var(--blue-lighter);border-radius:8px;font-size:0.9rem;line-height:1.8">
    <p style="margin:0 0 0.75rem 0"><strong>Sources and further reading:</strong></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.nosto.com/" target="_blank">Nosto</a> — AI product recommendations for e-commerce</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.clerk.io/" target="_blank">Clerk.io</a> — AI personalisation platform (Copenhagen)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.gorgias.com/" target="_blank">Gorgias</a> — AI customer service for 15,000 e-commerce brands</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.tidio.com/" target="_blank">Tidio</a> — AI chatbot for 300,000+ businesses</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://prisync.com/" target="_blank">Prisync</a> — AI dynamic pricing | <a href="https://competera.ai/" target="_blank">Competera</a> — AI pricing for enterprise retail</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.prediko.io/" target="_blank">Prediko</a> — AI demand forecasting for Shopify (1,000+ merchants)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.signifyd.com/" target="_blank">Signifyd</a> — AI fraud protection | <a href="https://www.riskified.com/" target="_blank">Riskified</a> — AI fraud prevention</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.klaviyo.com/" target="_blank">Klaviyo</a> — AI email marketing for 117,000+ Shopify brands</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://describely.ai/" target="_blank">Describely</a> — AI product description generator</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III: High-Risk AI Systems (Official EU text)</a> — Section 5 covers credit scoring</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4: AI Literacy (Official EU text)</a> | <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-16" target="_blank">Article 16: Provider obligations</a> | <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26" target="_blank">Article 26: Deployer obligations</a></p>
  </div>

  <p style="margin-top:2rem"><a href="../consultants.html" class="btn btn-primary">Find an AI Act Consultant →</a></p>
</article>
'''
write_page('blog/ai-act-ecommerce-shops.html', page('E-Commerce Shops: What the EU AI Act Means for Your Online Store', 'AI Act compliance for e-commerce. Product recommendations, chatbots, dynamic pricing, and BNPL credit scoring under EU regulation.', blog_post_7, '../'))

# Blog post 8: Accountants & Bookkeepers
blog_post_8 = '''
<article class="blog-post">
  <div class="breadcrumbs"><a href="../index.html">Home</a> <span>›</span> <a href="../blog.html">Blog</a> <span>›</span> AI Act for Accountants</div>
  <h1>Accountants: What the EU AI Act Means for Your Practice</h1>
  <p class="meta">February 2026 · 11 min read · <span style="background:var(--gold-light);color:var(--gray-800);padding:0.15rem 0.5rem;border-radius:4px;font-size:0.8rem;font-weight:600">Industry Use Case</span></p>

  <p>Accounting has embraced AI faster than most professions. 91 percent of UK accountants are either using or planning to use AI, and they spend an average of nearly three hours a day working with AI tools. Auto-categorisation, receipt scanning, cash flow forecasting, and anomaly detection are now standard features in the platforms accountants rely on every day.</p>
  <p>The EU AI Act, which comes fully into force in August 2026, applies to businesses that deploy AI systems. Most accounting AI falls into the minimal risk category, but there are specific areas — particularly around credit scoring and anti-money laundering — where the picture is more nuanced.</p>

  <h2>The AI Tools Accountants Actually Use</h2>

  <h3>Accounting Platforms</h3>
  <p><strong><a href="https://www.xero.com" target="_blank">Xero</a></strong> includes AI-powered auto-categorisation of expenses, automatic bank transaction matching, anomaly detection for unusual transactions, and receipt OCR. The system learns from your past categorisation patterns and improves over time.</p>
  <p><strong><a href="https://quickbooks.intuit.com/uk/" target="_blank">QuickBooks</a></strong> is rolling out Intuit Assist, a generative AI financial assistant, to UK users. It offers dynamic auto-categorisation, VAT error checking, Making Tax Digital compliance automation, and ongoing income tax projections. QuickBooks also uses AI to detect common bookkeeping errors like missing vendor information and duplicate entries.</p>
  <p><strong><a href="https://www.sage.com/en-gb/" target="_blank">Sage</a></strong> has introduced Sage Copilot and is developing agentic AI features for 2026. Current AI includes invoice processing from receipt photos, error detection and anomaly monitoring, automated payment chasing (reducing payment cycles by 7 days), and a Finance Intelligence agent that answers questions about your reports and transactions.</p>
  <p><strong><a href="https://www.freeagent.com/" target="_blank">FreeAgent</a></strong> offers Smart Capture for automatic receipt data extraction and has partnered with Jenesys to create "Jack," an AI intelligent bookkeeper that handles line-item categorisation into the general ledger.</p>

  <h3>Document Processing and OCR</h3>
  <p><strong><a href="https://dext.com/" target="_blank">Dext</a></strong> (formerly Receipt Bank), used by over 35,000 accountants and bookkeepers, processes 5+ million documents per month with 99 percent+ OCR accuracy. It automatically extracts dates, amounts, suppliers, tax, and invoice numbers, then auto-categorises based on past entries.</p>
  <p><strong><a href="https://www.autoentry.com/" target="_blank">AutoEntry</a></strong> serves 250,000+ businesses, processing 1.4 million documents monthly. Its AI interprets different invoice layouts, understands context for data points, and continuously improves through machine learning. <strong><a href="https://booke.ai/" target="_blank">Booke AI</a></strong> adds real-time OCR in any language and currency, with automatic transaction matching to invoices.</p>

  <h3>Audit and Anomaly Detection</h3>
  <p><strong><a href="https://www.mindbridge.ai/" target="_blank">MindBridge</a></strong> uses unsupervised learning algorithms to analyse 100 percent of financial data (not just samples). It risk-scores every transaction and identifies unintentional errors and potential fraud patterns, with dedicated visualisations for accounts receivable and payable analysis.</p>

  <h3>Cash Flow Forecasting</h3>
  <p><strong><a href="https://www.futrli.com/" target="_blank">Futrli</a></strong> (now owned by Sage), used by 45,000+ users across 140+ countries, generates 3-year financial forecasts using all your accounting data. <strong><a href="https://floatapp.com/" target="_blank">Float</a></strong> provides real-time visual cash flow forecasts with scenario planning, syncing directly with Xero, QuickBooks, and FreeAgent.</p>

  <h2>Risk Classification for Common Accounting AI</h2>

  <table style="width:100%;border-collapse:collapse;margin:1.5rem 0">
    <thead>
      <tr style="background:var(--blue);color:white">
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">AI Tool / Function</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Risk Level</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Why</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Auto-categorisation (Xero, QuickBooks, Sage, FreeAgent)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Internal bookkeeping tool. No impact on individuals' fundamental rights.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Receipt / invoice OCR (Dext, AutoEntry, Booke AI)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Data extraction only. No decision-making.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Anomaly detection / audit AI (MindBridge)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Supports the auditor's work. Human reviews all flagged items.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Cash flow forecasting (Futrli, Float)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Advisory tool. Human-reviewed predictions.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI chatbot / client communication</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Interacts with clients. Must disclose AI interaction.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Credit scoring for client lending decisions</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III, Section 5</a> covers AI used for creditworthiness assessment.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Anti-money laundering (AML) screening</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Fraud and financial crime detection is explicitly exempt from the high-risk credit-scoring category.</td>
      </tr>
    </tbody>
  </table>

  <h2>Where It Gets More Complex</h2>
  <p>Most day-to-day accounting AI — categorisation, OCR, reconciliation, forecasting — is clearly minimal risk. The areas that deserve closer attention:</p>
  <p><strong>Credit scoring:</strong> If your practice uses AI to assess clients' creditworthiness for lending purposes (not common for most accountants, but relevant for practices advising on finance applications), this falls under <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III, Section 5</a> as high-risk. The obligation primarily sits with the credit provider, but practices involved in the process should be aware.</p>
  <p><strong>AML screening:</strong> AI-powered anti-money laundering tools are used in larger practices. The good news: fraud detection is explicitly exempt from the high-risk credit-scoring category under the AI Act. However, transaction monitoring that goes beyond fraud detection into broader profiling may sit in a greyer area.</p>
  <p><strong>AI-generated tax advice:</strong> Tax calculations themselves are not high-risk under the AI Act. But as AI assistants like Intuit Assist begin generating tax advice and financial recommendations, the boundary between "tool" and "advisor" becomes relevant for professional liability, even if not strictly high-risk under the regulation.</p>

  <h2>What You Actually Need to Do</h2>

  <h3>1. Know What AI You Use</h3>
  <p>List every tool in your practice: Xero, QuickBooks, Sage, FreeAgent, Dext, AutoEntry, any forecasting tools, any chatbots. Note which AI features you actively use.</p>

  <h3>2. Ensure AI Literacy (Required Since February 2025)</h3>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4</a> requires sufficient AI literacy for anyone operating AI systems. For an accounting practice, this means you and your team should understand how the AI in your tools works — what auto-categorisation does, how anomaly detection flags items, what data your OCR processes. A documented internal briefing covers this.</p>

  <h3>3. Disclose AI Interactions</h3>
  <p>If you use an AI chatbot for client queries or an AI assistant that communicates directly with clients, disclose that it is AI. Most accounting chatbot tools already include this option.</p>

  <h3>4. Review Your Professional Standards</h3>
  <p>Beyond the AI Act, accounting bodies like ICAEW, ACCA, and CIMA are developing their own guidance on AI use in practice. Ensure your AI usage aligns with professional standards around competence, due care, and professional scepticism — particularly when AI generates financial advice or audit findings that you rely on.</p>

  <h3>5. Check Your Software Providers</h3>
  <p>The compliance burden falls on the providers (Xero, Sage, Intuit, Dext, etc.), not on you as a deployer. But confirm they are preparing. Ask them about their AI Act compliance plans.</p>

  <h2>Can You Handle This Yourself?</h2>
  <p>For the vast majority of accounting practices, yes. Your core AI tools are minimal risk. The steps above are straightforward. You would need professional guidance if:</p>
  <ul>
    <li>Your practice uses AI in credit scoring or lending assessment for clients</li>
    <li>You develop proprietary AI tools for client advisory</li>
    <li>You use AI for AML screening beyond standard fraud detection</li>
    <li>You operate across multiple EU jurisdictions</li>
  </ul>

  <h2>What "Compliant" Looks Like for an Accounting Practice</h2>
  <p>Consider a 5-person accounting practice using Xero, Dext, and Float. Here is what compliance looks like:</p>
  <ul>
    <li>You have a document listing your AI tools, their purpose, and risk level</li>
    <li>Your team has had a briefing on how the AI in Xero, Dext, and Float works</li>
    <li>If you use a client-facing chatbot, it identifies itself as AI</li>
    <li>Your privacy policy mentions AI-powered data processing</li>
    <li>You have emailed Xero, Dext, and Float about their AI Act compliance plans</li>
  </ul>
  <p>For most practices, that is the extent of it. Accounting AI is overwhelmingly in the minimal risk category, and the compliance effort reflects that.</p>

  <div style="margin-top:2rem;padding:1.5rem;background:var(--blue-lighter);border-radius:8px;font-size:0.9rem;line-height:1.8">
    <p style="margin:0 0 0.75rem 0"><strong>Sources and further reading:</strong></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.xero.com" target="_blank">Xero</a> — AI auto-categorisation, reconciliation, anomaly detection</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://quickbooks.intuit.com/uk/" target="_blank">QuickBooks UK</a> — Intuit Assist AI, VAT error checking, MTD compliance</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.sage.com/en-gb/" target="_blank">Sage</a> — Sage Copilot, agentic AI, invoice processing</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.freeagent.com/" target="_blank">FreeAgent</a> — Smart Capture, Jenesys AI bookkeeper partnership</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://dext.com/" target="_blank">Dext</a> — 35,000+ accountants, 5M+ documents/month, 99%+ OCR accuracy</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.autoentry.com/" target="_blank">AutoEntry</a> — 250,000+ businesses, 1.4M documents/month</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.mindbridge.ai/" target="_blank">MindBridge</a> — AI audit and anomaly detection (100% data review)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.futrli.com/" target="_blank">Futrli</a> — AI cash flow forecasting (45,000+ users, Sage-owned)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://floatapp.com/" target="_blank">Float</a> — real-time cash flow forecasting</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III: High-Risk AI Systems (Official EU text)</a> — Section 5 covers credit scoring</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4: AI Literacy (Official EU text)</a> — mandatory since February 2025</p>
  </div>

  <p style="margin-top:2rem"><a href="../consultants.html" class="btn btn-primary">Find an AI Act Consultant →</a></p>
</article>
'''
write_page('blog/ai-act-accountants.html', page('Accountants: What the EU AI Act Means for Your Practice', 'AI Act compliance for accountants and bookkeepers. Xero, QuickBooks, Sage, Dext, and other accounting AI tools under EU regulation.', blog_post_8, '../'))

# Blog post 9: GP Practices
blog_post_9 = '''
<article class="blog-post">
  <div class="breadcrumbs"><a href="../index.html">Home</a> <span>›</span> <a href="../blog.html">Blog</a> <span>›</span> AI Act for GP Practices</div>
  <h1>GP Practices: Your AI Triage and Diagnostic Tools Are High-Risk Under the EU AI Act</h1>
  <p class="meta">February 2026 · 14 min read · <span style="background:var(--red-light);color:var(--red);padding:0.15rem 0.5rem;border-radius:4px;font-size:0.8rem;font-weight:600">HIGH-RISK · Industry Use Case</span></p>

  <p>General practice is one of the sectors most affected by the EU AI Act. AI triage tools, clinical decision support, diagnostic imaging, and medical transcription are now embedded in NHS and European GP workflows. Unlike a hair salon using an AI booking system or a restaurant with an AI phone line, healthcare AI directly affects patient safety — and the regulation treats it accordingly.</p>
  <p>Healthcare AI is explicitly high-risk under <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III</a> of the AI Act. If your practice uses AI for triage, diagnosis, or clinical decision-making, the compliance requirements are significant. Here is what you need to know.</p>

  <h2>The AI Tools GP Practices Actually Use</h2>

  <h3>AI Triage and Symptom Assessment</h3>
  <p><strong><a href="https://klinikhealthcaresolutions.com" target="_blank">Klinik</a></strong> is a CE-marked Class IIa medical device that provides AI-powered online triage for GP practices. It recognises over 1,000 symptoms and conditions, ranks urgency, and recommends whether patients need a GP, nurse, pharmacist, or self-care. NHS practices using Klinik have reported a 20 percent reduction in administrative tasks and &pound;350,000 in capacity savings per primary care network.</p>
  <p><strong><a href="https://econsult.net" target="_blank">eConsult</a></strong> powers triage for over 3,200 GP practices covering 28 million patients, with 50+ million consultations conducted. Their eTriage system uses AI aligned with the Manchester Triage System to auto-triage patients and suggest urgency levels.</p>
  <p><strong><a href="https://ada.com" target="_blank">Ada Health</a></strong>, UKCA-marked, is one of the most widely used patient-facing symptom checkers. Patients describe their symptoms and the AI evaluates possible conditions, recommending appropriate triage levels.</p>

  <h3>AI Clinical Decision Support</h3>
  <p><strong><a href="https://ardens.org.uk" target="_blank">Ardens Clinical</a></strong> is used by 87 percent of GP practices in England. It integrates with EMIS Web and SystmOne to provide clinical templates, safety alerts, recall systems, and referral management.</p>
  <p><strong><a href="https://www.iatrox.com" target="_blank">iatroX</a></strong> provides a UK-centric AI clinical assistant that answers questions against UK-accepted clinical guidance with explicit citations, supports structured differential diagnosis, and provides confidence metrics.</p>

  <h3>AI Medical Transcription and Documentation</h3>
  <p><strong><a href="https://www.animahealth.com" target="_blank">Anima</a></strong> (Annie AI Scribe) is an MHRA Class I registered medical device used by 400+ GP practices serving 2 million patients. It transcribes consultations in under 5 seconds, generates clinical notes with automatic SNOMED coding, and reads inbound hospital documents to create summaries and propose follow-up tasks. It integrates directly with EMIS and SystmOne.</p>
  <p><strong><a href="https://www.accurx.com" target="_blank">Accurx Scribe</a></strong> (powered by Tandem Health) has been rolled out to 98 percent of GP practices using the Accurx platform, reaching 200,000+ NHS staff. It transcribes consultations, generates structured medical notes, and creates patient and referral letters with EMIS and SystmOne write-back.</p>

  <h3>AI Diagnostic Imaging</h3>
  <p><strong><a href="https://skin-analytics.com" target="_blank">Skin Analytics DERM</a></strong> analyses skin lesion images with 97 percent sensitivity for skin cancer detection. It has assessed 170,000+ NHS patients. NICE has recommended it for conditional use in the urgent skin cancer pathway, with the important caveat that dermatologist second-reads are mandatory for patients with black or brown skin tones.</p>
  <p><strong><a href="https://www.skinvision.com" target="_blank">SkinVision</a></strong> is a CE-marked Class IIa medical device used by 3 million+ users globally, with 87 percent sensitivity in clinical studies (92.1 percent for melanoma).</p>

  <h3>AI Administrative Tools</h3>
  <p><strong><a href="https://www.betterletter.ai" target="_blank">BetterLetter</a></strong> processes inbound clinical letters, matches them to patients, highlights key diagnoses, and proposes SNOMED codes using a human-in-the-loop approach where clinical coders review and confirm. <strong><a href="https://www.accurx.com/booking" target="_blank">AccuRx Booking</a></strong> has enabled over 1 million patients to self-book appointments.</p>

  <h2>Risk Classification for Common GP Practice AI</h2>

  <table style="width:100%;border-collapse:collapse;margin:1.5rem 0">
    <thead>
      <tr style="background:var(--red);color:white">
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">AI Tool / Function</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Risk Level</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Why</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI triage / symptom assessment (Klinik, eConsult, Ada Health)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Annex III explicitly covers AI for emergency triage and patient dispatch. Triage AI classifies patient urgency and directs care.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI diagnostic imaging (Skin Analytics DERM, SkinVision)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI-enabled medical device under both EU MDR and AI Act. Directly affects patient safety.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI clinical decision support (Ardens, iatroX)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>Potentially HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">If AI influences clinical decisions. May qualify as medical device under MDR depending on intended use.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI medical transcription (Anima, Accurx Scribe)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited to Potentially HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Transcription itself is limited risk. But if the tool auto-generates SNOMED codes used for clinical purposes, it edges toward high-risk.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI clinical coding (BetterLetter, OneAdvanced)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Human-in-the-loop approach with clinicians reviewing suggestions. Lower risk if final coding is always human-confirmed.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI appointment booking (AccuRx Booking)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Administrative tool. No clinical decision-making.</td>
      </tr>
    </tbody>
  </table>

  <h2>The Medical Device Overlap</h2>
  <p>Healthcare AI sits at the intersection of two regulatory frameworks: the EU AI Act and the EU Medical Device Regulation (MDR). Many AI tools used in GP practices — Klinik (Class IIa), Skin Analytics, SkinVision, Anima (Class I) — are already regulated as medical devices. The AI Act adds a layer on top.</p>
  <p>For AI-enabled medical devices classified under MDR, providers must comply with both MDR requirements (conformity assessment, notified body involvement, CE marking) and AI Act requirements (risk management, data governance, transparency, human oversight). The compliance deadline for medical device AI is August 2027 — one year later than the general AI Act deadline.</p>
  <p>This dual regulatory burden falls primarily on the vendors who develop these tools, not on GP practices. But practices need to understand that the tools they deploy must meet both standards.</p>

  <h2>What GP Practices Need to Do</h2>

  <h3>1. Know What AI You Use</h3>
  <p>Map every AI tool in your practice: triage systems, clinical decision support, transcription, coding, imaging, booking. Note which are registered medical devices and which are not.</p>

  <h3>2. Ensure AI Literacy (Required Since February 2025)</h3>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4</a> requires that staff operating AI systems understand how they work. For a GP practice, this means clinicians using AI triage, transcription, or diagnostic tools should understand what the AI does, what data it uses, and critically, where its limitations are. This is especially important for diagnostic AI — NICE's recommendation of mandatory dermatologist second-reads for Skin Analytics DERM in patients with darker skin tones illustrates why understanding AI limitations matters.</p>

  <h3>3. Maintain Human Oversight</h3>
  <p>This is the most important obligation for healthcare AI. High-risk AI systems must operate under meaningful human oversight. In practice:</p>
  <ul>
    <li>AI triage recommendations should be reviewed by a clinician, not acted upon blindly</li>
    <li>AI diagnostic results (skin lesion analysis, imaging) require clinical confirmation</li>
    <li>AI-generated clinical notes and SNOMED codes should be reviewed before being saved to the patient record</li>
    <li>Patients must be able to see a human clinician if they disagree with or are concerned about an AI assessment</li>
  </ul>

  <h3>4. Inform Patients</h3>
  <p>Patients must know when AI is being used in their care. This includes:</p>
  <ul>
    <li>Online triage tools should clearly state they are AI-powered</li>
    <li>If a skin lesion is assessed by AI before a dermatologist reviews it, the patient should be informed</li>
    <li>If a consultation is being transcribed by AI, the patient should be told</li>
    <li>Patients should have a mechanism to request a fully human assessment</li>
  </ul>

  <h3>5. Verify Your Vendors</h3>
  <p>The compliance burden sits primarily with the AI providers. But you should:</p>
  <ul>
    <li>Confirm your AI tools hold appropriate regulatory status (CE marking, MHRA registration, DTAC compliance)</li>
    <li>Ask vendors about their EU AI Act compliance roadmap</li>
    <li>Ensure data processing agreements are in place (GDPR + AI Act)</li>
    <li>Subscribe to vendor safety alerts and updates</li>
  </ul>

  <h3>6. Log and Report</h3>
  <p>For high-risk AI tools, maintain records of how the AI is used, document any incidents where the AI provided incorrect recommendations, and report serious incidents to the relevant authority (MHRA in the UK, notified bodies in the EU).</p>

  <h2>Can You Handle This Yourself?</h2>
  <p>Healthcare AI compliance is more involved than other industries covered in this series. While the technical compliance burden sits with your vendors, the deployer obligations — human oversight, patient information, incident logging, staff training — are more demanding for a GP practice than for a shop or salon.</p>
  <p>You would benefit from guidance if:</p>
  <ul>
    <li>You deploy AI triage that directly routes patients without clinical review</li>
    <li>You use AI diagnostic tools (imaging, skin analysis) in clinical pathways</li>
    <li>You are unsure whether your tools qualify as medical devices under MDR</li>
    <li>You want to formalise your AI governance and incident reporting processes</li>
  </ul>
  <p>Most GP practices will find that their vendors are already addressing the regulatory requirements. The practice's role is to use the tools responsibly, maintain human oversight, keep patients informed, and document their AI usage.</p>

  <h2>The Bottom Line</h2>
  <p>Healthcare AI is where the EU AI Act has its most significant impact. Triage, diagnostics, and clinical decision support are explicitly high-risk, and the regulatory requirements reflect the potential consequences of getting it wrong. For GP practices, the key message is: your vendors must ensure their tools are compliant, but you must ensure the tools are used with appropriate human oversight, that patients are informed, and that your team understands the AI's capabilities and limitations.</p>
  <p>This is not optional or aspirational compliance. Patient safety AI carries the highest regulatory expectations under the EU AI Act, and for good reason.</p>

  <div style="margin-top:2rem;padding:1.5rem;background:var(--red-light);border-radius:8px;font-size:0.9rem;line-height:1.8">
    <p style="margin:0 0 0.75rem 0"><strong>Sources and further reading:</strong></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://klinikhealthcaresolutions.com" target="_blank">Klinik Healthcare Solutions</a> — CE-marked AI triage for GP practices</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://econsult.net" target="_blank">eConsult</a> — 3,200+ GP practices, 28 million patients, AI triage</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ada.com" target="_blank">Ada Health</a> — UKCA-marked AI symptom checker</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ardens.org.uk" target="_blank">Ardens Clinical</a> — clinical decision support for 87% of English GP practices</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.animahealth.com" target="_blank">Anima (Annie AI Scribe)</a> — MHRA Class I, 400+ practices, 2M patients</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.accurx.com" target="_blank">Accurx Scribe</a> — AI transcription for 98% of Accurx practices (Tandem Health)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://skin-analytics.com" target="_blank">Skin Analytics DERM</a> — 97% sensitivity, 170,000+ NHS patients, NICE-recommended</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.skinvision.com" target="_blank">SkinVision</a> — CE Class IIa, 3M+ users, 87% sensitivity</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.betterletter.ai" target="_blank">BetterLetter</a> — AI clinical coding with human-in-the-loop</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III: High-Risk AI Systems (Official EU text)</a> — healthcare triage and diagnostics</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4: AI Literacy (Official EU text)</a> — mandatory since February 2025</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC11379845/" target="_blank">EU AI Act and Medical Device Regulation overlap</a> (PubMed Central)</p>
  </div>

  <p style="margin-top:2rem"><a href="../consultants.html" class="btn btn-primary">Find an AI Act Consultant →</a></p>
</article>
'''
write_page('blog/ai-act-gp-practices.html', page('GP Practices: Your AI Triage and Diagnostic Tools Are High-Risk Under the EU AI Act', 'AI Act compliance for GP practices. AI triage, diagnostics, clinical decision support, and medical transcription under EU regulation.', blog_post_9, '../'))

# ── Blog Post 10: Schools & Universities ──
blog_post_10 = '''
<article class="blog-post">
  <div class="breadcrumbs"><a href="../index.html">Home</a> <span>›</span> <a href="../blog.html">Blog</a> <span>›</span> AI Act for Schools</div>
  <h1>Schools and Universities: Most of Your AI Is High-Risk Under the EU AI Act</h1>
  <p class="meta">February 2026 · 14 min read · <span style="background:var(--red-light);color:var(--red);padding:0.15rem 0.5rem;border-radius:4px;font-size:0.8rem;font-weight:600">HIGH-RISK · Industry Use Case</span></p>

  <p>If you run a school, college, or university and use AI in any part of student assessment, admissions, or learning, this article matters. Education AI is <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">explicitly listed as high-risk in Annex III, Category 3</a> of the EU AI Act — one of the most detailed high-risk categories in the entire regulation.</p>
  <p>This is not a future concern. The prohibition on emotion recognition in education took effect in February 2025. AI literacy obligations are already in force. The full high-risk compliance deadline is <strong>August 2, 2026</strong>.</p>

  <h2>What the AI Act Actually Says About Education</h2>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III, Category 3</a> lists four specific types of high-risk AI in education:</p>
  <ul>
    <li><strong>3(a):</strong> AI systems intended to determine access to or assign persons to educational institutions — admissions algorithms, placement testing AI</li>
    <li><strong>3(b):</strong> AI systems intended to evaluate learning outcomes, including those that steer the learning process — automated grading, adaptive learning platforms, learning analytics</li>
    <li><strong>3(c):</strong> AI systems intended to assess the appropriate level of education an individual will receive — systems that place students in remedial or advanced tracks</li>
    <li><strong>3(d):</strong> AI systems intended to monitor and detect prohibited behaviour during tests — proctoring software, plagiarism detection with AI analysis</li>
  </ul>
  <p>That covers almost everything. If your AI tool grades, ranks, monitors, recommends, or decides anything about a student&rsquo;s educational path, it is almost certainly high-risk.</p>
  <p>There is a narrow exception under <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6" target="_blank">Article 6(3)</a> for AI that performs only &ldquo;narrow procedural tasks&rdquo; — for example, a tool that simply formats assignment submissions without scoring them. But the moment a system evaluates, ranks, or flags student work, it crosses into high-risk territory.</p>

  <h2>Emotion Recognition Is Banned in Schools</h2>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5" target="_blank">Article 5(1)(f)</a> prohibits AI systems that infer emotions from biometric data in educational institutions. This has been in force since <strong>February 2, 2025</strong>.</p>
  <p>This means schools cannot use facial recognition to assess student attention, voice analysis to measure engagement, or any biometric system that attempts to read how students are feeling. The only exceptions are for medical or safety purposes — detecting a student in medical distress, for example.</p>
  <p>If you have any attention-monitoring or engagement-tracking tools that use facial or voice analysis, they need to be removed. Now.</p>

  <h2>The AI Tools Schools and Universities Actually Use</h2>
  <p>Most educational institutions are already using AI across multiple areas. Here are the most common tools and what their AI does.</p>

  <h3>Proctoring and Exam Monitoring</h3>
  <p><strong><a href="https://web.respondus.com/he/lockdownbrowser/" target="_blank">Respondus LockDown Browser &amp; Monitor</a></strong> restricts student access to other applications during online tests, while the Monitor add-on uses AI to analyse audio and video for suspicious activity. In February 2024, the Ontario Privacy Commissioner found that McMaster University&rsquo;s use of Respondus Monitor violated student privacy protections — the software was using student data to improve its system without consent.</p>
  <p><strong><a href="https://www.proctorio.com" target="_blank">Proctorio</a></strong> offers remote proctoring with AI-powered eye-tracking, behaviour monitoring, browser tab tracking, and video/audio recording. These monitoring capabilities place it squarely within Annex III, Category 3(d).</p>
  <p><strong><a href="https://www.turnitin.com/products/examsoft" target="_blank">ExamSoft</a></strong> (a Turnitin subsidiary) provides secure online examinations with optional ExamMonitor and ExamID add-ons that use AI-driven behaviour detection during exams, including continuous audio and video recording with human review of flagged incidents.</p>

  <h3>Plagiarism Detection and AI Writing Detection</h3>
  <p><strong><a href="https://www.turnitin.com" target="_blank">Turnitin</a></strong> is the most widely used plagiarism detection platform in education. Its AI detection tool, Turnitin Clarity, identifies AI-generated content from models like ChatGPT and Claude. Pricing varies significantly — basic plagiarism detection costs $2.59–$2.71 per student, with AI detection as an add-on at $0.41–$0.48 per student. Pricing has been found to vary by up to 360% between institutions for the same service.</p>
  <p>Alternatives include <strong><a href="https://copyleaks.com" target="_blank">Copyleaks</a></strong> (99% AI detection accuracy across 30+ languages), <strong><a href="https://gptzero.me" target="_blank">GPTZero</a></strong> (purpose-built for educators), and <strong><a href="https://www.scribbr.com/plagiarism-checker/" target="_blank">Scribbr</a></strong> (uses the same database as Turnitin).</p>

  <h3>Adaptive Learning Platforms</h3>
  <p><strong><a href="https://www.century.tech" target="_blank">Century Tech</a></strong> uses AI, neuroscience, and learning science to create personalised learning pathways that constantly adapt to each student. Case studies report a 30% reduction in the attainment gap between disadvantaged students and their peers. This type of tool — AI that steers the learning process — falls directly under Annex III, Category 3(b).</p>
  <p><strong>Knewton</strong> (now integrated into major publishers like Pearson and Cengage) analyses student performance to create personalised learning paths. It identifies knowledge gaps and recommends content to close them. Again, this is AI evaluating and steering learning — high-risk by default.</p>

  <h3>Learning Management Systems with AI</h3>
  <p><strong>Canvas</strong> (by Instructure, which also owns Turnitin) is evolving into an AI-enabled learning hub with agentic AI features and modular add-ons. <strong>Blackboard</strong> (by Anthology) blends LMS, SIS, and CRM with embedded AI for personalised learning. <strong>D2L Brightspace</strong> offers Lumi Tutor, a student-facing AI tutor. Even <strong>Moodle</strong>, the open-source LMS, supports AI plugin integration.</p>
  <p>The risk classification of these platforms depends on how their AI features are used. If the AI merely organises content or schedules reminders, it is minimal risk. If it recommends learning paths, predicts student performance, or influences progression decisions, it is likely high-risk.</p>

  <h2>Risk Classification for Common Education AI</h2>

  <table style="width:100%;border-collapse:collapse;margin:1.5rem 0">
    <thead>
      <tr style="background:var(--red);color:white">
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">AI Tool / Function</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Risk Level</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Why</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Admissions algorithms / placement AI</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Annex III, Category 3(a): determines access to education.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Automated grading / AI marking (Turnitin, Gradescope)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Annex III, Category 3(b): evaluates learning outcomes.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Adaptive learning platforms (Century Tech, Knewton)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Annex III, Category 3(b): steers the learning process.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI proctoring (Proctorio, Respondus Monitor, ExamSoft)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Annex III, Category 3(d): monitors behaviour during tests.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI plagiarism / writing detection (Turnitin Clarity)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Annex III, Category 3(d): detects prohibited behaviour in assessments.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Predictive analytics (student performance, dropout risk)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Annex III, Category 3(b)/(c): influences educational decisions.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Emotion recognition in classrooms</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>PROHIBITED</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5" target="_blank">Article 5</a>: emotion recognition banned in education since Feb 2025.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI chatbot for student enquiries</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Must disclose AI interaction. Transparency obligation applies.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI scheduling / timetabling</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Administrative task. No evaluation of students.</td>
      </tr>
    </tbody>
  </table>

  <h2>What You Are Required to Do</h2>
  <p>As a school or university deploying high-risk AI, your obligations under <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26" target="_blank">Article 26</a> are substantial. Here is what is expected.</p>

  <h3>1. Audit Every AI Tool You Use</h3>
  <p>Create a complete inventory of every AI system in your institution. Document what it does, which Annex III category it falls under (3a, 3b, 3c, or 3d), who uses it, and what data it processes. Most institutions will be surprised by how many AI tools they are already running.</p>

  <h3>2. Remove Any Emotion Recognition Systems</h3>
  <p>If any of your tools attempt to infer student emotions from facial expressions, voice, or other biometric data, remove them immediately. This prohibition has been in force since February 2025. The only exception is medical or safety purposes.</p>

  <h3>3. Ensure Meaningful Human Oversight</h3>
  <p>High-risk AI systems in education must operate under meaningful human oversight. This means a qualified educator or administrator must review AI-generated grades, scores, admissions recommendations, and plagiarism flags before they become final decisions. The AI assists your staff — it does not replace their professional judgement.</p>

  <h3>4. Inform Students and Parents</h3>
  <p>You must tell students (and, where applicable, parents) that AI is being used in decisions that affect them. This includes explaining how proctoring software works, how plagiarism detection operates, how adaptive learning platforms make recommendations, and what role AI plays in admissions or grading.</p>

  <h3>5. Ensure AI Literacy Across Your Institution</h3>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4</a> requires that all staff involved in operating AI systems have sufficient AI literacy. Teachers using Turnitin need to understand how the AI detection works, what its false positive rate is, and when to override its results. Admissions staff using AI screening need to know its limitations. This obligation has been mandatory since February 2025.</p>

  <h3>6. Conduct Data Protection Impact Assessments</h3>
  <p>Under <a href="https://gdpr-info.eu/art-35-gdpr/" target="_blank">GDPR Article 35</a>, deploying high-risk AI that processes student data — especially data from minors — requires a Data Protection Impact Assessment (DPIA). Proctoring tools that record video and audio of students are particularly sensitive. If you do not have DPIAs for your AI tools, you need them.</p>

  <h3>7. Work With Your Software Providers</h3>
  <p>The heaviest technical obligations — risk management systems, conformity assessments, bias testing, CE marking — fall on the providers (the companies that build the AI). But you need to confirm your providers are preparing. Ask Turnitin, Proctorio, Century Tech, and every other AI vendor: are you conducting conformity assessments? Do you have technical documentation? Will you be ready by August 2026?</p>

  <h2>Can You Handle This Yourself?</h2>
  <p>Schools operate differently from businesses. Budget constraints are real, and compliance teams are rare. The good news is that most schools are <strong>deployers</strong>, not providers — you use existing AI tools rather than building your own. This significantly reduces your compliance burden.</p>
  <p>What you can do internally:</p>
  <ul>
    <li>Create your AI system inventory</li>
    <li>Implement transparency notices for students and parents</li>
    <li>Establish human review processes for AI-generated grades and flags</li>
    <li>Deliver AI literacy training to your staff</li>
  </ul>
  <p>Where you may need professional guidance:</p>
  <ul>
    <li>Conducting DPIAs for proctoring and assessment tools, especially those processing data from minors</li>
    <li>Reviewing contracts with AI providers to ensure they meet their provider obligations</li>
    <li>Assessing whether specific AI tools qualify for the Article 6(3) narrow procedural task exemption</li>
    <li>Preparing documentation that demonstrates compliance as a deployer</li>
  </ul>

  <h2>What &ldquo;Compliant&rdquo; Looks Like for a School</h2>
  <p>Consider a secondary school with 800 students using Turnitin for plagiarism detection, an adaptive learning platform for maths, and an AI-assisted admissions screening tool. Here is what compliance looks like by August 2026:</p>
  <ul>
    <li>You have documented every AI tool in use, its purpose, and which Annex III Category 3 subcategory it falls under</li>
    <li>Any emotion recognition tools have been removed</li>
    <li>Students and parents have been informed that AI is used in assessments, plagiarism detection, and admissions screening, with clear explanations of how each system works</li>
    <li>Every AI-generated plagiarism flag is reviewed by a teacher before any academic misconduct decision is made</li>
    <li>Admissions recommendations generated by AI are reviewed by human admissions staff before any offer or rejection</li>
    <li>All teaching staff using AI tools have completed AI literacy training covering how the tools work, their limitations, and known error rates</li>
    <li>DPIAs have been completed for all AI tools processing student data, with particular attention to proctoring tools recording minors</li>
    <li>You have written to each AI vendor confirming their compliance roadmap and have their responses on file</li>
    <li>You monitor AI system outputs for patterns of bias or inaccuracy and document any issues</li>
  </ul>

  <h2>The Penalties</h2>
  <p>Non-compliance with high-risk AI obligations can result in fines of up to <strong>&euro;15 million or 3% of annual turnover</strong>. For SMEs, the calculation uses whichever figure is lower, not higher — a meaningful protection for smaller institutions. Using prohibited AI (like emotion recognition in classrooms) carries fines of up to <strong>&euro;35 million or 7% of turnover</strong>.</p>
  <p>But for schools, the reputational risk may matter more than fines. Parents trust schools with their children&rsquo;s data and educational outcomes. Being found to use AI without transparency, oversight, or proper safeguards would be damaging in ways that go well beyond a regulatory penalty.</p>

  <h2>The Deadline</h2>
  <p>The emotion recognition prohibition and AI literacy requirements are already in force. The full high-risk system obligations under Annex III take effect on <strong>August 2, 2026</strong>. Schools that have not started preparing are already behind. The good news: as a deployer rather than a provider, your compliance path is more manageable than you might expect — but it requires action now, not in six months.</p>

  <div style="margin-top:2rem;padding:1.5rem;background:var(--red-light);border-radius:8px;font-size:0.9rem;line-height:1.8">
    <p style="margin:0 0 0.75rem 0"><strong>Sources and further reading:</strong></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III: High-Risk AI Systems</a> — Category 3 covers education and vocational training</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6" target="_blank">Article 6: Classification rules for high-risk AI</a></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26" target="_blank">Article 26: Deployer obligations</a></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5" target="_blank">Article 5: Prohibited AI practices</a> — includes emotion recognition in education</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4: AI Literacy</a> — mandatory since February 2025</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.digitaleducationcouncil.com/post/eu-ai-act-what-it-means-for-universities" target="_blank">EU AI Act: What It Means for Universities</a> (Digital Education Council)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://iscresearch.com/isl-magazine-the-eu-ai-act/" target="_blank">The EU AI Act: What School Leaders Need to Know</a> (ISC Research)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.turnitin.com" target="_blank">Turnitin</a> | <a href="https://web.respondus.com/he/lockdownbrowser/" target="_blank">Respondus</a> | <a href="https://www.century.tech" target="_blank">Century Tech</a></p>
    <p style="margin:0"><a href="https://gdpr-info.eu/art-35-gdpr/" target="_blank">GDPR Article 35: Data Protection Impact Assessment</a></p>
  </div>

  <p style="margin-top:2rem"><a href="../consultants.html" class="btn btn-primary">Find an AI Act Consultant &rarr;</a></p>
</article>
'''
write_page('blog/ai-act-schools-universities.html', page('Schools and Universities: Most of Your AI Is High-Risk Under the EU AI Act', 'AI Act compliance for schools and universities. Proctoring, grading, adaptive learning, and admissions AI are high-risk under Annex III.', blog_post_10, '../'))

# ── Blog Post 11: Marketing Agencies ──
blog_post_11 = '''
<article class="blog-post">
  <div class="breadcrumbs"><a href="../index.html">Home</a> <span>›</span> <a href="../blog.html">Blog</a> <span>›</span> AI Act for Marketing</div>
  <h1>Marketing Agencies: What the EU AI Act Means for Your AI-Generated Content and Ad Targeting</h1>
  <p class="meta">February 2026 · 12 min read · <span style="background:var(--gold-light);color:var(--gray-800);padding:0.15rem 0.5rem;border-radius:4px;font-size:0.8rem;font-weight:600">LIMITED RISK · Industry Use Case</span></p>

  <p>Marketing agencies live on AI. Content generation, image creation, ad targeting, customer segmentation, SEO optimisation — the tools you use every day are powered by it. The good news: most marketing AI falls into the <strong>limited risk</strong> or <strong>minimal risk</strong> categories under the EU AI Act. The bad news: that does not mean &ldquo;no obligations.&rdquo;</p>
  <p>There are specific transparency requirements that will affect how you create and publish content, how you deploy chatbots, and how you use AI for advertising. There are also prohibited practices that some agencies may already be skating close to. Here is what you need to know.</p>

  <h2>Where Marketing AI Sits in the Risk Framework</h2>
  <p>The EU AI Act uses a four-tier risk classification: prohibited, high-risk, limited risk, and minimal risk. Most marketing AI sits in the bottom two tiers, but there are important exceptions.</p>
  <p><strong>Minimal risk</strong> (no specific obligations): AI-powered SEO tools, content optimisation, email personalisation, basic analytics, and scheduling tools. These can be used freely.</p>
  <p><strong>Limited risk</strong> (transparency obligations): Chatbots, AI-generated content, deepfakes, and synthetic media. These require disclosure to the people interacting with them.</p>
  <p><strong>Prohibited</strong> (banned outright): Subliminal manipulation, exploitation of vulnerable groups, and deceptive techniques that materially distort decision-making. Some aggressive advertising tactics may cross this line.</p>

  <h2>The AI Tools Marketing Agencies Actually Use</h2>

  <h3>Content Generation</h3>
  <p><strong><a href="https://www.jasper.ai" target="_blank">Jasper AI</a></strong> (from $29/month) is one of the most popular AI writing assistants for marketing, offering 50+ content templates, Brand Voice consistency, and integration with Surfer SEO and Grammarly. <strong><a href="https://www.copy.ai" target="_blank">Copy.ai</a></strong> specialises in short-form copywriting with a freemium model (2,000 words/month free). Both are built on large language models like GPT-4 and Claude.</p>
  <p>Most agencies also use <strong>ChatGPT</strong>, <strong>Claude</strong>, or <strong>Gemini</strong> directly for brainstorming, drafting, and research. These are general-purpose AI (GPAI) models with their own set of obligations under the Act — primarily falling on the providers (OpenAI, Anthropic, Google), not on you as a downstream user.</p>

  <h3>Image and Video Generation</h3>
  <p><strong><a href="https://www.midjourney.com" target="_blank">Midjourney</a></strong> (from $10/month) and <strong>DALL-E 3</strong> (included in ChatGPT Plus at $20/month) are widely used for creating marketing visuals. <strong><a href="https://runwayml.com" target="_blank">Runway</a></strong> (from $12/month) handles AI video generation and editing. These tools produce synthetic media — content that looks real but is AI-generated — which triggers specific transparency obligations under the Act.</p>

  <h3>Ad Targeting and Optimisation</h3>
  <p><strong>Meta Advantage+</strong> uses AI to automate ad targeting, creative optimisation, and budget allocation across Facebook and Instagram. Meta has announced fully automated AI ads are expected by 2026. <strong>Google Ads AI Max</strong> rolled out 60+ AI-powered improvements in 2025, integrating AI into search advertising and audience targeting.</p>
  <p>Standard personalisation and audience segmentation through these platforms is not inherently high-risk. But AI-driven advertising that targets vulnerable populations or uses manipulative techniques crosses into prohibited territory.</p>

  <h3>Social Media Management</h3>
  <p><strong><a href="https://www.hootsuite.com" target="_blank">Hootsuite</a></strong> (from $99/month) includes OwlyWriter AI for caption generation and content repurposing. <strong><a href="https://sproutsocial.com" target="_blank">Sprout Social</a></strong> (from $199/month) offers 30+ AI-powered features including post suggestions, tone customisation, sentiment analysis, and automated tagging.</p>

  <h3>SEO and Content Optimisation</h3>
  <p><strong><a href="https://surferseo.com" target="_blank">Surfer SEO</a></strong> (from $79/month annually) and <strong><a href="https://www.clearscope.io" target="_blank">Clearscope</a></strong> (from $129/month) use AI for content optimisation and keyword research. These are minimal risk tools — they help you write better content but do not interact directly with consumers or make decisions about them.</p>

  <h2>The Three Rules Marketing Agencies Must Follow</h2>

  <h3>Rule 1: Disclose AI-Generated Content (Article 50)</h3>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50" target="_blank">Article 50</a> creates specific transparency obligations for AI-generated and manipulated content. These take full effect in <strong>August 2026</strong>.</p>
  <p><strong>For providers of AI content tools:</strong> Systems generating synthetic audio, images, video, or text must mark their outputs in a machine-readable format as artificially generated. This obligation falls on the tool makers (Midjourney, Runway, etc.), not on you.</p>
  <p><strong>For deployers (that&rsquo;s you):</strong></p>
  <ul>
    <li><strong>Deepfakes:</strong> If you publish AI-generated or manipulated image, audio, or video content that constitutes a deepfake, you must disclose it</li>
    <li><strong>AI-generated text:</strong> If you publish AI-generated text intended to inform the public on matters of public interest, you must disclose it</li>
    <li>There is a narrow exemption for &ldquo;artistic, creative, satirical, fictional, or analogous works&rdquo; — but commercial advertising does <strong>not</strong> qualify for this exemption</li>
  </ul>
  <p>In practice, this means: AI-generated product demonstration videos need disclosure. Synthetic spokesperson videos need disclosure. AI-generated images in advertising likely need disclosure. AI-written advertorials and sponsored content need disclosure.</p>

  <h3>Rule 2: Disclose Chatbots (Already in Force)</h3>
  <p>If you deploy chatbots for customer service, lead generation, or marketing engagement — on your own site or on behalf of clients — you must clearly disclose that users are interacting with AI. This has been enforceable since <strong>February 2, 2025</strong>.</p>
  <p>The disclosure must happen before or at the start of the interaction. Something like: &ldquo;Hi, I&rsquo;m an AI assistant. How can I help?&rdquo; No pretending the chatbot is human.</p>

  <h3>Rule 3: Do Not Cross Into Prohibited Territory (Article 5)</h3>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5" target="_blank">Article 5</a> bans AI practices that are considered unacceptable. Three of these are directly relevant to marketing:</p>
  <ul>
    <li><strong>Subliminal manipulation:</strong> AI systems using imperceptible visual or audio cues beyond conscious awareness to influence behaviour. Subliminal advertising is already illegal in most EU countries — the AI Act extends this explicitly to AI-generated content.</li>
    <li><strong>Behavioural distortion:</strong> AI systems deploying manipulative or deceptive techniques that materially distort a person&rsquo;s ability to make informed decisions.</li>
    <li><strong>Vulnerability exploitation:</strong> AI systems designed to exploit people&rsquo;s vulnerabilities based on age, disability, or socioeconomic situation. Example: AI detecting elderly users and targeting them with overpriced, unverified health products.</li>
  </ul>
  <p>Violations of Article 5 carry fines of up to <strong>&euro;35 million or 7% of global turnover</strong>. This is already in force.</p>

  <h2>AI Literacy Is Already Required</h2>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4</a> requires that staff who use or are affected by AI systems have sufficient AI literacy. For a marketing agency, this means your content creators, strategists, designers, and account managers all need to understand the AI tools they use — their capabilities, limitations, and risks.</p>
  <p>This does not require a formal certification. It means documented, role-specific training. A copywriter using Jasper needs to understand what the tool can and cannot do. A social media manager using Hootsuite&rsquo;s AI needs to know its limitations. An account director needs to understand the transparency obligations when presenting AI-generated work to clients.</p>
  <p>This obligation has been in force since <strong>February 2025</strong>. Full enforcement begins August 2026.</p>

  <h2>What About GPAI Models You Use?</h2>
  <p>General-purpose AI models like ChatGPT, Claude, and Gemini have their own set of obligations under <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53" target="_blank">Article 53</a>. These obligations primarily fall on the <strong>providers</strong> (OpenAI, Anthropic, Google), not on you as a downstream user.</p>
  <p>However, you should:</p>
  <ul>
    <li>Follow the acceptable use policies of the GPAI providers you use</li>
    <li>Respect copyright when using AI-generated content — the Act requires GPAI providers to establish policies respecting the EU Copyright Directive</li>
    <li>Not use GPAI outputs in ways that violate Article 5 prohibited practices</li>
  </ul>

  <h2>Risk Classification for Common Marketing AI</h2>

  <table style="width:100%;border-collapse:collapse;margin:1.5rem 0">
    <thead>
      <tr style="background:var(--navy);color:white">
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">AI Tool / Function</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Risk Level</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Key Obligation</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI content generation (Jasper, Copy.ai, ChatGPT)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Disclose AI-generated text when informing the public.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI image generation (Midjourney, DALL-E)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Disclose AI-generated images. Machine-readable marking required from provider.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI video / synthetic media (Runway, deepfakes)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Mandatory deepfake disclosure. No artistic exemption for commercial ads.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Marketing chatbots</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Disclose AI before or at start of interaction. Already in force.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">SEO tools (Surfer SEO, Clearscope)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">No specific obligations.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Email personalisation (Mailchimp AI, HubSpot)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">No specific obligations.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Ad targeting (Meta Advantage+, Google AI)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Standard targeting is fine. Manipulative targeting of vulnerable groups is prohibited.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Subliminal AI advertising techniques</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>PROHIBITED</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Banned under Article 5. Fines up to &euro;35M or 7% of turnover.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI targeting vulnerable populations with manipulative ads</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>PROHIBITED</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Banned under Article 5. Already in force.</td>
      </tr>
    </tbody>
  </table>

  <h2>What &ldquo;Compliant&rdquo; Looks Like for a Marketing Agency</h2>
  <p>Consider a mid-sized digital marketing agency with 20 staff, using Jasper for copywriting, Midjourney for visuals, ChatGPT for research, Hootsuite for social media, and Meta Advantage+ for ad campaigns. Here is what compliance looks like:</p>
  <ul>
    <li>You have documented which AI tools you use, their purpose, and their risk classification</li>
    <li>All client-facing chatbots clearly disclose that users are interacting with AI, before or at the start of the conversation</li>
    <li>AI-generated images in advertising are disclosed (a visible label or caption)</li>
    <li>AI-generated video content, especially synthetic spokespersons, includes prominent disclosure</li>
    <li>AI-written advertorials and sponsored content that could be mistaken for independent journalism include disclosure</li>
    <li>Your team has completed AI literacy training covering the tools they use, their limitations, and the transparency obligations</li>
    <li>You have reviewed your ad campaigns to ensure none target vulnerable populations with manipulative techniques</li>
    <li>Client contracts include clauses about AI use, disclosure responsibilities, and compliance obligations</li>
    <li>You have a content review process that checks whether AI-generated material needs disclosure before publication</li>
    <li>You respect copyright when using GPAI tools and follow the providers&rsquo; acceptable use policies</li>
  </ul>

  <h2>What About Your Clients?</h2>
  <p>If you produce AI-generated content for clients, both you and your client may have transparency obligations. Clarify in your contracts who is responsible for disclosure. If you hand a client an AI-generated video for their website, they need to know it requires disclosure — and ideally, you should provide them with the appropriate labelling.</p>

  <h2>The Penalties</h2>
  <p>For prohibited practices (subliminal manipulation, vulnerability exploitation): fines of up to <strong>&euro;35 million or 7% of global turnover</strong>. For transparency violations (failing to disclose AI-generated content or chatbots): fines of up to <strong>&euro;15 million or 3% of turnover</strong>. For SMEs, the calculation uses whichever figure is lower.</p>
  <p>The commercial risk is also real. As consumers become more aware of AI-generated content, agencies that are transparent will build trust. Those caught using undisclosed AI — or worse, manipulative AI — will lose clients.</p>

  <h2>The Timeline</h2>
  <p><strong>Already in force (February 2025):</strong> Article 5 prohibited practices, Article 4 AI literacy, chatbot disclosure obligations.</p>
  <p><strong>August 2025:</strong> General-purpose AI provider obligations (Article 53).</p>
  <p><strong>August 2026:</strong> Full enforcement of AI literacy requirements. Article 50 transparency obligations for AI-generated content take effect. The final Code of Practice on AI-Generated Content marking is expected by June 2026.</p>
  <p>Marketing agencies that start building disclosure workflows and AI governance now will be well ahead of the curve. The compliance burden is lighter than for high-risk industries — but it is not zero.</p>

  <div style="margin-top:2rem;padding:1.5rem;background:var(--gold-light);border-radius:8px;font-size:0.9rem;line-height:1.8">
    <p style="margin:0 0 0.75rem 0"><strong>Sources and further reading:</strong></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50" target="_blank">Article 50: Transparency obligations for AI-generated content</a></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5" target="_blank">Article 5: Prohibited AI practices</a></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4: AI Literacy</a></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53" target="_blank">Article 53: General-purpose AI obligations</a></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content" target="_blank">Code of Practice on AI-Generated Content Marking &amp; Labelling</a> (European Commission)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.jasper.ai" target="_blank">Jasper AI</a> | <a href="https://www.midjourney.com" target="_blank">Midjourney</a> | <a href="https://runwayml.com" target="_blank">Runway</a> | <a href="https://www.hootsuite.com" target="_blank">Hootsuite</a> | <a href="https://sproutsocial.com" target="_blank">Sprout Social</a></p>
    <p style="margin:0"><a href="https://surferseo.com" target="_blank">Surfer SEO</a> | <a href="https://www.clearscope.io" target="_blank">Clearscope</a></p>
  </div>

  <p style="margin-top:2rem"><a href="../consultants.html" class="btn btn-primary">Find an AI Act Consultant &rarr;</a></p>
</article>
'''
write_page('blog/ai-act-marketing-agencies.html', page('Marketing Agencies: What the EU AI Act Means for Your AI-Generated Content and Ad Targeting', 'AI Act compliance for marketing agencies. AI content generation, deepfakes, chatbots, ad targeting, and transparency obligations under EU regulation.', blog_post_11, '../'))

# ── Blog Post 12: Insurance Companies ──
blog_post_12 = '''
<article class="blog-post">
  <div class="breadcrumbs"><a href="../index.html">Home</a> <span>›</span> <a href="../blog.html">Blog</a> <span>›</span> AI Act for Insurance</div>
  <h1>Insurance Companies: Your Underwriting and Claims AI Is High-Risk Under the EU AI Act</h1>
  <p class="meta">February 2026 · 13 min read · <span style="background:var(--red-light);color:var(--red);padding:0.15rem 0.5rem;border-radius:4px;font-size:0.8rem;font-weight:600">HIGH-RISK · Industry Use Case</span></p>

  <p>If you are an insurance company, broker, or insurtech using AI for underwriting, risk pricing, or claims processing, the EU AI Act has you directly in its sights. Insurance AI is <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">explicitly listed as high-risk in Annex III, Category 5</a> — the same category that covers credit scoring, access to essential services, and financial decision-making that affects people&rsquo;s lives.</p>
  <p>This is not a grey area. AI used for risk assessment and pricing in life and health insurance is specifically named. The compliance requirements are substantial, and the deadline — <strong>August 2, 2026</strong> — leaves little room for delay.</p>

  <h2>What the AI Act Actually Says About Insurance</h2>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III, Category 5</a> covers AI systems used in access to and enjoyment of essential private services and essential public services and benefits. Two subcategories are directly relevant to insurance:</p>
  <ul>
    <li><strong>5(b):</strong> AI systems intended to evaluate the creditworthiness of natural persons or establish their credit score, <em>with the exception of AI systems used for the purpose of detecting financial fraud</em></li>
    <li><strong>5(c):</strong> AI systems intended for risk assessment and pricing in relation to natural persons in the case of life and health insurance</li>
  </ul>
  <p>This means: if your AI system determines whether someone gets insurance, how much they pay, or whether their claim is approved — and it affects life or health coverage — it is high-risk. The fraud detection exception in 5(b) is notable: AI used purely for fraud detection is not classified as high-risk under this category, though it still needs to operate within the law.</p>

  <h2>The AI Tools Insurance Companies Actually Use</h2>

  <h3>Claims Processing and Automation</h3>
  <p><strong><a href="https://www.lemonade.com" target="_blank">Lemonade</a></strong> is an AI-first insurance platform where 55% of claims are fully automated and 40% require zero human intervention. Their chatbot &ldquo;Jim&rdquo; uses dozens of anti-fraud algorithms and has processed a claim in as little as 2 seconds. This level of automation, while impressive, means Lemonade&rsquo;s AI is making decisions that directly affect policyholders&rsquo; access to insurance benefits.</p>
  <p><strong><a href="https://tractable.ai" target="_blank">Tractable</a></strong> uses computer vision to assess vehicle and property damage from photographs, handling approximately $2 billion worth of vehicle repairs annually and assisting over 1 million clients. Their AI provides damage estimates with certainty scores, enabling up to 10x reduction in claim resolution time.</p>

  <h3>Fraud Detection</h3>
  <p><strong><a href="https://www.shift-technology.com" target="_blank">Shift Technology</a></strong> offers an AI decision automation platform specifically for insurance fraud detection. Their &ldquo;Force&rdquo; platform achieves a 75% hit rate for fraud detection, identifies twice as much potential fraud as competitors, and has flagged over $5 billion in fraudulent claims. They serve approximately 100 customers across 25 countries, including Generali France and Mitsui Sumitomo.</p>
  <p>Importantly, fraud detection AI benefits from the <strong>Article 5(b) exception</strong> — it is not classified as high-risk under the creditworthiness category. However, if your fraud detection system also influences claim decisions or coverage eligibility, it may still be caught by Category 5(c).</p>

  <h3>Underwriting and Risk Pricing</h3>
  <p><strong><a href="https://www.zest.ai" target="_blank">Zest AI</a></strong> offers machine learning underwriting that uses 300+ data variables compared to the industry standard of approximately 20. They report a 20% average increase in approval rates with no added risk and up to 5x increase in automated approvals. While primarily focused on credit lending, their model management system applies to insurance underwriting as well.</p>
  <p>Core insurance platforms like <strong><a href="https://www.duckcreek.com" target="_blank">Duck Creek</a></strong> (200+ carriers globally) and <strong><a href="https://www.guidewire.com" target="_blank">Guidewire</a></strong> (450+ customers globally) increasingly embed AI for risk selection, pricing optimisation, and claims triage. Duck Creek has implemented AI testing protocols for algorithmic fairness in automated underwriting — a sign that the industry is already moving toward compliance.</p>

  <h3>Telematics and Usage-Based Insurance</h3>
  <p>AI-powered telematics analyse driving behaviour, health data from wearables, and IoT sensor data to personalise premiums. This data-intensive approach to pricing sits squarely within the high-risk classification because it directly determines what individuals pay for their insurance.</p>

  <h2>Risk Classification for Common Insurance AI</h2>

  <table style="width:100%;border-collapse:collapse;margin:1.5rem 0">
    <thead>
      <tr style="background:var(--red);color:white">
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">AI Tool / Function</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Risk Level</th>
        <th style="padding:0.75rem;text-align:left;border:1px solid var(--gray-200)">Why</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI underwriting / risk pricing (Zest AI, Duck Creek, Guidewire)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Annex III, Category 5(c): risk assessment and pricing for life and health insurance.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI credit scoring for insurance eligibility</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Annex III, Category 5(b): creditworthiness evaluation affecting access to services.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI claims decisions (Lemonade, automated approval/denial)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Determines access to insurance benefits. Falls under Category 5(c).</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI telematics / usage-based pricing</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Directly determines premiums based on personal behaviour data.</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI damage assessment (Tractable)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200);color:var(--red)"><strong>HIGH-RISK</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Influences claim settlement amounts. Affects access to insurance benefits.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">AI fraud detection (Shift Technology)</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Exempt*</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Category 5(b) explicitly exempts fraud detection. *But if fraud flags influence coverage decisions, may still be high-risk under 5(c).</td>
      </tr>
      <tr>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Customer service chatbot</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Limited</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Must disclose AI interaction. Transparency obligation applies.</td>
      </tr>
      <tr style="background:var(--gray-50)">
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">Internal analytics / reporting AI</td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)"><strong>Minimal</strong></td>
        <td style="padding:0.75rem;border:1px solid var(--gray-200)">No direct impact on individuals. No specific obligations.</td>
      </tr>
    </tbody>
  </table>

  <h2>What You Are Required to Do</h2>
  <p>As an insurance company deploying high-risk AI, your obligations under <a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26" target="_blank">Article 26</a> are among the most demanding in the Act. Here is what is expected.</p>

  <h3>1. Conduct a Fundamental Rights Impact Assessment</h3>
  <p>Before first use of high-risk AI in financial services, you must conduct a <strong>Fundamental Rights Impact Assessment (FRIA)</strong>. This goes beyond a standard DPIA. You need to identify which demographic groups are likely to be affected, quantify disparate-impact ratios, evaluate privacy-intrusive features, and assess whether the AI system could result in discriminatory pricing or denial of essential coverage.</p>

  <h3>2. Ensure Human Oversight</h3>
  <p>High-risk AI systems must operate under meaningful human oversight. Assign trained personnel with the competence, training, and authority to oversee AI decisions. This means a qualified underwriter or claims handler must review AI-generated recommendations, especially for coverage denials, high-value claims, and unusual risk assessments. The AI assists your team — it does not replace their judgement.</p>

  <h3>3. Maintain Decision Logs</h3>
  <p>You must maintain logs automatically generated by the AI system for a <strong>minimum of 6 months</strong> (or longer as appropriate). These logs must allow full reconstruction of how the system reached specific decisions. This is critical for claims disputes, bias investigations, and regulatory inspections. If a customer challenges an AI-driven premium or claim decision, you need to be able to explain exactly how the system arrived at that result.</p>

  <h3>4. Inform Policyholders</h3>
  <p>You must inform individuals that they are subject to high-risk AI systems. This notification must happen before or during the decision-making process. Policyholders have the right to know that AI is involved in their underwriting, pricing, or claims assessment, and to understand what role it plays.</p>

  <h3>5. Ensure AI Literacy</h3>
  <p><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4</a> requires that all personnel who build, operate, or use AI systems have role-based AI literacy training. Underwriters need to understand how the AI pricing model works. Claims handlers need to know when to override AI recommendations. Compliance officers need to understand the regulatory framework. This has been mandatory since February 2025.</p>

  <h3>6. Monitor for Bias and Discrimination</h3>
  <p>Insurance AI that determines pricing based on personal data carries inherent risks of discrimination. You must continuously monitor your AI systems for discriminatory outcomes across demographic groups, track approval and denial rates by protected characteristics, and document remediation of any discriminatory patterns identified.</p>

  <h3>7. Work With Your Technology Providers</h3>
  <p>If you use third-party AI platforms (Shift Technology, Tractable, Zest AI, Duck Creek, Guidewire), the heaviest technical obligations — risk management systems, conformity assessments, bias testing, technical documentation — fall on them as providers. But you need to verify they are preparing. Request their compliance documentation. Confirm their conformity assessment timelines. Ensure your contracts require them to support your compliance as a deployer.</p>

  <h2>Can You Handle This Yourself?</h2>
  <p>Insurance compliance is already heavily regulated (Solvency II, IDD, GDPR). Adding the AI Act creates another layer, but many of the concepts — risk management, documentation, governance, consumer protection — are familiar. The AI Act does introduce new requirements that may require specialist support:</p>
  <ul>
    <li>Conducting Fundamental Rights Impact Assessments (a new concept distinct from DPIAs)</li>
    <li>Algorithmic fairness testing and bias monitoring across demographic groups</li>
    <li>Interpreting whether specific AI tools qualify for the fraud detection exemption</li>
    <li>Preparing deployer documentation that satisfies both the AI Act and existing regulatory frameworks</li>
  </ul>
  <p>For smaller brokers using one or two AI tools, the compliance effort is manageable with guidance. For larger insurers or insurtechs with AI embedded across underwriting, claims, and customer service, a dedicated AI governance programme is advisable.</p>

  <h2>What &ldquo;Compliant&rdquo; Looks Like for an Insurance Company</h2>
  <p>Consider a mid-sized insurer using Zest AI for underwriting, Tractable for claims damage assessment, Shift Technology for fraud detection, and a chatbot for customer service. Here is what compliance looks like by August 2026:</p>
  <ul>
    <li>You have documented every AI system in use, its purpose, and which Annex III Category 5 subcategory it falls under</li>
    <li>A Fundamental Rights Impact Assessment has been completed for all underwriting and pricing AI, identifying affected demographic groups and potential discriminatory outcomes</li>
    <li>Every AI-generated underwriting decision, premium calculation, and claim assessment is reviewed by a qualified human before becoming final — especially coverage denials</li>
    <li>Decision logs are maintained for at least 6 months, allowing full reconstruction of how AI reached each decision</li>
    <li>Policyholders are informed that AI is used in their underwriting, pricing, and claims processes, with clear explanations of its role</li>
    <li>All relevant staff have completed AI literacy training covering how the tools work, their limitations, and when to override</li>
    <li>You continuously monitor AI outputs for bias and discrimination, with documented processes for remediation</li>
    <li>Fraud detection AI (Shift Technology) is documented as exempt under Category 5(b), but monitored to ensure it does not indirectly influence coverage decisions</li>
    <li>Your customer service chatbot clearly discloses that users are interacting with AI</li>
    <li>You have verified your technology providers&rsquo; AI Act compliance roadmaps and have their documentation on file</li>
  </ul>

  <h2>The Penalties</h2>
  <p>Non-compliance with high-risk AI obligations can result in fines of up to <strong>&euro;15 million or 3% of global annual turnover</strong>, whichever is higher for large companies. For SMEs, the calculation uses whichever figure is lower. Insurance companies also face the usual regulatory risks: licence conditions, supervisory actions from national insurance authorities, and potential civil claims from policyholders affected by non-compliant AI decisions.</p>
  <p>The compounding effect is significant. An insurer using AI that discriminates in pricing could face AI Act fines, GDPR fines (for automated decision-making without proper safeguards under Article 22), and civil litigation from affected policyholders — simultaneously.</p>

  <h2>The Deadline</h2>
  <p>AI literacy requirements and prohibited practices have been in force since February 2025. The full high-risk system obligations under Annex III take effect on <strong>August 2, 2026</strong>. Insurance companies that have not started their AI governance programmes are working against a tight timeline. The complexity of insurance regulation means that layering AI Act compliance onto existing frameworks (Solvency II, IDD, GDPR) requires careful planning — starting now.</p>

  <div style="margin-top:2rem;padding:1.5rem;background:var(--red-light);border-radius:8px;font-size:0.9rem;line-height:1.8">
    <p style="margin:0 0 0.75rem 0"><strong>Sources and further reading:</strong></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3" target="_blank">Annex III: High-Risk AI Systems</a> — Category 5 covers essential services including insurance</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26" target="_blank">Article 26: Deployer obligations</a></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6" target="_blank">Article 6: Classification rules for high-risk AI</a></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4" target="_blank">Article 4: AI Literacy</a></p>
    <p style="margin:0 0 0.25rem 0"><a href="https://hdsr.mitpress.mit.edu/pub/19cwd6qx" target="_blank">The Future of Credit Underwriting and Insurance Under the EU AI Act</a> (Harvard Data Science Review)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://bluearrow.ai/ai-act-and-insurance/" target="_blank">How the EU AI Act Will Impact Insurance</a> (Blue Arrow)</p>
    <p style="margin:0 0 0.25rem 0"><a href="https://www.shift-technology.com" target="_blank">Shift Technology</a> | <a href="https://tractable.ai" target="_blank">Tractable</a> | <a href="https://www.zest.ai" target="_blank">Zest AI</a> | <a href="https://www.lemonade.com" target="_blank">Lemonade</a></p>
    <p style="margin:0"><a href="https://www.duckcreek.com" target="_blank">Duck Creek</a> | <a href="https://www.guidewire.com" target="_blank">Guidewire</a></p>
  </div>

  <p style="margin-top:2rem"><a href="../consultants.html" class="btn btn-primary">Find an AI Act Consultant &rarr;</a></p>
</article>
'''
write_page('blog/ai-act-insurance-companies.html', page('Insurance Companies: Your Underwriting and Claims AI Is High-Risk Under the EU AI Act', 'AI Act compliance for insurance companies. Underwriting, risk pricing, claims processing, and fraud detection AI under EU regulation.', blog_post_12, '../'))

# Update blog index to include all posts
blog_body = '''
<div class="static-page">
  <h1>AI Act Resources</h1>
  <p>Guides, analysis, and updates on EU AI Act compliance.</p>
  <div class="blog-list">
    <div class="blog-card">
      <h2><a href="blog/ai-act-insurance-companies.html">Insurance Companies: Your Underwriting and Claims AI Is High-Risk</a></h2>
      <p class="meta">February 2026 · <span style="background:var(--red-light);color:var(--red);padding:0.1rem 0.4rem;border-radius:4px;font-size:0.75rem;font-weight:600">HIGH-RISK · Industry Use Case</span></p>
      <p>Lemonade, Tractable, Shift Technology, Zest AI — insurance AI for underwriting, claims, and risk pricing is explicitly high-risk under Annex III Category 5.</p>
    </div>
    <div class="blog-card">
      <h2><a href="blog/ai-act-marketing-agencies.html">Marketing Agencies: AI-Generated Content and Ad Targeting Under the EU AI Act</a></h2>
      <p class="meta">February 2026 · <span style="background:var(--gold-light);color:var(--gray-800);padding:0.1rem 0.4rem;border-radius:4px;font-size:0.75rem;font-weight:600">LIMITED RISK · Industry Use Case</span></p>
      <p>Jasper, Midjourney, ChatGPT, Meta Advantage+ — most marketing AI is limited risk, but transparency obligations and prohibited practices still apply.</p>
    </div>
    <div class="blog-card">
      <h2><a href="blog/ai-act-schools-universities.html">Schools and Universities: Most of Your AI Is High-Risk</a></h2>
      <p class="meta">February 2026 · <span style="background:var(--red-light);color:var(--red);padding:0.1rem 0.4rem;border-radius:4px;font-size:0.75rem;font-weight:600">HIGH-RISK · Industry Use Case</span></p>
      <p>Turnitin, Proctorio, Century Tech, adaptive learning — education AI is one of the most detailed high-risk categories in the entire EU AI Act.</p>
    </div>
    <div class="blog-card">
      <h2><a href="blog/ai-act-gp-practices.html">GP Practices: Your AI Triage and Diagnostic Tools Are High-Risk</a></h2>
      <p class="meta">February 2026 · <span style="background:var(--red-light);color:var(--red);padding:0.1rem 0.4rem;border-radius:4px;font-size:0.75rem;font-weight:600">HIGH-RISK · Industry Use Case</span></p>
      <p>Klinik, eConsult, Skin Analytics DERM, Anima — GP practice AI directly affects patient safety. Healthcare AI carries the highest regulatory requirements under the EU AI Act.</p>
    </div>
    <div class="blog-card">
      <h2><a href="blog/ai-act-accountants.html">Accountants: What the EU AI Act Means for Your Practice</a></h2>
      <p class="meta">February 2026 · <span style="background:var(--gold-light);color:var(--gray-800);padding:0.1rem 0.4rem;border-radius:4px;font-size:0.75rem;font-weight:600">Industry Use Case</span></p>
      <p>Xero, QuickBooks, Sage, and Dext all use AI. Most accounting AI is minimal risk, but credit scoring and AML screening deserve attention.</p>
    </div>
    <div class="blog-card">
      <h2><a href="blog/ai-act-ecommerce-shops.html">E-Commerce Shops: What the EU AI Act Means for Your Online Store</a></h2>
      <p class="meta">February 2026 · <span style="background:var(--gold-light);color:var(--gray-800);padding:0.1rem 0.4rem;border-radius:4px;font-size:0.75rem;font-weight:600">Industry Use Case</span></p>
      <p>Product recommendations, chatbots, dynamic pricing, and Klarna — e-commerce AI is everywhere. Most is low-risk, but BNPL credit scoring is explicitly high-risk.</p>
    </div>
    <div class="blog-card">
      <h2><a href="blog/ai-act-estate-agents.html">Estate Agents: Your AI Valuation Tools Could Be High-Risk</a></h2>
      <p class="meta">February 2026 · <span style="background:var(--gold-light);color:var(--gray-800);padding:0.1rem 0.4rem;border-radius:4px;font-size:0.75rem;font-weight:600">Potentially HIGH-RISK · Industry Use Case</span></p>
      <p>Hometrack, PriceHubble, Reapit AI, and Nurtur — estate agency AI is growing fast. Automated valuations and tenant screening may cross into high-risk territory.</p>
    </div>
    <div class="blog-card">
      <h2><a href="blog/ai-act-restaurants-cafes.html">Restaurant Owners: Is Your AI Ordering System Compliant?</a></h2>
      <p class="meta">February 2026 · <span style="background:var(--gold-light);color:var(--gray-800);padding:0.1rem 0.4rem;border-radius:4px;font-size:0.75rem;font-weight:600">Industry Use Case</span></p>
      <p>Toast, Popmenu, SevenRooms, and Lineup.ai — restaurant AI is everywhere. Here is what the EU AI Act means for your restaurant and what you need to do.</p>
    </div>
    <div class="blog-card">
      <h2><a href="blog/ai-act-recruitment-agencies.html">Recruitment Agencies: Why Your AI Hiring Tools Are High-Risk</a></h2>
      <p class="meta">February 2026 · <span style="background:var(--red-light);color:var(--red);padding:0.1rem 0.4rem;border-radius:4px;font-size:0.75rem;font-weight:600">HIGH-RISK · Industry Use Case</span></p>
      <p>CV screening, candidate scoring, and video interviewing tools are explicitly high-risk under Annex III. Here is what recruitment agencies need to do before August 2026.</p>
    </div>
    <div class="blog-card">
      <h2><a href="blog/ai-act-hairdressers-beauty-salons.html">Does the EU AI Act Apply to My Hair Salon?</a></h2>
      <p class="meta">February 2026 · <span style="background:var(--gold-light);color:var(--gray-800);padding:0.1rem 0.4rem;border-radius:4px;font-size:0.75rem;font-weight:600">Industry Use Case</span></p>
      <p>You use Fresha or Booksy? That is AI. Here is what the EU AI Act means for hairdressers and beauty salons — and what you actually need to do.</p>
    </div>
    <div class="blog-card">
      <h2><a href="blog/eu-ai-act-penalties-2026.html">EU AI Act Penalties: What Your Company Faces in 2026</a></h2>
      <p class="meta">February 2026</p>
      <p>Understanding the three-tier penalty structure, real enforcement actions, and why compliance costs far less than the alternative.</p>
    </div>
    <div class="blog-card">
      <h2><a href="blog/eu-ai-act-compliance-guide-smes.html">EU AI Act Compliance Guide for SMEs</a></h2>
      <p class="meta">February 2026</p>
      <p>A practical guide for small and medium enterprises navigating EU AI Act compliance requirements, risk classification, and next steps.</p>
    </div>
  </div>
</div>
'''
write_page('blog.html', page('AI Act Resources & Blog', 'Guides and analysis on EU AI Act compliance. Practical resources for businesses navigating AI regulation.', blog_body))

# ── 404 Page ──
page_404 = '''
<div class="static-page" style="text-align:center;padding:4rem 1.5rem">
  <h1 style="font-size:4rem;color:var(--navy);margin-bottom:0.5rem">404</h1>
  <p style="font-size:1.2rem;color:var(--gray-500);margin-bottom:2rem">This page could not be found.</p>
  <p>Looking for an AI Act consultant? Try browsing our directory.</p>
  <div style="margin-top:1.5rem;display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
    <a href="/index.html" class="btn btn-primary">Homepage</a>
    <a href="/consultants.html" class="btn btn-secondary">All Consultants</a>
    <a href="/countries.html" class="btn btn-secondary">By Country</a>
  </div>
</div>
'''
write_page('404.html', page('Page Not Found', 'The page you are looking for could not be found.', page_404))

# ── Simulator Page: "What Does the AI Act Mean for MY Business?" ──
simulator_page = '''
<style>
.sim-wrap .container{{max-width:900px;margin:0 auto;padding:2rem 1.5rem}}
.sim-wrap h1{{text-align:center;font-size:2rem;margin-bottom:0.5rem;color:#1B2A4A}}
.sim-wrap .subtitle{{text-align:center;color:#6b7280;margin-bottom:2.5rem;font-size:1.05rem}}
.sim-wrap .industry-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-bottom:2rem}}
.sim-wrap .industry-tile{{background:#fff;border:2px solid #e5e7eb;border-radius:14px;padding:1.25rem 1rem;text-align:center;cursor:pointer;transition:all 0.2s}}
.sim-wrap .industry-tile:hover{{border-color:#C9A84C;transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,0.08)}}
.sim-wrap .industry-tile .icon{{font-size:2.2rem;margin-bottom:0.5rem}}
.sim-wrap .industry-tile .label{{font-size:0.85rem;font-weight:600;color:#1B2A4A}}
.sim-wrap .industry-tile .risk-badge{{display:inline-block;font-size:0.65rem;font-weight:700;padding:0.1rem 0.4rem;border-radius:4px;margin-top:0.4rem}}
.sim-wrap .risk-high{{background:#fde8e8;color:#c0392b}}
.sim-wrap .risk-limited{{background:#fef3cd;color:#856404}}
.sim-wrap .risk-minimal{{background:#d4edda;color:#155724}}
.sim-wrap #activities-section{{display:none;animation:fadeIn 0.3s ease}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
.sim-wrap .activities-header{{margin-bottom:1.5rem}}
.sim-wrap .activities-header h2{{font-size:1.4rem;color:#1B2A4A;margin-bottom:0.25rem}}
.sim-wrap .activities-header p{{color:#6b7280;font-size:0.95rem}}
.sim-wrap .activity-list{{display:flex;flex-direction:column;gap:0.6rem;margin-bottom:2rem}}
.sim-wrap .activity-card{{background:#fff;border:2px solid #e5e7eb;border-radius:12px;padding:1rem 1.15rem;display:flex;align-items:flex-start;gap:0.75rem;cursor:pointer;transition:all 0.15s}}
.sim-wrap .activity-card:hover{{border-color:#C9A84C}}
.sim-wrap .activity-card.checked{{border-color:#1B2A4A;background:#f8faff}}
.sim-wrap .activity-card .checkbox{{width:22px;height:22px;border:2px solid #d1d5db;border-radius:6px;flex-shrink:0;margin-top:1px;display:flex;align-items:center;justify-content:center;transition:all 0.15s}}
.sim-wrap .activity-card.checked .checkbox{{background:#1B2A4A;border-color:#1B2A4A}}
.sim-wrap .activity-card.checked .checkbox::after{{content:'\2713';color:#fff;font-size:0.8rem;font-weight:700}}
.sim-wrap .activity-info{{flex:1}}
.sim-wrap .activity-name{{font-weight:600;font-size:0.95rem;color:#1B2A4A}}
.sim-wrap .activity-annex{{font-size:0.75rem;color:#6b7280;margin-top:0.1rem}}
.sim-wrap .activity-risk{{display:inline-block;font-size:0.65rem;font-weight:700;padding:0.1rem 0.35rem;border-radius:3px;margin-top:0.3rem}}
.sim-wrap .risk-prohibited{{background:#fde8e8;color:#c0392b}}
.sim-wrap .btn-primary{{display:inline-block;background:#1B2A4A;color:#fff;padding:0.7rem 2rem;border-radius:10px;font-weight:600;font-size:1rem;border:none;cursor:pointer;text-decoration:none;font-family:inherit}}
.sim-wrap .btn-primary:hover{{background:#2a3d6b}}
.sim-wrap .btn-secondary{{display:inline-block;background:#f3f4f6;color:#374151;border:1px solid #d1d5db;padding:0.5rem 1.25rem;border-radius:10px;font-weight:600;font-size:0.9rem;cursor:pointer;text-decoration:none;font-family:inherit}}
.sim-wrap .btn-secondary:hover{{background:#e5e7eb}}
.sim-wrap .btn-row{{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin-top:1.5rem}}
.sim-wrap #results-section{{display:none;animation:fadeIn 0.4s ease}}
.sim-wrap .results-summary{{background:linear-gradient(135deg,#1B2A4A 0%,#2a3d6b 100%);color:#fff;border-radius:16px;padding:2rem;margin-bottom:2rem}}
.sim-wrap .results-summary h2{{font-size:1.3rem;margin-bottom:0.5rem}}
.sim-wrap .results-summary .industry-name{{color:#C9A84C;font-weight:700}}
.sim-wrap .results-summary p{{opacity:0.9;font-size:0.95rem;line-height:1.6}}
.sim-wrap .overall-risk{{display:inline-block;padding:0.3rem 0.8rem;border-radius:6px;font-weight:700;font-size:0.85rem;margin-top:0.75rem}}
.sim-wrap .overall-prohibited{{background:#c0392b;color:#fff}}
.sim-wrap .overall-high{{background:#e74c3c;color:#fff}}
.sim-wrap .overall-limited{{background:#f39c12;color:#fff}}
.sim-wrap .overall-minimal{{background:#27ae60;color:#fff}}
.sim-wrap .risk-breakdown{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin-bottom:2rem}}
.sim-wrap .risk-group{{background:#fff;border-radius:14px;padding:1.25rem;border-left:4px solid}}
.sim-wrap .risk-group.prohibited{{border-color:#c0392b}}
.sim-wrap .risk-group.high{{border-color:#e74c3c}}
.sim-wrap .risk-group.limited{{border-color:#f39c12}}
.sim-wrap .risk-group.minimal{{border-color:#27ae60}}
.sim-wrap .risk-group h3{{font-size:0.85rem;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.75rem}}
.sim-wrap .risk-group.prohibited h3{{color:#c0392b}}
.sim-wrap .risk-group.high h3{{color:#e74c3c}}
.sim-wrap .risk-group.limited h3{{color:#f39c12}}
.sim-wrap .risk-group.minimal h3{{color:#27ae60}}
.sim-wrap .risk-group ul{{list-style:none;padding:0}}
.sim-wrap .risk-group li{{font-size:0.85rem;padding:0.3rem 0;color:#374151;border-bottom:1px solid #f3f4f6}}
.sim-wrap .risk-group li:last-child{{border:none}}
.sim-wrap .action-cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem;margin-bottom:2rem}}
.sim-wrap .action-card{{background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:1.25rem}}
.sim-wrap .action-card h3{{font-size:1rem;color:#1B2A4A;margin-bottom:0.5rem}}
.sim-wrap .action-card p{{font-size:0.85rem;color:#6b7280;line-height:1.5}}
.sim-wrap .action-card .deadline{{display:inline-block;background:#fde8e8;color:#c0392b;font-size:0.75rem;font-weight:700;padding:0.15rem 0.5rem;border-radius:4px;margin-top:0.5rem}}
.sim-wrap .action-card .done{{display:inline-block;background:#d4edda;color:#155724;font-size:0.75rem;font-weight:700;padding:0.15rem 0.5rem;border-radius:4px;margin-top:0.5rem}}
</style>
<div class="sim-wrap">
<div class="container">
  <h1>What Does the AI Act Mean for <em>My</em> Business?</h1>
  <p class="subtitle">Pick your industry. Tell us what you use AI for. Get your personalised compliance picture in 60 seconds.</p>

  <div id="industry-section">
    <div class="industry-grid" id="industry-grid"></div>
  </div>

  <div id="activities-section">
    <div class="activities-header">
      <h2 id="activities-title"></h2>
      <p id="activities-subtitle">Tick the activities that apply to your business. These are tied to the regulation, not specific products — so they won't go out of date.</p>
    </div>
    <div class="activity-list" id="activity-list"></div>
    <div class="btn-row">
      <button class="btn-secondary" onclick="backToIndustries()">&larr; Change Industry</button>
      <button class="btn-primary" onclick="showResults()">Show My Compliance Dashboard &rarr;</button>
    </div>
  </div>

  <div id="results-section">
    <div class="results-summary" id="results-summary"></div>
    <div class="risk-breakdown" id="risk-breakdown"></div>
    <h2 style="font-size:1.2rem;color:#1B2A4A;margin-bottom:1rem">What You Need to Do</h2>
    <div class="action-cards" id="action-cards"></div>
    <div class="btn-row" style="margin-top:2rem">
      <button class="btn-secondary" onclick="backToIndustries()">&larr; Try Another Industry</button>
      <a href="" class="btn-primary" id="blog-link">Read the Full Guide &rarr;</a>
      <a href="consultants.html" class="btn-primary" style="background:#C9A84C;color:#1B2A4A">Find a Consultant &rarr;</a>
    </div>
  </div>
</div>

<script>
const DATA = {{
  recruitment: {{
    name: "Recruitment Agency", icon: "\uD83D\uDC54",
    riskLevel: "high", blogSlug: "ai-act-recruitment-agencies.html",
    summary: "Recruitment AI is explicitly HIGH-RISK under Annex III, Category 4. The regulation targets the activity — screening, scoring, ranking candidates — not any specific product.",
    activities: [
      {{name:"We use AI to screen or rank CVs and applications",annex:"Annex III, Category 4(a) — explicitly listed",risk:"high",checked:true}},
      {{name:"We use AI to score or evaluate candidates",annex:"Annex III, Category 4(a) — evaluating candidates",risk:"high",checked:true}},
      {{name:"We use AI video interviewing or assessment",annex:"Annex III, Category 4(a) — AI evaluation of candidates",risk:"high",checked:false}},
      {{name:"We use AI to place targeted job advertisements",annex:"Annex III, Category 4(a) — explicitly named",risk:"high",checked:false}},
      {{name:"We use AI to match candidates to roles",annex:"Annex III, Category 4(a) — selection of candidates",risk:"high",checked:true}},
      {{name:"We use a chatbot for candidate enquiries",annex:"Article 50 — transparency obligation",risk:"limited",checked:false}},
      {{name:"We use AI for interview scheduling",annex:"Administrative task — no evaluation",risk:"minimal",checked:false}},
      {{name:"We use AI that analyses facial expressions or voice tone",annex:"Article 5 — BANNED since February 2025",risk:"prohibited",checked:false}}
    ],
    actions: [
      {{title:"Inform all candidates",text:"Tell candidates AI is used in screening. Explain how it works and what role it plays in decisions.",deadline:"Aug 2026"}},
      {{title:"Human oversight on every shortlist",text:"A qualified recruiter must review every AI-generated score, ranking, and recommendation before it becomes a hiring decision.",deadline:"Aug 2026"}},
      {{title:"AI literacy training",text:"All recruiters using AI tools need documented training on how the tools work, their limitations, and known biases.",deadline:"Already required"}},
      {{title:"Data Protection Impact Assessment",text:"High-risk AI processing personal data requires a DPIA under GDPR Article 35.",deadline:"Aug 2026"}},
      {{title:"Check your software providers",text:"Ask every AI vendor: are they conducting conformity assessments? Will they be ready by August 2026? Get it in writing.",deadline:"Now"}}
    ]
  }},
  schools: {{
    name: "School or University", icon: "\uD83C\uDF93",
    riskLevel: "high", blogSlug: "ai-act-schools-universities.html",
    summary: "Education AI is one of the most detailed HIGH-RISK categories in the entire Act (Annex III, Category 3). Four subcategories cover admissions, grading, adaptive learning, and exam monitoring. Emotion recognition in schools is already BANNED.",
    activities: [
      {{name:"We use AI to grade, mark, or score student work",annex:"Annex III, Category 3(b) — evaluating learning outcomes",risk:"high",checked:true}},
      {{name:"We use AI plagiarism or AI-writing detection",annex:"Annex III, Category 3(d) — detecting prohibited behaviour in assessments",risk:"high",checked:true}},
      {{name:"We use AI proctoring or exam monitoring",annex:"Annex III, Category 3(d) — monitoring behaviour during tests",risk:"high",checked:false}},
      {{name:"We use adaptive learning platforms that personalise student pathways",annex:"Annex III, Category 3(b) — steering the learning process",risk:"high",checked:false}},
      {{name:"We use AI in admissions or student placement decisions",annex:"Annex III, Category 3(a) — determining access to education",risk:"high",checked:false}},
      {{name:"We use AI to predict student performance or dropout risk",annex:"Annex III, Category 3(b)/(c) — influencing educational decisions",risk:"high",checked:false}},
      {{name:"We use a chatbot for student enquiries",annex:"Article 50 — transparency obligation",risk:"limited",checked:false}},
      {{name:"We use AI for timetabling or scheduling",annex:"Administrative task — no evaluation of students",risk:"minimal",checked:true}},
      {{name:"We use AI that monitors student attention or engagement via camera/microphone",annex:"Article 5 — BANNED since February 2025",risk:"prohibited",checked:false}}
    ],
    actions: [
      {{title:"Remove emotion recognition immediately",text:"AI inferring student emotions from biometric data has been PROHIBITED since February 2025. Remove any such systems now.",deadline:"Already banned"}},
      {{title:"Inform students and parents",text:"Tell students (and parents of minors) that AI is used in assessments, plagiarism detection, and admissions.",deadline:"Aug 2026"}},
      {{title:"Human review of all AI flags and grades",text:"Every plagiarism flag, AI-generated grade, and admissions recommendation must be reviewed by a qualified human before becoming final.",deadline:"Aug 2026"}},
      {{title:"AI literacy for all teaching staff",text:"Teachers using AI tools need training on how they work, their false positive rates, and when to override.",deadline:"Already required"}},
      {{title:"DPIAs for tools processing student data",text:"Proctoring tools recording video/audio of students (especially minors) require Data Protection Impact Assessments.",deadline:"Aug 2026"}}
    ]
  }},
  insurance: {{
    name: "Insurance Company", icon: "\uD83D\uDEE1\uFE0F",
    riskLevel: "high", blogSlug: "ai-act-insurance-companies.html",
    summary: "Insurance AI is explicitly HIGH-RISK under Annex III, Category 5 — covering risk assessment, pricing, and access to essential services. Life and health insurance AI is specifically named. Fraud detection gets a narrow exemption.",
    activities: [
      {{name:"We use AI for underwriting or risk assessment",annex:"Annex III, Category 5(c) — risk assessment for insurance",risk:"high",checked:true}},
      {{name:"We use AI to calculate or personalise premiums",annex:"Annex III, Category 5(c) — pricing in life and health insurance",risk:"high",checked:true}},
      {{name:"We use AI to approve or deny claims automatically",annex:"Annex III, Category 5 — access to insurance benefits",risk:"high",checked:false}},
      {{name:"We use AI to assess damage from photos or documents",annex:"Annex III, Category 5 — influences claim settlement",risk:"high",checked:false}},
      {{name:"We use telematics or wearable data for pricing",annex:"Annex III, Category 5(c) — behaviour-based premiums",risk:"high",checked:false}},
      {{name:"We use AI for credit scoring or eligibility checks",annex:"Annex III, Category 5(b) — creditworthiness evaluation",risk:"high",checked:false}},
      {{name:"We use AI for fraud detection only",annex:"Category 5(b) exception — fraud detection is exempt*",risk:"minimal",checked:false}},
      {{name:"We use a chatbot for policyholder enquiries",annex:"Article 50 — transparency obligation",risk:"limited",checked:true}}
    ],
    actions: [
      {{title:"Fundamental Rights Impact Assessment",text:"Before first use of high-risk AI in financial services, you must conduct an FRIA — identifying affected demographic groups and quantifying disparate-impact ratios.",deadline:"Aug 2026"}},
      {{title:"Human oversight on all coverage decisions",text:"Qualified underwriters and claims handlers must review AI recommendations, especially coverage denials.",deadline:"Aug 2026"}},
      {{title:"Decision logs for 6+ months",text:"Maintain AI-generated logs that allow full reconstruction of every underwriting, pricing, and claims decision.",deadline:"Aug 2026"}},
      {{title:"Inform policyholders",text:"Tell individuals that AI is involved in their underwriting, pricing, or claims assessment.",deadline:"Aug 2026"}},
      {{title:"Monitor for bias and discrimination",text:"Continuously track AI outcomes across demographic groups. Document and remediate discriminatory patterns.",deadline:"Aug 2026"}}
    ]
  }},
  gp: {{
    name: "GP Practice", icon: "\uD83E\uDE7A",
    riskLevel: "high", blogSlug: "ai-act-gp-practices.html",
    summary: "Healthcare AI directly affects patient safety. AI triage, diagnostic support, and clinical decision tools are HIGH-RISK and may also require medical device certification under the MDR.",
    activities: [
      {{name:"We use AI triage to assess patient urgency",annex:"Annex III, Category 1 — safety component affecting patient outcomes",risk:"high",checked:false}},
      {{name:"We use AI for diagnostic support or differential diagnosis",annex:"Annex III, Category 1 — clinical decision support",risk:"high",checked:false}},
      {{name:"We use AI to analyse skin lesions, scans, or images",annex:"Annex III, Category 1 + MDR — medical device AI",risk:"high",checked:false}},
      {{name:"We use AI for clinical coding or medical transcription",annex:"Article 50 — transparency if patient-facing",risk:"limited",checked:false}},
      {{name:"We use AI for appointment booking or scheduling",annex:"Administrative task — no clinical impact",risk:"minimal",checked:true}},
      {{name:"We use a patient-facing chatbot or symptom checker",annex:"Annex III if it triages; Article 50 if informational only",risk:"high",checked:false}}
    ],
    actions: [
      {{title:"Verify medical device compliance",text:"AI triage and diagnostic tools may require CE marking under the MDR. Check with your provider.",deadline:"Now"}},
      {{title:"Human oversight on all clinical AI",text:"No AI-generated triage, diagnosis, or recommendation should become a patient decision without clinician review.",deadline:"Aug 2026"}},
      {{title:"Inform patients",text:"Tell patients when AI is used in their triage, diagnosis, or referral process.",deadline:"Aug 2026"}},
      {{title:"AI literacy for clinical staff",text:"GPs and nurses need training on how AI tools work, their accuracy rates, and limitations.",deadline:"Already required"}},
      {{title:"DPIAs for health data AI",text:"AI processing patient health data requires a Data Protection Impact Assessment.",deadline:"Aug 2026"}}
    ]
  }},
  ecommerce: {{
    name: "E-Commerce Shop", icon: "\uD83D\uDED2",
    riskLevel: "minimal", blogSlug: "ai-act-ecommerce-shops.html",
    summary: "Most e-commerce AI is minimal risk. The one exception: BNPL (buy now, pay later) credit scoring is explicitly HIGH-RISK. Product recommendations, fraud detection, and inventory forecasting are all fine.",
    activities: [
      {{name:"We use AI product recommendations or personalisation",annex:"No specific obligation — standard business AI",risk:"minimal",checked:true}},
      {{name:"We use AI for fraud detection on orders",annex:"No specific obligation — protective, not evaluative",risk:"minimal",checked:true}},
      {{name:"We use AI dynamic pricing",annex:"Minimal risk unless targeting vulnerable groups",risk:"minimal",checked:false}},
      {{name:"We use AI for demand forecasting or inventory",annex:"No specific obligation — internal analytics",risk:"minimal",checked:false}},
      {{name:"We use a customer service chatbot",annex:"Article 50 — must disclose AI interaction",risk:"limited",checked:false}},
      {{name:"We use AI-generated product descriptions or images",annex:"Article 50 — disclosure if it could mislead",risk:"limited",checked:false}},
      {{name:"We offer buy now, pay later (BNPL) with AI credit scoring",annex:"Annex III, Category 5(b) — creditworthiness evaluation",risk:"high",checked:false}},
      {{name:"We use AI email personalisation or send-time optimisation",annex:"No specific obligation — standard marketing AI",risk:"minimal",checked:false}}
    ],
    actions: [
      {{title:"Disclose chatbots",text:"If you use any AI chatbot, clearly tell customers they're interacting with AI before or at the start of the conversation.",deadline:"Already required"}},
      {{title:"Check your BNPL provider",text:"If you offer Klarna, Afterpay, or Clearpay, confirm they're preparing for AI Act compliance on their credit scoring.",deadline:"Aug 2026"}},
      {{title:"AI literacy for your team",text:"Staff managing AI tools need basic training on what the tools do and their limitations.",deadline:"Already required"}},
      {{title:"Review dynamic pricing ethics",text:"Dynamic pricing is fine, but pricing that exploits vulnerable groups is PROHIBITED under Article 5.",deadline:"Already banned"}}
    ]
  }},
  restaurants: {{
    name: "Restaurant or Caf\u00e9", icon: "\uD83C\uDF7D\uFE0F",
    riskLevel: "minimal", blogSlug: "ai-act-restaurants-cafes.html",
    summary: "Good news: most restaurant AI is minimal risk. Demand forecasting, menu analytics, and inventory tools have no specific obligations. AI phone answering needs disclosure. Watch out for AI staff scheduling based on individual performance.",
    activities: [
      {{name:"We use AI for sales analytics or menu optimisation",annex:"No specific obligation — internal business AI",risk:"minimal",checked:true}},
      {{name:"We use AI for demand forecasting or labour scheduling",annex:"No specific obligation — operational AI",risk:"minimal",checked:false}},
      {{name:"We use AI phone answering for reservations or orders",annex:"Article 50 — must disclose AI interaction",risk:"limited",checked:false}},
      {{name:"We use AI for guest profiling or personalised marketing",annex:"No specific obligation — standard marketing",risk:"minimal",checked:false}},
      {{name:"We use AI for food waste tracking",annex:"No specific obligation — operational AI",risk:"minimal",checked:false}},
      {{name:"We use AI that evaluates individual staff performance for scheduling",annex:"Annex III, Category 4 — AI affecting work-related decisions",risk:"high",checked:false}}
    ],
    actions: [
      {{title:"Disclose AI phone systems",text:"If AI answers your phone, callers must be told they're speaking with AI.",deadline:"Already required"}},
      {{title:"Check staff scheduling AI",text:"If your scheduling tool ranks or evaluates individual employee performance using AI, it could be high-risk.",deadline:"Aug 2026"}},
      {{title:"Basic AI literacy",text:"Managers using AI tools should understand what the tools do. Light obligation for restaurants.",deadline:"Already required"}}
    ]
  }},
  estate: {{
    name: "Estate Agency", icon: "\uD83C\uDFE0",
    riskLevel: "limited", blogSlug: "ai-act-estate-agents.html",
    summary: "Most estate agency AI is minimal risk, but automated valuations (AVMs) used for mortgage decisions could be HIGH-RISK. AI tenant screening is explicitly HIGH-RISK. Virtual staging and property matching are fine.",
    activities: [
      {{name:"We use AI-powered automated property valuations",annex:"Potentially HIGH-RISK if used for mortgage/lending decisions",risk:"high",checked:false}},
      {{name:"We use AI for tenant screening or referencing",annex:"Annex III, Category 4 — AI affecting access to housing",risk:"high",checked:false}},
      {{name:"We use AI lead scoring or property matching",annex:"No specific obligation — standard business AI",risk:"minimal",checked:true}},
      {{name:"We use AI-generated property descriptions",annex:"No specific obligation — marketing content",risk:"minimal",checked:false}},
      {{name:"We use AI virtual staging or 3D tours",annex:"No specific obligation — visual marketing",risk:"minimal",checked:false}},
      {{name:"We use an AI voice system for enquiries",annex:"Article 50 — must disclose AI interaction",risk:"limited",checked:false}}
    ],
    actions: [
      {{title:"Check valuation AI usage",text:"If automated valuations feed into mortgage or lending decisions, they may be high-risk. Confirm with your AVM provider.",deadline:"Aug 2026"}},
      {{title:"Tenant screening obligations",text:"If you use AI for tenant screening, this is explicitly high-risk. Ensure human review of all AI-generated assessments.",deadline:"Aug 2026"}},
      {{title:"Disclose AI voice systems",text:"If AI answers enquiries, callers must be told they're interacting with AI.",deadline:"Already required"}},
      {{title:"AI literacy for agents",text:"Staff using AI tools need basic understanding of what the tools do and their limitations.",deadline:"Already required"}}
    ]
  }},
  accountants: {{
    name: "Accountancy Practice", icon: "\uD83D\uDCCA",
    riskLevel: "minimal", blogSlug: "ai-act-accountants.html",
    summary: "Accountants have one of the lightest compliance burdens. Auto-categorisation, OCR, and cash flow forecasting are all minimal risk. The exception: AI credit scoring for client lending is high-risk.",
    activities: [
      {{name:"We use AI auto-categorisation for transactions",annex:"No specific obligation — standard bookkeeping AI",risk:"minimal",checked:true}},
      {{name:"We use AI/OCR for invoice and receipt processing",annex:"No specific obligation — document processing",risk:"minimal",checked:true}},
      {{name:"We use AI for cash flow forecasting",annex:"No specific obligation — internal analytics",risk:"minimal",checked:false}},
      {{name:"We use AI for anomaly or fraud detection in audits",annex:"No specific obligation — protective AI",risk:"minimal",checked:false}},
      {{name:"We use a chatbot for client enquiries",annex:"Article 50 — must disclose AI interaction",risk:"limited",checked:false}},
      {{name:"We use AI to assess client creditworthiness for lending",annex:"Annex III, Category 5(b) — credit scoring",risk:"high",checked:false}}
    ],
    actions: [
      {{title:"Disclose chatbots",text:"If you use an AI chatbot for client enquiries, disclose that it's AI.",deadline:"Already required"}},
      {{title:"Check credit scoring usage",text:"If you advise on lending or use AI for creditworthiness, this is high-risk.",deadline:"Aug 2026"}},
      {{title:"Basic AI literacy",text:"Staff using AI tools should understand what they do. Light obligation.",deadline:"Already required"}}
    ]
  }},
  marketing: {{
    name: "Marketing Agency", icon: "\uD83D\uDCE3",
    riskLevel: "limited", blogSlug: "ai-act-marketing-agencies.html",
    summary: "Most marketing AI is limited risk — transparency obligations, not heavy compliance. You must disclose AI-generated content, label deepfakes, and tell people when they're talking to a chatbot. Subliminal manipulation and targeting vulnerable groups is PROHIBITED.",
    activities: [
      {{name:"We use AI to write copy, articles, or social posts",annex:"Article 50 — disclose if informing the public",risk:"limited",checked:true}},
      {{name:"We use AI to generate images for marketing",annex:"Article 50 — disclose AI-generated images in ads",risk:"limited",checked:true}},
      {{name:"We use AI to generate or edit video content",annex:"Article 50 — mandatory deepfake disclosure for ads",risk:"limited",checked:false}},
      {{name:"We deploy chatbots for lead generation or customer service",annex:"Article 50 — must disclose AI interaction",risk:"limited",checked:false}},
      {{name:"We use AI for ad targeting and optimisation",annex:"Minimal risk unless targeting vulnerable groups",risk:"minimal",checked:true}},
      {{name:"We use AI for SEO or content optimisation",annex:"No specific obligation — internal tool",risk:"minimal",checked:false}},
      {{name:"We use AI for email personalisation",annex:"No specific obligation — standard marketing",risk:"minimal",checked:false}},
      {{name:"We use AI techniques that target vulnerable groups or use subliminal manipulation",annex:"Article 5 — BANNED. Fines up to \u20ac35M or 7% turnover",risk:"prohibited",checked:false}}
    ],
    actions: [
      {{title:"Disclose AI-generated content",text:"AI-generated images, videos, and text intended to inform the public must be labelled. Commercial ads do NOT get the artistic exemption.",deadline:"Aug 2026"}},
      {{title:"Label all deepfakes",text:"Synthetic spokesperson videos, manipulated images, and AI audio in advertising must be clearly disclosed.",deadline:"Aug 2026"}},
      {{title:"Disclose chatbots",text:"Any chatbot must tell users they're interacting with AI before the conversation starts.",deadline:"Already required"}},
      {{title:"Review ad targeting practices",text:"Ensure no campaigns target vulnerable populations with manipulative techniques.",deadline:"Already banned"}},
      {{title:"AI literacy for your team",text:"Content creators, designers, and account managers all need training on the tools they use.",deadline:"Already required"}}
    ]
  }},
  hairdressers: {{
    name: "Hair Salon / Beauty", icon: "\uD83D\uDC87",
    riskLevel: "minimal", blogSlug: "ai-act-hairdressers-beauty-salons.html",
    summary: "Hair salons have the lightest compliance burden of any industry we cover. Booking AI is minimal risk. AI phone answering needs to disclose it's AI. That's essentially it.",
    activities: [
      {{name:"We use AI-powered booking or scheduling",annex:"No specific obligation — administrative AI",risk:"minimal",checked:true}},
      {{name:"We use AI for client recommendations or upselling",annex:"No specific obligation — standard business AI",risk:"minimal",checked:false}},
      {{name:"We use AI phone answering (24/7 receptionist)",annex:"Article 50 — must disclose AI interaction",risk:"limited",checked:false}},
      {{name:"We use AI colour matching or styling technology",annex:"No specific obligation — product assistance",risk:"minimal",checked:false}}
    ],
    actions: [
      {{title:"Disclose AI phone answering",text:"If AI answers your phone, callers must be told they're speaking with AI.",deadline:"Already required"}},
      {{title:"Basic AI literacy",text:"You and your staff should have a basic understanding of the AI tools you use.",deadline:"Already required"}}
    ]
  }}
}};

let selectedIndustry = null;

function init() {{
  const grid = document.getElementById('industry-grid');
  const order = ['recruitment','schools','insurance','gp','ecommerce','marketing','estate','restaurants','accountants','hairdressers'];
  order.forEach(key => {{
    const d = DATA[key];
    const tile = document.createElement('div');
    tile.className = 'industry-tile';
    tile.onclick = () => selectIndustry(key);
    const bc = d.riskLevel === 'high' ? 'risk-high' : d.riskLevel === 'limited' ? 'risk-limited' : 'risk-minimal';
    const bt = d.riskLevel === 'high' ? 'HIGH-RISK' : d.riskLevel === 'limited' ? 'LIMITED RISK' : 'MINIMAL RISK';
    tile.innerHTML = '<div class="icon">'+d.icon+'</div><div class="label">'+d.name+'</div><div class="risk-badge '+bc+'">'+bt+'</div>';
    grid.appendChild(tile);
  }});
}}

function selectIndustry(key) {{
  selectedIndustry = key;
  const d = DATA[key];
  document.getElementById('industry-section').style.display = 'none';
  document.getElementById('activities-section').style.display = 'block';
  document.getElementById('results-section').style.display = 'none';
  document.getElementById('activities-title').textContent = "You're a " + d.name;
  const list = document.getElementById('activity-list');
  list.innerHTML = '';
  d.activities.forEach((a, i) => {{
    const card = document.createElement('div');
    card.className = 'activity-card' + (a.checked ? ' checked' : '');
    card.onclick = () => {{ a.checked = !a.checked; card.classList.toggle('checked'); }};
    const rc = a.risk === 'high' ? 'risk-high' : a.risk === 'prohibited' ? 'risk-prohibited' : a.risk === 'limited' ? 'risk-limited' : 'risk-minimal';
    const rl = a.risk === 'high' ? 'HIGH-RISK' : a.risk === 'prohibited' ? 'PROHIBITED' : a.risk === 'limited' ? 'LIMITED' : 'MINIMAL';
    card.innerHTML = '<div class="checkbox"></div><div class="activity-info"><div class="activity-name">'+a.name+'</div><div class="activity-annex">'+a.annex+'</div><div class="activity-risk '+rc+'">'+rl+'</div></div>';
    list.appendChild(card);
  }});
  window.scrollTo({{top:0,behavior:'smooth'}});
}}

function backToIndustries() {{
  document.getElementById('industry-section').style.display = 'block';
  document.getElementById('activities-section').style.display = 'none';
  document.getElementById('results-section').style.display = 'none';
  window.scrollTo({{top:0,behavior:'smooth'}});
}}

function showResults() {{
  const d = DATA[selectedIndustry];
  const checked = d.activities.filter(a => a.checked);
  document.getElementById('activities-section').style.display = 'none';
  document.getElementById('results-section').style.display = 'block';
  window.scrollTo({{top:0,behavior:'smooth'}});

  const prohibited = checked.filter(a => a.risk === 'prohibited');
  const high = checked.filter(a => a.risk === 'high');
  const limited = checked.filter(a => a.risk === 'limited');
  const minimal = checked.filter(a => a.risk === 'minimal');

  let overallRisk = 'minimal'; let overallClass = 'overall-minimal'; let overallLabel = 'MINIMAL RISK';
  if (limited.length > 0) {{ overallRisk = 'limited'; overallClass = 'overall-limited'; overallLabel = 'LIMITED RISK'; }}
  if (high.length > 0) {{ overallRisk = 'high'; overallClass = 'overall-high'; overallLabel = 'HIGH-RISK'; }}
  if (prohibited.length > 0) {{ overallRisk = 'prohibited'; overallClass = 'overall-prohibited'; overallLabel = 'PROHIBITED AI DETECTED'; }}

  let urgency = 'Based on '+checked.length+' activit'+(checked.length!==1?'ies':'y')+' you selected: ';
  if (prohibited.length > 0) urgency += '<strong>'+prohibited.length+' PROHIBITED</strong> practice'+(prohibited.length>1?'s':'')+' that must stop immediately. ';
  if (high.length > 0) urgency += '<strong>'+high.length+' HIGH-RISK</strong> activit'+(high.length>1?'ies':'y')+' requiring full compliance by August 2, 2026. ';
  if (limited.length > 0) urgency += '<strong>'+limited.length+'</strong> with transparency obligations. ';
  if (minimal.length > 0) urgency += '<strong>'+minimal.length+'</strong> with no specific obligations. ';
  if (checked.length === 0) urgency = 'You didn\'t select any activities. Go back and tick the ones that apply to your business.';

  document.getElementById('results-summary').innerHTML = '<h2>Your Compliance Dashboard: <span class="industry-name">'+d.name+'</span></h2><p>'+urgency+'</p><div class="overall-risk '+overallClass+'">Overall: '+overallLabel+'</div>';

  const breakdown = document.getElementById('risk-breakdown');
  breakdown.innerHTML = '';
  [{{label:'Prohibited',key:'prohibited',items:prohibited}},{{label:'High-Risk',key:'high',items:high}},{{label:'Limited Risk',key:'limited',items:limited}},{{label:'Minimal Risk',key:'minimal',items:minimal}}].forEach(g => {{
    if (g.items.length > 0) {{
      const div = document.createElement('div');
      div.className = 'risk-group ' + g.key;
      let h = '<h3>'+g.label+' ('+g.items.length+')</h3><ul>';
      g.items.forEach(a => {{ h += '<li>'+a.name+'</li>'; }});
      div.innerHTML = h + '</ul>';
      breakdown.appendChild(div);
    }}
  }});

  const actions = document.getElementById('action-cards');
  actions.innerHTML = '';
  d.actions.forEach(a => {{
    const card = document.createElement('div');
    card.className = 'action-card';
    const isDone = a.deadline.toLowerCase().includes('already');
    card.innerHTML = '<h3>'+a.title+'</h3><p>'+a.text+'</p><span class="'+(isDone?'done':'deadline')+'">'+a.deadline+'</span>';
    actions.appendChild(card);
  }});

  const link = document.getElementById('blog-link');
  link.href = 'blog/' + d.blogSlug;
  link.textContent = 'Read the Full ' + d.name + ' Guide \u2192';

  if (typeof gtag !== 'undefined') {{
    gtag('event', 'simulator_complete', {{industry: selectedIndustry, activities: checked.length, high_risk: high.length, prohibited: prohibited.length}});
  }}
}}

init();
</script>
</div>
'''
write_page('quiz.html', page('What Does the AI Act Mean for MY Business? — Free Simulator', 'Pick your industry, tick your AI activities, and get a personalised compliance dashboard in 60 seconds. Free, evergreen, tied to the regulation.', simulator_page))

# ── Adventure Page: "Choose Your Compliance Path" ──
adventure_page = '''
<div style="background:#0f1729;margin:-2rem -1.5rem;padding:0">
<style>
.adv-wrap .container{{max-width:720px;margin:0 auto;padding:2rem 1.5rem}}
.adv-wrap h1{{text-align:center;font-size:1.8rem;margin-bottom:0.25rem;color:#fff}}
.adv-wrap .subtitle{{text-align:center;color:#C9A84C;margin-bottom:2rem;font-size:0.95rem}}
.adv-wrap .progress-bar{{background:rgba(255,255,255,0.08);border-radius:99px;height:8px;margin-bottom:0.5rem;overflow:hidden}}
.adv-wrap .progress-fill{{background:linear-gradient(90deg,#C9A84C,#27ae60);height:100%;border-radius:99px;transition:width 0.5s ease}}
.adv-wrap .progress-text{{text-align:right;font-size:0.75rem;color:#6b7280;margin-bottom:1.5rem}}
.adv-wrap .score-bar{{display:flex;justify-content:center;gap:1.5rem;margin-bottom:2rem}}
.adv-wrap .score-item{{text-align:center}}
.adv-wrap .score-item .val{{font-size:1.5rem;font-weight:800}}
.adv-wrap .score-item .lbl{{font-size:0.7rem;text-transform:uppercase;letter-spacing:0.05em;opacity:0.6}}
.adv-wrap .score-good .val{{color:#27ae60}}
.adv-wrap .score-bad .val{{color:#e74c3c}}
.adv-wrap .score-badges .val{{color:#C9A84C}}
.adv-wrap .scenario{{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:2rem;margin-bottom:1.5rem;animation:fadeIn 0.4s ease}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:translateY(0)}}}}
.adv-wrap .scenario-context{{font-size:0.8rem;color:#C9A84C;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.75rem}}
.adv-wrap .scenario h2{{font-size:1.2rem;color:#fff;margin-bottom:1rem;line-height:1.4}}
.adv-wrap .scenario p{{font-size:0.95rem;line-height:1.6;opacity:0.85;margin-bottom:1.25rem}}
.adv-wrap .choices{{display:flex;flex-direction:column;gap:0.6rem}}
.adv-wrap .choice{{background:rgba(255,255,255,0.04);border:2px solid rgba(255,255,255,0.12);border-radius:12px;padding:1rem 1.15rem;cursor:pointer;transition:all 0.2s;display:flex;gap:0.75rem;align-items:flex-start}}
.adv-wrap .choice:hover{{border-color:#C9A84C;background:rgba(201,168,76,0.08)}}
.adv-wrap .choice .letter{{background:rgba(255,255,255,0.08);width:28px;height:28px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.85rem;flex-shrink:0;color:#C9A84C}}
.adv-wrap .choice .text{{font-size:0.92rem;line-height:1.4}}
.adv-wrap .feedback{{border-radius:14px;padding:1.5rem;margin-bottom:1.5rem;animation:fadeIn 0.3s ease}}
.adv-wrap .feedback.correct{{background:rgba(39,174,96,0.12);border:1px solid rgba(39,174,96,0.3)}}
.adv-wrap .feedback.wrong{{background:rgba(231,76,60,0.12);border:1px solid rgba(231,76,60,0.3)}}
.adv-wrap .feedback.partial{{background:rgba(243,156,18,0.12);border:1px solid rgba(243,156,18,0.3)}}
.adv-wrap .feedback h3{{font-size:1rem;margin-bottom:0.5rem}}
.adv-wrap .feedback.correct h3{{color:#27ae60}}
.adv-wrap .feedback.wrong h3{{color:#e74c3c}}
.adv-wrap .feedback.partial h3{{color:#f39c12}}
.adv-wrap .feedback p{{font-size:0.88rem;line-height:1.5;opacity:0.9}}
.adv-wrap .feedback .article-ref{{display:inline-block;background:rgba(255,255,255,0.08);padding:0.15rem 0.5rem;border-radius:4px;font-size:0.75rem;font-weight:600;margin-top:0.5rem}}
.adv-wrap .btn-next{{display:block;width:100%;background:#C9A84C;color:#0f1729;padding:0.75rem;border-radius:10px;font-weight:700;font-size:1rem;border:none;cursor:pointer;font-family:inherit;margin-top:1rem}}
.adv-wrap .btn-next:hover{{background:#e6c45a}}
.adv-wrap .badge-unlock{{display:inline-flex;align-items:center;gap:0.35rem;background:rgba(201,168,76,0.15);border:1px solid rgba(201,168,76,0.3);padding:0.3rem 0.7rem;border-radius:8px;font-size:0.8rem;font-weight:600;color:#C9A84C;margin-top:0.75rem}}
.adv-wrap .final-results{{text-align:center;animation:fadeIn 0.5s ease}}
.adv-wrap .final-grade{{font-size:4rem;font-weight:900;margin:1rem 0 0.5rem}}
.adv-wrap .grade-a{{color:#27ae60}}
.adv-wrap .grade-b{{color:#C9A84C}}
.adv-wrap .grade-c{{color:#f39c12}}
.adv-wrap .grade-d{{color:#e67e22}}
.adv-wrap .grade-f{{color:#e74c3c}}
.adv-wrap .final-title{{font-size:1.3rem;color:#fff;margin-bottom:0.5rem}}
.adv-wrap .final-desc{{font-size:0.95rem;opacity:0.8;max-width:500px;margin:0 auto 2rem;line-height:1.6}}
.adv-wrap .badges-earned{{display:flex;flex-wrap:wrap;gap:0.5rem;justify-content:center;margin-bottom:2rem}}
.adv-wrap .badge-display{{background:rgba(201,168,76,0.1);border:1px solid rgba(201,168,76,0.25);border-radius:10px;padding:0.5rem 0.75rem;font-size:0.8rem;color:#C9A84C}}
.adv-wrap .btn-row{{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap}}
.adv-wrap .btn-primary{{display:inline-block;background:#C9A84C;color:#0f1729;padding:0.65rem 1.5rem;border-radius:10px;font-weight:700;font-size:0.9rem;text-decoration:none;border:none;cursor:pointer;font-family:inherit}}
.adv-wrap .btn-outline{{display:inline-block;background:transparent;color:#fff;border:1px solid rgba(255,255,255,0.2);padding:0.65rem 1.5rem;border-radius:10px;font-weight:600;font-size:0.9rem;text-decoration:none;cursor:pointer;font-family:inherit}}
</style>
<div class="adv-wrap">
<div class="container">
  <h1>AI Act: Choose Your Compliance Path</h1>
  <p class="subtitle">You're the new compliance lead. 10 scenarios. Every choice teaches a real AI Act concept.</p>

  <div class="progress-bar"><div class="progress-fill" id="progress-fill" style="width:0%"></div></div>
  <div class="progress-text" id="progress-text">Scenario 1 of 10</div>

  <div class="score-bar">
    <div class="score-item score-good"><div class="val" id="score-good">0</div><div class="lbl">Correct</div></div>
    <div class="score-item score-bad"><div class="val" id="score-bad">0</div><div class="lbl">Wrong</div></div>
    <div class="score-item score-badges"><div class="val" id="score-badges">0</div><div class="lbl">Badges</div></div>
  </div>

  <div id="game-area"></div>
</div>

<script>
const SCENARIOS = [
  {{
    context: "Week 1 \u2014 Your first day",
    title: "The CEO asks: \u201CDo we even need to worry about the AI Act? We don\u2019t build AI, we just use it.\u201D",
    desc: "Your company uses several AI-powered tools for HR, customer service, and marketing. The CEO thinks the AI Act only applies to companies that develop AI.",
    choices: [
      {{text:"The CEO is right \u2014 the Act only applies to AI developers, not users",correct:false}},
      {{text:"We\u2019re a \u2018deployer\u2019 \u2014 the Act applies to us too, with specific obligations",correct:true}},
      {{text:"We should stop using AI entirely to avoid any risk",correct:false}}
    ],
    feedback: {{
      correct: {{type:"correct",title:"Exactly right.",text:"The AI Act distinguishes between \u2018providers\u2019 (who build AI) and \u2018deployers\u2019 (who use it). Most SMEs are deployers. You have lighter obligations than providers, but you\u2019re definitely covered \u2014 especially if you use high-risk AI.",ref:"Article 3 \u2014 Definitions, Article 26 \u2014 Deployer obligations"}},
      wrong0: {{type:"wrong",title:"Not quite.",text:"The AI Act applies to both providers AND deployers. As a company that uses AI tools, you\u2019re a \u2018deployer\u2019 under Article 3, with obligations under Article 26. Ignoring this could lead to fines.",ref:"Article 3 \u2014 Definitions"}},
      wrong2: {{type:"wrong",title:"Overreaction.",text:"You don\u2019t need to stop using AI. Most business AI is minimal or limited risk with light obligations. The key is understanding which of your tools might be high-risk and what you need to do for those.",ref:"Article 6 \u2014 Classification rules"}}
    }},
    badge: "\uD83C\uDFAF Deployer Detected"
  }},
  {{
    context: "Week 1 \u2014 The AI inventory",
    title: "You start documenting every AI tool in the company. Marketing says their chatbot \u201Cdoesn\u2019t count as AI.\u201D",
    desc: "The marketing team deployed a customer service chatbot last year. They argue it\u2019s \u201Cjust a chatbot, not real AI\u201D and shouldn\u2019t be on your inventory.",
    choices: [
      {{text:"They\u2019re right \u2014 simple chatbots aren\u2019t AI under the Act",correct:false}},
      {{text:"Add it to the inventory \u2014 chatbots have specific transparency obligations",correct:true}},
      {{text:"Remove the chatbot entirely to be safe",correct:false}}
    ],
    feedback: {{
      correct: {{type:"correct",title:"Good call.",text:"Chatbots are explicitly covered. Article 50 requires you to tell users they\u2019re interacting with AI \u2014 before or at the start of the conversation. This is a \u2018limited risk\u2019 transparency obligation and it\u2019s already in force since February 2025.",ref:"Article 50 \u2014 Transparency obligations"}},
      wrong0: {{type:"wrong",title:"Wrong.",text:"Chatbots are covered by the AI Act. Article 50 specifically requires deployers to disclose when someone is interacting with AI. This is already enforceable. Add it to your inventory and check you\u2019re disclosing properly.",ref:"Article 50 \u2014 Transparency obligations"}},
      wrong2: {{type:"partial",title:"Unnecessary.",text:"You don\u2019t need to remove it \u2014 chatbots are limited risk, not banned. Just make sure it clearly tells users they\u2019re talking to AI. A simple disclosure at the start of the conversation is enough.",ref:"Article 50 \u2014 Transparency obligations"}}
    }},
    badge: "\uD83D\uDCCB Inventory Master"
  }},
  {{
    context: "Week 2 \u2014 The HR bombshell",
    title: "HR reveals they\u2019ve been using AI to screen CVs and rank candidates for the past 18 months.",
    desc: "The Head of HR shows you a platform that automatically scores applicants, ranks them by suitability, and generates shortlists. She says it saves 40 hours a week.",
    choices: [
      {{text:"That\u2019s fine \u2014 it\u2019s just helping HR work faster",correct:false}},
      {{text:"This is HIGH-RISK AI \u2014 it needs full compliance under Annex III",correct:true}},
      {{text:"We should switch it off immediately until we\u2019ve assessed it",correct:false}}
    ],
    feedback: {{
      correct: {{type:"correct",title:"Spot on.",text:"AI that screens, scores, or ranks job candidates is explicitly HIGH-RISK under Annex III, Category 4(a). This triggers the full set of deployer obligations: human oversight, transparency to candidates, AI literacy training for HR staff, a DPIA, and provider compliance verification. The deadline is August 2, 2026.",ref:"Annex III, Category 4(a) \u2014 Employment, recruitment"}},
      wrong0: {{type:"wrong",title:"This is a serious gap.",text:"CV screening AI is one of the most explicitly regulated categories in the entire Act. Annex III, Category 4(a) specifically names AI used to \u2018analyse and filter job applications and evaluate candidates.\u2019 This needs immediate attention.",ref:"Annex III, Category 4(a)"}},
      wrong2: {{type:"partial",title:"Close, but not quite.",text:"You don\u2019t necessarily need to switch it off \u2014 but you DO need to act fast. Ensure human oversight of every shortlist, inform candidates AI is used, train HR staff, and conduct a DPIA. The tool can stay if you build compliance around it.",ref:"Article 26 \u2014 Deployer obligations"}}
    }},
    badge: "\u26A0\uFE0F High-Risk Spotter"
  }},
  {{
    context: "Week 3 \u2014 The emotion scanner",
    title: "A vendor pitches software that reads employee facial expressions during meetings to measure \u201Cengagement levels.\u201D",
    desc: "The vendor says Fortune 500 companies use it. The Operations Director is interested. The software analyses webcam footage to detect emotions and flag disengaged employees.",
    choices: [
      {{text:"Interesting \u2014 let\u2019s trial it with proper oversight",correct:false}},
      {{text:"This is PROHIBITED \u2014 reject it immediately",correct:true}},
      {{text:"It\u2019s probably fine if employees consent",correct:false}}
    ],
    feedback: {{
      correct: {{type:"correct",title:"Absolutely right.",text:"Emotion recognition in the workplace is PROHIBITED under Article 5(1)(f). This has been banned since February 2, 2025 \u2014 no trial, no consent workaround, no exceptions except for medical or safety purposes. Using this could trigger fines of up to \u20ac35 million or 7% of global turnover.",ref:"Article 5(1)(f) \u2014 Prohibited AI practices"}},
      wrong0: {{type:"wrong",title:"This would be illegal.",text:"Emotion recognition AI in workplaces is completely banned under Article 5. Not high-risk with compliance obligations \u2014 outright prohibited. No amount of human oversight or good intentions makes this legal. Reject the vendor.",ref:"Article 5(1)(f) \u2014 Prohibited AI practices"}},
      wrong2: {{type:"wrong",title:"Consent doesn\u2019t override the ban.",text:"Article 5 prohibitions are absolute. Employee consent does not create an exemption. Emotion recognition in workplaces is banned regardless of whether employees agree to it. The only exceptions are for medical or safety purposes.",ref:"Article 5(1)(f)"}}
    }},
    badge: "\uD83D\uDEAB Prohibition Enforcer"
  }},
  {{
    context: "Week 4 \u2014 AI literacy deadline",
    title: "You discover that nobody in the company has received AI literacy training. Your CTO says: \u201CThat doesn\u2019t kick in until 2026.\u201D",
    desc: "Article 4 requires AI literacy for all staff involved in operating or affected by AI systems. You need to check when this actually takes effect.",
    choices: [
      {{text:"The CTO is right \u2014 AI literacy is an August 2026 requirement",correct:false}},
      {{text:"AI literacy has been mandatory since February 2, 2025 \u2014 we\u2019re already late",correct:true}},
      {{text:"AI literacy is only recommended, not required",correct:false}}
    ],
    feedback: {{
      correct: {{type:"correct",title:"Correct \u2014 and urgent.",text:"Article 4 (AI literacy) came into force on February 2, 2025 alongside the Article 5 prohibitions. It\u2019s not a future requirement \u2014 it\u2019s already law. You need documented, role-specific training for all staff who use or are affected by AI systems. Not a certification \u2014 but documented training they understand the tools, limitations, and risks.",ref:"Article 4 \u2014 AI literacy"}},
      wrong0: {{type:"wrong",title:"Your CTO is mistaken.",text:"AI literacy (Article 4) came into force on February 2, 2025 \u2014 not August 2026. This is one of the earliest enforcement dates in the entire Act. You\u2019re already behind and need to start training immediately.",ref:"Article 4 \u2014 AI literacy"}},
      wrong2: {{type:"wrong",title:"It\u2019s mandatory, not optional.",text:"Article 4 is a binding obligation, not guidance. Non-compliance can result in enforcement action. Start documented training for all staff who interact with AI systems.",ref:"Article 4 \u2014 AI literacy"}}
    }},
    badge: "\uD83D\uDCDA Literacy Champion"
  }},
  {{
    context: "Week 5 \u2014 The marketing deepfake",
    title: "Your creative team made a promotional video using an AI-generated spokesperson who looks and sounds completely real.",
    desc: "The video is polished and convincing. The team wants to publish it across social media and the company website. Nobody watching would know the person isn\u2019t real.",
    choices: [
      {{text:"Publish it \u2014 it\u2019s creative content, so it qualifies for the artistic exemption",correct:false}},
      {{text:"Publish it with clear disclosure that it\u2019s AI-generated",correct:true}},
      {{text:"Don\u2019t publish it \u2014 deepfakes are banned",correct:false}}
    ],
    feedback: {{
      correct: {{type:"correct",title:"Perfect approach.",text:"Article 50 requires disclosure of AI-generated synthetic content, including deepfakes. The \u2018artistic, creative, or fictional\u2019 exemption does NOT apply to commercial advertising. You can absolutely publish it \u2014 but it must be clearly labelled as AI-generated. A visible disclosure in the video or description is required.",ref:"Article 50 \u2014 Transparency for AI-generated content"}},
      wrong0: {{type:"wrong",title:"The artistic exemption doesn\u2019t cover ads.",text:"Commercial advertising is explicitly excluded from the creative/artistic exemption in Article 50. A synthetic spokesperson in a promotional video must be disclosed as AI-generated.",ref:"Article 50 \u2014 Transparency obligations"}},
      wrong2: {{type:"partial",title:"Deepfakes aren\u2019t banned \u2014 they need disclosure.",text:"AI-generated video isn\u2019t prohibited. It\u2019s \u2018limited risk\u2019 with transparency obligations. You can use synthetic media in marketing as long as you clearly disclose it\u2019s AI-generated. Don\u2019t throw away good content \u2014 just label it.",ref:"Article 50"}}
    }},
    badge: "\uD83C\uDFAC Transparency Pro"
  }},
  {{
    context: "Week 6 \u2014 The insurance crisis",
    title: "Your insurance division uses AI to calculate premiums for health insurance. Compliance asks: \u201CIs this high-risk?\u201D",
    desc: "The AI analyses customer data including age, health history, and lifestyle factors to generate personalised premium quotes for life and health insurance.",
    choices: [
      {{text:"It\u2019s probably minimal risk \u2014 it\u2019s just calculating prices",correct:false}},
      {{text:"This is explicitly HIGH-RISK under Annex III, Category 5(c)",correct:true}},
      {{text:"It depends on whether we built the AI or bought it",correct:false}}
    ],
    feedback: {{
      correct: {{type:"correct",title:"Exactly.",text:"Annex III, Category 5(c) specifically names \u2018AI systems intended for risk assessment and pricing in relation to natural persons in the case of life and health insurance.\u2019 This is one of the most clearly defined high-risk categories. You need a Fundamental Rights Impact Assessment, human oversight, decision logging for 6+ months, and bias monitoring.",ref:"Annex III, Category 5(c) \u2014 Essential services"}},
      wrong0: {{type:"wrong",title:"This is explicitly high-risk.",text:"Insurance pricing AI isn\u2019t \u2018just calculating prices\u2019 \u2014 it determines whether people can afford essential coverage. Annex III, Category 5(c) specifically names this as high-risk. Full deployer obligations apply.",ref:"Annex III, Category 5(c)"}},
      wrong2: {{type:"wrong",title:"The classification doesn\u2019t depend on that.",text:"Whether you\u2019re the provider or deployer changes your obligations, but the risk classification is the same. Insurance pricing AI is high-risk regardless of who built it. As a deployer, you still have substantial obligations under Article 26.",ref:"Article 26 \u2014 Deployer obligations"}}
    }},
    badge: "\uD83D\uDEE1\uFE0F Insurance Inspector"
  }},
  {{
    context: "Week 7 \u2014 The school contract",
    title: "A university client asks your consultancy to review their AI proctoring tool. Students are flagged for \u201Csuspicious eye movement.\u201D",
    desc: "The proctoring software records students during online exams and uses AI to detect suspicious behaviour including eye movement patterns, background noise, and browser activity.",
    choices: [
      {{text:"Proctoring is minimal risk \u2014 it\u2019s just monitoring exams",correct:false}},
      {{text:"This is HIGH-RISK under Annex III, Category 3(d) \u2014 and check it\u2019s not doing emotion recognition",correct:true}},
      {{text:"The university should switch to in-person exams to avoid the Act entirely",correct:false}}
    ],
    feedback: {{
      correct: {{type:"correct",title:"Thorough thinking.",text:"AI proctoring is HIGH-RISK under Annex III, Category 3(d): \u2018AI systems intended to monitor and detect prohibited behaviour during tests.\u2019 And you\u2019re right to check for emotion recognition \u2014 if the tool analyses facial expressions to infer student emotions (stress, attention), that element is PROHIBITED under Article 5. The university needs human review of all flags, transparency to students, and DPIAs given it records minors.",ref:"Annex III, Category 3(d) + Article 5(1)(f)"}},
      wrong0: {{type:"wrong",title:"Proctoring is specifically high-risk.",text:"Annex III, Category 3(d) explicitly covers AI that monitors behaviour during tests. This triggers full deployer obligations including human oversight, student transparency, and DPIAs.",ref:"Annex III, Category 3(d)"}},
      wrong2: {{type:"partial",title:"Impractical and unnecessary.",text:"Online proctoring can continue \u2014 it just needs compliance. Human review of AI flags, transparency to students, and a DPIA are required. Switching to in-person exams might avoid the Act but creates other costs and accessibility issues.",ref:"Annex III, Category 3(d)"}}
    }},
    badge: "\uD83C\uDF93 Education Expert"
  }},
  {{
    context: "Week 8 \u2014 The vendor letter",
    title: "You write to all your AI vendors asking about their AI Act compliance roadmap. Three out of five don\u2019t respond.",
    desc: "Your conformity letters went out two weeks ago. Two providers confirmed they\u2019re working on compliance. Three haven\u2019t replied at all.",
    choices: [
      {{text:"Not our problem \u2014 compliance is their responsibility as providers",correct:false}},
      {{text:"Follow up urgently \u2014 if they can\u2019t demonstrate compliance, we may need alternatives",correct:true}},
      {{text:"Wait for the August 2026 deadline before worrying about vendor readiness",correct:false}}
    ],
    feedback: {{
      correct: {{type:"correct",title:"Smart move.",text:"While the heaviest technical obligations fall on providers, you as the deployer must use AI systems \u2018in accordance with the instructions of use\u2019 (Article 26). If your provider can\u2019t demonstrate compliance, you\u2019re taking a risk. You should: follow up in writing, set a response deadline, evaluate alternatives, and document everything. Compliance takes 8\u201314 months \u2014 providers who haven\u2019t started are a red flag.",ref:"Article 26 \u2014 Deployer obligations"}},
      wrong0: {{type:"wrong",title:"Partially true, but risky.",text:"Provider obligations are heavier, yes. But you have deployer obligations too \u2014 and you can\u2019t properly fulfil them if your provider isn\u2019t compliant. If their system fails a conformity assessment, your use of it becomes non-compliant too.",ref:"Article 26 \u2014 Deployer obligations"}},
      wrong2: {{type:"wrong",title:"Too late by then.",text:"Compliance takes 8\u201314 months. Waiting until August 2026 to worry about vendor readiness means you\u2019ll likely be caught with non-compliant systems. Start the vendor assessment process now.",ref:"Timeline \u2014 Implementation deadlines"}}
    }},
    badge: "\uD83D\uDCE7 Vendor Verifier"
  }},
  {{
    context: "Week 10 \u2014 The board presentation",
    title: "You present your compliance plan to the board. The CFO asks: \u201CWhat happens if we just ignore this?\u201D",
    desc: "The board wants to understand the real consequences of non-compliance. Some members think the Act won\u2019t be enforced against SMEs.",
    choices: [
      {{text:"Fines are capped at \u20ac500K for SMEs, so the risk is manageable",correct:false}},
      {{text:"Fines go up to \u20ac35M or 7% of turnover for prohibited practices, with SME relief using \u2018whichever is lower\u2019",correct:true}},
      {{text:"There are no fines \u2014 the Act is self-regulatory",correct:false}}
    ],
    feedback: {{
      correct: {{type:"correct",title:"Well prepared.",text:"The fine structure has three tiers: up to \u20ac35M/7% for prohibited practices, \u20ac15M/3% for high-risk violations, and \u20ac7.5M/1% for providing incorrect information. For SMEs, the calculation uses \u2018whichever is lower\u2019 instead of \u2018whichever is higher\u2019 \u2014 meaningful relief, but not immunity. Beyond fines: enforcement is complaint-driven through national market surveillance authorities, and reputational damage from non-compliance can outweigh any penalty.",ref:"Article 99 \u2014 Penalties"}},
      wrong0: {{type:"wrong",title:"No such cap exists.",text:"There is no \u20ac500K SME cap. SMEs benefit from \u2018whichever is lower\u2019 rather than \u2018whichever is higher\u2019 for fine calculations, but the potential penalties are still substantial \u2014 up to millions for serious violations.",ref:"Article 99 \u2014 Penalties"}},
      wrong2: {{type:"wrong",title:"The Act has teeth.",text:"The EU AI Act includes enforceable penalties administered by national market surveillance authorities. It is not self-regulatory. Enforcement is complaint-driven \u2014 a disgruntled employee, candidate, or customer can trigger an investigation.",ref:"Article 99 \u2014 Penalties"}}
    }},
    badge: "\uD83C\uDFC6 Compliance Champion"
  }}
];

let currentScenario = 0;
let scoreGood = 0;
let scoreBad = 0;
let badges = [];
let answered = false;

function renderScenario() {{
  const s = SCENARIOS[currentScenario];
  document.getElementById('progress-fill').style.width = ((currentScenario) / SCENARIOS.length * 100) + '%';
  document.getElementById('progress-text').textContent = 'Scenario ' + (currentScenario + 1) + ' of ' + SCENARIOS.length;
  answered = false;

  let html = '<div class="scenario"><div class="scenario-context">' + s.context + '</div>';
  html += '<h2>' + s.title + '</h2><p>' + s.desc + '</p>';
  html += '<div class="choices">';
  s.choices.forEach((c, i) => {{
    html += '<div class="choice" onclick="choose(' + i + ')" id="choice-' + i + '"><div class="letter">' + String.fromCharCode(65 + i) + '</div><div class="text">' + c.text + '</div></div>';
  }});
  html += '</div></div>';
  html += '<div id="feedback-area"></div>';
  document.getElementById('game-area').innerHTML = html;
}}

function choose(index) {{
  if (answered) return;
  answered = true;
  const s = SCENARIOS[currentScenario];
  const choice = s.choices[index];

  // Highlight selection
  document.querySelectorAll('.choice').forEach((c, i) => {{
    if (i === index) c.style.borderColor = choice.correct ? '#27ae60' : '#e74c3c';
    else c.style.opacity = '0.4';
    c.style.cursor = 'default';
  }});

  // Get feedback
  let fb;
  if (choice.correct) {{
    fb = s.feedback.correct;
    scoreGood++;
  }} else {{
    fb = s.feedback['wrong' + index] || s.feedback['wrong0'];
    if (fb.type === 'partial') scoreGood += 0.5;
    else scoreBad++;
  }}

  // Update scores
  document.getElementById('score-good').textContent = Math.floor(scoreGood);
  document.getElementById('score-bad').textContent = scoreBad;

  // Badge
  let badgeHtml = '';
  if (choice.correct && s.badge) {{
    badges.push(s.badge);
    document.getElementById('score-badges').textContent = badges.length;
    badgeHtml = '<div class="badge-unlock">\u2B50 Badge unlocked: ' + s.badge + '</div>';
  }}

  // Show feedback
  const area = document.getElementById('feedback-area');
  area.innerHTML = '<div class="feedback ' + fb.type + '"><h3>' + fb.title + '</h3><p>' + fb.text + '</p><div class="article-ref">' + fb.ref + '</div>' + badgeHtml + '</div>' +
    '<button class="btn-next" onclick="nextScenario()">' + (currentScenario < SCENARIOS.length - 1 ? 'Next Scenario \u2192' : 'See My Results \u2192') + '</button>';
}}

function nextScenario() {{
  currentScenario++;
  if (currentScenario >= SCENARIOS.length) {{
    showFinalResults();
  }} else {{
    renderScenario();
    window.scrollTo({{top:0,behavior:'smooth'}});
  }}
}}

function showFinalResults() {{
  document.getElementById('progress-fill').style.width = '100%';
  document.getElementById('progress-text').textContent = 'Complete!';

  const pct = Math.round((scoreGood / SCENARIOS.length) * 100);
  let grade, gradeClass, title, desc;
  if (pct >= 90) {{ grade = 'A'; gradeClass = 'grade-a'; title = 'Compliance Expert'; desc = 'You navigated the AI Act with near-perfect judgement. You understand the risk classifications, prohibited practices, and deployer obligations. Your company is in safe hands.'; }}
  else if (pct >= 70) {{ grade = 'B'; gradeClass = 'grade-b'; title = 'Strong Foundation'; desc = 'You have a solid understanding of the AI Act. A few areas need sharpening, but you\'re well ahead of most businesses. Review the scenarios you missed and you\'ll be fully prepared.'; }}
  else if (pct >= 50) {{ grade = 'C'; gradeClass = 'grade-c'; title = 'Work to Do'; desc = 'You\'ve got the basics, but some critical concepts caught you out. The good news: you now know exactly where the gaps are. Our industry guides cover each topic in depth.'; }}
  else if (pct >= 30) {{ grade = 'D'; gradeClass = 'grade-d'; title = 'Needs Attention'; desc = 'Several key concepts need attention before August 2026. Consider working with a specialist consultant to build your compliance programme. Our directory can help you find one.'; }}
  else {{ grade = 'F'; gradeClass = 'grade-f'; title = 'Urgent Action Needed'; desc = 'Your company has significant compliance gaps. The AI Act deadline is August 2, 2026 and compliance typically takes 8\u201314 months. Professional guidance is strongly recommended.'; }}

  let html = '<div class="final-results">';
  html += '<div class="final-grade ' + gradeClass + '">' + grade + '</div>';
  html += '<div class="final-title">' + title + '</div>';
  html += '<div class="final-desc">' + desc + '</div>';
  html += '<div style="margin-bottom:1.5rem;font-size:0.9rem;opacity:0.7">You scored <strong>' + Math.floor(scoreGood) + '/' + SCENARIOS.length + '</strong> correct answers</div>';

  if (badges.length > 0) {{
    html += '<div style="margin-bottom:0.5rem;font-size:0.85rem;opacity:0.6">Badges earned:</div><div class="badges-earned">';
    badges.forEach(b => {{ html += '<div class="badge-display">' + b + '</div>'; }});
    html += '</div>';
  }}

  html += '<div class="btn-row">';
  html += '<a href="consultants.html" class="btn-primary">Find a Consultant \u2192</a>';
  html += '<a href="blog.html" class="btn-outline">Read Our Guides \u2192</a>';
  html += '<button class="btn-outline" onclick="resetGame()">Play Again</button>';
  html += '</div></div>';

  document.getElementById('game-area').innerHTML = html;
  window.scrollTo({{top:0,behavior:'smooth'}});

  if (typeof gtag !== 'undefined') {{
    gtag('event', 'adventure_complete', {{score: Math.floor(scoreGood), grade: grade, badges: badges.length}});
  }}
}}

function resetGame() {{
  currentScenario = 0; scoreGood = 0; scoreBad = 0; badges = [];
  document.getElementById('score-good').textContent = '0';
  document.getElementById('score-bad').textContent = '0';
  document.getElementById('score-badges').textContent = '0';
  renderScenario();
  window.scrollTo({{top:0,behavior:'smooth'}});
}}

// Keyboard support
document.addEventListener('keydown', (e) => {{
  if (!answered) {{
    if (e.key === 'a' || e.key === 'A' || e.key === '1') choose(0);
    if (e.key === 'b' || e.key === 'B' || e.key === '2') choose(1);
    if (e.key === 'c' || e.key === 'C' || e.key === '3') choose(2);
  }} else {{
    if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); nextScenario(); }}
  }}
}});

renderScenario();
</script>
</div>
</div>
'''
write_page('adventure.html', page('AI Act: Choose Your Compliance Path — Interactive Game', '10 real-world scenarios testing your AI Act knowledge. Every choice teaches a real concept. Earn badges and get graded A through F.', adventure_page))

# ── Periodic Table of AI Act Terms ──
periodic_page = '''
<div style="background:#0f1729;margin:-2rem -1.5rem;padding:1.5rem;display:flex;flex-direction:column;align-items:center">
<style>
.pt-wrap h1{{font-size:1.6rem;color:#fff;margin-bottom:0.15rem;text-align:center}}
.pt-wrap .subtitle{{color:#C9A84C;font-size:0.85rem;text-align:center;margin-bottom:1.25rem}}
.pt-wrap .legend{{display:flex;gap:0.6rem;flex-wrap:wrap;justify-content:center;margin-bottom:1.25rem}}
.pt-wrap .legend-item{{display:flex;align-items:center;gap:0.3rem;font-size:0.7rem;font-weight:600;opacity:0.8}}
.pt-wrap .legend-dot{{width:12px;height:12px;border-radius:3px}}
.pt-wrap .ptable{{display:grid;grid-template-columns:repeat(8,1fr);gap:4px;max-width:820px;width:100%}}
.pt-wrap .cell{{position:relative;border-radius:6px;padding:6px;cursor:pointer;transition:all 0.15s;aspect-ratio:1;display:flex;flex-direction:column;justify-content:space-between;min-height:0}}
.pt-wrap .cell:hover{{transform:scale(1.08);z-index:10;box-shadow:0 4px 20px rgba(0,0,0,0.4)}}
.pt-wrap .cell .abbr{{font-size:1.1rem;font-weight:800;line-height:1}}
.pt-wrap .cell .name{{font-size:0.5rem;font-weight:600;line-height:1.15;opacity:0.85;overflow:hidden}}
.pt-wrap .cell .num{{font-size:0.5rem;opacity:0.5;text-align:right}}
.pt-wrap .c-prohibited{{background:rgba(196,30,58,0.7);color:#fff}}
.pt-wrap .c-risk{{background:rgba(231,76,60,0.6);color:#fff}}
.pt-wrap .c-core{{background:rgba(27,42,74,0.9);color:#fff;border:1px solid rgba(201,168,76,0.3)}}
.pt-wrap .c-regulation{{background:rgba(99,102,241,0.5);color:#fff}}
.pt-wrap .c-compliance{{background:rgba(14,165,233,0.45);color:#fff}}
.pt-wrap .c-other{{background:rgba(139,92,246,0.45);color:#fff}}
.pt-wrap .c-empty{{background:transparent;pointer-events:none}}
.pt-wrap .c-title{{background:transparent;pointer-events:none;display:flex;align-items:center;justify-content:center}}
.pt-wrap .c-title span{{font-size:0.65rem;color:#C9A84C;font-weight:600;text-align:center;line-height:1.3}}
.pt-wrap .tooltip{{display:none;position:fixed;z-index:100;background:#1a2540;border:1px solid rgba(201,168,76,0.4);border-radius:12px;padding:1.25rem;max-width:340px;width:90vw;box-shadow:0 8px 30px rgba(0,0,0,0.5);pointer-events:none}}
.pt-wrap .tooltip.show{{display:block}}
.pt-wrap .tooltip .tt-cat{{font-size:0.7rem;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.25rem}}
.pt-wrap .tooltip .tt-name{{font-size:1.1rem;font-weight:700;color:#fff;margin-bottom:0.15rem}}
.pt-wrap .tooltip .tt-short{{font-size:0.8rem;color:#C9A84C;margin-bottom:0.5rem}}
.pt-wrap .tooltip .tt-def{{font-size:0.82rem;line-height:1.5;opacity:0.85}}
.pt-wrap .tt-prohibited{{color:#e74c3c}}
.pt-wrap .tt-risk{{color:#e74c3c}}
.pt-wrap .tt-core{{color:#C9A84C}}
.pt-wrap .tt-regulation{{color:#818cf8}}
.pt-wrap .tt-compliance{{color:#38bdf8}}
.pt-wrap .tt-other{{color:#a78bfa}}
.pt-wrap .footer{{margin-top:1.25rem;text-align:center;font-size:0.7rem;opacity:0.4}}
.pt-wrap .footer a{{color:#C9A84C;text-decoration:none}}
@media(max-width:700px){{  .pt-wrap .ptable{{grid-template-columns:repeat(6,1fr);max-width:400px}}
  .pt-wrap .cell .abbr{{font-size:0.85rem}}
  .pt-wrap .cell .name{{font-size:0.42rem}}}}
@media(max-width:420px){{  .pt-wrap .ptable{{grid-template-columns:repeat(5,1fr);max-width:330px}}}}
</style>
<div class="pt-wrap">
<h1>The Periodic Table of AI Act Terms</h1>
<p class="subtitle">Hover over any element to see the definition. 43 terms every business needs to know.</p>

<div class="legend">
  <div class="legend-item"><div class="legend-dot" style="background:rgba(196,30,58,0.8)"></div>Prohibited</div>
  <div class="legend-item"><div class="legend-dot" style="background:rgba(231,76,60,0.7)"></div>Risk Levels</div>
  <div class="legend-item"><div class="legend-dot" style="background:rgba(27,42,74,0.9);border:1px solid rgba(201,168,76,0.3)"></div>Core Concepts</div>
  <div class="legend-item"><div class="legend-dot" style="background:rgba(99,102,241,0.6)"></div>Key Articles</div>
  <div class="legend-item"><div class="legend-dot" style="background:rgba(14,165,233,0.5)"></div>Compliance</div>
  <div class="legend-item"><div class="legend-dot" style="background:rgba(139,92,246,0.5)"></div>Other</div>
</div>

<div class="ptable" id="ptable"></div>

<div class="tooltip" id="tooltip">
  <div class="tt-cat" id="tt-cat"></div>
  <div class="tt-name" id="tt-name"></div>
  <div class="tt-short" id="tt-short"></div>
  <div class="tt-def" id="tt-def"></div>
</div>

<div class="footer">Free to share with attribution &middot; <a href="https://aiactadvisors.com">aiactadvisors.com</a> &middot; February 2026</div>

<script>
const ELEMENTS = [
  // Row 1: Risk levels + header
  {{abbr:"Pr",name:"Prohibited AI",cat:"prohibited",short:"The banned uses (Article 5)",def:"AI uses too dangerous for any compliance pathway. Includes real-time facial recognition, emotion recognition at work/school, subliminal manipulation, and social scoring. Completely banned."}},
  {{abbr:"Un",name:"Unacceptable Risk",cat:"prohibited",short:"Synonym for prohibited",def:"The highest risk tier. These AI uses are completely banned in the EU with no compliance pathway. Fines up to \u20ac35M or 7% of turnover."}},
  {{abbr:"Hi",name:"High-Risk AI",cat:"risk",short:"Annex III listed systems",def:"AI that significantly impacts fundamental rights \u2014 hiring tools, credit scoring, medical AI, education AI. Triggers the heaviest compliance: conformity assessment, CE marking, human oversight."}},
  {{abbr:"Li",name:"Limited Risk",cat:"risk",short:"Transparency (Article 50)",def:"AI with some risk but not high-risk. Must disclose AI is being used. Covers chatbots, AI-generated content, deepfakes."}},
  {{abbr:"Mi",name:"Minimal Risk",cat:"risk",short:"Most business AI",def:"AI that doesn\u2019t significantly impact rights \u2014 recommendations, scheduling, analytics. Minimal requirements, but banned practices still apply."}},
  {{type:"title",text:"RISK\nLEVELS"}},
  {{type:"empty"}},{{type:"empty"}},

  // Row 2: Core concepts
  {{abbr:"AS",name:"AI System",cat:"core",short:"What the Act considers \u201CAI\u201D",def:"Software using machine learning or logic-based approaches to generate predictions or decisions. Tools that learn from data or follow rules to make decisions."}},
  {{abbr:"Pv",name:"Provider",cat:"core",short:"Company that builds AI",def:"The organisation that creates or develops an AI system. If you\u2019re building your own AI, you have provider obligations \u2014 the heaviest in the Act."}},
  {{abbr:"Dp",name:"Deployer",cat:"core",short:"Business that uses AI",def:"The organisation that uses an AI system in operations. Using ChatGPT, analytics, or hiring tools? You\u2019re a deployer. Lighter obligations than providers."}},
  {{abbr:"Op",name:"Operator",cat:"core",short:"Providers + deployers",def:"Umbrella term for any organisation in the AI value chain \u2014 either building it or using it. The Act imposes different obligations on each."}},
  {{abbr:"GP",name:"General-Purpose AI",cat:"core",short:"ChatGPT, Claude, etc.",def:"Large language models trained on broad data for many uses. The Act has specific rules for GPAI providers about transparency and safety testing."}},
  {{abbr:"AL",name:"AI Literacy",cat:"core",short:"Article 4: train your staff",def:"Obligation to ensure staff understand AI systems they use. Mandatory since February 2025. Documented, role-specific training required."}},
  {{abbr:"PM",name:"Placing on Market",cat:"core",short:"Making AI available in EU",def:"When a provider first makes an AI system available for distribution or use. Triggers compliance obligations."}},
  {{abbr:"PS",name:"Putting into Service",cat:"other",short:"First use for its purpose",def:"When an AI system is first actually used in the real world. The deployer puts it into service."}},

  // Row 3: Key articles (regulation)
  {{abbr:"A3",name:"Annex III",cat:"regulation",short:"The high-risk AI list",def:"Lists specific uses classified as high-risk: hiring (Cat 4), credit scoring (Cat 5), education (Cat 3), healthcare (Cat 1). Determines which systems need the most work."}},
  {{abbr:"A4",name:"Article 4",cat:"regulation",short:"AI literacy obligation",def:"Staff using high-risk AI must be trained on how the system works. Document training and keep records. In force since February 2025."}},
  {{abbr:"A5",name:"Article 5",cat:"regulation",short:"Prohibited practices",def:"Complete ban on certain AI uses \u2014 emotion recognition at work/school, subliminal manipulation, social scoring. No exceptions. In force since February 2025."}},
  {{abbr:"A6",name:"Article 6",cat:"regulation",short:"Classification rules",def:"Defines which systems are high-risk based on intended use and impact on people\u2019s rights. Critical for understanding your category."}},
  {{abbr:"A14",name:"Article 14",cat:"regulation",short:"Human oversight",def:"Humans must stay meaningfully involved in high-risk AI decisions. Not a token button-press \u2014 real ability to understand and override the system."}},
  {{abbr:"A26",name:"Article 26",cat:"regulation",short:"Deployer obligations",def:"The main compliance checklist for SMEs using high-risk AI: monitor performance, keep records, report incidents, ensure human oversight."}},
  {{abbr:"A27",name:"Article 27",cat:"regulation",short:"Rights impact assessment",def:"Deployers of high-risk AI must assess how it might affect people\u2019s rights. Document potential harms and mitigation measures before deployment."}},
  {{abbr:"A50",name:"Article 50",cat:"regulation",short:"Transparency (limited)",def:"Tell people when they\u2019re interacting with AI and disclose how it works. Applies to chatbots, AI-generated content, deepfakes."}},

  // Row 4: More regulation + compliance
  {{abbr:"A99",name:"Article 99",cat:"regulation",short:"Penalties",def:"Maximum fines: \u20ac35M/7% for prohibited practices, \u20ac15M/3% for high-risk violations. SMEs get \u2018whichever is lower\u2019 relief."}},
  {{abbr:"MDR",name:"Medical Device Reg",cat:"regulation",short:"Healthcare AI overlap",def:"EU rules for medical devices. Overlaps with AI Act for healthcare AI \u2014 you may need to comply with both."}},
  {{abbr:"GDR",name:"GDPR",cat:"other",short:"Data protection overlap",def:"The EU\u2019s general data protection regulation. Overlaps significantly with the AI Act since AI systems often process personal data."}},
  {{abbr:"CE",name:"CE Marking",cat:"compliance",short:"The compliance label",def:"A mark placed on high-risk AI systems to show they meet AI Act requirements. Similar to CE marks on other EU products."}},
  {{abbr:"CA",name:"Conformity Assessment",cat:"compliance",short:"Formal compliance check",def:"Independent review verifying your high-risk system meets all legal requirements. Mandatory before placing on market."}},
  {{abbr:"NB",name:"Notified Body",cat:"compliance",short:"Independent assessor",def:"A government-accredited third party that conducts conformity assessments. You hire them to verify compliance."}},
  {{abbr:"HO",name:"Human Oversight",cat:"compliance",short:"Humans in the loop",def:"Humans must remain meaningfully involved in high-risk AI decisions \u2014 understand the system, monitor it, can override or stop it."}},
  {{abbr:"FR",name:"Rights Impact Assess.",cat:"compliance",short:"Article 27 FRIA",def:"Documented review of how high-risk AI might violate people\u2019s rights. Identify and mitigate harms before deployment."}},

  // Row 5: More compliance
  {{abbr:"RM",name:"Risk Management",cat:"compliance",short:"Systematic risk ID",def:"Your documented process for identifying, assessing, and reducing AI-related risks. Required for high-risk systems."}},
  {{abbr:"TD",name:"Technical Docs",cat:"compliance",short:"Provider must maintain",def:"Detailed records of how AI was built, trained, and tested. Includes data, algorithms, testing results, performance metrics."}},
  {{abbr:"TO",name:"Transparency Oblig.",cat:"compliance",short:"Article 50 disclosure",def:"For limited-risk AI: disclose that AI is involved and explain how it works. Builds trust and meets legal requirements."}},
  {{abbr:"PO",name:"Post-Market Monitor",cat:"compliance",short:"Ongoing compliance",def:"After deploying high-risk AI, continuously monitor performance, gather feedback, check for problems."}},
  {{abbr:"DB",name:"EU Database",cat:"compliance",short:"Public register",def:"Transparency tool where providers register high-risk AI systems. Lets customers verify what they\u2019re using."}},
  {{abbr:"MS",name:"Market Surveillance",cat:"compliance",short:"National enforcer",def:"Your national regulator for AI Act compliance. Each EU member state has one. Contact them for guidance."}},
  {{abbr:"SM",name:"Significant Modif.",cat:"compliance",short:"Deployer \u2192 provider",def:"Substantial changes to how you use or modify AI may shift you from deployer to provider \u2014 triggering new obligations."}},
  {{abbr:"CP",name:"Codes of Practice",cat:"other",short:"Voluntary frameworks",def:"Optional industry standards demonstrating good compliance. Useful for showing extra diligence beyond minimums."}},

  // Row 6: Other terms
  {{abbr:"DF",name:"Deep Fake",cat:"other",short:"AI synthetic media",def:"Video, audio, or images created or altered by AI to look real. The Act requires labelling of all synthetic media in commercial contexts."}},
  {{abbr:"ER",name:"Emotion Recognition",cat:"other",short:"Detecting feelings via AI",def:"AI that claims to identify emotions from facial expressions or voice. Banned in workplaces and schools since February 2025."}},
  {{abbr:"BC",name:"Biometric Categ.",cat:"other",short:"Classifying by traits",def:"AI assigning people to categories (age, gender, ethnicity) from biometric data. Often banned or heavily restricted."}},
  {{abbr:"RB",name:"Remote Biometric ID",cat:"prohibited",short:"Banned facial recognition",def:"Real-time facial recognition in public spaces. Banned in most EU contexts. Very narrow exceptions for law enforcement only."}},
  {{abbr:"RS",name:"Regulatory Sandbox",cat:"other",short:"Safe testing for SMEs",def:"Government-provided space where SMEs can test innovative AI with lighter requirements. Ask your national authority."}},
  {{type:"title",text:"OTHER\nTERMS"}},
  {{type:"empty"}},{{type:"empty"}}
];

function buildTable() {{
  const table = document.getElementById('ptable');
  ELEMENTS.forEach((el, i) => {{
    const div = document.createElement('div');
    if (el.type === 'empty') {{
      div.className = 'cell c-empty';
    }} else if (el.type === 'title') {{
      div.className = 'cell c-title';
      div.innerHTML = '<span>' + el.text.replace('\n','<br>') + '</span>';
    }} else {{
      div.className = 'cell c-' + el.cat;
      div.innerHTML = '<div class="num">' + (i + 1) + '</div><div class="abbr">' + el.abbr + '</div><div class="name">' + el.name + '</div>';
      div.addEventListener('mouseenter', (e) => showTooltip(e, el));
      div.addEventListener('mousemove', (e) => moveTooltip(e));
      div.addEventListener('mouseleave', hideTooltip);
      // Touch support
      div.addEventListener('touchstart', (e) => {{
        e.preventDefault();
        const touch = e.touches[0];
        showTooltipAt(touch.clientX, touch.clientY, el);
      }});
    }}
    table.appendChild(div);
  }});

  // Close tooltip on touch outside
  document.addEventListener('touchstart', (e) => {{
    if (!e.target.closest('.cell')) hideTooltip();
  }});
}}

function showTooltip(e, el) {{
  const tt = document.getElementById('tooltip');
  const catLabels = {{prohibited:'PROHIBITED',risk:'RISK LEVEL',core:'CORE CONCEPT',regulation:'KEY ARTICLE',compliance:'COMPLIANCE',other:'OTHER'}};
  document.getElementById('tt-cat').textContent = catLabels[el.cat] || el.cat;
  document.getElementById('tt-cat').className = 'tt-cat tt-' + el.cat;
  document.getElementById('tt-name').textContent = el.name;
  document.getElementById('tt-short').textContent = el.short;
  document.getElementById('tt-def').textContent = el.def;
  tt.classList.add('show');
  moveTooltip(e);
}}

function showTooltipAt(x, y, el) {{
  const tt = document.getElementById('tooltip');
  const catLabels = {{prohibited:'PROHIBITED',risk:'RISK LEVEL',core:'CORE CONCEPT',regulation:'KEY ARTICLE',compliance:'COMPLIANCE',other:'OTHER'}};
  document.getElementById('tt-cat').textContent = catLabels[el.cat] || el.cat;
  document.getElementById('tt-cat').className = 'tt-cat tt-' + el.cat;
  document.getElementById('tt-name').textContent = el.name;
  document.getElementById('tt-short').textContent = el.short;
  document.getElementById('tt-def').textContent = el.def;
  tt.classList.add('show');
  positionTooltip(x, y);
}}

function moveTooltip(e) {{
  positionTooltip(e.clientX, e.clientY);
}}

function positionTooltip(x, y) {{
  const tt = document.getElementById('tooltip');
  const rect = tt.getBoundingClientRect();
  let left = x + 15;
  let top = y - 10;
  if (left + rect.width > window.innerWidth - 10) left = x - rect.width - 15;
  if (top + rect.height > window.innerHeight - 10) top = y - rect.height - 10;
  if (top < 10) top = 10;
  if (left < 10) left = 10;
  tt.style.left = left + 'px';
  tt.style.top = top + 'px';
}}

function hideTooltip() {{
  document.getElementById('tooltip').classList.remove('show');
}}

buildTable();
</script>
</div>
</div>
'''
write_page('jargon-buster.html', page('The Periodic Table of AI Act Terms — 43 Key Definitions', '43 essential EU AI Act terms in an interactive periodic table. Hover to see plain-English definitions. Colour-coded by category.', periodic_page))


# ── Products Page ──
products_page = f'''
<div class="container" style="max-width:960px;margin:0 auto;padding:3rem 1.5rem">
  <h1 style="text-align:center;font-size:2.2rem;margin-bottom:0.5rem">AI Act Compliance Tools</h1>
  <p style="text-align:center;color:#6b7280;margin-bottom:2.5rem;font-size:1.05rem;max-width:600px;margin-left:auto;margin-right:auto">Everything you need to start your EU AI Act compliance journey. From free resources to comprehensive starter kits.</p>

  <!-- Free Tools -->
  <h2 style="font-size:1.1rem;color:#C9A84C;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:1.25rem;border-bottom:2px solid #C9A84C;padding-bottom:0.5rem">Free Tools</h2>

  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.25rem;margin-bottom:3rem">
    <!-- Simulator -->
    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:1.5rem;transition:box-shadow 0.2s">
      <div style="background:#FFFDF5;border-radius:10px;padding:0.75rem;text-align:center;margin-bottom:1rem">
        <span style="font-size:2rem">&#x1F3AF;</span>
      </div>
      <h3 style="font-size:1.1rem;margin-bottom:0.5rem">What Does the AI Act Mean for My Business?</h3>
      <p style="font-size:0.9rem;color:#6b7280;margin-bottom:1rem">Pick your industry, tick your AI activities, get a personalised compliance dashboard. 10 industries, 60 seconds, tied to the regulation.</p>
      <a href="quiz.html" style="display:inline-block;background:#1B2A4A;color:#fff;padding:0.5rem 1.25rem;border-radius:10px;font-weight:600;font-size:0.9rem;text-decoration:none">Try the Simulator</a>
    </div>

    <!-- Compliance Game -->
    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:1.5rem;transition:box-shadow 0.2s">
      <div style="background:#FFFDF5;border-radius:10px;padding:0.75rem;text-align:center;margin-bottom:1rem">
        <span style="font-size:2rem">&#x1F3AE;</span>
      </div>
      <h3 style="font-size:1.1rem;margin-bottom:0.5rem">Choose Your Compliance Path</h3>
      <p style="font-size:0.9rem;color:#6b7280;margin-bottom:1rem">10 real-world scenarios. Every choice teaches a real AI Act concept. Earn badges, get graded A through F. Can you become a Compliance Expert?</p>
      <a href="adventure.html" style="display:inline-block;background:#1B2A4A;color:#fff;padding:0.5rem 1.25rem;border-radius:10px;font-weight:600;font-size:0.9rem;text-decoration:none">Play the Game</a>
    </div>

    <!-- Periodic Table -->
    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:1.5rem;transition:box-shadow 0.2s">
      <div style="background:#FFFDF5;border-radius:10px;padding:0.75rem;text-align:center;margin-bottom:1rem">
        <span style="font-size:2rem">&#x1F9EA;</span>
      </div>
      <h3 style="font-size:1.1rem;margin-bottom:0.5rem">Periodic Table of AI Act Terms</h3>
      <p style="font-size:0.9rem;color:#6b7280;margin-bottom:1rem">43 key terms in an interactive periodic table. Hover to see plain-English definitions. Colour-coded by category. One page, zero jargon.</p>
      <a href="jargon-buster.html" style="display:inline-block;background:#1B2A4A;color:#fff;padding:0.5rem 1.25rem;border-radius:10px;font-weight:600;font-size:0.9rem;text-decoration:none">Explore the Table</a>
    </div>
  </div>

  <!-- Paid Products -->
  <h2 style="font-size:1.1rem;color:#C9A84C;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:1.25rem;border-bottom:2px solid #C9A84C;padding-bottom:0.5rem">Compliance Kits</h2>

  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.25rem;margin-bottom:3rem">
    <!-- Starter Kit -->
    <div style="background:#fff;border:2px solid #C9A84C;border-radius:14px;padding:1.5rem;position:relative">
      <div style="position:absolute;top:-12px;right:16px;background:#C9A84C;color:#fff;padding:0.2rem 0.75rem;border-radius:99px;font-size:0.75rem;font-weight:700">MOST POPULAR</div>
      <div style="background:#FFFDF5;border-radius:10px;padding:0.75rem;text-align:center;margin-bottom:1rem">
        <span style="font-size:2rem">&#x1F4E6;</span>
      </div>
      <h3 style="font-size:1.1rem;margin-bottom:0.25rem">AI Act Compliance Starter Kit</h3>
      <p style="font-size:1.5rem;font-weight:800;color:#1B2A4A;margin-bottom:0.5rem">&euro;49 <span style="font-size:0.85rem;font-weight:400;color:#6b7280">one-off payment</span></p>
      <p style="font-size:0.9rem;color:#6b7280;margin-bottom:1rem">7 ready-to-use templates and tools. Everything an SME needs to start AI Act compliance today.</p>
      <ul style="list-style:none;padding:0;margin:0 0 1.25rem 0;font-size:0.85rem">
        <li style="padding:0.3rem 0;border-bottom:1px solid #f3f4f6">{svg_check()} AI Inventory Template (pre-filled)</li>
        <li style="padding:0.3rem 0;border-bottom:1px solid #f3f4f6">{svg_check()} Risk Classification Flowchart</li>
        <li style="padding:0.3rem 0;border-bottom:1px solid #f3f4f6">{svg_check()} AI Literacy Briefing Template</li>
        <li style="padding:0.3rem 0;border-bottom:1px solid #f3f4f6">{svg_check()} Transparency Disclosure Templates</li>
        <li style="padding:0.3rem 0;border-bottom:1px solid #f3f4f6">{svg_check()} Provider Compliance Letter</li>
        <li style="padding:0.3rem 0;border-bottom:1px solid #f3f4f6">{svg_check()} Compliance Checklist</li>
        <li style="padding:0.3rem 0">{svg_check()} Quick Reference Card</li>
      </ul>
      <a href="#" style="display:block;text-align:center;background:#C9A84C;color:#fff;padding:0.65rem 1.25rem;border-radius:10px;font-weight:700;font-size:0.95rem;text-decoration:none">Coming Soon</a>
      <p style="text-align:center;font-size:0.75rem;color:#9ca3af;margin-top:0.5rem">Instant download &bull; 30-day money-back guarantee</p>
    </div>

    <!-- Industry Guides (coming soon) -->
    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:1.5rem;opacity:0.85">
      <div style="background:#f3f4f6;border-radius:10px;padding:0.75rem;text-align:center;margin-bottom:1rem">
        <span style="font-size:2rem">&#x1F3ED;</span>
      </div>
      <h3 style="font-size:1.1rem;margin-bottom:0.25rem">Industry-Specific Guides</h3>
      <p style="font-size:1.5rem;font-weight:800;color:#1B2A4A;margin-bottom:0.5rem">&euro;29 <span style="font-size:0.85rem;font-weight:400;color:#6b7280">per industry</span></p>
      <p style="font-size:0.9rem;color:#6b7280;margin-bottom:1rem">Pre-filled templates customised for your exact sector. Available for 7 industries including recruitment, healthcare, e-commerce, and more.</p>
      <div style="background:#f9fafb;border-radius:8px;padding:0.75rem;text-align:center;color:#6b7280;font-size:0.9rem;font-weight:600">Coming Soon</div>
    </div>
  </div>

  <!-- CTA -->
  <div style="background:#1B2A4A;border-radius:16px;padding:2rem;text-align:center;color:#fff">
    <h3 style="font-size:1.3rem;margin-bottom:0.5rem;color:#fff">Not sure where to start?</h3>
    <p style="color:#d1d5db;margin-bottom:1rem;font-size:0.95rem">Try our free simulator to find your risk level, then pick the right tools for your business.</p>
    <a href="quiz.html" style="display:inline-block;background:#C9A84C;color:#fff;padding:0.65rem 2rem;border-radius:10px;font-weight:700;text-decoration:none;font-size:0.95rem">Try the Free Simulator</a>
    <span style="color:#6b7280;margin:0 0.75rem">or</span>
    <a href="consultants.html" style="display:inline-block;background:transparent;color:#C9A84C;border:2px solid #C9A84C;padding:0.55rem 1.5rem;border-radius:10px;font-weight:600;text-decoration:none;font-size:0.95rem">Find a Consultant</a>
  </div>
</div>
'''
write_page('products.html', page('AI Act Compliance Tools & Templates', 'EU AI Act compliance tools, templates, and guides for SMEs. Free quiz, risk classification flowchart, and comprehensive starter kit.', products_page))

# ── Sitemap ──
urls = ['index.html', 'consultants.html', 'countries.html', 'sectors.html', 'blog.html', 'about.html', 'list-your-practice.html', 'privacy.html', 'terms.html', 'disclaimer.html', 'quiz.html', 'adventure.html', 'jargon-buster.html', 'products.html', 'blog/eu-ai-act-compliance-guide-smes.html', 'blog/eu-ai-act-penalties-2026.html', 'blog/ai-act-hairdressers-beauty-salons.html', 'blog/ai-act-recruitment-agencies.html', 'blog/ai-act-restaurants-cafes.html', 'blog/ai-act-estate-agents.html', 'blog/ai-act-ecommerce-shops.html', 'blog/ai-act-accountants.html', 'blog/ai-act-gp-practices.html', 'blog/ai-act-schools-universities.html', 'blog/ai-act-marketing-agencies.html', 'blog/ai-act-insurance-companies.html']
for c in consultants:
    urls.append(f'consultant/{c["id"]}.html')
for country in cc:
    urls.append(f'country/{slug(country)}.html')
for sector in sc:
    urls.append(f'sector/{slug(sector)}.html')
for (city, country) in city_counts():
    urls.append(f'city/{slug(city)}.html')

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in urls:
    sitemap += f'  <url><loc>https://aiactadvisors.com/{url}</loc><changefreq>weekly</changefreq></url>\n'
sitemap += '</urlset>'
write_page('sitemap.xml', sitemap)

# robots.txt
write_page('robots.txt', 'User-agent: *\nAllow: /\nSitemap: https://aiactadvisors.com/sitemap.xml\n')

# ── Summary ──
page_count = len(urls) + 2  # sitemap + robots
print(f"Build complete!")
print(f"Pages generated: {page_count}")
print(f"  - Consultant profiles: {len(consultants)}")
print(f"  - Country pages: {len(cc)}")
print(f"  - Sector pages: {len(sc)}")
print(f"  - City pages: {len(city_counts())}")
print(f"  - Static pages: 17")
print(f"  - Blog posts: 12")
print(f"Sitemap URLs: {len(urls)}")
