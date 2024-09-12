const cells = document.querySelectorAll('.cell');
const restartBtn = document.getElementById('restart');
const undoBtn = document.getElementById('undo');
const humanScoreElement = document.getElementById('human-score');
const aiScoreElement = document.getElementById('ai-score');
const tieScoreElement = document.getElementById('tie-score');

let board = Array(9).fill('');
const humanPlayer = 'X';
const aiPlayer = 'O';
let humanScore = 0;
let aiScore = 0;
let tieScore = 0;
let moveHistory = [];

// Winning combinations
const winCombos = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
  [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
  [0, 4, 8], [2, 4, 6]             // Diagonals
];

// Start the game
startGame();

function startGame() {
  board.fill('');
  moveHistory = [];
  cells.forEach(cell => {
    cell.innerText = '';
    cell.classList.remove('x', 'o');
    cell.addEventListener('click', handleTurnClick, { once: true });
  });
}

function handleTurnClick(e) {
  const index = e.target.getAttribute('data-index');
  if (!board[index]) {
    playTurn(index, humanPlayer);
    moveHistory.push(index);
    if (!checkWin(board, humanPlayer) && !checkTie()) {
      setTimeout(() => {
        const aiIndex = bestMove();
        playTurn(aiIndex, aiPlayer);
        moveHistory.push(aiIndex);
        checkTie(); // Check for tie after AI's move
      }, 500);
    }
  }
}

function playTurn(index, player) {
  board[index] = player;
  const cell = document.querySelector(`.cell[data-index='${index}']`);
  cell.innerText = player;
  cell.classList.add(player === humanPlayer ? 'x' : 'o');
  if (checkWin(board, player)) {
    gameOver(player);
  }
}

function checkWin(board, player) {
  return winCombos.some(combo => combo.every(i => board[i] === player));
}

function checkTie() {
  if (board.every(cell => cell)) {
    tieScore++;
    alert('It\'s a tie!');
    updateScores();
    return true;
  }
  return false;
}

function gameOver(winner) {
  cells.forEach(cell => cell.removeEventListener('click', handleTurnClick));
  if (winner === humanPlayer) {
    humanScore++;
    alert("You win!");
  } else {
    aiScore++;
    alert("AI wins!");
  }
  updateScores();
}

function updateScores() {
  humanScoreElement.textContent = humanScore;
  aiScoreElement.textContent = aiScore;
  tieScoreElement.textContent = tieScore;
}

// Undo the last move
function undoLastMove() {
  if (moveHistory.length > 0) {
    const lastMove = moveHistory.pop();
    board[lastMove] = '';
    const cell = document.querySelector(`.cell[data-index='${lastMove}']`);
    cell.innerText = '';
    cell.classList.remove('x', 'o');
    cell.addEventListener('click', handleTurnClick, { once: true });
  }
}

undoBtn.addEventListener('click', undoLastMove);

// Minimax algorithm for AI
function bestMove() {
  let bestScore = -Infinity;
  let move;
  for (let i = 0; i < board.length; i++) {
    if (!board[i]) {
      board[i] = aiPlayer;
      const score = minimax(board, 0, false);
      board[i] = '';
      if (score > bestScore) {
        bestScore = score;
        move = i;
      }
    }
  }
  return move;
}

function minimax(board, depth, isMaximizing) {
  if (checkWin(board, aiPlayer)) return 10 - depth;
  if (checkWin(board, humanPlayer)) return depth - 10;
  if (board.every(cell => cell)) return 0;

  if (isMaximizing) {
    let bestScore = -Infinity;
    for (let i = 0; i < board.length; i++) {
      if (!board[i]) {
        board[i] = aiPlayer;
        const score = minimax(board, depth + 1, false);
        board[i] = '';
        bestScore = Math.max(score, bestScore);
      }
    }
    return bestScore;
  } else {
    let bestScore = Infinity;
    for (let i = 0; i < board.length; i++) {
      if (!board[i]) {
        board[i] = humanPlayer;
        const score = minimax(board, depth + 1, true);
        board[i] = '';
        bestScore = Math.min(score, bestScore);
      }
    }
    return bestScore;
  }
}

restartBtn.addEventListener('click', startGame);
