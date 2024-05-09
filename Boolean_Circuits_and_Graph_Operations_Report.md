# Project Report: Boolean Circuits and Graph Operations

## Introduction
This project comprises several Python modules providing tools to work with boolean circuits, matrix operations, and open directed graphs (digraphs). Each module specializes in specific tasks like graph representation, node management, and circuit operations. This report offers a detailed overview of each module and its functions.

## Modules Overview and Key Functions

For reference, this photo of a class diagram shows the dependencies between the files and therefore its organisation.

### `__init__.py`
This file acts as an initializer for the package, but it does not contain any custom functions or classes.

### `bool_circ.py`
This module focuses on boolean circuits and contains the following functions:

1. **`__init__`**  
   Initializes the `bool_circ` class, setting up the circuit's internal data structures.

2. **`is_well_formed`**  
   Validates whether the current boolean circuit is well-formed.

3. **`insert_node`**  
   Inserts a new node into the circuit at a specified location.

4. **`add_copy_node`**  
   Adds a "copy" node to the circuit, duplicating the input signal.

5. **`add_and_node`**  
   Adds an "AND" node that outputs a logical AND of its inputs.

6. **`add_or_node`**  
   Adds an "OR" node that outputs a logical OR of its inputs.

7. **`add_not_node`**  
   Adds a "NOT" node that inverts the input signal.

8. **`add_xor_node`**  
   Adds an "XOR" node that outputs a logical XOR of its inputs.

9. **`add_constant_node`**  
   Adds a node that always outputs a constant logical value (0 or 1).

10. **`identity`**  
    Checks if two boolean circuits are identical.

11. **`parse_parentheses`**  
    Parses a circuit defined with parentheses notation into a boolean circuit object.

12. **`random_circ_bool`**  
    Generates a random boolean circuit with the specified number of nodes.

13. **`adder_helper`**  
    Helper function for adding two boolean circuits.

14. **`adder`**  
    Adds two boolean circuits using logical addition.

15. **`half_adder`**  
    Implements a half-adder circuit using logical gates.

16. **`create_registre`**  
    Creates a register with the specified configuration.

17. **`copy_gate`**  
    Implements a "copy" logical gate.

18. **`not_gate`**  
    Implements a "NOT" logical gate.

19. **`and_gate`**  
    Implements an "AND" logical gate.

20. **`or_gate`**  
    Implements an "OR" logical gate.

21. **`xor_gate`**  
    Implements an "XOR" logical gate.

22. **`neutral_element`**  
    Returns a circuit with a neutral element.

23. **`evaluate`**  
    Evaluates the boolean circuit and returns the logical output.

24. **`encodeur_4bits`**  
    Implements a 4-bit encoder circuit.

25. **`decodeur_7bits`**  
    Implements a 7-bit decoder circuit.

26. **`assoc_xor`**  
    Checks the associativity of XOR logical gates.

27. **`assoc_and`**  
    Checks the associativity of AND logical gates.

28. **`assoc_or`**  
    Checks the associativity of OR logical gates.

29. **`assoc_copy`**  
    Checks the associativity of copy logical gates.

30. **`involution_xor`**  
    Checks the involution property of XOR logical gates.

31. **`effacement`**  
    Validates the logical circuit's effacement.

32. **`not_xor`**  
    Validates if NOT and XOR logical gates satisfy specific logical constraints.

33. **`not_copy`**  
    Checks specific logical constraints involving NOT and copy logical gates.

34. **`involution_not`**  
    Validates the involution property of NOT logical gates.

35. **`transform_circuit`**  
    Transforms the boolean circuit into another logical representation.

36. **`transform_once`**  
    Applies a single transformation to the circuit.

37. **`calculate`**  
    Computes logical results based on the circuit's nodes.

38. **`perturbe_bit`**  
    Randomly perturbs a single bit in a logical circuit.

39. **`CL_4bit`**  
    Implements a 4-bit carry-lookahead adder circuit.

40. **`CLA_4bit`**  
    Implements a 4-bit carry-lookahead adder.

41. **`CLA_helper`**  
    Helper function for the carry-lookahead adder.

