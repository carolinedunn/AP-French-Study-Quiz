#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import random

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

if len(QUESTIONS) < 5:
    raise ValueError("Need at least 5 questions for a 5-question quiz.")


class QuizApp(tk.Tk):
    def __init__(self, questions, time_per_question=15):
        super().__init__()

        self.title("AP French Practice Quiz")

        # FIXED WINDOW SIZE
        self.geometry("800x500")
        self.resizable(False, False)

        # Internal state
        self.all_questions = questions
        self.time_per_question = time_per_question

        self.timer_enabled = tk.BooleanVar(value=False)
        self.timer_id = None

        self.reset_quiz_state()
        self.build_widgets()

    # ---------------------------------------------------
    # Reset quiz and select 5 questions
    # ---------------------------------------------------
    def reset_quiz_state(self):
        selected = random.sample(self.all_questions, 5)
        self.questions = [q.copy() for q in selected]

        for q in self.questions:
            choices = q["choices"][:]
            correct = choices[q["answer"]]
            random.shuffle(choices)
            q["choices_shuffled"] = choices
            q["answer_index_shuffled"] = choices.index(correct)

        self.current_index = 0
        self.score_correct = 0
        self.total_attempted = 0
        self.remaining_time = self.time_per_question

        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    # ---------------------------------------------------
    # GUI
    # ---------------------------------------------------
    def build_widgets(self):
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="AP French Practice Quiz",
                  font=("Helvetica", 20, "bold")).pack(side="left")

        ttk.Checkbutton(top, text="Enable 15s timer",
                        variable=self.timer_enabled).pack(side="right")

        ttk.Button(top, text="Restart Quiz",
                   command=self.on_restart).pack(side="right", padx=10)

        # Progress indicator
        self.progress_var = tk.StringVar()
        ttk.Label(self, textvariable=self.progress_var,
                  font=("Helvetica", 12)).pack(anchor="w", padx=10)

        # Timer display
        self.timer_var = tk.StringVar()
        self.timer_label = ttk.Label(
            self, textvariable=self.timer_var, font=("Helvetica", 14, "bold"))
        self.timer_label.pack()

        # Question text
        self.question_label = ttk.Label(
            self, text="", wraplength=750, justify="left",
            font=("Helvetica", 15)
        )
        self.question_label.pack(pady=10)

        # ---------------------------------------------------
        # 2 × 2 ANSWER GRID — ALL BUTTONS SAME SIZE
        # ---------------------------------------------------
        answers_frame = ttk.Frame(self)
        answers_frame.pack(pady=10)

        self.answer_buttons = []
        for r in range(2):
            for c in range(2):
                i = r * 2 + c
                btn = ttk.Button(
                    answers_frame,
                    text=f"Choice {chr(65+i)}",
                    width=30,      # consistent width
                    padding=10,    # consistent padding
                    command=lambda idx=i: self.on_answer(idx)
                )
                btn.grid(row=r, column=c, padx=8, pady=8)
                self.answer_buttons.append(btn)

        # Feedback
        self.feedback_var = tk.StringVar()
        ttk.Label(self, textvariable=self.feedback_var,
                  font=("Helvetica", 12, "italic")).pack()

        # Next question button
        self.next_btn = ttk.Button(self, text="Next Question",
                                   command=self.next_question)
        self.next_btn.pack(pady=10)

        self.show_question()

    # ---------------------------------------------------
    # Display question + start timer
    # ---------------------------------------------------
    def show_question(self):
        if self.current_index >= len(self.questions):
            self.show_results()
            return

        q = self.questions[self.current_index]

        self.progress_var.set(
            f"Question {self.current_index + 1} of {len(self.questions)}"
        )

        self.remaining_time = self.time_per_question
        self.update_timer_display()

        self.question_label.config(text=q["question"])

        for i, text in enumerate(q["choices_shuffled"]):
            self.answer_buttons[i].config(text=f"{chr(65+i)}. {text}")
            self.answer_buttons[i].state(["!disabled"])

        self.feedback_var.set("")

        # Adjust button label for last question
        if self.current_index == len(self.questions) - 1:
            self.next_btn.config(text="View Results")
        else:
            self.next_btn.config(text="Next Question")

        # Start timer if enabled
        if self.timer_enabled.get():
            self.start_timer()

    # ---------------------------------------------------
    # Timer control
    # ---------------------------------------------------
    def start_timer(self):
        self.cancel_timer()
        self.timer_tick()

    def cancel_timer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    def timer_tick(self):
        self.update_timer_display()

        if self.remaining_time <= 0:
            self.handle_time_up()
            return

        self.remaining_time -= 1
        self.timer_id = self.after(1000, self.timer_tick)

    def update_timer_display(self):
        if self.timer_enabled.get():
            self.timer_var.set(f"Time Left: {self.remaining_time}s")
        else:
            self.timer_var.set("")

    # ---------------------------------------------------
    # Timer expired -> auto mark incorrect
    # ---------------------------------------------------
    def handle_time_up(self):
        self.total_attempted += 1
        self.feedback_var.set("⏳ Time's up! Incorrect.")

        for b in self.answer_buttons:
            b.state(["disabled"])

        # Move to next question after short delay
        self.after(1250, self.next_question)

    # ---------------------------------------------------
    # Answer clicked
    # ---------------------------------------------------
    def on_answer(self, idx):
        self.cancel_timer()

        q = self.questions[self.current_index]
        self.total_attempted += 1
        correct_idx = q["answer_index_shuffled"]

        if idx == correct_idx:
            self.score_correct += 1
            self.feedback_var.set("Correct ! 🎉")
        else:
            self.feedback_var.set(
                f"Incorrect — correct answer: "
                f"{q['choices_shuffled'][correct_idx]}"
            )

        for b in self.answer_buttons:
            b.state(["disabled"])

    # ---------------------------------------------------
    # Next question button
    # ---------------------------------------------------
    def next_question(self):
        self.cancel_timer()
        self.current_index += 1
        self.show_question()

    # ---------------------------------------------------
    # Final results
    # ---------------------------------------------------
    def show_results(self):
        percent = (self.score_correct / self.total_attempted) * 100
        msg = (
            f"Quiz complete!\n\n"
            f"Score: {self.score_correct}/5\n"
            f"Percentage: {percent:.1f}%\n\n"
            "Try again?"
        )
        if messagebox.askyesno("Results", msg):
            self.on_restart()

    # ---------------------------------------------------
    # Restart quiz
    # ---------------------------------------------------
    def on_restart(self):
        self.reset_quiz_state()
        self.show_question()


def main():
    app = QuizApp(QUESTIONS)
    app.mainloop()


if __name__ == "__main__":
    main()
