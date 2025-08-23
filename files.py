import os
import json

class MyFile:
    def __init__(self, path):
        self.path = path
    
    def create_files(self):
        os.makedirs(self.path, exist_ok=True)
        files_to_create = {
        'history.json': '[]',
        'theme.json': json.dumps({'bg': True}),
        'button.json': json.dumps({'color': 'blue'})}
            
        for file_name, default_contents in files_to_create.items():
            file_path = os.path.join(self.path, file_name)
            
            # This check is good, but let's make the read_file function more robust
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                with open(file_path, "wt") as f:
                    f.write(default_contents)

    def read_file(self, file_name):
        file_path = os.path.join(self.path, file_name)
        
        # Check if the file exists and is not empty before attempting to read
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            try:
                with open(file_path, 'rt') as f:
                    return json.loads(f.read())
            except (json.JSONDecodeError, ValueError, IndexError, EOFError):
                # If there's a JSON decoding error or an EOFError,
                # return a default value based on the file type.
                if file_name == 'history.json':
                    return []
                else:
                    return {'bg': True} if file_name == 'theme.json' else {'color': 'blue'}

        # If the file does not exist, return a default value
        if file_name == 'history.json':
            return []
        if file_name == 'theme.json':
            return {'bg': True}
        if file_name == 'button.json':
            return {'color': 'blue'}
            
    def write_file(self, file_name, content):
        with open(os.path.join(self.path, file_name), 'wt') as f:
            f.write(json.dumps(content))
