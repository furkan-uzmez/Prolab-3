import base64
from flask import Flask, render_template, request, jsonify
import time
from bst import BSTVisualizer,convert_bst_to_json
from main import load_authors, process_ister1, process_single_author
from flask_cors import CORS

global temp_bst
global temp_path
global temp_idler

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

@app.route('/api/graph-data')
def get_graph_data():
    global temp_idler
    yazarlar,idler,graph = load_authors()
    nodes = []
    links = []
    node_map = {}
    temp_idler = idler

    # Create nodes
    for i, yazar in enumerate(yazarlar):
        node_map[yazar.id] = i
        nodes.append({
            'id': i,
            'name': yazar.name,
            'orcid': yazar.id,
            'group': 1,  # You can modify grouping based on your needs
            'papers': len(yazar.makaleler),
            'details': {  # Detay bilgileri buraya eklenebilir
                'papers': yazar.makaleler,
                'connections': yazar.dict_edges_names
            }
        })

    # Create links
    for yazar in yazarlar:
        for coauthorid, weight in yazar.dict_edges.items():
            if coauthorid in node_map:
                links.append({
                    'source': node_map[yazar.id],
                    'target': node_map[coauthorid],
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
            for i, j in x.dict_edges_names.items():
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
        result = submit_ister1(author_a, author_b)
        print('Result :',result)
        return result
    else :
        return submit_single_author(author_a,ister_number)


@app.route('/submit_ister1',methods=['POST'])
def submit_ister1(author_a, author_b):
    global temp_bst
    global temp_path

    result,path,bst = process_ister1(author_a, author_b)
    temp_bst = bst
    temp_path = path
    print("Path :", path)
    print("Temp_bst:", temp_bst)
    return jsonify({'result': result, 'path': path})  # Çıktıyı doğrudan gönder

@app.route('/submit_single_author', methods=['POST'])
def submit_single_author(author_id,ister_number):
    global temp_bst
    global temp_path
    # Analiz fonksiyonunu çağır
    if ister_number == 3:
        print("İndex:",temp_path.index(author_id))
        print("Temp_bst:")
        temp_bst.Print(temp_bst.root)
        temp_bst.root = temp_bst.Remove(temp_bst.root,temp_path.index(author_id))
        temp_path.remove(author_id)
        print("Temp_bst:")
        temp_bst.Print(temp_bst.root)
        return handle_bst(temp_bst,f"{temp_idler[author_id].name} çıkarıldı")
    else:
        result, path = process_single_author(author_id, ister_number)
        return jsonify({'result': result, 'path': path})


#BST visualization
def handle_bst(temp_bst,message):

    if temp_bst is None:
        return jsonify({'status': 'error', 'message': 'No BST data available'})

    # Check Accept header
    accept_header = request.headers.get('Accept', '')

    try:
        visualizer = BSTVisualizer()

        if 'application/json' in accept_header:
            # Return JSON representation
            tree_data = convert_bst_to_json(temp_bst.root)
            return jsonify({
                'status': 'success',
                 'tree': tree_data,
                'message': message
              })
        else:
            # Return PNG image with base64 encoding
            png_buffer = visualizer.visualize_to_png(temp_bst)
            base64_image = base64.b64encode(png_buffer.getvalue()).decode('utf-8')
            return jsonify({
                'status': 'success',
                'image': f'data:image/png;base64,{base64_image}',
                'message': message
            })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == "__main__":
    app.run(debug=True)