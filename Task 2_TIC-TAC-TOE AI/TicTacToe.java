import java.util.Scanner;

public class TicTacToe {
    private static final char EMPTY = ' ';
    private static final char HUMAN = 'X';
    private static final char AI = 'O';
    private static final char[][] board = {
        {EMPTY, EMPTY, EMPTY},
        {EMPTY, EMPTY, EMPTY},
        {EMPTY, EMPTY, EMPTY}
    };

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        boolean gameOver = false;

        printBoard();
        while (!gameOver) {
            humanMove(scanner);
            if (checkWin(HUMAN)) {
                printBoard();
                System.out.println("You win!");
                gameOver = true;
                break;
            }
            if (checkTie()) {
                printBoard();
                System.out.println("It's a tie!");
                gameOver = true;
                break;
            }

            aiMove();
            if (checkWin(AI)) {
                printBoard();
                System.out.println("AI wins!");
                gameOver = true;
                break;
            }
            if (checkTie()) {
                printBoard();
                System.out.println("It's a tie!");
                gameOver = true;
            }

            printBoard();
        }
        scanner.close();
    }

    private static void printBoard() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                System.out.print(" " + board[i][j] + " ");
                if (j < 2) System.out.print("|");
            }
            System.out.println();
            if (i < 2) System.out.println("---|---|---");
        }
    }

    private static void humanMove(Scanner scanner) {
        int row, col;
        while (true) {
            System.out.println("Enter your move row : ");
            row = scanner.nextInt() - 1;
 System.out.println("Enter your move column: ");
            col = scanner.nextInt() - 1;
            if (row >= 0 && row < 3 && col >= 0 && col < 3 && board[row][col] == EMPTY) {
                board[row][col] = HUMAN;
                break;
            } else {
                System.out.println("This move is not valid.");
            }
        }
    }

    private static void aiMove() {
        int[] bestMove = minimax(board, AI);
        board[bestMove[0]][bestMove[1]] = AI;
    }

    private static int[] minimax(char[][] board, char player) {
        char opponent = (player == AI) ? HUMAN : AI;
        int bestScore = (player == AI) ? Integer.MIN_VALUE : Integer.MAX_VALUE;
        int[] move = {-1, -1};

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == EMPTY) {
                    board[i][j] = player;
                    int score = minimaxScore(board, player);
                    board[i][j] = EMPTY;

                    if (player == AI) {
                        if (score > bestScore) {
                            bestScore = score;
                            move[0] = i;
                            move[1] = j;
                        }
                    } else {
                        if (score < bestScore) {
                            bestScore = score;
                            move[0] = i;
                            move[1] = j;
                        }
                    }
                }
            }
        }
        return move;
    }

    private static int minimaxScore(char[][] board, char player) {
        if (checkWin(AI)) return 10;
        if (checkWin(HUMAN)) return -10;
        if (checkTie()) return 0;

        char opponent = (player == AI) ? HUMAN : AI;
        int bestScore = (player == AI) ? Integer.MIN_VALUE : Integer.MAX_VALUE;

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == EMPTY) {
                    board[i][j] = player;
                    int score = minimaxScore(board, opponent);
                    board[i][j] = EMPTY;

                    if (player == AI) {
                        bestScore = Math.max(score, bestScore);
                    } else {
                        bestScore = Math.min(score, bestScore);
                    }
                }
            }
        }
        return bestScore;
    }

    private static boolean checkWin(char player) {
        for (int i = 0; i < 3; i++) {
            if (board[i][0] == player && board[i][1] == player && board[i][2] == player) return true;
            if (board[0][i] == player && board[1][i] == player && board[2][i] == player) return true;
        }
        if (board[0][0] == player && board[1][1] == player && board[2][2] == player) return true;
        if (board[0][2] == player && board[1][1] == player && board[2][0] == player) return true;
        return false;
    }

    private static boolean checkTie() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == EMPTY) return false;
            }
        }
        return true;
    }
}
