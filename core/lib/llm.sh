#!/bin/bash
# =============================================================================
# LLM Utilities
# =============================================================================

# Call LLM to generate iteration summary points
# Usage: call_llm_iteration_summary <iteration> <spec_name> [model] [timeout]
call_llm_iteration_summary() {
    local iteration="$1"
    local spec_name="$2"
    local model="${3:-anthropic/claude-3.5-sonnet}"
    local timeout="${4:-60}"

    python3 -c "
import os
import sys
sys.path.insert(0, '../core')
from llm_client import call_llm_with_timeout_handling
api_key = os.getenv('OPENROUTER_API_KEY')
if api_key:
    model = '$model'
    prompt = '''

Du har just avslutat iteration $iteration av $spec_name.
Skriv 2-3 korta punkter om:
1. Vad implementerades
2. Eventuella gotchas eller patterns du upptäckte
3. Filer som ändrades

Svara ENDAST med punkterna, inget annat.'''
    messages = [{'role': 'user', 'content': prompt}]
    result = call_llm_with_timeout_handling(api_key, model, messages, timeout=$timeout)
    if result and 'choices' in result:
        print(result['choices'][0]['message']['content'])
"
}