from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from backend.solver_logic import CP_solver_setup, get_all_solutions
import webbrowser
import threading

move_transition = np.array([ 
#   [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#   [ R,R2,R', L,L2,L', r,r2,r', l,l2,l', M,M2,M', U,U2,U', D,D2,D', u,u2,u', d,d2,d', E,E2,E', F,F2,F', B,B2,B', f,f2,f', b,b2,b', S,S2,S'],
    [ 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 1, 1, 1], # 1. Standard
    [ 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2], # 2. Standard
])


app = Flask(__name__)

# Dictionary to map user-friendly mode names to actual mode settings
MODE_SETTINGS = {
    "FB": {"search_depth": 4, "table_depth": 4},
    "FB_D": {"search_depth": 4, "table_depth": 4},
    "Line": {"search_depth": 3, "table_depth": 3},
    "DLcorners": {"search_depth": 2, "table_depth": 3},
    "223": {"search_depth": 5, "table_depth": 5},
    "223+EO": {"search_depth": 6, "table_depth": 6},
}

# Global solver variables
search_algs = None
table = None
mode = None

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/initialize", methods=["POST"])
def initialize_solver():
    global search_algs, table, mode

    mode = request.form["mode"]
    settings = MODE_SETTINGS.get(mode, {"search_depth": 4, "table_depth": 4})
    search_depth = settings["search_depth"]
    table_depth = settings["table_depth"]

    # Display message while initializing
    print("Initiating solver with mode:", mode)

    # Run solver setup
    search_algs, table = CP_solver_setup(
        mode, search_depth, table_depth, move_transition=move_transition, start_grips=np.array([1]), skip_U=True, prnt=False
    )
    print(len(search_algs), "algorithms loaded.")
    print(len(table), "table entries loaded.")

    print("Solver initialized. Redirecting to solve page.")
    return redirect(url_for("solve"))

@app.route("/solve", methods=["GET", "POST"])
def solve():
    global search_algs, table, mode

    if request.method == "POST":
        orientation = request.form["orientation"]
        neutrality = request.form["neutrality"]
        scramble = request.form["scramble"]

        # Store in global variables
        global last_orientation, last_neutrality, last_scramble
        last_orientation = orientation
        last_neutrality = neutrality
        last_scramble = scramble

        print("Solving:", scramble)
        print("Orientation:", orientation)
        print("Neutrality:", neutrality)
        print("Mode:", mode)
        solves = get_all_solutions(scramble, mode, search_algs, table, orientation, neutrality)

        # Sort solutions
        def sort_solves(solves):
            solves.sort(key=lambda x: x.count("S") + x.count("M") + x.count("E"))
            solves.sort(key=lambda x: (len(x.split(" ")) - (x.count("x") + x.count("y") + x.count("z"))) ) # TODO: Fix this to sort by actual moves (?)
            solves.sort(key=lambda x: x.count("f") + x.count("F"))
            return solves

        solves = sort_solves(solves)

        return render_template(
            "solve.html",
            mode=mode,
            orientation=orientation,
            neutrality=neutrality,
            scramble=scramble,
            output_list=solves
        )

    return render_template(
        "solve.html",
        mode=mode,
        orientation=last_orientation if "last_orientation" in globals() else "",
        neutrality=last_neutrality if "last_neutrality" in globals() else "x2y",  # Default to x2y
        scramble=last_scramble if "last_scramble" in globals() else ""
    )



def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()  # Delay to allow Flask to start
    app.run()