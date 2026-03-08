import re
import urllib.parse

def analyze_url(url):
    """
    Analyzes a URL for suspicious phishing characteristics.
    Returns a dictionary with risk_level, trust_score, reasons, and safety_suggestions.
    """
    if not url.startswith('http'):
        url = 'https://' + url

    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path
    protocol = parsed_url.scheme
    
    # Extract TLD from domain
    domain_parts = domain.split('.')
    tld = '.' + domain_parts[-1] if len(domain_parts) > 1 else ''
    domain_name = domain.replace(tld, '') if tld else domain
    
    trust_score = 100
    reasons = []
    safety_suggestions = [
        "Always verify the sender before clicking links.",
        "Check for spelling errors in the domain name."
    ]
    
    # 1. Check for IP address in domain (common in phishing)
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain):
        trust_score -= 60
        reasons.append("URL uses an IP address instead of a domain name")
        
    # 2. Check for suspicious keywords in domain or path
    suspicious_keywords = ["free", "gift", "prize", "winner", "update", "verify", "secure", "login", "account", "support", "billing"]
    found_keywords = [kw for kw in suspicious_keywords if kw in domain.lower() or kw in path.lower()]
    
    if found_keywords:
        trust_score -= (30 * len(found_keywords))
        reasons.append(f"Suspicious keywords detected: {', '.join(found_keywords)}")
        
    # 3. Check for excessive hyphens in domain
    if domain.count('-') > 2:
        trust_score -= 40
        reasons.append("Domain name pattern contains multiple hyphens")
        
    # 4. Check for unusual TLDs often used for spam
    unusual_tlds = [".xyz", ".top", ".loan", ".win", ".club", ".tk", ".ml"]
    if any(domain.endswith(tld) for tld in unusual_tlds):
        trust_score -= 50
        reasons.append("Domain uses a top-level domain commonly associated with spam")
        
    # 5. Check for fake news / clickbait / disinformation keywords
    fake_news_keywords = ["gossip", "shocking", "truth", "exposed", "scandal", "daily", "buzz", "viral", "unbiased", "patriot", "report", "news-update", "breaking"]
    found_fake_news_keywords = [kw for kw in fake_news_keywords if kw in domain.lower()]
    
    if found_fake_news_keywords:
        trust_score -= (25 * len(found_fake_news_keywords))
        reasons.append(f"Domain contains patterns typical of unreliable news or clickbait: {', '.join(found_fake_news_keywords)}")

    # 6. Check URL length
    if len(url) > 75:
        trust_score -= 15
        reasons.append("URL is unusually long, which can hide the true destination")
        
    # Normalize score
    trust_score = max(0, min(100, trust_score))
    
    # Determine Risk Level and Explanation
    detailed_explanation = ""
    
    if trust_score < 40:
        risk_level = "High Risk"
        safety_suggestions.append("Do not enter any personal or financial information on this site.")
        detailed_explanation = (
            "This link exhibits severe signs of being a phishing or scam website. "
            "Attackers often use misleading patterns like suspicious keywords (e.g., 'free', 'prize') and unusual top-level domains to trick victims into believing the site is legitimate. "
            "Never click on unexpected links sent via SMS or social media, especially those claiming you've won something or urgently need to verify an account."
        )
    elif trust_score < 75:
        risk_level = "Medium Risk"
        safety_suggestions.append("Proceed with caution. Verify the source independently.")
        detailed_explanation = (
            "This link has some concerning elements. It might be a legitimate site with a poor URL structure, or it could be a newer scam attempt. "
            "Always verify the sender's identity. If a 'friend' sent this out of nowhere, their account might be compromised."
        )
    else:
        risk_level = "Low Risk"
        detailed_explanation = "This link appears structurally safe. However, always remain vigilant as attackers continuously evolve their methods."
        
    return {
        "risk_level": risk_level,
        "trust_score": trust_score,
        "reasons": reasons,
        "safety_suggestions": safety_suggestions,
        "detailed_explanation": detailed_explanation,
        "url_components": {
            "protocol": protocol + '://' if protocol else '',
            "domain_name": domain_name,
            "tld": tld,
            "path": path
        }
    }
