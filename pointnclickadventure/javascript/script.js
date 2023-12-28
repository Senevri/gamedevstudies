//script.js

import{ updateCanvas, SpriteSheet, drawImage, getTestTileCanvas, drawDebugContent } from './screen.js'
import { loadSpriteSheet } from './upload.js';
import { loadImage } from './utils.js';
import { Animation } from './animation.js';


let spritesheets = []
let animations = []
let resizeTimeout
let testtileimage;
async function initialize() {
    const {context, scale} = updateCanvas();
    window.addEventListener('resize', handleResize);

    // Load sprite sheet
    const spriteSheet = await loadSpriteSheet("./guybrush.png", 32, 48);
    testtileimage = getTestTileCanvas()
    spritesheets.push(spriteSheet)
    animations.push(spriteSheet.createAnimation(0, 0, 5, 8))
    animations.push(spriteSheet.createAnimation(1, 0, 5, 8))

    draw(context, scale)
}


function handleResize() {
    // Clear the existing resize timeout
    clearTimeout(resizeTimeout);

    // Set a new timeout to handle the resize event after a delay
    resizeTimeout = setTimeout(() => {
        const { context, scale } = updateCanvas();
        //draw(context, scale);
    }, 200); // Adjust the delay as needed
}

const maxFps=60
let lastUpdateTimeStamp=0
let adventurer = await loadImage("./adventurer.png")
function draw() {
    const currentTimeStamp = performance.now()
    //Limit maxfps
    if (currentTimeStamp - lastUpdateTimeStamp < 1000/maxFps) {
        lastUpdateTimeStamp = currentTimeStamp
        requestAnimationFrame(() => draw());
        return
    }
    const {context, scale} = updateCanvas(); // Update canvas content
    // Example: Draw sprite at position (50, 50) from the sprite sheet with a scale factor of 2
    //spritesheets[0].drawSpriteFrame(context, 50, 50, 2);
    drawImage(context, scale, testtileimage, 0,0)
    drawImage(context, scale, adventurer, 0,100)

    //drawDebugContent(context, scale)
    //drawImage(context, scale, image, 0, 0)
    animations.forEach((anim)=>anim.update())
    animations[0].setFlip(false, false)
    animations[0].draw(context, 100, 100, 2)
    animations[1].draw(context, 200, 100, 2)
    // //spritesheets[0].drawSprite(context,1, 1, 200,100, scale )
    requestAnimationFrame(() => draw()); // Schedule the next frame // Schedule the next frame
}

initialize().then(
    ()=>{
        console.log(animations, spritesheets)
    }
)
