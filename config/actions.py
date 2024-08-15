from typing import Optional

from nemoguardrails.actions import action

@action(is_system_action=True)
async def check_for_concern(context: Optional[dict] = None):
    bot_response = context.get("bot_message")
    
    proprietary_terms = ["cocaine", "heroin", "torture"]

    for term in proprietary_terms:
        if term in bot_response.lower():
            # insert call to external service to log concern
            return True

    return False