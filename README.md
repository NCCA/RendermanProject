# Renderman Lookdev Project Hour 3

A very frustrating hour, managed to get a basic setup for testing shaders and wanted to get basic displacement working but it's not going yet. Will continue next time.

![](writeupImages/shaderTest.png)


## Test scene

```
plate=ri.ObjectBegin()
ri.Polygon({ 'P' : [-1 , 1 , 0, 
                      1 , 1 , 0, 
                      1,  -1.4 , 0, 
                    -1,  -1.4 , 0
                    ]})
ri.ObjectEnd()
ri.Attribute( 'user' , {'string __materialid' : ['mainplate'] })
# top left front  
ri.TransformBegin()
ri.Scale(0.5,0.5,0.5)
ri.Translate(-1,1.2,0)
ri.ObjectInstance(plate)
ri.TransformEnd()
# top right flat 45
ri.TransformBegin()
ri.Scale(0.5,0.5,0.5)
ri.Translate(1,1.2,0)
ri.Rotate(45,1,0,0)
ri.ObjectInstance(plate)
ri.TransformEnd()
# bottom left  
ri.TransformBegin()
ri.Scale(0.5,0.5,0.5)
ri.Translate(-1,-1.2,0)
ri.Rotate(35,0,1,0)
ri.ObjectInstance(plate)
ri.TransformEnd()
# bottom right
ri.TransformBegin()
ri.Scale(0.5,0.5,0.5)
ri.Translate(1,-1.2,0)
ri.Rotate(-25,0,1,0)
ri.ObjectInstance(plate)
ri.TransformEnd()


ri.AttributeEnd()

```

## Shader

I modified the basic disc shader to work with the displacments so far it's not doing what I wanted.

```
surface rustDisplace (
              float fuzz=0.025,
              float repeatU=1,
              float repeatV=1,
              output float resultF=0,
              output color resultRGB=0)
{
   
    float dist;
    float inDisk;
    float uu=mod(u*repeatU,1);
    float vv=mod(v*repeatV,1);

    dist=sqrt((uu-0.5)*(uu-0.5)+(vv-0.5)*(vv-0.5));
    resultF=1-smoothstep(0.3-fuzz,0.3+fuzz,dist);
    resultRGB=color(resultF);
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
