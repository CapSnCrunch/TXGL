class Interval {
    constructor(type, a, b, color){
        this.a = a;
        this.b = b;
        this.color = color;
    }
}
  
function setup(){
    var cnv = createCanvas(500, 500);
    cnv.parent('canvas');  
}

let N = 38;
let r = 200;
function draw(){
    clear();
    for(let i = 0; i < N; i++){
        let theta = TWO_PI * i / N;
        let ellipseX = 250 + r * cos(theta);
        let ellipseY = 250 + r * sin(theta);

        fill(255, 255, 255);
        if (pow(mouseX - ellipseX, 2) + pow(mouseY - ellipseY, 2) < 100){
            fill(255, 0, 0);
        }
        ellipse(ellipseX, ellipseY, 20, 20);
      }
}