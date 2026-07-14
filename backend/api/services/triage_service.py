"""AI triage service for the EasyBirth backend."""
from __future__ import annotations

from api.schemas.triage import TriageRequest, TriageResponse


class TriageService:
    def assess(self, payload: TriageRequest) -> TriageResponse:
        # TODO: replace this stub with an Anthropic Claude API call.
        # The current behavior is a stable placeholder for demo wiring.
        transcript = payload.transcript.lower()
        high_risk_keywords = [
            'ciwon kai',
            'kumbura',
            'dukkan',
            'jini',
            'zafi mai zafi',
            'idanuna',
            'babban ciwo',
        ]

        detected = [
            keyword for keyword in high_risk_keywords if keyword in transcript
        ]

        if detected:
            return TriageResponse(
                decision='conclude',
                follow_up_question=None,
                risk_level='HIGH',
                detected_symptoms=['Severe headache', 'Swollen hands', 'Blurred vision'],
                recommendation='Please go to the nearest health centre immediately.',
                reasoning='The symptoms indicate possible pre-eclampsia or another urgent maternal emergency.',
            )

        return TriageResponse(
            decision='conclude',
            follow_up_question=None,
            risk_level='LOW',
            detected_symptoms=['No danger signs detected'],
            recommendation='Keep your next ANC appointment and rest well.',
            reasoning='No red-flag symptoms were identified in the reported transcript.',
        )
