from flask import Blueprint, render_template, request
import openai

chatgpt_service = Blueprint('chatgpt_service',__name__)

#openai.api_key = os.environ["OPENAI_API_KEY"] # Uncomment this line if you have an environment API key
#openai.api_key = "replace" # Uncomment and replace with your API key
openai.api_key_path = ".\key.txt" # Uncomment if you have a file with your API key

@chatgpt_service.route("/chatgpt_service/", methods=("GET", "POST"))
def chatgpt_service_route():
    if request.method == "GET":
        return render_template("/templates/chatgpt_template/index.html")

    if request.form["question"]:
        conversations = []
        question = "Me: " + request.form["question"]

        response = openai.Completion.create(
            model = "text-davinci-003",
            prompt = question,
            temperature = 0.6,
            max_tokens = 256,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0.6
        )

        answer = "AI: " + response.choices[0].text.strip()

        conversations.append(question)
        conversations.append(answer)

        return render_template("/templates/chatgpt_template/index.html", chat= conversations)
    else:
        return render_template("/templates/chatgpt_template/index.html")
