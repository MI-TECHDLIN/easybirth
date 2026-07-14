# AmaraAI — Pregnancy Vaccine &amp; Progress Tracker
## Flutter Developer Specification Document

**Project:** AmaraAI — Offline-first maternal health voice assistant
**Target:** Rural Nigeria — Hausa, Yoruba, Igbo, Nigerian Pidgin
**Your role:** Flutter frontend developer
**Backend:** Python ML/API developer (see `AMARAAI_ML_BACKEND.md`) — separate person
**Hackathon:** COUCH 2026 — Healthcare Track

---

## 1. What You Are Building

Two linked widgets that live on the patient's home screen:

1. **Pregnancy Journey Graph** — a contribution-graph-style calendar (same
   visual idea as a GitHub contributions grid) that spans the full 40-week
   pregnancy. Every day is one cell. Cells light up when that day carries a
   scheduled ANC contact or vaccine dose, and change colour once it's
   completed, due soon, or missed.
2. **Progress Tracker** — a compact card (ring + bar) showing where the
   patient is right now: current week out of 40, trimester, estimated due
   date, and a one-line summary of what's outstanding.

Both are driven by a single source of truth: the patient's **last menstrual
period (LMP)** date, which is used to derive every gestational week/day and
therefore every vaccine and ANC due-date in the app. No cell is ever
hand-scheduled — it's all computed from LMP + the fixed schedule below.

A static mockup of both widgets is attached (`pregnancy_tracker_mockup.html`)
— open it in a browser to see the interaction (tap a highlighted cell to see
what's linked to that day).

---

## 2. The Medical Schedule This Widget Encodes

This is the fixed reference data. Hard-code it once as a constant table (see
§4) — do not let it drift, since it drives every reminder and every cell
colour in the app.

### 2.1 ANC contacts — WHO 8-contact model

The 2016 WHO model replaces the old 4-visit schedule with a minimum of eight
antenatal contacts, timed as follows:

| Contact # | Gestational week | Trimester |
|---|---|---|
| 1 | 12 | 1st |
| 2 | 20 | 2nd |
| 3 | 26 | 2nd |
| 4 | 30 | 3rd |
| 5 | 34 | 3rd |
| 6 | 36 | 3rd |
| 7 | 38 | 3rd |
| 8 | 40 | 3rd |

This maps directly onto the existing `anc_visits` table in the Python
backend (`visit_number 1–8`), so keep the numbering identical — it's what
gets synced via `POST /api/sync/patient`.

### 2.2 Tetanus toxoid (TT) vaccine doses

Tetanus toxoid is the vaccine routinely given during pregnancy in Nigeria to
prevent maternal and neonatal tetanus. For a patient in her **current**
pregnancy the app needs to schedule:

| Dose | Timing | Notes |
|---|---|---|
| TT1 | At first ANC contact (week 12), or as soon as pregnancy is confirmed if later | Given regardless of prior doses |
| TT2 | 4 weeks after TT1 (week 16) | Two doses (TT1+TT2) already give meaningful protection for a first pregnancy |
| TT3 | 6 months after TT2, or in a subsequent pregnancy | 5 years' protection — model as a booster, not mandatory in-app for a single pregnancy |
| TT4 | 1 year after TT3, or in a subsequent pregnancy | 10 years' protection |
| TT5 | 1 year after TT4, or in a subsequent pregnancy | Lifelong protection |

For the hackathon build, schedule **TT1 and TT2 automatically** for every
pregnancy. Treat TT3–TT5 as boosters tied to obstetric history rather than
to this pregnancy's calendar — flag them as a `future enhancement` once the
patient record supports multi-pregnancy history (it doesn't yet — the
current `patients` table only has `parity`, not a per-dose vaccination
history).

### 2.3 Extensibility

Keep the schedule as data, not logic, so a CHW-configurable vaccine (e.g.
influenza, which some programmes recommend in pregnancy) can be added later
without touching the widget code — see the `VaccineScheduleEntry` model in
§4.

---

## 3. Where This Fits the Existing Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Flutter App                           │
│                                                          │
│  PregnancyProfile (LMP-derived)                          │
│        │                                                 │
│        ├── generates ──> 280 PregnancyDay cells           │
│        │                  (Pregnancy Journey Graph)       │
│        │                                                 │
│        └── generates ──> ProgressSnapshot                 │
│                           (Progress Tracker card)          │
│                                                          │
│  Stored offline-first in Hive; synced opportunistically   │
│  to the same `anc_visits` table + a new `vaccine_doses`   │
│  table on the Python backend via /api/sync/patient        │
└─────────────────────────────────────────────────────────┘
```

**Backend coordination needed:** the Python dev's schema currently has
`anc_visits` but no vaccine table. Ask them to add:

```sql
CREATE TABLE vaccine_doses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id),
    dose_code VARCHAR(10),        -- 'TT1', 'TT2', ...
    scheduled_date DATE,
    administered_date DATE,
    status VARCHAR(20)            -- upcoming | due_soon | completed | missed
);
```

and extend the `/api/sync/patient` body to `{ patient, sessions, anc_visits,
vaccine_doses }`. Until that lands, keep vaccine doses Hive-only.

---

## 4. Data Model (Dart)

```dart
// lib/models/pregnancy_profile.dart

