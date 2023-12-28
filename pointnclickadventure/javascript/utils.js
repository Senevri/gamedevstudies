//utils.js
function downloadJSON(data, filename) {
    const jsonData = JSON.stringify(data, null, 2); // The third parameter adds indentation for better readability
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function loadJSONFromServer() {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const jsonData = JSON.parse(xhr.responseText);
            console.log('Loaded JSON from server:', jsonData);

            // Handle the loaded JSON data as needed
        }
    };
    xhr.open('GET', 'path/to/your/file.json', true);
    xhr.send();
}

// utils.js
export function loadImage(src) {
    return new Promise((resolve, reject) => {
        const image = new Image();
        image.onload = () => resolve(image);
        image.onerror = reject;
        image.src = src;
    });
}
