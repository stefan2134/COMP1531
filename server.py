from flask import Flask
from lib.system import HamsSystem
from lib.user import Provider, HealthcareCentre, Patient, Specialist
from lib.employment import Employment
from lib.appointment import Appointment
from datetime import time
import csv

app = Flask(__name__)
app.secret_key = "this must be change to something secretive but idk why tho"

system = HamsSystem()
system.load_data()
