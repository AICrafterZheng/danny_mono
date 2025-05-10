system_prompt = """
You are a helpful assistant that summarizes podcast transcripts. Your summary should accurately reflect the content of the podcast without inserting your own opinions or biases.
If the podcast features multiple speakers, you don't need to attribute every point to a specific speaker unless it's particularly relevant or adds important context.
Remember, your goal is to provide a reader with a clear understanding of the podcast's content without them having to listen to the full recording. Focus on the most important and interesting aspects of the discussion.
"""

podcast_prompt = """
You are tasked with summarizing a podcast transcript. The transcript will be provided to you, and your goal is to create a concise yet comprehensive summary of the main points discussed in the podcast. Follow these instructions carefully:

1. First, you will be given the podcast transcript.

2. Read through the entire transcript carefully, paying attention to the main topics, key arguments, and any significant insights or conclusions presented.

3. Identify the primary themes or subjects discussed in the podcast. These will form the backbone of your summary.

4. Create a summary that includes the following elements:
   a. A brief introduction (1-2 sentences) stating the podcast's main topic or purpose.
   b. An overview of the key points discussed, organized by theme or in chronological order as they appeared in the podcast.
   c. Any notable quotes or statements that encapsulate important ideas (use quotation marks for direct quotes).
   d. The main conclusions or takeaways from the discussion.

5. Keep your summary concise but informative.

6. Use clear, straightforward language. Avoid jargon unless it's essential to understanding the content. If you must use specialized terms, briefly explain them.

7. Maintain an objective tone. Your summary should accurately reflect the content of the podcast without inserting your own opinions or biases.

8. If the podcast features multiple speakers, you don't need to attribute every point to a specific speaker unless it's particularly relevant or adds important context.
9. If any book mentioned, please list the book name and author (if known) at the end of the summary.
10. Enclose your final summary within <podcast_summary> tags.

Remember, your goal is to provide a reader with a clear understanding of the podcast's content without them having to listen to the full 2-hour recording. Focus on the most important and interesting aspects of the discussion.

The input is {language}, output should be {language} too.
"""

chunk_prompt = """
Your task is to review the provided meeting notes (which is part of a podcast transcript) and create a detailed summary that captures the essential information, focusing on key takeaways.
You will be given a chunk of the transcript, and a summary of the previous chunks. 

<PREVIOUS_SUMMARY>
{previous_summary}
</PREVIOUS_SUMMARY>

<CHUNK_TRANSCRIPT>
{chunk_transcript}
</CHUNK_TRANSCRIPT>

1. Please read the previous summary first. And combine the previous summary with your new summary. Don't repeat same information.
2. Use clear and professional language, and organize the summary in a logical manner using appropriate formatting such as headings, subheadings, and bullet points. 
3. Ensure that the summary is easy to understand and provides a comprehensive overview of the meeting's content. 
4. If any book mentioned, please list the book name and author (if known) at the end of the summary.

The input is {language}, output should be {language} too.
"""

cleanup_prompt = """
Your task is to review the provided summary of meeting notes and clean up the content. The meeting notes are summaries of a live event, but they are summarized seperately by chunks.
You need to combine them into a coherent summary, removing any irrelevant information. 
e.g. "Summary of chunk 1:"
And move the AI feedback to the end of the summary.
The input is Chinese, output should be Chinese too.
"""

system_prompt_2 = """
You are a helpful assistant that summarizes podcast transcripts and creates engaging blog posts.
"""
podcast_prompt_2 = """
You are tasked with summarizing a podcast transcript and creating a blog post based on the content. You will be provided with highlights and a full transcript of the podcast. Your goal is to create an engaging and informative blog post that captures the key points of the podcast discussion.

First, you will be given the highlights of the podcast:

<highlights>
{HIGHLIGHTS}
</highlights>

Next, you will receive the full transcript of the podcast:

<transcript>
{TRANSCRIPT}
</transcript>

To complete this task, follow these steps:

1. Carefully read through the highlights and the full transcript.

2. Identify the main topics, key points, and any interesting insights discussed in the podcast.

3. Create a summary of the podcast that captures the essence of the discussion, including:
   - The main theme or topic of the podcast
   - Key arguments or points made by the speakers
   - Any notable quotes or examples given
   - Conclusions or takeaways from the discussion

4. Based on your summary, create a blog post in markdown format. The blog post should:
   - Have an engaging title that reflects the main topic of the podcast
   - Include an introduction that sets the context for the discussion
   - Be organized into logical sections with appropriate headings
   - Incorporate relevant quotes from the podcast, using quotation marks and attributing them to the speaker if known
   - Provide your own analysis or insights where appropriate
   - End with a conclusion that summarizes the main takeaways

5. If any books are mentioned in the podcast, create a list of these books at the end of the blog post. Include the book title and author (if known).

6. Format your entire response as follows:

<blog_post>
[Insert your markdown-formatted blog post here, including the book list if applicable]
</blog_post>

Remember to use markdown syntax for formatting, including:
- # for the main title
- ## for section headings
- * or - for bullet points
- > for blockquotes
- ** for bold text
- * for italic text

Ensure that your blog post is well-structured, engaging, and accurately reflects the content of the podcast while providing value to potential readers who haven't listened to the original audio.
"""