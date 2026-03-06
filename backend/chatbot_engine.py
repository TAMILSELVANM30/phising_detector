import re

def get_chatbot_response(message):
    """
    A robust rule-based intent matching engine tailored for Women's Cyber Safety and General Phishing Education.
    """
    msg = message.lower()
    
    # INTENT: Romance Scams
    import random
    
    # EXACT PHRASING MATCHES (Highest Priority)
    if msg == "hello" or msg == "hi" or msg == "hey" or msg == "start":
        return "Hello there! I'm Aura, your Cyber Safety Teacher. Think of me as a friendly guide who can help you spot online tricks. What would you like to learn about today? You can ask me about fake links, romance scams, or how to secure your accounts."
        
    if msg == "help":
        return "I'm here to help make the internet less confusing! Try asking me a direct question like:\n- What is a phishing link?\n- How do I know if a job offer is fake?\n- What should I do if my account is hacked?"

    # WHAT IS A SCAM / PHISHING (Basic Education)
    if any(keyword in msg for keyword in ['what is a scam', 'what is phishing', 'what is phish', 'explain scam']):
        return (
            "**What is Phishing?** \n\n"
            "Think of phishing like someone wearing a mask. A scammer sends you a message pretending to be someone you trust—like your bank, Amazon, or even your boss—and tries to trick you into handing over your password or money. \n\n"
            "**My Advice:** Never click links in random emails or texts. If your bank needs you, type their website directly into your browser yourself!"
        )

    # INTENT: Deepfakes & AI Voice Cloning
    if any(keyword in msg for keyword in ['deepfake', 'voice clone', 'ai generated', 'fake video', 'ai image', 'ai voice']):
        return (
            "**Deepfakes and AI Voices** \n\n"
            "Nowadays, scammers can use computer programs to copy exactly what your friends or family sound like! They might call you sounding like your child, crying that they need bail money.\n\n"
            "**My Advice:** If a loved one calls begging for money from a weird number, hang up immediately! Call them back on the real number you have saved in your phone to check if they are actually okay."
        )

    # INTENT: Crypto & Investment Scams (Pig Butchering)
    elif any(keyword in msg for keyword in ['crypto', 'bitcoin', 'investment', 'trading', 'forex', 'returns', 'guaranteed profit']):
        return (
            "**Fake Investments (Crypto Scams)** \n\n"
            "Has a stranger ever texted you 'by accident', become your friend, and then told you they make huge money trading crypto? That is a scam. They will show you a fake website where it looks like you are making money, but when you try to take your cash out, it's gone.\n\n"
            "**My Advice:** Real investments do not happen through WhatsApp or random text messages. Keep your money safe in real banks."
        )

    # INTENT: Tech Support Scams
    elif any(keyword in msg for keyword in ['tech support', 'microsoft', 'apple support', 'virus popup', 'computer infected', 'remote access', 'anydesk']):
        return (
            "**Tech Support Scams** \n\n"
            "If a scary red box pops up on your computer saying 'WARNING: You have a virus, call this number!', do not call it. It is a trick.\n\n"
            "**My Advice:** Real companies like Microsoft and Apple will *never* call you out of nowhere to fix your computer. Just close the window or restart your computer."
        )

    # INTENT: Giveaways & Lottery Scams
    elif any(keyword in msg for keyword in ['iphone', 'lottery', 'giveaway', 'won a prize', 'lucky winner', 'claim prize']):
        return (
            "**Fake Prize Scams** \n\n"
            "Did you get a text saying you won a free iPhone or a massive lottery? Notice how they always ask you to click a link or pay a small 'shipping fee' to get your free prize?\n\n"
            "**My Advice:** If you didn't buy a ticket, you didn't win the lottery. Never pay money to receive a 'free' prize."
        )

    # INTENT: Password Security
    elif any(keyword in msg for keyword in ['password', 'secure', '2fa', 'authenticator', 'mfa']):
        return (
            "**How to make strong passwords:** \n\n"
            "The biggest mistake people make is using the same password for their email and their bank. If one website gets hacked, the scammers try that password everywhere!\n\n"
            "**My Advice:** Make your passwords long, like a sentence (e.g., 'MyCatEats2Apples!'). And always turn on 'Two-Factor Authentication' so even if they guess your password, they can't get in without your phone."
        )

    # INTENT: Romance Scams
    elif any(keyword in msg for keyword in ['romance', 'dating', 'tinder', 'bumble', 'love', 'boyfriend', 'girlfriend', 'sugar daddy', 'military doctor']):
        return (
            "**Romance Scams** \n\n"
            "These break my heart. Scammers will spend weeks talking to you on dating apps or Instagram, making you fall in love with them. But they will always have an excuse for why they can't meet in person or do a video call. Eventually, they will have a 'medical emergency' and beg you for money.\n\n"
            "**My Advice:** Never, ever send money, gift cards, or crypto to someone you have not met in real life."
        )
        
    # INTENT: Job Offer Scams
    elif any(keyword in msg for keyword in ['job', 'work from home', 'part time', 'hiring', 'recruiter', 'salary', 'daily income', 'data entry']):
        return (
            "**Fake Job Offers** \n\n"
            "If a strange number texts you offering $200 a day for 'easy remote work' like just liking YouTube videos, it is a trap. They want to steal your personal info or make you pay an 'onboarding fee'.\n\n"
            "**My Advice:** Real jobs won't hire you through random WhatsApp texts. And a real employer will never ask *you* to pay *them* to start working."
        )
        
    # INTENT: Online Harassment / Cyberstalking
    elif any(keyword in msg for keyword in ['harass', 'stalk', 'bully', 'threaten', 'blackmail', 'photos', 'nudes', 'sextortion']):
        return (
            "**Online Blackmail (Sextortion)** \n\n"
            "This is very serious. If someone is threatening you, saying they will post private photos of you online unless you pay them, it is incredibly scary. \n\n"
            "**My Advice:** Do not pay them. If you pay, they will just demand more money tomorrow. Take screenshots of their threats, block their account, and contact the police."
        )

    # INTENT: Identity Theft / Hacked Account
    elif any(keyword in msg for keyword in ['hack', 'stolen', 'identity', 'breach', 'lost account', 'locked out']):
        return (
            "**What to do if you are hacked:** \n\n"
            "Stay calm! If you can still log in, change your password immediately. If you are totally locked out, use the website's 'Recover Account' page.\n\n"
            "**My Advice:** Warn your friends! Hackers will use your stolen account to message your friends and try to scam them, because your friends trust your name."
        )

    # --- MASSIVE CYBERSECURITY DICTIONARY ---

    # HTTP vs HTTPS
    elif any(keyword in msg for keyword in ['http', 'https', 'padlock', 'secure connection', 'ssl', 'tls']):
        return (
            "**What is HTTPS?** \n\n"
            "HTTPS (with the 'S' for Secure) means the connection between your computer and the website is locked. If you type in a password, hackers on the same Wi-Fi can't read it.\n\n"
            "**My Advice:** Just because a website has HTTPS or a 'padlock' icon does NOT mean it's safe! Scammers can easily buy HTTPS for their fake websites. Always check the spelling of the domain."
        )

    # Malware General (Virus, Trojan, Worm)
    elif any(keyword in msg for keyword in ['malware', 'virus', 'trojan', 'worm']):
        return (
            "**What is Malware?** \n\n"
            "Malware stands for 'Malicious Software'. It's bad code that gets onto your device to break things or steal your data.\n"
            "- **Virus:** Attaches to a clean file and infects your computer when you open it.\n"
            "- **Trojan:** Pretends to be a useful program (like a free game) but secretly installs a backdoor for hackers.\n\n"
            "**My Advice:** Never download apps or programs from random websites. Only use the official App Store or Google Play Store."
        )

    # Ransomware
    elif any(keyword in msg for keyword in ['ransomware', 'ransom', 'files locked', 'encrypting my files']):
        return (
            "**What is Ransomware?** \n\n"
            "Ransomware is a terrible type of malware that locks all the files, photos, and documents on your computer. The hacker then tells you they will only unlock them if you pay a 'ransom' in Bitcoin.\n\n"
            "**My Advice:** The best defense is to always have a backup of your important files on an external hard drive or in the cloud. And be careful opening email attachments!"
        )

    # Spyware & Keyloggers
    elif any(keyword in msg for keyword in ['spyware', 'keylogger', 'tracking me', 'camera hacked']):
        return (
            "**What is Spyware?** \n\n"
            "Spyware secretly watches what you do. A **Keylogger** is a specific type of spyware that records every single key you press—including your passwords!\n\n"
            "**My Advice:** Only install software from official sources, and keep your computer's antivirus program turned on. Cover your webcam when you aren't using it."
        )

    # Adware
    elif any(keyword in msg for keyword in ['adware', 'popups', 'too many ads', 'browser hijacked']):
        return (
            "**What is Adware?** \n\n"
            "Adware isn't usually extremely dangerous, but it is annoying. It's software that bombards you with pop-up ads or redirects your internet browser to strange search engines to make money for the creator.\n\n"
            "**My Advice:** Use a good Adblocker (like uBlock Origin) and uninstall any weird browser extensions you don't recognize."
        )

    # Cookies
    elif any(keyword in msg for keyword in ['cookie', 'tracking cookie', 'cache']):
        return (
            "**What are Online Cookies?** \n\n"
            "Cookies are tiny text files websites save on your computer. They help the website remember you (so you don't have to log in every time you open a new tab). But 'Tracking Cookies' follow you across the internet to figure out what ads to show you.\n\n"
            "**My Advice:** You don't need to fear all cookies. But you can set your browser to 'Block Third-Party Cookies' to stop creepy tracking."
        )

    # Firewalls
    elif any(keyword in msg for keyword in ['firewall', 'network defense']):
        return (
            "**What is a Firewall?** \n\n"
            "Think of a firewall as a security guard standing at the door of your computer. It checks all the internet traffic trying to come in and go out, and blocks anything that looks dangerous.\n\n"
            "**My Advice:** Leave the default firewall turned on in Windows or Mac settings! It is your first line of defense."
        )

    # Encryption / E2EE
    elif any(keyword in msg for keyword in ['encryption', 'encrypted', 'e2ee', 'end to end']):
        return (
            "**What is End-to-End Encryption (E2EE)?** \n\n"
            "If an app like WhatsApp uses E2EE, it means your message is locked on your phone and can ONLY be unlocked by your friend's phone. Even the company that owns the app cannot read your messages!\n\n"
            "**My Advice:** Use encrypted messaging apps (like Signal or WhatsApp) for private conversations."
        )

    # IP Addresses
    elif any(keyword in msg for keyword in ['ip address', 'my ip', 'what is ip']):
        return (
            "**What is an IP Address?** \n\n"
            "An IP address is the digital 'home address' of your internet connection. Whenever you visit a website, the website needs your IP address to know where to send the page back to.\n\n"
            "**My Advice:** Your IP address reveals a rough estimate of what city you live in. If you want to hide it, use a Virtual Private Network (VPN)."
        )

    # Botnets / DDoS
    elif any(keyword in msg for keyword in ['botnet', 'ddos', 'denial of service', 'website down']):
        return (
            "**What are Botnets and DDoS Attacks?** \n\n"
            "A **Botnet** is an army of hacked computers acting like zombies controlled by a hacker. The hacker uses this army to flood a website with millions of fake clicks all at once, causing the website to crash. This is called a **DDoS** attack.\n\n"
            "**My Advice:** This mostly affects big companies, but keeping your devices updated ensures your computer doesn't get tricked into joining a zombie botnet."
        )
        
    # Zero-Day
    elif any(keyword in msg for keyword in ['zero day', '0 day', '0day', 'zero-day']):
        return (
            "**What is a Zero-Day Vulnerability?** \n\n"
            "Imagine a thief discovering a secret broken window on a house, but the owner doesn't know about it yet. A 'Zero-Day' is a completely brand new flaw in software that the creators have had 'zero days' to fix.\n\n"
            "**My Advice:** You can't perfectly stop a zero-day attack, which is why it is critical to always install 'Security Updates' on your phone and computer the moment they become available."
        )

    # CHAT BOT PERSONALITY
    elif any(keyword in msg for keyword in ['who are you', 'what are you', 'your name', 'are you ai', 'are you a real person']):
        return (
            "I'm **CyberAura**, an artificial intelligence built to be your personal Cyber Safety Teacher. "
            "I don't just find scams—I want to teach you exactly how they work so you never get tricked in the real world. Ask me a question!"
        )

    # PLATFORM FEATURES & EDUCATION (AI Confidence Meter, Scores, Website Terminology)
    elif any(keyword in msg for keyword in ['confidence meter', 'ai confidence', 'what is confidence']):
        return (
            "**The AI Confidence Meter** is a special feature on our Results Page. While the Trust Score tells you *how dangerous* a message is, the Confidence Meter tells you *how sure the AI is* about its decision! \n\n"
            "If the AI sees 3 or 4 clear scam keywords (like 'urgent' and 'password'), the Confidence Meter will be very high (90%+). If the text is weird but doesn't hit many rules, the confidence might be lower."
        )

    elif any(keyword in msg for keyword in ['what is trust score', 'safety score', 'how does scoring work', 'score meaning']):
        return (
            "**Your Trust Score (or Safety Score)** starts at 100% (Perfectly Safe).\n"
            "Whenever our AI finds something suspicious—like a fake URL, a request for money, or urgent scam words—it subtracts points. \n\n"
            "- **60-100%**: Low Risk (Safe, but be careful)\n"
            "- **40-59%**: Medium Risk (Suspicious, verify before trusting)\n"
            "- **0-39%**: High Risk (Extremely dangerous, delete immediately!)"
        )
        
    elif any(keyword in msg for keyword in ['how to use', 'scan image', 'scan text', 'dashboard', 'features']):
        return (
            "**Welcome to the CyberGuard Platform!** Here is how you use it:\n\n"
            "1. **Text Scanner**: Paste any weird email or SMS you receive. I will look for money requests, urgent words, or fake job offers.\n"
            "2. **URL Scanner**: Paste a suspicious link before clicking it! I will check if it's a fake clone website.\n"
            "3. **Image Scanner**: Upload a screenshot of a weird Instagram DM or suspicious payment receipt. I will actually *read* the text inside the image to catch scams!"
        )

    # DEFAULT FALLBACK
    else:
        responses = [
            "I want to make sure I am giving you the easiest answer! I am trained mostly on how to spot scams and protect your accounts. If you don't know what to ask, try: 'What is a fake job offer?' or 'How do I know if this link is safe?'",
            "Think of me as your online safety teacher! I don't know the answer to every riddle, but I am an expert in stopping scammers. Could you ask me about 'Crypto Scams' or 'Romance Scams' instead?",
            "Hmm, that's a bit outside my lesson plan! Could you ask your question in a slightly simpler way? I love answering questions about online safety and how to protect yourself on social media."
        ]
        return random.choice(responses)
