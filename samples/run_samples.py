"""POST each samples/*.txt to a running ScamCheck server and print the verdict."""
import json, pathlib, sys, urllib.parse, urllib.request

url = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000") + "/api/analyze"
for f in sorted(pathlib.Path(__file__).parent.glob("*.txt")):
    body = urllib.parse.urlencode({"text": f.read_text()}).encode()  # form-encoded; Flask reads it via request.form
    try:
        d = json.load(urllib.request.urlopen(url, body, timeout=120))
        print(f"{f.name:15} {d['verdict'].upper():11} {d['confidence']:>3}%  {d['headline']}")
    except urllib.error.HTTPError as e:
        print(f"{f.name:15} HTTP {e.code}: {e.read().decode()[:200]}")
