from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    ObjectProperty
)
from src.room.office import Office
from person.worker import Worker
from person.repairman import Repairman

from src.room.toilet import Toilet


class CorporationGame(FloatLayout):
    game_field = ObjectProperty(None)
    object_layer = ObjectProperty(None)
    worker_layer = ObjectProperty(None)

    gui = ObjectProperty(None)
    is_worker_opened = False
    is_office_opened = False
    current_office = 'office'
    current_worker = 'person'

    money_display = None
    money = 1100

    time = 0
    salary_time = 15 * 60

    workers = []
    offices = []

    current_state = 'none'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def prepare(self):
        self.game_field.fill_grass()

    def set_state(self, state):
        self.current_state = state

    def tick(self, dt):
        if self.money <= -100:
            pass

        self.time += 1
        self.money_display.text = str(self.money)

        for office in self.offices:
            office.update()

        for worker in self.workers:
            worker.update()

            if self.time == self.salary_time:
                self.money -= worker.salary
                self.time = 0

    def place(self, pos, office=None):
        if self.current_state == 'person':
            if self.current_worker == 'person':
                self.place_worker(pos, office)
            else:
                self.place_repairman(pos, office)
            return

        if self.current_state == 'office':
            if self.current_office == 'office':
                self.place_office(pos)
            else:
                self.place_toilet(pos)
            return

    def add_money(self, money):
        self.money += money

    def remove_money(self, money):
        self.money -= money

    def place_worker(self, pos, office):
        if self.game_field.data[pos[1]][pos[0]].contains_office:
            w = Worker(pos=self.game_field.get_pos(pos),
                       cell_size=self.game_field.cell_size,
                       size_hint=(None, None),
                       office=office)
            self.worker_layer.add_widget(w)
            self.remove_money(w.price)
            self.workers.append(w)

    def place_repairman(self, pos, office):
        if self.game_field.data[pos[1]][pos[0]].contains_office:
            r = Repairman(pos=self.game_field.get_pos(pos),
                          cell_size=self.game_field.cell_size,
                          size_hint=(None, None),
                          office=office)
            self.worker_layer.add_widget(r)
            self.remove_money(r.price)
            self.workers.append(r)

    def place_office(self, pos, length=6):
        if self.game_field.can_be_placed(pos=pos, length=length):
            o = Office(pos=self.game_field.get_pos(pos),
                       cell_size=self.game_field.cell_size,
                       size_hint=(None, None),
                       position=pos)
            self.remove_money(o.price)
            self.object_layer.add_widget(o)
            self.offices.append(o)
            for i in range(length):
                self.game_field.data[pos[1]][pos[0] + i].contains_office = True

    def place_toilet(self, pos, length=2):
        if self.game_field.can_be_placed(pos=pos, length=length):
            t = Toilet(pos=self.game_field.get_pos(pos),
                       cell_size=self.game_field.cell_size,
                       size_hint=(None, None),
                       position=pos)
            self.remove_money(t.price)
            for i in range(length):
                self.game_field.data[pos[1]][pos[0] + i].contains_office = True

    def switch_state(self, state):
        if state == self.current_state:
            self.set_state('none')
            return

        self.set_state(state)
