import json
import sys
import numpy as np
import uuid

delimiter = '|'

int_features = {
    'n_messages':40,
    'user1_sent_picture':2,            # Boolean
    'user2_sent_picture':2,            # Boolean
}

def get_profile_ids(user_json='fake_profiles.json'):
    with open(user_json) as json_file:
        data = json.load(json_file)
    profile_ids = [key for key in data.keys()]
    return profile_ids


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
            fake_int_features[k] = int(np.random.choice(range(v[0], v[1] + 1)))
        else:
            fake_int_features[k] = int(np.random.choice(v))
    return fake_int_features

def get_fake_users():
    user_library = get_profile_ids()
    user1 = np.random.choice(user_library)
    user2 = np.random.choice(user_library)
    while user2 == user1:
        user2 = np.random.choice(user_library)
    return (user1, user2)

def generate_fake_conversation(n_conversations=10):
    fake_conversation_dict = {}
    for _ in range(n_conversations):
        conversation_id = str(uuid.uuid4())
        fake_chat_data = generate_int_features(int_features)
        fake_users = get_fake_users()
        fake_chat_data['user1'] = fake_users[0]
        fake_chat_data['user2'] = fake_users[1]
        fake_conversation_dict[conversation_id] = fake_chat_data
    return fake_conversation_dict

def export_json(n_samples, file_name = 'fake_chats.json'):
    fake_chats = generate_fake_conversation(n_samples)
    with open(file_name, 'w', encoding='utf8') as json_file:
        json.dump(fake_chats, json_file, indent=4, default=str)

if __name__ == '__main__':
    export_json(int(sys.argv[1]))