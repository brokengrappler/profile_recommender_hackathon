import numpy as np
from random import randint
from faker import Faker
import json
import sys

faker_seed = 2022

############### SELECTION OF FEATURES AND DESCRIPTIONS #####################
int_features = {
    'AGE':(18,80),            # between 18 - 65
    'ETHNICITY_ID':8,         # 1-9
    'BODYTYPE_ID':5,          # 1-6
    'RELATIONSHIPTYPE_ID':7,  # 1-8
    'SHOWAGE':1,              # boolean
    'SHOWDISTANCE':1,         # boolean
    'SEXUALPOSITION_ID':6,    # 1-7
    'GENDER_CATEGORY':12,      # 1-13
    'PRONOUNS_CATEGORY':3,    # 1-4
    'TRIBE_IDS':12,            # 1-13
    'THIRD_PARTY_TYPE':3,     # 0-4
    'HAS_PHONE':1,            # Boolean
    'NSFW_ID':2               # 1-3
}
#
# faker_features = [
#     'UPDATED_AT',           # timestamp
#     'HEIGHT',               # generate via faker
#     'WEIGHT',               # generate via faker
#     'LONGITUDE',            # generate via faker
#     'LATITUDE',             # generate via faker
# ]
#
# misc_features = [
#     'APP_CATEGORY',         # ['Free', 'Xtra', 'Unlimited', 'Free_Xtra', 'Free_NoAds', 'Free_Unlimited']
# ]

def generate_int_features(features):
    '''
    Populate features with int values, including boolean (0 vs. 1)
    :param
        features: dictionary with feature name as key and either int to provide range (0:int) or tuple if
        range is specified (e.g., (18,70) for age range)
    :return:
        dictionary with feature:value
    '''
    fake_int_features = {}
    for k, v in features.items():
        if isinstance(v, tuple):
            fake_int_features[k] = int(np.random.choice(range(v[0], v[1])))
        else:
            fake_int_features[k] = int(np.random.choice(v)+1)
    return fake_int_features

def generate_faker_features(faker_seed):
    '''
    Generate data using faker library
    :param
        faker_seed: global var
    :return:
        dict with key and values
    '''
    faker_features = {}
    fake = Faker()
    Faker.seed(faker_seed)
    reg=''
    while reg != 'Los_Angeles':
        loc_samp = fake.local_latlng()
        reg = loc_samp[4].split('/')[1]
    faker_features['LONGITUDE'] = loc_samp[1]
    faker_features['LATITUDE'] = loc_samp[0]
    faker_features['UPDATED_AT'] = fake.date_time_this_year()
    # TODO: for MVP exclude height and weight; rely on body type
    # faker_features['HEIGHT'] = ''
    # faker_features['WEIGHT'] = ''
    return faker_features

def generate_misc_features():
    # random app class
    return np.random.choice(['Free', 'Xtra', 'Unlimited', 'Free_Xtra', 'Free_NoAds', 'Free_Unlimited'])

def aggregate_fake_features(int_features, faker_seed):
    '''
    Aggregate features generated using random int and faker module
    :param
        int_features: dictionary with feature name as key and either int to provide range (0:int) or tuple if
        range is specified (e.g., (18,70) for age range)
        faker_seed: seed for recreation of list
    :return:
        dictionary of all features
    '''
    aggregate_features = dict(generate_int_features(int_features))
    aggregate_features.update(generate_faker_features((faker_seed)))
    return aggregate_features

def generate_fake_profiles(n_samples):
    n_sample_dict = {}
    for _ in range(n_samples):
        # profile_id is random int between 1000000, 10000000
        profile_id = randint(1000000, 10000000)
        user_data = aggregate_fake_features(int_features, faker_seed)
        n_sample_dict[profile_id] = user_data
    return n_sample_dict

def export_json(n_samples=10, file_name = 'fake_profiles.json'):
    fake_profiles = generate_fake_profiles(n_samples)
    with open(file_name, 'w', encoding='utf8') as json_file:
        json.dump(fake_profiles, json_file, indent=4, default=str)

if __name__ == '__main__':
    export_json(int(sys.argv[1]))
