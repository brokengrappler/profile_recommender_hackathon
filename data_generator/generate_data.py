import numpy as np
from random import randint
from faker import Faker
import json
import sys

############### SELECTION OF FEATURES AND DESCRIPTIONS #####################
int_features = {
    'AGE':(18,80),            # between 18 - 65
    'ETHNICITY_ID':(1,9),         # 1-9
    'BODYTYPE_ID':(1,6),          # 1-6
    'RELATIONSHIPTYPE_ID':(1,8),  # 1-8
    'SHOWAGE':2,              # boolean
    'SHOWDISTANCE':2,         # boolean
    'SEXUALPOSITION_ID':(1,7),    # 1-7
    'GENDER_CATEGORY': (1,13),      # 1-13
    'PRONOUNS_CATEGORY': (1,4),    # 1-4
    'TRIBE_IDS': (1,13),            # 1-13
    'THIRD_PARTY_TYPE': 5,     # 0-4
    'HAS_PHONE':2,            # Boolean
    'NSFW_ID': (1,3)              # 1-3
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
            fake_int_features[k] = int(np.random.choice(range(v[0], v[1]+1)))
        else:
            fake_int_features[k] = int(np.random.choice(v))
    return fake_int_features

def generate_faker_features():
    '''
    Generate data using faker library
    :return:
        dict with key and values
    '''
    faker_features = {}
    fake = Faker()
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

def aggregate_fake_features(int_features):
    '''
    Aggregate features generated using random int and faker module
    :param
        int_features: dictionary with feature name as key and either int to provide range (0:int) or tuple if
        range is specified (e.g., (18,70) for age range)
    :return:
        dictionary of all features
    '''
    aggregate_features = dict(generate_int_features(int_features))
    aggregate_features.update(generate_faker_features())
    return aggregate_features

def generate_fake_profiles(n_samples):
    n_sample_dict = {}
    for _ in range(n_samples):
        # profile_id is random int between 1000000, 10000000
        profile_id = randint(1000000, 10000000)
        user_data = aggregate_fake_features(int_features)
        n_sample_dict[profile_id] = user_data
    return n_sample_dict

def export_json(n_samples=10, file_name = 'fake_profiles.json'):
    fake_profiles = generate_fake_profiles(n_samples)
    with open(file_name, 'w', encoding='utf8') as json_file:
        json.dump(fake_profiles, json_file, indent=4, default=str)

if __name__ == '__main__':
    export_json(int(sys.argv[1]))
