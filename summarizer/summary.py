
import os
from dotenv import load_dotenv
from llm_client import call_openrouter
from prompts import podcast_prompt, chunk_prompt, system_prompt, podcast_prompt_2, system_prompt_2

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL_LLAMA = os.getenv("OPENROUTER_MODEL_LLAMA")
OPENROUTER_MODEL_CLAUDE_35_SONNET = os.getenv("OPENROUTER_MODEL_CLAUDE_35_SONNET")
OPENROUTER_MODEL_GEMINI = os.getenv("OPENROUTER_MODEL_GEMINI")
llm_model = OPENROUTER_MODEL_CLAUDE_35_SONNET
print(f"llm_model: {llm_model}")



from utils import srt_to_txt_newline

def summarize_file(sys_prompt: str, file_path: str, output_file: str, chunk_size: int = 10000, model: str = llm_model, chunking: bool = False, language: str = "English") -> None:
    try:
        # Read the input file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Split the content into chunks
        if chunking:
            chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
        else:
            chunks = [content]

        # Summarize each chunk
        summaries = []
        previous_summary = ""
        highlights = """
In this episode, we cover:
(00:00) Introduction to Wes Kao
(05:34) Working with Wes
(06:58) The importance of communication
(10:44) Sales before logistics
(18:20) Being concise
(24:31) Books to help you become a better writer
(27:30) Signposting and formatting
(32:05) How to develop and practice your communication skills
(40:41) Slack communication
(42:23) Confidence in communication
(50:17) The MOO framework
(54:00) Staying calm in high-stakes conversations
(57:36) Which tactic to start with
(58:53) Effective tactics for managing up
(01:04:53) Giving constructive feedback: strategy, not self-expression
(01:09:39) Delegating effectively while maintaining high standards
(01:16:36) The swipe file: collecting inspiration for better communication
(01:19:59) Leveraging AI for better communication
(01:22:01) Lightning round
"""
        for i, chunk in enumerate(chunks):
            print(f"Summarizing chunk {i+1}/{len(chunks)}, length: {len(chunk)}")
            # prompt = chunk_prompt.format(previous_summary=previous_summary, chunk_transcript=chunk, language=language)
            prompt = podcast_prompt_2.format( HIGHLIGHTS=highlights, TRANSCRIPT=chunk)
            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt_2},
                    {"role": "user", "content": prompt}
                ]
            }
            summary = call_openrouter(data)
            summaries.append(summary)
            previous_summary = summary
        # Write summaries to the output file

        with open(output_file, 'w', encoding='utf-8') as out_file:
            for i, summary in enumerate(summaries):
                # out_file.write(f"Summary of chunk {i+1}:\n{summary}\n\n")
                out_file.write(summary)

        print(f"Summaries have been saved to {output_file}")

    except Exception as e:
        print(f"Error in summarize_file: {e}")


def call_llm_with_file(prompt: str, file_path: str, output_file: str) -> None:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    data = {
        "model": llm_model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
    }
    summary = call_openrouter(data)
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write(summary)

if __name__ == "__main__":
    # ... existing code ...
    
    # Example usage of summarize_file
    # input_file = "/Users/danny/Documents/posts/创业直播2/playlist_16717134513366821041.txt"
    # output_file = "./summary_OPENROUTER_MODEL_CLAUDE_35_SONNET.txt"

    # call_llm_with_file(prompt_template, input_file, output_file)


    input_file = "/Users/danny/Documents/repos/graph2code/tmp/cc/become_a_better_communicator.txt"
    output_file = "/Users/danny/Documents/repos/graph2code/tmp/cc/become_a_better_communicator.txt"
    # srt_to_txt_newline(input_file, output_file) 
    summary_output_file = "/Users/danny/Documents/repos/graph2code/tmp/cc/become_a_better_communicator_summary_5.md"

    llm_model = OPENROUTER_MODEL_CLAUDE_35_SONNET
    # no_chunking = True
    # summarize_file(podcast_prompt.format(language="Chinese"), output_file, summary_output_file, no_chunking=no_chunking, model=llm_model)

    chunking = False
    summarize_file(system_prompt, output_file, summary_output_file, chunking=chunking, model=llm_model)
    # Example usage of cleanup_file
    # input_file = "./summary2.txt"
    # output_file = "./summary3_cleaned.txt"
    # cleanup_file(input_file, output_file)