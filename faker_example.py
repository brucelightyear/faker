import numpy as np
import pandas as pd
from faker import Faker
fake = Faker(['fr-CA'])
fake.locales
from faker.providers.person.fr_CA import Provider

def random_names(name_type, size):
    """
    Generate n-length ndarray of person names.
    name_type: a string, either first_names or last_names
    """
    names = getattr(Provider, name_type)
    return np.random.choice(names, size=size)

def random_genders(size, p=None):
    """Generate n-length ndarray of genders."""
    if not p:
        # default probabilities
        p = (0.49, 0.49, 0.01, 0.01)
    gender = ("M", "F", "O", "")
    return np.random.choice(gender, size=size, p=p)

def random_dates(start, end, size):
    """
    Generate random dates within range between start and end.    
    Adapted from: https://stackoverflow.com/a/50668285
    """
    # Unix timestamp is in nanoseconds by default, so divide it by
    # 24*60*60*10**9 to convert to days.
    divide_by = 24 * 60 * 60 * 10**9
    start_u = start.value // divide_by
    end_u = end.value // divide_by
    return pd.to_datetime(np.random.randint(start_u, end_u, size), unit="D")

def random_address(size):
    """
    Generate n-length ndarray of address.
    """
    fake = Faker('en_CA')
    addressList = []
    for _ in range(size):
        address = fake.address().split(", ")[0].replace('\n', ', ')
        addressList.append(address + ", QC " + fake.postalcode_in_province("QC"))
    
    return np.random.choice(addressList, size=size)

def random_nas(size):
    fake = Faker('en_CA')
    nasList = []
    for _ in range(size):
        nasList.append(fake.ssn())
    
    return np.random.choice(nasList, size=size)

# How many records do we want to create in our CSV? In this example
# we are generating 100, but you could also find relatively fast results generating 
# much larger datasets
size = 1000 
df = pd.DataFrame(columns=['First', 'Last', 'Gender', 'Birthdate','Address', 'NAS'])

df['First'] = random_names('first_names', size)
df['Last'] = random_names('last_names', size) 
df['Gender'] = random_genders(size) 
df['Birthdate'] = random_dates(start=pd.to_datetime('1940-01-01'), end=pd.to_datetime('2008-01-01'), size=size)
df['Address'] = random_address(size)
df['NAS'] = random_nas(size)
df.to_csv('fake-file.csv')

print("Terminé")