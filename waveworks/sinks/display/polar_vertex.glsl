#version 120
attribute vec3 a_position;
void main (void) {
    gl_Position = vec4(a_position, 1.0);
    gl_PointSize = 3840.0;
}

 