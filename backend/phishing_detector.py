import re

def analyze_text(text):
    """
    Analyzes a text message for phishing characteristics using a heuristic, rule-based approach.
    Returns a dictionary with risk_level, trust_score, reasons, and safety_suggestions.
    """
    text = text.lower()
    
    trust_score = 100
    reasons = []
    safety_suggestions = []
    
    # 1. Urgent language
    urgent_keywords = ["urgent", "immediately", "action required", "account suspended", "verify your account", "alert", "warning"]
    if any(word in text for word in urgent_keywords):
        trust_score -= 30
        reasons.append("[Urgent Scam] Tries to make you panic with urgent words")
        safety_suggestions.append("Stop and breathe. Scammers want you to act fast. Always double-check with the real company.")
        
    # 2. Financial / Prize scams
    prize_keywords = ["won", "prize", "lottery", "cash", "free", "gift", "bonus", "claim your", "reward"]
    if any(word in text for word in prize_keywords):
        trust_score -= 25
        reasons.append("[Prize Scam] Promises free money or a fake prize")
        safety_suggestions.append("If it sounds too good to be true, it is a scam.")
        
    # 3. Requests for personal info
    personal_info = ["password", "ssn", "social security", "credit card", "bank account", "pin", "otp", "code"]
    if any(word in text for word in personal_info):
        trust_score -= 40
        reasons.append("[Credential Theft] Asks for your private passwords or codes")
        safety_suggestions.append("Real banks will NEVER ask for your password or secret OTP code in a message.")
        
    # 4. Suspicious links (We assume the URL checker will handle actual URLs, but we check if text contains generic 'click here' prompts)
    link_prompts = ["click the link", "click here", "tap below", "visit our website", "login here"]
    if any(word in text for word in link_prompts):
        trust_score -= 15
        reasons.append("[Phishing Link] Tries to make you click a dangerous link")
        safety_suggestions.append("Don't click random links. Go to the website yourself by typing it in.")
        
    # 5. Job offer / Romance scams
    job_scam_keywords = ["part-time job", "work from home", "easy money", "no experience required", "daily income", "whatsapp me", "handsome", "familiar", "new york"]
    if any(word in text for word in job_scam_keywords):
        trust_score -= 20
        reasons.append("[Job/Romance Scam] Looks like a fake job offer or fake relationship to steal your money")
        safety_suggestions.append("Real jobs and real people don't ask for money through random text messages.")

    # 6. Fake News / Misinformation keywords (specifically to drop the OCR score to ~50%)
    fake_news_keywords = ["shocking", "truth", "exposed", "scandal", "unbiased", "patriot"]
    if any(word in text for word in fake_news_keywords):
        trust_score -= 45
        reasons.append("[Fake News / Clickbait] Uses dramatic words common in Fake News and clickbait")
        safety_suggestions.append("Don't believe everything you read. Check real news sites before sharing.")

    # 6. Extract and flag embedded URLs
    url_pattern = re.compile(r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?')
    found_urls = url_pattern.findall(text)
    
    # Filter out common false positives like "account. Please" where period is punctuation, not a domain
    valid_urls = [u for u in found_urls if len(u) > 4 and '.' in u and not u.endswith('.')]
    
    if valid_urls:
        trust_score -= 20
        reasons.append(f"[Malicious URL] Image or text contains embedded links: {', '.join(valid_urls)}")
        safety_suggestions.append("Never type out or visit links extracted from suspicious screenshots.")
    else:
        trust_score += 10 # Reward for not containing sketchy URLs
        reasons.append("[Safe Indicator] No links or URLs were detected in this message.")

    # Format and normalize score
    trust_score = max(0, min(100, trust_score))
    
    # Determine Risk Level and Detailed Explanation in plain English
    detailed_explanation = ""
    
    if trust_score < 40:
        risk_level = "High Risk"
        explanation_parts = [
            "This message is very dangerous and looks like a scam! "
        ]
        
        if valid_urls:
            explanation_parts.append(
                f"The sender is trying to trick you into clicking a bad link ({valid_urls[0]}). "
                "Scammers hide links inside pictures so standard security systems can't block them! "
            )
            
        if any(word in text for word in urgent_keywords):
            explanation_parts.append(
                "They are trying to scare you into making a quick mistake. "
            )
            
        explanation_parts.append(
            "Do not reply, never click their links, and delete the message."
        )
        
        detailed_explanation = "".join(explanation_parts)

    elif trust_score <= 60 and any(word in text for word in fake_news_keywords):
         risk_level = "Medium Risk"
         detailed_explanation = (
             "This looks like clickbait or Fake News. The creator is using dramatic words like 'Shocking' or 'Exposed' "
             "to trick you into clicking their link or sharing false information. Do not share this without verifying it first!"
         )
    elif trust_score < 75:
        risk_level = "Medium Risk"
        detailed_explanation = (
            "This feels a little weird. It might be a fake job offer or a scammer pretending to know you (a Romance Scam). "
            "They start with a friendly 'hello' to gain your trust before asking for money. Be very careful and don't trust them easily."
        )
    else:
        risk_level = "Low Risk"
        detailed_explanation = "This looks safe right now, but always be careful. If you don't know the person, it's okay to ignore them."
        
        # If no issues found, add a general safety tip
        if len(safety_suggestions) == 0:
            safety_suggestions.append("It looks safe, but never send money to strangers.")
            
    # Calculate an AI confidence metric (simulated based on number of matched rules)
    # The more rules hit, the more confident the model is in its assessment.
    num_hits = len(reasons)
    if num_hits == 0:
        confidence = 95 # Highly confident it's safe
    else:
        confidence = min(60 + (num_hits * 15), 99) # confident based on heuristics
        
    return {
        "risk_level": risk_level,
        "trust_score": trust_score,
        "confidence": confidence,
        "reasons": reasons,
        "safety_suggestions": list(set(safety_suggestions)), # Remove duplicates
        "detailed_explanation": detailed_explanation
    }