class PregnancyProfile {
  final String patientId;
  final DateTime lastMenstrualPeriod; // LMP — the single source of truth
  const PregnancyProfile({required this.patientId, required this.lastMenstrualPeriod});

  DateTime get estimatedDueDate => lastMenstrualPeriod.add(const Duration(days: 280));

  int get currentGestationalDay =>
      DateTime.now().difference(lastMenstrualPeriod).inDays.clamp(0, 280);

  int get currentGestationalWeek => (currentGestationalDay / 7).floor() + 1;

  int get daysRemaining => 280 - currentGestationalDay;

  String get trimester {
    if (currentGestationalWeek <= 12) return '1st trimester';
    if (currentGestationalWeek <= 26) return '2nd trimester';
    return '3rd trimester';
  }
}
```

```dart
// lib/models/vaccine_schedule.dart

enum DoseType { anc, vaccine }
enum DoseStatus { upcoming, dueSoon, completed, missed }

class ScheduleEntry {
  final String code;          // 'anc_1'..'anc_8', 'tt1', 'tt2'
  final DoseType type;
  final int scheduledWeek;
  final int scheduledDayOfWeek; // 1–7, default 1 (Monday of that week)
  final String label;         // display text, e.g. "ANC contact 3/8"
  DateTime? completedDate;
  DoseStatus status;

  ScheduleEntry({
    required this.code,
    required this.type,
    required this.scheduledWeek,
    this.scheduledDayOfWeek = 1,
    required this.label,
    this.completedDate,
    this.status = DoseStatus.upcoming,
  });
}

/// The fixed reference schedule from §2 — do not derive this per-patient,
/// only the dates change (via PregnancyProfile.lastMenstrualPeriod).
final List<ScheduleEntry> defaultSchedule = [
  ScheduleEntry(code: 'anc_1', type: DoseType.anc, scheduledWeek: 12, label: 'ANC contact 1/8'),
  ScheduleEntry(code: 'tt1',   type: DoseType.vaccine, scheduledWeek: 12, scheduledDayOfWeek: 3, label: 'TT1 – Tetanus Toxoid'),
  ScheduleEntry(code: 'tt2',   type: DoseType.vaccine, scheduledWeek: 16, scheduledDayOfWeek: 3, label: 'TT2 – Tetanus Toxoid'),
  ScheduleEntry(code: 'anc_2', type: DoseType.anc, scheduledWeek: 20, label: 'ANC contact 2/8'),
  ScheduleEntry(code: 'anc_3', type: DoseType.anc, scheduledWeek: 26, label: 'ANC contact 3/8'),
  ScheduleEntry(code: 'anc_4', type: DoseType.anc, scheduledWeek: 30, label: 'ANC contact 4/8'),
  ScheduleEntry(code: 'anc_5', type: DoseType.anc, scheduledWeek: 34, label: 'ANC contact 5/8'),
  ScheduleEntry(code: 'anc_6', type: DoseType.anc, scheduledWeek: 36, label: 'ANC contact 6/8'),
  ScheduleEntry(code: 'anc_7', type: DoseType.anc, scheduledWeek: 38, label: 'ANC contact 7/8'),
  ScheduleEntry(code: 'anc_8', type: DoseType.anc, scheduledWeek: 40, label: 'ANC contact 8/8'),
];
```

```dart
// lib/models/pregnancy_day.dart

class PregnancyDay {
  final int dayIndex;     // 1–280
  final int week;         // 1–40
  final int dayOfWeek;    // 1 (Mon) – 7 (Sun)
  final DateTime calendarDate;
  final List<ScheduleEntry> events; // usually empty, 1 for most, could be 2
  DoseStatus get cellStatus =>
      events.isEmpty ? DoseStatus.upcoming /* unused visually */ : events.first.status;
}

