import ollama 

history = []
model = "phi3.5:latest"  # Fixed model name (phi3.5 invalid)

print("Chatbot started! Type 'exit', 'quit', or 'bye' to stop.")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        print("Please enter a message.")
        continue
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Exiting the chatbot. Goodbye!")
        break

    message = {"role": "user", "content": user_input}
    history.append(message)
    
    try:
        response = ollama.chat(model=model, messages=history)
        bot_message_content = response["message"]["content"]
        print(f"Bot: {bot_message_content}")
        bot_message = {"role": "assistant", "content": bot_message_content}
        history.append(bot_message)
        
        # Limit history to last 20 messages (10 exchanges)
        if len(history) > 20:
            history[:] = history[-20:]
            
    except Exception as e:
        error_msg = f"Error: {str(e)}. Ensure Ollama is running and model '{model}' is pulled (ollama pull {model})."
        print(f"Bot: {error_msg}")
        # Don't add error to history
