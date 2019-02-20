# Renderman Lookdev Project Hour 5

Today started work on the stripes shader for the salt stripes (see Detail 3)
![](writeupImages/shaderTest.png)

The plan is to use this as a layer and add to the top of the base scene. Going to attempt this tomorrow. For now the basic shader still needs lots of work but gives the start point.



## Shader
```
float pulse (float a,float b,float fuzz,float x)
{
    return (smoothstep((a)-(fuzz), (a), (x)) - smoothstep((b)-(fuzz), (b), (x)));
}


float stripe(point Pos ,int Number,float uu, float vv)
{
  float Fac = 0;
  float x = mod(Pos[0]+cos(noise("perlin",v)*sin(noise(v))),1);
  int i;
	
  for(i=1; i <= Number; i++)
	{
    if( x < (float)i/Number )
		{
      Fac = i % 2;
      break;
    }
  }
	return Fac;
}

shader stripes(
 color C1 = color(1,0,0),
 color C2 = color(0,0,1),
 float begin=0.3,
 float end=0.6,
 float repeat=8,
 float fuzzy = 0.2,
 output	color Cout=0 

)
{
float uu=fmod(u*repeat,1.0);
float vv=fmod(v*repeat,1.0);
point pos=transform("world","shader",P);
Cout=mix(C1,C2,stripe(pos,22,uu,vv));
}

```



# More reference.

Most of today has been about taking reference images and analyzing them for designing the shading networks I need.

As it was a sunny day I decided to take a quick panoram using my iPhone to use for the image map, whilst this is not ideal it is HDRI and allows a quick mock up of the lighting. 

I converted it using ```txmake -envlatl lightMap.exr  lightMap.tx``` and it produced this image

![](writeupImages/lightMap.jpg)

The following list shows some more reference and ideas about what I need to do to generate it. This will form the basis of the next few iterations.

## Detail 1
![](writeupImages/Detail1.png)

This first images show the different layers on the white section, you can see that some of the paint is gloss whilst other is matte so we need to change these (shiny) parameters. Also notice the displacement and holes in some areas, this is on the base metal so we need to simulate some form of displacement then pass this through all layers.

## Detail 2

![](writeupImages/Detail2.png)

This image shows holes in the surface a lot better, these are quite deep depressions with quite sharp edges so they can be generated via a displacement shader or a map. You can now also see the paint flecks which are the topmost level, these are quite matte so can be added using a procedural process and perhaps a simple diffuse shader.

We can also see the effects of the streaks and what I assume is salt spray / water on the surface. Again this can be added as a layer. Also transition between paint layers is quite rough so need to add noise for this.


## Detail 3

![](writeupImages/Detail3.png)

Note as it is bright today we have a definite Fresnel effect going on so we need to think how the glossy elements work. 

## Detail 4/5

![](writeupImages/Detail4.png)
![](writeupImages/Detail5.png)

There is a lot of deformation on the surface with the paint being very think and not drying correctly, this needs to be added using either normal maps or other procedural means, need to test.

Also note how the paint flecks mix.

## Detail 6

![](writeupImages/Detail6.png)

A closer look at the streaks, this can be produced with a simple line / noise shader then mixed with the other layers.

## Detail 7
![](writeupImages/Detail7.png)
![](writeupImages/Detail8.png)
![](writeupImages/Detail9.png)
![](writeupImages/Detail10.png)

The rest of the images are for reference but will feed into the overall design.

This is the end of Hour 2
