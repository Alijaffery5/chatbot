from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Load the pre-trained Flan-T5 base model for sequence-to-sequence tasks
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

# Load the tokenizer for Flan-T5, which converts text to token IDs and vice versa.
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

def generate_response(user_input):
    # Encode the user input into token IDs, producing a PyTorch tensor with input data.
    inputs = tokenizer(user_input, return_tensors="pt")

    # Generate a response using the model with specified generation parameters.
    outputs = model.generate(
        **inputs,  # Provide the encoded inputs to the model.
        max_new_tokens=100,  # Set a maximum limit of 100 tokens for the generated response.
        num_beams=5,  # Use beam search with 5 beams to enhance the quality of the output.
        no_repeat_ngram_size=2,  # Prevent repeating any 2-word sequences in the generated response.
        top_k=50,  # Use top-k sampling, considering the top 50 options at each step.
        do_sample=True,
        top_p=0.9,  # Apply top-p (nucleus) sampling to include tokens from the top 90% probability mass.
        early_stopping=True  # Stop generating tokens once an end-of-sequence token is predicted.
    )

    # Decode the generated tokens back into a readable string, ignoring special tokens used by the model.
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Return the generated response as a text string.
    return response
