var intervals = [];
  
let N = Object.keys(triangleGraph).length; // Number of intervals to create
function setup(){
    var cnv = createCanvas(1000, 500);
    cnv.parent('canvas');  

    for(let i = 0; i < N; i++){
        append(intervals, new Interval(50, 100, colors[i]));
    }
}

let pressing = false
let selected = -1
let radius = 200; // Radius of circle graph sits on

function draw(){
    clear();

    // Draw edges of graph as arcs between nodes
    for(let i = 0; i < Object.keys(triangleGraph).length; i++){
        for(let j = 0; j < Object.keys(triangleGraph[i]).length; j++){
            let theta1 = TWO_PI * i / N;
            let ellipse1X = 250 + radius * cos(theta1);
            let ellipse1Y = 250 + radius * sin(theta1);

            let theta2 = TWO_PI * Object.keys(triangleGraph[i])[j] / N;
            let ellipse2X = 250 + radius * cos(theta2);
            let ellipse2Y = 250 + radius * sin(theta2);

            // let centerX = (ellipse1X + ellipse2X) / 2
            // let centerY = (ellipse1Y + ellipse2Y) / 2
            // let radius = pow(pow(ellipse2X - ellipse1X, 2) + pow(ellipse2Y - ellipse1Y, 2), 1/2)

            // Link for calculating the center of the hyperbolic arc between two points
            // https://math.stackexchange.com/questions/1503466/algebraic-solutions-for-poincar%C3%A9-disk-arcs
            // let centerX = ellipse2Y * (pow(ellipse1X, 2) + pow(ellipse1Y, 2) + 1) - ellipse1Y * (pow(ellipse2X, 2) + pow(ellipse2Y, 2) + 1) / (2 * (ellipse1X * ellipse2Y - ellipse1Y * ellipse2X))
            // let centerY = -ellipse2X * (pow(ellipse1X, 2) + pow(ellipse1Y, 2) + 1) + ellipse1X * (pow(ellipse2X, 2) + pow(ellipse2Y, 2) + 1) / (2 * (ellipse1X * ellipse2Y - ellipse1Y * ellipse2X))
            // let radius = pow(pow(centerX, 2) + pow(centerY, 2) - 1, 1/2)

            // Link for calculating the hyperbolic arc between two angles
            // https://mathworld.wolfram.com/PoincareHyperbolicDisk.html
            
            let theta = (theta1 + theta2) / 2
            let dtheta = abs(theta1 - theta2) / 2
            let r = radius * tan(dtheta)
            let R = radius / cos(dtheta)
            let centerX = 250 + R * cos(theta)
            let centerY = 250 + R * sin(theta)
            let phi = asin(cos(dtheta))
            let gamma = PI - PI/2 + max(theta1, theta2)
            
            strokeWeight(1)
            stroke(200)
            if (i == selected || pow(mouseX - ellipse1X, 2) + pow(mouseY - ellipse1Y, 2) < 100){
                strokeWeight(3)
                stroke(colors[i][0], colors[i][1], colors[i][2])
                ellipse(centerX, centerY, 3,)
            }
            noFill()
            // ellipse(centerX, centerY, 3, 3)
            arc(centerX, centerY, 2*r, 2*r, gamma, gamma + 2*phi)
            // line(ellipse1X, ellipse1Y, ellipse2X, ellipse2Y)
        }
    }

    // Draw nodes of automatic structure
    strokeWeight(1)
    for(let i = 0; i < N; i++){
        let theta = TWO_PI * i / N;
        let ellipseX = 250 + radius * cos(theta);
        let ellipseY = 250 + radius * sin(theta);

        stroke(colors[i][0], colors[i][1], colors[i][2])
        noFill()
        if (i == selected || pow(mouseX - ellipseX, 2) + pow(mouseY - ellipseY, 2) < 100){
            fill(colors[i][0], colors[i][1], colors[i][2])
        }
        ellipse(ellipseX, ellipseY, 20, 20);
    }

    // Draw intervals
    for(let i = 0; i < N; i++){
        let intervalHeight = 50 + i * (height-100) / (N - 1);
        stroke(200)
        strokeWeight(1)
        line(width/2 + 50, intervalHeight, width, intervalHeight)
        
        intervals[i].draw(intervalHeight);
        // let image = intervals[i].getImage(triangleGraph[0][1]);
        // image.draw(intervalHeight)

    }
}

function mousePressed(){
    for(let i = 0; i < N; i++){
        let theta = TWO_PI * i / N;
        let ellipseX = 250 + radius * cos(theta);
        let ellipseY = 250 + radius * sin(theta);

        if (pow(mouseX - ellipseX, 2) + pow(mouseY - ellipseY, 2) < 100){
            selected = i
            break
        } else {
            selected = -1
        }
    }
    
}

function mouseReleased(){
    pressing = false
}