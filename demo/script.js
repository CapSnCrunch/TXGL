function setup(){
    var cnv = createCanvas(1000, 550);
    cnv.parent('canvas');  
}

let pressing = false
let selected = -1
let radius = 200; // Radius of circle graph sits on
let intervalView = 'line'

// Get the current group along with its associated automatic structure and valid intervals
//  Set the color of each disconnected interval
let graph = cyclicGraph
let intervals = cyclicIntervals
for(let i = 0; i < Object.keys(graph).length; i++){
    intervals[i].color = colors[i]
}

function drawEdge(theta1, theta2, color = 200){
    // Link for calculating the hyperbolic arc between two angles
    // https://mathworld.wolfram.com/PoincareHyperbolicDisk.html
    let theta = (theta1 + theta2) / 2
    let dtheta = abs(theta1 - theta2) / 2
    let r = radius * tan(dtheta)
    let R = radius / cos(dtheta)
    let centerX = 250 + R * cos(theta)
    let centerY = 250 + R * sin(theta)
    let phi = asin(cos(dtheta))
    
    strokeWeight(1)
    stroke(200)
    
    if (color != 200){
        strokeWeight(3)
        stroke(color[0], color[1], color[2])
    }

    noFill()
    if (phi > 0){
        let gamma = PI - PI/2 + max(theta1, theta2)
        arc(centerX, centerY, 2*r, 2*r, gamma, gamma + 2*phi)
    } else {
        let gamma = PI - PI/2 + min(theta1, theta2)
        arc(centerX, centerY, 2*r, 2*r, gamma, gamma - 2*phi)
    }
}

function draw(){
    clear();

    // Draw the edges of graph
    for(let i = 0; i < Object.keys(graph).length; i++){
        for(let j = 0; j < Object.keys(graph[i]).length; j++){
            let theta1 = TWO_PI * i / intervals.length;
            let theta2 = TWO_PI * Object.keys(graph[i])[j] / intervals.length;

            let ellipse1X = 250 + radius * cos(theta1);
            let ellipse1Y = 250 + radius * sin(theta1);
            if (pow(mouseX - ellipse1X, 2) + pow(mouseY - ellipse1Y, 2) < 100){
                selected = i
            }

            drawEdge(theta1, theta2)
        }
    }

    // Draw the highlighted edges of the graph
    if (selected != -1){
        for(let j = 0; j < Object.keys(graph[selected]).length; j++){
            let theta1 = TWO_PI * selected / intervals.length;
            let theta2 = TWO_PI * Object.keys(graph[selected])[j] / intervals.length;

            drawEdge(theta1, theta2, intervals[selected].color)
        }
    }

    // Draw the nodes of the graph
    selected = -1
    for(let i = 0; i < intervals.length; i++){
        let theta = TWO_PI * i / intervals.length;
        let ellipseX = 250 + radius * cos(theta);
        let ellipseY = 250 + radius * sin(theta);
        
        fill(255)
        strokeWeight(2)
        stroke(colors[i][0], colors[i][1], colors[i][2])
        if (i == selected || pow(mouseX - ellipseX, 2) + pow(mouseY - ellipseY, 2) < 100){
            fill(colors[i][0], colors[i][1], colors[i][2])
            selected = i
        }
        ellipse(ellipseX, ellipseY, 25, 25);
    }

    // Draw the intervals depending on view
    if (intervalView == 'line'){
        // Draw intervals (line version)
        for(let i = 0; i < intervals.length; i++){
            let intervalHeight = 50 + i * (height-150) / (intervals.length - 1);
            intervals[i].drawLine(intervalHeight, selected == i)

            // let image = intervals[i].getImage(graph[0][1])
            // image.draw(intervalHeight)
        }
    } else {
        // Draw intervals (arc version)
        noFill()
        stroke(200)
        strokeWeight(1)
        ellipse(width - 250, 250, 2 * radius, 2 * radius)
        for(let i = 0; i < intervals.length; i++){
            stroke(200)
            strokeWeight(1)
            if (selected == - 1 || selected == i){
                intervals[i].drawArc([width - 250, 250], radius, selected == i)
            }
        }
    }

    // Draw the buttons for switching the graph
    fill(255)
    strokeWeight(2)
    stroke(230)
    rect(130, height - 75, 80, 50, 5)
    rect(230, height - 75, 80, 50, 5)
    rect(330, height - 75, 80, 50, 5)

    // Draw the buttons for switching the interval view
    fill(255)
    strokeWeight(2)
    stroke(230)
    rect(width/2 + 100, height - 75, 130, 50, 5)
    rect(width/2 + 280, height - 75, 130, 50, 5)
    
}

function mousePressed(){
    // for(let i = 0; i < N; i++){
    //     let theta = TWO_PI * i / N;
    //     let ellipseX = 250 + radius * cos(theta);
    //     let ellipseY = 250 + radius * sin(theta);

    //     if (pow(mouseX - ellipseX, 2) + pow(mouseY - ellipseY, 2) < 100){
    //         selected = i
    //         break
    //     } else {
    //         selected = -1
    //     }
    // }

    // Buttons for switching 
    if (130 < mouseX && mouseX < 210 && height - 75 < mouseY && mouseY < height - 25){
        graph = cyclicGraph
        intervals = cyclicIntervals
    }
    if (230 < mouseX && mouseX < 310 && height - 75 < mouseY && mouseY < height - 25){
        graph = triangleGraph
        intervals = triangleIntervals
    }
    if (330 < mouseX && mouseX < 410 && height - 75 < mouseY && mouseY < height - 25){
        graph = surfaceGraph
        intervals = surfaceIntervals
    }

    // Buttons for switching interval view
    if (width/2 + 100 < mouseX && mouseX < width/2 + 230 && height - 75 < mouseY && mouseY < height - 25){
        intervalView = 'circle'
    }
    if (width/2 + 280 < mouseX && mouseX < width/2 + 360 && height - 75 < mouseY && mouseY < height - 25){
        intervalView = 'line'
    }
    
}

function mouseReleased(){
    pressing = false
}