42. **`CLA_adder`**  
    Implements a carry-lookahead adder circuit.

43. **`convert_to_binary_string`**  
    Converts the circuit's results to a binary string.

44. **`find_bigger_2_pow`**  
    Finds the next largest power of 2 given a number.

45. **`add_registre_CLA`**  
    Adds a carry-lookahead adder register to the circuit.

46. **`add_CLA`**  
    Adds a carry-lookahead adder to the circuit.

47. **`add_registre_naive`**  
    Adds a naive register circuit to the boolean circuit.

48. **`add_naive`**  
    Implements a naive addition operation in the boolean circuit.

49. **`check_invarients`**  
    Verifies that the circuit satisfies specific invariants.

### `matrix_operations.py`
This module provides various matrix operations and contains the following functions:

1. **`random_int_list`**  
   Generates a list of random integers.

2. **`random_int_matrix`**  
   Generates a random matrix of integers.

3. **`random_symetric_int_matrix`**  
   Generates a random symmetric matrix of integers.

4. **`random_oriented_int_matrix`**  
   Generates a random oriented matrix of integers.

5. **`random_dag_int_matrix`**  
   Generates a random directed acyclic graph (DAG) matrix.

6. **`print_m`**  
   Prints the given matrix in a human-readable format.

7. **`identity_matrix`**  
   Creates an identity matrix of the given size.

8. **`copy_matrix`**  
   Returns a copy of the given matrix.

9. **`degree_matrix`**  
   Computes the degree matrix for the given adjacency matrix.

10. **`laplacian`**  
    Computes the Laplacian matrix for the given adjacency matrix.

11. **`swap_rows`**  
    Swaps two rows in the given matrix.

12. **`scale_row`**  
    Scales a row in the matrix by a specified factor.

13. **`add_scaled_row`**  
    Adds a scaled version of one row to another in the given matrix.

14. **`gauss`**  
    Applies Gaussian elimination to the given matrix.

15. **`rank`**  
    Calculates the rank of the given matrix.

16. **`kernel_dim`**  
    Determines the dimension of the kernel of the given matrix.

### `node.py`
This module manages nodes within graphs, circuits, and other structures. It contains several classes and functions:

#### Classes
- **`copy_node` Class**  
  Represents a copy node in a graph structure.

- **`and_node` Class**  
  Represents an AND node in a graph structure.

- **`or_node` Class**  
  Represents an OR node in a graph structure.

- **`not_node` Class**  
  Represents a NOT node in a graph structure.

- **`xor_node` Class**  
  Represents an XOR node in a graph structure.

- **`constant_node` Class**  
  Represents a constant node in a graph structure.

#### Functions

1. **`__init__`**  
   Initializes a node with an ID, label, and optional lists of input and output edges.

2. **`copy`**  
   Creates a copy of the node.

3. **`indegree`**  
   Calculates the indegree (number of incoming edges) of a node.

4. **`outdegree`**  
   Calculates the outdegree (number of outgoing edges) of a node.

5. **`degree`**  
   Calculates the total degree (sum of indegree and outdegree) of a node.

6. **`is_copy`**  
   Determines if the node is a copy node.

7. **`is_or`**  
   Determines if the node is an OR node.

8. **`is_and`**  
   Determines if the node is an AND node.

9. **`is_not`**  
   Determines if the node is a NOT node.

10. **`is_xor`**  
    Determines if the node is an XOR node.

11. **`is_constant`**  
    Determines if the node is a constant node.

12. **`transform`**  
    Applies a transformation to the node.

### `open_digraph.py`
This module manages open directed graphs and contains the following functions and classes:

#### Classes
- **`open_digraph` Class**  
  Represents an open directed graph with nodes and edges.

#### Functions

1. **`graph_from_adjacency_matrix`**  
   Creates a graph based on the given adjacency matrix.

2. **`__init__`**  
   Initializes an empty graph or one with given nodes and edges.

3. **`__eq__`**  
   Determines whether two graphs are equal by comparing their nodes and edges.

4. **`__ne__`**  
   Determines whether two graphs are not equal.

5. **`empty`**  
   Returns an empty graph.

6. **`add_input_id`**  
   Adds a node to the graph's input list.

