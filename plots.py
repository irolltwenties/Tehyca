# -*- coding: utf-8 -*-
import plotly

def draw_main(calculated_data_array):
    drawing = plotly.graph_objs.Figure()
    drawing.add_trace(plotly.graph_objs.Scatter(
        x = calculated_data_array[:len(calculated_data_array)], \
            y = calculated_data_array[0])
        )
    drawing.add_trace(plotly.graph_objs.Scatter(
        x = calculated_data_array[:len(calculated_data_array)], \
            y = calculated_data_array[:1])
        )
    drawing.add_trace(plotly.graph_objs.Scatter(
        x = calculated_data_array[:len(calculated_data_array)], \
            y = calculated_data_array[:3])
        )
    return drawing