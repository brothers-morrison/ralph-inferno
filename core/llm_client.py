r"""
/llm_client.py
LLM Client module for handling API interactions with OpenRouter.

This module contains functions for calling LLM APIs with proper timeout handling,
retry logic, and response validation.
"""

import re
import json
import time
import requests
import os
import click
from typing import List, Dict, Any, Optional

def is_llm_response_incomplete(response_text: str) -> bool:
    """
    Check if the LLM response appears to be incomplete/cut off.
    """
    if not response_text:
        return True

    # Check for incomplete JSON
    try:
        json.loads(response_text)
        return False  # Valid JSON
    except json.JSONDecodeError:
        pass

    # Check for common incomplete patterns
    incomplete_patterns = [
        r'}\s*$',  # Ends with closing brace but might be incomplete
        r',\s*$',  # Ends with comma
        r':\s*$',  # Ends with colon
        r'"\s*$',  # Ends with quote
        r'\[\s*$',  # Ends with opening bracket
        r'{\s*$',  # Ends with opening brace
    ]

    for pattern in incomplete_patterns:
        if re.search(pattern, response_text.strip()):
            return True

    # Check if response is very short (likely incomplete)
    if len(response_text.strip()) < 50:
        return True

    return False

def call_llm_with_timeout_handling(
    api_key: str,
    model: str,
    messages: List[Dict[str, str]],
    max_retries: int = 3,
    timeout: int = 120
) -> Optional[Dict[str, Any]]:
    """
    Call LLM API with timeout handling and retry logic for incomplete responses.
    """
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 4000,  # Limit response size to reduce timeout risk
    }

    for attempt in range(max_retries):
        try:
            print(f"LLM API call attempt {attempt + 1}/{max_retries}")

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()

            result = response.json()

            # Check if response is complete
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]

                if is_llm_response_incomplete(content):
                    print(f"Response appears incomplete on attempt {attempt + 1}, retrying...")
                    time.sleep(2)  # Brief pause before retry
                    continue

                return result

        except requests.exceptions.Timeout:
            print(f"LLM API call timed out on attempt {attempt + 1}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"LLM API call failed on attempt {attempt + 1}: {e}")
            continue

    print("All LLM API attempts failed or returned incomplete responses")
    return None


@click.command()
@click.option('--api-key', default=lambda: os.environ.get('OPENROUTER_API_KEY'), help='API key for OpenRouter (defaults to OPENROUTER_API_KEY env var)')
@click.argument('query', required=True)
@click.option('--model', default='anthropic/claude-3-haiku:beta', help='Model to use (default: best free coding model)')
@click.option('--timeout', default=120, type=int, help='Timeout in seconds (default: 120)')
def main(api_key, query, model, timeout):
    if not api_key:
        raise click.ClickException("API key is required. Set OPENROUTER_API_KEY environment variable or provide --api-key.")
    if not query.strip():
        raise click.ClickException("Query cannot be blank.")
    messages = [{"role": "user", "content": query}]
    result = call_llm_with_timeout_handling(api_key, model, messages, timeout=timeout)
    if result and "choices" in result and len(result["choices"]) > 0:
        click.echo(result["choices"][0]["message"]["content"])
    else:
        click.echo("Failed to get response from LLM.")


if __name__ == "__main__":
    main()