import copy

class Node:
    """
    Rappresenta un nodo nella rete.
    Ogni nodo mantiene una lista dei suoi vicini e una tabella di routing.
    """
    def __init__(self, name):
        self.name = name
        self.neighbors = {}  # Dizionario {nome_vicino: costo_link}
        self.routing_table = {}  # Dizionario {destinazione: (costo, next_hop)}

    def add_neighbor(self, neighbor, cost):
        """
        Aggiunge un vicino al nodo con il costo specificato.
        Inizializza la tabella di routing con il costo del collegamento al vicino.
        """
        self.neighbors[neighbor] = cost
        self.routing_table[neighbor] = (cost, neighbor)

    def initialize_routing_table(self, all_nodes):
        """
        Inizializza la tabella di routing per tutti i nodi della rete.
        Imposta il costo verso se stesso a 0 e verso gli altri nodi a infinito se non direttamente connessi.
        """
        for node in all_nodes:
            if node != self.name and node not in self.routing_table:
                self.routing_table[node] = (float('inf'), None)
        self.routing_table[self.name] = (0, self.name)

    def send_routing_table(self):
        """
        Restituisce una copia della tabella di routing per inviarla ai vicini.
        """
        return copy.deepcopy(self.routing_table)

    def update_routing_table(self, neighbor, neighbor_table):
        """
        Aggiorna la tabella di routing basandosi sulle informazioni ricevute da un vicino.
        Restituisce True se la tabella è stata aggiornata, False altrimenti.
        """
        updated = False
        cost_to_neighbor = self.neighbors[neighbor]
        
        for destination, (neighbor_cost, neighbor_next_hop) in neighbor_table.items():
            if destination == self.name:
                continue  # Ignora se la destinazione è se stesso
            # Calcola il nuovo costo tramite il vicino
            new_cost = cost_to_neighbor + neighbor_cost
            current_cost, current_next_hop = self.routing_table.get(destination, (float('inf'), None))
            if new_cost < current_cost:
                self.routing_table[destination] = (new_cost, neighbor)
                updated = True
        return updated

    def print_routing_table(self):
        """
        Stampa la tabella di routing del nodo in modo leggibile.
        """
        print(f"Routing table for Node {self.name}:")
        print("Destination\tCost\tNext Hop")
        for destination, (cost, next_hop) in sorted(self.routing_table.items()):
            cost_display = "∞" if cost == float('inf') else cost
            next_hop_display = "-" if next_hop is None else next_hop
            print(f"{destination}\t\t{cost_display}\t{next_hop_display}")
        print("\n")


class Network:
    """
    Rappresenta la rete composta da più nodi.
    Gestisce l'aggiunta di nodi e link, l'inizializzazione delle tabelle di routing,
    e l'esecuzione dell'algoritmo di Distance Vector Routing.
    """
    def __init__(self):
        self.nodes = {}  # Dizionario {nome_nodo: oggetto_Node}

    def add_node(self, node_name):
        """
        Aggiunge un nodo alla rete se non esiste già.
        """
        if node_name not in self.nodes:
            self.nodes[node_name] = Node(node_name)

    def add_link(self, node1, node2, cost):
        """
        Aggiunge un collegamento bidirezionale tra node1 e node2 con il costo specificato.
        """
        self.add_node(node1)
        self.add_node(node2)
        self.nodes[node1].add_neighbor(node2, cost)
        self.nodes[node2].add_neighbor(node1, cost)

    def initialize_routing_tables(self):
        """
        Inizializza le tabelle di routing per tutti i nodi nella rete.
        """
        all_nodes = self.nodes.keys()
        for node in self.nodes.values():
            node.initialize_routing_table(all_nodes)

    def distance_vector_routing(self):
        """
        Esegue l'algoritmo di Distance Vector Routing fino alla convergenza.
        Stampa le tabelle di routing ad ogni iterazione.
        """
        self.initialize_routing_tables()
        iteration = 0
        while True:
            print(f"--- Iteration {iteration} ---")
            updated = False
            # Step 1: Ogni nodo invia la propria tabella di routing ai vicini
            sent_tables = {node.name: node.send_routing_table() for node in self.nodes.values()}
            # Step 2: Ogni nodo aggiorna la propria tabella basandosi sulle tabelle ricevute dai vicini
            for node in self.nodes.values():
                for neighbor in node.neighbors:
                    neighbor_table = sent_tables[neighbor]
                    if node.update_routing_table(neighbor, neighbor_table):
                        updated = True
            # Step 3: Stampa le tabelle di routing attuali
            for node in self.nodes.values():
                node.print_routing_table()
            if not updated:
                print("Convergenza raggiunta.\n")
                break
            iteration += 1

    def print_final_routing_tables(self):
        """
        Stampa le tabelle di routing finali per tutti i nodi nella rete.
        """
        print("--- Routing Tables Finali ---")
        for node in self.nodes.values():
            node.print_routing_table()


def main():
    """
    Funzione principale che definisce la topologia della rete, esegue il protocollo di routing
    e stampa le tabelle di routing finali.
    """
    # Creazione della rete
    network = Network()

    # Definizione delle connessioni (esempio)
    # Supponiamo una rete con 4 nodi: A, B, C, D
    network.add_link('A', 'B', 1)
    network.add_link('A', 'C', 4)
    network.add_link('B', 'C', 2)
    network.add_link('B', 'D', 5)
    network.add_link('C', 'D', 1)
    
    # Esecuzione del protocollo di routing
    network.distance_vector_routing()
    
    # Stampa delle tabelle di routing finali
    network.print_final_routing_tables()


if __name__ == "__main__":
    main()
