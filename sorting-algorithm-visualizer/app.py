import random

from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go

from algorithms import get_sorting_steps


app = Dash(
    __name__,
    prevent_initial_callbacks="initial_duplicate"
)
app.title = "Sorting Algorithm Visualizer"


def create_figure(array, comparing=None, swapping=None, sorted_indices=None):

    comparing = comparing or []
    swapping = swapping or []
    sorted_indices = sorted_indices or []

    colors = []

    for i in range(len(array)):

        if i in swapping:
            colors.append("#e74c3c")

        elif i in comparing:
            colors.append("#f1c40f")

        elif i in sorted_indices:
            colors.append("#2ecc71")

        else:
            colors.append("#3498db")

    figure = go.Figure(
        data=[
            go.Bar(
                x=list(range(len(array))),
                y=array,
                marker_color=colors,
                text=array,
                textposition="outside"
            )
        ]
    )

    figure.update_layout(
        title="Array Visualization",
        xaxis_title="Array Index",
        yaxis_title="Value",
        yaxis=dict(range=[0, max(array) + 15]),
        xaxis=dict(
            tickmode="linear",
            dtick=1
        ),
        height=500,
        margin=dict(l=50, r=30, t=70, b=50),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    return figure


initial_array = [42, 17, 85, 31, 63, 9, 54, 28, 76, 12]


app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f4f6f8",
        "minHeight": "100vh",
        "padding": "30px"
    },

    children=[

        html.Div(
            style={
                "maxWidth": "1100px",
                "margin": "auto"
            },

            children=[

                html.Div(
                    style={
                        "backgroundColor": "#1f3c88",
                        "color": "white",
                        "padding": "25px",
                        "borderRadius": "12px",
                        "textAlign": "center",
                        "marginBottom": "25px"
                    },

                    children=[

                        html.H1(
                            "Sorting Algorithm Visualizer",
                            style={
                                "margin": "0",
                                "fontSize": "32px"
                            }
                        ),

                        html.P(
                            "Visualize sorting algorithms step by step",
                            style={
                                "marginBottom": "0",
                                "fontSize": "17px"
                            }
                        )
                    ]
                ),

                html.Div(
                    style={
                        "backgroundColor": "white",
                        "padding": "25px",
                        "borderRadius": "12px",
                        "marginBottom": "25px"
                    },

                    children=[

                        html.Div(
                            style={
                                "display": "flex",
                                "gap": "15px",
                                "alignItems": "center",
                                "flexWrap": "wrap"
                            },

                            children=[

                                html.Div(
                                    children=[

                                        html.Label(
                                            "Select Algorithm",
                                            style={
                                                "fontWeight": "bold",
                                                "display": "block",
                                                "marginBottom": "7px"
                                            }
                                        ),

                                        dcc.Dropdown(
                                            id="algorithm-dropdown",

                                            options=[
                                                {
                                                    "label": "Bubble Sort",
                                                    "value": "Bubble Sort"
                                                },
                                                {
                                                    "label": "Selection Sort",
                                                    "value": "Selection Sort"
                                                },
                                                {
                                                    "label": "Insertion Sort",
                                                    "value": "Insertion Sort"
                                                }
                                            ],

                                            value="Bubble Sort",
                                            clearable=False,
                                            style={
                                                "width": "220px"
                                            }
                                        )
                                    ]
                                ),

                                html.Button(
                                    "Generate Random Array",
                                    id="generate-btn",
                                    n_clicks=0,
                                    style={
                                        "backgroundColor": "#3498db",
                                        "color": "white",
                                        "border": "none",
                                        "padding": "12px 18px",
                                        "borderRadius": "7px",
                                        "cursor": "pointer"
                                    }
                                ),

                                html.Button(
                                    "Start Sorting",
                                    id="start-btn",
                                    n_clicks=0,
                                    style={
                                        "backgroundColor": "#27ae60",
                                        "color": "white",
                                        "border": "none",
                                        "padding": "12px 18px",
                                        "borderRadius": "7px",
                                        "cursor": "pointer"
                                    }
                                ),

                                html.Button(
                                    "Reset",
                                    id="reset-btn",
                                    n_clicks=0,
                                    style={
                                        "backgroundColor": "#e74c3c",
                                        "color": "white",
                                        "border": "none",
                                        "padding": "12px 18px",
                                        "borderRadius": "7px",
                                        "cursor": "pointer"
                                    }
                                )
                            ]
                        ),

                        html.Br(),

                        html.Label(
                            "Sorting Speed",
                            style={
                                "fontWeight": "bold"
                            }
                        ),

                        dcc.Slider(
                            id="speed-slider",
                            min=100,
                            max=1000,
                            step=100,
                            value=500,

                            marks={
                                100: "Fast",
                                500: "Medium",
                                1000: "Slow"
                            }
                        )
                    ]
                ),

                html.Div(
                    style={
                        "backgroundColor": "white",
                        "padding": "15px",
                        "borderRadius": "12px"
                    },

                    children=[

                        dcc.Graph(
                            id="sorting-graph",
                            figure=create_figure(initial_array)
                        )
                    ]
                ),

                html.Div(
                    id="status-message",

                    children="Ready to sort!",

                    style={
                        "textAlign": "center",
                        "fontSize": "18px",
                        "fontWeight": "bold",
                        "marginTop": "20px"
                    }
                ),

                dcc.Interval(
                    id="animation-interval",
                    interval=500,
                    n_intervals=0,
                    disabled=True
                ),

                dcc.Store(
                    id="array-store",
                    data=initial_array
                ),

                dcc.Store(
                    id="steps-store",
                    data=[]
                ),

                dcc.Store(
                    id="step-index-store",
                    data=0
                )
            ]
        )
    ]
)


