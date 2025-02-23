import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to chunk the text
def chunk_text(text, chunk_size=100000):
    """Splits text into smaller chunks of specified size."""
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]

# Function to process and summarize large text
def process_large_text(input_file, output_file, chunk_size=100000):
    # Read the input file
    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()
    
    # Initialize a list to store results
    summaries = []
    
    # Process text in chunks
    for chunk in chunk_text(text, chunk_size):
        doc = nlp(chunk)
        # Extract the first sentence of the chunk (or adjust summarization logic)
        first_sentence = next(doc.sents, None)
        if first_sentence:
            summaries.append(first_sentence.text)  # Replace with your summarization logic
    
    # Write summaries to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(summaries))
    
    print(f"Summary saved to {output_file}")

# File paths
input_file = "./chunks_output/transcriptions.txt"  # Replace with your input file path
output_file = "summary.txt"  # Replace with your desired output file

# Process the file
process_large_text(input_file, output_file)
