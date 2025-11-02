from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# example of data
RELATIONS = [
    ("Person 1", "Person 2", "#isRelatedTo"),
    ("Person 1", "Person 3", "#isRelatedTo"),
    ("Person 1", "Person 4", "#isRelatedTo"),
    ("Person 1", "Person 5", "#isRelatedTo"),
    ("Person 1", "Person 6", "#isRelatedTo")
]

@app.route("/relation")
def relation():
    # if values are passed through querystring use them;
    # otherwise use one randomly
    node_from = request.args.get("source")
    node_to = request.args.get("target")
    relation = request.args.get("relation")

    if not node_from or not node_to or not relation:
        node_from, node_to, relation = random.choice(RELATIONS)

    return render_template(
        "relation.html",
        node_from=node_from,
        node_to=node_to,
        relation=relation
    )

@app.route("/handle_decision", methods=["POST"])
def handle_decision():
    # get info from the form
    decision = request.form.get("decision")
    nodo_from = request.form.get("nodo_from")
    nodo_to = request.form.get("nodo_to")
    relation = request.form.get("relation")

    # could be saving the decision in the db
    print(f"Decisione: {decision} per {nodo_from} {relation} {nodo_to}")

    # create a new input
    new_from, new_to, new_relation = random.choice(RELATIONS)

    # redirect to the same page with new data
    return redirect(url_for(
        "relation",
        source=new_from,
        target=new_to,
        relation=new_relation
    ))

if __name__ == "__main__":
    app.run(debug=True)
