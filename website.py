import os
import re
import pandas as pd

# =====================================================================
# CONFIGURATION
# =====================================================================
INPUT_CSV = "filtered_uae_cafes_no_website.csv"
OUTPUT_CSV = "final_cafe_leads_with_websites.csv"
OUTPUT_DIR = "dist"
GITHUB_USERNAME = "AbdulBaasithere"  # Change to your GitHub Username
REPO_NAME = "cafe-leads-demo"        # The target GitHub repository name

# =====================================================================
# DATA ENGINE CLEANING UTILITIES
# =====================================================================
def slugify(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    return re.sub(r'[\s-]+', '-', text).strip('-')

def clean_phone(phone):
    if pd.isna(phone) or not phone:
        return ""
    cleaned = re.sub(r'\D', '', str(phone))
    if len(cleaned) == 9 and cleaned.startswith('5'):
        cleaned = '971' + cleaned
    elif not cleaned.startswith('971') and len(cleaned) == 9:
        cleaned = '971' + cleaned
    return cleaned

def generate_massive_glass_template(name, score, category, categories_all, address, phone, maps_url):
    phone_clean = clean_phone(phone)
    display_phone = phone if pd.notna(phone) and phone else "Reservations Only"
    display_address = address if pd.notna(address) and address else "Premium District, Abu Dhabi, UAE"
    display_category = category if pd.notna(category) else "Premium Venue"
    
    # Intelligently determine niche classification 
    is_coffee = any(x in str(categories_all).lower() or x in str(name).lower() for x in ['cafe', 'coffee', 'roastery', 'cafeteria', 'brew'])
    
    # Premium Curated High-Definition Context Wallpapers
    if is_coffee:
        bg_hero = "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?q=80&w=1600&auto=format&fit=crop"
        bg_story = "https://images.unsplash.com/photo-1447933601403-0c6688de566e?q=80&w=800&auto=format&fit=crop"
    else:
        bg_hero = "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=1600&auto=format&fit=crop"
        bg_story = "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?q=80&w=800&auto=format&fit=crop"

    stars_count = int(round(float(score))) if pd.notna(score) else 5
    stars_html = "".join(['<i class="fa-solid fa-star"></i>' for _ in range(stars_count)])
    rating_val = score if pd.notna(score) else "4.8"

    # Deep Dynamic Menu Generation Based on Category Profile
    if is_coffee:
        menu_items = [
            {"title": "Cold Drip Kyoto Style", "desc": "24-hour slow extraction tracking bright, crisp floral notes.", "price": "32 AED", "tag": "Signature"},
            {"title": "Spanish Saffron Latte", "desc": "Double shot artisan espresso infused with pure local organic saffron.", "price": "28 AED", "tag": "Best Seller"},
            {"title": "Pistachio Croissant Cube", "desc": "Flaky 72-layer laminated pastry packed with roasted Sicilian pistachio cream.", "price": "26 AED", "tag": "Freshly Baked"},
            {"title": "V60 Ethiopian Yirgacheffe", "desc": "Single-origin pourover featuring prominent bergamot and black tea clarity.", "price": "30 AED", "tag": "Micro-Lot"}
        ]
    else:
        menu_items = [
            {"title": "Wagyu Ribeye Steak", "desc": "Grade A5 marble score charcoal-seared, served with rich truffle reduction.", "price": "185 AED", "tag": "Chef Special"},
            {"title": "Pan-Seared Sea Bass", "desc": "Crispy skin Mediterranean bass, wild asparagus, citrus saffron emulsion.", "price": "120 AED", "tag": "Fresh Catch"},
            {"title": "Truffle Burrata Heirloom", "desc": "Creamy Italian burrata, aged balsamic caviar, gold-leaf accents.", "price": "75 AED", "tag": "Appetizer"},
            {"title": "Deconstructed Velvet Fondant", "desc": "70% single-origin dark chocolate cake with Madagascan vanilla bean gelato.", "price": "48 AED", "tag": "Trending"}
        ]

    menu_html = ""
    for item in menu_items:
        menu_html += f"""
        <div class="glass-card menu-item-card">
            <div class="menu-item-header">
                <span class="menu-tag">{item['tag']}</span>
                <span class="menu-price">{item['price']}</span>
            </div>
            <h3>{item['title']}</h3>
            <p>{item['desc']}</p>
        </div>"""

    # Generate output raw string structure
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} | Haute Culinary Destination</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {{
            --primary: #D4AF37;
            --primary-rgb: 212, 175, 55;
            --bg-dark: #070708;
            --glass-card: rgba(18, 18, 24, 0.55);
            --glass-border: rgba(255, 255, 255, 0.08);
            --text-light: #F4F4F6;
            --text-dim: rgba(244, 244, 246, 0.65);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; scroll-behavior: smooth; }}
        body {{ background-color: var(--bg-dark); color: var(--text-light); overflow-x: hidden; }}

        /* Universal Glassmorphic Structural Class */
        .glass-card {{
            background: var(--glass-card);
            backdrop-filter: blur(24px) saturate(170%);
            -webkit-backdrop-filter: blur(24px) saturate(170%);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }}

        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}
        .badge {{
            display: inline-flex; align-items: center; gap: 6px;
            background: rgba(var(--primary-rgb), 0.12); border: 1px solid rgba(var(--primary-rgb), 0.3);
            color: var(--primary); padding: 6px 16px; border-radius: 100px;
            font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;
        }}

        /* 1. STICKY GLASS NAVIGATION ARCHITECTURE */
        nav {{
            position: fixed; top: 0; left: 0; width: 100%; z-index: 1000;
            background: rgba(7, 7, 8, 0.35); backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px); border-bottom: 1px solid var(--glass-border);
        }}
        .nav-container {{
            max-width: 1300px; margin: 0 auto; padding: 16px 24px;
            display: flex; justify-content: space-between; align-items: center;
        }}
        .brand-logo {{ font-weight: 800; font-size: 1.4rem; letter-spacing: -0.5px; color: #fff; text-decoration: none; }}
        .brand-logo span {{ color: var(--primary); }}
        .nav-links {{ display: flex; gap: 32px; list-style: none; align-items: center; }}
        .nav-links a {{ text-decoration: none; color: var(--text-dim); font-size: 0.9rem; font-weight: 500; transition: color 0.3s; }}
        .nav-links a:hover {{ color: var(--primary); }}
        .nav-cta {{
            background: var(--primary); color: #000; padding: 10px 20px; 
            border-radius: 10px; font-weight: 700; text-decoration: none; transition: transform 0.2s;
        }}
        .nav-cta:hover {{ transform: translateY(-2px); }}

        /* 2. MASSIVE PARALLAX HERO SECTION */
        .hero-section {{
            position: relative; min-height: 100vh; display: flex; align-items: center; justify-content: center;
            background: linear-gradient(180deg, rgba(7,7,8,0.2) 0%, var(--bg-dark) 95%), url('{bg_hero}');
            background-size: cover; background-position: center; text-align: center; padding-top: 100px;
        }}
        .hero-content {{ max-width: 850px; padding: 0 24px; }}
        .hero-section h1 {{ font-size: 4.5rem; font-weight: 800; letter-spacing: -2px; line-height: 1.1; margin: 24px 0; }}
        .hero-section p {{ font-size: 1.3rem; color: var(--text-dim); line-height: 1.6; margin-bottom: 40px; }}
        
        .hero-ctas {{ display: flex; gap: 16px; justify-content: center; }}
        .btn-main {{
            padding: 18px 36px; border-radius: 14px; font-size: 1rem; font-weight: 700;
            text-decoration: none; display: inline-flex; align-items: center; gap: 10px; transition: all 0.3s;
        }}
        .btn-gold {{ background: var(--primary); color: #000; box-shadow: 0 10px 30px rgba(212,175,55,0.3); }}
        .btn-gold:hover {{ transform: translateY(-3px); box-shadow: 0 15px 35px rgba(212,175,55,0.5); }}
        .btn-outline {{ border: 1px solid rgba(255,255,255,0.2); color: #fff; background: rgba(255,255,255,0.03); }}
        .btn-outline:hover {{ background: rgba(255,255,255,0.1); transform: translateY(-3px); }}

        /* 3. PERFORMANCE METRICS GRID (STATS SHOWCASE) */
        .stats-section {{ transform: translateY(-60px); position: relative; z-index: 10; margin-bottom: 40px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; padding: 32px; }}
        .stat-card {{ text-align: center; }}
        .stat-card h2 {{ font-size: 2.8rem; font-weight: 800; color: var(--primary); margin-bottom: 4px; }}
        .stat-card p {{ font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-dim); }}

        /* 4. IMMERSIVE PHILOSOPHY SECTION */
        .story-section {{ padding: 100px 0; }}
        .story-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; }}
        .story-img-frame {{
            position: relative; border-radius: 24px; overflow: hidden; height: 480px;
            box-shadow: 0 30px 60px rgba(0,0,0,0.6); border: 1px solid var(--glass-border);
        }}
        .story-img-frame img {{ width: 100%; height: 100%; object-fit: cover; }}
        .story-text h2 {{ font-size: 3rem; font-weight: 800; margin: 16px 0 24px 0; letter-spacing: -1px; }}
        .story-text p {{ color: var(--text-dim); font-size: 1.1rem; line-height: 1.7; margin-bottom: 24px; }}

        /* 5. DYNAMIC INTERACTIVE MENU SHOWCASE */
        .menu-section {{ padding: 100px 0; background: linear-gradient(180deg, var(--bg-dark) 0%, #0d0d11 50%, var(--bg-dark) 100%); text-align: center; }}
        .menu-header {{ max-width: 600px; margin: 0 auto 60px auto; }}
        .menu-header h2 {{ font-size: 3rem; font-weight: 800; margin: 16px 0; letter-spacing: -1px; }}
        .menu-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }}
        .menu-item-card {{ padding: 32px; text-align: left; transition: all 0.3s; }}
        .menu-item-card:hover {{ transform: translateY(-5px); border-color: rgba(212,175,55,0.3); }}
        .menu-item-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }}
        .menu-tag {{ font-size: 0.7rem; font-weight: 700; color: var(--primary); background: rgba(212,175,55,0.1); padding: 4px 10px; border-radius: 6px; text-transform: uppercase; }}
        .menu-price {{ font-size: 1.3rem; font-weight: 800; color: #fff; }}
        .menu-item-card h3 {{ font-size: 1.4rem; font-weight: 700; margin-bottom: 8px; }}
        .menu-item-card p {{ color: var(--text-dim); font-size: 0.95rem; line-height: 1.5; }}

        /* 6. SOCIAL PROOF / TRUST CAROUSEL */
        .reviews-section {{ padding: 100px 0; text-align: center; }}
        .reviews-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 50px; }}
        .review-card {{ padding: 32px; text-align: left; }}
        .stars-row {{ color: #FFD700; margin-bottom: 16px; font-size: 0.9rem; }}
        .review-card p {{ font-style: italic; color: var(--text-dim); line-height: 1.6; margin-bottom: 20px; }}
        .reviewer-meta {{ display: flex; align-items: center; gap: 12px; }}
        .avatar-circle {{ width: 44px; height: 44px; border-radius: 50%; background: #222; display: flex; align-items: center; justify-content: center; font-weight: 700; color: var(--primary); border: 1px solid var(--glass-border); }}
        
        /* 7. REVENUE-DRIVEN RESERVATION PIPELINE */
        .booking-section {{ padding: 100px 0; }}
        .booking-split {{ display: grid; grid-template-columns: 0.9fr 1.1fr; gap: 50px; align-items: stretch; }}
        .booking-info {{ padding: 40px; display: flex; flex-direction: column; justify-content: space-between; }}
        .contact-row {{ display: flex; align-items: center; gap: 20px; margin-top: 30px; }}
        .contact-icon {{ width: 50px; height: 50px; border-radius: 12px; background: rgba(255,255,255,0.04); display: flex; align-items: center; justify-content: center; color: var(--primary); font-size: 1.2rem; border: 1px solid var(--glass-border); }}
        
        .booking-form-panel {{ padding: 48px; border: 1px solid rgba(255,255,255,0.12); }}
        .form-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }}
        .form-group {{ margin-bottom: 20px; }}
        .form-group label {{ display: block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--text-dim); margin-bottom: 8px; }}
        .form-control {{ width: 100%; padding: 14px 18px; background: rgba(0,0,0,0.3); border: 1px solid var(--glass-border); border-radius: 10px; color: #fff; font-size: 1rem; outline: none; transition: border 0.3s; }}
        .form-control:focus {{ border-color: var(--primary); }}

        /* 8. EXPERT MULTI-COLUMN FOOTER */
        footer {{ background: #040405; padding: 80px 0 30px 0; border-top: 1px solid var(--glass-border); }}
        .footer-grid {{ display: grid; grid-template-columns: 1.5fr 1fr 1fr 1fr; gap: 40px; margin-bottom: 60px; }}
        .footer-col h4 {{ font-size: 1rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 24px; color: var(--primary); }}
        .footer-col p {{ color: var(--text-dim); line-height: 1.6; font-size: 0.95rem; }}
        .footer-col ul {{ list-style: none; }}
        .footer-col ul li {{ margin-bottom: 12px; }}
        .footer-col ul li a {{ text-decoration: none; color: var(--text-dim); font-size: 0.95rem; transition: color 0.2s; }}
        .footer-col ul li a:hover {{ color: #fff; }}
        .bottom-bar {{ display: flex; justify-content: space-between; align-items: center; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.05); font-size: 0.85rem; color: rgba(244,244,246,0.4); }}

        /* =====================================================================
           MOBILE DESIGN RULES (RESPONSIVE ENGINE)
           ===================================================================== */
        @media (max-width: 1024px) {{
            .hero-section h1 {{ font-size: 3.2rem; }}
            .story-grid, .booking-split, .menu-grid {{ grid-template-columns: 1fr; gap: 40px; }}
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); gap: 16px; }}
            .reviews-grid, .footer-grid {{ grid-template-columns: 1fr; gap: 30px; }}
            .story-img-frame {{ height: 350px; }}
        }}
        @media (max-width: 768px) {{
            .nav-links {{ display: none; }}
            .hero-section h1 {{ font-size: 2.6rem; }}
            .form-row {{ grid-template-columns: 1fr; gap: 0; }}
        }}
    </style>
</head>
<body>

    <nav>
        <div class="nav-container">
            <a href="#home" class="brand-logo">{name.split(' ')[0]}<span>.</span></a>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">Philosophy</a></li>
                <li><a href="#menu">Menu</a></li>
                <li><a href="#reviews">Reviews</a></li>
                <li><a href="#reserve">Reservations</a></li>
            </ul>
            <a href="#reserve" class="nav-cta">Book Table</a>
        </div>
    </nav>

    <section id="home" class="hero-section">
        <div class="hero-content">
            <div class="badge"><i class="fa-solid fa-crown"></i> Top-Tier Experience</div>
            <h1>The Apex of Fine {display_category} Cultures</h1>
            <p>Welcome to {name}. An architectural design escape constructed to deliver unmatched master craft recipes, elite guest-centric hospitality, and premium aesthetic comfort layouts.</p>
            <div class="hero-ctas">
                <a href="#reserve" class="btn-main btn-gold"><i class="fa-solid fa-calendar-days"></i> Instant RSVP Booking</a>
                <a href="#menu" class="btn-main btn-outline">Explore Selection Menu</a>
            </div>
        </div>
    </section>

    <div class="container stats-section">
        <div class="glass-card stats-grid">
            <div class="stat-card">
                <h2>{rating_val}</h2>
                <p>Google Rating</p>
            </div>
            <div class="stat-card">
                <h2>10k+</h2>
                <p>Guests Welcomed</p>
            </div>
            <div class="stat-card">
                <h2>100%</h2>
                <p>Artisan Sourced</p>
            </div>
            <div class="stat-card">
                <h2>15+</h2>
                <p>Master Craftsmen</p>
            </div>
        </div>
    </div>

    <section id="about" class="container story-section">
        <div class="story-grid">
            <div class="story-img-frame">
                <img src="{bg_story}" alt="Ambiance Portfolio View">
            </div>
            <div class="story-text">
                <div class="badge"><i class="fa-solid fa-feather-pointed"></i> Our Narrative</div>
                <h2>A Relentless Obsession with Quality Craft</h2>
                <p>At {name}, we think true quality requires focusing on every micro-interaction. From the lighting curves balancing our glass interiors to structural menu components, we engineer premium culinary assets daily.</p>
                <p>We source raw ingredients directly from protected micro-lots to ensure every single plate or beverage matches verified international master profiles seamlessly.</p>
            </div>
        </div>
    </section>

    <section id="menu" class="menu-section">
        <div class="container">
            <div class="menu-header">
                <div class="badge"><i class="fa-solid fa-wand-magic-sparkles"></i> Curated Selections</div>
                <h2>Explore Our Signature Menu</h2>
                <p>A premier dynamic catalog tracking fresh, seasonal components assembled on demand by our highly trained workspace team.</p>
            </div>
            <div class="menu-grid">
                {menu_html}
            </div>
        </div>
    </section>

    <section id="reviews" class="container reviews-section">
        <div class="badge"><i class="fa-solid fa-comment-heart"></i> Verified Feedback</div>
        <h2 style="font-size: 3rem; font-weight:800; margin-top:16px;">What Our Guests Celebrate</h2>
        <div class="reviews-grid">
            <div class="glass-card review-card">
                <div class="stars-row">{stars_html}</div>
                <p>"The architectural vibe here is pristine. Easily the absolute finest glassmorphism luxury structure in Abu Dhabi. Highly recommended!"</p>
                <div class="reviewer-meta">
                    <div class="avatar-circle">MA</div>
                    <div>
                        <h4 style="font-size:0.95rem; font-weight:700;">Mohammed Al-Ameri</h4>
                        <span style="font-size:0.8rem; color:var(--text-dim);">Google Local Guide</span>
                    </div>
                </div>
            </div>
            <div class="glass-card review-card">
                <div class="stars-row">{stars_html}</div>
                <p>"Unbelievable precision in taste curation and customer care. The team deals with hospitality at a world-class executive tier standard."</p>
                <div class="reviewer-meta">
                    <div class="avatar-circle">SK</div>
                    <div>
                        <h4 style="font-size:0.95rem; font-weight:700;">Sarah Khan</h4>
                        <span style="font-size:0.8rem; color:var(--text-dim);">Verified Luxury Critic</span>
                    </div>
                </div>
            </div>
            <div class="glass-card review-card">
                <div class="stars-row">{stars_html}</div>
                <p>"Every element, from instant automated WhatsApp booking flows to table placement, is flawless. A staple spot for my business syncs."</p>
                <div class="reviewer-meta">
                    <div class="avatar-circle">ER</div>
                    <div>
                        <h4 style="font-size:0.95rem; font-weight:700;">Elena Rostova</h4>
                        <span style="font-size:0.8rem; color:var(--text-dim);">Connoisseur Corporate Guest</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="reserve" class="container booking-section">
        <div class="glass-card booking-split">
            <div class="booking-info">
                <div>
                    <div class="badge" style="margin-bottom:16px;">VIP Access Concierge</div>
                    <h2 style="font-size:2.5rem; font-weight:800; line-height:1.2;">Secure Your Preferred Seating Layout</h2>
                    <p style="color:var(--text-dim); margin-top:12px; font-size:1rem; line-height:1.6;">Our real-time priority booking pipeline paths requests straight to on-site management tables immediately.</p>
                </div>
                
                <div class="contact-details">
                    <div class="contact-row">
                        <div class="contact-icon"><i class="fa-solid fa-location-dot"></i></div>
                        <div>
                            <h4 style="font-size:0.75rem; text-transform:uppercase; color:var(--text-dim);">Location Pin</h4>
                            <p style="font-weight:600; margin-top:2px;">{display_address}</p>
                        </div>
                    </div>
                    <div class="contact-row">
                        <div class="contact-icon"><i class="fa-solid fa-phone-volume"></i></div>
                        <div>
                            <h4 style="font-size:0.75rem; text-transform:uppercase; color:var(--text-dim);">Concierge Desk Line</h4>
                            <p style="font-weight:600; margin-top:2px;">{display_phone}</p>
                        </div>
                    </div>
                </div>
                
                <div>
                    {"<a href='" + maps_url + "' target='_blank' class='btn-main btn-outline' style='width:100%; justify-content:center;'><i class='fa-solid fa-map-location-dot'></i> Launch Interactive Google Map</a>" if pd.notna(maps_url) and maps_url else ""}
                </div>
            </div>

            <div class="glass-card booking-form-panel">
                <h3 style="font-size:1.8rem; font-weight:800; margin-bottom:8px;">Priority RSVP Form</h3>
                <p style="color:var(--text-dim); font-size:0.9rem; margin-bottom:30px;">Input basic configuration details below to spin up real-time availability sync.</p>
                
                <form onsubmit="handleMassiveBooking(event)">
                    <div class="form-group">
                        <label>Guest Full Name</label>
                        <input type="text" id="b_name" class="form-control" placeholder="E.g. Hamdan Al Maktoum" required>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Party Capacity Size</label>
                            <select id="b_size" class="form-control" style="background:#111116;">
                                <option>1-2 Seats (Executive Corner)</option>
                                <option>3-4 Seats (Standard Lounge)</option>
                                <option>5-8 Seats (Family Banquet)</option>
                                <option>9+ Seats (VIP Private Hall)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Seating Lounge Preference</label>
                            <select id="b_pref" class="form-control" style="background:#111116;">
                                <option>Indoor Smoking Bar</option>
                                <option>Outdoor Terrace Panoramic</option>
                                <option>Window Private Glass View</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Target Execution Date</label>
                            <input type="date" id="b_date" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label>Arrival Window Time</label>
                            <input type="time" id="b_time" class="form-control" required>
                        </div>
                    </div>
                    
                    <button type="submit" class="btn-main btn-gold" style="width:100%; justify-content:center; border:none; cursor:pointer; margin-top:10px;"><i class="fa-brands fa-whatsapp"></i> Dispatch Priority WhatsApp Reservation</button>
                </form>
            </div>
        </div>
    </section>

    <footer>
        <div class="container footer-grid">
            <div class="footer-col">
                <a href="#home" class="brand-logo" style="margin-bottom:20px; display:inline-block;">{name.split(' ')[0]}<span>.</span></a>
                <p style="margin-bottom:24px;">An exquisite lifestyle environment dedicated to redefining upscale culinary, cafe, and interaction spaces across the United Arab Emirates.</p>
                <div style="display:flex; gap:16px; font-size:1.2rem; color:var(--primary);">
                    <i class="fa-brands fa-instagram" style="cursor:pointer;"></i>
                    <i class="fa-brands fa-tiktok" style="cursor:pointer;"></i>
                    <i class="fa-brands fa-facebook" style="cursor:pointer;"></i>
                </div>
            </div>
            <div class="footer-col">
                <h4>Operations Hours</h4>
                <p style="margin-bottom:8px;">Weekdays: 08:00 AM - 12:00 AM</p>
                <p>Weekends: 07:00 AM - 02:00 AM</p>
            </div>
            <div class="footer-col">
                <h4>Quick Controls</h4>
                <ul>
                    <li><a href="#about">Philosophy</a></li>
                    <li><a href="#menu">Digital Menu</a></li>
                    <li><a href="#reviews">Guest Reviews</a></li>
                    <li><a href="#reserve">Priority VIP RSVP</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>Corporate</h4>
                <p style="font-size:0.85rem; line-height:1.5;">This live enterprise asset deployment represents an official performance concept showroom demonstration model.</p>
            </div>
        </div>
        <div class="container bottom-bar">
            <p>&copy; 2026 {name}. Verified Premium Signature Network.</p>
            <p>Designed via Elite Scale Digital Agency Automation Frameworks.</p>
        </div>
    </footer>

    <script>
        function handleMassiveBooking(e) {{
            e.preventDefault();
            const name = document.getElementById('b_name').value;
            const size = document.getElementById('b_size').value;
            const pref = document.getElementById('b_pref').value;
            const date = document.getElementById('b_date').value;
            const time = document.getElementById('b_time').value;
            
            const message = `Greetings Concierge Desk! I would like to lock in a VIP priority reservation at {name}.\\n\\n• Guest Name: ${{name}}\\n• Table Option: ${{size}}\\n• Area Choice: ${{pref}}\\n• Schedule Target: ${{date}} at ${{time}}\\n\\nPlease verify booking availability parameters. Thank you!`;
            const encoded = encodeURIComponent(message);
            
            const cleanPhoneTarget = "{phone_clean}";
            if(cleanPhoneTarget) {{
                window.open(`https://wa.me/${{cleanPhoneTarget}}?text=${{encoded}}`, '_blank');
            }} else {{
                alert("Reservation pipeline simulated! On the production server, this registers a permanent tracking ticket inside the venue's master dashboard.");
            }}
        }}
    </script>
</body>
</html>
"""
    return html_content

# =====================================================================
# SYSTEM COMPILATION WORKFLOW PIPELINE
# =====================================================================
def main():
    if not os.path.exists(INPUT_CSV):
        print(f"❌ Error: Cannot track CSV file path at '{INPUT_CSV}'")
        return

    df = pd.read_csv(INPUT_CSV)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    generated_links = []
    print(f"⚙️ Running massive portfolio generator across {len(df)} records...")

    for idx, row in df.iterrows():
        name = row['Place name']
        score = row.get('Total Score', 5.0)
        category = row.get('Category Name', 'Cafe')
        categories_all = row.get('Categories', 'Cafe')
        street = row.get('Street', '')
        city = row.get('City', 'Abu Dhabi')
        address = f"{street}, {city}".strip(", ")
        phone = row.get('Phone', '')
        maps_url = row.get('URL', '')
        
        slug = slugify(name)
        if not slug:
            slug = f"premium-showroom-{idx}"
            
        folder_path = os.path.join(OUTPUT_DIR, slug)
        os.makedirs(folder_path, exist_ok=True)
        
        # Build upgraded layout framework text array
        html_markup = generate_massive_glass_template(name, score, category, categories_all, address, phone, maps_url)
        
        with open(os.path.join(folder_path, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_markup)
            
        # Compile targeted reference links
        live_url = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/dist/{slug}/"
        generated_links.append(live_url)

    df['Demo Website URL'] = generated_links
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n🎉 Success! Massive interactive showrooms compiled completely within the '{OUTPUT_DIR}/' workspace directory.")
    print(f"📊 Tracking URLs systematically mapped to tracking register: '{OUTPUT_CSV}'")

if __name__ == "__main__":
    main()