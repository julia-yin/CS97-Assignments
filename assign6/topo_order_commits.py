'''
CS 97 Fall 2020 Assignment 6
Git Repository Organization: Topologically Ordered Commits
Julia Yin
'''

import os
import sys
import zlib
from collections import deque

def topo_order_commits():
    commits_dict = dict()
    build_commits(commits_dict)


# topo_sort: topologically sorts all commits
def topo_sort(sorted_commits=[]):
    commits_dict = build_commits()

    # Find all nodes with no incoming edge (parents)
    root_commits = []
    for c in commits_dict:
        print("Item in commits_dict: " + c)
        if not commits_dict[c].parents:
            root_commits.append(c)

    # Topological sort using Kahn's algorithm
    while root_commits:
        node = commits_dict[root_commits[-1]]
        sorted_commits.append(node.commit_hash)
        for c in node.children:
            c.parents.remove(node)
            if not c.parents:
                root_commits.append(c)

    


# build_commits: builds the commit graph of CommitNodes
def build_commits(commits_dict=dict()):
    # Get all local branch heads
    branches_dict = dict()
    get_local_branches(branches_dict)

    # Depth-first traversal through nodes in branch, starting with head
    objects = os.path.realpath(os.path.join(find_git_dir(), "objects"))
    for root, _, files in os.walk(objects):
        for b in branches_dict:
            # DFS through each branch using a stack
            stack = deque()
            stack.append(b)
            while stack:
                commit = stack.pop()
                path = os.path.join(os.path.join(root, commit[:2]), commit[2:])
                data = zlib.decompress(open(path, 'rb').read()).decode()
                #print("Current commit: " + commit)
                #print("Commit data: " + str(data))
                
                # Get parents of current commit and append them to stack
                parents = []
                for line in data.split("\n"):
                    if line.startswith("parent"):
                        #print("Parent: " + line[7:])
                        parents.append(line[7:])
                        stack.append(line[7:])

                # Insert commit into dict as a CommitNode
                if commit not in commits_dict:
                    commits_dict[commit] = CommitNode(commit)
                # Add parents wherever necessary
                for parent in parents:
                    if parent not in commits_dict:
                        commits_dict[parent] = CommitNode(parent)
                    commits_dict[commit].parents.add(parent)
                    commits_dict[parent].children.add(commit)


# get_local_branches: gets all local branches indexed by commit hash
def get_local_branches(branches_dict=dict()):
    # Get path to .git/refs/heads (pointers to each branch)
    heads = os.path.join(os.path.join(find_git_dir(), "refs"), "heads")
    branches = []

    # For all branches with pointers in heads, store into branches list
    for root, _, files in os.walk(heads):
        # Add each file to branches (remove path to head from file path)
        for f in files:
            path = os.path.join(root, f)
            path = path[len(heads)+1:]
            branches.append(path)
        
        # Insert all branches into dictionary with commit hash as keys
        for b in branches:
            b_hash = open(os.path.join(heads, b), 'r').read().split("\n")[0]
            if b_hash not in branches:
                branches_dict[b_hash] = []
            branches_dict[b_hash].append(b)


# find_git_dir: returns the path to the .git directory
def find_git_dir():
    # Get path to current directory
    path = os.path.abspath(os.curdir)

    # Search through cur and all parent directories for .git until root
    while True:
        for d in os.listdir(path):
            if (d == ".git"):
                # Return path to the .git folder
                return os.path.abspath(os.path.join(path, d))
        if os.path.dirname(path) == path:
            # At root, exit with error message
            sys.exit("Not inside a Git repository")
        # Not at root, continue search with parent directory
        path = os.path.join(path, os.pardir)


class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

if __name__ == '__main__':
    topo_order_commits()
