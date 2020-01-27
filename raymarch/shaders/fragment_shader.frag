//#version 330
#version 460
// not sure which version to pick

in vec2 screenspace;
out vec3 f_color;

uniform float time_elapsed;
uniform vec3 camera_position;
uniform mat3x3 camera_rotation_mat;

const float EPSILON = 1e-4;
const int MAX_ITERATIONS = 256;
const int MAX_BOUNCES = 8;

// ---------------- http://iquilezles.org/www/articles/distfunctions/distfunctions.htm

float sphereSDF(vec3 p, float radius){
	return length(p) - radius;
}

float boxSDF(vec3 p, vec3 boxSize){
	vec3 q = abs(p) - boxSize;
	return length(max(q, 0)) + min(max(q.x, max(q.y, q.z)), 0);
}


float opUnion(float d1, float d2) {return min(d1,d2);}
float opSubtraction(float d1, float d2) {return max(-d1,d2);}
float opIntersection(float d1, float d2){return max(d1,d2);}

float opSmoothUnion(float d1, float d2, float k){
    float h = clamp(0.5 + 0.5*(d2-d1)/k, 0.0, 1.0);
    return mix(d2, d1, h) - k*h*(1.0-h);
}
float opSmoothSubtraction(float d1, float d2, float k){
    float h = clamp(0.5 - 0.5*(d2+d1)/k, 0.0, 1.0);
    return mix(d2, -d1, h) + k*h*(1.0-h);
}
float opSmoothIntersection(float d1, float d2, float k){
    float h = clamp(0.5 - 0.5*(d2-d1)/k, 0.0, 1.0);
    return mix(d2, d1, h) + k*h*(1.0-h);
}

vec3 opRep(vec3 p, vec3 c){
    return mod(p+0.5*c,c)-0.5*c;
}
vec3 opRep(vec3 p, float c){
    return mod(p+0.5*c,c)-0.5*c;
}

// ----------------

vec3 closestAxis(vec3 v){
    vec3 v_ = abs(v);
    if(v_.x > v_.y){
        if(v_.z > v_.x) return vec3(0, 0, sign(v.z));
        else return vec3(sign(v.x), 0, 0);
    }
    else{
        if(v_.z > v_.y) return vec3(0, 0, sign(v.z));
        else return vec3(0, sign(v.y), 0);
    }
}

// ----------------

//float worldSDF(vec3 p);
//vec3 worldColor(vec3 p);

// TODO give this a better name
struct WorldSDFHitData{
    vec3 color;
    vec3 normal;
    bool shouldBounce;
};

float worldSDF(vec3 p, out bool hit, out WorldSDFHitData hitData);

void marchWorld(vec3 startPos, vec3 startDirection, out vec3 color){
    vec3 currentPos = startPos;
    vec3 currentDirection = startDirection;
    vec3 colorAddFactor = vec3(1);
    color = vec3(0);
    int numBounces = 0;
    for(int i = 0; i < MAX_ITERATIONS; i++){
        WorldSDFHitData hitData;
        bool hit = false;
        float dist = worldSDF(currentPos, hit, hitData);
        if(hit){
            if(!hitData.shouldBounce){
                color = mix(color, hitData.color, colorAddFactor);
                break;
            }
            else{
                color = mix(color, hitData.color, colorAddFactor);
                colorAddFactor *= .25+normalize(hitData.color)/4;
                currentPos += currentDirection * 2 * -EPSILON;
                currentDirection = reflect(currentDirection, hitData.normal);
                if(++numBounces >= MAX_BOUNCES) break;
            }
        }
        currentPos += currentDirection * dist;
    }
}

const float aspectRatio = 1;

void main() {
    time_elapsed;
    // vec3 cameraSpace = vec3(screenspace, 0) + camera_pos;
    vec3 rayOrigin = camera_position;
    vec3 rayDirecition = camera_rotation_mat * normalize(vec3(screenspace, 1));
//    rayDirecition = (camera_to_world_matrix * vec4(rayDirecition, 1)).xyz;
    vec3 worldColor;
    marchWorld(rayOrigin, rayDirecition, worldColor);
    f_color = worldColor;
}

float worldSDF(vec3 p, out bool hit, out WorldSDFHitData hitData){
    float minDistance = 1.0e32; // TODO figure out how to get infinity, make that a #defined constant
    { // ground plane
        float currentDistance = p.y + 4;
        if(hit = currentDistance <= EPSILON){
            hitData.normal = vec3(0, 1, 0);
            hitData.color = mix(vec3(.2, 1, 1), vec3(.2, .2, 1), sin(p.x * 2) > cos(p.z * 2));
            hitData.shouldBounce = true;
            return currentDistance;
        }
        minDistance = min(minDistance, currentDistance);
    }
    { // cube
//        vec3 p_ = p - vec3(-1.5, 0, 4);
//        float currentDistance = boxSDF(p_, vec3(1, 1, 1));
//        if(hit = currentDistance <= EPSILON){
//            hitData.normal = closestAxis(p_);
//            hitData.color = vec3(1, .2, .2);
//            hitData.shouldBounce = true;
//            return currentDistance;
//        }
//        minDistance = min(minDistance, currentDistance);
    }
    { // sphere
        vec3 p_ = opRep(p - vec3(0,-2.5,2), 4);
        float currentDistance = sphereSDF(p_, 1);
        if(hit = currentDistance <= EPSILON){
            hitData.normal = normalize(p_);
            hitData.color = normalize(round(abs(opRep((p-.5)/4, 2)))+EPSILON/*avoid 0 div*/);
            hitData.shouldBounce = true;
        }
        minDistance = min(minDistance, currentDistance);
    }
    // nothing was closest
    return minDistance;
}


/*
#define size 2


vec3 worldColor(vec3 p){
    p -= 1;
    p = abs(opRep(p, size * 10));
    return round(p) / (size * 5);
}

float worldSDF(vec3 p){
    p -= 1;
    p = opRep(p, size);
    float d1 = sphereSDF(p, .25);
    #define r .05
    float d2 = opUnion(opUnion(boxSDF(p, vec3(size,r,r)), boxSDF(p, vec3(r,size,r))), boxSDF(p, vec3(r,r,size)));
    #undef r
    return opSmoothUnion(d1, d2, sin(time_elapsed)/2+.5);
//    return opUnion(d1, d2);
}
*/
