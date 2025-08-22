import os
import json

class MyFile:
    def __init__(self,path):
        self.path = path
        
    def create_files(self):
        os.makedirs(self.path,exist_ok=True)
        
        files_to_create = {
        'history.json':'[]',
        'theme.json':json.dumps({'bg':True}),
        'button.json':json.dumps({'color':'blue'})}
            
        for file_name,default_contents in files_to_create.items():
                file_path = os.path.join(self.path,file_name)
                
                if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                    with open(file_path,"wt") as f:
                        f.write(default_contents)
                    
                

    def read_file(self,file_name):
        with open(os.path.join(self.path,file_name),'rt') as f:
            return json.loads(f.read())
                
    def write_file(self,file_name,content):
        with open(os.path.join(self.path,file_name),'wt') as f:
            f.write(json.dumps(content))
                    
                
            
        
        