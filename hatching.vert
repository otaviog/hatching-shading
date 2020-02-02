#version 420

layout (location = 0) in vec4 in_position;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec2 in_texcoord;

uniform int NumTones;

uniform mat4 Modelview;
uniform mat4 ProjectionModelview;
uniform mat3 NormalModelview;

out VertexOut {
  vec3 pos;
  vec3 normal;
  vec2 tex_coord;  
} vout;


void main() {
  gl_Position = ProjectionModelview*in_position;

  vout.pos = (Modelview*in_position).xyz;
  vout.normal = NormalModelview*in_normal;
  vout.tex_coord = in_texcoord;
}
