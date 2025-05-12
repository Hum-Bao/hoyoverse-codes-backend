import os
from pathlib import Path

from github import Github, InputGitTreeElement


def push(path: Path, file_names: list[str]) -> None:
    g = Github(os.getenv("GITHUB_TOKEN", ""))
    repo = g.get_user().get_repo(os.getenv("GITHUB_REPO", ""))
    commit_message = "Python commit"
    master_ref = repo.get_git_ref("heads/main")
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)

    element_list = []
    for file in file_names:
        file_path = path / file
        with file_path.open() as input_file:
            data = input_file.read()
        element = InputGitTreeElement(file, "100644", "blob", data)
        element_list.append(element)

    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)
