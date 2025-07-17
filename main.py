import os
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

KV = '''
ScreenManager:
    LoginScreen:
    RegisterScreen:
    DashboardScreen:
    AddTransactionScreen:

<LoginScreen>:
    name: 'login'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        Label:
            text: 'Login'
            font_size: 24
        TextInput:
            id: email
            hint_text: 'Email'
            multiline: False
        TextInput:
            id: password
            hint_text: 'Password'
            password: True
            multiline: False
        Button:
            text: 'Login'
            on_press: root.login(email.text, password.text)
        Button:
            text: 'Register'
            on_press: app.root.current = 'register'

<RegisterScreen>:
    name: 'register'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        Label:
            text: 'Register'
            font_size: 24
        TextInput:
            id: email
            hint_text: 'Email'
            multiline: False
        TextInput:
            id: password
            hint_text: 'Password'
            password: True
            multiline: False
        Button:
            text: 'Register'
            on_press: root.register(email.text, password.text)
        Button:
            text: 'Back to Login'
            on_press: app.root.current = 'login'

<DashboardScreen>:
    name: 'dashboard'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        Label:
            text: 'Dashboard'
            font_size: 24
        Label:
            text: 'Saldo: R$' + str(app.balance)
        Button:
            text: 'Adicionar Transação'
            on_press: app.root.current = 'add'

<AddTransactionScreen>:
    name: 'add'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        Label:
            text: 'Adicionar Transação'
            font_size: 24
        TextInput:
            id: title
            hint_text: 'Título'
            multiline: False
        TextInput:
            id: amount
            hint_text: 'Valor'
            multiline: False
        TextInput:
            id: category
            hint_text: 'Categoria'
            multiline: False
        Button:
            text: 'Salvar'
            on_press: root.add_transaction(title.text, amount.text, category.text)
        Button:
            text: 'Voltar'
            on_press: app.root.current = 'dashboard'
'''

Base = declarative_base()
DB_PATH = os.path.join(os.path.dirname(__file__), 'finance.db')
engine = create_engine(f'sqlite:///{DB_PATH}')
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String)
    amount = Column(Float)
    category = Column(String)
    date = Column(Date, default=datetime.utcnow)

Base.metadata.create_all(engine)

class LoginScreen(Screen):
    def login(self, email, password):
        session = Session()
        user = session.query(User).filter_by(email=email, password=password).first()
        if user:
            App.get_running_app().user_id = user.id
            App.get_running_app().root.current = 'dashboard'
        else:
            Popup(title='Erro', content=Label(text='Usuário ou senha incorretos'), size_hint=(None, None), size=(400, 200)).open()
        session.close()

class RegisterScreen(Screen):
    def register(self, email, password):
        session = Session()
        if session.query(User).filter_by(email=email).first():
            Popup(title='Erro', content=Label(text='Usuário já existe'), size_hint=(None, None), size=(400, 200)).open()
        else:
            user = User(email=email, password=password)
            session.add(user)
            session.commit()
            Popup(title='Sucesso', content=Label(text='Registrado com sucesso'), size_hint=(None, None), size=(400, 200)).open()
            App.get_running_app().root.current = 'login'
        session.close()

class DashboardScreen(Screen):
    pass

class AddTransactionScreen(Screen):
    def add_transaction(self, title, amount, category):
        try:
            amount_val = float(amount)
        except ValueError:
            Popup(title='Erro', content=Label(text='Valor inválido'), size_hint=(None, None), size=(400, 200)).open()
            return
        session = Session()
        transaction = Transaction(user_id=App.get_running_app().user_id, title=title, amount=amount_val, category=category)
        session.add(transaction)
        session.commit()
        session.close()
        App.get_running_app().update_balance()
        Popup(title='Sucesso', content=Label(text='Transação adicionada'), size_hint=(None, None), size=(400, 200)).open()
        App.get_running_app().root.current = 'dashboard'

class FinanceApp(App):
    balance = NumericProperty(0.0)
    user_id = None
    def build(self):
        self.title = 'Financeiro'
        return Builder.load_string(KV)

    def on_start(self):
        self.update_balance()

    def update_balance(self):
        if not self.user_id:
            self.balance = 0
            return
        session = Session()
        income = session.query(Transaction).filter(Transaction.user_id==self.user_id, Transaction.amount>0).all()
        expense = session.query(Transaction).filter(Transaction.user_id==self.user_id, Transaction.amount<0).all()
        income_total = sum(t.amount for t in income)
        expense_total = sum(t.amount for t in expense)
        self.balance = income_total + expense_total
        session.close()

if __name__ == '__main__':
    FinanceApp().run()
