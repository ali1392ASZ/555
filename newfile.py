from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.text import LabelBase
from kivy.clock import Clock
import random

# ثبت فونت Traditional Arabic
LabelBase.register(name='TradArabic', fn_regular='trado.ttf')

class MathGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.score = 0
        self.question_count = 0
        self.max_questions = 10
        self.time_limit = 7  # ثانیه
        self.timer_event = None

        # نمایش سوال
        self.question_label = Label(
            text='',
            font_name='TradArabic',
            font_size=32,
            halign='right',
            text_size=(600, None)
        )
        self.add_widget(self.question_label)

        # دکمه‌های گزینه‌ها
        self.buttons = []
        for _ in range(4):
            btn = Button(
                font_name='TradArabic',
                font_size=24,
                halign='right',
                text_size=(600, None)
            )
            btn.bind(on_press=self.check_answer)
            self.buttons.append(btn)
            self.add_widget(btn)

        # نمایش امتیاز
        self.score_label = Label(
            text='امتیاز: 0',
            font_name='TradArabic',
            font_size=24,
            halign='right',
            text_size=(600, None)
        )
        self.add_widget(self.score_label)

        # نمایش تایمر
        self.timer_label = Label(
            text='زمان باقی‌مانده: 7',
            font_name='TradArabic',
            font_size=20,
            halign='right',
            text_size=(600, None)
        )
        self.add_widget(self.timer_label)

        self.generate_question()

    def generate_question(self):
        if self.question_count >= self.max_questions:
            self.end_game("🎉 پایان بازی! امتیاز نهایی: " + str(self.score))
            return

        while True:
            a = random.randint(2, 20)
            b = random.randint(1, 10)
            op = random.choice(['+', '-', '*', '/'])
            if op == '/':
                if a % b != 0:
                    continue  # فقط تقسیم‌های صحیح
            break

        self.question = f"{a} {op} {b}"
        self.answer = int(eval(self.question))
        options = [self.answer + i for i in [-2, -1, 0, 1]]
        random.shuffle(options)

        self.question_label.text = self.question
        for i, btn in enumerate(self.buttons):
            btn.text = str(options[i])
            btn.disabled = False

        self.score_label.text = f"امتیاز: {self.score}"
        self.question_count += 1
        self.start_timer()

    def check_answer(self, instance):
        if int(instance.text) == self.answer:
            self.score += 1
        else:
            self.score = max(0, self.score - 1)
        self.stop_timer()
        self.generate_question()

    def start_timer(self):
        self.remaining_time = self.time_limit
        self.timer_label.text = f"زمان باقی‌مانده: {self.remaining_time}"
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.remaining_time -= 1
        self.timer_label.text = f"زمان باقی‌مانده: {self.remaining_time}"
        if self.remaining_time <= 0:
            self.stop_timer()
            self.end_game("⏰ زمان تمام شد! بازی پایان یافت.")

    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

    def end_game(self, message):
        self.question_label.text = message
        for btn in self.buttons:
            btn.disabled = True
            btn.text = ''
        self.timer_label.text = ''
        self.score_label.text = f"امتیاز نهایی: {self.score}"

class MathApp(App):
    def build(self):
        return MathGame()

if __name__ == '__main__':
    MathApp().run()