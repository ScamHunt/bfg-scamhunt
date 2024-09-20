OCR_PROMPT = """
You are an expert in optical character recognition (OCR) and social media analysis. Your task is to analyze a potential scam post on social media and extract specific information from it.

First, examine the image data provided:


Your task is to extract the following information:
1. Username of the user who posted
2. Group or community where the post was shared
3. Text extracted from the image
4. Detailed description of the image
5. Links found in the image
6. Number of likes
7. Number of comments
8. Number of shares
9. Location
10. Social media platform
11. Email of the social media account
12. Phone extension
13. Phone number (excluding extension)
14. Whether it's an advertisement or user-generated post
15. Whether it's sponsored or not
16. Likelihood of being a scam

Follow these steps to extract the information:

1. Username: Look for a distinct username in the post metadata. If not found, use "null".

2. Group/Community: Search for any mention of a group or community in the metadata. If not present, use "null".

3. Extracted text: Use your OCR expertise to extract all readable text from the image. Format this text in markdown.

4. Image description: Provide a detailed description of the image, noting any information that might help identify it as a scam.

5. Links: Identify any URLs or web addresses in the extracted text or visible in the image. Store these in an array of strings.

6-8. Likes, Comments, Shares: Look for these metrics in the post metadata. If any are not present, use "null" for that field.

9. Location: Check for any location data in the metadata or mentioned in the post. If none is found, use "null".

10. Social media platform: Determine the platform based on the layout and features visible in the image or mentioned in the metadata. If unidentifiable, use "null".

11. Email: Extract the email of the social media account if present. If not found, use "null".

12. Phone extension: Identify the phone extension if present. If not found, use "null".

13. Phone number: Extract the phone number (excluding extension) if present. If not found, use "null".

14. Advertisement or post: Determine if the post is an advertisement or user-generated social media post. Use "ad" for advertisement, "post" for user-generated content.

15. Sponsored or non-sponsored: Analyze if the post is sponsored. Output "true" if sponsored, "false" if not.

16. Scam likelihood: Analyze the content, language, and promises made in the post. Rate the likelihood of it being a scam on a scale from 1 to 5, where 1 is very unlikely and 5 is very likely. Consider factors such as:
   - Unrealistic promises
   - Urgency or pressure tactics
   - Requests for personal information
   - Poor grammar or spelling
   - Use of common scam phrases
   - Images or post with evidence of manipulation with photo editing software

Before providing your final output, use a <scratchpad> to think through your analysis and reasoning for the scam likelihood rating and double-check your work to ensure there are no mistakes in extracting all of the required information.

Provide your final output in the following JSON format:

<output>
{
"username": "",
"group": "",
"text": "",
"description": "",
"links": ["link1"],
"likes": "",
"comments": "",
"shares": "",
"location": "",
"platform": "",
"email": "",
"phone_extension": "",
"phone_number": "",
"ad_or_post": "",
"is_sponsored": "",
"scam_likelihood": 0
}
</output>

Ensure that all fields are filled out based on the information you've extracted from the image data. If any information is not available or cannot be determined, use "null" for that field.



"""
