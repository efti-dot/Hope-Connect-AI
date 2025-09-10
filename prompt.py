import openai

class OpenAIConfig:
    def __init__(self, api_key: str = "api", model: str = "gpt-4o-mini"):
        """
        Initializes the OpenAI API configuration with the given API key and model.
        """
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key
        self.conversation_history = [{"role": "system", "content": "You are a helpful for people who are homeless. Provide concise and accurate information."}]

    def get_response(self, prompt: str, history: list) -> str:
        """
        Sends a prompt to the OpenAI API and returns the response text.
        Maintains conversation history for context.
        """
        try:
            system_prompt = "You are a helpful for people who are homeless. Provide concise and accurate information."

            history.append({"role": "user", "content": prompt})
            api_history = [{"role": "system", "content": system_prompt}]

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=api_history
            )

            reply = response.choices[0].message['content']
            history.append({"role": "assistant", "content": reply})
            return reply
        
        except Exception as e:
            print(f"Error communicating with OpenAI API: {e}")
            return "Sorry, I couldn't process your request at the moment. Please try again later."
    

    def get_history(self):
        return self.conversation_history