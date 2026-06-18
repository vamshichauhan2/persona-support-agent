from src.classifier import classify_persona

query = input("Enter your message: ")

result = classify_persona(query)

print("\nDetected Persona")
print(result)