import json
from io import StringIO
from dataclasses import dataclass


def create_patient(json_data: str):
    data = json.loads(json_data)

    return Patient(data['pregnancies'], data['glucose'], data['blood_pressure'], data['skin_thickness'],
                   data['insulin'], data['bmi'],
                   data['pedigree'], data['age'])


def patient_names():
    return ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age']


@dataclass
class Patient:
    """
    A representation of a patient that should be tested for diabetes
    """
    pregnancies: int
    glucose: int
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    pedigree: float
    age: int

    def to_json(self):
        return json.dumps(self.__dict__)

    def to_array(self):
        a = [self.pregnancies, self.glucose, self.blood_pressure, self.skin_thickness,
             self.insulin, self.bmi, self.pedigree, self.age]
        return StringIO(','.join(map(str, a)))
