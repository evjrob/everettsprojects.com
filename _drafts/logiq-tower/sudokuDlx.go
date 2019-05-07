package sudokuDlx

import "github.com/evjrob/dlx"

func getRowIndex(cellIndex, puzzleDim int) int {
  return cellIndex / puzzleDim
}

func getColumnIndex(cellIndex, puzzleDim int) int {
  return cellIndex % puzzleDim
}

func getCellIndex(rowIndex, columnIndex, puzzleDim int) int {
  return rowIndex * puzzleDim + columnIndex
}

func getBlockIndex(cellIndex, blockXDim, blockYDim int) int {
  puzzleDim := blockXDim * blockYDim
  rowIndex := getRowIndex(cellIndex, puzzleDim)
  columnIndex := getColumnIndex(cellIndex, puzzleDim)

  return ((rowIndex / blockYDim) * blockYDim) + (columnIndex / blockXDim)
}

// encode takes a sudoku puzzle in 2D slice form with its block dimensions
// and converts it to a dlx matrix
func encode(puzzle [][]int, blockXDim, blockYDim int) dlx.Matrix {
  puzzleDim := blockXDim * blockYDim
  m := dlx.NewMatrix(puzzleDim * puzzleDim * 4)
  for row := 0; row < puzzleDim; row++ {
		for column := 0; column < puzzleDim; column++ {
      cellIndex := getCellIndex(row, column, puzzleDim)
      blockIndex := getBlockIndex(cellIndex, blockXDim, blockYDim)

      // Create a row for the provided value and add it to the matrix
      if puzzle[row][column] > 0 {
        cellValue := puzzle[row][column]
        matrixCellIndex := cellIndex
        matrixRowIndex := (puzzleDim * puzzleDim) + (row * puzzleDim) + (cellValue - 1)
        matrixColumnIndex := 2 * (puzzleDim * puzzleDim) + (column * puzzleDim) + (cellValue - 1)
        matrixBlockIndex := 3 * (puzzleDim * puzzleDim) + (blockIndex * puzzleDim) + (cellValue - 1)
        matrixRow := []int{matrixCellIndex, matrixRowIndex, matrixColumnIndex, matrixBlockIndex}

        m.AddRow(matrixRow)

      // Create a row for every possible value and add them to the matrix
      } else {
        for cellValue := 1; cellValue <= puzzleDim; cellValue++ {
          matrixCellIndex := cellIndex
          matrixRowIndex := (puzzleDim * puzzleDim) + (row * puzzleDim) + (cellValue - 1)
          matrixColumnIndex := 2 * (puzzleDim * puzzleDim) + (column * puzzleDim) + (cellValue - 1)
          matrixBlockIndex := 3 * (puzzleDim * puzzleDim) + (blockIndex * puzzleDim) + (cellValue - 1)
          matrixRow := []int{matrixCellIndex, matrixRowIndex, matrixColumnIndex, matrixBlockIndex}

          m.AddRow(matrixRow)
        }
      }
    }
  }

  return m
}

// decode takes a solution map from a dlx matrix and turns it back into a solved
// 2D int slice
func decode(solutionRows map[int][]int, blockXDim, blockYDim int) [][]int {
  puzzleDim := blockXDim * blockYDim
  solution := make([][]int, puzzleDim)
  for i := 0; i < puzzleDim; i++ {
    solution[i] = make([]int, puzzleDim)
  }

  for _, matrixRow := range solutionRows {
    matrixRowIndex := matrixRow[1]
    matrixColumnIndex := matrixRow[2]
    row := (matrixRowIndex - (puzzleDim * puzzleDim)) / puzzleDim
    column := (matrixColumnIndex - 2 * (puzzleDim * puzzleDim)) / puzzleDim
    value := 1 + matrixRowIndex - (puzzleDim * puzzleDim) - (row * puzzleDim)

    solution[row][column] = value
  }

  return solution
}

// Solve takes a sudoku in the form of an 2D slice ([][]int]) with block dimensions
// and converts it to a dlx exact cover problem to get a solution and then converts
// it back to the [][]int form.
func Solve(puzzle [][]int, blockXDim, blockYDim int) ([][]int , bool) {
  var solution [][]int
  matrix := encode(puzzle, blockXDim, blockYDim)
  matrixSolution, success := matrix.Solve()
  if success {
    solution = decode(matrixSolution, blockXDim, blockYDim)
    return solution, true
  }

  return nil, false
}
