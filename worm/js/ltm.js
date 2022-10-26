//'use strict'
(()=>{
    function setattributes(element, attrs) {
        for (const attr in attrs){
            element.setAttribute(attr, attrs[attr])
        }
    }
    const max_x = 21
    const max_y = 21
    const square_width=10
    const margin=4
    let high_score = 0
    let cur_score = 0

    function drawSquares(ctx) {
        ctx.fillStyle="#00F"
        for (let i=0;i<max_x;i++) {
            for (let j=0;j<max_y;j++){
                ctx.fillStyle="rgba("+i*10+", "+j*10+", 255, 255)"
                let x=margin+(square_width+margin)*i
                let y=margin+(square_width+margin)*j
                
                ctx.fillRect(
                    x,y,
                    square_width,
                    square_width) 
            }

        }
    }

    function drawSquare(ctx, x,y,color) {
        ctx.fillStyle = color
        ctx.fillRect(
            margin+(square_width+margin)*x,
            margin+(square_width+margin)*y,
            square_width,square_width
        )

    }

    function drawPill(ctx,pill) {
        drawSquare(ctx, pill.x, pill.y, "#fff")
    }

    function getRandomPos(){
        return {x: Math.floor(Math.random()*max_x), y:Math.floor(Math.random()*max_y)}

    }

    function drawWorm(ctx, worm){
        const wormColor = "#FF0"
        for (const pos of worm){
            drawSquare(ctx, pos.x, pos.y, wormColor)
        }
    }

    function drawHighScore(ctx){
        const fontsize=16
        const x = (square_width+margin)*max_x
        ctx.fillstyle = "#000000"        
        ctx.fillRect(x+4, 8, 10*fontsize, 3*fontsize) // FIXME: Y yellow?
        ctx.fillStyle = "#0000ff"
        ctx.font = fontsize+"px Courier New"
        ctx.fillText("High Score:"+high_score, x+4,8+fontsize)
        ctx.fillText("Score:"+cur_score, x +4,  2*(8+fontsize))
    }

    
    function updateWorm(worm, cur_dir, hungry){
            const x = worm[0].x+cur_dir.x
            const y = worm[0].y+cur_dir.y
            //check for self collision
            if (worm.length > 1 && worm.some(v=>{                
                return coordsMatch(v, {x:x,y:y})                
            })) {       
                return false
            }
            //check for border collision
            if (x*(x-20) <=0 && y*(y-20) <=0) {
               worm.unshift({x:x,y:y})
            } else {
                return false
            }
            if(hungry) {
                worm.pop()
            } else {
                hungry = true
            }

            return true 
    }

    function coordsMatch(c1, c2) {        
        return (c1.x == c2.x && c1.y == c2.y)
    }

    function startUpdateLoop(ctx) {
        let pill_pos = getRandomPos()
        let worm = [{x:10,y:10}]
        let cur_dir = {x:0, y:0}
        let hungry = true
        let alive = true
        let input = document.addEventListener("keydown", (key)=>{
            console.log(key)
            const updates = {
                "w": {x:0, y:-1},
                "a": {x:-1, y:0},
                "s": {x:0, y:1},
                "d": {x:1, y:0},
            }
            if (key.key in updates) {
                cur_dir = updates[key.key]
            }            
        })

        let heartbeat = window.setInterval(()=>{            
            drawSquares(ctx)

            hungry=!coordsMatch(pill_pos, worm[0])
            if (!hungry) {
                pill_pos = getRandomPos()
            }
            drawPill(ctx, pill_pos)
            
            alive = updateWorm(worm, cur_dir, hungry)
            if (alive){
                cur_score = worm.length
                if (worm.length > high_score){
                    high_score = worm.length
                }
            }
            else{
                worm = [{x:10,y:10}]                
                cur_dir={x:0, y:0}
            }
            drawWorm(ctx, worm)
            drawHighScore(ctx)

        }, 100)
    }

    window.onload = ()=>{
        let mycanvas = document.createElement("canvas")
        setattributes(mycanvas, {
            "width": "500",
            "height": "500",
            "id": "screen"
        })


        document.querySelector("#main").append(mycanvas)
        const ctx = mycanvas.getContext('2d')
        ctx.fillStyle="#000"
        //ctx.clearRect(0,0, mycanvas.width, mycanvas.height)
        ctx.fillRect(0,0,mycanvas.width, mycanvas.height)

        drawSquares(ctx)

        //drawPill(ctx, {x:0, y:0})
        startUpdateLoop(ctx)
    }
})()


