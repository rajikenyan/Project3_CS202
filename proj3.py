from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(order=True, frozen=True)
class Node:
    freq: int
    char: str
    left: Node | None = None
    right: Node | None  = None

    def __str__(self):
        return f"Node: {self.char}, Freq: {self.freq}"

    def smaller_than(self, other: Node)->bool:
        """
        During Huffman tree building, merged nodes have more than one char.
        Tie breaker: merged nodes with longer lenght (depth) are greater.
        """
        if self.freq < other.freq:
            return True
        elif self.freq == other.freq:
             """
             if len(self.char) < len(other.char):
                  return True
             elif len(self.char) == len(other.char):
                  return self.char < other.char 
             else:
                   return False
             """
             return self.char < other.char
        return False


@dataclass(frozen=True)
class MinHeap:
    data: list[Node] = field(default_factory=list)

    def size(self)->int:
        return len(self.data)

    def get(self, index)->int:
        return self.data[index].freq

    def get_node(self, index)->int:
        return self.data[index]



def heap_replace(heap:MinHeap, index, node:Node)->MinHeap:
    new_node = Node(node.freq, node.char, node.left, node.right)
    new_heap = MinHeap(heap.data[:index]+ [new_node] + heap.data[index+1:])
    return new_heap

def heapify_up(heap: MinHeap, index: int) -> MinHeap:
    new_heap = heap
    # The loop does the "up" part
    for i in range(index, -1, -1):
        new_heap = heapify_down(new_heap, i)

    return new_heap


def insert(heap: MinHeap, element: Node) -> MinHeap:
    last = len(heap.data) ## Where you need to add
    new_heap_data = [element if i == last else heap.data[i] for i in range(0, last+1)]
    new_heap = MinHeap(new_heap_data)
    return heapify_up(new_heap, last)

def heapify_down(heap: MinHeap, index: int) -> MinHeap: 
  # Find the smallest among root, left child, and right child
   smallest = index  
   left = 2 * index + 1
   right = 2 * index + 2
   """
   if left < heap.size() and heap.get(left) < heap.get(smallest):
       smallest = left
   if right < heap.size() and heap.get(right) < heap.get(smallest):
       smallest = right
   """

   smallest_node = heap.get_node(smallest)

   if left < heap.size():
       left_node = heap.get_node(left)
       if left_node.smaller_than(smallest_node):  #left_node < smallest_node
            smallest = left
            smallest_node = heap.get_node(smallest)

   if right < heap.size():
       right_node = heap.get_node(right)    
       if right_node.smaller_than(smallest_node): #right_node < smallest_node
            smallest = right

   # Swap and continue heapifying if root is not the smallest
   if smallest != index:
       # Replace node at smallest with that at index and vice-versa
       node_smallest = heap.get_node(smallest)
       node_index = heap.get_node(index)
       new_heap = heap_replace(heap, index, node_smallest)
       new_heap2 = heap_replace(new_heap, smallest, node_index)
       return heapify_down(new_heap2, smallest)

   return heap


def extract_min(heap: MinHeap) -> tuple[MinHeap, Node|Node]:
   if heap.size() == 0:
       print("Heap is empty!")
       return heap, None

   if heap.size() == 1:
       return MinHeap(), heap.get_node(0)

   last_non_leaf = heap.size()//2 -1
   new_heap = heapify_up(heap, last_non_leaf)
   #Smallest node at root of new_heap
   min_node = new_heap.get_node(0)
   #In sorting we swap the root with the last node. Here we simply put the last node at the root position 
   #and forget the removed node.
   last_node = new_heap.get_node(new_heap.size() -1)
   new_heap2 = heap_replace(new_heap, 0, last_node)
   #Shrink the heap 
   new_heap3 = MinHeap(new_heap2.data[:-1]) # Create a new heap without the last element
   return new_heap3, min_node


def count_frequency(s: str)-> dict[str,int]:
    freq = {}
    for c in s:
        if c not in freq.keys():
            freq[c] = 1
        else:
            freq[c] += 1

    return freq


def create_priority_queue(frequency: dict[str, int]) -> MinHeap:
    new_heap = MinHeap()
    for char in frequency.keys():
        new_heap = insert(new_heap, Node(frequency[char], char, None, None))
    return new_heap


