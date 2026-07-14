"""AI triage service for the EasyBirth backend."""
from __future__ import annotations

import json
from typing import Any

import httpx

from api.core.config import settings
from api.schemas.triage import ConversationTurn, TriageRequest, TriageResponse
from api.services.triage_session_store import store as triage_session_store


class TriageService:
    def assess(self, payload: TriageRequest) -> TriageResponse:
        persisted_history = triage_session_store.get_history(payload.session_id)
        request_history = payload.conversation_history or persisted_history

        response = None
        if settings.anthropic_api_key:
            try:
                response = self._assess_with_anthropic(payload)
            except Exception as exc:
                print(f'Anthropic triage failed: {exc}')

        if response is None:
            response = self._keyword_fallback(payload)

        if response.decision == 'need_more_info' and response.follow_up_question:
            request_history = [
                *request_history,
                ConversationTurn(role='assistant', content=response.follow_up_question),
            ]

        triage_session_store.save_history(payload.session_id, request_history)
        return response

    def _assess_with_anthropic(self, payload: TriageRequest) -> TriageResponse:
        prompt = self._build_prompt(payload)
        request_body = {
            'model': settings.anthropic_model,
            'prompt': prompt,
            'max_tokens_to_sample': 512,
            'temperature': 0.2,
            'stop_sequences': ['\n\n'],
        }

        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                'https://api.anthropic.com/v1/complete',
                headers={
                    'x-api-key': settings.anthropic_api_key,
                    'Content-Type': 'application/json',
                },
                json=request_body,
            )
            response.raise_for_status()
            payload_json = response.json()

        completion = payload_json.get('completion')
        if not isinstance(completion, str):
            raise ValueError('Invalid completion format from Anthropic')

        parsed = self._parse_json_response(completion)
        if parsed is None:
            raise ValueError('Unable to parse Anthropic JSON response')

        return TriageResponse(**parsed)

    def _build_prompt(self, payload: TriageRequest) -> str:
        return (
            'You are a maternal health triage assistant for rural Nigeria. '
            'The user has spoken a symptom description in the target language. '
            'Analyze the transcript and respond ONLY with a JSON object containing the following keys: '
            'decision, follow_up_question, risk_level, detected_symptoms, recommendation, reasoning. '
            'Use "need_more_info" if you need exactly one follow-up question. Use "conclude" only when you have a final risk decision. '
            'The risk_level MUST be HIGH, MODERATE, or LOW. '
            'If there are no urgent danger signs, set follow_up_question to null. '
            'Keep the recommendation concise and appropriate for a pregnant woman. '
            'Provide the response in the same language as the transcript. '
            '\n\n'
            f'Conversation history: {json.dumps([turn.model_dump() for turn in payload.conversation_history])}\n'
            f'Transcript: {payload.transcript}\n'
            f'Language: {payload.language}\n'
            f'Gestational week: {payload.gestational_week}\n'
            f'Patient name: {payload.patient_name}\n'
        )

    def _parse_json_response(self, completion: str) -> dict[str, Any] | None:
        try:
            return json.loads(completion)
        except json.JSONDecodeError:
            start = completion.find('{')
            end = completion.rfind('}')
            if start != -1 and end != -1 and end > start:
                try:
                    return json.loads(completion[start:end + 1])
                except json.JSONDecodeError:
                    return None
            return None

    def _keyword_fallback(self, payload: TriageRequest) -> TriageResponse:
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
