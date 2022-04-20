function det(matrix){
    // Return the determinant of a matrix
    //  Note: currently this only accepts 2x2 NumJs matrices
    return matrix.get(0,0) * matrix.get(1,1) - matrix.get(0,1) * matrix.get(1,0)
}

function rp1ToS1(v){
    // Map a vector v in R^2 - {0} to S1 by the homeomorphism RP1 -> S1
    let x = v[0];
    let y = v[1];

    return nj.array([
        [2*x*y / (x*x + y*y)],
        [(x*x - y*y) / (x*x + y*y)]
    ])
}

function rp1Interval(theta1, theta2){
    // Get a pair of points in RP1 representing the pair of angles theta1, theta2
    //  Note: theta1, theta2 parametrize the double cover of RP1
    return nj.array([
        [cos(theta1), cos(theta2)],
        [sin(theta1), sin(theta2)]
    ])
}

class Interval {
    constructor(a, b, color){
        this.a = a;
        this.b = b;
        this.color = color;
    }

    draw(intervalHeight){
        // Draw the interval to the canvas at a specified height
        stroke(this.color[0], this.color[1], this.color[2])
        strokeWeight(7)
        line(width/2 + 50, intervalHeight, width/2 + 50 + this.b - this.a, intervalHeight)
    }

    getImage(matrix){
        // Get the image of the interval under an action in SL(2,R)
        //  Return the image as an Interval object
        let temp = matrix * rp1Interval(this.a % PI, this.b % PI)
        let x = temp[0];
        let y = temp[1];

        console.log('det is', det(matrix))
        if (det(matrix) < 0){
            console.log(nj.arctan(y, x))
            let temp2 = nj.arctan(y, x)
            let b = temp2.get(0) % PI;
            let a = temp2.get(1) % PI;
        } else {
            let a = temp2.get(0) % PI;
            let b = temp2.get(1) % PI;
        }

        return new Interval(a, b, this.color)
    }
}
