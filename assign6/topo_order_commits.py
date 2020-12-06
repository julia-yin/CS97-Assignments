'''
CS 97 Fall 2020 Assignment 6
Git Repository Organization: Topologically Ordered Commits
Julia Yin
'''

import os
import sys
import zlib

def topo_order_commits():
    branches_dict = dict()
    get_local_branches(branches_dict)


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
            print(b)
            print(b_hash)


def find_git_dir():
    # Get path to current directory
    path = os.path.abspath(os.curdir)

    # Search through cur and all parent directories for .git until root
    while True:
        for d in os.listdir(path):
            if (d == ".git"):
                # Return path to the .git folder
                print("abspath: " + os.path.abspath(os.path.join(path, d)))
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
