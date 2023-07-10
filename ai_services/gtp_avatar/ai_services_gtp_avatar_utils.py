import openai



def get_gpt_response(prompt):
    openai.api_key = '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' #os.environ.get('OPENAI_API_KEY')
    response = openai.Completion.create(
      engine="davinci",
      prompt=prompt,
      temperature=0.5,
      max_tokens=250,
      n=1,
      stop=None,
      presence_penalty=0.6,
      frequency_penalty=0.6,
      best_of=1
    )

    return response.choices[0].text.strip()