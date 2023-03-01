"""
Приложение Банюшка
В наличие дожен быть выбор даты и времени, возможна ремарка через спичрекогнишз, произведение записи всей информации в
файл базы данных, показ всех уже имеющихся записей на календаре
Дополнительно поле О нас с картой проезда, поле Связаться с телефоном.
Желательно интересный фон и прикольные фишечки в виде веников, ушатов и т.п.

MDTapTargetView для звонка
"""
import datetime

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.dialog.dialog import MDDialog
from kivymd.uix.button.button import MDFlatButton
from kivymd.uix.card.card import MDCardSwipe
from kivy.properties import StringProperty
from kivymd.uix.fitimage.fitimage import FitImage

from kivy.uix.anchorlayout import AnchorLayout

# Window.size = (864, 900)
Window.clearcolor = (0, 0.17, 0.55, 1)
Window.maximize()
global choice_period

KV = '''
BoxLayout:
    orientation:'vertical'

    Image:
        source: "bnshk.jpg"
        size: self.texture_size  
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_y: None
        size_hint_x: None 


    MDBottomNavigation:
        sizehint: 

        MDBottomNavigationItem:
            text: "Позвонить"
            icon: "phone-forward"
            # on_tab_press: 


        MDBottomNavigationItem:
            text: "Выбрать дату-время"
            icon: "timetable"
            on_tab_press: app.show_date_picker()

        MDBottomNavigationItem:
            text: "Как добраться"
            icon: "car-multiple"
            on_tab_press: app.map_dialog()


<ItemConfirm>
    on_release: root.set_icon(check)
    CheckboxLeftWidget:
        id: check
        group: 'check'
'''


# day_schedule ={'',{}}
#
# class InformTab:
#     def __init__(self, day_schedule):
#         self.day_schedule = day_schedule


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        global choice_period
        # instance_check передает только сам активный объек, но не выставляет его свойство active в положение True
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in range(len(check_list)):
            if check_list[check] != instance_check:
                check_list[check].active = False
            else:
                choice_period = check + 1  # определение кличества забронированных часов


class BanushkaApp(MDApp):
    global choice_period
    choice_date = datetime.date.today()  # выбранная дата сеанса
    choice_time = ''  # выбранное время начала сеанса
    choice_period = ''
    warning_title = ''
    warning_text = ''

    def map_dialog(self):
        warning_table_map = MDDialog(title='Hello', size_hint_y=.9, size_hint_x=.9)
        warning_table_map.add_widget(FitImage(source="map.jpg"))
        warning_table_map.open()

    def choice_period_dialog(self):
        self.warning_table_choice_period = MDDialog(title='Выберите количество часов', type='confirmation',
                                                    items=[
                                                        ItemConfirm(text='1 час'),
                                                        ItemConfirm(text='2 часа'),
                                                        ItemConfirm(text='3 часа'),
                                                        ItemConfirm(text='4 часа'),
                                                        ItemConfirm(text='5 часов'),
                                                        ItemConfirm(text='6 часов')],
                                                    buttons=[MDFlatButton(text='Отменить',
                                                                          theme_text_color="Custom",
                                                                          halign='center',
                                                                          on_release=self.close_Dialog
                                                                          ),
                                                             MDFlatButton(text='Ok',
                                                                          theme_text_color="Custom",
                                                                          halign='center',
                                                                          on_release=self.ok_Dialog
                                                                          )
                                                             ]
                                                    )
        self.warning_table_choice_period.open()

    def ok_Dialog(self, items):

        self.confirm_choice()
        self.warning_table_choice_period.dismiss()

        pass

    def close_Dialog(self, inst):
        self.warning_table_choice_period.dismiss()

        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.warning_table = MDDialog(title=self.warning_title, text=self.warning_text, buttons=[MDFlatButton(
            text="Ok",
            theme_text_color="Custom",
            halign='center',
            on_press=self.close_call_warning)])
        self.time_dialog = MDTimePicker()
        self.date_dialog = MDDatePicker(min_year=self.choice_date.year,
                                        max_year=self.choice_date.year + 2,
                                        title_input="Введите дату",
                                        title='Выберите дату'
                                        )

    def build(self):
        return Builder.load_string(KV)

    # процедура вызова выбора даты
    def show_date_picker(self):
        self.date_dialog.bind(on_save=self.customer_date_choice)
        self.date_dialog.bind(on_cancel=self.close_date_picker)
        self.date_dialog.open()

    # процедура записи даты
    def customer_date_choice(self, instance, value, date_range):
        self.choice_date = value
        if self.choice_date <= datetime.date.today():
            self.warning_table.title = 'Внимание!'
            self.warning_table.text = 'Дата не может быть в прошлом!' \
                                      '' \
                                      ' Выберите дату в будущем периоде'
            return self.date_dialog.open(), self.call_warning()
        else:
            self.choice_date = value
            return self.date_dialog.dismiss, self.show_time_picker()

    # процедура вызова выбора времени
    def show_time_picker(self):
        self.time_dialog.am_pm = 'pm'
        self.time_dialog.bind(on_save=self.on_save_time_dialog)
        self.time_dialog.bind(on_cancel=self.on_cancel_time_dialog)
        self.time_dialog.open()

    # процедура записи времени
    def customer_time_choice(self, instance, value):
        self.choice_time = value
        return self.time_dialog.dismiss()

    # процедура окна предупреждения
    def call_warning(self):
        self.warning_table.open()
        self.date_dialog.dismiss()

    def on_cancel_time_dialog(self, *args):
        self.time_dialog.dismiss()
        self.date_dialog.open()

    def on_save_time_dialog(self, instance, value):
        self.customer_time_choice(instance, value)
        self.choice_period_dialog()

    def close_date_picker(self, instance, value):
        self.date_dialog.dismiss()

    # def close_time_picker(self, instance):
    #     self.time_dialog.dismiss()

    def confirm_choice(self):
        self.warning_table.title = 'Подтвердите ваш выбор :'
        print(str(choice_period) + 'choice_period')
        self.warning_table.text = str(self.choice_date) + '  в ' + str(self.choice_time) + '  на ' + str(
            choice_period) + ' ч.'
        self.call_warning()

    def close_call_warning(self, *args):
        global choice_period
        self.warning_table.dismiss()
        self.warning_table.title = ''
        self.warning_table.text = ''
        choice_period = ''


if __name__ == "__main__":
    BanushkaApp().run()

