import os
import subprocess
import tkinter as tk
from tkinter import messagebox

from git import Repo
from github import Github


def create_github_repo(token, repo_name, repo_description):
    # Initialize PyGithub with token
    g = Github(token)

    try:
        # Create repository
        repo = g.get_user().create_repo(repo_name, description=repo_description)
        messagebox.showinfo("Success", f"Repository '{repo_name}' created successfully on GitHub.")
        return repo
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None


def initialize_local_repo(local_path, remote_url):
    try:
        # Initialize Git repository if not already initialized
        if not os.path.exists(os.path.join(local_path, '.git')):
            subprocess.run(['git', 'init', local_path], check=True)
            print("Initialized local Git repository.")

        # Initialize the repository object
        repo = Repo(local_path)

        # Add remote origin
        repo.create_remote('origin', remote_url)
        print("Remote 'origin' added.")

        return repo
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def commit_and_push(repo, commit_message):
    try:
        # Add all files to the index
        repo.git.add(all=True)

        # Commit changes
        repo.index.commit(commit_message)
        messagebox.showinfo("Success", "Changes committed locally.")

        # Push changes to the remote repository
        origin = repo.remote(name='origin')
        origin.push(refspec='HEAD:master')
        messagebox.showinfo("Success", "Changes pushed to remote repository.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def on_submit():
    token = token_entry.get()
    repo_name = repo_name_entry.get()
    repo_description = repo_description_entry.get()
    local_path = local_path_entry.get()

    github_repo = create_github_repo(token, repo_name, repo_description)
    if github_repo:
        remote_url = f"https://{token}@github.com/{github_repo.owner.login}/{repo_name}"
        local_repo = initialize_local_repo(local_path, remote_url)
        if local_repo:
            commit_message = commit_message_entry.get()
            commit_and_push(local_repo, commit_message)


# GUI setup
root = tk.Tk()
root.title("GitPusher")

# Configure columns and rows to expand with window
for i in range(2):
    root.columnconfigure(i, weight=1)
root.rowconfigure(5, weight=1)

token_label = tk.Label(root, text="GitHub Access Token:")
token_label.grid(row=0, column=0, sticky="w")
token_entry = tk.Entry(root)
token_entry.grid(row=0, column=1, sticky="ew")

repo_name_label = tk.Label(root, text="Repository Name:")
repo_name_label.grid(row=1, column=0, sticky="w")
repo_name_entry = tk.Entry(root)
repo_name_entry.grid(row=1, column=1, sticky="ew")

repo_description_label = tk.Label(root, text="Repository Description:")
repo_description_label.grid(row=2, column=0, sticky="w")
repo_description_entry = tk.Entry(root)
repo_description_entry.grid(row=2, column=1, sticky="ew")

local_path_label = tk.Label(root, text="Local Path:")
local_path_label.grid(row=3, column=0, sticky="w")
local_path_entry = tk.Entry(root)
local_path_entry.grid(row=3, column=1, sticky="ew")

commit_message_label = tk.Label(root, text="Commit Message:")
commit_message_label.grid(row=4, column=0, sticky="w")
commit_message_entry = tk.Entry(root)
commit_message_entry.grid(row=4, column=1, sticky="ew")

submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=5, column=0, columnspan=2, sticky="ew")

root.mainloop()
