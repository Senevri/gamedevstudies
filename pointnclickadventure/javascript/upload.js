// upload.js
//import { loadImage } from './utils.js';
import { SpriteSheet } from './screen.js';
import { getResource } from './resources.js'

function handleFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
            const jsonData = JSON.parse(event.target.result);
            console.log('Uploaded JSON:', jsonData);

            // Handle the uploaded JSON data as needed
        };
        reader.readAsText(file);
    }
}

async function loadSpriteSheet(img_src, width, height) {
    try {
        const spriteSheetImage = getResource(img_src); // Replace with your sprite sheet path
        return new SpriteSheet(spriteSheetImage, width, height); // Adjust spriteWidth and spriteHeight as needed
    } catch (error) {
        console.error('Error loading sprite sheet:', error);
        throw error;
    }
}

export {loadSpriteSheet, handleFileUpload}
