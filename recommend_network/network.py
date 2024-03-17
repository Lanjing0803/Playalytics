#Below is an example of creating networks for keywords
import networkx as nx
import matplotlib.pyplot as plt

co_occurrence_matrix = {
    "kingdom": {
        "system": 2.0,
     
    },
    "battle": {
        "system": 2.0,
       
        "player": 1.0,
     
    },
    "adventure": {
        "system": 2.0,
      
        "action": 2.0,
      
    },
    "system": {
      
        "kingdom": 2.0,
    
        "battle": 2.0,
        "adventure": 2.0,
    
    },
    "fantasy": {
      
        "classic": 2.0,
        "battle": 1.0,
       
        "action": 1.0,
     
        "experience": 1.0,
      
    },
    "classic": {
      
        "fantasy": 2.0,
    },
    "experience": {
      
        "fantasy": 1.0,

    },
    "action": {
       
        "fantasy": 1.0,
        "adventure": 2.0,
       
        "journey": 1.0,
    },
    "player": {
       
        "battle": 1.0,
      
        "horror": 2.0,
      
        "journey": 1.0,
    },
    "journey": {
      
        "action": 1.0,
      
        "player": 1.0,
     
    },
    "horror": {
      
        "multiplayer": 2.0,
     
        "player": 2.0,
   
    },
    "multiplayer": {
       "horror": 2.0,
        "experience": 1.0,
         },
    "survive": {
        "fight": 1.0,
          },
    "war": {
         "pc": 1.0,
       },
    "fight": {
        "survive": 1.0,
          "war": 1.0
    },
    "pc": {
              "story": 1.0,
            "war": 1.0
    },
    "story": {
            "pc": 1.0,
         }
}

G = nx.DiGraph()

for source, targets in co_occurrence_matrix.items():
    for target, weight in targets.items():
        G.add_edge(source, target, weight=weight)

pos = nx.spring_layout(G)

nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=7, font_weight='bold', edge_color='gray')

edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title('Word Co-occurrence Network')
plt.show()
