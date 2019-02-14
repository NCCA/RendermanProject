#!/usr/bin/python
from __future__ import print_function
import prman
import ProcessCommandLine as cl

# Main rendering routine
def main(filename,shadingrate=10,pixelvar=0.1,
         fov=45.0,width=1024,height=720,
         integrator='PxrPathTracer',integratorParams={}
        ) :
  print ('shading rate {} pivel variance {} using {} {}'.format(shadingrate,pixelvar,integrator,integratorParams))
  ri = prman.Ri() # create an instance of the RenderMan interface

  # this is the begining of the rib archive generation we can only
  # make RI calls after this function else we get a core dump
  ri.Begin(filename)
  ri.Option('searchpath', {'string archive':'./assets/:@'})
  ri.Option('searchpath', {'string texture':'../sourceImages/:@'})

  # now we add the display element using the usual elements
  # FILENAME DISPLAY Type Output format
  ri.Display('ferry.exr', 'it', 'rgba')
  ri.Format(width,height,1)

  # setup the raytrace / integrators
  ri.Hider('raytrace' ,{'int incremental' :[1]})
  ri.ShadingRate(shadingrate)
  ri.PixelVariance (pixelvar)
  #ri.Integrator (integrator ,'integrator',integratorParams)
  ri.Option( 'statistics', {'filename'  : [ 'stats.txt' ] } )
  ri.Option( 'statistics', {'endofframe' : [ 1 ] })
  ri.Projection(ri.PERSPECTIVE,{ri.FOV:fov})

  #ri.Rotate(12,1,0,0)
  ri.Translate( 0, 0 ,3.5)


  # now we start our world
  ri.WorldBegin()
  #######################################################################
  #Lighting We need geo to emit light
  #######################################################################
  ri.TransformBegin()
  ri.Rotate(-90,1,0,0)
  ri.Rotate(180,0,0,1)
  ri.Light( 'PxrDomeLight', 'domeLight', { 
            'string lightColorMap'  : 'lightMap.tex'
   })
  ri.TransformEnd()
  #######################################################################
  # end lighting
  #######################################################################

  ri.AttributeBegin()
  ri.Pattern('PxrRamp','plateBase',
  {
    "int rampType" : [1],
    "int tile" : [0],
    "int useNewRamp" : [1],
    "int colorRamp" : [5] ,
    "color[5] colorRamp_Colors" : [1, 1, 1,1 ,0, 0, 1, 1 ,1 ,0 ,0.0228114408, 0.827000022, 1 ,1 ,1],
    "float[5] colorRamp_Knots" : [0.204839006 ,0.258064985, 0.306452006, 0.30806452, 1],
    "string colorRamp_Interpolation" : ["constant"],
  })
  ri.Attribute( 'user' , {'string __materialid' : ['mainplate'] })
  # simple bxdf for now
  ri.Bxdf ('PxrSurface' , 'mainplate', 
  {
      'float diffuseGain' : [0.8],
      'reference color diffuseColor'  :['plateBase:resultRGB']  , 
      'int specularFresnelMode' : [1],
      'color specularEdgeColor' : [1 ,1 ,1],
      'color specularIor' : [4.3696842, 2.916713, 1.654698],
      'color specularExtinctionCoeff' : [0.1, 0.1, 0.1],
      'float specularRoughness' : [0.01], 
      'integer specularModelType' : [1], 
      'string __materialid' : ['mainplate'],
  })
  ri.Polygon({ 'P' : [-1 , 1 , 0, 
                       1 , 1 , 0, 
                       1,  -1.4 , 0, 
                      -1,  -1.4 , 0
                      ]})
  ri.AttributeEnd()


  ri.AttributeBegin()
  ri.Attribute( 'user' , {'string __materialid' : ['portHole'] })
  # simple bxdf for now
  ri.Bxdf ('PxrSurface' , 'portHole', 
  {
      'color diffuseColor'  : [0.8 ,0.0, 0.0] , 
         'float diffuseGain' : [0.8],
      'int specularFresnelMode' : [1],
      'color specularEdgeColor' : [1 ,1 ,1],
      'color specularIor' : [4.3696842, 2.916713, 1.654698],
      'color specularExtinctionCoeff' : [0.1, 0.1, 0.1],
      'float specularRoughness' : [0.01], 
      'integer specularModelType' : [1], 

      'string __materialid' : ['portHole']
  })
  ri.TransformBegin()
  ri.Translate(0.2 ,-0.3,0)
  ri.Torus(0.2,0.05,180,360,360)
  ri.TransformEnd()





  ri.AttributeEnd()


  
  # end our world
  ri.WorldEnd()
  # and finally end the rib file
  ri.End()




if __name__ == '__main__':  
  cl.ProcessCommandLine('testScenes.rib')
  main(cl.filename,cl.args.shadingrate,cl.args.pixelvar,cl.args.fov,cl.args.width,cl.args.height,cl.integrator,cl.integratorParams)

