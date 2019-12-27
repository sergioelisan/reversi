from Resources import ReversiIO

class Ranking:
    ''' Classe que abstrai um ranking e suas operacoes '''
    
    def __init__(self):
        self.file = "res/ranking.dat"        

    def register(self, name, points):
        ''' Registra o nome dos jogadores no Ranking '''
        rank = self.getRank()
        rank[points] = name
        self.saveRank(rank)

    def getRank(self):
        ''' Pega um ranking do aquivo '''
        io = ReversiIO(self.file)
        return io.read()
    
    def toString(self):
        ''' Retorna uma representacao em Lista de Strings do Ranking '''
        rank = self.getRank().items()
        rank.sort()
        rank.reverse()

        string = ""
        for person in rank[:5]:
            string += str(person[0]) + " - " + str(person[1]) + "\n"

        return string.split("\n")

    def saveRank(self, rank):
        ''' Salva o ranking no arquivo'''
        io = ReversiIO(self.file)
        io.save(rank)
