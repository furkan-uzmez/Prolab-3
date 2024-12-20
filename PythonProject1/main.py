import polars as pl
import ast
import dijkstra
from pqueue import PriorityQueue


class Yazar:
    def __init__(self, name, id=0):
        self.id = id
        self.name = name
        self.makaleler = []
        self.dict_edges = {}

    def add_makele(self, makale):
        self.makaleler.append(makale)

    def add_edge(self, edges):
        for edge in edges:
            if self.name == edge.name:
                continue
            if edge.name not in self.dict_edges:
                self.dict_edges[edge.name] = 0
            self.dict_edges[edge.name] += 1

    def get_lenght_edges(self): # 5.ister
        return len(self.dict_edges)

    def get_lenght_makale(self):
        return len(self.makaleler)


def create_queue(author,names): # 2.ister
    kuyruk = PriorityQueue()
    yazarlar = [(author.name,author.get_lenght_makale())]
    for node in author.dict_edges:
        x = names[node]
        yazarlar.append((x.name,x.get_lenght_makale()))
    for node , priority in yazarlar:
        print(kuyruk.queue)
        kuyruk.push(node, priority)
    #print(kuyruk.queue)
    return kuyruk.toString()

def shortest_path_collaborators(author,names): # 4.ister
    graph = {author: author.dict_edges}
    for i,j in author.dict_edges.items():
        x = names[i]
        graph[x.name] = x.dict_edges
    #dijkstra.shortest_path(graph)


def en_cok_isbirligi(yazarlar): # 6.ister
    maximum = yazarlar[0]
    for x in yazarlar:
        if x.get_lenght_edges()>maximum.get_lenght_edges():
            maximum = x
    print("Maximum name:")
    print(maximum.name,maximum.get_lenght_edges())
    return maximum
def longest_path(graph, start): #7.ister
    if start not in graph:
        return []

    def dfs_recursive(node, visited):
        if not graph[node]:
            return [node]

        longest = [node]

        for neighbor in graph[node]:
            if neighbor not in visited:
                new_visited = visited | {node}
                new_path = dfs_recursive(neighbor, new_visited)

                if len(new_path) > len(longest) - 1:
                    longest = [node] + new_path
        return longest

    return dfs_recursive(start, set())

def load_authors():
    try:
        yazarlar = []
        adlar = {}
        idler = {}
        polars_df = pl.read_excel("PROLAB 3 - GÜNCEL DATASET.xlsx")

        polars_df = polars_df.head(100)

        authors = zip(polars_df['orcid'], polars_df['author_name'],polars_df['paper_title'])

        # id den yazar oluşturma
        for id, name, makale in authors:
            if id not in idler:
                yazar = Yazar(name, id)
                yazar.add_makele(makale)
                yazarlar.append(yazar)
                idler[id] = yazar
                adlar[name] = yazar
            else:
                yazar = idler[id]
                yazar.add_makele(makale)

        authors = zip( polars_df['author_position'],polars_df['coauthors'], polars_df['paper_title'])

        # co authors dan yazar oluşturma
        for position, coauthors, makale in authors:
            coauthors_list = ast.literal_eval(coauthors)
            for x in range(len(coauthors_list)):
                if x == position - 1:
                    continue
                if coauthors_list[x] in adlar:
                    adlar[coauthors_list[x]].add_makele(makale)
                else:
                    temp = Yazar(coauthors_list[x])
                    adlar[coauthors_list[x]] = temp
                    temp.add_makele(makale)
                    yazarlar.append(temp)

        toplam = 0

        # Edge oluşturma
        authors = zip(polars_df['orcid'], polars_df['author_position'], polars_df['coauthors'])
        for id, position, coauthors in authors:
            coauthors_list = ast.literal_eval(coauthors)
            toplam += len(coauthors_list)
            edges = [idler[id]]
            for i in range(len(coauthors_list)):
                if i == position - 1:
                    continue
                edges.append(adlar[coauthors_list[i]])
            for x in edges:
                x.add_edge(edges)
            edges.clear()

        toplam_edge = 0
        yazar_edges = {}
        for x in yazarlar:
            toplam_edge += x.get_lenght_edges()
            yazar_edges[x.name] = x.dict_edges
        #for author_name, connections in yazar_edges.items():
         #   print(author_name, connections)
        #dijkstra.shortest_path(yazar_edges,'B. Rajakumar','Revathy Kaipara')
        #print(idler['0000-0001-5111-8680'].dict_edges)
        #print(idler['0000-0001-5111-8680'].get_lenght_edges())
        #create_queue(idler['0000-0002-9851-4047'],names)
        #print(longest_path(yazar_edges,idler['0000-0002-9851-4047']))
        print(toplam)
        print(toplam_edge)
        print(len(yazarlar))
        return yazarlar,adlar,yazar_edges

    except Exception as e:
        print(f"Error loading data: {e}")
        return []


def process_ister1(author_a, author_b):
    # İki yazar arasındaki ilişkiyi analiz eden kod
    yazarlar,names,graph = load_authors()

    # Yazarları bul
    yazar1 = next((y for y in yazarlar if y.name == author_a), None)
    yazar2 = next((y for y in yazarlar if y.name == author_b), None)

    if not yazar1 or not yazar2:
        return "Yazarlardan biri bulunamadı!"

    # Ortak makaleler, işbirlikleri vb. analiz edilebilir
    ortak_makaleler = set(yazar1.makaleler) & set(yazar2.makaleler)

    return dijkstra.shortest_path(graph,yazar1.name,yazar2.name)


def process_single_author(author_id, ister_number):
    yazarlar,names,graph = load_authors()

    # Yazarı bul
    yazar = next((y for y in yazarlar if y.id == author_id), None)

    if ister_number == 6:
        yazar = en_cok_isbirligi(yazarlar)
        return f"""
                En çok işbirliği yapan yazar :\n
                {yazar.name}: {yazar.get_lenght_edges()}
               """
        
    if not yazar:
        return "Yazar bulunamadı!"

    if ister_number == 2:
        return create_queue(yazar,names)
    elif ister_number == 3:
        return f"""
            3. İster Sonuçları:
            - Yazar Adı: {yazar.name}
            - İşbirliği Sayısı: {yazar.get_lenght_edges()}
            """

    elif ister_number == 4:
        return shortest_path_collaborators(yazar,names)
    elif ister_number == 5:
        return f"""
                {yazar.name} : {yazar.get_lenght_edges()}
                """
    elif ister_number == 7:
        return longest_path(graph , yazar.name)

    return "Geçersiz ister numarası!"
