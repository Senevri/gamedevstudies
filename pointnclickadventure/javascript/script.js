//script.js

import{ updateCanvas, SpriteSheet, drawImage } from './screen.js'
import { loadSpriteSheet } from './upload.js';
import { Animation } from './animation.js';


let spritesheets = []
let animations = []
let resizeTimeout
async function initialize() {
    const {context, scale} = updateCanvas();
    window.addEventListener('resize', handleResize);

    // Load sprite sheet
    const spriteSheet = await loadSpriteSheet("./guybrush.png", 32, 48);
    //const spriteSheet = new SpriteSheet(new Image("./guybrush.png"), 24, 49)
    spritesheets.push(spriteSheet)
    animations.push(spriteSheet.createAnimation(0, 0, 5, 6))
    animations.push(spriteSheet.createAnimation(1, 0, 5, 6))
    // Example: Draw sprite at position (50, 50) from the sprite sheet
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

function draw(context, scale) {
    updateCanvas(); // Update canvas content
    // Example: Draw sprite at position (50, 50) from the sprite sheet with a scale factor of 2
    //spritesheets[0].drawSpriteFrame(context, 50, 50, 2);
    animations.forEach((anim)=>anim.update())
    animations[0].draw(context, 100, 100, scale)
    animations[1].draw(context, 200, 100, scale)
    //spritesheets[0].drawSprite(context,1, 1, 200,100, scale )
    requestAnimationFrame(() => draw(context, scale)); // Schedule the next frame // Schedule the next frame
}

initialize().then(
    ()=>{
        console.log(animations, spritesheets)
    }
)
