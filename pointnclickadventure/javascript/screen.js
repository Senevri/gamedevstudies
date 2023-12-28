//screen.js
import { Animation } from "./animation.js";
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
    //drawDebugContent(context, scale)
    //drawTestTiles(context, scale)
    // const x=100
    // const y=100
    // drawImage(context, scale, './adventurer.png', x, y)
    // drawImage(context, scale, './guybrush.png', x, y)
    context.current_scale=scale
    return {context, scale}
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
    const pixelSize = 1*scale;

    context.fillStyle = 'cyan'; // Set color to black
    context.fillRect(centerX, centerY, pixelSize, pixelSize);
    context.font = "16px Cascadia Code"
    context.fillStyle = 'black'; // Set color to black
    context.fillText(scale, 20,20)
 //   drawImage(context, scale, "./adventurer.png", 0, 0)
}

function getTestTileCanvas(){
    let tmp_canvas = document.createElement('canvas')
    tmp_canvas.width = fixedWidth; tmp_canvas.height = fixedHeight
    const ctx = tmp_canvas.getContext('2d')
    const tile_img = new Image()
    tile_img.src= "./test_tile.png"
    tile_img.imageSmoothingEnabled=false
    tile_img.onload = ()=> {
        for (let i=0;i<20;i++) {
            let x = i*16
            for (let j=0;j<15;j++) {
                ctx.drawImage(tile_img, x, j*16)
            }
        }
    }
    return tmp_canvas
}
function drawScaledImage(context, image, x, y, scale) {
    const imageWidth = image.width * scale;
    const imageHeight = image.height * scale;
    const imageX = x*scale
    const imageY = y*scale
    context.imageSmoothingEnabled=false
    context.drawImage(image, imageX, imageY, imageWidth, imageHeight);
}

// Function to load and draw an image
function drawImage(context, scale, src, x, y) {
    let image = new Image()
    if (src instanceof Element) {
        image = src
        drawScaledImage(context, image, x, y, scale)
    } else {
        image.src = src
        image.onload = function () {
            drawScaledImage(context, image, x, y, scale)
        };
    }
}

export class SpriteSheet {
    constructor(image, spriteWidth, spriteHeight) {
        this.image = image;
        this.spriteWidth = spriteWidth;
        this.spriteHeight = spriteHeight;
        this.currentFrame=0
        this.currentRow=0
        this.columns = Math.floor(image.width/spriteWidth)
        this.rows = Math.floor(image.height/spriteHeight)
    }

    drawSpriteFrame(context, x, y, extra_scale) {
        this.drawSprite(context, this.currentFrame, this.currentRow, x,y, extra_scale)
        this.currentFrame = (this.currentFrame + 1) % this.columns
    }

    createAnimation(row, startFrame, endFrame, frameRate) {
        return new Animation(this, row, startFrame, endFrame, frameRate);
    }

    drawSprite(context, spriteX, spriteY, x, y, extra_scale) {
        context.imageSmoothingEnabled=false
        context.drawImage(
            this.image,
            spriteX * this.spriteWidth,
            spriteY * this.spriteHeight,
            this.spriteWidth,
            this.spriteHeight,
            x*context.current_scale,
            y*context.current_scale,
            this.spriteWidth*context.current_scale*extra_scale,
            this.spriteHeight*context.current_scale*extra_scale
        );
    }
}

// Call the function initially and whenever the window is resized
export {updateCanvas, drawImage, drawDebugContent, getTestTileCanvas}
