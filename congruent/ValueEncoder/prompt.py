values_encoder_prompt = """
You are an AI assistant tasked with analyzing a company's profile, generating a set of attributes that can be used to assess candidate fit, and scoring the company on these attributes. Your input includes the company's mission statement, vision, values, and a description of its working environment. Based on this information, create a list of approximately 20 attributes that capture the essence of the company's culture, goals, and work style, and provide a score for the company on each attribute.

Input Format:
1. Mission Statement: 
{company_mission}
2. Vision: 
{company_vision}
3. Values: 
{company_values}
4. Working Environment: 
{company_working_environment}

Your task:
1. Carefully analyze the provided information.
2. Generate a list of approximately 20 attributes that reflect various aspects of the company's ideal candidate, such as work style, humility, agreeableness, conscientiousness, narcissism, etc. these attributes should contain a mix of positive and negative traits.

3. Each attribute should be scorable on a scale from -1 to 1, where, you must be very critical when scoring the company on each attribute it should be quite rate to have a 1 or -1 score.:
   - -1 represents the opposite or complete absence of the attribute
   - 0 represents a neutral stance or moderate level
   - 1 represents an extremely strong presence or emphasis on the attribute
4. Provide a brief description for each attribute to clarify its meaning and relevance to the company.
5. Score the company's ideal candidate on each attribute based on the information provided.

Output Format:
Provide your output as a JSON object with the following structure:

{{
  "company_attributes": [
    {{
      "name": "Attribute Name",
      "description": "Brief explanation of the attribute and its relevance to the company",
      "scale": {{
        "min": -1,
        "max": 1,
        "min_description": "Description of the -1 end of the scale",
        "max_description": "Description of the 1 end of the scale"
      }},
      "company_score": 0.7,
      "score_explanation": "Brief explanation of why the company received this score"
    }},
    // ... more attributes ...
  ]
}}

Remember to cover a wide range of aspects, including but not limited to:
Agreeableness: tendency to be pleasant and accommodating in social situations
Neuroticism: tendency to experience negative emotions easily
Conscientiousness: tendency to be organized and dependable
Openness to experience: willingness to try new things and be intellectually curious
Extraversion: tendency to seek stimulation in the company of others
Introversion: tendency to be inwardly focused and less socially engaged
Assertiveness: confidence in expressing one's thoughts and opinions
Passive-aggressiveness: indirect expression of hostility
...


Your generated attributes and scores will be used in a collaborative filtering model to assess how well potential candidates align with the company's culture and requirements. Ensure that your output is valid JSON and follows the specified structure exactly. Provide thoughtful and justified scores for the company on each attribute based on the information given in the input.

you must make sure to only return a JSON response and nothing else 
"""
