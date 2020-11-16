import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function Square(props) {
  return (
    <button
      className="square"
      onClick={props.onClick}
    >
      {props.value}
    </button>
  );
}

class Board extends React.Component {
  renderSquare(i) {
    return (
      <Square
        value={this.props.squares[i]}
        onClick={() => this.props.onClick(i)}
      />
    );
  }

  render() {
    return (
      <div>
        <div className="board-row">
          {this.renderSquare(0)}
          {this.renderSquare(1)}
          {this.renderSquare(2)}
        </div>
        <div className="board-row">
          {this.renderSquare(3)}
          {this.renderSquare(4)}
          {this.renderSquare(5)}
        </div>
        <div className="board-row">
          {this.renderSquare(6)}
          {this.renderSquare(7)}
          {this.renderSquare(8)}
        </div>
      </div>
    );
  }
}

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      history: [{
        squares: Array(9).fill(null),
      }],
      stepNumber: 0,
      xIsNext: true,
      symbolCountX: 0,
      symbolCount0: 0,
      currentSymbol: 'X',
      secondStep: false,
      moveThisSquare: 0,
    };
  }

  handleClick(i) {
    const history = this.state.history.slice(0, this.state.stepNumber + 1);
    const current = history[history.length - 1];
    const squares = current.squares.slice();
    const checkPossibleWin = current.squares.slice();
    let currentSymbol = this.state.currentSymbol;
    let xIsNext = this.state.xIsNext;
    let oppSymbol = !xIsNext ? 'X' : '0';
    let moveThisSquare = this.state.moveThisSquare;
    let secondStep = this.state.secondStep;
    let vacateCenter = false;

    // Count symbols within the current board (unchanged)
    let symbolCountX = countSymbol(squares, 'X');
    let symbolCount0 = countSymbol(squares, '0');
    let currentSymbolCount = this.state.xIsNext ? symbolCountX : symbolCount0;

    // Check for Winner
    if (calculateWinner(squares)) {
      return;
    }

    // Check if center square is filled by current symbol
    if (squares[4] == currentSymbol)
      vacateCenter = true;

    // Center square must either vacate or win, so check for winner
    if (vacateCenter && currentSymbolCount >= 3) {
      if (secondStep && squares[i] == null) {
        checkPossibleWin[i] = xIsNext ? 'X' : '0';
        checkPossibleWin[moveThisSquare] = null;
        if (!calculateWinner(checkPossibleWin) && moveThisSquare!=4) {
          this.setState({ secondStep: false });
          return;
        }
      } else {
        if (squares[i] == null) {
          checkPossibleWin[i] = xIsNext ? 'X' : '0';
          if (!calculateWinner(checkPossibleWin))
            return;
        }
      }
    }

    if (squares[i] == oppSymbol) {
      return;
    // Current square is empty
    } else if (squares[i] == null) {
      // Do nothing if a piece isn't being moved and symbol count > 3, or if new square is not adjacent to the old square
      if ((!secondStep && currentSymbolCount >= 3) || (secondStep && !isAdjacent(i, moveThisSquare)))
        return;

      // Piece is being moved
      if (secondStep) {
        // Update status of current square and change current symbol
        squares[i] = xIsNext ? 'X' : '0';
        currentSymbol = !xIsNext ? 'X' : '0';
        xIsNext = !xIsNext;

        // Set the previous square to null and secondStep to false once done
        squares[moveThisSquare] = null;
        secondStep = false;
      
      // Adding a new piece to the board
      } else if (currentSymbolCount < 3) {
        // Update status of current square and change current symbol
        squares[i] = xIsNext ? 'X' : '0';
        currentSymbol = !xIsNext ? 'X' : '0';
        xIsNext = !xIsNext;

        // Increment the counters
        symbolCountX += xIsNext;
        symbolCount0 += !xIsNext;
      }

    // Must keep introducing new pieces if max 3 isn't filled
    } else if (currentSymbolCount < 3) {
      return;
    // If clicked square is the same symbol as current (moving a piece)
    } else if (squares[i] == currentSymbol) {
      moveThisSquare = i;
      secondStep = true;
      
      // Update Game's state
      this.setState({
        secondStep: secondStep,
        moveThisSquare: moveThisSquare,
      });

      return;
    }

    // Update Game's state
    this.setState({
      history: history.concat([{
        squares: squares
      }]),
      stepNumber: history.length,
      xIsNext: xIsNext,
      symbolCountX: symbolCountX,
      symbolCount0: symbolCount0,
      currentSymbol: currentSymbol,
      secondStep: secondStep,
      moveThisSquare: moveThisSquare,
    });
  }

  jumpTo(step) {
    const history = this.state.history.slice(0, step + 1);
    const current = history[history.length - 1];
    const squares = current.squares.slice();

    // Count symbols within the new "step"
    let symbolCountX = countSymbol(squares, 'X');
    let symbolCount0 = countSymbol(squares, '0');

    this.setState({
      stepNumber: step,
      xIsNext: (step % 2) === 0,
      currentSymbol: !(step%2) ? 'X' : '0',
      symbolCountX: symbolCountX,
      symbolCount0: symbolCount0,
    });
  }

  render() {
    const history = this.state.history;
    const current = history[this.state.stepNumber]
    const winner = calculateWinner(current.squares);

    const moves = history.map((step, move) => {
      const desc = move ? 'Go to move #' + move :
                   'Go to game start';
      return (
        <li key={move}>
          <button onClick={() => this.jumpTo(move)}>{desc}</button>
        </li>
      );
    });
    
    let status;
    if (winner) {
      status = 'Winner: ' + winner;
    } else {
      status = 'Next player: ' + this.state.currentSymbol;
    }

    return (
      <div className="game">
        <div className="game-board">
          <Board
            squares={current.squares}
            onClick={(i) => this.handleClick(i)}
          />
        </div>
        <div className="game-info">
          <div>{status}</div>
          <ol>{moves}</ol>
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <Game />,
  document.getElementById('root')
);

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

function countSymbol(squares, symbol) { 
  let count = 0;
  let i = 0;

  for (i = 0; i < 9; i++) {
    if (squares[i] == symbol)
      count++;
  }

  return count;
}

function isAdjacent(a, b) {
  if (a == 4 || b == 4)
    return true;

  const validMoves = [
    [1, 3, 4], 
    [0, 2, 3, 4, 5],
    [1, 4, 5],
    [0, 1, 4, 6, 7],
    [],
    [1, 2, 4, 7, 8],
    [3, 4, 7],
    [3, 4, 5, 6, 8],
    [4, 5, 7],
  ]

  if (validMoves[a].includes(b))
    return true;

  return false;
}
