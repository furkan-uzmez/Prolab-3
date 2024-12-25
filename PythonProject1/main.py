import polars as pl
import ast
import dijkstra
import time
from pqueue import PriorityQueue
from  bst import BST

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
            if self.id == edge.id:
                continue
            if edge.id not in self.dict_edges:
                self.dict_edges[edge.id] = 0
            self.dict_edges[edge.id] += 1

    def get_lenght_edges(self): # 5.ister
        return len(self.dict_edges)

    def get_lenght_makale(self):
        return len(self.makaleler)


def create_queue(author,idler): # 2.ister
    kuyruk = PriorityQueue()
    yazarlar = [(author.id,author.get_lenght_makale())]
    print(idler['22'])
    for id,_ in author.dict_edges.items():
        x = idler[id]
        yazarlar.append((id,x.get_lenght_makale()))
    for node , priority in yazarlar:
        print(kuyruk.queue)
        kuyruk.push(node, priority)
    #print(kuyruk.queue)
    return kuyruk.queue

def shortest_path_collaborators(author,idler): # 4.ister
    graph = {author.id : author.dict_edges}

    unvisited = []

    for i,_ in author.dict_edges.items():
        unvisited.append(i)
        x = idler[i]
        graph[x.id] = x.dict_edges

    visited = set()

    shortest_paths = {}
    distances = {}
    for x in unvisited:
        if x not in visited:
            shortest_paths[x],distances[x],_ = dijkstra.shortest_path(graph,author.id,x)
            visited.add(x)

    return shortest_paths,distances

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
        uniq_id = 1
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
                    temp = Yazar(coauthors_list[x],str(uniq_id))
                    idler[str(uniq_id)] = temp
                    uniq_id += 1
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
            yazar_edges[x.id] = x.dict_edges

        print(toplam)
        print(toplam_edge)
        print(len(yazarlar))
        return yazarlar,idler,yazar_edges

    except Exception as e:
        print(f"Error loading data: {e}")
        return []


def process_ister1(author_a, author_b):
    # İki yazar arasındaki ilişkiyi analiz eden kod
    yazarlar,names,graph = load_authors()

    # Yazarları bul
    yazar1 = next((y for y in yazarlar if y.id == author_a), None)
    yazar2 = next((y for y in yazarlar if y.id == author_b), None)

    if not yazar1 or not yazar2:
        return "Yazarlardan biri bulunamadı!"

    # Ortak makaleler, işbirlikleri vb. analiz edilebilir
    #ortak_makaleler = set(yazar1.makaleler) & set(yazar2.makaleler)

    path,distance,kuyruk = dijkstra.shortest_path(graph,yazar1.id,yazar2.id)

    print(kuyruk.Print())
    bst = BST()
    curr = kuyruk.head
    while curr != None:
        temp_list = [curr.data[0],curr.data[1]]
        bst.root = bst.Insert(bst.root,temp_list)
        curr = curr.next
    bst.Print(bst.root)

    formatted_path = "<br>".join(path)
    return f"Yazar1:{yazar1.name}<br>Yazar2:{yazar2.name}<br><br>En Kısa Yol:<br>{formatted_path}<br><br>Maliyet: {distance}",path


def process_single_author(author_id, ister_number):
    yazarlar,idler,graph = load_authors()

    # Yazarı bul
    yazar = next((y for y in yazarlar if y.id == author_id), None)

    if ister_number == 6:
        yazar = en_cok_isbirligi(yazarlar)
        path = [yazar.id]
        formatted_path = "<br>".join([f"{bağlantı} : {ağırlık}" for bağlantı, ağırlık in yazar.dict_edges.items()])
        return f"""
                En çok işbirliği yapan yazar :<br>
                {yazar.name}: {yazar.get_lenght_edges()} işbirliği<br><br>
                Bağlantılar :<br>
                {formatted_path}<br>
               """,path
        
    if not yazar:
        return "Yazar bulunamadı!"

    if ister_number == 2:
        path= []
        kuyruk = create_queue(yazar,idler)
        kuyruk.reverse()
        print(kuyruk)
        formatted_path = "<br>".join([f"{t[1]}: {t[0]}" for t in kuyruk])
        return "Yazar - Ağırlık(Makale Sayısı)<br>" + formatted_path , path
    elif ister_number == 3:
        return f"""
            3. İster Sonuçları:
            - Yazar Adı: {yazar.name}
            - İşbirliği Sayısı: {yazar.get_lenght_edges()}
            """

    elif ister_number == 4:
        path = []
        shortest_paths,distances = shortest_path_collaborators(yazar,idler)
        string = " "
        for i,j in shortest_paths.items():
            string += f"{yazar.name} - {i} en kısa yol :<br><br>"
            for k in j:
                string += f"{k}<br>"
            string += "<br>"
            string += f"Maliyet : {distances[i]}<br><br><br>"
        return string,path
    elif ister_number == 5:
        path = [yazar.id]
        formatted_path = "<br>".join([f"{bağlantı} : {ağırlık}" for bağlantı, ağırlık in yazar.dict_edges.items()])
        return f"""
                Yazar adı: {yazar.name}  <br>
                İş birliği yaptığı yazar sayısı: {yazar.get_lenght_edges()} <br><br>
                Bağlantılar :<br>
                {formatted_path}<br>
                """,path
    elif ister_number == 7:
        start_time = time.time()
        path = longest_path(graph , yazar.id)
        end_time = time.time()
        print(f"İşlem süresi: {end_time - start_time:.5f} saniye")
        distance = len(path)
        formatted_path = "<br>".join(path)
        return f"Yazar adı : {yazar.name}<br>En uzun yol:<br>{formatted_path}<br>Maliyet: {distance}",path

    return "Geçersiz ister numarası!"
