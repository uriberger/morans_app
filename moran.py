import pandas as pd
import networkx as nx
from pyvis.network import Network
from csv import reader
import streamlit as st
import streamlit.components.v1 as components

st.title('Moran\'s app')
G = nx.Graph()
first = True
i = 0
with open('moran.csv', newline='', encoding='utf8') as csvfile:
    reader = reader(csvfile)
    for row in reader:
        if first:
            name_list = row[1:]
            G.add_nodes_from(name_list, size=5)
            first = False
        else:
            for j in range(1, 24):
                val = int(row[j])
                if val > 0:
                    G.add_edge(name_list[i], name_list[j-1], width=val)
            i += 1

st.write(pd.read_csv('moran.csv'))
clients = st.multiselect('Select clients', name_list, default=name_list)

filtered_G = G.copy()
for name in name_list:
    if name not in clients:
        filtered_G.remove_node(name)

net = Network(notebook=True)
net.from_nx(filtered_G)
net.show_buttons(filter_=['physics'])
net.show('example.html')
components.html(html=net.html, height=550)
