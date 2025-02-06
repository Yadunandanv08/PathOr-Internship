import os
import google.generativeai as genai

class queryModel:
    def __init__(self, chunks):
        self.chunks = chunks
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    def query(self, question):
        context = self._get_context(question)
        return self._generate_response(question, context)
    
    def _get_context(self, question):
        keywords = set(question.lower().split())
        return sorted(
            (chunk for chunk in self.chunks 
             if keywords & set(chunk['text'].lower().split())),
            key=lambda x: len(keywords & set(x['text'].lower().split())),
            reverse=True
        )[:5]

    def _generate_response(self, question, context):
        context_str = '\n\n'.join([f"Page {c['meta']['page']}:\n{c['text']}" 
                                  for c in context])
        
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        Answer strictly based on this context:
        {context_str}
        
        Question: {question}
        
        If the answer isn't in the context, respond with:
        "The document doesn't contain information about this."
        """
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1
            )
        )
        return response.text