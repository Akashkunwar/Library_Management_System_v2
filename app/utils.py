# Define your utility functions or helper functions here
import os
import datetime

def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def update_issue_status(book_issues):
    today = datetime.date.today().strftime('%Y-%m-%d')
    for book_issue in book_issues:
        if book_issue.IssueStatus == 'Approved' and book_issue.IssueDate < today:
            book_issue.IssueStatus = 'Rejected'
