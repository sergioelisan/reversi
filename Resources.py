import pickle

class ReversiIO:
    ''' Classe que abstrai as operacoes de arquivo '''
    
    def __init__(self, path):
        self.file_path = path

    def save(self, obj):
        ''' Salva o dicionario do rank do arquivo '''
        output = open(self.file_path, 'w')
        pickle.dump(obj, output)
        output.close()

    def read(self):
        ''' Le o dicinario do rank do arquivo '''
        file = open(self.file_path, 'r')
        try:
            obj = pickle.load(file)
        except:
            self.save("{}")
            obj = pickle.load(file)
        file.close()
        return obj

