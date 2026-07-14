# EasyBirth — Demo Completion TODO
**Project:** AmaraAI / EasyBirth · COUCH 2026 Healthcare Track  
**Status:** Foundation built · Moving to working demo  
**Last updated:** July 2026

---

## How to read this doc

Each task has a **priority tag**:
- `🔴 CRITICAL` — demo breaks without this
- `🟡 IMPORTANT` — judges will notice if missing  
- `🟢 POLISH` — makes the demo better, not required to function

And an **owner tag**:
- `[FE]` — Flutter frontend developer
- `[BE]` — Python backend developer  
- `[BOTH]` — requires coordination between both

Work in the order presented. Do not skip 🔴 items.

---

## PHASE 1 — Critical Path (do this first, demo works after)

Goal: A complete voice triage loop that actually runs end-to-end.  
Home → Voice → Agent asks follow-up → Result → Action.

---

### 1.1 Wire Frontend to Backend `[BOTH]` 🔴

The backend is scaffolded but the Flutter app currently does everything
locally. You need a real API connection before anything else matters.

**Backend tasks:**
- [ ] Confirm backend runs locally: `uvicorn api.main:app --reload --port 8000`
- [ ] Confirm `/health` endpoint returns `{ "status": "ok" }` 
- [ ] Add `ANTHROPIC_API_KEY` to `.env` and verify it loads via `settings.py`
- [ ] Make sure CORS in `main.py` allows `*` for local dev (tighten for prod later)

**Frontend tasks:**
- [ ] Create `lib/services/api_service.dart` — single Dio client wrapping all backend calls
- [ ] Set base URL via `lib/config/` — `http://10.0.2.2:8000` for Android emulator,
  `http://localhost:8000` for iOS simulator
- [ ] Add `dio: ^5.4.3` to `pubspec.yaml` if not already there
- [ ] Test: call `/health` from Flutter and print result to console

```dart
// lib/services/api_service.dart — minimal starting point
class ApiService {
  final Dio _dio = Dio(BaseOptions(
    baseUrl: AppConfig.apiBaseUrl,
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 30),
  ));

  Future<bool> checkHealth() async {
    try {
      final res = await _dio.get('/health');
      return res.data['status'] == 'ok';
    } catch (_) { return false; }
  }
}
```

---

### 1.2 Risk Assessment Endpoint — Make It Real `[BE]` 🔴

The `/api/v1/risk` route exists but needs to actually call Claude and
return a structured triage response the Flutter app can use.

- [ ] Open `backend/api/routes/` — find the risk/assessment route file
- [ ] Replace any stub/mock response with a real Anthropic API call
- [ ] Use `claude-haiku-4-5` model (fast, low cost, good enough for demo)
- [ ] Request body should accept:
  ```python
  class TriageRequest(BaseModel):
      transcript: str           # raw speech text from Flutter
      language: str             # "hausa" | "yoruba" | "igbo" | "pidgin"
      session_id: str           # UUID
      conversation_history: list[dict]  # prior turns
      gestational_week: int
      patient_name: str = "Patient"
  ```
- [ ] Response must return:
  ```python
  class TriageResponse(BaseModel):
      decision: str             # "need_more_info" | "conclude"
      follow_up_question: str | None    # in target language
      risk_level: str | None            # "HIGH" | "MODERATE" | "LOW"
      detected_symptoms: list[str]
      recommendation: str | None        # in target language
      reasoning: str | None
  ```
- [ ] System prompt in `backend/api/services/` — tell Claude to behave as
  a midwife, ask at most one follow-up question per turn, respond in
  the target language, and always return valid JSON
- [ ] Test with curl before moving to Flutter:
  ```bash
  curl -X POST http://localhost:8000/api/v1/risk/assess \
    -H "Content-Type: application/json" \
    -d '{"transcript":"I have a bad headache","language":"hausa","session_id":"test-123","conversation_history":[],"gestational_week":30}'
  ```

