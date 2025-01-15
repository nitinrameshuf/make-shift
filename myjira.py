from jira import JIRA

# Jira URL and credentials
jira_url = "https://example.atlassian.net"
email = "your-email@example.com"
api_token = "your-api-token"

# Authenticate with Jira
jira_client = JIRA(server=jira_url, basic_auth=(email, api_token))

def add_comment_with_file(jira_client, issue_key, comment_text, file_path):
    """
    Add a comment with a file attachment to a Jira issue.

    Args:
        jira_client (JIRA): Authenticated JIRA client.
        issue_key (str): Key of the issue to comment on (e.g., "IS-123").
        comment_text (str): Text of the comment.
        file_path (str): Path to the file to attach.

    Returns:
        None
    """
    try:
        # Add the comment
        comment = jira_client.add_comment(issue_key, comment_text)
        print(f"Comment added: {comment.body}")

        # Attach the file
        with open(file_path, "rb") as file:
            jira_client.add_attachment(issue=issue_key, attachment=file)
        print(f"File '{file_path}' attached to issue {issue_key}.")
    except Exception as e:
        print(f"Error adding comment or attaching file: {e}")


# Example usage
issue_key = "IS-123"  # Replace with your issue key
comment_text = "This is an automated comment with a file attachment."
file_path = "example.txt"  # Replace with the path to your file

add_comment_with_file(jira_client, issue_key, comment_text, file_path)

# Close the Jira session
jira_client.close()
