class AVLTreeNode:
    def __init__(self, key, translation, explanation_haw, explanation_eng):
        self.key = key  # Hawaiian saying
        self.translation = translation  # English translation
        self.explanation_haw = explanation_haw  # Explanation in Hawaiian
        self.explanation_eng = explanation_eng  # Explanation in English
        self.height = 1  # Height for balancing
        self.left = None  # Left child
        self.right = None  # Right child


class AVLTree:
    def __init__(self):
        self.root = None

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = max(self._get_height(y.left), self._get_height(y.right)) + 1
        x.height = max(self._get_height(x.left), self._get_height(x.right)) + 1
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = max(self._get_height(x.left), self._get_height(x.right)) + 1
        y.height = max(self._get_height(y.left), self._get_height(y.right)) + 1
        return y

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def insert(self, root, key, translation, explanation_haw, explanation_eng):
        if not root:
            return AVLTreeNode(key, translation, explanation_haw, explanation_eng)
        
        if key < root.key:
            root.left = self.insert(root.left, key, translation, explanation_haw, explanation_eng)
        elif key > root.key:
            root.right = self.insert(root.right, key, translation, explanation_haw, explanation_eng)
        else:
            return root  

        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        balance = self._get_balance(root)

        # Left Left Case
        if balance > 1 and key < root.left.key:
            return self._rotate_right(root)

        # Right Right Case
        if balance < -1 and key > root.right.key:
            return self._rotate_left(root)

        # Left Right Case
        if balance > 1 and key > root.left.key:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)

        # Right Left Case
        if balance < -1 and key < root.right.key:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)

        return root

    def search(self, root, key):
        if not root or root.key == key:
            return root
        if key < root.key:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def first(self, root):
        if not root:
            return None
        while root.left:
            root = root.left
        return root

    def last(self, root):
        if not root:
            return None
        while root.right:
            root = root.right
        return root

    def predecessor(self, root, key):
        node = self.search(root, key)
        if not node:
            return None
        
        if node.left:
            return self.last(node.left)
        
        predecessor = None
        while root:
            if key > root.key:
                predecessor = root
                root = root.right
            elif key < root.key:
                root = root.left
            else:
                break
        return predecessor

    def successor(self, root, key):
        node = self.search(root, key)
        if not node:
            return None
        
        if node.right:
            return self.first(node.right)
        
        successor = None
        while root:
            if key < root.key:
                successor = root
                root = root.left
            elif key > root.key:
                root = root.right
            else:
                break
        return successor


class ProverbsDatabase:
    def __init__(self):
        self.tree = AVLTree()
        self.hawaiian_words = {}  
        self.english_words = {}  

    def insert(self, key, translation, explanation_haw, explanation_eng):
        
        self.tree.root = self.tree.insert(self.tree.root, key, translation, explanation_haw, explanation_eng)
        
        
        for word in key.split():
            if word not in self.hawaiian_words:
                self.hawaiian_words[word] = []
            self.hawaiian_words[word].append(key)

       
        for word in translation.split():
            if word not in self.english_words:
                self.english_words[word] = []
            self.english_words[word].append(key)

    def member(self, key):
        return self.tree.search(self.tree.root, key) is not None

    def first(self):
        return self.tree.first(self.tree.root)

    def last(self):
        return self.tree.last(self.tree.root)

    def predecessor(self, key):
        return self.tree.predecessor(self.tree.root, key)

    def successor(self, key):
        return self.tree.successor(self.tree.root, key)

    def mehua(self, word):
        return self.hawaiian_words.get(word, [])

    def withword(self, word):
        return self.english_words.get(word, [])



db = ProverbsDatabase()
db.insert("ʻAʻa i ka hula", "Dare to dance", "E ʻōlelo ana i ka wiwo ʻole i ka hula ʻana", "Encouraging one to be fearless in dancing.")
db.insert("Huli ka lima i lalo", "Turn the hands down", "Ke kāhea i ka hana ʻana", "A call to action.")
db.insert("I ka wā ma mua, ka wā ma hope", "The future is in the past", "E kuhikuhi i ka hoʻokele ʻana mai ka wā ma mua", "The past informs the future.")
db.insert("Piliʻuhane", "Spirit bond", "Ka pili o nā ʻuhane i loko o ke ʻano kūpilikiʻi", "A close, spiritual bond during difficult times.")
db.insert("Kūlia i ka nuʻu", "Strive for the summit", "E hoʻoikaika e kū i ka nuʻu", "Encouraging someone to always strive for their best.")
db.insert("He aliʻi ka ʻāina, he kauwā ke kanaka", "The land is chief, man is its servant", "ʻO ke kanaka ke kauā o ka ʻāina", "Reminds people of the importance of respecting the land.")
db.insert("Ua mau ke ea o ka ʻāina i ka pono", "The life of the land is perpetuated in righteousness", "Ua mau ke ea o ka ʻāina i ke koʻikoʻi o ka pono", "This phrase serves as a reminder of the importance of righteousness.")


print(db.mehua("hula"))  
print(db.withword("dance")) 
print(db.member("ʻAʻa i ka hula"))  
print(db.first().key) 
print(db.last().key) 

predecessor_node = db.predecessor("Huli ka lima i lalo")
if predecessor_node:
    print(f"Predecessor of 'Huli ka lima i lalo': {predecessor_node.key}")
else:
    print("No predecessor found for 'Huli ka lima i lalo'")

successor_node = db.successor("ʻAʻa i ka hula")
if successor_node:
    print(f"Successor of 'ʻAʻa i ka hula': {successor_node.key}")
else:
    print("No successor found for 'ʻAʻa i ka hula'")

predecessor_node = db.predecessor("Piliʻuhane")
if predecessor_node:
    print(f"Predecessor of 'Piliʻuhane': {predecessor_node.key}")
else:
    print("No predecessor found for 'Piliʻuhane'")

successor_node = db.successor("Piliʻuhane")
if successor_node:
    print(f"Successor of 'Piliʻuhane': {successor_node.key}")
else:
    print("No successor found for 'Piliʻuhane'")