---

### 1.3 Complete the Voice Triage Loop `[FE]` 🔴

You have `voice_listening_screen.dart` but the full flow needs to be
connected: listen → send to backend → process → result.

- [ ] In `voice_listening_screen.dart`, after the user taps "Done":
  - Take the transcript text
  - Call `ApiService().runTriageTurn(transcript, language, sessionId, history)`
  - Navigate to `ProcessingScreen` while awaiting the response
- [ ] Build `lib/screens/processing_screen.dart` (the orb in processing state)
  - Dark background `#0D1F17`
  - Orb animating with rotating conic gradient
  - Status text: "Checking your symptoms…"
  - Auto-navigates when API response arrives
- [ ] Build `lib/screens/risk_result_screen.dart`
  - Receives `TriageResponse` from API
  - If `decision == "need_more_info"`: speak follow-up via TTS, return
    to listening screen with follow-up question pre-loaded
  - If `decision == "conclude"`: show full risk result UI
- [ ] The Risk Result screen must show:
  - Risk pill (HIGH / MODERATE / LOOKING GOOD) with semantic colors
  - Detected symptoms as chips
  - Recommendation text in local language
  - Action buttons: Find PHC · Call CHW · Learn more
- [ ] Wire TTS: use `flutter_tts` to speak agent's follow-up question and
  final recommendation aloud in the target language
  ```dart
  final FlutterTts tts = FlutterTts();
  await tts.setLanguage("ha-NG"); // Hausa
  await tts.speak(response.followUpQuestion!);
  ```

---

### 1.4 The Orb Widget — Unify All 4 States `[FE]` 🔴

The orb appears across multiple screens. It must be a single reusable
widget with 4 clean state transitions.

- [ ] Create `lib/widgets/the_orb.dart` as a standalone `StatefulWidget`
- [ ] Accept `OrbState orbState` enum: `idle | listening | processing | result`
- [ ] Idle: 180dp, `#1B6B4A`, scale 0.97→1.03 pulse loop, radial glow
- [ ] Listening: 240dp, white, 3 staggered expanding ring animations
- [ ] Processing: 200dp, gradient `#1B6B4A`→`#6B4E9E`, rotating ring
- [ ] Result: snaps to semantic color (green/red/amber), elastic settle pulse
- [ ] Add `Hero(tag: 'main_orb')` wrapper so it transitions smoothly between screens
- [ ] Replace any existing orb/mic button in `home_screen.dart` and
  `voice_listening_screen.dart` with this single widget

---

### 1.5 Language State — Make It Global `[FE]` 🔴

Right now the language selection may not be passed through all screens.
Every screen that touches voice, TTS, or API calls needs the current language.

- [ ] Create `lib/providers/language_provider.dart`
  ```dart
  enum AppLanguage { hausa, yoruba, igbo, pidgin }
  
  class LanguageNotifier extends StateNotifier<AppLanguage> {
    LanguageNotifier() : super(AppLanguage.hausa);
    void setLanguage(AppLanguage lang) => state = lang;
  }
  ```
- [ ] Wrap app in `ProviderScope` in `main.dart` if not already
- [ ] All API calls pass `language: ref.read(languageProvider).name`
- [ ] All TTS calls use the correct `setLanguage()` for selected language:
  - Hausa: `ha-NG`
  - Yoruba: `yo-NG`  
  - Igbo: `ig-NG`
  - Pidgin: `en-NG` (closest available)
- [ ] Suggestion chips on home screen must update when language changes

---

## PHASE 2 — Full Demo Features (do this second)

Goal: All screens a judge will click through work properly.

---

### 2.1 Onboarding — Connect to Navigation Flow `[FE]` 🟡

The onboarding screen was built. Make sure it's wired into the app correctly.

- [ ] In `main.dart` — check `SharedPreferences` for `onboarding_complete` key
  - If false/missing → show `OnboardingScreen`
  - If true → skip to home or language selection
