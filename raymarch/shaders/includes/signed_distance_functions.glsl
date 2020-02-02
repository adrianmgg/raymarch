#ifndef SIGNED_DISTANCE_FUNCTIONS
#define SIGNED_DISTANCE_FUNCTIONS

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

#endif