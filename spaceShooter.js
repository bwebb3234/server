const canvas = document.getElementById("spaceShooter");
const ctx = canvas.getContext("2d");

// Player settings
const player = { x: 50, y: canvas.height / 2 - 20, width: 40, height: 40, speed: 5 };

// Controls
const keys = { ArrowUp: false, ArrowDown: false, ArrowLeft: false, ArrowRight: false, Space: false };

// Bullets
const bullets = [];

// Enemies
const enemies = [];
const enemySpeed = 2;
let enemyTimer = 0;

// Score
let score = 0;
let gameOver = false;

// Handle keydown - includes restart on Enter
window.addEventListener("keydown", e => {
  if (e.code === "Enter" && gameOver) {
    resetGame();
  }
  if (keys.hasOwnProperty(e.code)) keys[e.code] = true;
});

// Handle keyup
window.addEventListener("keyup", e => {
  if (keys.hasOwnProperty(e.code)) keys[e.code] = false;
});

function createEnemy() {
  const size = 30 + Math.random() * 20;
  const y = Math.random() * (canvas.height - size);
  enemies.push({ x: canvas.width, y, width: size, height: size });
}

function update() {
  if (gameOver) return;

  // Move player
  if (keys.ArrowUp && player.y > 0) player.y -= player.speed;
  if (keys.ArrowDown && player.y + player.height < canvas.height) player.y += player.speed;
  if (keys.ArrowLeft && player.x > 0) player.x -= player.speed;
  if (keys.ArrowRight && player.x + player.width < canvas.width) player.x += player.speed;

  // Shoot bullet
  if (keys.Space && (!bullets.length || bullets[bullets.length - 1].x > player.x + 100)) {
    bullets.push({ x: player.x + player.width, y: player.y + player.height / 2 - 2, width: 10, height: 4, speed: 7 });
  }

  // Move bullets
  for (let i = bullets.length - 1; i >= 0; i--) {
    bullets[i].x += bullets[i].speed;
    if (bullets[i].x > canvas.width) bullets.splice(i, 1);
  }

  // Create enemies periodically
  enemyTimer++;
  if (enemyTimer > 90) {
    createEnemy();
    enemyTimer = 0;
  }

  // Move enemies and check collisions
  for (let i = enemies.length - 1; i >= 0; i--) {
    enemies[i].x -= enemySpeed;

    // Check collision with player
    if (
      player.x < enemies[i].x + enemies[i].width &&
      player.x + player.width > enemies[i].x &&
      player.y < enemies[i].y + enemies[i].height &&
      player.y + player.height > enemies[i].y
    ) {
      gameOver = true;
    }

    // Check collision with bullets
    for (let j = bullets.length - 1; j >= 0; j--) {
      if (
        bullets[j].x < enemies[i].x + enemies[i].width &&
        bullets[j].x + bullets[j].width > enemies[i].x &&
        bullets[j].y < enemies[i].y + enemies[i].height &&
        bullets[j].y + bullets[j].height > enemies[i].y
      ) {
        enemies.splice(i, 1);
        bullets.splice(j, 1);
        score += 1;
        break;
      }
    }

    // Remove enemies that have passed the left edge
    if (enemies[i] && enemies[i].x + enemies[i].width < 0) enemies.splice(i, 1);
  }
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw player (white triangle)
  ctx.fillStyle = "white";
  ctx.beginPath();
  ctx.moveTo(player.x, player.y + player.height / 2);
  ctx.lineTo(player.x + player.width, player.y);
  ctx.lineTo(player.x + player.width, player.y + player.height);
  ctx.closePath();
  ctx.fill();

  // Draw bullets
  ctx.fillStyle = "yellow";
  bullets.forEach(b => ctx.fillRect(b.x, b.y, b.width, b.height));

  // Draw enemies (red squares)
  ctx.fillStyle = "red";
  enemies.forEach(e => ctx.fillRect(e.x, e.y, e.width, e.height));

  // Draw score
  ctx.fillStyle = "white";
  ctx.font = "20px sans-serif";
  ctx.fillText("Score: " + score, 10, 30);

  if (gameOver) {
    ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
    ctx.fillRect(0, canvas.height / 2 - 40, canvas.width, 80);
    ctx.fillStyle = "red";
    ctx.font = "40px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 + 10);
    ctx.font = "20px sans-serif";
    ctx.fillText("Press Enter to Restart", canvas.width / 2, canvas.height / 2 + 40);
    ctx.textAlign = "start";
  }
}

function gameLoop() {
  update();
  draw();
  if (!gameOver) {
    requestAnimationFrame(gameLoop);
  }
}

function resetGame() {
  // Reset player position
  player.x = 50;
  player.y = canvas.height / 2 - 20;

  // Clear bullets and enemies
  bullets.length = 0;
  enemies.length = 0;

  // Reset score and timer
  score = 0;
  enemyTimer = 0;

  // Reset game over flag
  gameOver = false;

  // Restart game loop
  gameLoop();
}

// Start the game loop
gameLoop();