def build_tree_from_queue(priority_queue: MinHeap) -> Node:
    """
    root = None
    LOOP until there is one entry left in PQ:
       min1 = extract_min(pq)
       min2 = extract_min(pq)
       new node with min1+min2 frequency and left as min1 and right as min2
       insert new node in the PQ
    """

    new_pq3 = priority_queue
    while(True):
        new_pq, min1_node  = extract_min(new_pq3)
        if new_pq.size() == 0:
           root = min1_node
           return root
        new_pq2, min2_node = extract_min(new_pq)
        new_freq = min1_node.freq + min2_node.freq
        new_char = min1_node.char + min2_node.char
        new_node = Node(new_freq,new_char, min1_node, min2_node)
        new_pq3 = insert(new_pq2, new_node)

def show_tree(root: Node, level: int = 0, label: str = "Root"):
    if root is None:
        return
    print("--" * level + f">[{label}] ({root.char}, {root.freq})")
    show_tree(root.left, level + 1, "L")
    show_tree(root.right, level + 1, "R")


def print_tree(node, indent="", is_left=True):
    if node is None:
        return

    # Print right subtree first (so it appears on top)
    print_tree(node.right, indent + ("│   " if is_left else "    "), False)

    # Print current node
    print(indent + ("└── " if is_left else "┌── ") + f"({node.char}, {node.freq})")

    # Print left subtree
    print_tree(node.left, indent + ("    " if is_left else "│   "), True)



def generate_codes(node: Node | None, prefix="", code: dict | None =None)-> dict:
    if code is None:
        code = {}  
    if node == None:
        return 
    if node.left == None and node.right == None:
        #Leaf node
        code[node.char] = prefix
        #if the tree has only one node, the code for the only char will be an empty prefix rather than having a 0 or 1.
        #Test it by passing a single char string as input to the test.

    if node.left != None:
        generate_codes(node.left, prefix + "0", code)
    if node.right != None:
        generate_codes(node.right, prefix + "1", code)
    return code



def encode(s: str, codes: dict)-> str:
    out_str = ""
    for c in s:
        if c not in codes.keys():
            print(f"Invalid char '{c}' in stream")
            continue
        out_str += codes[c]

    return out_str


def decode(encoded_string: str, root: Node)->str:
    mystr = ""
    save = root
    for v in encoded_string:
        if v == '0':  #Note: Compare with char 0 not integer 0.
            save = save.left
        else:
            save = save.right
        if save.left == None and save.right == None:
            mystr += save.char
            save = root
    return mystr

def huffman_encoding(s:str):
    #Do Not Change this function
    frequency = count_frequency(s)
    pq = create_priority_queue(frequency)
    root = build_tree_from_queue(pq)
    codes = generate_codes(root)
    encoded_string = encode(s, codes)
    decoded_string = decode(encoded_string,root)
    return encoded_string, decoded_string, codes


if __name__ == "__main__":
    """
    arr = [9, 7, 2, 1, 4, 6, 8, 3, 5 ]  
    input=[]
    seed = 'a'
    for i,v in enumerate(arr):
        letter = chr(ord(seed) + i)
        input.append(Node(v,letter,None,None ))
    print(input)

    my_heap = MinHeap(input)
    new_heap, min = extract_min(my_heap)
    print(f"Min freq: {min.freq}")
    #print(f"Heap: {new_heap.data}")

    new_heap, min = extract_min(new_heap)
    print(f"Min freq: {min.freq}")
    #print(f"Heap: {new_heap.data}")

    new_heap, min = extract_min(new_heap)
    print(f"Min freq: {min.freq}")
    #print(f"Heap: {new_heap.data}")
    """
    s  = "BEEP_BOOP_BEER_"
    s = "creative writing is an art that not everyone gets"
    s = "hello"
    freq_dict = count_frequency(s)
    print(freq_dict)
    pq = create_priority_queue(freq_dict)
    print(pq)
    tree = build_tree_from_queue(pq)
    #show_tree(tree)  
    print_tree(tree)
    code = generate_codes(tree, "", None)
    print(code)
    enc_str = encode(s, code)
    print(enc_str)
    dec_str = decode(enc_str, tree)
    print(dec_str)
    enc, dec, codes = huffman_encoding(s)
    print(enc, dec, codes)
