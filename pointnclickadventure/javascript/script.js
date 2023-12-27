const canvas = document.getElementById('myCanvas');
const context = canvas.getContext('2d');

// Set the fixed canvas size
const fixedWidth = 320; // Set your desired fixed width
const fixedHeight = 240; // Set your desired fixed height
canvas.width = fixedWidth;
canvas.height = fixedHeight;

// Function to update the canvas size and draw on the canvas
function updateCanvas() {
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;

    // Calculate the scaling factors
    const scaleWidth = windowWidth / fixedWidth;
    const scaleHeight = windowHeight / fixedHeight;

    // Use the minimum scaling factor to maintain the aspect ratio
    const scale = Math.min(scaleWidth, scaleHeight);

    // Update the canvas size based on the scaling factor
    canvas.width = fixedWidth * scale;
    canvas.height = fixedHeight * scale;

    // Clear the canvas
    context.clearRect(0, 0, canvas.width, canvas.height);
    drawDebugContent(context, scale)
    drawImage(context, scale)

}

function drawDebugContent(context, scale) {
    // Draw a box with corner markers
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = 'rgba(255, 0, 0, 0.3)';
    context.fillRect(50, 50, canvas.width - 100, canvas.height - 100);
    // Draw corner markers
    context.fillStyle = '#000';
    context.fillRect(50 - 5, 50 - 5, 10, 10);
    context.fillRect(canvas.width - 50 - 5, 50 - 5, 10, 10);
    context.fillRect(canvas.width - 50 - 5, canvas.height - 50 - 5, 10, 10);
    context.fillRect(50 - 5, canvas.height - 50 - 5, 10, 10);


    // Draw a single pixel at the center
    const centerX = Math.floor(canvas.width / 2);
    const centerY = Math.floor(canvas.height / 2);
    const pixelSize = 4*scale;

    context.fillStyle = '#000'; // Set color to black
    context.fillRect(centerX, centerY, pixelSize, pixelSize);
    context.font = "16px Cascadia Code"
    context.fillText(scale, 100,100)
}

// Function to load and draw an image
function drawImage(context) {
    const image = new Image();
    image.src = './adventurer.png'; // Replace with the path to your image
    image.onload = function () {
        const scale = canvas.width / fixedWidth;
        const imageWidth = image.width * scale;
        const imageHeight = image.height * scale;
        const imageX = Math.floor(canvas.width / 2 - imageWidth / 2);
        const imageY = Math.floor(canvas.height / 2 - imageHeight / 2);
        context.imageSmoothingEnabled=false
        context.drawImage(image, imageX, imageY, imageWidth, imageHeight);
    };
}

// Call the function initially and whenever the window is resized
updateCanvas();
window.addEventListener('resize', updateCanvas);