7. **`add_output_id`**  
   Adds a node to the graph's output list.

8. **`new_id`**  
   Generates a new unique node ID.

9. **`add_edge`**  
   Adds an edge between two nodes.

10. **`add_edges`**  
    Adds multiple edges between node pairs.

11. **`add_node`**  
    Adds a new node to the graph.

12. **`remove_edge`**  
    Removes an edge between two nodes.

13. **`remove_parallel_edges`**  
    Removes all parallel edges between a pair of nodes.

14. **`remove_node_by_id`**  
    Removes a node by its ID and updates the graph.

15. **`remove_edges`**  
    Removes multiple edges between pairs of nodes.

16. **`remove_nodes_by_id`**  
    Removes multiple nodes from the graph by their IDs.

17. **`is_well_formed`**  
    Checks whether the graph is well-formed.

18. **`add_input_node`**  
    Adds an input node to the graph.

19. **`add_output_node`**  
    Adds an output node to the graph.

20. **`copy`**  
    Creates a deep copy of the graph.

21. **`__str__`**  
    Returns a string representation of the graph.

22. **`__repr__`**  
    Returns a string representation for debugging.

23. **`id_map`**  
    Maps node IDs between two graphs.

24. **`adjacency_matrix`**  
    Returns the adjacency matrix representation of the graph.

25. **`random`**  
    Generates a random graph based on the given parameters.

26. **`save_as_dot_file`**  
    Saves the graph in the DOT format.

27. **`display_graph`**  
    Displays the graph using Graphviz.

28. **`from_dot_file`**  
    Loads a graph from a DOT file.

29. **`is_acyclic`**  
    Determines if the graph is acyclic.

30. **`dfs`**  
    Performs a depth-first search on the graph.

31. **`identity`**  
    Returns an identity graph.

32. **`component_list`**  
    Returns a list of all components in the graph.

33. **`merge_nodes`**  
    Merges two or more nodes into one.

### `open_digraph_composition_mx.py`
This module focuses on matrix representations for graph composition operations and contains the following functions:

1. **`min_id`**  
   Returns the minimum node ID in the graph.

2. **`max_id`**  
   Returns the maximum node ID in the graph.

3. **`shift_indices`**  
   Shifts the indices of all nodes in the graph by a specified amount.

4. **`shift_keys`**  
   Shifts the keys of all nodes in the graph's data structure.

5. **`iparallel`**  
   Performs an in-place parallel composition of two graphs.

6. **`parallel`**  
   Returns a parallel composition of two graphs.

7. **`icompose`**  
   Performs an in-place composition of two graphs.

8. **`compose`**  
   Returns a composition of two graphs.

9. **`connected_components`**  
   Returns the connected components of a graph.

10. **`dfs`**  
    Performs a depth-first search on the graph.

### `open_digraph_paths_distance_mx.py`
This module handles path and distance calculations using matrix operations and contains the following functions:

1. **`dijkstra`**  
   Finds the shortest path from a source node to all other nodes using Dijkstra's algorithm.

2. **`shortest_path`**  
   Returns the shortest path between two nodes.

3. **`distances_from_common_ancestors`**  
   Computes distances from a given node to common ancestors.

4. **`topological_sort`**  
   Arranges nodes in topological order in a directed acyclic graph.

5. **`get_coleave`**  
   Returns a list of nodes that have no common descendants.

6. **`depth_node_acyclic_knowing_Topological_sort`**  
   Returns the depth of a node, assuming the graph is sorted topologically.

7. **`depth_node_acyclic`**  
   Calculates the depth of a node in an acyclic graph.

8. **`depth_acyclic`**  
   Computes the depth of an acyclic graph.

9. **`longest_path`**  
   Determines the longest path between two nodes in a directed acyclic graph.


## Conclusion
This project provides a robust suite of tools for working with boolean circuits, matrix operations, and open directed graphs. Each module is carefully designed to encapsulate key computational operations, allowing for efficient manipulation and analysis of these data structures. Further development in optimization and Implementation of more graph algorithms (e.g., Bellman-Ford for shortest paths) and more circuit gates could expand the project's reach and applicability.

