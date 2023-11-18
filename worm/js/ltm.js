//'use strict'
(() => {
    function setattributes(element, attrs) {
        for (const attr in attrs) {
            element.setAttribute(attr, attrs[attr])
        }
    }
    const max_x = 21
    const max_y = 21
    const square_width = 16
    const margin = 4

    function drawSquares(ctx) {
        for (let i = 0; i < max_x; i++) {
            for (let j = 0; j < max_y; j++) {
                const color = "rgba(" + i * 10 + ", " + j * 10 + ", 255, 255)"
                drawSquare(ctx, i, j, color)
            }
        }
    }

    function drawSquare(ctx, x, y, color) {
        ctx.fillStyle = color
        ctx.fillRect(
            margin + (square_width + margin) * x,
            margin + (square_width + margin) * y,
            square_width, square_width
        )
    }

    function drawPill(ctx, pill) {
        drawSquare(ctx, pill.x, pill.y, "#fff")
    }

    function getRandomPos() {
        return { x: Math.floor(Math.random() * max_x), y: Math.floor(Math.random() * max_y) }

    }

    function drawWorm(ctx, worm) {
        const wormColor = "#FF0"
        worm.map(pos => drawSquare(ctx, pos.x, pos.y, wormColor))
    }

    function drawScores(ctx, cur_score, high_score) {
        const fontsize = 18
        const x = (square_width + margin) * max_x
        ctx.fillStyle = "#000"
        ctx.fillRect(x + margin, 8, 10 * fontsize, 3 * fontsize)
        ctx.fillStyle = "#0f0"
        ctx.font = "bold " + fontsize + "px Courier New"
        ctx.fillText("High Score:" + high_score, x + 4, 8 + fontsize)
        ctx.fillText("Score:" + cur_score, x + 4, 2 * (8 + fontsize))
    }


    function updateWorm(worm, cur_dir, hungry) {
        const x = worm[0].x + cur_dir.x
        const y = worm[0].y + cur_dir.y

        if (
            worm.length > 1 && worm.some(v => coordsMatch(v, { x: x, y: y })) || //check for self collision
            !(x * (x - 20) <= 0 && y * (y - 20) <= 0) //check for border collision
        ) {
            return false
        }
        worm.unshift({ x: x, y: y })

        if (hungry) {
            worm.pop()
        }
        hungry = true
        return true
    }

    function coordsMatch(c1, c2) {
        return (c1.x == c2.x && c1.y == c2.y)
    }

    function isCompleteReversal(currentDirection, newDirection) {
        return currentDirection.x + newDirection.x === 0 && currentDirection.y + newDirection.y === 0;
    }

    function startUpdateLoop(ctx) {
        const fps = 10
        let pill_pos = getRandomPos()
        let worm = [{ x: 10, y: 10 }]
        let cur_dir = { x: 0, y: 0 }
        let hungry = true
        let alive = true
        let cur_score = 0
        let high_score = 0
        let input = document.addEventListener("keydown", (key) => {
            const updates = {
                "w": { x: 0, y: -1 },
                "a": { x: -1, y: 0 },
                "s": { x: 0, y: 1 },
                "d": { x: 1, y: 0 },
            }
            if (key.key in updates) {
                // prevent self-collision in reverse
                if ((cur_score > 0) && isCompleteReversal(updates[key.key], cur_dir)) {
                    return
                }

                cur_dir = updates[key.key]
            }
        })

        let heartbeat = window.setInterval(() => {
            drawSquares(ctx)

            hungry = !coordsMatch(pill_pos, worm[0])
            if (!hungry) {
                pill_pos = getRandomPos()
            }
            drawPill(ctx, pill_pos)

            alive = updateWorm(worm, cur_dir, hungry)
            if (alive) {
                cur_score = worm.length - 1
                high_score = (cur_score > high_score) ? cur_score : high_score
            }
            else {
                //dead, reset game
                worm = [{ x: 10, y: 10 }]
                cur_dir = { x: 0, y: 0 }
            }
            drawScores(ctx, cur_score, high_score)
            drawWorm(ctx, worm)
        }, 1000 / fps)
    }

    window.onload = () => {
        let mycanvas = document.createElement("canvas")
        setattributes(mycanvas, {
            "width": (square_width + margin) * (max_x + 10),
            "height": (square_width + margin) * (max_x + 1),
            "id": "screen"
        })

        document.querySelector("#main").append(mycanvas)
        const ctx = mycanvas.getContext('2d')
        ctx.fillStyle = "#000"
        ctx.fillRect(0, 0, mycanvas.width, mycanvas.height)
        startUpdateLoop(ctx)
    }
})()
