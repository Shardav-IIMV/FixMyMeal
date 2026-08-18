"""Gemini API integration for analyzing food quality complaints."""

import json
import base64
from typing import Optional
import streamlit as st
import google.generativeai as genai


def get_gemini_api_key() -> Optional[str]:
    """Get Gemini API key from Streamlit secrets or environment."""
    try:
        # First try Streamlit secrets (for Streamlit Cloud)
        api_key = st.secrets.get("GEMINI_API_KEY")
        if api_key:
            return api_key
    except (FileNotFoundError, AttributeError):
        pass
    
    # Fallback to environment variable (for local development)
    import os
    return os.getenv("GEMINI_API_KEY")


def validate_api_key() -> bool:
    """Validate that Gemini API key is available."""
    api_key = get_gemini_api_key()
    return api_key is not None


def analyze_complaint(complaint_text: str, meal: str, image_data: Optional[bytes] = None) -> dict:
    """
    Analyze a student complaint using Gemini.
    
    Args:
        complaint_text: Student's written complaint
        meal: Selected meal (Breakfast, Lunch, Snacks, Dinner)
        image_data: Optional image as bytes
    
    Returns:
        Dictionary with keys: category, severity, summary
        Or error dict if analysis fails
    """
    api_key = get_gemini_api_key()
    if not api_key:
        return {
            "error": True,
            "message": "Gemini API key not configured. Please add GEMINI_API_KEY to Streamlit Secrets.",
        }
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Build the prompt
        prompt = f"""You are analyzing a food quality complaint from a college hostel student.

Student's complaint about {meal}:
"{complaint_text}"

Analyze this complaint and return ONLY a valid JSON object with these fields:
- category: One of [Hygiene, Taste, Quantity, Timing, Other]
- severity: One of [Low, Medium, High, Critical]
- summary: A short, neutral, factual summary (1-2 sentences) of what was reported

Important guidelines:
- Use neutral, cautious language (e.g., "reported", "possible", "appears")
- Do not make assumptions or add information not stated
- Do not identify people in images
- Do not make medical diagnoses
- Focus on what the student reported

Return ONLY the JSON object, no other text."""
        
        # If image is provided, include it
        if image_data:
            # Encode image to base64
            base64_image = base64.standard_b64encode(image_data).decode("utf-8")
            
            response = model.generate_content([
                prompt,
                {
                    "mime_type": "image/jpeg",
                    "data": base64_image,
                }
            ])
        else:
            response = model.generate_content(prompt)
        
        # Parse response
        response_text = response.text.strip()
        
        # Try to extract JSON from response
        # Sometimes Gemini wraps it in markdown code blocks
        if response_text.startswith("```json"):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith("```"):
            response_text = response_text[3:]  # Remove ```
        if response_text.endswith("```"):
            response_text = response_text[:-3]  # Remove trailing ```
        
        response_text = response_text.strip()
        
        analysis = json.loads(response_text)
        
        # Validate response
        validation_error = validate_gemini_response(analysis)
        if validation_error:
            return {
                "error": True,
                "message": f"Invalid AI response: {validation_error}",
            }
        
        return {
            "error": False,
            "category": analysis["category"],
            "severity": analysis["severity"],
            "summary": analysis["summary"],
        }
    
    except json.JSONDecodeError as e:
        return {
            "error": True,
            "message": f"Failed to parse AI response: {str(e)}",
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"Error analyzing complaint: {str(e)}",
        }


def validate_gemini_response(response: dict) -> Optional[str]:
    """
    Validate Gemini's response.
    
    Returns:
        Error message if invalid, None if valid
    """
    valid_categories = ["Hygiene", "Taste", "Quantity", "Timing", "Other"]
    valid_severities = ["Low", "Medium", "High", "Critical"]
    
    if "category" not in response:
        return "Missing 'category' field"
    
    if response["category"] not in valid_categories:
        return f"Invalid category: {response['category']}"
    
    if "severity" not in response:
        return "Missing 'severity' field"
    
    if response["severity"] not in valid_severities:
        return f"Invalid severity: {response['severity']}"
    
    if "summary" not in response:
        return "Missing 'summary' field"
    
    if not isinstance(response["summary"], str) or not response["summary"].strip():
        return "Summary must be a non-empty string"
    
    return None
