from ariadne import QueryType, graphql_sync, make_executable_schema,types
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, request, jsonify

type_defs = '''
    type Query {
        hello: String
    }
'''
query = QueryType()

@query.field("hello")
def resolve_hello(_, info):
    return "world"

shema = make_executable_schema(type_defs, query)

explorer_html = ExplorerGraphiQL().html(None)

app = Flask(__name__)

@app.route("/graphql", methods=["GET"])
def graphql_explorer():
    return explorer_html, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        shema,
        data,
        context_value={"request": request},
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(debug=True)