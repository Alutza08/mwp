from kivy.app import App
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

text_color = (2/255, 200/255, 214/255, 1)
text_input_background = (140/255, 6/255, 6/255, 1)
text_input_foreground = (0/255, 0/255, 0/255, 1)


def my_label(text):
    return Label(
        text=text,
        font_size=28,
        color=text_color,
        halign="center"
    )

def my_text_input(hint, is_int=False):
    return TextInput(
        hint_text=hint,
        font_size=20,
        size_hint=(1, 0.4),
        multiline=False,
        input_filter="int" if is_int else None,
        background_color = text_input_background,
        foreground_color = text_input_foreground,
        hint_text_color = text_color
    )

def calc_rufier(p1, p2, p3):
    return round((p1 + p2 + p3 - 200) / 10, 1)


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(my_label(text="Ця програма дозволить вам пройти тест Руф'є.\nВведіть ім’я та вік:"))

        self.name_input = my_text_input("Ім'я")
        self.age_input = my_text_input("Вік", True)

        layout.add_widget(self.name_input)
        layout.add_widget(self.age_input)

        btn = Button(text="Почати")
        btn.bind(on_press=self.next_screen)
        layout.add_widget(btn)

        self.add_widget(layout)

    def next_screen(self, instance):
        if self.name_input.text == "" or self.age_input == "":
            if self.name_input.text == "":
                self.name_input.hint_text = "Введіть ім'я обов'язково!!!"
                self.name_input.hint_text_color = (1, 0, 0, 1)
            if self.age_input.text == "":
                self.age_input.hint_text = "Введіть вік обов'язково!!!"
                self.age_input.hint_text_color = (1, 0, 0, 1)
            return
        app = App.get_running_app()
        app.user_name = self.name_input.text
        app.user_age = int(self.age_input.text)
        app.sm.current = 'second'


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_time= 1
        self.elapsed = self.total_time

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(my_label(text="Виміряйте пульс за 15 секунд\nВведіть результат нижче:"))

        self.progress = ProgressBar(max=self.total_time)
        layout.add_widget(self.progress)

        self.p1_input = my_text_input("Пульс", True)
        layout.add_widget(self.p1_input)

        self.btn = Button(text="Розпочати")
        self.btn.bind(on_press=self.start_timer)
        layout.add_widget(self.btn)

        self.add_widget(layout)
        self.p1_input.disabled = True
    def start_timer(self, instance):
        self.btn.disabled = True
        Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        if self.elapsed > 0:
            self.elapsed -= 1
            self.progress.value = self.elapsed
        else:
            self.btn.disabled = False
            self.p1_input.disabled = False
            self.btn.text = "Продовжити"
            Clock.unschedule(self.update_timer)
            self.btn.unbind(on_press=self.start_timer)
            self.btn.bind(on_press=self.next_screen)

    def next_screen(self, instance):
        if self.p1_input.text == "":
            self.p1_input.hint_text = "Введіть пульс обов'язково!!!"
            self.p1_input.hint_text_color = (1, 0, 0, 1)
            return
        App.get_running_app().p1 = int(self.p1_input.text)
        App.get_running_app().sm.current = 'third'


class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(my_label(text="Виконайте 30 присідань за 45 секунд"))
        self.total_time= 1
        self.elapsed = self.total_time


        self.progress = ProgressBar(max=self.total_time)
        layout.add_widget(self.progress)

        self.btn = Button(text="Розпочати")
        self.btn.bind(on_press=self.start_timer)
        layout.add_widget(self.btn)

        self.add_widget(layout)

    def start_timer(self, instance):
        self.btn.disabled = True
        Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        if self.elapsed > 0:
            self.elapsed -= 1
            self.progress.value = self.elapsed
        else:
            self.btn.disabled = False
            self.btn.text = "Продовжити"
            Clock.unschedule(self.update_timer)
            self.btn.unbind(on_press=self.start_timer)
            self.btn.bind(on_press=self.next_screen)

    def next_screen(self, instance):
        App.get_running_app().sm.current = 'fourth'


class FourthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_time = 1
        self.elapsed = self.total_time
        self.step = 1
        self.next = True

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(my_label(
            text="Після присідань:\n- Заміряйте пульс за перші 15 секунд\n- Потім 15 секунд відпочинку\n- І знову пульс 15 секунд"))

        self.p2_input = my_text_input("Перший пульс", True)
        self.p3_input = my_text_input("Другий пульс", True)

        layout.add_widget(self.p2_input)
        layout.add_widget(self.p3_input)

        self.progress = ProgressBar(max=self.total_time)
        layout.add_widget(self.progress)

        self.btn = Button(text="Розпочати")
        self.btn.bind(on_press=self.start_timer)
        layout.add_widget(self.btn)

        self.add_widget(layout)
        self.p2_input.disabled = True
        self.p3_input.disabled = True
    def start_timer(self, instance):
        if self.step == 2 and self.p2_input.disabled == False:
            if self.p2_input.text == "":
                self.p2_input.hint_text = "Введіть пульс обов'язково!!!"
                self.p2_input.hint_text_color = (1, 0, 0, 1)
                return
        self.btn.disabled = True
        self.p2_input.disabled = True
        self.p3_input.disabled = True
        self.next = True
        self.elapsed = self.total_time
        Clock.unschedule(self.update_timer)
        Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        if self.elapsed > 0:
            self.elapsed -= 1
            self.progress.value = self.elapsed
        elif self.step == 1 and self.next:
            self.btn.disabled = False
            self.p2_input.disabled = False
            self.btn.text = "Розпочати"
            self.step = 2
            self.next = False
        elif self.step == 2 and self.next:
            self.btn.disabled = False
            self.btn.text = "Розпочати"
            self.step = 3
            self.next = False
        elif self.step == 3 and self.next:
            self.btn.disabled = False
            self.p3_input.disabled = False
            self.btn.text = "Продовжити"
            Clock.unschedule(self.update_timer)
            self.btn.unbind(on_press=self.start_timer)
            self.btn.bind(on_press=self.next_screen)




    def next_screen(self, instance):
        if self.step == 3 and self.p3_input.disabled == False:
            if self.p3_input.text == "":
                self.p3_input.hint_text = "Введіть пульс обов'язково!!!"
                self.p3_input.hint_text_color = (1, 0, 0, 1)
                return
        app = App.get_running_app()
        app.p2 = int(self.p2_input.text)
        app.p3 = int(self.p3_input.text)
        app.sm.current = 'fifth'


class FifthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = my_label(text="")
        layout = BoxLayout(orientation='vertical', padding=20)
        layout.add_widget(self.label)
        self.add_widget(layout)

    def on_enter(self):
        app = App.get_running_app()
        index = calc_rufier(app.p1, app.p2, app.p3)
        self.label.text = f"{app.user_name},\nВаш індекс Руф’є: {index}\nПрацездатність серця: {self.get_result(index)}"

    def get_result(self, index):
        if index < 0:
            return "Низьке навантаження"
        elif index <= 5:
            return "Добрий результат"
        elif index <= 10:
            return "Задовільний результат"
        else:
            return "Низька працездатність"


class RufierApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.user_name = ""
        self.user_age = 0
        self.p1 = 0
        self.p2 = 0
        self.p3 = 0

        self.sm.add_widget(FirstScreen(name='first'))
        self.sm.add_widget(SecondScreen(name='second'))
        self.sm.add_widget(ThirdScreen(name='third'))
        self.sm.add_widget(FourthScreen(name='fourth'))
        self.sm.add_widget(FifthScreen(name='fifth'))

        return self.sm


RufierApp().run()
