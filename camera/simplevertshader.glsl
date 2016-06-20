
attribute vec4 vertex;
uniform vec2 offset;
uniform vec2 scale;
uniform float rot;
varying vec2 tcoord;
void main(void) 
{
	vec4 pos = vertex;
	tcoord.xy = pos.xy;
	pos.xy = pos.xy*scale+offset;
	gl_Position = pos;
	mat4 RotationMatrix = mat4( cos(rot), -sin(rot), 0.0, 0.0,
                              sin(rot),  cos(rot), 0.0, 0.0,
                              0.0,           0.0, 1.0, 0.0,
                              0.0,           0.0, 0.0, 1.0 );
	gl_Position = RotationMatrix * gl_Position;
}
