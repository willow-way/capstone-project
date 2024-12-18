from langchain.text_splitter import RecursiveCharacterTextSplitter
from helper_functions.llm import get_completion, get_embedding

# **Library Membership Data Collector Class**: Collect and process library membership data
class LibraryMembershipDataCollector:
    def __init__(self, text_path):
        self.text_path = text_path
        self.membership_data = self._load_membership_data()
        self.vector_store = self._process_membership_data()  # Directly store processed data

# **Load Membership Data Function**: Read membership data from a text file
    def _load_membership_data(self):
        """Load membership data from the specified text file."""
        try:
            with open(self.text_path, 'r') as file:
                data = file.read()
            print("Loaded membership data.")
            return data
        except FileNotFoundError:
            raise FileNotFoundError("membership.txt file not found in data folder.")

# **Process Membership Data Function**: Split and embed membership data
    def _process_membership_data(self):
        """Process the loaded membership data into vector embeddings."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " "]
        )

        chunks = text_splitter.split_text(self.membership_data)
        print(f"Chunks created: {len(chunks)}")

        processed_data = []  # Store processed chunks and their embeddings
        
        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk, model='text-embedding-ada-002')

            if embedding is None:
                print(f"Skipping Chunk {i} - failed to generate embedding.")
                continue
            
            if not isinstance(embedding, list):
                print(f"Skipping Chunk {i} - embedding is not a list.")
                continue
            
            print(f"Chunk {i} embedding dimension: {len(embedding)}")
            processed_data.append({
                'document': chunk,
                'embedding': embedding,
                'id': str(i)
            })

        return processed_data  # Return the processed data

# **Extract Membership Types Function**: Extract membership types from the context
    def _extract_membership_types(self, context):
        membership_types = []
        for line in context.split('\n'):
            if "membership" in line.lower():
                membership_types.append(line.strip())
        return "; ".join(membership_types) if membership_types else "various membership types"

    def answer_query(self, user_query):
        try:
            prompt_template = (
                "You are an AI assistant providing information about library memberships and services. "
                "Answer the question using ONLY the information from the following context. "
                "If the exact answer is in the context, use it. If not, provide the most relevant information available. "
                "Do not invent or assume any information not present in the context. "
                "If the information is not available in the context, say so clearly.\n\n"
                "Context:\n{context}\n\n"
                "Question: {question}\n\n"
                "Answer:"
            )
            context = self._retrieve_relevant_context(user_query)
            prompt = prompt_template.format(context=context, question=user_query)
            response = get_completion(prompt)

            if "I don't have that specific information" in response or "no relevant information" in response.lower():
                membership_types = self._extract_membership_types(context)
                return (f"While I don't have the exact number, our library offers several types of memberships. "
                        f"Based on the available information, these include: {membership_types}. "
                        f"Would you like more details about any of these membership options?")

            return response
        except Exception as e:
            print(f"An error occurred while processing your query: {str(e)}")
            return "I apologize, but I encountered an error while processing your query. Please try again or ask about our general membership options."

    def _retrieve_relevant_context(self, user_query):
        try:
            query_embedding = get_embedding(user_query, model='text-embedding-ada-002')
            if query_embedding is None:
                raise ValueError("Failed to generate query embedding")

            # Retrieve the relevant context based on embedding similarity or simply return processed data
            documents = [data['document'] for data in self.vector_store]  # Fetch all processed documents
            
            if not documents:
                return "No relevant context found."
            return "\n".join(documents)  # Return all documents for now
        except Exception as e:
            print(f"Error during context retrieval: {str(e)}")
            return f"Error retrieving context: {str(e)}"
        
    def answer_membership_query(self, user_query):
        """Alias for answer_query to provide compatibility."""
        return self.answer_query(user_query)