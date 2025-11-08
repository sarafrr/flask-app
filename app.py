#%%
from flask import Flask, render_template, request, redirect, url_for
import os

from utils.utils import *
from constants import *

file_name = 'statements_and_metrics_UNSEEN_PROJECTED_mod.json'
file_path = os.path.join(DATA_PATH, file_name)

statements_metrics = load_data(file_path)

RELATIONS = []
for sm in statements_metrics:
    if 'src_label' in sm and 'dest_label' in sm:
        RELATIONS.append((sm['src_label'], sm['dest_label'], '#isRelatedTo', sm['properties']['probability']))

IDX_REL = 0
#%%
app = Flask(__name__)
#%%

@app.route("/relation")
def relation():
    global RELATIONS
    # if values are passed through querystring use them;
    # otherwise use one randomly
    node_from = request.args.get("source")
    node_to = request.args.get("target")
    relation = request.args.get("relation")
    probability = request.args.get("probability")

    if not node_from or not node_to or not relation:
        node_from, node_to, relation, probability = RELATIONS[0]
    
    probability = round(float(probability), 2)

        
    return render_template(
        "relation.html",
        node_from=node_from,
        node_to=node_to,
        relation=relation,
        probability=probability
    )

@app.route("/handle_decision", methods=["POST"])
def handle_decision():
    global IDX_REL
    # get info from the form
    decision = request.form.get("decision")
    nodo_from = request.form.get("nodo_from")
    nodo_to = request.form.get("nodo_to")
    relation = request.form.get("relation")

    # could be saving the decision in the db
    print(f"Decision: {decision} per {nodo_from} {relation} {nodo_to}")

    # create a new input
    new_from, new_to, new_relation, probability = RELATIONS[IDX_REL]
    probability = round(float(probability), 2)
    if IDX_REL < len(RELATIONS)-1:
        IDX_REL += 1
    else:
        IDX_REL = 0
    # redirect to the same page with new data
    return redirect(url_for(
        "relation",
        source=new_from,
        target=new_to,
        relation=new_relation,
        probability=probability
    ))

if __name__ == "__main__":
    app.run(debug=True)
