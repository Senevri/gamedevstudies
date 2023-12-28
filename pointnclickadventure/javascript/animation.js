// animation.js
export class Animation {
    constructor(spriteSheet, row, startFrame, endFrame, frameRate = 60) {
        this.spriteSheet = spriteSheet;
        this.row=row
        this.startFrame = startFrame;
        this.endFrame = endFrame;
        this.frameRate = frameRate;
        this.frameDelay = Math.floor(60 / this.frameRate);
        this.framesSinceLastUpdate = 0;
        this.currentFrame = startFrame;
        this.flipX=1
        this.flipY=1
    }
    setFlip(x,y){
        this.flipX = x ? -1 : 1
        this.flipY = y ? -1 : 1
    }

    update() {
        // Increment frame based on frameDelay
        this.framesSinceLastUpdate++;
        if (this.framesSinceLastUpdate >= this.frameDelay) {
            this.currentFrame = (this.currentFrame + 1) % (this.endFrame - this.startFrame + 1);
            this.framesSinceLastUpdate = 0;
        }
    }

    draw(ctx, x, y, extra_scale) {
        ctx.save();
        //Apply flipping transformations
        ctx.scale(this.flipX, this.flipY);
        x = this.flipX * x
        y = this.flipY * y
        if (this.flipX==-1) {
            ctx.translate(x + this.flipX*this.spriteSheet.spriteWidth, 0);

        }
        if (this.flipY ==-1){
            ctx.translate(0, y + this.flipY*this.spriteSheet.spriteHeight);
        }

        this.spriteSheet.drawSprite(ctx, this.currentFrame, this.row, x, y, extra_scale);
        ctx.restore()
    }
}