# ---------------------------------------
# Generate / Reset
# ---------------------------------------

@app.callback(

    Output("array-store", "data"),

    Output(
        "sorting-graph",
        "figure"
    ),

    Output(
        "steps-store",
        "data"
    ),

    Output(
        "step-index-store",
        "data"
    ),

    Output(
        "animation-interval",
        "disabled"
    ),

    Output(
        "status-message",
        "children"
    ),

    Input("generate-btn", "n_clicks"),

    Input("reset-btn", "n_clicks"),

    prevent_initial_call=True
)
def generate_or_reset(generate_clicks, reset_clicks):

    new_array = [
        random.randint(10, 100)
        for _ in range(10)
    ]

    return (
        new_array,
        create_figure(new_array),
        [],
        0,
        True,
        "New array generated!"
    )


# ---------------------------------------
# Start Sorting
# ---------------------------------------

@app.callback(

    Output(
        "steps-store",
        "data",
        allow_duplicate=True
    ),

    Output(
        "step-index-store",
        "data",
        allow_duplicate=True
    ),

    Output(
        "animation-interval",
        "disabled",
        allow_duplicate=True
    ),

    Output(
        "status-message",
        "children",
        allow_duplicate=True
    ),

    Input("start-btn", "n_clicks"),

    State("array-store", "data"),

    State("algorithm-dropdown", "value"),

    prevent_initial_call=True
)
def start_sorting(n_clicks, array, algorithm):

    steps = get_sorting_steps(
        array,
        algorithm
    )

    return (
        steps,
        0,
        False,
        f"{algorithm} started..."
    )


# ---------------------------------------
# Animation
# ---------------------------------------

@app.callback(

    Output(
        "sorting-graph",
        "figure",
        allow_duplicate=True
    ),

    Output(
        "step-index-store",
        "data",
        allow_duplicate=True
    ),

    Output(
        "animation-interval",
        "disabled",
        allow_duplicate=True
    ),

    Output(
        "status-message",
        "children",
        allow_duplicate=True
    ),

    Input(
        "animation-interval",
        "n_intervals"
    ),

    State(
        "steps-store",
        "data"
    ),

    State(
        "step-index-store",
        "data"
    ),

    prevent_initial_call=True
)
def update_animation(
    n_intervals,
    steps,
    step_index
):

    if not steps:

        return (
            create_figure(initial_array),
            0,
            True,
            "No sorting steps available."
        )

    if step_index >= len(steps):

        final_step = steps[-1]

        figure = create_figure(
            final_step["array"],
            final_step.get("comparing", []),
            final_step.get("swapping", []),
            final_step.get("sorted", [])
        )

        return (
            figure,
            step_index,
            True,
            "Sorting completed!"
        )

    step = steps[step_index]

    figure = create_figure(
        step["array"],
        step.get("comparing", []),
        step.get("swapping", []),
        step.get("sorted", [])
    )

    next_index = step_index + 1

    if next_index >= len(steps):

        return (
            figure,
            next_index,
            True,
            "Sorting completed!"
        )

    return (
        figure,
        next_index,
        False,
        f"Sorting... Step {next_index} / {len(steps)}"
    )


# ---------------------------------------
# Speed
# ---------------------------------------

@app.callback(

    Output(
        "animation-interval",
        "interval"
    ),

    Input(
        "speed-slider",
        "value"
    )
)
def change_speed(speed):

    return speed


# ---------------------------------------
# Run
# ---------------------------------------

if __name__ == "__main__":

    app.run(debug=True)