- [ ] `OnboardingScreen` `onComplete` callback must:
  - Set `onboarding_complete = true` in SharedPreferences
  - Navigate to `LanguageSelectionScreen`
- [ ] `LanguageSelectionScreen` `onComplete` callback must:
  - Save selected language via `languageProvider`
  - Save to SharedPreferences: `selected_language`
  - Navigate to home (if profile exists) or profile setup
- [ ] Make sure asset paths in `onboarding_screen.dart` match your actual
  files in `app/assets/images/`:
  ```dart
  const _kSlide1Asset = 'assets/images/onboarding_slide_1.png';
  ```
  Update these to your exact filenames.

---

### 2.2 Pregnancy Profile Setup `[FE]` 🟡

If no profile exists (first run after onboarding), the user must enter their LMP.

- [ ] Create `lib/screens/profile_setup_screen.dart` if not already built
- [ ] Fields: patient name (optional), Last Menstrual Period date (date picker),
  language (pre-filled from previous step)
- [ ] On save: compute and store `PregnancyProfile` with:
  - LMP date
  - Due date (LMP + 280 days)
  - Current gestational week
  - Trimester
- [ ] Save via `StorageService` (already exists)
- [ ] Navigate to `HomeScreen` after save
- [ ] In `HomeScreen`: if no profile found, redirect to profile setup

---

### 2.3 ANC + Vaccine Schedule — Make Events Tappable `[FE]` 🟡

The `PregnancyJourneyGraph` and `ProgressTrackerCard` exist. Make them
interactive so judges can engage with them.

- [ ] Each event on `PregnancyJourneyGraph` (ANC contact, vaccine) must be
  tappable and show a bottom sheet with:
  - Event name (e.g., "ANC Contact 4")
  - Scheduled date
  - What happens at this visit
  - "Mark as completed" button
  - Status chip: Done / Upcoming / Missed (in semantic colors)
- [ ] `ProgressTrackerCard` must show:
  - Current week (e.g., "Week 28")
  - Trimester label
  - Due date formatted: "Due: 14 Oct 2026"
  - Next event countdown: "Next: ANC 5 in 12 days"
  - Missed events count with red indicator if any
- [ ] Completed events must persist via `StorageService` and show on the
  graph as visually distinct (filled vs outlined)

---

### 2.4 Danger Signs Education Screen `[FE]` 🟡

A simple but judge-visible screen. Linked from home and risk result.

- [ ] Create `lib/screens/danger_signs_screen.dart`
- [ ] 6 expandable tiles with icons and local language text:
  - Severe headache
  - Swollen face or hands
  - Blurred vision or seeing spots
  - Heavy vaginal bleeding
  - High fever
  - Baby not moving
- [ ] Each tile expands to a 2-sentence explanation in the current language
- [ ] Red warning banner at top: go to health centre if any of these present
- [ ] FAB: "Speak your symptoms" → voice triage
- [ ] Link to this screen from: home bottom nav (Education tab) +
  risk result "Learn more" button

---

### 2.5 CHW Notification — Backend Must Send SMS `[BE]` 🟡

After a HIGH risk result, the backend should notify the linked CHW.
This is a visible, impressive feature for judges.

- [ ] Add Termii API key to `.env`:
  ```
  TERMII_API_KEY=your_termii_key_here
  TERMII_SENDER_ID=EasyBirth
  ```
- [ ] In the risk assessment service, after concluding HIGH risk:
  ```python
  async def notify_chw(chw_phone: str, patient_name: str, symptoms: list[str], week: int):
      async with httpx.AsyncClient() as client:
          await client.post("https://api.ng.termii.com/api/sms/send", json={
              "to": chw_phone,
              "from": "EasyBirth",
              "sms": f"URGENT — EasyBirth Alert\nPatient: {patient_name}\nWeek {week}\nSymptoms: {', '.join(symptoms[:3])}\nAdvised to go to PHC immediately.",
              "type": "plain",
              "channel": "generic",
              "api_key": settings.TERMII_API_KEY,
          })
  ```
