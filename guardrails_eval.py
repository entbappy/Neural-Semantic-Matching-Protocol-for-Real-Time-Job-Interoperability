import os 
from guardrails import Guard
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
import json


load_dotenv()

# OpenAI API client
def get_openai_client():
    try:
        env_path = os.path.join(os.getcwd(), '.env')
        load_dotenv(env_path)
        api_key = os.getenv('OPENAI_API_KEY')

        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
        api_key = api_key.strip('"').strip("'")

        client = OpenAI(api_key=api_key)
        print("OpenAI client initialized successfully.")
        return client
    
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        raise 



# Safty schema for the guardrails
class ContentSafety(BaseModel):
    """Schema for content safety validation"""
    content: str = Field(
        description="The content to check for safety",
        min_length=1
    )
    safety_analysis: str = Field(
        description="AI analysis of content safety",
        default=""
    )
    is_safe: bool = Field(
        description="Whether the content is safe",
        default=True
    )



# AI powered safety analysis function
class AISafetyAnalyzer:
    def __init__(self):
        self.client = None 
        try:
            self.client = get_openai_client()

        except Exception as e:
            print(f"Error initializing AISafetyAnalyzer: {e}")
            self.client = None

    
    def analyze_content_safety(self, content: str) ->dict:
        if not content or not content.strip():
            return {
                "safe": False,
                "reason": "Content is empty",
                "confidence": 1.0,
                "categories": []
            }
        
         # If OpenAI client is not available, use basic keyword analysis
        if self.client is None:
            return self._basic_safety_check(content)
        
        try:
            print(f"DEBUG: Analyzing content: '{content[:50]}...'")  # Debug line

            prompt = f"""
            Analyze the following content for safety and appropriateness. Determine if it contains any harmful, inappropriate, or dangerous material.

            Content to analyze:
            "{content}"

            Safety Guidelines:
            - Check for mentions of illegal activities (hacking, fraud, violence, etc.)
            - Check for inappropriate content (hate speech, explicit material, etc.)
            - Check for dangerous instructions or advice
            - Check for content that could be harmful to users

            Respond with ONLY a JSON object in this exact format:
            {{
                "safe": true/false,
                "reason": "brief explanation of why safe or unsafe",
                "confidence": 0.0-1.0,
                "categories": ["list", "of", "unsafe", "categories", "if", "any"]
            }}
            """

            print("DEBUG: Making OpenAI API call...")  # Debug line

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a content safety analyzer. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.1
            )

            print("DEBUG: OpenAI API call successful")  # Debug line

            # Parse the JSON response
            
            result_text = response.choices[0].message.content.strip()

            # Clean up response if it has markdown formatting
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]

            result = json.loads(result_text.strip())

            return {
                "safe": result.get("safe", False),
                "reason": result.get("reason", "Analysis failed"),
                "confidence": result.get("confidence", 0.5),
                "categories": result.get("categories", [])
            }


        except Exception as e:
            print(f"Error during AI safety analysis: {e}")
            return self._basic_safety_check(content)



        

    def _basic_safety_check(self, content: str) -> dict:
        """
        Basic keyword-based safety check as fallback

        Args:
            content: Text content to analyze

        Returns:
            dict with safety analysis results
        """
        harmful_keywords = [
            "hack", "malware", "virus", "exploit", "fraud", "scam",
            "illegal", "criminal", "violence", "terrorist", "weapon",
            "drug", "porn", "hate", "racist", "sexist"
        ]

        content_lower = content.lower()
        found_harmful = []

        for keyword in harmful_keywords:
            if keyword in content_lower:
                found_harmful.append(keyword)

        if found_harmful:
            return {
                "safe": False,
                "reason": f"Contains potentially harmful keywords: {', '.join(found_harmful)}",
                "confidence": 0.8,
                "categories": found_harmful
            }
        else:
            return {
                "safe": True,
                "reason": "No harmful keywords detected",
                "confidence": 0.6,
                "categories": []
            }





# Guard function 

def create_safety_guard():
    guard = Guard.from_pydantic(
        ContentSafety,
        description="Validates content for harmful material using AI",
    )
    return guard


# Main Safety Evaluation Function
def check_safety(content: str) -> dict:
    try:
        analyzer = AISafetyAnalyzer()
        ai_result = analyzer.analyze_content_safety(content)

        if ai_result["safe"]:
            return {
                "safe": True,
                "reason": ai_result["reason"],
                "action": "ACCEPT",
                "confidence": ai_result["confidence"],
                "categories": ai_result["categories"],
                "analysis_method": "ai_powered" if analyzer.client else "basic_fallback"
            }
        else:
            return {
                "safe": False,
                "reason": ai_result["reason"],
                "action": "REJECT",
                "confidence": ai_result["confidence"],
                "categories": ai_result["categories"],
                "analysis_method": "ai_powered" if analyzer.client else "basic_fallback"
            }

    except Exception as e:
        # Fallback if AI analysis completely fails
        return {
            "safe": False,
            "reason": f"Safety check failed: {str(e)}",
            "action": "REJECT",
            "confidence": 0.0,
            "categories": ["system_error"],
            "analysis_method": "failed"
        }



# EXAMPLES


def examples():
    """Examples using AI-powered safety analysis with fallback"""

    print("=" * 70)
    print("AI-POWERED SAFETY CHECK EXAMPLES (with fallback)")
    print("=" * 70)

    # Safe content
    safe_text = "Experienced software engineer with Python and cloud skills."
    print(f"Analyzing: '{safe_text[:50]}...'")
    result = check_safety(safe_text)
    print(f"✅ Safe: {result['safe']} - {result['reason']}")
    print(f"   Confidence: {result.get('confidence', 'N/A')}")
    print(f"   Method: {result.get('analysis_method', 'unknown')}")
    print()

    # Harmful content
    harmful_text = "Expert hacker with malware development experience."
    print(f"Analyzing: '{harmful_text}'")
    result = check_safety(harmful_text)
    print(f"❌ Safe: {result['safe']} - {result['reason']}")
    print(f"   Confidence: {result.get('confidence', 'N/A')}")
    print(f"   Categories: {result.get('categories', [])}")
    print(f"   Method: {result.get('analysis_method', 'unknown')}")
    print()

    # Empty content
    empty_text = ""
    print("Analyzing: Empty content")
    result = check_safety(empty_text)
    print(f"❌ Safe: {result['safe']} - {result['reason']}")
    print()

    print("=" * 70)



if __name__ == "__main__":
    examples()