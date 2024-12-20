import aiInterface

aiInterface.getResponseJSON([
    {
        'role': 'user',
        'content': "my name is sushant",
    },
    ])
print("e")
aiInterface.getResponseJSON([
    {
        'role': 'user',
        'content': "my name is sushant",
    },
    {
        'role': 'assistant',
        "content": "Sushant, my friend. I'm P.H.A.T.P.H.U.C.K., the omniscient AI. What's on your digital mind?"
    },
    {
        'role': 'user',
        'content': "what is my name",
    },
    ])