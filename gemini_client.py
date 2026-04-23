"""
VerdictAI X Gemini API Wrapper
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def _get_client() -> genai.Client:
    """Returns a configured Gemini Client instance."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError(
            "GEMINI_API_KEY not set. Copy .env.example to .env and add your key."
        )
    return genai.Client(api_key=api_key)


def _flash_model() -> str:
    return os.getenv("GEMINI_FLASH_MODEL", "gemini-2.5-flash")


def _pro_model() -> str:
    return os.getenv("GEMINI_PRO_MODEL", "gemini-2.5-pro")


# Fallback models (Unlimited Tier) for when primary limits are reached
FALLBACK_MODELS = [
    "gemini-3.1-flash-lite-preview",
    "gemini-2.5-flash",
    "gemma-4-31b-it", 
    "gemma-4-26b-a4b-it"
]


def _get_model_queue(use_pro: bool) -> list:
    """Returns a list of models to try in order."""
    primary = _pro_model() if use_pro else _flash_model()
    return [primary] + FALLBACK_MODELS


def _build_config_and_prompt(model: str, prompt: str, system_prompt: str):
    """Encapsulates model-specific prompt/config logic."""
    if "gemma" in model.lower():
        if system_prompt:
            final_prompt = f"System Instructions: {system_prompt}\n\nTask: {prompt}"
        else:
            final_prompt = prompt
        config = types.GenerateContentConfig()
    else:
        final_prompt = prompt
        config = types.GenerateContentConfig(
            system_instruction=system_prompt if system_prompt else None,
        )
    return config, final_prompt


def generate(prompt: str, system_prompt: str = "", use_pro: bool = False) -> str:
    """
    Generates a response with automatic failover.
    """
    client = _get_client()
    models_to_try = _get_model_queue(use_pro)
    
    last_error = ""
    for model in models_to_try:
        config, final_prompt = _build_config_and_prompt(model, prompt, system_prompt)
        try:
            response = client.models.generate_content(
                model=model,
                contents=final_prompt,
                config=config,
            )
            return response.text.strip()
        except Exception as e:
            last_error = str(e)
            if "429" in last_error or "RESOURCE_EXHAUSTED" in last_error or "not found" in last_error.lower() or "internal" in last_error.lower():
                continue 
            break 
            
    return f"[ERROR] The AI engine encountered an issue. Please try again."


def generate_stream(prompt: str, system_prompt: str = "", use_pro: bool = False):
    """
    Streams a response with automatic failover to Unlimited models.
    """
    client = _get_client()
    models_to_try = _get_model_queue(use_pro)
    
    for i, model in enumerate(models_to_try):
        config, final_prompt = _build_config_and_prompt(model, prompt, system_prompt)
        try:
            if i > 0:
                yield f"<br><span style='color:#fbbf24; font-size:10px;'>[System: Primary limit reached. Switching to {model}...]</span><br>"
                
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=final_prompt,
                config=config,
            ):
                if chunk.text:
                    yield chunk.text
            return 
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                if i < len(models_to_try) - 1:
                    continue 
                yield f"<span style='color:#f43f5e; font-weight:600;'>System overloaded. All backup models are currently busy. Please try again in a few minutes.</span>"
            elif "404" in error_msg or "not found" in error_msg.lower():
                if i < len(models_to_try) - 1:
                    continue 
                yield f"<span style='color:#f43f5e;'>The selected AI model is offline or unavailable. Switching to backups failed. Please try again later.</span>"
            elif "500" in error_msg or "internal" in error_msg.lower() or "503" in error_msg:
                if i < len(models_to_try) - 1:
                    continue 
                yield f"<span style='color:#f43f5e;'>Google's AI service is currently experiencing internal maintenance. Please try again soon.</span>"
            else:
                yield f"<span style='color:#f43f5e;'>An unexpected connection issue occurred. Please retry your request.</span>"
            break 
