// resources.js

const resources = {};

const baseURL = "./assets/";

const typeHandlers = {
    png: async (fname) => {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => resolve(img);
            img.onerror = () => reject(`Error loading image: ${fname}`);
            img.src = baseURL + fname;
        });
    }
};

const resStrings = [
    "guybrush.png",
    "adventurer.png"
];

async function loadResources() {
    const promises = resStrings.map(async (asset) => {
        const type = asset.substring(asset.length - 3);
        try {
            resources[asset] = await typeHandlers[type](asset);
        } catch (error) {
            console.error(error);
        }
    });

    // Wait for all promises to resolve
    await Promise.all(promises);
}

// Load resources immediately when the module is imported
await loadResources();

console.log(resources)
console.log(resources["guybrush.png"])
console.log("done")

export function getResource(resString) {
    return  resources[resString];
}
