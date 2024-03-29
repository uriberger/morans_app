import csv
import torch
import pandas as pd
import networkx as nx
from pyvis.network import Network
from csv import reader
import streamlit as st
import streamlit.components.v1 as components

st.title('Moran\'s app')
G = nx.Graph()
# r = csv.reader(open('moran.csv', encoding='utf8'))  # Here your csv file
# lines = list(r)
# torch.save(lines, 'moran.data')
data = torch.load('moran.data')

name_list = data[0][1:]
G.add_nodes_from(name_list, size=5)

for i in range(1, len(data)):
    for j in range(1, 24):
        val = int(data[i][j])
        if val > 0:
            G.add_edge(name_list[i-1], name_list[j-1], width=val)
    i += 1

# st.write(pd.read_csv('moran.csv'))
client_for_changing = st.selectbox('Choose client for name changing', name_list)
new_name = st.text_input('Change the name of ' + str(client_for_changing) + ' to:')
if new_name != '':
    client_ind = [i for i in range(len(name_list)) if client_for_changing == name_list[i]][0]
    data[0][client_ind + 1] = new_name
    data[client_ind][0] = new_name
    torch.save(data, 'moran.data')
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
