import requests
try:
    res = requests.post('https://phisingdetectorsafeher-93wck0hd6-tamilselvanm30s-projects.vercel.app/api/scan-text', json={'text':'hello'})
    print(f"Status: {res.status_code}")
    print(res.text)
except Exception as e:
    print(e)