- [ ] Add `chw_phone` as an optional field in `TriageRequest`
- [ ] In Flutter: let user enter CHW phone in profile setup (optional field)
  Store in `StorageService`, pass in every triage request
- [ ] Show "CHW notified ✓" banner on risk result screen when HIGH risk

---

### 2.6 Offline Mode — Show Status Clearly `[FE]` 🟡

Judges care about offline. Show it visibly, don't just let it silently fail.

- [ ] Add `connectivity_plus` to `pubspec.yaml`
- [ ] Create `lib/providers/connectivity_provider.dart`
  ```dart
  final connectivityProvider = StreamProvider<ConnectivityResult>((ref) {
    return Connectivity().onConnectivityChanged;
  });
  ```
- [ ] Create `lib/widgets/status_chip.dart` — a small chip shown in AppBar:
  - Online: `● Online` green dot
  - Offline: `● Offline — AI works locally` green dot (reassuring, not alarming)
- [ ] When offline and user runs triage:
  - Show message: "No internet — using on-device AI (less detailed)"
  - Use simple rule-based fallback in Flutter instead of API call:
    ```dart
    // Offline fallback: check for danger sign keywords in transcript
    // If found → HIGH RISK, else → MODERATE with "see CHW" advice
    ```
  - Queue the session to sync when back online (Hive box `pending_sessions`)
- [ ] When connectivity restores: flush `pending_sessions` queue to backend

---

## PHASE 3 — Demo Day Polish (do this third)

Goal: The demo looks and feels production-ready for judges and exhibition.

---

### 3.1 Demo Mode — Seed Scenarios `[FE]` 🟡

For the exhibition, you cannot rely on real microphone input working
perfectly in a noisy venue. Build a demo mode.

- [ ] Create `lib/screens/demo_mode_screen.dart`
- [ ] 3 pre-built scenarios (no mic needed):
  ```dart
  final demoScenarios = [
    DemoScenario(
      name: "Amina",
      language: AppLanguage.hausa,
      transcript: "Ina jin ciwon kai sosai, tafin hannuna yana kumbura",
      expectedRisk: RiskLevel.high,
      avatar: "A",
      description: "Pre-eclampsia warning signs — Week 32",
    ),
    DemoScenario(
      name: "Fatima",
      language: AppLanguage.yoruba,
      transcript: "Mo ni irora diẹ ninu ikun, mo ti jẹ daradara",
      expectedRisk: RiskLevel.low,
      avatar: "F",
      description: "Normal third trimester check — Week 28",
    ),
    DemoScenario(
      name: "Ngozi",
      language: AppLanguage.igbo,
      transcript: "Anya m adịghị ọcha, ọ bụ ihe atọ n'izu",
      expectedRisk: RiskLevel.moderate,
      avatar: "N",
      description: "Visual disturbance, monitoring needed — Week 36",
    ),
  ];
  ```
- [ ] Tapping "Run Demo" skips mic entirely — sends pre-written transcript
  to backend and plays through full triage flow with real API response
- [ ] Access demo mode: 5-tap easter egg on the app logo on home screen
  (discrete — not visible in normal use)
- [ ] Demo mode screen has dark green background to visually distinguish
  it from the real app

---

### 3.2 Impact Stats Screen `[FE]` 🟢

For the exhibition stand. Shows potential scale of impact.

- [ ] Create `lib/screens/impact_stats_screen.dart`
- [ ] Animated roll-up counters (use `AnimationController` with `Tween<int>`):
  - 247 women screened
  - 34 high-risk flags raised
  - 891 ANC reminders sent
