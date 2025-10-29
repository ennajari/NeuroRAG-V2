#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime
from github import Github, GithubException, Auth
from colorama import Fore, init
from dotenv import load_dotenv

init(autoreset=True)
load_dotenv()

print("\n=== GITHUB AUTOMATION - NeuroRAG V2.0 ===\n")

# Charger token
token = os.getenv('GITHUB_TOKEN')
username = os.getenv('GITHUB_USERNAME', 'ennjari')

if not token:
    print("ERREUR: GITHUB_TOKEN manquant dans .env")
    sys.exit(1)

# Connexion
try:
    auth = Auth.Token(token)
    g = Github(auth=auth)
    user = g.get_user()
    print(f"OK Connecte: {user.login}\n")
except Exception as e:
    print(f"ERREUR connexion: {e}")
    sys.exit(1)

# Charger config
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    print("OK Configuration chargee\n")
except Exception as e:
    print(f"ERREUR config.json: {e}")
    sys.exit(1)

repo_name = config['repo_name']
print(f"Repository a creer: {repo_name}")
print(f"Labels: {len(config['labels'])}")
print(f"Milestones: {len(config['milestones'])}")
total_issues = sum(len(m.get('issues', [])) for m in config['milestones'])
print(f"Issues: {total_issues}\n")

choice = input("Continuer? (o/n): ")
if choice.lower() != 'o':
    print("Annule")
    sys.exit(0)

# Créer repo
print("\n=== CREATION REPOSITORY ===\n")
try:
    try:
        repo = user.get_repo(repo_name)
        print(f"Repository existe deja: {repo.html_url}")
        reuse = input("Reutiliser? (o/n): ")
        if reuse.lower() != 'o':
            sys.exit(0)
    except:
        print(f"Creation de {repo_name}...")
        repo = user.create_repo(
            name=repo_name,
            description=config['repo_description'],
            private=False,
            has_issues=True,
            has_projects=True,
            auto_init=True
        )
        if config.get('topics'):
            repo.replace_topics(config['topics'])
        print(f"OK Cree: {repo.html_url}\n")
except Exception as e:
    print(f"ERREUR: {e}")
    sys.exit(1)

# Créer labels
print("=== CREATION LABELS ===\n")
for label in repo.get_labels():
    try:
        label.delete()
    except:
        pass

for label_data in config['labels']:
    try:
        repo.create_label(
            name=label_data['name'],
            color=label_data['color'],
            description=label_data.get('description', '')
        )
        print(f"OK Label: {label_data['name']}")
    except:
        pass

# Créer milestones et issues
print("\n=== CREATION MILESTONES & ISSUES ===\n")
for ms_data in config['milestones']:
    try:
        due = None
        if ms_data.get('due_date'):
            due = datetime.strptime(ms_data['due_date'], '%Y-%m-%d')
        
        milestone = repo.create_milestone(
            title=ms_data['title'],
            description=ms_data.get('description', ''),
            due_on=due
        )
        print(f"\nOK Milestone: {milestone.title}")
        
        if 'issues' in ms_data:
            for issue_data in ms_data['issues']:
                try:
                    labels = []
                    if 'labels' in issue_data:
                        labels = [repo.get_label(l) for l in issue_data['labels']]
                    
                    issue = repo.create_issue(
                        title=issue_data['title'],
                        body=issue_data['body'],
                        milestone=milestone,
                        labels=labels
                    )
                    print(f"  OK Issue #{issue.number}: {issue.title[:40]}...")
                except Exception as e:
                    print(f"  ERREUR issue: {e}")
    except Exception as e:
        print(f"ERREUR milestone: {e}")

print("\n=== TERMINE ===\n")
print(f"Repository: {repo.html_url}")
print(f"\nClone avec: git clone {repo.clone_url}")
print("\nBon developpement!\n")
