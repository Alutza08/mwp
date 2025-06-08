from kivy.app import App
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


def calc_rufier(p1, p2, p3):
    return round((p1 + p2 + p3 - 200) / 10, 1)


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Label(text="Ця програма дозволить вам пройти тест Руф'є.\nВведіть ім’я та вік:"))

        self.name_input = TextInput(hint_text="Ім'я")
        self.age_input = TextInput(hint_text="Вік", input_filter='int')

        layout.add_widget(self.name_input)
        layout.add_widget(self.age_input)

        btn = Button(text="Почати")
        btn.bind(on_press=self.next_screen)
        layout.add_widget(btn)

        self.add_widget(layout)

    def next_screen(self, instance):
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
        layout.add_widget(Label(text="Виміряйте пульс за 15 секунд\nВведіть результат нижче:"))

        self.progress = ProgressBar(max=self.total_time)
        layout.add_widget(self.progress)

        self.p1_input = TextInput(hint_text="Пульс", input_filter='int')
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
        App.get_running_app().p1 = int(self.p1_input.text)
        App.get_running_app().sm.current = 'third'


class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Label(text="Виконайте 30 присідань за 45 секунд"))
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
        self.total_time = 15
        self.elapsed = self.total_time
        self.step = 1
        self.next = True

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Label(
            text="Після присідань:\n- Заміряйте пульс за перші 15 секунд\n- Потім 15 секунд відпочинку\n- І знову пульс 15 секунд"))

        self.p2_input = TextInput(hint_text="Перший пульс", input_filter='int')
        self.p3_input = TextInput(hint_text="Другий пульс", input_filter='int')

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
        self.btn.disabled = True
        self.p2_input.disabled = True
        self.p3_input.disabled = True
        self.next = True
        self.elapsed = self.total_time
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
        app = App.get_running_app()
        app.p2 = int(self.p2_input.text)
        app.p3 = int(self.p3_input.text)
        app.sm.current = 'fifth'


class FifthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(text="", halign='center')
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