- [ ] "100% on-device · Zero cloud costs · Zero data uploaded" chips
- [ ] SDG 3 (Good Health) + SDG 10 (Reduced Inequalities) badge row
- [ ] Dark background `#0D1F17` for dramatic exhibition feel
- [ ] Access from: settings or demo mode screen

---

### 3.3 Visual Polish Pass `[FE]` 🟢

30 minutes of polish before the demo makes a big difference to judges.

- [ ] Ensure every screen uses `#F2EDE8` as background (not white)
- [ ] Every `FilledButton` uses `#1B6B4A` and `borderRadius: 16`
- [ ] All chip text is Nunito SemiBold
- [ ] All headlines are Plus Jakarta Sans Bold or SemiBold
- [ ] No placeholder text visible anywhere (no "TODO", "Lorem ipsum", "Test")
- [ ] App name consistently "EasyBirth" or "AmaraAI" — pick one and commit
- [ ] App icon set (run `flutter_launcher_icons` — add to `pubspec.yaml`)
- [ ] Splash screen matches brand colors (not default white Flutter splash)
- [ ] Loading states everywhere — no screen that just hangs blank
- [ ] All error states handled: API down, mic permission denied, no profile

---

### 3.4 Backend — Stability for Demo Day `[BE]` 🟡

The backend must not crash during the demo. Basic hardening:

- [ ] All endpoints wrapped in try/except with proper HTTP error responses
  ```python
  @router.post("/assess")
  async def assess(request: TriageRequest):
      try:
          return await risk_service.assess(request)
      except anthropic.APIError as e:
          raise HTTPException(status_code=503, detail="AI service unavailable")
      except Exception as e:
          logger.error(f"Triage error: {e}")
          raise HTTPException(status_code=500, detail="Internal error")
  ```
- [ ] Add response time logging — if Claude takes > 8 seconds, the Flutter
  app will timeout. Test response times under load.
- [ ] Rate limit: 10 requests/minute per IP (use `slowapi` package)
- [ ] Deploy to Railway before demo day — do NOT demo off localhost
  - Run: `railway up` from backend directory
  - Update Flutter `AppConfig.apiBaseUrl` to Railway URL
  - Test live URL from a real Android device (not emulator) the day before
- [ ] Set `ENVIRONMENT=production` in Railway environment variables
- [ ] Health check: Railway has a health check URL, point it to `/health`

---

### 3.5 End-to-End Test Checklist `[BOTH]` 🔴

Run this checklist the day before the demo on a real Android device:

```
ONBOARDING
[ ] Fresh install — onboarding appears correctly
[ ] All 3 slides scroll, page indicator animates
[ ] Language selection saves and persists after app restart

HOME SCREEN
[ ] Correct gestational week shown
[ ] Progress tracker card renders with correct data
[ ] Journey graph shows ANC events on correct dates
[ ] Voice orb is visible and pulsing
[ ] Suggestion chips show text in selected language

VOICE TRIAGE
[ ] Tapping orb opens listening screen
[ ] Mic activates (check mic permission requested on first use)
[ ] Transcript appears as user speaks
[ ] Tapping "Done" sends to backend
[ ] Processing screen shows while backend responds (not blank)
[ ] If online: Claude responds within 8 seconds
[ ] If offline: offline fallback message appears

RISK RESULT
[ ] High risk shows red pill
[ ] Moderate shows amber
[ ] Low shows green
[ ] Recommendation text visible in correct language
[ ] TTS speaks recommendation aloud (check device volume)
[ ] "Find Health Centre" button works
[ ] If CHW phone set: "CHW notified" banner appears

DEMO MODE
[ ] 5-tap easter egg opens demo mode
[ ] All 3 scenarios run end-to-end without mic
[ ] Each produces the expected risk level

OFFLINE MODE
[ ] Disable WiFi — status chip updates
[ ] Triage still works (offline fallback)
[ ] Re-enable WiFi — status updates back
```

---

