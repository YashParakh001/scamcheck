# ScamCheck

Drop in a screenshot or paste a suspicious text, email or URL and get a scam verdict from Gemini (Interactions API + Google Search grounding).

## Run

```bash
pip install -r requirements.txt
echo GEMINI_API_KEY=your-key > .env   # optional second line: GEMINI_MODEL=gemini-3.8-flash
python app.py
```

Open http://localhost:5000.

## Demo prep

With the server running:

```bash
python samples/run_samples.py
```

This sends the three sample messages (phishing, fake USPS notice, legitimate GitHub email) and prints each verdict.
