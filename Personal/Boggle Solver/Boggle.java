import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.*;

public class Boggle {
    private static Trie dictionary = new Trie();
    private static Piece[][] grid = new Piece[4][4];
    private static ArrayList<String> found = new ArrayList<>();
    private static char[][] board = new char[4][4];

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String input = scan.nextLine();
        int c = 0;
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                board[i][j] = input.charAt(c++);
            }
        }

        convert(board);

        try {
            buildTrie();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        solve();
        int sum = 0;
        Collections.sort(found);
        System.out.println("The following words were found:");
        for (String word : found) {
            int len = word.length();
            if (len <= 4)
                sum++;
            else if (len == 5)
                sum += 2;
            else if (len == 6)
                sum += 3;
            else if (len == 7)
                sum += 5;
            else
                sum += 11;
            System.out.println(word);
        }
        System.out.println("Total: " + sum);

    }

    private static void buildTrie() throws FileNotFoundException {
        Scanner in = new Scanner(new FileReader("dictionary.txt"));
        while (in.hasNext()) {
            String s = in.next();
            dictionary.add(s);
        }
    }

    private static void solve() {
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid.length; j++) {
                Piece[][] gridCopy = copyArray(grid);
                findWords(i, j, gridCopy, "");
            }
        }
    }

    private static void convert(char[][] in) {
        for (int i = 0; i < in.length; i++) {
            for (int j = 0; j < in.length; j++) {
                grid[i][j] = new Piece(in[i][j]);
            }
        }
    }

    private static boolean checkWord(String word) {
        TrieNode search = dictionary.searchNode(word);
        return search != null && search.isWord();
    }

    private static boolean hasPotential(String word) {
        TrieNode search = dictionary.searchNode(word);
        return search != null && !search.children.isEmpty();
    }

    private static void printBoard() {
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                System.out.print(grid[i][j].data + " ");
            }
            System.out.println();
        }
    }

    private static Piece[][] copyArray(Piece[][] a) {
        Piece[][] array = new Piece[4][4];
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                array[i][j] = a[i][j].copy();
            }
        }
        return array;
    }


    private static void findWords(int i, int j, Piece[][] gridCopy, String path) {
        path += gridCopy[i][j].data;
        gridCopy[i][j].setVisited();
        if (path.length() > 2) {
            if (checkWord(path))
                if (!found.contains(path))
                    found.add(path);
        }
        if (hasPotential(path)) {
            if (i > 0 && !gridCopy[i - 1][j].visited)
                findWords(i - 1, j, copyArray(gridCopy), path);
            if (i > 0 && j < 3 && !gridCopy[i - 1][j + 1].visited)
                findWords(i - 1, j + 1, copyArray(gridCopy), path);
            if (j < 3 && !gridCopy[i][j + 1].visited)
                findWords(i, j + 1, copyArray(gridCopy), path);
            if (i < 3 && j < 3 && !gridCopy[i + 1][j + 1].visited)
                findWords(i + 1, j + 1, copyArray(gridCopy), path);
            if (i < 3 && !gridCopy[i + 1][j].visited)
                findWords(i + 1, j, copyArray(gridCopy), path);
            if (j > 0 && i < 3 && !gridCopy[i + 1][j - 1].visited)
                findWords(i + 1, j - 1, copyArray(gridCopy), path);
            if (j > 0 && !gridCopy[i][j - 1].visited)
                findWords(i, j - 1, copyArray(gridCopy), path);
            if (j > 0 && i > 0 && !gridCopy[i - 1][j - 1].visited)
                findWords(i - 1, j - 1, copyArray(gridCopy), path);
        }

    }

    static class Piece {
        char data;
        boolean visited;

        public Piece(char data) {
            this.data = Character.toLowerCase(data);
            visited = false;
        }

        public Piece(char data, boolean visited) {
            this.data = Character.toLowerCase(data);
            this.visited = visited;
        }

        public Piece copy() {
            return new Piece(this.data, this.visited);
        }

        public char getData() {
            return data;
        }

        public void setData(char data) {
            this.data = data;
        }

        public boolean getVisited() {
            return visited;
        }

        public void setVisited() {
            this.visited = true;
        }
    }

    static class TrieNode {
        char c;
        boolean leaf;
        boolean word;
        HashMap<Character, TrieNode> children = new HashMap<>();

        public TrieNode() {
        }

        public TrieNode(char c) {
            this.c = c;
            word = false;
        }

        public boolean isWord() {
            return word;
        }

        public void setWord() {
            word = true;
        }


    }

    static class Trie {
        private TrieNode root;

        public Trie() {
            root = new TrieNode();
        }

        public void add(String word) {
            HashMap<Character, TrieNode> children = root.children;
            int out = 0;
            for (int i = 0; i < word.length(); i++) {
                char c = word.charAt(i);

                TrieNode t;

                if (children.containsKey(c)) {
                    t = children.get(c);
                } else {
                    t = new TrieNode(c);
                    children.put(c, t);
                }

                children = t.children;
                if (i == word.length() - 1) {
                    t.setWord();
                }
            }
        }

        public TrieNode searchNode(String search) {
            Map<Character, TrieNode> children = root.children;
            TrieNode t = null;

            for (int i = 0; i < search.length(); i++) {
                char c = search.charAt(i);
                if (children.containsKey(c)) {
                    t = children.get(c);
                    children = t.children;
                } else {
                    return null;
                }
            }
            return t;
        }
    }
}