## PHASE 4 — COUCH Submission Materials

Due at Phase 01 submission. These are non-negotiable for the application.

---

### 4.1 Pitch Deck `[Ez]` 🔴

10–12 slides. Judges read fast — every slide must have one clear point.

- [ ] **Slide 1 — Cover:** App name, tagline, team name, COUCH 2026
- [ ] **Slide 2 — The Problem (with numbers):**
  - Nigeria = 28% of global maternal deaths (~75,000 per year)
  - Doctor ratio: 3.9 per 10,000 (far below WHO minimum)
  - 85% of facilities are underfunded PHCs
  - Low literacy, English-dominant tools exclude rural women
- [ ] **Slide 3 — The Three Delays:**
  Show the WHO three-delays model as a simple diagram. EasyBirth addresses
  all three: Delay 1 (not knowing when to seek care), Delay 2 (deciding
  to seek care), Delay 3 (reaching care).
- [ ] **Slide 4 — Our Solution:**
  One sentence: "EasyBirth is an offline-first, voice-based maternal
  health AI that triages symptoms in Hausa, Yoruba, Igbo, and Pidgin —
  no internet, no literacy required."
  Show the 3 onboarding slide screenshots side by side.
- [ ] **Slide 5 — How It Works:**
  Simple 4-step flow diagram: Speak → AI Investigates → Risk Decision → Action
  Include the multi-turn agent conversation as a screenshot or mockup.
- [ ] **Slide 6 — AI / Technology:**
  - On-device TFLite risk classifier (no internet needed)
  - Agentic ReAct loop via Anthropic Claude Haiku
  - Hybrid: on-device when offline, cloud-enhanced when connected
  - 4 Nigerian languages with keyword maps + semantic matching
  This is 25% of your score — make it detailed.
- [ ] **Slide 7 — Demo Screenshot / GIF:**
  The most important slide after the problem. Show the orb, a conversation,
  a risk result. Real screenshots from your app.
- [ ] **Slide 8 — Impact:**
  - Reduces Delay 1: Danger sign education in local language
  - Reduces Delay 2: Clear HIGH/MODERATE/LOW → immediate action
  - Reduces Delay 3: PHC finder + CHW notification
  - Target: rural LGAs with MMR > 800 per 100,000
- [ ] **Slide 9 — Equity & Inclusion:**
  - No internet required
  - No literacy required (voice-first)
  - 4 Nigerian languages
  - Works on sub-$50 Android devices
  This is 10% of your score.
- [ ] **Slide 10 — Commercial Viability:**
  - B2G: State Ministry of Health licensing per LGA
  - B2B: NGO/INGO white-label (MSF, CARE, UNFPA)
  - Grant pathway: NHSRII, Gates Foundation, USAID
  - CHW supervision SaaS: ₦500/CHW/month
- [ ] **Slide 11 — The Team:**
  Photos, names, roles. Be honest — judges appreciate a small focused team.
- [ ] **Slide 12 — Ask / Next Steps:**
  "We are applying for COUCH incubation to deploy a pilot in [LGA name].
  We need: mentorship, medical validation partnership, and 3-month runway."

---

### 4.2 Pitch Video `[Ez]` 🔴

Maximum 3 minutes. Structure:

```
0:00 – 0:20  Hook — open with a statistic or a real woman's story
0:20 – 0:50  The problem — maternal mortality in rural Nigeria
0:50 – 1:40  Demo — screen recording of the app in action
             Show: orb → speak in Hausa → agent asks follow-up
             → HIGH RISK result → CHW notified
1:40 – 2:10  The tech — briefly explain AI + offline architecture
2:10 – 2:40  Impact + equity — who benefits, how it scales
2:40 – 3:00  Team + ask — who you are, what you're asking COUCH for
```

Recording tips:
- Use Android screen recorder (built-in) for the demo portion
- Record voice-over separately and sync in editing
- Subtitles for the Hausa/Yoruba/Igbo/Pidgin speech in demo
- Tools: CapCut, DaVinci Resolve (free), or Canva Video

