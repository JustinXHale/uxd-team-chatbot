# UXD Team Chatbot

This is a team knowledge project for Red Hat's UXD organization. It allows contributors to add Markdown bios and makes them searchable using semantic search.

## 👥 Contribute Your Bio

To add yourself to the chatbot:

1. Fork this repo
2. Create a new folder inside `bios/` using your name
3. Add a `bio.md` using [our template](./CONTRIBUTING.md)
4. Submit a Pull Request

That’s it! You’ll be searchable in our CLI chatbot.

---

## 🧪 Maintainers

To re-embed team bios:

```bash
python embed_bios.py --reset
