#version 420

uniform int NumTones;
uniform vec3 LightPos;

uniform vec3 LightAmbient;
uniform vec3 LightDiffuse;
uniform vec3 Ambient;
uniform vec3 Diffuse;

uniform sampler2D hatches[6];

in VertexOut {
  vec3 pos;
  vec3 normal;
  vec2 tex_coord;
} vin;

vec3 ComputeHatchingLight(vec3 normal_vec, vec3 light_vec,
						  vec2 tex_coord, int num_tones) {
  float diffuse_factor = max(dot(normal_vec, light_vec), 0.0);
  float hatching_amount = max(num_tones - diffuse_factor*num_tones, 0);
  
  int hatch_tex_a = int(hatching_amount);
  int hatch_tex_b = int(ceil(hatching_amount));
  float t = hatching_amount - floor(hatching_amount);
  
  vec3 hc1 = texture2D(hatches[hatch_tex_a], tex_coord.xy).xyz;
  vec3 hc2 = texture2D(hatches[hatch_tex_b], tex_coord.xy).xyz;
  
  vec3 hatch_color = hc1*(1.0 - t) + hc2*t;

  
  float diffuse_tone = floor(diffuse_factor*float(num_tones))/float(num_tones);
  
  return (Ambient*hatch_color + Diffuse.xyz*diffuse_tone);
}

out vec4 frag_color;

void main() {
  vec3 light_vec = normalize(LightPos - vin.pos);
  vec3 hatch_color = ComputeHatchingLight(vin.normal, light_vec,
										  vin.tex_coord,
										  NumTones);
  frag_color = vec4(hatch_color, 1.0);
}
