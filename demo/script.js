class Interval {
    constructor(a, b, color){
        this.a = a;
        this.b = b;
        this.color = color;
    }

    draw(intervalHeight){
        stroke(this.color[0], this.color[1], this.color[2])
        strokeWeight(7)
        line(width/2 + 50, intervalHeight, width/2 + 50 + this.b - this.a, intervalHeight)
    }
}

var intervals = [];
  
let N = 21; // Number of intervals to create
function setup(){
    var cnv = createCanvas(1000, 500);
    cnv.parent('canvas');  

    for(let i = 0; i < N; i++){
        append(intervals, new Interval(50, 100, colors[i]));
    }

}

function draw(){
    clear();

    // Draw nodes of automatic structure
    stroke(1)
    strokeWeight(1)
    let r = 200; // Radius of circle graph sits on
    for(let i = 0; i < N; i++){
        let theta = TWO_PI * i / N;
        let ellipseX = 250 + r * cos(theta);
        let ellipseY = 250 + r * sin(theta);

        fill(255, 255, 255);
        if (pow(mouseX - ellipseX, 2) + pow(mouseY - ellipseY, 2) < 100){
            fill(colors[i][0], colors[i][1], colors[i][2])
        }
        ellipse(ellipseX, ellipseY, 20, 20);
      }

    // Draw intervals
    for(let i = 0; i < N; i++){
        let intervalHeight = 50 + i * (height-100) / (N - 1);
        console.log(i, '*', height - 100, '/', N, '=', intervalHeight)
        stroke(200)
        strokeWeight(1)
        line(width/2 + 50, intervalHeight, width, intervalHeight)
        intervals[i].draw(intervalHeight);
    }
}