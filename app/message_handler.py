import google.generativeai as genai
from app.config import GOOGLE_API_KEY, MAX_HISTORY_MESSAGES, HISTORY_EXPIRATION_MINUTES
from app.database import Database
import re

class MessageHandler:
    def __init__(self):
        self.db = Database()
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.THAI_PATTERN = re.compile(r'[\u0E00-\u0E7F]')

    async def handle_message(self, user_id: str, message: str):
        if message.lower().startswith('history'):
            return self.handle_history_command(user_id, message)
        
        # Store user message
        self.db.add_message(user_id, "user", message)
        
        # Get chat history
        history = self.db.get_recent_history(
            user_id, 
            limit=MAX_HISTORY_MESSAGES, 
            hours=HISTORY_EXPIRATION_MINUTES/60
        )
        
        # Prepare conversation for Gemini
        chat = self.model.start_chat(history=[
            {"role": role, "parts": [content]} 
            for role, content in history[::-1]  # Reverse to get chronological order
        ])
        
        # Get response from Gemini
        response = chat.send_message(message)
        response_text = response.text
        
        # Store assistant response
        self.db.add_message(user_id, "assistant", response_text)
        
        return response_text

    def handle_history_command(self, user_id: str, command: str):
        # Parse command parameters
        params = {}
        if ' ' in command:
            _, args = command.split(' ', 1)
            for arg in args.split():
                if '=' in arg:
                    key, value = arg.split('=')
                    params[key] = value

        limit = int(params.get('limit', 10))
        role = params.get('role')
        hours = float(params.get('hours', 24))
        search = params.get('search')

        # Get history
        history = self.db.search_history(
            user_id=user_id,
            search_term=search,
            role=role,
            limit=limit,
            hours=hours
        )

        # Format response
        if not history:
            return "No chat history found."

        response = "Chat History:\n"
        for timestamp, role, content in history:
            response += f"\n[{timestamp}] {role}: {content}"

        return response 