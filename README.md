# AP French Study Quiz (Python + Raspberry Pi + ChatGPT)

This project shows how to build your own AP French multiple choice study quiz using Python and a Raspberry Pi.  
All versions of the code inside this repo were generated using iterative prompts through ChatGPT.

[![AP French Study Quiz: Vibe Code Your Own Practice App](play-French%20AP%20Quiz-thumbnail.jpg)](https://youtu.be/usuw_jBj3vo)

## What This Project Does

This quiz helps you study for AP French using multiple choice questions.  
As you progress through each version, you will see:

- AP-style questions across vocabulary, grammar, culture, and reading comprehension  
- score tracking across questions  
- GUI built with Tkinter on Raspberry Pi OS  
- timer support to simulate test pressure  
- layout and UX improvements through each iteration  

This is a real example of “vibe coding” where you use AI to iterate your way into a better tool by giving targeted update prompts.

## Requirements

- Raspberry Pi (any recent version works)  
- Python 3 installed  
- Raspberry Pi OS Desktop  
- Geany Programmer’s Editor (preinstalled on Raspberry Pi OS Desktop)  
- Internet access to log in to ChatGPT (free tier works)
## How to Run

1) Clone or download this repo to your Raspberry Pi  
2) Open the version you want to run in Genie (or your editor of choice)  
3) Save the file with `.py` extension  
4) Click the “paper plane” run icon in Genie or run from terminal:

## Versions Inside This Repo

| Version File   | What Changed                                                                 |
|----------------|-------------------------------------------------------------------------------|
| `v1`           | First ChatGPT-generated AP French quiz (23 questions, basic Tkinter UI, optional timer)                   |
| `v2`           | Limited to 5 questions, fixed window size, 2x2 answer grid, minor layout cleanups        |
| `v3`           | Timer countdown displayed, automatic advance on timeout, improved end-of-quiz behavior  |

You can continue to build from any version.

---

## Ideas for Your Own Updates

This project is intended to be modified.  
Try these next:

- swap in your own AP French questions from class or your study guide
- add listening questions with attached audio files
- include explanations for each answer (in French or English)
- categorize questions (vocab, grammar, culture, reading) and let users pick a category
- tweak timer length for practice vs. “exam mode”
- log results to a file so you can track your progress over time

---

## How the Code Was Generated

Every version came from a single starting prompt to ChatGPT on a free account.

Then I asked for targeted upgrades over time:

- UI and layout fixes (window size, 2x2 answer buttons)
- timer behavior and countdown display
- score and feedback handling
- suggestions for future improvements (scrollable question area, study mode, etc.)

This shows how AI can be used to learn Python and AP French at the same time.

---

## 📚 Author
Created by **Caroline Dunn**  
- 🌐 [winningintech.com](https://winningintech.com/)  
- 📺 [YouTube.com/Caroline](https://www.youtube.com/caroline)  
- 📘 [A Woman’s Guide to Winning in Tech](https://amzn.to/3YxHVO7)  

---

## License

MIT License — you can use, remix, and modify this code for your own study tools.

If you build your own version, please share it!
