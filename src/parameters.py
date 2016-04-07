import json

class Parameters:

    #Test initialization, gives dummy values
    def __init__(self):
        self.boid_count = 10
        self.weight_cohesion = 5
        self.weight_separation = 5
        self.weight_alignment = 5

    
    def load_from_file(self, file_name):
        file = open(file_name, 'rt')
        json_data = json.load(file)[0]
        if not 'boid_count' in json_data and 'weight_cohesion' in json_data and 'weight_separation' in json_data and 'weight_alignment' in json_data:
            raise ValueError("The configuration could not be read.")
        self.boid_count = json_data['boid_count']
        self.weight_cohesion = json_data['weight_cohesion']
        self.weight_separation = json_data['weight_separation']
        self.weight_alignment = json_data['weight_alignment']
        file.close()

    
    def save_to_file(self, file_name):
        try:
            file = open(file_name, 'wt')
            json_data = {}
            json_data['weight_cohesion'] = self.weight_cohesion
            json_data['weight_separation'] = self.weight_separation
            json_data['weight_alignment'] = self.weight_alignment
            json_data['boid_count'] = self.boid_count
            json.dump([json_data], file, sort_keys = True)
            file.close()
        except Exception as e:
            raise e


