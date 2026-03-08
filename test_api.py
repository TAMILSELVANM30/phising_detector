import requests

try:
    with open('requirements.txt', 'rb') as f:
        res = requests.post(
            'https://phisingdetectorsafeher-93wck0hd6-tamilselvanm30s-projects.vercel.app/api/scan-image', 
            files={'image': f}
        )
    print(f"Status: {res.status_code}")
    print(res.text)
except Exception as e:
    print(e)
