document.getElementById('start').addEventListener('click', function() {
    fetch('/game', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            document.getElementById('game_id').value = data.game_id;
            updateBoard(data.board);
        });
});

document.getElementById('end').addEventListener('click', function() {
    const game_id = document.getElementById('game_id').value;
    fetch(`/game/${game_id}/end`, {method: 'POST'})
        .then(() => {
            document.getElementById('board').innerHTML = '';
        });
});

document.getElementById('play').addEventListener('click', function() {
    const game_id = document.getElementById('game_id').value;
    const startPosition = document.getElementById('startPosition').value;
    const endPosition = document.getElementById('endPosition').value;
    fetch(`/game/${game_id}/move`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            start: startPosition,
            end: endPosition,
        }),
    })
    .then(response => response.json())
    .then(data => {
        updateBoard(data.board);
    });
});

function updateBoard(board) {
    const boardDiv = document.getElementById('board');
    boardDiv.innerHTML = '';
    for (let i = 0; i < board.length; i++) {
        for (let j = 0; j < board[i].length; j++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.textContent = board[i][j];
            boardDiv.appendChild(cell);
        }
        boardDiv.appendChild(document.createElement('br'));
    }
}