# Contributing to UXD Team Chatbot

Thanks for helping build a more connected Red Hat UXD team!  
This project powers a chatbot that indexes team bios using markdown + vector search.

If you're new to GitHub or want a full walkthrough, check out: LEARN_GIT.md

## Quick Contribution Flow

1. **Fork** the repo  
2. **Create a new branch**: `add-your-name`
3. **Create a folder** inside `bios/` named after yourself
4. **Add your `bio.md`** file using the [template below](#template)
5. **Commit + push** your changes
6. **Open a Pull Request** to `main`

## Bio Template

Create this file: `bios/your-name/bio.md`

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
Feel free to tag @justinxhale in your PR if you get stuck.