// Tic Tac Toe edited from EECS 16A Lab Touch 2
// Game implemented by Shuming Xu (Fall '21)

// defining the pin mapping
#define Ypos A0
#define Xpos A1
#define Xneg A2
#define Yneg A3

// global variables
uint32_t x_raw, y_raw;
uint8_t coordinates[] = {0, 0};

// tic tac toe
boolean player_x = true;
String board[3][3] = {
  {" ", " ", " "},
  {" ", " ", " "},
  {" ", " ", " "}  
};

/*  ToDo: Finish this function
    getLoc returns integer value coordinates of
    where a touch was detected
*/
void getLoc(uint32_t x_raw, uint32_t y_raw) {
  float raw_range = 4096.0;
  int width  = 3;
  int height = 3;

  // BEGIN {{
  int x_coordinate = // YOUR CODE HERE
  int y_coordinate = // YOUR CODE HERE
  // }} END

  coordinates[0] = (uint8_t) x_coordinate;
  coordinates[1] = (uint8_t) y_coordinate;
}

String getPlayer() {
  return player_x ? "X" : "O";
}


boolean hasEnded() {
  // test rows
  for (int i = 0; i < 3; i++) {
    if (board[i][0] != " " && board[i][0] == board[i][1] && board[i][1] == board[i][2]) {
      return true;
    }
  }

  // test columns
  for (int i = 0; i < 3; i++) {
    if (board[0][i] != " " && board[0][i] == board[1][i] && board[1][i] == board[2][i]) {
      return true;
    }
  }

  // test verticals
  if (board[0][0] != " " && board[0][0] == board[1][1] && board[1][1] == board[2][2]) {
    return true;
  }
  if (board[0][2] != " " && board[0][2] == board[1][1] && board[1][1] == board[2][0]) {
    return true;
  }
  return false;
}

void resetGame() {
  // clear board
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      board[i][j] = " ";
    }
  }
  // always start on player X
  player_x = true;
}

boolean allFilled() {
  // used for checking if there is a tie
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      if (board[i][j] == " ") {
        return false;
      }
    }
  }
  return true;
}

void makeMove() {
  int col = coordinates[0];
  int row = 2 - coordinates[1];

  // can't fill in the same slot
  if (board[row][col] != " ") {
    Serial.println("Oops! That is already filled.");
    return;
  }

  // set state
  board[row][col] = getPlayer();

  // check if player wins
  if (hasEnded()) {
    // has ended, reset board
    printBoard();
    Serial.println("Player " + getPlayer() + " wins!");
    Serial.println("*****************************");
    Serial.println("New Game:");
    resetGame();
  } else if (allFilled()) {
    // tie!
    printBoard();
    Serial.println("There is a a tie!");
    Serial.println("*****************************");
    Serial.println("New Game:");
    resetGame();
  } else {
    // game continues
    player_x = !player_x;
  }

}

void printBoard() {
  Serial.println(board[0][0] + "|" + board[0][1] + "|" + board[0][2]);
  Serial.println("-+-+-");
  Serial.println(board[1][0] + "|" + board[1][1] + "|" + board[1][2]);
  Serial.println("-+-+-");
  Serial.println(board[2][0] + "|" + board[2][1] + "|" + board[2][2]);
}

void setup()
{
  // start serial port at 115200 bps:
  Serial.begin(115200);
  Serial.println("+-----------------------+");
  while (!Serial);
  Serial.println("+-----------------------+");
  Serial.println("| Resistive Touchscreen |");
  Serial.println("|   with Tic Tac Toe!   |");
  Serial.println("| Start Pressing Points |"); 
  Serial.println("+-----------------------+");
  printBoard();
  Serial.println("It is now player " + getPlayer() + "'s turn.");
}

void loop() {
  if (touch()) {
    Serial.println("==========");
    x_raw = meas(Xneg, Xpos, Yneg, Ypos);
    y_raw = meas(Yneg, Ypos, Xneg, Xpos);
    getLoc(x_raw, y_raw);
    Serial.print("X = ");
    Serial.print(coordinates[0]);
    Serial.print(" Y = ");
    Serial.println(coordinates[1]);
    makeMove();
    printBoard();
    Serial.println("It is now player " + getPlayer() + "'s turn.");
    delay(1000);
  }
}

/* touch returns true if a touch has been detected;
  returns false otherwise.  */
boolean touch()
{
  pinMode(Ypos, INPUT_PULLUP);
  pinMode(Yneg, INPUT);
  pinMode(Xneg, OUTPUT);
  pinMode(Xpos, INPUT);
  digitalWrite(Xneg, LOW);
  boolean touch = false;
  if (!digitalRead(Ypos)) {
    touch = true;
  }
  //Serial.println(touch);
  return touch;
}

uint32_t meas(int pwr_neg, int pwr_pos, int sense_neg, int sense_pos) {
  pinMode(sense_neg, INPUT); // sets sense_neg to be an input pin
  pinMode(sense_pos, INPUT); // sets sense_pos to be an input pin
  digitalWrite(sense_neg, LOW); // outputs GND to sense_neg to protect from floating voltages
  pinMode(pwr_neg, OUTPUT); // sets pwr_neg to output
  digitalWrite(pwr_neg, LOW); // outputs GND to pwr_neg
  pinMode(pwr_pos, OUTPUT); // sets pwr_pos to output
  digitalWrite(pwr_pos, HIGH); // outputs +3V to pwr_pos
  return analogRead(sense_pos);
}