---

### 4.3 Business Model Canvas `[Ez]` 🔴

One-page. Use the Strategyzer template format. Fill these 9 blocks:

```
Customer Segments:
  Primary: Pregnant women in rural Nigeria (especially North, SE)
  Secondary: Community Health Workers (CHWs) and midwives
  Tertiary: State Ministries of Health, NGOs

Value Propositions:
  For women: Know when to go to the clinic — in your own language
  For CHWs: Dashboard + automatic alerts for high-risk patients
  For government: Scalable triage that extends limited health workforce

Channels:
  CHW distribution: train CHWs to install and enrol patients
  NGO partnerships: MSF, CARE, UNFPA field deployment
  NHIS/NHSRII integration: government procurement

Customer Relationships:
  CHW-mediated onboarding for low-literacy users
  Automated ANC reminders (no human needed after setup)
  CHW supervision dashboard for ongoing engagement

Revenue Streams:
  Government licensing: per-LGA annual subscription
  NGO white-label: per-deployment contract
  CHW SaaS: ₦500 per CHW per month
  Research data licensing: anonymised aggregate to LSHTM, JHSPH

Key Resources:
  AI models (on-device TFLite + Anthropic API)
  Language keyword maps (4 Nigerian languages)
  CHW network relationships
  Medical validation partnerships

Key Activities:
  Model training and accuracy improvement
  CHW training and onboarding
  Language model expansion (more dialects, more African languages)
  Regulatory engagement (NDH, NAFDAC for digital health tools)

Key Partnerships:
  Nigeria Ministry of Health / State MOH (deployment)
  NHSRII / MAMII (alignment + co-funding)
  Nigerian medical schools (validation + clinical audit)
  Termii (SMS infrastructure)
  Anthropic (AI API)

Cost Structure:
  Anthropic API usage (online tier)
  Railway hosting
  Termii SMS
  CHW training content creation
  Clinical validation studies
```

---

## Quick Priority Summary

```
THIS WEEK — must complete to have a demo that works:

Day 1:  1.1 Wire frontend to backend (health check working)
        1.2 Risk assessment endpoint returns real Claude response

Day 2:  1.3 Complete voice triage loop (listen → process → result)
        1.4 Orb widget unified across all screens

Day 3:  1.5 Language state global
        2.1 Onboarding wired into nav flow
        2.2 Profile setup screen working

Day 4:  2.3 Journey graph events tappable
        2.5 CHW SMS notification (Termii)
        2.6 Offline mode visible

Day 5:  3.1 Demo mode with seed scenarios
        3.4 Deploy backend to Railway
        3.5 Full end-to-end test on real device

Day 6+: 3.2 Impact stats screen
        3.3 Visual polish pass
        4.1 Pitch deck
        4.2 Pitch video recording
        4.3 Business Model Canvas
```

---

## Files to Create (not yet in repo)

```
app/lib/
├── providers/
│   ├── language_provider.dart        ← global language state
│   └── connectivity_provider.dart    ← offline/online stream
├── services/
│   └── api_service.dart              ← Dio wrapper for all API calls
├── screens/
│   ├── processing_screen.dart        ← orb processing state
│   ├── risk_result_screen.dart       ← triage conclusion + actions
│   ├── danger_signs_screen.dart      ← 6 expandable danger signs
│   ├── demo_mode_screen.dart         ← seed scenarios for exhibition
│   └── impact_stats_screen.dart      ← roll-up counters for exhibition
└── widgets/
    ├── the_orb.dart                  ← unified 4-state orb widget
    ├── risk_badge.dart               ← HIGH / MODERATE / LOW chip
    └── status_chip.dart              ← offline/online AppBar chip
```

---

*EasyBirth · COUCH 2026 · Built for rural Nigeria*