/// Builds all 280 days for a profile, attaching any matching schedule entries.
List<PregnancyDay> buildPregnancyCalendar(PregnancyProfile profile, List<ScheduleEntry> schedule) {
  return List.generate(280, (i) {
    final dayIndex = i + 1;
    final week = (i ~/ 7) + 1;
    final dayOfWeek = (i % 7) + 1;
    final date = profile.lastMenstrualPeriod.add(Duration(days: i));
    final events = schedule
        .where((e) => e.scheduledWeek == week && e.scheduledDayOfWeek == dayOfWeek)
        .toList();
    return PregnancyDay(
      dayIndex: dayIndex, week: week, dayOfWeek: dayOfWeek,
      calendarDate: date, events: events,
    );
  });
}
```

Persist `PregnancyProfile` and the `ScheduleEntry` completion states in Hive
(`pregnancy_box`), keyed by `patientId` — this is what makes the whole thing
work fully offline, consistent with the rest of the app.

---

## 5. Widget 1 — Pregnancy Journey Graph

**Visual model:** 40 columns (weeks) × 7 rows (days), same grid logic as a
GitHub contribution graph, grouped into three column-bands labelled
"1st trimester / 2nd trimester / 3rd trimester" instead of months.

**Cell states &amp; colours:**

| State | Meaning | Colour |
|---|---|---|
| Empty | No ANC contact or vaccine due that day | Neutral dark grey |
| Upcoming / due soon | Scheduled, not yet due, or due within 7 days | Amber outline |
| Completed | Marked done by the CHW or patient | Solid teal/green |
| Missed | Scheduled date has passed with no completion logged | Red/terracotta |
| Today | Ring/outline marker, independent of the above | Indigo outline |

**Behaviour:**
- Only cells with a `ScheduleEntry` are tappable; tapping opens a detail
  sheet (`ScheduleEntryDetailSheet`) showing the linked vaccine or ANC
  contact, its due date, and a "Mark as completed" action for CHWs.
- The grid auto-scrolls horizontally to the patient's current week on open.
- Build with `GridView.builder` (280 cells renders fine; no need for
  `CustomPainter` unless you see jank on very low-end devices, in which case
  fall back to a painted canvas — same data model either way).
- Recommended package: plain `GridView` + `Table` for the day/trimester
  labels is enough; `table_calendar` is unnecessary here since this isn't a
  month calendar.

---

## 6. Widget 2 — Progress Tracker Card

A small always-visible card, not a scrollable grid:

- **Ring or bar** showing `currentGestationalWeek / 40`.
- **Trimester chip** (`profile.trimester`).
- **Due date line**: "Estimated due date `estimatedDueDate` · `daysRemaining`
  days to go."
- **Status line**: count of upcoming/missed items, e.g. "1 vaccine dose
  upcoming · 1 ANC contact missed" — pull this by filtering `defaultSchedule`
  for `status != completed`.

This card is also the natural candidate for an Android/iOS **home-screen
widget** later (via `home_widget` package) since it's a single glanceable
snapshot rather than an interactive grid — flag that as a nice-to-have,
not required for the hackathon build.

---

## 7. Reminders (offline-safe)

Schedule local notifications (`flutter_local_notifications`) for every
`ScheduleEntry`, fired a few days before `scheduledWeek`'s calendar date and
again on the day itself. This must work fully offline — do not depend on
the FastAPI server for reminders; only use `chw_notifier`/SMS (server-side,
already in the Python spec) as the CHW-facing channel when online.

---

## 8. Build Order

```
Day 1 — Data layer
  - PregnancyProfile, ScheduleEntry, PregnancyDay models
  - buildPregnancyCalendar() + unit tests against known LMP dates
  - Hive box wired up

Day 2 — Progress Tracker card
  - Ring/bar UI, trimester chip, due-date + outstanding-items line

Day 3 — Pregnancy Journey Graph
  - GridView of 280 cells, trimester bands, day labels
  - Tap → detail sheet, "mark completed" action

Day 4 — Reminders + sync
  - Local notifications for upcoming entries
  - Hive → /api/sync/patient once vaccine_doses table exists

Day 5 — Integration test with backend dev
  - Confirm anc_visits numbering matches, confirm sync payload shape
```

---

## 9. Handoff Checklist

- [ ] `PregnancyProfile` computed correctly from LMP (unit-tested against a
      few known dates, including due-date arithmetic across month boundaries)
- [ ] All 10 default schedule entries render on the correct week/day
- [ ] Cell colour states match §5 table exactly (this is what a CHW will
      scan at a glance — don't get the states wrong)
- [ ] Grid opens auto-scrolled to current week
- [ ] Progress tracker's outstanding-items count matches the grid's missed/
      upcoming cells
- [ ] Everything above works with the device in airplane mode
- [ ] Backend dev has been asked about `vaccine_doses` table + sync payload

---

*AmaraAI Flutter Frontend — Built for COUCH 2026 Healthcare Track*
