from flask import Flask, render_template, request, jsonify
import time
from main import load_authors, process_ister1, process_single_author
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

@app.route('/api/graph-data')
def get_graph_data():
    yazarlar,names,graph = load_authors()
    nodes = []
    links = []
    node_map = {}

    # Create nodes
    for i, yazar in enumerate(yazarlar):
        node_map[yazar.name] = i
        nodes.append({
            'id': i,
            'name': yazar.name,
            'group': 1,  # You can modify grouping based on your needs
            'papers': len(yazar.makaleler),
            'details': {  # Detay bilgileri buraya eklenebilir
                'papers': yazar.makaleler,
                'connections': yazar.dict_edges
            }
        })

    # Create links
    for yazar in yazarlar:
        for coauthorname, weight in yazar.dict_edges.items():
            if coauthorname in node_map:
                links.append({
                    'source': node_map[yazar.name],
                    'target': node_map[coauthorname],
                    'value': weight
                })

    return jsonify({
        'nodes': nodes,
        'links': links
    })

@app.route("/")
def home():
    start_time = time.time()
    yazarlar,names,graph = load_authors()
    end_time = time.time()

    print(f"İşlem süresi: {end_time - start_time:.5f} saniye")

    with open("output.txt", "w", encoding="utf-8") as dosya:
        for x in yazarlar:
            dosya.write(f"{x.name} : {x.id}\n{x.makaleler}\n[")
            for i, j in x.dict_edges.items():
                dosya.write(f"' {i} : {j}  ',")
            dosya.write("]\n\n")

    return render_template('index.html', output="", graph="", current_ister=None)

@app.route('/ister/<int:number>')
def ister(number):
    output = ""
    graph = ""

    if number == 6:
        # Special case for requirement 6 - show form
        return render_template('index.html', output=output, graph=graph, current_ister=None)

    return render_template('index.html',
                           output=output,
                           graph=graph,
                           current_ister=number)


@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.json
    author_a = data.get('authorA')
    author_b = data.get('authorB')
    ister_number = data.get('isterNumber')

    print(f"İster {ister_number} alındı: {author_a}, {author_b}")
    if ister_number == 1:
        return submit_ister1(author_a, author_b)
    else :
        return submit_single_author(author_a,ister_number)


@app.route('/submit_ister1', methods=['POST'])
def submit_ister1(author_a, author_b):
    # Analiz fonksiyonunu çağır
    result = process_ister1(author_a, author_b)

    return result  # Çıktıyı doğrudan gönder


@app.route('/submit_single_author', methods=['POST'])
def submit_single_author(author_id,ister_number):
    # Analiz fonksiyonunu çağır
    result = process_single_author(author_id, ister_number)

    return result  # Çıktıyı doğrudan gönder

if __name__ == "__main__":
    app.run(debug=True)