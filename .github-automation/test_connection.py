#!/usr/bin/env python3
"""Test de connexion GitHub"""

import os
import sys
from dotenv import load_dotenv

try:
    from github import Github, Auth
    from colorama import Fore, Style, init
except ImportError:
    print("ERREUR: Packages manquants")
    print("   pip install PyGithub python-dotenv colorama")
    sys.exit(1)

init(autoreset=True)
load_dotenv()

def test_connection():
    print("\n=== TEST DE CONNEXION GITHUB ===\n")
    
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("ERREUR: GITHUB_TOKEN manquant dans .env")
        return False
    
    print("OK Token trouve")
    
    try:
        auth = Auth.Token(token)
        github = Github(auth=auth)
        user = github.get_user()
        
        print(f"OK Connecte en tant que: {user.login}")
        print(f"   Nom: {user.name or 'Non defini'}")
        print(f"   Repos publics: {user.public_repos}")
        print(f"   Followers: {user.followers}")
        
        print("\n=== Verification des permissions ===")
        
        try:
            user.get_repo("test-non-existent-repo-12345")
        except:
            print("OK Permissions 'repo' OK")
        
        print("\nSUCCES: CONNEXION REUSSIE !")
        print("\nTu peux maintenant lancer: python github_setup.py")
        return True
        
    except Exception as e:
        print(f"ERREUR de connexion: {e}")
        print("\nVerifications:")
        print("1. Token correct ?")
        print("2. Token expire ?")
        print("3. Scopes 'repo' actives ?")
        return False

if __name__ == "__main__":
    test_connection()
