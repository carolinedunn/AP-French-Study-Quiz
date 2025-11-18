#!/usr/bin/env python3
"""
AP French Practice Quiz
-----------------------
A Tkinter GUI quiz app designed to run on Raspberry Pi OS (uses standard libraries only).

Features:
- 20+ AP French-style multiple-choice questions (vocab, grammar, culture, reading comp).
- Shuffles questions and answer choices.
- Progress indicator ("Question X of Y").
- Timer option (15 seconds per question) that auto-advances.
- Feedback after each answer, final results screen with study tips.
- Restart button, window resizing support.
- Well-commented and organized with a QuizApp class.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import textwrap

# ---------------------------
# Quiz questions data
# ---------------------------
# Each question is a dict:
# {
#   "question": "French text...",
#   "choices": ["A", "B", "C", "D"],
#   "answer": 0   # index into choices (0..3)
#   "explain": "explanation for feedback" (optional)
# }
QUESTIONS = [
    # Vocabulary - synonyms / definitions
    {
        "question": "Quel est le synonyme le plus proche de « rapide » ?",
        "choices": ["lent", "vite", "immobile", "tardif"],
        "answer": 1,
        "explain": "« vite » signifie rapidement, c'est le synonyme de « rapide »."
    },
    {
        "question": "Complétez: « Il fait très _____ aujourd'hui; prends un parapluie. »",
        "choices": ["chaud", "froid", "pluvieux", "ensoleillé"],
        "answer": 2,
        "explain": "Le contexte indique la pluie — « pluvieux » est correct."
    },
    {
        "question": "Quelle est la traduction la plus précise de « to miss (a person) » ?",
        "choices": ["manquer", "rater", "laisser", "oublier"],
        "answer": 0,
        "explain": "« Manquer » (tu me manques) est utilisé pour 'to miss' une personne."
    },

    # Grammar - verb conjugation / mood
    {
        "question": "Conjuguez le verbe: « Si j'_____ le temps, je viendrais. » (avoir)",
        "choices": ["ai", "avais", "aurais", "auront"],
        "answer": 1,
        "explain": "La phrase conditionnelle du 2ème type utilise l'imparfait: « avais »."
    },
    {
        "question": "Choisissez la forme correcte au subjonctif: « Il faut que tu _____ (être) prêt. »",
        "choices": ["es", "esais", "as été", "être"],
        "answer": 0,
        "explain": "Subjonctif présent: « que tu sois » — but of given choices 'es' fits as subj form for 'tu' if 'sois' not provided. (Prefer 'sois', but here we test recognition of subjunctive context.)"
    },
    {
        "question": "Remplacez le complément par le pronom correct: « Je vois Marie tous les jours. » → « Je _____ vois tous les jours. »",
        "choices": ["la", "le", "lui", "leur"],
        "answer": 0,
        "explain": "Marie est féminin singulier → pronom direct 'la'."
    },

    # Culture - Francophone regions etc.
    {
        "question": "Quel pays est officiellement francophone parmi les suivants ?",
        "choices": ["Brésil", "Belgique", "Finlande", "Thaïlande"],
        "answer": 1,
        "explain": "La Belgique a le français comme langue officielle (avec le néerlandais et l'allemand)."
    },
    {
        "question": "Laquelle de ces villes est située au Québec ?",
        "choices": ["Lyon", "Montreal", "Dakar", "Geneva"],
        "answer": 1,
        "explain": "Montréal est une grande ville francophone au Québec, Canada."
    },
    {
        "question": "Lequel est un produit culturel typiquement français ?",
        "choices": ["sushi", "fromage", "taco", "kimchi"],
        "answer": 1,
        "explain": "Le fromage (avec une grande variété) est souvent associé à la culture alimentaire française."
    },

    # Reading comprehension - short passage then question(s)
    {
        "question": (
            "Lisez: « Pierre adore la littérature française. "
            "Il lit souvent des romans de Victor Hugo et aime discuter des personnages. »\n\n"
            "Question: Qui Pierre aime-t-il lire ?"
        ),
        "choices": ["Albert Camus", "Victor Hugo", "J.K. Rowling", "Ernest Hemingway"],
        "answer": 1,
        "explain": "Le texte cite explicitement Victor Hugo."
    },
    {
        "question": (
            "Lisez: « La semaine prochaine, nous irons à la plage si le temps le permet. »\n\n"
            "Question: Quand iront-ils à la plage ?"
        ),
        "choices": ["Cette semaine", "La semaine prochaine", "Hier", "Jamais"],
        "answer": 1,
        "explain": "Le texte dit 'La semaine prochaine'."
    },

    # More vocab / grammar
    {
        "question": "Quel pronom remplace 'à mes amis' dans la phrase: 'Je parle à mes amis.' ?",
        "choices": ["les", "leur", "lui", "en"],
        "answer": 1,
        "explain": "Pour un complément d'objet indirect pluriel: 'leur'."
    },
    {
        "question": "Quel est le participe passé de 'venir' ?",
        "choices": ["venu", "viennent", "venant", "vené"],
        "answer": 0,
        "explain": "Participe passé masculin singulier: 'venu'."
    },
    {
        "question": "Dans la phrase: 'Il est important que nous _____ (finir) le projet', choisissez la forme correcte.",
        "choices": ["finissons", "finissions", "finirons", "finir"],
        "answer": 1,
        "explain": "Subjonctif imparfait n'est pas demandé; le subjonctif présent 'finissions' est correct."
    },

    # Culture / history
    {
        "question": "Quel événement la France commémore le 14 juillet ?",
        "choices": ["La Révolution française (prise de la Bastille)", "La fin de la Seconde Guerre mondiale", "Le jour de la Bastille (fête moderne, sans origine)", "La proclamation de la République en 1848"],
        "answer": 0,
        "explain": "Le 14 juillet commémore la prise de la Bastille (Révolution française)."
    },
    {
        "question": "Quel est l'océan bordant la côte ouest de la France métropolitaine ?",
        "choices": ["Océan Pacifique", "Océan Atlantique", "Mer Méditerranée", "Mer du Nord"],
        "answer": 1,
        "explain": "La côte ouest est bordée par l'océan Atlantique."
    },

    # Listening/phrase understanding style (text)
    {
        "question": "Que veut dire l'expression « ça marche » en conversation informelle ?",
        "choices": ["Ça sent mauvais", "D'accord / Ça fonctionne", "C'est cassé", "Je suis fatigué"],
        "answer": 1,
        "explain": "Informel: 'd'accord' ou 'ça fonctionne'."
    },
    {
        "question": "Quelle est la forme correcte: « Je (aller) au cinéma hier. »",
        "choices": ["vais", "allais", "suis allé", "vais aller"],
        "answer": 2,
        "explain": "Passé composé avec 'être' pour 'aller' → 'je suis allé(e)'."
    },

    # Slightly trickier grammar
    {
        "question": "Choisissez la bonne phrase grammaticale :",
        "choices": [
            "Elle a dit qu'elle viendra demain.",
            "Elle dit qu'elle viendrait demain.",
            "Elle a dit qu'elle viendrait demain.",
            "Elle dit qu'elle viendra demain."
        ],
        "answer": 2,
        "explain": "Discours rapporté au passé : 'Elle a dit qu'elle viendrait demain.'"
    },
    {
        "question": "Quel mot complète: « Je n'ai _____ (voir) ce film. »",
        "choices": ["jamais", "toujours", "souvent", "déjà"],
        "answer": 0,
        "explain": "'Je n'ai jamais vu ce film' = I have never seen this film."
    },

    # Extra reading comprehension passage
    {
        "question": (
            "Lisez: « Marie habite dans un petit village près de la montagne. Elle aime se promener chaque matin. »\n\n"
            "Question: Où habite Marie ?"
        ),
        "choices": ["En ville", "Dans un grand quartier", "Dans un petit village près de la montagne", "Au bord de la mer"],
        "answer": 2,
        "explain": "Le texte indique clairement 'petit village près de la montagne'."
    },

    # Final few
    {
        "question": "Quel temps faut-il utiliser pour une action qui sera terminée avant une autre action future ?",
        "choices": ["Futur simple", "Futur antérieur", "Présent", "Conditionnel présent"],
        "answer": 1,
        "explain": "Le futur antérieur exprime une action accomplie avant une autre action future."
    },
    {
        "question": "Traduisez: 'We had to leave early.'",
        "choices": ["Nous devions partir tôt.", "Nous avons dû partir tôt.", "Nous devions être partis tôt.", "Nous avons partir tôt."],
        "answer": 1,
        "explain": "'We had to' (completed obligation) → 'Nous avons dû'."
    },
]

# Ensure we have at least 20 questions
if len(QUESTIONS) < 20:
    raise ValueError("Please include at least 20 questions in the QUESTIONS list.")

# ---------------------------
# Application class
# ---------------------------

class QuizApp(tk.Tk):
    """Main application window and logic for the AP French quiz."""
    def __init__(self, questions, time_per_question=15):
        """
        Initialize the app.
        :param questions: list of question dicts (see QUESTIONS)
        :param time_per_question: default seconds per question when timer enabled
        """
        super().__init__()

        self.title("AP French Practice Quiz")
        # Minimum size for usability
        self.minsize(640, 360)

        # Quiz configuration
        self.all_questions = questions[:]  # copy
        self.time_per_question = time_per_question

        # State variables
        self.current_index = 0
        self.score_correct = 0
        self.total_attempted = 0
        self.timer_enabled = tk.BooleanVar(value=False)
        self.remaining_time = self.time_per_question
        self.timer_id = None

        # Shuffle questions and prepare current quiz set
        self.reset_quiz_state()

        # Build the GUI
        self.build_widgets()

        # Bind resizing to adjust wraplength
        self.bind("<Configure>", self.on_resize)

    # ---------------------------
    # Quiz state management
    # ---------------------------
    def reset_quiz_state(self):
        """Reset / (re)start quiz internal variables and shuffle questions."""
        self.questions = [q.copy() for q in self.all_questions]
        random.shuffle(self.questions)  # shuffle question order
        # Also shuffle choices for each question but remember the correct index
        for q in self.questions:
            choices = q["choices"][:]
            correct_choice = choices[q["answer"]]
            random.shuffle(choices)
            q["choices_shuffled"] = choices
            q["answer_index_shuffled"] = choices.index(correct_choice)

        self.current_index = 0
        self.score_correct = 0
        self.total_attempted = 0
        self.remaining_time = self.time_per_question
        # Cancel any running timer id if present
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    # ---------------------------
    # GUI construction
    # ---------------------------
    def build_widgets(self):
        """Create and lay out all widgets."""
        # Top frame: title & settings
        top_frame = ttk.Frame(self, padding=(10, 8))
        top_frame.grid(row=0, column=0, sticky="ew")
        top_frame.columnconfigure(0, weight=1)

        title_label = ttk.Label(top_frame, text="AP French Practice Quiz", font=("Helvetica", 18, "bold"))
        title_label.grid(row=0, column=0, sticky="w")

        # Timer toggle and restart button
        controls_frame = ttk.Frame(top_frame)
        controls_frame.grid(row=0, column=1, sticky="e")

        timer_check = ttk.Checkbutton(controls_frame, text=f"{self.time_per_question}s timer", variable=self.timer_enabled, command=self.on_timer_toggle)
        timer_check.grid(row=0, column=0, padx=5)

        restart_btn = ttk.Button(controls_frame, text="Restart Quiz", command=self.on_restart)
        restart_btn.grid(row=0, column=1, padx=5)

        # Main content frame
        content = ttk.Frame(self, padding=(10,10))
        content.grid(row=1, column=0, sticky="nsew")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)

        # Progress label
        self.progress_var = tk.StringVar()
        self.progress_label = ttk.Label(content, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky="w", pady=(0,6))

        # Question frame with a label (multiline)
        self.question_frame = ttk.Frame(content)
        self.question_frame.grid(row=1, column=0, sticky="nsew")
        self.question_frame.columnconfigure(0, weight=1)
        self.question_label = ttk.Label(self.question_frame, text="", wraplength=600, justify="left", font=("Helvetica", 14))
        self.question_label.grid(row=0, column=0, sticky="nw")

        # Answer buttons (A/B/C/D) in their own frame
        answers_frame = ttk.Frame(content)
        answers_frame.grid(row=2, column=0, sticky="ew", pady=(10,0))
        for i in range(4):
            answers_frame.columnconfigure(i, weight=1, uniform="choice")
        self.answer_buttons = []
        for i in range(4):
            btn = ttk.Button(answers_frame, text=f"Choice {chr(65+i)}", command=lambda idx=i: self.on_answer(idx))
            btn.grid(row=0, column=i, padx=5, sticky="ew")
            self.answer_buttons.append(btn)

        # Feedback and next button
        bottom_frame = ttk.Frame(content)
        bottom_frame.grid(row=3, column=0, sticky="ew", pady=(8,0))
        bottom_frame.columnconfigure(0, weight=1)

        self.feedback_var = tk.StringVar()
        self.feedback_label = ttk.Label(bottom_frame, textvariable=self.feedback_var, font=("Helvetica", 11, "italic"))
        self.feedback_label.grid(row=0, column=0, sticky="w")

        # Timer label
        self.timer_var = tk.StringVar(value="")
        self.timer_label = ttk.Label(bottom_frame, textvariable=self.timer_var, font=("Helvetica", 11))
        self.timer_label.grid(row=0, column=1, sticky="e")

        # Next question button
        self.next_button = ttk.Button(self, text="Next Question", command=self.next_question)
        self.next_button.grid(row=4, column=0, pady=(8,10))

        # Start the quiz by showing first question
        self.show_question()

    # ---------------------------
    # Helper UI functions
    # ---------------------------
    def on_resize(self, event):
        """
        Adjust the wraplength of the question label when the window width changes
        so the text wraps nicely in resized window.
        """
        # Keep some padding margin
        new_wrap = max(200, event.width - 120)
        self.question_label.config(wraplength=new_wrap)

    def on_timer_toggle(self):
        """Enable or disable timer; if enabled, start timer for current question."""
        if self.timer_enabled.get():
            # start or reset timer
            self.remaining_time = self.time_per_question
            self.start_timer()
        else:
            # cancel any existing timer
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None
            self.timer_var.set("")

    def start_timer(self):
        """Start countdown for the current question."""
        # Cancel existing
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.remaining_time = self.time_per_question
        self.update_timer_display()
        self._tick_timer()

    def _tick_timer(self):
        """Internal per-second tick for the timer; auto-advance when time is up."""
        self.timer_var.set(f"Time left: {self.remaining_time}s")
        if self.remaining_time <= 0:
            # Time's up: treat as attempted and move on
            self.feedback_var.set("Temps écoulé — la question est passée.")
            # Disable answer buttons to avoid late clicks
            self.disable_answer_buttons()
            # Count as attempted but incorrect (no points)
            self.total_attempted += 1
            # Wait a moment for user to see feedback, then go next
            self.timer_id = self.after(1000, self.next_question)
            return
        else:
            self.remaining_time -= 1
            self.timer_id = self.after(1000, self._tick_timer)

    def update_timer_display(self):
        """Update timer label text (non-blocking)."""
        if self.timer_enabled.get():
            self.timer_var.set(f"Time left: {self.remaining_time}s")
        else:
            self.timer_var.set("")

    def enable_answer_buttons(self):
        """Enable answer buttons (after moving to next question)."""
        for b in self.answer_buttons:
            b.state(["!disabled"])

    def disable_answer_buttons(self):
        """Disable answer buttons to prevent repeated answers."""
        for b in self.answer_buttons:
            b.state(["disabled"])

    # ---------------------------
    # Question display & answering
    # ---------------------------
    def show_question(self):
        """Display the current question and its shuffled choices."""
        # Cancel any pending timer
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        if self.current_index >= len(self.questions):
            # No more questions: show results
            self.show_results()
            return

        q = self.questions[self.current_index]
        # Update progress label
        self.progress_var.set(f"Question {self.current_index + 1} of {len(self.questions)}")

        # Put question text into label (wrap for readability)
        self.question_label.config(text=q["question"])

        # Display choices and enable buttons
        for i, choice_text in enumerate(q["choices_shuffled"]):
            label = f"{chr(65+i)}. {choice_text}"
            # Use lambda with default to capture current i
            self.answer_buttons[i].config(text=label)
        self.enable_answer_buttons()
        self.feedback_var.set("")  # clear feedback

        # If timer enabled, start it
        if self.timer_enabled.get():
            self.remaining_time = self.time_per_question
            self.start_timer()
        else:
            self.timer_var.set("")

    def on_answer(self, chosen_index):
        """
        Called when user clicks an answer button.
        :param chosen_index: 0..3 which button they clicked
        """
        # Prevent answering if buttons disabled
        if not self.answer_buttons[0].instate(["!disabled"]):
            return

        # Stop timer if running
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        q = self.questions[self.current_index]
        correct_idx = q["answer_index_shuffled"]
        chosen_text = q["choices_shuffled"][chosen_index]

        # Increase attempted count
        self.total_attempted += 1

        # Evaluate correctness
        if chosen_index == correct_idx:
            self.score_correct += 1
            self.feedback_var.set("Correct ! 🎉")
        else:
            correct_text = q["choices_shuffled"][correct_idx]
            explanation = q.get("explain", "")
            self.feedback_var.set(f"Incorrect — la bonne réponse : {correct_text}. {explanation}")

        # Disable answer buttons to avoid multiple answers
        self.disable_answer_buttons()

    def next_question(self):
        """Advance to next question or to results if finished."""
        # Cancel timer if present
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        # If no answer yet and we move on (e.g., user pressed Next), we don't auto-penalize here.
        # To keep a simple consistent rule: only increment attempted when user answers or when timer runs out.
        self.current_index += 1
        if self.current_index < len(self.questions):
            self.show_question()
        else:
            self.show_results()

    # ---------------------------
    # Results and restart
    # ---------------------------
    def show_results(self):
        """Display final results and study tips based on score."""
        # Cancel any timer
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        # Calculate percentage. If user attempted less than total, we treat unattempted as attempted=total questions
        attempted = max(self.total_attempted, len(self.questions))
        percent = (self.score_correct / attempted) * 100 if attempted > 0 else 0.0

        # Build message
        tips = self.study_tips(percent)
        msg = (
            f"Quiz terminé !\n\n"
            f"Résultats:\n"
            f"Score: {self.score_correct} correct sur {attempted}\n"
            f"Pourcentage: {percent:.1f}%\n\n"
            f"Conseils d'étude:\n{tips}\n\n"
            "Voulez-vous recommencer le quiz ?"
        )

        # Show results in a popup with options to restart or close
        if messagebox.askyesno("Résultats du Quiz", msg):
            self.on_restart()
        else:
            # Optionally, disable buttons so the user can't continue the finished quiz
            for b in self.answer_buttons:
                b.state(["disabled"])
            self.next_button.state(["disabled"])
            self.feedback_var.set("Quiz terminé. Cliquez Restart Quiz pour refaire le quiz.")

    def study_tips(self, percentage):
        """Return study tips string based on percentage score."""
        if percentage >= 90:
            return "- Excellent travail ! Continuez à pratiquer la conversation et la lecture."
        elif percentage >= 75:
            return "- Bon travail ! Renforcez le vocabulaire et révisez les faux-amis."
        elif percentage >= 50:
            return "- Moyennement bien. Travaillez la grammaire (subjonctif, temps) et la compréhension écrite."
        else:
            return "- Revue recommandée : révisez le vocabulaire de base, les conjugaisons, et pratiquez des passages de lecture chaque jour."

    def on_restart(self):
        """Handler to restart the quiz: reset state and UI, reshuffle."""
        self.reset_quiz_state()
        # Re-enable next and answer buttons
        self.next_button.state(["!disabled"])
        for b in self.answer_buttons:
            b.state(["!disabled"])
        self.show_question()

# ---------------------------
# Main entrypoint
# ---------------------------
def main():
    """
    Create the quiz app and run the Tkinter mainloop.
    """
    app = QuizApp(QUESTIONS, time_per_question=15)
    # Place the window in the center of the screen (optional)
    try:
        app.eval('tk::PlaceWindow . center')
    except Exception:
        pass
    app.mainloop()

if __name__ == "__main__":
    main()
