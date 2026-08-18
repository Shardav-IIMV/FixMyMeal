# FixMyMeal

**Transparent food quality tracking for your hostel mess.**

A Digital Product Management course project demonstrating product thinking, appropriate AI integration, and user-centred MVP design.

---

## Product Overview

### Target User
Hostel resident/student

### Problem
Students can report mess food issues, but complaints are often fragmented, unstructured, and difficult to convert into visible evidence that leads to action.

### Solution
A transparent platform where students report food-quality issues. AI-powered analysis (Gemini) converts unstructured complaints into structured, neutral incident records.

### Primary Use Case
A student reports a food quality issue with AI-assisted structuring.

### User Workflow
- Student opens FixMyMeal
- Selects "Report an Issue"
- Enters meal + complaint
- Optionally uploads photo
- Clicks "Analyse Report"
- Gemini analyzes and returns: category, severity, summary
- Student reviews AI output
- Clicks "Confirm & Submit"
- Issue appears in feed

---

## Technology Stack

- **Framework**: Streamlit (Python)
- **AI**: Google Gemini 1.5 Flash
- **Language**: Python 3.8+
- **Deployment**: Streamlit Cloud
- **Storage**: Session state (MVP)

---

## Project Structure

```
FixMyMeal/
├── streamlit_app.py          # Main app
├── gemini_service.py         # AI integration
├── models.py                 # Data models
├── data.py                   # Mock data
├── utils.py                  # Helpers
├── requirements.txt          # Dependencies
├── README.md                 # This file
├── .gitignore
└── .env.example
```

---

## Quick Start

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```
GEMINI_API_KEY=your_key_here
```

3. Run app:
```bash
streamlit run streamlit_app.py
```

Visit `http://localhost:8501`

### Streamlit Cloud Deployment

1. Push to GitHub
2. Open [share.streamlit.io](https://share.streamlit.io)
3. Select repo: `Shardav-IIMV/FixMyMeal`
4. Main file: `streamlit_app.py`
5. Add secret in Advanced Settings:
   ```
   GEMINI_API_KEY = "your_key"
   ```

---

## Features

### ✅ Included
- Home page with today's menu & recent issues
- Report issue page with meal selector
- Optional photo upload
- Gemini AI analysis (category, severity, summary)
- Human-in-the-loop review before submit
- Issue feed with filtering & sorting
- Issue detail page
- Session-state persistence

### ❌ NOT Included
- Authentication
- Persistent database
- Admin dashboard
- Resolution workflow
- Notifications
- Analytics
- Advanced AI features

---

## AI Integration

### What Gemini Does
- Analyzes student complaints
- Classifies into categories: Hygiene, Taste, Quantity, Timing, Other
- Assigns severity: Low, Medium, High, Critical
- Generates neutral, factual summary

### Important Constraints
- Uses cautious language: "reported", "possible", "appears"
- Never identifies people in images
- No medical diagnoses
- No invented facts
- Always human-reviewable

---

## Error Handling

Gracefully handles:
- Missing API key
- Gemini API errors
- Network timeouts
- Invalid images
- Malformed responses
- Empty input
- Rate limiting

---

## Gemini API Setup

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create API Key
3. Add to `.env` (local) or Streamlit Secrets (cloud)

⚠️ Never commit real keys to GitHub.

---

## Testing

- [ ] Home page loads
- [ ] Menu displays correctly
- [ ] Report form accepts input
- [ ] Image upload works
- [ ] Gemini analysis succeeds
- [ ] Edit/reanalyze works
- [ ] Confirm & Submit adds issue
- [ ] Issue appears in feed
- [ ] Filtering works
- [ ] Sorting works
- [ ] Detail page works
- [ ] Missing API key shows error
- [ ] Validation errors work

---

## Limitations

- Session state only (issues lost on refresh)
- No authentication
- No persistent database
- No admin workflow
- No notifications

**All intentional for MVP scope.**

---

## Future Phases

- Phase 2: Database + persistent storage
- Phase 3: Analytics & insights
- Phase 4: Admin dashboard
- Phase 5: Advanced AI
- Phase 6: Notifications
- Phase 7: Multi-hostel support

---

## Course Context

This demonstrates:
- ✅ Customer understanding
- ✅ Problem definition
- ✅ Product thinking
- ✅ Appropriate AI use
- ✅ MVP discipline
- ✅ Human-in-the-loop design

---

## License

ISC

---

**FixMyMeal MVP — Transparent food quality tracking for college hostels.**

*Built for Digital Product Management course.*
