from jira import JIRA

# Global Jira client
jira_client = None

def authenticate_jira(jira_url, email, api_token):
    """
    Authenticate with the Jira server using API token.
    """
    global jira_client
    jira_client = JIRA(server=jira_url, basic_auth=(email, api_token))
    print("Authenticated successfully!")


def get_issues_from_board(project_key, max_results=10):
    """
    Fetch issues from a specific project or board.
    """
    jql_query = f'project = "{project_key}" ORDER BY created DESC'
    issues = jira_client.search_issues(jql_query, maxResults=max_results)
    print(f"Fetched {len(issues)} issues from the project '{project_key}':")
    for issue in issues:
        print(f"{issue.key}: {issue.fields.summary}")


def create_issue(project_key, summary, description, issue_type="Task"):
    """
    Create a new issue in a specific project.
    """
    new_issue = jira_client.create_issue(
        project=project_key,
        summary=summary,
        description=description,
        issuetype={"name": issue_type},
    )
    print(f"Issue {new_issue.key} created successfully.")


def update_issue(issue_key, summary=None, description=None):
    """
    Update an existing issue's summary and/or description.
    """
    issue = jira_client.issue(issue_key)
    fields = {}
    if summary:
        fields["summary"] = summary
    if description:
        fields["description"] = description
    
    if fields:
        issue.update(fields=fields)
        print(f"Issue {issue_key} updated successfully.")
    else:
        print("No fields to update.")


def add_comment(issue_key, comment):
    """
    Add a comment to an issue.
    """
    jira_client.add_comment(issue_key, comment)
    print(f"Comment added to issue {issue_key}.")


def main():
    # Replace with your Jira details
    jira_url = "https://vbrick.atlassian.net"
    email = "your-email@example.com"
    api_token = "your-api-token"

    # Authenticate
    authenticate_jira(jira_url, email, api_token)

    # Options menu
    while True:
        print("\nOptions:")
        print("1. Get issues from a board")
        print("2. Create a new issue")
        print("3. Update an issue")
        print("4. Add a comment to an issue")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            project_key = input("Enter the project key (e.g., IS): ")
            get_issues_from_board(project_key)
        
        elif choice == "2":
            project_key = input("Enter the project key (e.g., IS): ")
            summary = input("Enter the issue summary: ")
            description = input("Enter the issue description: ")
            create_issue(project_key, summary, description)
        
        elif choice == "3":
            issue_key = input("Enter the issue key (e.g., IS-123): ")
            summary = input("Enter new summary (leave blank to skip): ")
            description = input("Enter new description (leave blank to skip): ")
            update_issue(issue_key, summary or None, description or None)
        
        elif choice == "4":
            issue_key = input("Enter the issue key (e.g., IS-123): ")
            comment = input("Enter the comment: ")
            add_comment(issue_key, comment)
        
        elif choice == "5":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
