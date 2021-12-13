# version 400 core

 in vec2 v_texture;

 out vec4 out_color;

 uniform sampler2D s_texture;

 void main(void)
 {
     out_color = texture(s_texture, v_texture);
 }