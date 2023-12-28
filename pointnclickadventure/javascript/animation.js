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
    }

    update() {
        // Increment frame based on frameDelay
        this.framesSinceLastUpdate++;
        if (this.framesSinceLastUpdate >= this.frameDelay) {
            this.currentFrame = (this.currentFrame + 1) % (this.endFrame - this.startFrame + 1);
            this.framesSinceLastUpdate = 0;
        }
    }

    draw(context, x, y, extra_scale) {
        this.spriteSheet.drawSprite(context, this.currentFrame, this.row, x, y, extra_scale);
    }
}
