# Contributing to the UXD Team Chatbot
**New to GitHub? No problem. This guide will walk you through every step — no experience needed.**
**These instructions assume you are using MacOS**

Thanks for helping build a more connected Red Hat UXD team! This project creates a searchable, conversational chatbot based on our team bios (for now). Let’s keep it structured and scalable.
This is a GitHub-first, VS Code-powered UXD journey that gently introduces terminal work only when needed, while reinforcing GitHub-native flows.

## 1. Create a GitHub Account, Download VS Code, and Sign In
You’ll need a GitHub account and a code editor to contribute.
1. Create your GitHub account - **https://github.com/join**
2. Install Visual Studio Code (VS Code)
VS Code is the editor we’ll use to open and edit your files. - **https://code.visualstudio.com**
3. Sign in to VS Code with GitHub
When VS Code opens, sign in with your GitHub account — this helps you sync changes, commit code, and contribute directly.

## 2. Fork the UXD Team Chatbot Repo
This creates your own copy so you can safely edit without disrupting the main branch.
1. Navigate to **https://github.com/JustinXHale/uxd-team-chatbot**
2. Click **Fork**
3. Choose **owner** (probably yourself)
4. Give repo a name (or keep the same)
5. Click **create fork**

## 3. Create a Branch on GitHub
Branches let you make your changes without touching the main project. It’s a safe place to work on your bio before submitting it to be added.
1. From your fork click **Branch** (next to main)
2. Click **New branch**
3. Give the branch a **name** like "justin-ux-bio"
4. Click **Create new branch**

## 4. Clone your repo
1. From your repo click the **Code** dropdown, select the HTTPS tab and copy the code. It should look something like: **https://github.com/USERNAME/uxd-team-chatbot.git**
2. Open Mac Terminal 
3. Navigate to the directory the clone will save to
- If this is your first time in the terminal type **ls** to list your directories
- to change directories type **cd** the the directory name (ex: cd documents)
4. Run code
bash
```
git clone https://github.com/USERNAME/uxd-team-chatbot.git
```

## 5. Creating Directory & Bio
Though we can do this by simply navigating to the directory on the Mac and creating a new folder. Let’s use the terminal to create what we need — this gives you a chance to get comfortable with basic commands.
1. cd into your cloned repo 
bash 
```
cd uxd-team-chat
```
2. navigate to the bios directory 
bash 
```
cd bios
```
3. make your personal directory
bash
```
mkdir YOUR-NAME
```
4. Add bio.md
bash
```
touch YOUR-NAME/bio.md
```
5. Open your Markdown (md) in Visual Code Studio (VS Code)
bash
```
code bios/YOUR-NAME/bio.md
```

## 6. Change Branch and Add your Bio
1. Change to the branch you created in GitHub
- bottom left of the screen you should see something like 'uxd-tem-chatbot' (an icon) 'main'
- Click **main** and select the branch you created earlier. This ensures we will commit back to the right branch of our repo.
```yaml
1a. My branch isn't list
- Click the sync icon next to main to sync your local copy with Github
- - if it still doesnt display click 'main' then select 'Create new branch' and give it a name
```
2. Update your bio.md
Your bio should follow the same template below. You can copy and paste into vscode and change the needed information. This ensures our chatbot can read the information faster and easier.
3. Save

### Template
```yaml
---
name: Your Full Name
title: Your Title
start_date: Month Year
location: City, State
team: Your Team Name
email: you@email.com
github: yourgithubhandle
interests:
  - UX
  - Gardening
  - Dungeons & Dragons
bio: >
  Write a few sentences about yourself. This is used by the chatbot!
---
```

## 7. Commit back to your repo
Now that you are done saving, you need to put this information back on GitHub so that it can be merged with the main repo, and eventually ingested to the UXD Team Chatbot.
1. Select **Source Control** from the left panel (2nd Icon)
Here you can see every file that was changed since you've last synced.
2. Scroll over **Changes** and you will see a **+** icon (Stage all changes). Click it.
This is telling VS Code I want every file to be staged to be sent to GitHub, you can also select individual files.
3. Write a message in Commit **"adding justin's bio"**
This should be clear that if someone else reads it, they know what it is.
4. Click **Commit**. After that, click **Sync Changes** to push your commit back to GitHub.
Congratulations you just committed something back to your GitHub Repository!

## 8. Open a Pull Request (PR)
You're almost done! Now its time to create a PR to send it to the main repository.
1. Go to your forked repo on GitHub
2. You’ll see a **Compare & pull** request button — click it
3. Make sure the base is main from the original repo
4. Click **Create pull request**
5. Leave a helpful note like **“Adding Justin’s UXD bio”**

THATS IT. Your bio will be reviewed and added to the UXD chatbot on merge.

✅ Helpful Reminders
- Don’t edit anyone else's folder or script files
- Don’t commit .venv/ or other system files
- .DS_Store and .cache.json are ignored by default

Thanks again for being part of the project!

If you have questions or run into trouble, open an issue or tag @justinxhale in your PR.
