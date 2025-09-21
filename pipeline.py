from file_uploder import file_uploder
from prompt import OpenAIConfig

class HopePipeline:
    def __init__(self, api_key):
        self.openai = OpenAIConfig(api_key=api_key)

    def run(self, user_input, location, csv_data, history):
        enriched_input = user_input
        if location:
            enriched_input += f"\n\n[User is currently located at: {location}]"

        context = ""
        keywords = file_uploder.extract_keywords(user_input)

        if csv_data is not None and keywords:
            filtered_df = file_uploder.filter_by_keywords(csv_data, keywords)
            if not filtered_df.empty:
                chunks = file_uploder.chunk_dataframe(filtered_df) 
                context = chunks[0]

        prompt = self.build_prompt(enriched_input, context)

        # Send prompt to OpenAI, but do NOT store it as user message
        response = self.openai.get_response(prompt, history, context)

        # Manually append clean user_input to history for display
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": response})

        return response

    def build_prompt(self, enriched_input, context):
        if context:
            return f"""
                    User said: {enriched_input}

                    Please respond with:
                    1. A short, emotionally supportive message based on the user's need.
                    2. Then suggest 1 to 3 nearby resources using the data provided below. Include name and Google Maps link if available.

                    Data:
                    {context}
                    """
        else:
            return f"""
                    User said: {enriched_input}

                    Please respond with:
                    1. A short, emotionally supportive message based on the user's need.
                    2. If no data is available, gently ask if the user would like to expand the search or clarify their request.
                    """
