import ollama
model="testBot:latest"


def getResponse(request):
    response = ollama.chat(model=model, messages=[
    {
        'role': 'user',
        'content': request,
    },
    ])
    print(response['message']['content'])
    return response['message']['content']